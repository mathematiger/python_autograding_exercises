# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_049_datenbanklog.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_049_datenbanklog

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

Die lambda-Funktion dafür kennen Sie aus Aufgabe 3_025. liste.index(x)
gibt die Stelle zurück, an der x zuerst in der Liste steht:
REIHENFOLGE.index("Silber") ist 1.
"""

SCHWEREGRADE = ["ERROR", "WARN", "INFO"]


def zaehle_eintraege(logpfad):
    """Zählt die Einträge je Schweregrad und die ungültigen Zeilen der Logdatei."""
    zaehlung = {"ERROR": 0, "WARN": 0, "INFO": 0, "ungueltig": 0}
    with open(logpfad, encoding="utf-8") as datei:
        for zeile in datei:
            teile = zeile.split()
            if teile == []:
                continue
            if len(teile) >= 3 and teile[2] in SCHWEREGRADE:
                zaehlung[teile[2]] += 1
            else:
                zaehlung["ungueltig"] += 1
    return zaehlung


def schreibe_bericht(berichtpfad, zaehlung):
    """Schreibt die Anzahlen je Schweregrad, die größte zuerst, und die Zahl der ungültigen Zeilen."""
    reihenfolge = sorted(SCHWEREGRADE, key=lambda grad: (-zaehlung[grad], SCHWEREGRADE.index(grad)))
    with open(berichtpfad, "w", encoding="utf-8") as datei:
        for grad in reihenfolge:
            datei.write(f"{grad}: {zaehlung[grad]}\n")
        datei.write(f"Ungültige Zeilen: {zaehlung['ungueltig']}\n")


def werte_log_aus(logpfad, berichtpfad):
    """Schreibt den Bericht zur Logdatei und gibt die Zahl der gültigen Einträge zurück."""
    zaehlung = zaehle_eintraege(logpfad)
    schreibe_bericht(berichtpfad, zaehlung)
    return zaehlung["ERROR"] + zaehlung["WARN"] + zaehlung["INFO"]



# Idee: zaehle_eintraege beginnt mit einem Dictionary, in dem alle vier Schlüssel auf 0 stehen, liest
# die Datei Zeile für Zeile und zerlegt jede mit split(). Eine leere Liste heißt leere Zeile und wird
# übersprungen; hat die Zeile mindestens drei Teile und ist teile[2] ein bekannter Schweregrad, zählt
# sie dort, sonst als ungültig. schreibe_bericht sortiert die drei Schweregrade mit dem key
# (-anzahl, Stelle in SCHWEREGRADE) und schreibt je eine Zeile, danach die ungültigen. werte_log_aus
# ruft beide auf und addiert die drei gültigen Anzahlen.
# Anderer Weg: Die Reihenfolge im Bericht geht auch ohne Tupel, weil sorted stabil ist:
# sorted(SCHWEREGRADE, key=lambda grad: -zaehlung[grad]) lässt gleich große in der Reihenfolge der
# Liste stehen. Die Summe in werte_log_aus geht auch mit sum(zaehlung[grad] for grad in SCHWEREGRADE).
# Typische Fehler: split(" ") statt split() (Tabulatoren und doppelte Leerzeichen zerlegen falsch),
# teile[2] ohne Prüfung der Länge (IndexError bei kurzen Zeilen), leere Zeilen als ungültig zählen,
# "ERROR" in zeile statt teile[2] == "ERROR", reverse=True mit dem Namen als zweitem Kriterium (dreht
# auch den Gleichstand um), "\n" vergessen oder die ungültigen in werte_log_aus mitzählen.
# Laufzeit: O(n) für n Zeichen der Logdatei; der Bericht sortiert nur drei Einträge.
