# -*- coding: utf-8 -*-
"""Показывает разрешения, receiver'ы и targetSdk из готового APK (без Android SDK).

Запуск:  python tools/apk_manifest.py bin/medicare-1.0-...-debug.apk
Нужно, чтобы убедиться, что в сборку попали INTERNET, уведомления и будильники.
"""
import struct
import sys
import zipfile


def parse(data):
    u16 = lambda o: struct.unpack_from("<H", data, o)[0]
    _, hsz, psize, scnt, _st, flags, sstart, _t = struct.unpack_from("<HHIIIIII", data, 8)
    utf8 = bool(flags & 0x100)
    offs = struct.unpack_from("<%dI" % scnt, data, 8 + hsz)
    strs = []
    for o in offs:
        p = 8 + sstart + o
        if utf8:
            p += 1 if not data[p] & 0x80 else 2
            n = data[p]; p += 1
            if n & 0x80:
                n = ((n & 0x7F) << 8) | data[p]; p += 1
            strs.append(data[p:p + n].decode("utf8", "replace"))
        else:
            n = u16(p); p += 2
            strs.append(data[p:p + n * 2].decode("utf16", "replace"))
    pos = 8 + psize
    out = []
    while pos < len(data):
        t, _h, sz = struct.unpack_from("<HHI", data, pos)
        if t == 0x102:
            _ns, name, _s, _asz, cnt = struct.unpack_from("<iiHHH", data, pos + 16)
            attrs = {}
            for i in range(cnt):
                _a, an, araw, _sz, _r, at, ad = struct.unpack_from("<iiiHBBi", data, pos + 36 + i * 20)
                attrs[strs[an]] = strs[araw] if araw != -1 else (strs[ad] if at == 3 else (bool(ad) if at == 0x12 else ad))
            out.append((strs[name], attrs))
        pos += sz
    return out


def main(path):
    with zipfile.ZipFile(path) as z:
        items = parse(z.read("AndroidManifest.xml"))
    perms = [a.get("name") for n, a in items if n == "uses-permission"]
    recv = [a.get("name") for n, a in items if n == "receiver"]
    sdk = [a for n, a in items if n == "uses-sdk"]
    app = [a for n, a in items if n == "application"]
    print("targetSdk:", sdk[0].get("targetSdkVersion") if sdk else "?")
    print("allowBackup:", app[0].get("allowBackup") if app else "?")
    print("permissions:", perms or "НЕТ")
    print("receivers:", recv or "НЕТ")
    need = ["android.permission.INTERNET", "android.permission.POST_NOTIFICATIONS",
            "android.permission.RECEIVE_BOOT_COMPLETED"]
    missing = [p for p in need if p not in perms]
    if missing:
        print("ВНИМАНИЕ, нет разрешений:", missing)
    if not any(r and r.endswith("AlarmReceiver") for r in recv):
        print("ВНИМАНИЕ: AlarmReceiver не зарегистрирован — фоновые напоминания не заработают")


if __name__ == "__main__":
    main(sys.argv[1])
