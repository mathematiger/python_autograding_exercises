# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_017_logauswertung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_017_logauswertung

"""Aufgabe 3_017 – Logauswertung                                 Stufe 3 ★★★☆☆

Ein Überwachungsprogramm (Monitoring) beobachtet die Server einer Firma.
Es schreibt jede Beobachtung als Zeile in ein Protokoll, ein Log: zuerst
die Uhrzeit, dann die Stufe, also wie ernst die Meldung ist (INFO,
WARNUNG, FEHLER …), dann der Text der Meldung. Außerdem misst es jede
Minute, wie viele Anfragen ein Server bearbeitet. Das Bereitschaftsteam
will daraus schnell Listen ziehen, ohne jedes Mal eine Schleife zu
schreiben.

Schreiben Sie drei Funktionen, jede mit einer List Comprehension und ohne
for-Schleife und ohne append:

- `meldungen(zeilen, stufe)`: Gibt die Texte aller Zeilen mit dieser
  Stufe zurück, in ihrer Reihenfolge. Eine Zeile hat die Form
  "<Uhrzeit> <STUFE> <Text>", jeweils durch genau ein Leerzeichen
  getrennt; der Text kann selbst Leerzeichen enthalten.
- `auslastung(anfragen, kapazitaet)`: Gibt zu jedem Messwert die
  Auslastung in Prozent zurück, abgerundet auf eine ganze Zahl
  (anfrage * 100 // kapazitaet).
- `spitzen(anfragen, grenze)`: Gibt die Positionen (ab 0) aller Messwerte
  zurück, die größer als grenze sind.

    zeilen = ["04:30:12 INFO Sicherung gestartet",
              "04:31:05 FEHLER Festplatte /dev/sdb voll",
              "04:32:40 WARNUNG CPU-Temperatur 81 Grad",
              "04:35:00 FEHLER Dienst mail antwortet nicht"]
    meldungen(zeilen, "FEHLER")
        →  ["Festplatte /dev/sdb voll", "Dienst mail antwortet nicht"]
    auslastung([150, 600, 480, 0], 600)   →  [25, 100, 80, 0]
    spitzen([150, 600, 480, 0], 450)      →  [1, 2]

Grenzen: zeilen und anfragen haben 0 bis 100 000 Einträge. Uhrzeit und
Stufe enthalten keine Leerzeichen, der Text ist nicht leer. Die Stufe im
Aufruf ist ein Wort aus Großbuchstaben. 1 ≤ kapazitaet ≤ 10**6, jeder
Messwert und grenze sind ganze Zahlen von 0 bis kapazitaet.

Hintergrund: Eine List Comprehension baut eine neue Liste in einer
einzigen Zeile. Statt

    quadrate = []
    for x in zahlen:
        if x > 0:
            quadrate.append(x * x)

schreibt man

    quadrate = [x * x for x in zahlen if x > 0]

Man liest sie wie in der Mathematik: „x mal x für jedes x aus zahlen,
für das x > 0 ist“. Vorne steht der Ausdruck, der in die neue Liste
kommt (das Abbilden), dann die for-Klausel, und am Ende kann ein if
stehen, das Elemente auslässt (das Filtern). Ohne if kommt für jedes
Element genau eines in die Liste. Die for-Klausel kann auch auspacken,
etwa [i for i, x in enumerate(zahlen) if x == 0] (enumerate aus Aufgabe
2_021). Die ursprüngliche Liste bleibt dabei unverändert.

Tipp: zeile.split(" ", 2) teilt nur an den ersten beiden Leerzeichen und
liefert drei Teile: Uhrzeit, Stufe, Text. Ein Teil davon ist
zeile.split(" ", 2)[2].
"""


def meldungen(zeilen, stufe):
    """Gibt die Texte der Zeilen mit der Stufe stufe zurück."""
    return [zeile.split(" ", 2)[2] for zeile in zeilen if zeile.split(" ", 2)[1] == stufe]


def auslastung(anfragen, kapazitaet):
    """Gibt die Auslastung jedes Messwerts in ganzen Prozent (abgerundet) zurück."""
    return [anfrage * 100 // kapazitaet for anfrage in anfragen]


def spitzen(anfragen, grenze):
    """Gibt die Positionen der Messwerte über grenze zurück."""
    return [position for position, anfrage in enumerate(anfragen) if anfrage > grenze]


zeilen = [
    "04:30:12 INFO Sicherung gestartet",
    "04:31:05 FEHLER Festplatte /dev/sdb voll",
    "04:32:40 WARNUNG CPU-Temperatur 81 Grad",
    "04:35:00 FEHLER Dienst mail antwortet nicht",
]
print(meldungen(zeilen, "FEHLER"))
print(auslastung([150, 600, 480, 0], 600))
print(spitzen([150, 600, 480, 0], 450))


# Idee: Jede Funktion ist eine einzige List Comprehension. meldungen filtert mit if
# zeile.split(" ", 2)[1] == stufe und bildet auf zeile.split(" ", 2)[2] ab, den Text mit allen
# Leerzeichen. auslastung bildet nur ab: anfrage * 100 // kapazitaet für jede Anfrage. spitzen packt
# mit enumerate Position und Wert aus, filtert mit anfrage > grenze und behält die Position.
#
# Anderer Weg: die gewohnte for-Schleife mit append, die genau dasselbe tut, nur in vier Zeilen. Für
# meldungen kann man auch erst eine Liste der zerlegten Zeilen bauen und daraus filtern:
# [teile[2] for teile in [zeile.split(" ", 2) for zeile in zeilen] if teile[1] == stufe].
#
# Typische Fehler: split() ohne Begrenzung (dann ist der Text in Wörter zerstückelt), stufe in zeile
# statt Vergleich der Stufe (findet das Wort auch im Text), anfrage // kapazitaet * 100 (ergibt fast
# immer 0), >= statt > bei spitzen oder die Werte statt der Positionen zurückgeben.
#
# Laufzeit: O(n) für n Zeilen oder Messwerte; jede Comprehension geht die Liste genau einmal durch.
# Schneller als die Schleife mit append ist sie nur um einen kleinen festen Faktor.
