"""Aufgabe 4_002 – Abfahrtstafel                                 Stufe 4 ★★★★☆

Ein Bahnhof bekommt ein neues Anzeigesystem. Jede Abfahrt ist ein Objekt der
Klasse `Abfahrt` mit Zugname, Ziel, Stunde und Minute. Für die Fahrgäste soll
eine Abfahrt lesbar aussehen, für die Entwicklerinnen beim Fehlersuchen soll
sie eindeutig sein. Vervollständigen Sie die Klasse:

- `__str__(self)` liefert die Zeile für die Anzeigetafel, Stunde und Minute
  immer zweistellig: "09:05 ICE 597 nach München".
- `__repr__(self)` liefert den Python-Ausdruck, mit dem man genau dieses Objekt
  wieder erzeugen könnte: "Abfahrt('ICE 597', 'München', 9, 5)".

    abfahrt = Abfahrt("ICE 597", "München", 9, 5)
    print(abfahrt)      →  09:05 ICE 597 nach München
    print([abfahrt])    →  [Abfahrt('ICE 597', 'München', 9, 5)]

Hintergrund: Python kennt zwei Arten, ein Objekt als Text darzustellen.
str(objekt) ruft objekt.__str__() auf und ist für Menschen gedacht, die das
Programm benutzen; print und f-Strings verwenden es. repr(objekt) ruft
objekt.__repr__() auf und ist für Programmierende gedacht: Die Darstellung soll
eindeutig sein und, wenn möglich, wie gültiger Python-Code aussehen, der ein
gleiches Objekt erzeugt. Man sieht den Unterschied an Texten:

    >>> print(str("München"))
    München
    >>> print(repr("München"))
    'München'

Nur repr zeigt die Anführungszeichen; so erkennt man, ob "5" ein Text oder 5
eine Zahl ist. Wichtig: Listen, Tupel und Dictionaries stellen ihre Elemente
immer mit repr dar, auch wenn man die Liste mit print ausgibt. Und hat eine
Klasse nur __repr__, verwendet str() das automatisch mit; umgekehrt nicht.
Ohne beide Methoden sieht man nur etwas wie <__main__.Abfahrt object at 0x7f…>.

In f-Strings wählt man die Darstellung selbst: f"{wert}" benutzt str,
f"{wert!r}" benutzt repr. Zahlen formatiert man mit einer Formatangabe nach
dem Doppelpunkt; f"{7:02d}" ergibt "07" (ganze Zahl, mindestens zwei Stellen,
vorne mit Nullen aufgefüllt):

    def __repr__(self):
        return f"Punkt({self.x!r}, {self.y!r})"

Tipp: Benutzen Sie in __repr__ für die Texte !r statt selbst Anführungszeichen
zu setzen. Dann stimmt die Darstellung auch für ein Ziel wie "Val d'Isère",
das selbst ein Apostroph enthält.
"""


class Abfahrt:
    """Eine Abfahrt auf der Anzeigetafel eines Bahnhofs."""

    def __init__(self, zug, ziel, stunde, minute):
        self.zug = zug
        self.ziel = ziel
        self.stunde = stunde
        self.minute = minute

    def __str__(self):
        """Gibt die Zeile für die Anzeigetafel zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __repr__(self):
        """Gibt einen Python-Ausdruck zurück, der diese Abfahrt erzeugt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


abfahrt = Abfahrt("ICE 597", "München", 9, 5)
print(abfahrt)
print([abfahrt])
