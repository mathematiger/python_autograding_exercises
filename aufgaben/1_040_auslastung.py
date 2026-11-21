"""Aufgabe 1_040 – Auslastung                                    Stufe 1 ★☆☆☆☆

Ein Monitoring-Programm misst jede Minute die CPU-Auslastung eines
Servers in Prozent. Liegt ein Messwert über der Alarmgrenze, soll die
Zeile dieser Minute als ALARM markiert werden, damit die Bereitschaft
sie sofort sieht. Ein Wert genau auf der Grenze ist noch kein Alarm.

Das Programm unten ist vorgegeben: Es fragt nach der Alarmgrenze, liest
Messwerte, bis stop eingegeben wird, gibt für jede Minute eine Zeile
aus und zum Schluss, wie viele Alarme es gab. Schreiben Sie oben die
drei Funktionen, die es benutzt:

- ist_alarm(wert, grenze) gibt True zurück, wenn wert größer als grenze
  ist, sonst False.
- statuszeile(minute, wert, grenze) gibt einen Text wie
  "Minute 2: 92 % ALARM" zurück, bei einem Wert ohne Alarm einen wie
  "Minute 1: 45 % ok". Benutzen Sie dafür ist_alarm.
- anzahl_alarme(werte, grenze) bekommt eine Liste von Messwerten und
  gibt zurück, wie viele davon über der Grenze liegen. Gehen Sie die
  Liste mit for durch und benutzen Sie wieder ist_alarm.

Bei der Grenze 80 und den Messwerten 45, 92, 80, 81 und dann stop:

    Minute 1: 45 % ok
    Minute 2: 92 % ALARM
    Minute 3: 80 % ok
    Minute 4: 81 % ALARM
    Alarme: 2 von 4

Grenzen: Die Alarmgrenze und alle Messwerte sind ganze Zahlen von 0 bis
100. Es gibt 0 bis 60 Messwerte, danach kommt immer genau stop.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Funktionen mit
mehreren Parametern legen Sie mit def fest und geben ihr Ergebnis mit
return zurück (Aufgaben 1_038 und 1_039). Eine Funktion darf in ihrem
Rumpf eine andere aufrufen, so wie hier beschreibung ist_gerade aufruft:

    def ist_gerade(zahl):
        return zahl % 2 == 0

    def beschreibung(zahl):
        if ist_gerade(zahl):
            return f"{zahl} ist gerade"
        return f"{zahl} ist ungerade"

Ein Vergleich wie wert > grenze ist selbst schon True oder False (Aufgabe
1_016); return wert > grenze gibt dieses Ergebnis direkt zurück. Wie man
in einer for-Schleife über eine Liste mitzählt, steht in den Aufgaben
1_025 und 1_028.
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


grenze = int(input("Alarmgrenze in Prozent: "))
werte = []
eingabe = input("Auslastung in Prozent (stop zum Beenden): ")
while eingabe != "stop":
    werte.append(int(eingabe))
    eingabe = input("Auslastung in Prozent (stop zum Beenden): ")

for nummer in range(len(werte)):
    print(statuszeile(nummer + 1, werte[nummer], grenze))
print(f"Alarme: {anzahl_alarme(werte, grenze)} von {len(werte)}")
