package org.medicare.reminder;

import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;

/**
 * Читает план напоминаний alarms.json (его пишет Python, см. alarm_plan.py), показывает
 * наступившие уведомления и ставит системный будильник на ближайшую запись.
 *
 * Время, тексты и правила (тихие часы, принятые дозы) уже учтены в плане, здесь их нет.
 * Используется setAlarmClock: он точный, не засыпает в Doze и не требует особого разрешения.
 */
public final class ReminderCore {
    private static final String TAG = "MediCareReminder";
    static final String ACTION_FIRE = "org.medicare.reminder.FIRE";
    private static final String PREFS = "medicare_reminder";
    private static final String PLAN_FILE = "alarms.json";
    private static final String BEAT_FILE = "foreground.beat";
    /** Записи старше этого срока не показываем (телефон был выключен, это уже неактуально). */
    private static final long STALE_MS = 90L * 60L * 1000L;
    /** Приложение считается открытым, если отметка свежее этого срока. */
    private static final long FOREGROUND_MS = 45L * 1000L;

    private ReminderCore() {}

    /** Показать наступившее и поставить следующий будильник (вызов из приёмников). */
    public static void run(Context ctx) {
        try {
            JSONObject plan = readPlan(ctx);
            if (plan == null) {
                return;
            }
            long now = System.currentTimeMillis();
            showDue(ctx, plan, now);
            scheduleNext(ctx, plan, now);
        } catch (Throwable t) {
            Log.e(TAG, "run failed", t);
        }
    }

    /** Только поставить следующий будильник (вызывает Python после записи нового плана). */
    public static void schedule(Context ctx) {
        try {
            JSONObject plan = readPlan(ctx);
            if (plan != null) {
                scheduleNext(ctx, plan, System.currentTimeMillis());
            }
        } catch (Throwable t) {
            Log.e(TAG, "schedule failed", t);
        }
    }

    /** Снять будильник (напоминания выключены или план пуст). */
    public static void cancel(Context ctx) {
        try {
            AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
            am.cancel(firePending(ctx));
        } catch (Throwable t) {
            Log.e(TAG, "cancel failed", t);
        }
    }

    // ---------------------------------------------------------------- план

    private static JSONObject readPlan(Context ctx) throws Exception {
        File file = new File(ctx.getFilesDir(), PLAN_FILE);
        if (!file.exists()) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        try (BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF-8"))) {
            String line;
            while ((line = r.readLine()) != null) {
                sb.append(line).append('\n');
            }
        }
        return new JSONObject(sb.toString());
    }

    private static boolean appInForeground(Context ctx, long now) {
        try {
            File file = new File(ctx.getFilesDir(), BEAT_FILE);
            if (!file.exists()) {
                return false;
            }
            StringBuilder sb = new StringBuilder();
            try (BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF-8"))) {
                String line = r.readLine();
                if (line != null) {
                    sb.append(line.trim());
                }
            }
            long beat = Long.parseLong(sb.toString());
            return beat > 0 && now - beat >= 0 && now - beat < FOREGROUND_MS;
        } catch (Throwable t) {
            return false;
        }
    }

    // ---------------------------------------------------------------- показ

    private static void showDue(Context ctx, JSONObject plan, long now) throws Exception {
        SharedPreferences sp = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        long last = sp.getLong("last_shown", 0L);
        long newest = last;
        boolean foreground = appInForeground(ctx, now);
        JSONArray alarms = plan.optJSONArray("alarms");
        if (alarms == null) {
            return;
        }
        for (int i = 0; i < alarms.length(); i++) {
            JSONObject e = alarms.getJSONObject(i);
            long at = e.getLong("at");
            if (at <= last || at > now || now - at > STALE_MS) {
                continue;
            }
            if (at > newest) {
                newest = at;
            }
            if (foreground) {
                continue; // приложение открыто: оно само покажет окно напоминания
            }
            notify(ctx, plan, e);
        }
        if (newest != last) {
            sp.edit().putLong("last_shown", newest).apply();
        }
    }

    private static void notify(Context ctx, JSONObject plan, JSONObject e) {
        boolean sound = plan.optBoolean("sound", true);
        boolean vibrate = plan.optBoolean("vibrate", true);
        String channelId = "medicare_doses_" + (sound ? "s" : "q") + (vibrate ? "v" : "n");
        NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm.getNotificationChannel(channelId) == null) {
            NotificationChannel ch = new NotificationChannel(
                    channelId, plan.optString("channel_name", "MediCare"), NotificationManager.IMPORTANCE_HIGH);
            ch.enableVibration(vibrate);
            if (!sound) {
                ch.setSound(null, null);
            }
            ch.setLockscreenVisibility(Notification.VISIBILITY_PRIVATE);
            nm.createNotificationChannel(ch);
        }
        String title = e.optString("title", "MediCare");
        String text = e.optString("text", "");
        // Маленький значок уведомления должен быть однотонным: цветной значок приложения
        // Android рисует белым квадратом. Берём системный значок напоминания.
        int icon = android.R.drawable.ic_popup_reminder;

        // Что видно на заблокированном экране: без названий лекарств (медицинские данные).
        Notification publicVersion = new Notification.Builder(ctx, channelId)
                .setSmallIcon(icon).setContentTitle(title).build();
        Notification.Builder b = new Notification.Builder(ctx, channelId)
                .setSmallIcon(icon)
                .setContentTitle(title)
                .setContentText(text)
                .setStyle(new Notification.BigTextStyle().bigText(text))
                .setCategory(Notification.CATEGORY_REMINDER)
                .setVisibility(Notification.VISIBILITY_PRIVATE)
                .setPublicVersion(publicVersion)
                .setAutoCancel(true);
        PendingIntent open = launchPending(ctx, 2);
        if (open != null) {
            b.setContentIntent(open);
        }
        nm.notify(e.optString("id", "x").hashCode(), b.build());
    }

    // ---------------------------------------------------------------- будильник

    private static void scheduleNext(Context ctx, JSONObject plan, long now) throws Exception {
        JSONArray alarms = plan.optJSONArray("alarms");
        long next = Long.MAX_VALUE;
        if (alarms != null) {
            for (int i = 0; i < alarms.length(); i++) {
                long at = alarms.getJSONObject(i).getLong("at");
                if (at > now && at < next) {
                    next = at;
                }
            }
        }
        AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
        if (next == Long.MAX_VALUE) {
            am.cancel(firePending(ctx));
            return;
        }
        PendingIntent show = launchPending(ctx, 1);
        if (show == null) {
            return;
        }
        am.setAlarmClock(new AlarmManager.AlarmClockInfo(next, show), firePending(ctx));
    }

    private static PendingIntent firePending(Context ctx) {
        Intent i = new Intent(ctx, ReminderReceiver.class).setAction(ACTION_FIRE);
        return PendingIntent.getBroadcast(ctx, 0, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    private static PendingIntent launchPending(Context ctx, int requestCode) {
        Intent launch = ctx.getPackageManager().getLaunchIntentForPackage(ctx.getPackageName());
        if (launch == null) {
            return null;
        }
        return PendingIntent.getActivity(ctx, requestCode, launch,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }
}
