r"""Aufgabe 3_049 – Datenbanklog                                  Stufe 3 ★★★☆☆

Der Datenbankserver einer Firma schreibt jedes Ereignis als Zeile in
eine Logdatei: Datum, Uhrzeit, Schweregrad und Meldung, durch
Leerzeichen getrennt. Der Schweregrad ist INFO (alles in Ordnung), WARN
(Warnung, etwa eine langsame Abfrage) oder ERROR (Fehler). Weil die
Datei manchmal von Hand bearbeitet wird oder ein anderes Programm
hineinschreibt, stehen auch kaputte Zeilen darin:

    2026-11-20 08:00:01 INFO Datenbank gestartet
    2026-11-20 08:15:02 WARN Langsame Abfrage: 2.4 s
    2026-11-20 08:15:09 INFO Sicherung begonnen
    2026-11-20 08:20:44 ERROR Verbindung abgelehnt: zu viele Clients
    kaputte Zeile
    2026-11-20 08:21:00 WARN Langsame Abfrage: 3.1 s
    2026-11-20 08:30:12 INFO Sicherung beendet

    2026-11-20 08:31:00 DEBUG Puffer geleert

Jeden Morgen soll ein Skript daraus einen kurzen Bericht für das
Betriebsteam machen. Schreiben Sie drei Funktionen:

- `zaehle_eintraege(logpfad)` gibt ein Dictionary mit genau den
  Schlüsseln "ERROR", "WARN", "INFO" und "ungueltig" zurück. Eine Zeile
  zählt bei ihrem Schweregrad, wenn sie mindestens drei durch Leerraum
  getrennte Teile hat und der dritte genau ERROR, WARN oder INFO ist.
  Jede andere Zeile, die weder leer ist noch nur aus Leerraum besteht,
  zählt als ungültig.
- `schreibe_bericht(berichtpfad, zaehlung)` bekommt so ein Dictionary
  und schreibt den Bericht in die Datei berichtpfad (ein alter Inhalt
  wird ersetzt): zuerst eine Zeile je Schweregrad, auch bei 0, sortiert
  nach der Anzahl, die größte zuerst; bei gleicher Anzahl kommt ERROR
  vor WARN vor INFO. Dann die Zeile mit den ungültigen Zeilen. Jede
  Zeile endet mit einem Zeilenumbruch.
- `werte_log_aus(logpfad, berichtpfad)` zählt mit zaehle_eintraege,
  schreibt mit schreibe_bericht und gibt zurück, wie viele gültige
  Einträge die Logdatei hat.

Für die Logdatei oben:

    zaehle_eintraege(logpfad)  →  {"ERROR": 1, "WARN": 2, "INFO": 3, "ungueltig": 2}
    werte_log_aus(logpfad, berichtpfad)  →  6

und die Berichtsdatei enthält:

    INFO: 3
    WARN: 2
    ERROR: 1
    Ungültige Zeilen: 2

Grenzen: Die Logdatei ist in UTF-8 gespeichert und hat 0 bis 100 000
Zeilen mit höchstens 300 Zeichen; die letzte kann mit oder ohne
Zeilenumbruch enden. Der Ordner der Berichtsdatei existiert. Die
Anzahlen in zaehlung sind ganze Zahlen von 0 bis 100 000.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Eine Datei
lesen Sie mit with open(pfad, encoding="utf-8") Zeile für Zeile
(Aufgabe 3_046), schreiben mit dem Modus "w" und datei.write(...),
den Zeilenumbruch hängen Sie selbst an (Aufgabe 3_048). zeile.split()
ohne Argument zerlegt an beliebig viel Leerraum, auch an Tabulatoren,
und lässt den Zeilenumbruch weg (Aufgabe 2_015). Gezählt wird in einem
Dictionary mit festen Schlüsseln (Aufgabe 2_025). Nach mehreren
Kriterien sortiert sorted mit einem key, der ein Tupel liefert (Aufgabe
3_027); ein Minuszeichen dreht die Richtung für eine Zahl um, und die
gewünschte Reihenfolge der Namen liefert eine Liste mit index:

    REIHENFOLGE = ["Gold", "Silber", "Bronze"]
    stufen = {"Gold": 2, "Silber": 5, "Bronze": 2}
    sorted(stufen, key=lambda name: (-stufen[name], REIHENFOLGE.index(name)))
                                   →  ["Silber", "Gold", "Bronze"]

Die lambda-Funktion dafür kennen Sie aus Aufgabe 3_025.
"""

SCHWEREGRADE = ["ERROR", "WARN", "INFO"]


def zaehle_eintraege(logpfad):
    """Zählt die Einträge je Schweregrad und die ungültigen Zeilen der Logdatei."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def schreibe_bericht(berichtpfad, zaehlung):
    """Schreibt die Anzahlen je Schweregrad, die größte zuerst, und die Zahl der ungültigen Zeilen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def werte_log_aus(logpfad, berichtpfad):
    """Schreibt den Bericht zur Logdatei und gibt die Zahl der gültigen Einträge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
