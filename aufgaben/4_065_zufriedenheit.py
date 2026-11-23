"""Aufgabe 4_065 – Zufriedenheit                                 Stufe 4 ★★★★☆

Nach jedem Vor-Ort-Einsatz bittet ein IT-Dienstleister den Kunden um
eine Schulnote von 1 (sehr zufrieden) bis 6 und einen kurzen Kommentar.
Die Auswertung soll zeigen, welche Einsätze schlecht liefen und was die
Kunden schreiben. Die Einsätze liegen als Objekte der vorgegebenen
Datenklasse Einsatz vor, der Export aus dem Umfragewerkzeug als Liste
von Dictionaries, und die Kommentare sind von Hand eingetippt, mit
Leerzeichen am Rand und wilder Groß- und Kleinschreibung.

Schreiben Sie drei Funktionen mit dem Modul operator:

- `sortiert(einsaetze, *felder)` gibt eine neue Liste der Einsätze
  zurück, sortiert nach den Attributen mit den Namen felder: zuerst
  nach dem ersten, bei Gleichstand nach dem zweiten und so weiter.
  Einsätze, die in allen Feldern gleich sind, behalten ihre
  Reihenfolge. Benutzen Sie attrgetter.
- `spalten(zeilen, *schluessel)` gibt für jedes Dictionary in zeilen
  ein Tupel mit den Werten unter den angegebenen Schlüsseln zurück, in
  dieser Reihenfolge, als Liste. Auch bei nur einem Schlüssel ist jedes
  Element ein Tupel. Benutzen Sie itemgetter.
- `bereinigt(kommentare, *schritte)` wendet auf jeden Kommentar die
  Schritte nacheinander an und gibt die Ergebnisse als Liste zurück.
  Jeder Schritt ist ein Tupel aus dem Namen einer Methode von str und
  ihren Argumenten, etwa ("strip",) oder ("replace", "-", " ").
  Benutzen Sie methodcaller.

    einsaetze = [Einsatz("Ada", "Meyer", 45, 2), Einsatz("Bo", "Kraus", 120, 4),
                 Einsatz("Ada", "Lenz", 30, 4)]
    sortiert(einsaetze, "note", "minuten")
    →  [Einsatz("Ada", "Meyer", 45, 2), Einsatz("Ada", "Lenz", 30, 4),
        Einsatz("Bo", "Kraus", 120, 4)]

    zeilen = [{"kunde": "Meyer", "note": 2, "kommentar": "Top"},
              {"kunde": "Kraus", "note": 4, "kommentar": "zu spät"}]
    spalten(zeilen, "note", "kunde")  →  [(2, "Meyer"), (4, "Kraus")]
    spalten(zeilen, "kunde")          →  [("Meyer",), ("Kraus",)]

    bereinigt(["  Sehr GUT ", "schnell-und-nett"], ("strip",), ("lower",),
              ("replace", "-", " "))
    →  ["sehr gut", "schnell und nett"]

Die übergebenen Listen bleiben unverändert.

Grenzen: 0 bis 100 000 Einsätze, Zeilen oder Kommentare. felder und
schluessel enthalten mindestens einen Namen, und jeder Name kommt in
jedem Einsatz beziehungsweise jedem Dictionary vor. schritte enthält 0
bis 10 Schritte; jeder Name ist eine Methode von str, die mit diesen
Argumenten wieder einen Text liefert.

Hintergrund: Mit lambda (Aufgabe 3_025) baut man kleine Funktionen, die
etwas aus einem Wert herausholen, zum Beispiel als key für sorted. Für
die drei häufigsten Fälle hat das Modul operator fertige Bausteine, die
schneller sind und beim Lesen sofort sagen, was passiert. Jeder ist eine
Funktion, die eine Funktion zurückgibt:

    from operator import attrgetter, itemgetter, methodcaller

    hole_note = attrgetter("note")          # wie lambda e: e.note
    hole_note(einsatz)                      →  2
    attrgetter("note", "minuten")(einsatz)  →  (2, 45)

    hole_kunde = itemgetter("kunde")        # wie lambda z: z["kunde"]
    itemgetter("note", "kunde")(zeile)      →  (2, "Meyer")
    itemgetter(0)([7, 8, 9])                →  7

    gross = methodcaller("upper")           # wie lambda t: t.upper()
    methodcaller("replace", "-", " ")("a-b")  →  "a b"

Weil das Ergebnis eine Funktion ist, kann man es überall einsetzen, wo
eine Funktion erwartet wird: sorted(einsaetze, key=attrgetter("note")),
map(itemgetter("kunde"), zeilen) (Aufgabe 3_026), max(..., key=...).
Mit mehreren Namen liefern attrgetter und itemgetter ein Tupel, und
Tupel vergleicht sorted Element für Element; so sortiert man nach
mehreren Feldern auf einmal. Vorsicht: Mit genau einem Namen kommt kein
Tupel heraus, sondern der Wert selbst, itemgetter("kunde")(zeile) ist
"Meyer", nicht ("Meyer",). Wer immer ein Tupel braucht, muss den Fall
eines einzigen Namens selbst behandeln.

Die Argumente einer Funktion mit *felder (Aufgabe 4_018) kommen als
Tupel an; mit attrgetter(*felder) reicht man sie einzeln weiter. Ein
Schritt ("replace", "-", " ") wird so zu methodcaller("replace", "-", " ")
oder kürzer methodcaller(*schritt).
"""

from dataclasses import dataclass
from operator import attrgetter, itemgetter, methodcaller


@dataclass
class Einsatz:
    """Ein Vor-Ort-Einsatz mit Techniker, Kunde, Dauer in Minuten und Schulnote des Kunden."""

    techniker: str
    kunde: str
    minuten: int
    note: int


def sortiert(einsaetze, *felder):
    """Gibt die Einsätze als neue Liste sortiert nach den Attributen felder zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def spalten(zeilen, *schluessel):
    """Gibt für jedes Dictionary das Tupel seiner Werte unter schluessel zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bereinigt(kommentare, *schritte):
    """Wendet auf jeden Kommentar die Methodenaufrufe in schritte nacheinander an."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


einsaetze = [Einsatz("Ada", "Meyer", 45, 2), Einsatz("Bo", "Kraus", 120, 4), Einsatz("Ada", "Lenz", 30, 4)]
for einsatz in sortiert(einsaetze, "note", "minuten"):
    print(einsatz)
zeilen = [{"kunde": "Meyer", "note": 2, "kommentar": "Top"}, {"kunde": "Kraus", "note": 4, "kommentar": "zu spät"}]
print(spalten(zeilen, "note", "kunde"))
print(bereinigt(["  Sehr GUT ", "schnell-und-nett"], ("strip",), ("lower",), ("replace", "-", " ")))
