"""Pure foreground reminder scheduling, independent of the Kivy UI."""
import datetime as dt
import core


class ReminderScheduler:
    def __init__(self):
        self.fired = set()
        self.snoozed = {}
        self.day = None

    def snooze(self, key, now, minutes=10):
        self.snoozed[key] = now + dt.timedelta(minutes=minutes)

    def due(self, data, now):
        if self.day != now.date():
            self.fired.clear()
            self.day = now.date()
        notif = data.get("notif", {})
        if not notif.get("all", True) or (notif.get("quiet") and core.in_quiet(now)):
            return []
        result = []
        valid = set()
        for tm, med in core.doses_for(data, now.date()):
            key = "%s|%s" % (now.date().isoformat(), core.key_of(med, tm))
            valid.add(key)
            if core.is_taken(data, now.date(), med, tm):
                self.snoozed.pop(key, None)
                continue
            due = dt.datetime.combine(now.date(), dt.time.fromisoformat(tm), tzinfo=now.tzinfo)
            delayed = self.snoozed.get(key)
            ready = (delayed is not None and now >= delayed)
            # Catch missed polling ticks/resume within 60 minutes, never send
            # repeated missed-dose alerts or imply that taking late is safe.
            ready |= delayed is None and key not in self.fired and due <= now < due + dt.timedelta(hours=1)
            if ready:
                self.fired.add(key)
                self.snoozed.pop(key, None)
                result.append((now.date(), med, tm, key))
        self.snoozed = {k: v for k, v in self.snoozed.items() if k in valid}
        return result