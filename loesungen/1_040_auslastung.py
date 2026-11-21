# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_040_auslastung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_040_auslastung

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

def ist_alarm(wert, grenze):
    """Gibt True zurück, wenn der Messwert über der Grenze liegt."""
    return wert > grenze


def statuszeile(minute, wert, grenze):
    """Gibt die Zeile für eine Minute zurück, mit ALARM oder ok am Ende."""
    if ist_alarm(wert, grenze):
        return f"Minute {minute}: {wert} % ALARM"
    return f"Minute {minute}: {wert} % ok"


def anzahl_alarme(werte, grenze):
    """Zählt, wie viele Messwerte über der Grenze liegen."""
    anzahl = 0
    for wert in werte:
        if ist_alarm(wert, grenze):
            anzahl = anzahl + 1
    return anzahl


grenze = int(input("Alarmgrenze in Prozent: "))
werte = []
eingabe = input("Auslastung in Prozent (stop zum Beenden): ")
while eingabe != "stop":
    werte.append(int(eingabe))
    eingabe = input("Auslastung in Prozent (stop zum Beenden): ")

for nummer in range(len(werte)):
    print(statuszeile(nummer + 1, werte[nummer], grenze))
print(f"Alarme: {anzahl_alarme(werte, grenze)} von {len(werte)}")


# Idee: ist_alarm vergleicht nur und gibt das Ergebnis des Vergleichs zurück. statuszeile fragt
# ist_alarm und gibt je nach Antwort einen der beiden Texte zurück. anzahl_alarme beginnt mit
# einem Zähler 0, geht die Liste mit for durch und erhöht den Zähler, wenn ist_alarm True liefert.
# Die Regel „über der Grenze“ steht so nur an einer Stelle im Programm.
# Anderer Weg: ist_alarm mit if/else schreiben (if wert > grenze: return True, sonst return False).
# In statuszeile kann man das Ende erst in eine Variable legen, etwa zustand = "ALARM" oder "ok",
# und dann einen einzigen f-String zurückgeben.
# Typische Fehler: >= statt > (ein Wert genau auf der Grenze wird dann Alarm), in statuszeile print
# statt return (dann gibt das Programm None aus), in anzahl_alarme den Zähler in der Schleife auf 0
# setzen oder return in die Schleife einrücken (dann zählt nur der erste Wert).
