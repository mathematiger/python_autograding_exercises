"""Aufgabe 3_025 – Stilregeln                                    Stufe 3 ★★★☆☆

Ein Entwicklungsteam hat sich auf Regeln für sauberen Code (Clean Code)
geeinigt, damit alle Dateien gleich aussehen und sich gut lesen lassen.
Vor jedem Einchecken soll ein kleines Prüfprogramm die Zeilen einer
Datei durchsehen und jeden Verstoß melden. Jede Regel ist eine kleine
Funktion, die eine Zeile bekommt und True liefert, wenn die Zeile gegen
die Regel verstößt. Das Programm sammelt die Regeln in der Liste REGELN
und wendet sie in befunde auf alle Zeilen an; das ist schon fertig.
Schreiben Sie die vier Regeln, jede als lambda-Ausdruck in einer Zeile:

- `zu_lang(zeile, grenze=79)`: Die Zeile hat mehr als grenze Zeichen.
- `leerraum_am_ende(zeile)`: Die Zeile endet mit einem Leerzeichen oder
  einem Tabulator "\\t".
- `tabulator(zeile)`: Die Zeile enthält irgendwo einen Tabulator.
- `schiefe_einrueckung(zeile)`: Die Anzahl der Leerzeichen am
  Zeilenanfang (vor dem ersten Zeichen, das kein Leerzeichen ist) ist
  nicht durch 4 teilbar.

    zu_lang("x" * 80)                    →  True
    zu_lang("x" * 80, 100)               →  False
    leerraum_am_ende("print(1) ")        →  True
    tabulator("\\tprint(1)")              →  True
    schiefe_einrueckung("   return 0")   →  True    (3 Leerzeichen)
    schiefe_einrueckung("        pass")  →  False   (8 Leerzeichen)
    befunde(["def f():", "   return 1 "])
        →  [(2, "Leerraum am Ende"), (2, "schiefe Einrückung")]

Grenzen: zeile ist ein Text mit 0 bis 200 Zeichen aus druckbaren
ASCII-Zeichen (Buchstaben, Ziffern, Satzzeichen, Leerzeichen) und
Tabulatoren, ohne Zeilenumbruch. grenze ist eine ganze Zahl von 0 bis
200. befunde bekommt 0 bis 10 000 Zeilen.

Hintergrund: Ein lambda-Ausdruck erzeugt eine Funktion, ohne ihr mit
def einen Namen zu geben. Hinter dem Wort lambda stehen die Parameter,
nach dem Doppelpunkt ein einziger Ausdruck, dessen Wert die Funktion
zurückgibt; ein return schreibt man nicht:

    doppelt = lambda x: 2 * x
    # tut dasselbe wie
    def doppelt(x):
        return 2 * x

    doppelt(21)                          →  42
    summe = lambda a, b=10: a + b        # auch mehrere Parameter und Standardwerte (Aufgabe 2_011)
    summe(1)                             →  11
    (lambda wort: wort.upper())("ok")    →  "OK"

Weil eine Funktion in Python ein Wert ist wie eine Zahl, kann man sie
einer Variablen zuweisen, in eine Liste legen und später aufrufen; das
tut REGELN. Im Rumpf eines lambda-Ausdrucks ist nur ein Ausdruck
erlaubt, also kein if-Block, keine Schleife und keine Zuweisung. Ein
Vergleich wie len(text) > 5 oder eine Verknüpfung mit and und or ist
aber ein Ausdruck und liefert True oder False. Ein lambda-Ausdruck hat
keinen eigenen Namen: doppelt.__name__ ist "<lambda>". Für Funktionen,
die man an vielen Stellen braucht, schreibt man deshalb meist def;
seine Stärke spielt lambda aus, wenn man eine kleine Funktion direkt
an eine andere Funktion übergibt, etwa an sorted (kommt in Aufgabe
3_027).

Tipp: text.lstrip(" ") liefert den Text ohne die Leerzeichen am Anfang.
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

REGELN = [
    ("zu lang", zu_lang),
    ("Leerraum am Ende", leerraum_am_ende),
    ("Tabulator", tabulator),
    ("schiefe Einrückung", schiefe_einrueckung),
]


def befunde(zeilen):
    """Gibt für jeden Verstoß ein Tupel (zeilennummer, regel) zurück; die Zeilen zählen ab 1."""
    ergebnis = []
    for nummer, zeile in enumerate(zeilen, start=1):
        for name, regel in REGELN:
            if regel(zeile):
                ergebnis.append((nummer, name))
    return ergebnis


print(befunde(["def f():", "   return 1 "]))
