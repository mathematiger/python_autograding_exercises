# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_022_lauflaengen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_022_lauflaengen

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
    if text == "":
        return
    aktuell = text[0]
    anzahl = 0
    for zeichen in text:
        if zeichen == aktuell:
            anzahl = anzahl + 1
        else:
            yield aktuell, anzahl
            aktuell = zeichen
            anzahl = 1
    yield aktuell, anzahl


def kodiere(text):
    """Gibt die Liste aller Läufe von text zurück."""
    return list(laeufe(text))


def entpacke(paare):
    """Liefert die Zeichen des ursprünglichen Textes einzeln."""
    for zeichen, anzahl in paare:
        for _ in range(anzahl):
            yield zeichen


print(list(laeufe("AAAABBC")))
print(kodiere("xxyxx"))
print("".join(entpacke([("A", 3), ("b", 1)])))


# Idee: laeufe merkt sich das Zeichen des laufenden Laufs und zählt mit. Kommt ein anderes Zeichen, ist der
# Lauf fertig: yield liefert (zeichen, anzahl), und ein neuer Lauf mit Anzahl 1 beginnt. Nach der Schleife
# fehlt noch der letzte Lauf, der ebenfalls geliefert wird; ein leerer Text liefert gar nichts (ein return
# ohne Wert beendet den Generator sofort). kodiere
# sammelt die Läufe mit list(laeufe(text)). entpacke liefert in zwei verschachtelten Schleifen jedes
# Zeichen anzahl-mal mit yield, darum entsteht nie der ganze Text auf einmal.
#
# Anderer Weg: laeufe über die Indizes mit einer inneren while-Schleife, die das Ende des Laufs sucht
# (wie die Vergleichslösung in den Tests), oder später mit itertools.groupby (Stufe 4). entpacke könnte
# yield zeichen * anzahl liefern, dann wären die Teile aber bis zu 10**9 Zeichen lang; dasselbe gilt für
# for z in zeichen * anzahl, das den Lauf erst ganz zusammensetzt (das bemerken die Tests).
#
# Typische Fehler: den letzten Lauf vergessen, bei leerem Text text[0] lesen (IndexError), in laeufe eine
# Liste mit return zurückgeben statt yield zu benutzen, gleiche Zeichen im ganzen Text zusammenzählen
# statt nur direkt hintereinander, oder in entpacke erst "".join(...) bauen und dann zurückgeben.
#
# Laufzeit: laeufe sieht jedes Zeichen einmal an, O(n) für n Zeichen; entpacke braucht O(1) Schritte je
# geliefertem Zeichen.
