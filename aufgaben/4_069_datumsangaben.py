r"""Aufgabe 4_069 – Datumsangaben                                 Stufe 4 ★★★★☆

Ein Unternehmen untersucht, wie lange Bestellungen von der Anfrage bis
zur Freigabe brauchen. Die Bearbeitungsnotizen kommen auch von der
Niederlassung in den USA, und dort schreibt man Daten als
Monat/Tag/Jahr: 3/7/2026 ist der 7. März 2026, nicht der 3. Juli. Bevor
die Notizen ausgewertet werden, sollen alle Daten in die deutsche Form
TT.MM.JJJJ gebracht werden, mit führender Null bei Tag und Monat.

    Fall 17: Antrag 3/7/2026 eingegangen, geprüft 3/12/2026, Version 2/3 freigegeben 11/23/2026.

Ein Datum ist hier eine Stelle aus ein oder zwei Ziffern für den Monat,
einem Schrägstrich, ein oder zwei Ziffern für den Tag, einem
Schrägstrich und genau vier Ziffern für das Jahr, die als eigenes Wort
dasteht: davor und dahinter keine Ziffer, kein Buchstabe und kein _.
„Version 2/3“ ist also kein Datum, 011/23/2026 und 1/2/20265 auch nicht.

Schreiben Sie mit dem Modul re zwei Funktionen:

- `vereinheitliche(text)` gibt den Text zurück, in dem jedes Datum
  durch TT.MM.JJJJ ersetzt ist; alles andere bleibt, wie es ist.
  Benutzen Sie re.sub mit einer Funktion als Ersatz.
- `fundstellen(text)` gibt für jedes Datum im Text das Tupel (anfang,
  ende, datum) zurück: anfang und ende sind die Positionen im
  ursprünglichen Text wie bei Slicing (text[anfang:ende] ist das Datum
  in US-Form), datum ist das Datum als TT.MM.JJJJ. Benutzen Sie
  re.finditer.

    vereinheitliche(notiz)
    →  "Fall 17: Antrag 07.03.2026 eingegangen, geprüft 12.03.2026, Version 2/3 freigegeben 23.11.2026."
    fundstellen(notiz)
    →  [(16, 24, "07.03.2026"), (46, 55, "12.03.2026"), (81, 91, "23.11.2026")]

Grenzen: text hat 0 bis 100 000 Zeichen; als Ziffern kommen nur 0 bis 9
vor. Jedes Datum im Sinne der Aufgabe ist ein gültiges Datum (Monat 1 bis
12, Tag passend zum Monat), gern mit führender Null (03/07/2026).

Hintergrund: Aus Aufgabe 4_067 kennen Sie re.search, re.findall und
Gruppen. re.sub(muster, ersatz, text) ersetzt jede passende Stelle und
gibt den neuen Text zurück. Im Ersatztext stehen \1, \2 … (oder
\g<name>) für die Gruppen des Treffers:

    re.sub(r"(\d+)-(\d+)", r"\2-\1", "Raum 4-12")   →  "Raum 12-4"

Mehr als umstellen kann ein Ersatztext nicht: Er kann nicht rechnen,
keine Null voranstellen und nichts nachschlagen. Dafür darf ersatz eine
Funktion sein. re.sub ruft sie für jeden Treffer mit dem Treffer-Objekt
auf und setzt ein, was sie zurückgibt (einen Text):

    def verdoppeln(treffer):
        return str(2 * int(treffer.group(1)))

    re.sub(r"(\d+) Stück", verdoppeln, "3 Stück und 10 Stück")   →  "6 und 20"

Hier wird die ganze passende Stelle „3 Stück“ durch "6" ersetzt. Mit
treffer.groups() bekommt man alle Gruppen als Tupel von Texten, und ein
f-String wie f"{int(tag):02d}" stellt eine Null voran (Aufgabe 4_066).

re.findall liefert nur die Texte. re.finditer(muster, text) liefert
dagegen nacheinander ein Treffer-Objekt für jede passende Stelle, und
das weiß auch, wo im Text sie steht:

    for treffer in re.finditer(r"\d+", "a 12 bc 345"):
        print(treffer.group(), treffer.start(), treffer.end())
    # 12 2 4
    # 345 8 11

treffer.span() ist das Paar (start(), end()). finditer ist ein Iterator
(Aufgabe 4_034): Er sucht erst weiter, wenn man den nächsten Treffer
verlangt, und braucht keine Liste aller Treffer im Speicher. Wer
dieselbe Umwandlung in beiden Funktionen braucht, schreibt sie einmal
als eigene Funktion, die einen Treffer bekommt; re.sub kann sie direkt
benutzen, und in der Schleife über finditer ruft man sie selbst auf.
Ein Muster, das man mehrfach braucht, legt man als Konstante ab; mit
re.compile(muster) wird daraus ein Objekt mit denselben Methoden
(DATUM.sub(…), DATUM.finditer(…)).
"""

import re

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vereinheitliche(text):
    """Gibt text zurück, in dem jedes Datum Monat/Tag/Jahr durch TT.MM.JJJJ ersetzt ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fundstellen(text):
    """Gibt für jedes Datum (anfang, ende, TT.MM.JJJJ) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


notiz = "Fall 17: Antrag 3/7/2026 eingegangen, geprüft 3/12/2026, Version 2/3 freigegeben 11/23/2026."
print(vereinheitliche(notiz))
print(fundstellen(notiz))
