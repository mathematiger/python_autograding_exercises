"""Aufgabe 4_035 – Tabreihenfolge                                Stufe 4 ★★★★☆

Wer eine Eingabemaske nur mit der Tastatur bedient, etwa weil er keine
Maus benutzen kann, springt mit der Tabulatortaste von Feld zu Feld und
mit Umschalt+Tab zurück. Für die Barrierefreiheit muss diese
Tabreihenfolge sinnvoll sein: Jedes Feld bekommt eine Position, die
Felder werden nach aufsteigender Position angesprungen, und abgeschaltete
Felder (etwa „Firmenname“, solange „Privatkunde“ angekreuzt ist) werden
übersprungen. Haben zwei Felder dieselbe Position, kommt das zuerst
hinzugefügte zuerst.

Vervollständigen Sie die Klasse `Eingabemaske`:

- `__init__(self)` legt eine leere Maske an.
- `hinzufuegen(self, name, position, aktiv=True)` fügt ein Feld hinzu.
- `aktiv_setzen(self, name, aktiv)` schaltet ein vorhandenes Feld ein oder
  ab.
- `__iter__(self)` liefert die Namen der aktiven Felder in
  Tabreihenfolge. Schreiben Sie es als Generatormethode mit yield, ohne
  eigene Iterator-Klasse.
- `rueckwaerts(self)` liefert dieselben Namen in umgekehrter Reihenfolge
  (Umschalt+Tab), ebenfalls als Generatormethode.

    maske = Eingabemaske()
    maske.hinzufuegen("Name", 10)
    maske.hinzufuegen("Firma", 20, aktiv=False)
    maske.hinzufuegen("E-Mail", 30)
    maske.hinzufuegen("Absenden", 99)
    maske.hinzufuegen("Vorname", 10)
    list(maske)               →  ["Name", "Vorname", "E-Mail", "Absenden"]
    list(maske.rueckwaerts()) →  ["Absenden", "E-Mail", "Vorname", "Name"]
    maske.aktiv_setzen("Firma", True)
    list(maske)               →  ["Name", "Vorname", "Firma", "E-Mail", "Absenden"]

Eine Maske lässt sich beliebig oft durchlaufen, auch verschachtelt; jeder
Durchlauf sieht den Stand der Maske, den sie bei seinem Beginn hat.

Grenzen: Eine Maske hat 0 bis 2000 Felder mit verschiedenen Namen (Texte).
Positionen sind ganze Zahlen von 0 bis 10**6. aktiv_setzen wird nur für
Namen aufgerufen, die es gibt.

Hintergrund: In Aufgabe 4_033 haben Sie ein Iterable mit einer eigenen
Iterator-Klasse gebaut: __iter__ gab einen neuen PlanIterator zurück,
der sich in Attributen merkte, wo er stand, und in __next__ von Hand
StopIteration auslöste. Das geht viel kürzer. Eine Funktion mit yield
liefert beim Aufruf einen Generator (Aufgabe 3_022), und ein Generator
ist ein Iterator: Er hat __next__, merkt sich seinen Stand in seinen
lokalen Variablen und löst am Ende von selbst StopIteration aus. Das gilt
auch für Methoden. Schreibt man __iter__ mit yield, entsteht bei jedem
iter(objekt), also bei jedem for, ein neuer, unabhängiger Generator:

    class Woche:
        def __init__(self, tage):
            self.tage = tage

        def __iter__(self):
            for tag in self.tage:
                yield tag

    woche = Woche(["Mo", "Di", "Mi"])
    list(woche)        →  ["Mo", "Di", "Mi"]
    list(woche)        →  noch einmal dasselbe
    [(a, b) for a in woche for b in woche]   →  9 Paare, verschachtelt

Das ersetzt die ganze PlanIterator-Klasse aus Aufgabe 4_033. Der Rumpf
der Generatormethode läuft erst beim ersten next() los, nicht schon beim
Aufruf von iter(). Andere Methoden, die etwas zum Durchlaufen liefern,
schreibt man genauso, etwa eine Methode rueckwaerts mit yield, die man
mit for name in maske.rueckwaerts() aufruft.

Zum Sortieren nach der Position hilft sorted mit key (Aufgabe 3_027).
sorted ist stabil: Elemente mit gleichem Schlüssel behalten ihre
bisherige Reihenfolge. Das gilt auch für sorted(..., reverse=True); wer
eine fertige Reihenfolge genau umdrehen will, nimmt reversed(...).
"""


class Eingabemaske:
    """Eine Eingabemaske, deren aktive Felder man in Tabreihenfolge durchläuft."""

    def __init__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def hinzufuegen(self, name, position, aktiv=True):
        """Fügt ein Feld mit Position und Zustand hinzu."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def aktiv_setzen(self, name, aktiv):
        """Schaltet das Feld mit diesem Namen ein oder ab."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __iter__(self):
        """Liefert die Namen der aktiven Felder in Tabreihenfolge."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def rueckwaerts(self):
        """Liefert die Namen der aktiven Felder in umgekehrter Tabreihenfolge."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


maske = Eingabemaske()
maske.hinzufuegen("Name", 10)
maske.hinzufuegen("Firma", 20, aktiv=False)
maske.hinzufuegen("E-Mail", 30)
maske.hinzufuegen("Absenden", 99)
maske.hinzufuegen("Vorname", 10)
print(list(maske))
print(list(maske.rueckwaerts()))
