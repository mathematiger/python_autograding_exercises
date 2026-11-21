"""Aufgabe 4_038 – Testdatenquelle                               Stufe 4 ★★★★☆

Ein Entwicklungsteam benutzt eine ältere Bibliothek, die Testdaten für
seine automatischen Tests erzeugt. Ihre Schnittstelle ist unbequem: Es
gibt nur eine Funktion ohne Parameter, die bei jedem Aufruf den nächsten
Testfall zurückgibt und None, wenn keiner mehr kommt. Ein Testfall kann
jeder Wert sein, auch 0, "" oder False. Außerdem kommen große
Testdatensätze als Text aus einem Datenstrom, den man mit
datei.read(anzahl) in Stücken liest; am Ende liefert read den leeren
Text "". Bisher steht überall Code wie dieser:

    def alle_testfaelle(naechster):
        ergebnis = []
        while True:
            fall = naechster()
            if fall is None:
                break
            ergebnis.append(fall)
        return ergebnis

Im Zuge eines Umbaus sollen die Daten nicht mehr als Liste gesammelt,
sondern Stück für Stück abgeholt werden, damit auch sehr lange Quellen
in den Speicher passen. Schreiben Sie dafür zwei Funktionen, jede mit
iter(funktion, endmarke) statt einer while-Schleife:

- `testfaelle(naechster)` gibt einen Iterator über alle Testfälle bis
  zum ersten None zurück (das None selbst nicht). Er ruft naechster erst
  auf, wenn der nächste Wert abgeholt wird.
- `bloecke(datei, groesse)` gibt einen Iterator über die Stücke des
  Datenstroms zurück: jedes Stück hat groesse Zeichen, nur das letzte
  darf kürzer sein; der leere Text am Ende gehört nicht dazu. Auch
  dieser Iterator liest erst, wenn das nächste Stück abgeholt wird.

    werte = iter([3, 0, "", None, 7])
    list(testfaelle(lambda: next(werte)))   →  [3, 0, ""]
    datei = io.StringIO("ABCDEFGH")
    list(bloecke(datei, 3))                 →  ["ABC", "DEF", "GH"]

Grenzen: naechster liefert bis zu 100 000 Werte vor dem ersten None,
danach wird es nicht mehr aufgerufen. Der Datenstrom enthält 0 bis
10**6 Zeichen; 1 ≤ groesse ≤ 10**6.

Hintergrund: Mit einem Argument macht iter(iterable) aus einer Liste
oder einem anderen Iterable einen Iterator (Aufgabe 4_032). Mit zwei
Argumenten macht iter etwas ganz anderes: iter(funktion, endmarke) baut
einen Iterator, der bei jedem next() die Funktion ohne Argumente aufruft
und ihr Ergebnis liefert, bis es gleich (==) der Endmarke ist; dann ist
er erschöpft. Die Endmarke heißt auch Sentinel (Wächter). So ersetzt
eine Zeile die ganze while-True-Schleife mit break:

    import random

    zufall = random.Random(1)
    wuerfe = iter(lambda: zufall.randint(1, 6), 6)   # würfeln bis zur ersten 6
    list(wuerfe)  →  [2, 5, 1, 3, 1, 4, 4, 4]   (die 6 selbst nicht)

Wie bei einem Generator passiert beim Anlegen noch nichts; die Funktion
läuft erst bei next(), in for-Schleifen oder bei list(...). Die Funktion
muss ohne Argumente aufrufbar sein. Braucht sie welche, wie read(3),
legt man sie mit lambda: datei.read(3) oder mit functools.partial
(Aufgabe 4_028) vorher fest:

    from functools import partial
    stueckweise = iter(partial(datei.read, 3), "")

Achtung: Die Endmarke wird mit == verglichen. Ist sie 0, hört der
Iterator auch bei 0.0 und False auf, denn False == 0 ist True; mit None
als Endmarke passiert das nicht. Und kommt die Endmarke nie, endet auch
der Iterator nie.
"""

import io
from functools import partial


def testfaelle(naechster):
    """Gibt einen Iterator über die Werte von naechster() bis zum ersten None zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bloecke(datei, groesse):
    """Gibt einen Iterator über die Stücke von datei mit je groesse Zeichen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


werte = iter([3, 0, "", None, 7])
print(list(testfaelle(lambda: next(werte))))
print(list(bloecke(io.StringIO("ABCDEFGH"), 3)))
