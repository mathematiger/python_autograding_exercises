"""Aufgabe 4_019 – Logzeilen                                      Stufe 4 ★★★★☆

Ein Monitoring-System sammelt die Meldungen aller Server eines
Rechenzentrums in einem zentralen Log. Jede Zeile beginnt mit Datum,
Uhrzeit, Rechnername und Stufe, danach folgt der eigentliche Text der
Meldung, der beliebig viele Wörter haben kann, auch keins:

    2026-11-03 04:12:07 web01 ERROR upstream timed out
    2026-11-03 04:12:09 db02 INFO backup gestartet
    2026-11-03 04:13:00 web01 WARN

Außerdem misst das System alle fünf Minuten die CPU-Last eines Servers
und speichert eine Messreihe als Liste von Tupeln (uhrzeit, last), und
es führt eine Liste der Ausfälle als Tupel (rechner, (von, bis)) mit den
Minuten seit Mitternacht. Vervollständigen Sie:

- `zerlege(zeile)` gibt das Tupel (rechner, stufe, text) zurück; text
  sind die Wörter der Meldung, mit je einem Leerzeichen verbunden, bei
  einer Zeile ohne Meldung der leere Text.
- `verlauf(messreihe)` gibt das Tupel (erste_uhrzeit, letzte_uhrzeit,
  veraenderung) zurück, wobei veraenderung die letzte minus die erste
  Last ist. Hat die Messreihe nur eine Messung, ist sie zugleich die
  erste und die letzte.
- `ausfallzeit(ausfaelle)` gibt ein Dictionary zurück, das jedem
  Rechner die Summe seiner Ausfallminuten (bis - von) zuordnet, in der
  Reihenfolge, in der die Rechner zuerst vorkommen.

Benutzen Sie dafür Entpacken: in zerlege und verlauf mit einem
Sternausdruck (*rest), in ausfallzeit verschachtelt im Kopf der
for-Schleife.

    zerlege("2026-11-03 04:12:07 web01 ERROR upstream timed out")
        →  ("web01", "ERROR", "upstream timed out")
    zerlege("2026-11-03 04:13:00 web01 WARN")
        →  ("web01", "WARN", "")
    verlauf([("04:00", 31), ("04:05", 58), ("04:10", 47)])
        →  ("04:00", "04:10", 16)
    ausfallzeit([("web01", (120, 135)), ("db02", (300, 302)), ("web01", (600, 610))])
        →  {"web01": 25, "db02": 2}

Grenzen: Eine Zeile besteht aus Datum, Uhrzeit, Rechner, Stufe und 0
bis 100 Wörtern, getrennt durch je ein Leerzeichen; keins davon enthält
selbst ein Leerzeichen. messreihe hat 1 bis 100 000 Messungen, die
Uhrzeiten sind Texte, die Lasten ganze Zahlen von 0 bis 100. ausfaelle
hat 0 bis 100 000 Einträge, von und bis sind ganze Zahlen mit
0 ≤ von ≤ bis ≤ 1440. Die übergebenen Listen bleiben unverändert.

Hintergrund: Auspacken kennen Sie schon: a, b = (1, 2) verteilt die
Werte eines Tupels auf zwei Variablen. Dafür muss die Anzahl der
Variablen genau passen, sonst gibt es einen ValueError. Ein
Sternausdruck sammelt alles, was übrig bleibt, in einer Liste, und
zwar an beliebiger Stelle:

    kopf, *rest = [1, 2, 3, 4]        # kopf = 1, rest = [2, 3, 4]
    *anfang, ende = "a b c".split()   # anfang = ["a", "b"], ende = "c"
    erstes, *mitte, letztes = [7, 8]  # erstes = 7, mitte = [], letztes = 8

Der Stern-Teil darf leer bleiben, die übrigen Variablen müssen aber
alle einen Wert bekommen: erstes, *mitte, letztes = [7] ist ein
ValueError, weil nur ein Wert da ist. Pro Zuweisung ist nur ein Stern
erlaubt. Den Namen _ nimmt man für Werte, die man nicht braucht:
_, _, rechner, *_ = zeile.split().

Auspacken geht auch verschachtelt. Die linke Seite bildet dann die
Form der Daten nach, mit Klammern für die inneren Tupel. Das klappt
überall, wo Python Namen zuweist, auch im Kopf einer for-Schleife:

    punkte = [("A", (0, 3)), ("B", (4, 1))]
    for name, (x, y) in punkte:
        print(name, x + y)

Ohne Entpacken stünden dort punkt[0], punkt[1][0] und punkt[1][1], und
man müsste beim Lesen erst nachzählen, was welcher Index bedeutet. Die
Sterne aus Aufgabe 4_018 sind verwandt: Dort sammelt *args die
übrigen Argumente eines Aufrufs, hier sammelt *rest die übrigen Werte
einer Zuweisung.
"""


def zerlege(zeile):
    """Gibt (rechner, stufe, text) einer Logzeile zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verlauf(messreihe):
    """Gibt (erste Uhrzeit, letzte Uhrzeit, letzte minus erste Last) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ausfallzeit(ausfaelle):
    """Gibt zu jedem Rechner die Summe seiner Ausfallminuten zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(zerlege("2026-11-03 04:12:07 web01 ERROR upstream timed out"))
print(zerlege("2026-11-03 04:13:00 web01 WARN"))
print(verlauf([("04:00", 31), ("04:05", 58), ("04:10", 47)]))
print(ausfallzeit([("web01", (120, 135)), ("db02", (300, 302)), ("web01", (600, 610))]))
