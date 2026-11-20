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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print("12.02.2021", ist_palindrom(nur_ziffern("12.02.2021")))
print("01.01.2025", ist_palindrom(nur_ziffern("01.01.2025")))
print("22.02.2022", ist_palindrom(nur_ziffern("22.02.2022")))
