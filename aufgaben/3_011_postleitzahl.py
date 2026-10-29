"""Aufgabe 3_011 – Testfälle für die Postleitzahl                 Stufe 3 ★★★☆☆

Ein Onlineshop prüft im Bestellformular die Postleitzahl, bevor die
Bestellung abgeschickt wird. Ist sie ungültig, erscheint neben dem
Eingabefeld ein roter Hinweis. Die Prüfung übernimmt die Funktion
`ist_plz(eingabe)`, die schon im Code steht. Ihre Beschreibung:

- Leerzeichen am Anfang und am Ende der Eingabe werden ignoriert, weil
  sie beim Kopieren oft mit hineingeraten.
- Was dann übrig bleibt, muss aus genau fünf Ziffern 0 bis 9 bestehen.
  Auch eine 0 am Anfang ist erlaubt, etwa 01067 für Dresden.
- Dann ist das Ergebnis True, sonst False. Die Funktion löst nie eine
  Ausnahme aus, auch nicht bei einer leeren Eingabe.

    ist_plz("33098")      →  True
    ist_plz(" 33098 ")    →  True
    ist_plz("3309")       →  False
    ist_plz("33 098")     →  False

Die Funktion soll noch oft geändert werden, etwa für Postleitzahlen
anderer Länder. Damit dabei nichts kaputtgeht, braucht sie Testfälle.
Schreiben Sie die Funktion `testfaelle()`, die eine Liste von Testfällen
zurückgibt. Jeder Testfall ist ein Tupel (eingabe, erwartet), zum
Beispiel ("33098", True).

Die Tests dieser Aufgabe prüfen Ihre Testfälle: Alle müssen mit der
richtigen ist_plz übereinstimmen. Außerdem haben die Tests einige
fehlerhafte Fassungen von ist_plz, wie sie beim Programmieren leicht
entstehen. Jede davon muss an mindestens einem Ihrer Testfälle
scheitern, entweder mit einem falschen Ergebnis oder mit einer Ausnahme.

Grenzen: Die Liste hat 1 bis 100 Testfälle. Jede eingabe ist ein Text aus
0 bis 20 Zeichen, jedes erwartet ist True oder False.

Hintergrund: Ein Testfall legt eine Eingabe fest und das Ergebnis, das
laut Beschreibung herauskommen muss, und zwar bevor man den Code
ansieht. Gute Testfälle findet man, indem man die Beschreibung Satz für
Satz durchgeht und sich fragt, was ein Programmierer an dieser Stelle
falsch machen könnte. Besonders oft gehen Randfälle schief:

- die leere Eingabe "" (und eine, die nur aus Leerzeichen besteht),
- Eingaben direkt an einer Grenze: vier, fünf und sechs Ziffern,
- Sonderfälle aus der Beschreibung: die 0 am Anfang, Leerzeichen am Rand,
- Zeichen, die nicht erlaubt sind: Buchstaben, Leerzeichen in der Mitte.

Ein Test mit "33098" allein beweist wenig: Auch eine Funktion, die immer
True liefert, besteht ihn. Ein Testfall ist erst dann wertvoll, wenn eine
falsche Funktion an ihm scheitert. Genau so arbeiten die Tests dieser
Aufgabe: Sie geben Ihren Testfällen absichtlich falsche Funktionen und
schauen, ob Ihre Testfälle das merken.

Tipp: Mit dem Programm unten sehen Sie, was die richtige ist_plz für Ihre
Testfälle liefert.
"""


def ist_plz(eingabe):
    """Gibt True zurück, wenn eingabe ohne Leerzeichen am Rand aus genau fünf Ziffern besteht."""
    plz = eingabe.strip(" ")
    if len(plz) != 5:
        return False
    for zeichen in plz:
        if zeichen not in "0123456789":
            return False
    return True


def testfaelle():
    """Gibt eine Liste von Testfällen (eingabe, erwartet) für ist_plz zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for eingabe, erwartet in testfaelle():
    print(f"ist_plz({eingabe!r}) ergibt {ist_plz(eingabe)}, erwartet: {erwartet}")
