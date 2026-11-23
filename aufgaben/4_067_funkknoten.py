"""Aufgabe 4_067 – Funkknoten                                    Stufe 4 ★★★★☆

In einem Gewächshaus messen kleine Funkknoten Temperatur und
Luftfeuchte. Jeder Knoten heißt K und eine Nummer mit einer bis vier
Ziffern (K7, K17, K0042). Ein Gateway, also das Gerät, das die Funksignale
empfängt und ans Netz weitergibt, schreibt alles in ein Textprotokoll,
leider in wechselnder Form, weil die Knoten verschiedene Firmware haben:

    [09:35:12] knoten=K17   temp=21.5C feuchte=48%
    [09:35:14] knoten=K3 temp=-2C feuchte=100%  (Kühlraum)
    09:35:20 Gateway: K17 meldet Fehler E42, K3 meldet Fehler E7

Schreiben Sie mit dem Modul re drei Funktionen:

- `knoten(text)` gibt alle Knotennamen im Text als Liste zurück, in der
  Reihenfolge ihres Vorkommens, auch mehrfach. Ein Knotenname ist ein
  großes K mit ein bis vier Ziffern, das als eigenes Wort dasteht: In
  "XK17", "K17a" und "K12345" steckt kein Knotenname, in "K17," und
  "(K3)" schon.
- `messung(zeile)` sucht in der Zeile den Teil
  knoten=<Name> temp=<Zahl>C feuchte=<Ganzzahl>% (zwischen den drei
  Angaben ein oder mehrere Leerzeichen) und gibt ein Dictionary mit den
  Schlüsseln "knoten" (Text), "temp" (float) und "feuchte" (int)
  zurück. Die Temperatur kann ein Minus und Nachkommastellen haben, die
  Feuchte hat ein bis drei Ziffern. Fehlt der Teil, kommt None zurück.
- `fehler(text)` gibt für jede Stelle "<Knoten> meldet Fehler E<Nummer>"
  das Paar (knoten, nummer) zurück, nummer als int.

    knoten("K17 an K3: (K0042) XK9 K12345")  →  ["K17", "K3", "K0042"]
    messung("[09:35:12] knoten=K17   temp=21.5C feuchte=48%")
    →  {"knoten": "K17", "temp": 21.5, "feuchte": 48}
    messung("[09:35:13] knoten=K17 temp=?C")  →  None
    fehler("K17 meldet Fehler E42, K3 meldet Fehler E7")
    →  [("K17", 42), ("K3", 7)]

Grenzen: Die Texte haben 0 bis 100 000 Zeichen; als Ziffern kommen nur 0
bis 9 vor.
In fehler stehen zwischen den Wörtern genau ein Leerzeichen, die Nummer
hat ein bis fünf Ziffern.

Hintergrund: Ein regulärer Ausdruck beschreibt ein Textmuster. Die
meisten Zeichen stehen für sich selbst, einige haben eine Bedeutung:

    \\d        eine Ziffer               \\s    ein Leerzeichen (auch Tab)
    .         ein beliebiges Zeichen    \\.    ein echter Punkt
    x+        x einmal oder öfter       x*    x keinmal oder öfter
    x?        x keinmal oder einmal     x{1,4}  x ein- bis viermal
    [abc]     eines der Zeichen         \\b    Wortgrenze (kein Zeichen)

Man schreibt Muster als rohe Strings r"...", damit Python die
Backslashes nicht selbst deutet. re.search(muster, text) sucht die erste
passende Stelle irgendwo im Text und gibt ein Treffer-Objekt zurück oder
None; re.fullmatch verlangt, dass der ganze Text passt; re.findall gibt
alle passenden Stellen als Liste zurück:

    import re
    re.findall(r"\\d+", "3 Knoten, 12 Werte")   →  ["3", "12"]
    re.search(r"\\d+", "keine Zahl")            →  None

Klammern bilden Gruppen, die man aus dem Treffer einzeln herausholt.
Mit (?P<name>...) bekommt eine Gruppe einen Namen, und groupdict()
liefert alle benannten Gruppen als Dictionary (immer als Texte; umwandeln
müssen Sie selbst):

    treffer = re.search(r"(?P<stunde>\\d\\d):(?P<minute>\\d\\d)", "um 09:35 Uhr")
    treffer.group(0)          →  "09:35"   (die ganze Stelle)
    treffer.group("minute")   →  "35"
    treffer.groupdict()       →  {"stunde": "09", "minute": "35"}

Hat das Muster Gruppen, liefert findall statt der ganzen Stellen die
Gruppen: bei einer Gruppe eine Liste von Texten, bei mehreren eine Liste
von Tupeln.

    re.findall(r"(\\w+)=(\\d+)", "a=1 b=22")    →  [("a", "1"), ("b", "22")]

\\b passt zwischen einem Wortzeichen (Buchstabe, Ziffer, _) und einem
anderen Zeichen oder dem Textrand. r"\\bK\\d{1,4}\\b" findet also K17 in
"(K17)", aber nicht in "XK17" oder "K17a". Klammern, die nur
zusammenfassen und keine Gruppe sein sollen, schreibt man (?:...), etwa
(?:\\.\\d+)? für „vielleicht ein Punkt mit Nachkommastellen“.
"""

import re


def knoten(text):
    """Gibt alle Knotennamen (K mit ein bis vier Ziffern als eigenes Wort) in der Reihenfolge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def messung(zeile):
    """Gibt Knoten, Temperatur und Feuchte der Messung in zeile als Dictionary zurück, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fehler(text):
    """Gibt alle Paare (knoten, nummer) aus "<Knoten> meldet Fehler E<Nummer>" zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(knoten("K17 an K3: (K0042) XK9 K12345"))
print(messung("[09:35:12] knoten=K17   temp=21.5C feuchte=48%"))
print(fehler("09:35:20 Gateway: K17 meldet Fehler E42, K3 meldet Fehler E7"))
