# -*- coding: utf-8 -*-
"""Защищённое хранение небольших секретов (токен сервера, идентификатор установки).

Почему отдельно от medicare.json: сервер выдаёт токен любому, кто назвал install_id, поэтому
install_id фактически равен паролю. Лежать открытым текстом рядом с расписанием он не должен.

Android: ключ AES-256 создаётся и остаётся внутри Android Keystore (из приложения его
не достать, он привязан к устройству); секреты шифруются AES-GCM, на диск попадает только шифртекст.
Если Keystore не работает, секрет НЕ пишется на диск: он живёт только в памяти до закрытия
приложения (чат продолжит работать, но устройство зарегистрируется заново).

Компьютер (разработка): шифрования нет — файл с правами 0600. Для боевых данных не использовать.
"""
import base64
import importlib
import json
import os
import tempfile

_ALIAS = "medicare_secrets_v1"
_FILE = "secrets.bin"


class SecureStoreError(Exception):
    pass


def _to_jbytes(data):
    """bytes -> список знаковых байт, который pyjnius принимает как byte[]."""
    return [b - 256 if b > 127 else b for b in data]


def _from_jbytes(arr):
    if isinstance(arr, (bytes, bytearray)):
        return bytes(arr)
    return bytes((x & 0xFF) for x in arr)


class AndroidKeystoreBackend:
    """AES-256-GCM, ключ в AndroidKeyStore. Формат шифртекста: iv(12) + данные + тег."""

    encrypts = True

    def __init__(self):
        jnius = importlib.import_module("jnius")
        self._auto = jnius.autoclass
        self._ks = self._auto("java.security.KeyStore").getInstance("AndroidKeyStore")
        self._ks.load(None)
        if not self._ks.containsAlias(_ALIAS):
            self._create_key()

    def _create_key(self):
        auto = self._auto
        props = auto("android.security.keystore.KeyProperties")
        builder = auto("android.security.keystore.KeyGenParameterSpec$Builder")(
            _ALIAS, props.PURPOSE_ENCRYPT | props.PURPOSE_DECRYPT)
        builder = builder.setBlockModes([props.BLOCK_MODE_GCM])
        builder = builder.setEncryptionPaddings([props.ENCRYPTION_PADDING_NONE])
        builder = builder.setKeySize(256)
        gen = auto("javax.crypto.KeyGenerator").getInstance(props.KEY_ALGORITHM_AES, "AndroidKeyStore")
        gen.init(builder.build())
        gen.generateKey()

    def _cipher(self, mode, iv=None):
        auto = self._auto
        cipher_cls = auto("javax.crypto.Cipher")
        cipher = cipher_cls.getInstance("AES/GCM/NoPadding")
        key = self._ks.getKey(_ALIAS, None)
        if mode == "enc":
            cipher.init(cipher_cls.ENCRYPT_MODE, key)
        else:
            spec = auto("javax.crypto.spec.GCMParameterSpec")(128, _to_jbytes(iv))
            cipher.init(cipher_cls.DECRYPT_MODE, key, spec)
        return cipher

    def encrypt(self, plain):
        cipher = self._cipher("enc")
        iv = _from_jbytes(cipher.getIV())
        return iv + _from_jbytes(cipher.doFinal(_to_jbytes(plain)))

    def decrypt(self, blob):
        iv, body = blob[:12], blob[12:]
        return _from_jbytes(self._cipher("dec", iv).doFinal(_to_jbytes(body)))


class PlainFileBackend:
    """Только для разработки на компьютере: без шифрования."""

    encrypts = False

    def encrypt(self, plain):
        return plain

    def decrypt(self, blob):
        return blob


class MemoryOnlyBackend:
    """Запасной вариант, если Keystore сломан: на диск ничего не пишется."""

    encrypts = True
    memory_only = True

    def encrypt(self, plain):
        raise SecureStoreError("memory only")

    decrypt = encrypt


def default_backend():
    from kivy.utils import platform
    if platform == "android":
        try:
            return AndroidKeystoreBackend()
        except Exception as exc:                      # Keystore бывает сломан на редких прошивках
            print("keystore unavailable, secrets stay in memory:", exc)
            return MemoryOnlyBackend()
    return PlainFileBackend()


class SecureStore:
    def __init__(self, directory, backend=None):
        self.path = os.path.join(directory, _FILE)
        self.backend = backend or default_backend()
        self._cache = {}
        self._memory_only = bool(getattr(self.backend, "memory_only", False))
        self._loaded = False

    # -- файл ---------------------------------------------------------------
    def _load(self):
        if self._loaded:
            return
        self._loaded = True
        if self._memory_only:
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if not isinstance(raw, dict):
                raise ValueError("bad format")
        except FileNotFoundError:
            return
        except Exception as exc:
            print("secrets file unreadable, starting empty:", exc)
            self._discard_file()
            return
        for name, value in raw.items():
            try:
                self._cache[name] = self.backend.decrypt(base64.b64decode(value)).decode("utf-8")
            except Exception:
                # ключ мог пропасть (сброс экрана блокировки, смена прошивки): секрет просто «забываем»
                continue

    def _discard_file(self):
        try:
            os.remove(self.path)
        except OSError:
            pass

    def _flush(self):
        if self._memory_only:
            return
        directory = os.path.dirname(self.path) or "."
        os.makedirs(directory, exist_ok=True)
        payload = {n: base64.b64encode(self.backend.encrypt(v.encode("utf-8"))).decode("ascii")
                   for n, v in self._cache.items()}
        fd, tmp = tempfile.mkstemp(prefix=".sec-", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(payload, f)
                f.flush()
                os.fsync(f.fileno())
            try:
                os.chmod(tmp, 0o600)
            except OSError:
                pass
            os.replace(tmp, self.path)
        except Exception:
            try:
                os.remove(tmp)
            except OSError:
                pass
            raise

    # -- публичный интерфейс --------------------------------------------------
    def get(self, name):
        self._load()
        return self._cache.get(name)

    def set(self, name, value):
        self._load()
        if not isinstance(value, str):
            raise TypeError("secret must be str")
        self._cache[name] = value
        try:
            self._flush()
        except Exception as exc:
            # не удалось зашифровать/записать: оставляем только в памяти, но не пишем открытым текстом
            print("secret not persisted:", exc)
            self._memory_only = True

    def delete(self, name):
        self._load()
        self._cache.pop(name, None)
        try:
            self._flush()
        except Exception as exc:
            print("secret delete flush failed:", exc)

    def clear(self):
        self._load()
        self._cache.clear()
        self._discard_file()

    @property
    def persistent(self):
        return not self._memory_only
