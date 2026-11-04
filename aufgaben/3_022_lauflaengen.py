"""Aufgabe 3_022 – Lauflängen                                   Stufe 3 ★★★☆☆

Eine Firma archiviert verschlüsselte Sicherungen ihrer Personaldaten.
Bevor sie verschlüsselt werden, werden sie komprimiert, damit das
Archiv kleiner wird. Ein sehr einfaches Verfahren dafür ist die
Lauflängenkodierung: Ein Lauf ist eine Folge gleicher Zeichen direkt
hintereinander, und statt "AAAABBC" speichert man die Paare
("A", 4), ("B", 2), ("C", 1). Bei Daten mit vielen Wiederholungen,
etwa Statusbildern aus wenigen Farben, spart das viel Platz. Schreiben
Sie drei Funktionen:

- `laeufe(text)` ist ein Generator: Er liefert mit yield nacheinander
  für jeden Lauf in text das Tupel (zeichen, anzahl), von vorn nach
  hinten.
- `kodiere(text)` gibt die Liste aller Läufe zurück. Benutzen Sie dafür
  laeufe.
- `entpacke(paare)` ist ein Generator: Er bekommt etwas Durchlaufbares
  mit Paaren (zeichen, anzahl) und liefert mit yield die Zeichen des
  ursprünglichen Textes einzeln, ohne den ganzen Text auf einmal
  zusammenzusetzen.

    list(laeufe("AAAABBC"))          →  [("A", 4), ("B", 2), ("C", 1)]
    kodiere("xxyxx")                 →  [("x", 2), ("y", 1), ("x", 2)]
    kodiere("")                      →  []
    "".join(entpacke([("A", 3), ("b", 1)]))  →  "AAAb"

Grenzen: text hat 0 bis 100 000 beliebige Zeichen, Groß- und
Kleinbuchstaben sind verschiedene Zeichen. paare enthält 0 bis 100 000
Paare aus einem einzelnen Zeichen und einer ganzen Zahl von 1 bis
10**9; die Gesamtlänge kann also riesig sein, deshalb darf entpacke
nichts im Voraus berechnen. Ihre Lösung soll O(n) Schritte brauchen.

Hintergrund: Eine Funktion, in der yield vorkommt, ist eine
Generatorfunktion. Ruft man sie auf, läuft noch keine Zeile ihres
Rumpfs; man bekommt einen Generator, einen Iterator (Aufgabe 3_020).
Erst next() lässt den Rumpf bis zum nächsten yield laufen; der Wert
hinter yield ist das Ergebnis von next(), und die Funktion hält genau
dort an, mit allen ihren Variablen. Das nächste next() macht hinter dem
yield weiter. Endet der Rumpf, löst der Generator StopIteration aus.

    def countdown(n):
        while n > 0:
            yield n
            n = n - 1

    for zahl in countdown(3):
        print(zahl)              # 3, 2, 1
    print(list(countdown(2)))    # [2, 1]

Statt eine Liste aufzubauen und am Ende zurückzugeben, liefert ein
Generator also jedes Element, sobald es fertig ist. Das spart Speicher,
und wer nur die ersten Elemente braucht, muss die übrigen nie
berechnen. Wie jeder Iterator ist ein Generator nach einem Durchlauf
verbraucht (Aufgabe 3_021); mit list(...) sammelt man seine Werte in
einer Liste.
"""


def laeufe(text):
    """Liefert für jeden Lauf gleicher Zeichen das Tupel (zeichen, anzahl)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kodiere(text):
    """Gibt die Liste aller Läufe von text zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def entpacke(paare):
    """Liefert die Zeichen des ursprünglichen Textes einzeln."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(list(laeufe("AAAABBC")))
print(kodiere("xxyxx"))
print("".join(entpacke([("A", 3), ("b", 1)])))
