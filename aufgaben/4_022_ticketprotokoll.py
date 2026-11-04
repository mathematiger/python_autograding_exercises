"""Aufgabe 4_022 – Ticketprotokoll                              Stufe 4 ★★★★☆

Im Ticketsystem eines IT-Dienstleisters gibt es Funktionen, die Tickets
verändern: eine Störung eskalieren, ein Ticket einer Person zuweisen,
ein Ticket schließen. Für Rückfragen von Kunden und für die Prüfung der
vereinbarten Servicezeiten muss jede solche Aktion nachvollziehbar
sein: Wer hat wann was mit welchem Ergebnis getan? Statt in jede
Funktion dieselben Zeilen fürs Protokoll zu schreiben, soll ein
Dekorator das übernehmen. Vervollständigen Sie `protokolliere`:

- `protokolliere(funktion)` gibt eine Hüllfunktion zurück, die
  funktion mit allen Argumenten aufruft und ihr Ergebnis zurückgibt.
  Vorher oder nachher hängt sie an die Liste PROTOKOLL eine Zeile an:
  den Funktionsnamen, in Klammern die Argumente (die nach Position mit
  repr, dann die nach Namen als name=repr(wert), in der Reihenfolge des
  Aufrufs, durch ", " getrennt), dann " -> " und repr des Ergebnisses.
- Löst funktion eine Ausnahme aus, steht hinter " -> " stattdessen
  "Fehler: " und der Name der Ausnahmeklasse, und die Ausnahme wird
  unverändert weitergegeben.
- Die Hüllfunktion trägt dank functools.wraps Namen, Docstring und
  `__wrapped__` der ursprünglichen Funktion.

    @protokolliere
    def eskaliere(ticket, stufe=1):
        ...

    eskaliere("T-17", stufe=2)   →  "T-17 auf Stufe 2"
    schliesse("T-99")            →  ValueError
    PROTOKOLL                    →  ["eskaliere('T-17', stufe=2) -> 'T-17 auf Stufe 2'",
                                     "schliesse('T-99') -> Fehler: ValueError"]
    eskaliere.__name__           →  "eskaliere"

Grenzen: Die dekorierten Funktionen bekommen 0 bis 10 Argumente nach
Position und 0 bis 10 nach Namen, Werte, deren repr ein kurzer Text
ist. Sie können jede Ausnahme auslösen, die von Exception abstammt.
Das Ergebnis darf auch None sein. Bis zu 100 000 Aufrufe hintereinander
werden protokolliert.

Hintergrund: Ein Dekorator ist eine Funktion, die eine Funktion bekommt
und eine (meist neue) Funktion zurückgibt. Die Schreibweise mit @ ist
nur eine Abkürzung:

    @protokolliere
    def schliesse(ticket):
        ...

bedeutet genau

    def schliesse(ticket):
        ...
    schliesse = protokolliere(schliesse)

Ab dann ruft jeder Aufruf schliesse("T-1") die Hüllfunktion auf. Damit
sie zu jeder Funktion passt, nimmt sie mit *args und **kwargs (Aufgabe
4_018) beliebige Argumente an und reicht sie weiter. Sie ist eine
Closure (Aufgabe 4_021): Sie merkt sich, welche Funktion sie umhüllt.

    import functools

    def laut(funktion):
        @functools.wraps(funktion)
        def huelle(*args, **kwargs):
            print("Aufruf von", funktion.__name__)
            return funktion(*args, **kwargs)
        return huelle

Ohne @functools.wraps(funktion) hieße die dekorierte Funktion nach außen
„huelle“, ihr Docstring wäre weg, und help(), Fehlermeldungen und
Testwerkzeuge zeigten die falschen Angaben. wraps kopiert __name__,
__doc__, __qualname__ und weitere Angaben von der ursprünglichen
Funktion auf die Hülle und legt in __wrapped__ einen Verweis auf das
Original ab. Eine Ausnahme der umhüllten Funktion fängt man mit
try/except ab, schreibt ins Protokoll und gibt sie mit einem raise ohne
Argument unverändert weiter. Ein finally-Block ist hier nicht passend,
weil Erfolg und Fehler verschieden protokolliert werden. kwargs ist ein
Dictionary; es enthält die benannten Argumente in der Reihenfolge, in
der sie beim Aufruf standen.
"""

import functools

PROTOKOLL = []


def protokolliere(funktion):
    """Dekorator: schreibt jeden Aufruf von funktion mit Argumenten und Ergebnis in PROTOKOLL."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@protokolliere
def eskaliere(ticket, stufe=1):
    """Hebt ein Ticket auf eine höhere Eskalationsstufe."""
    return f"{ticket} auf Stufe {stufe}"


@protokolliere
def schliesse(ticket):
    """Schließt ein Ticket; T-99 ist noch in Bearbeitung und lässt sich nicht schließen."""
    if ticket == "T-99":
        raise ValueError("T-99 ist noch in Bearbeitung")
    return None


eskaliere("T-17", stufe=2)
try:
    schliesse("T-99")
except ValueError:
    pass
print(PROTOKOLL)
print(eskaliere.__name__)
