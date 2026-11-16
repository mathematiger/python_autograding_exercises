"""Aufgabe 4_032 – Fertigungstakt                                Stufe 4 ★★★★☆

Ein Betrieb analysiert die Abläufe in seiner Fertigung. Jeder Auftrag
durchläuft mehrere Prozessschritte nacheinander, zum Beispiel Zuschnitt,
Montage und Prüfung, jeder mit einer festen Dauer in Minuten. Die
Anzeige an der Maschine zählt außerdem die Restzeit eines Schritts im
Takt der Anlage herunter. Beides soll man mit for durchlaufen können,
ohne vorher eine Liste aller Werte anzulegen. Vervollständigen Sie
drei Klassen, ohne yield zu benutzen:

- `Restzeit(minuten, takt)` ist ein Iterator. Er liefert erst minuten,
  dann jeweils takt weniger, solange das Ergebnis über 0 liegt, und
  zum Schluss genau einmal 0 (der Schritt ist fertig). Danach löst
  jeder weitere Aufruf von next StopIteration aus.
- `Zeitplan(schritte)` ist ein Iterator über eine Liste von Tupeln
  (name, dauer). Er liefert für jeden Schritt ein Tupel
  (name, beginn, ende): Der erste Schritt beginnt bei Minute 0, jeder
  weitere dort, wo der vorige endet, und ende ist beginn + dauer.
- `Prozess(schritte)` ist iterierbar, aber selbst kein Iterator: Jeder
  Aufruf von iter(prozess) liefert einen neuen Zeitplan, sodass man den
  Prozess beliebig oft durchlaufen kann.

    list(Restzeit(10, 3))   →  [10, 7, 4, 1, 0]
    list(Restzeit(9, 3))    →  [9, 6, 3, 0]
    montage = Prozess([("Zuschnitt", 15), ("Montage", 40), ("Prüfung", 10)])
    list(montage)
        →  [("Zuschnitt", 0, 15), ("Montage", 15, 55), ("Prüfung", 55, 65)]
    list(montage)           →  dieselbe Liste noch einmal

Grenzen: minuten ist eine ganze Zahl von 0 bis 10**9, takt eine ganze
Zahl von 1 bis 10**9 (bei minuten = 0 kommt nur die 0). schritte hat 0
bis 100 000 Einträge, jede dauer ist eine ganze Zahl von 0 bis 10**4.
Ein Iterator soll sich nur den aktuellen Stand merken und nicht schon
beim Anlegen alle Werte ausrechnen: Bei Restzeit(10**9, 1) muss der
erste Wert sofort da sein. Die Liste schritte darf nicht verändert
werden.

Hintergrund: Aufgabe 3_020 hat gezeigt, was for im Hintergrund tut:

    iterator = iter(daten)          # ruft daten.__iter__() auf
    while True:
        try:
            wert = next(iterator)   # ruft iterator.__next__() auf
        except StopIteration:
            break
        ...                         # Rumpf der Schleife

Eigene Klassen nehmen an diesem Iterator-Protokoll teil, indem sie die
beiden Methoden selbst schreiben. Ein Iterator hat `__next__`, das den
nächsten Wert liefert oder `raise StopIteration` auslöst, wenn es
keinen mehr gibt, und `__iter__`, das `return self` enthält; so kann
man den Iterator selbst in einer for-Schleife benutzen. Den Stand
merkt er sich in Attributen:

    class Hochzaehlen:
        def __init__(self, bis):
            self.aktuell = 1
            self.bis = bis

        def __iter__(self):
            return self

        def __next__(self):
            if self.aktuell > self.bis:
                raise StopIteration
            wert = self.aktuell
            self.aktuell += 1
            return wert

Ein Iterator ist nach einem Durchlauf verbraucht (Aufgabe 3_021). Eine
Liste dagegen ist iterierbar, aber kein Iterator: Ihr `__iter__` gibt
bei jedem Aufruf einen neuen Iterator zurück, der vorn beginnt. Das
ist die Arbeitsteilung, die Prozess und Zeitplan nachbauen: Das
iterierbare Objekt hält die Daten, der Iterator nur die Stelle, an der
er gerade ist. Deshalb laufen auch zwei verschachtelte for-Schleifen
über dasselbe iterierbare Objekt unabhängig voneinander. Ein Generator
mit yield (Aufgabe 3_022) erzeugt einen solchen Iterator automatisch;
hier soll er von Hand entstehen.
"""


class Restzeit:
    """Iterator über die Restzeit eines Schritts im Takt der Anlage, bis einschließlich 0."""

    def __init__(self, minuten, takt):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __next__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Zeitplan:
    """Iterator über die Schritte mit Beginn und Ende in Minuten."""

    def __init__(self, schritte):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __next__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Prozess:
    """Ein Ablauf aus Schritten, der sich beliebig oft durchlaufen lässt."""

    def __init__(self, schritte):
        self.schritte = schritte

    def __iter__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(list(Restzeit(10, 3)))
montage = Prozess([("Zuschnitt", 15), ("Montage", 40), ("Prüfung", 10)])
for name, beginn, ende in montage:
    print(f"{name}: Minute {beginn} bis {ende}")
