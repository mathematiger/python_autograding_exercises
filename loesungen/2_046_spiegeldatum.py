# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_046_spiegeldatum.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_046_spiegeldatum

"""Aufgabe 2_046 – Spiegeldatum                                  Stufe 2 ★★☆☆☆

Ein Projektteam plant den Go-Live seiner neuen Software, also den
Meilenstein, an dem sie in Betrieb geht. Die Projektleiterin möchte ihn
auf ein Spiegeldatum legen: ein Datum, dessen Ziffern vorwärts und
rückwärts gelesen gleich sind, zum Beispiel der 12.02.2021 mit den
Ziffern 12022021. Solche Texte heißen Palindrome. Die vorgegebene
Funktion nur_ziffern entfernt die Punkte aus einem Datum.

Vervollständigen Sie die Funktion `ist_palindrom(text)`, die True
zurückgibt, wenn text vorwärts und rückwärts gleich ist, sonst False.
Schreiben Sie sie rekursiv, ohne for, ohne while und ohne den Text
umzudrehen (kein [::-1], kein reversed):

- Ein Text mit höchstens einem Zeichen ist ein Palindrom.
- Sind das erste und das letzte Zeichen verschieden, ist er keins. Dann
  steht das Ergebnis fest: Geben Sie sofort False zurück, ohne sich noch
  einmal aufzurufen.
- Sonst ist er genau dann ein Palindrom, wenn der Text ohne das erste
  und das letzte Zeichen eins ist.

    ist_palindrom("12022021")  →  True
    ist_palindrom("20250101")  →  False
    ist_palindrom("1221")      →  True
    ist_palindrom("")          →  True

Grenzen: text hat 0 bis 800 Zeichen, beliebige Zeichen. Groß- und
Kleinschreibung zählt („Aa“ ist kein Palindrom).

Hintergrund: Bei einer Rekursion (Aufgabe 2_044) muss jeder Aufruf das
Problem verkleinern, bis ein Fall erreicht ist, dessen Antwort man
direkt kennt. Bei Zahlen war das n - 1, bei Texten ist es ein kürzerer
Text. Mit Slicing (Aufgabe 1_012) schneidet man vorn und hinten je ein
Zeichen ab:

    text = "radar"
    text[0], text[-1]   →  ("r", "r")
    text[1:-1]          →  "ada"

So wird der Text bei jedem Aufruf um zwei Zeichen kürzer und landet
sicher bei einem Text mit 0 oder 1 Zeichen. Weil ein Aufruf nur dann
weiter in die Tiefe geht, wenn die beiden äußeren Zeichen gleich sind,
bricht die Rekursion beim ersten Unterschied ab.
"""


def nur_ziffern(datum):
    """Entfernt die Punkte aus einem Datum wie "12.02.2021" (vorgegeben)."""
    return datum.replace(".", "")


def ist_palindrom(text):
    """Gibt True zurück, wenn text vorwärts und rückwärts gleich ist."""
    if len(text) <= 1:
        return True
    if text[0] != text[-1]:
        return False
    return ist_palindrom(text[1:-1])


print("12.02.2021", ist_palindrom(nur_ziffern("12.02.2021")))
print("01.01.2025", ist_palindrom(nur_ziffern("01.01.2025")))
print("22.02.2022", ist_palindrom(nur_ziffern("22.02.2022")))


# Idee: Texte mit 0 oder 1 Zeichen sind Palindrome, das ist die Abbruchbedingung. Sonst vergleicht
# die Funktion das erste und das letzte Zeichen: Sind sie verschieden, ist das Ergebnis False; sind
# sie gleich, entscheidet der kürzere Text text[1:-1], also gibt die Funktion ist_palindrom(text[1:-1])
# zurück. Jeder Aufruf macht den Text um zwei Zeichen kürzer.
# Anderer Weg: Ohne Rekursion ginge es mit text == text[::-1] in einer Zeile oder mit einer Schleife,
# die zwei Positionen von außen nach innen wandern lässt (links = 0, rechts = len(text) - 1). Hier
# soll aber das Verkleinern des Problems geübt werden.
# Typische Fehler: nur len(text) == 1 als Abbruchbedingung (dann bricht der leere Text bei text[0] mit
# einem IndexError ab, und jeder Text mit gerader Länge landet dort),
# text[1:] statt text[1:-1] (dann wird das letzte Zeichen mehrfach verglichen), return vor dem
# rekursiven Aufruf vergessen (dann kommt None zurück) oder bei gleichen äußeren Zeichen sofort True.
# Laufzeit: höchstens etwa n / 2 Aufrufe; weil jedes Slicing den Text kopiert, sind es insgesamt
# etwa n² / 4 kopierte Zeichen, was bei 800 Zeichen keine Rolle spielt.
