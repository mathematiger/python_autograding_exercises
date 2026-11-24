# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_060_materialliste.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_060_materialliste

"""Aufgabe 2_060 – Materialliste                                  Stufe 2 ★★☆☆☆

Bevor eine Servicetechnikerin zu einem Kunden fährt, um dort Arbeitsplätze
einzurichten, packt sie ihren Werkstattkoffer: Patchkabel, Netzteile,
SSDs, Kabelbinder. Damit nichts fehlt, stellt sie vorher eine
Materialliste zusammen und ändert sie oft mehrmals, weil das Ticket noch
ergänzt wird. Schreiben Sie dafür ein kleines Konsolenprogramm. Die Liste
ist ein Dictionary: Schlüssel ist der Artikel, Wert die Anzahl, etwa
{"Patchkabel": 10, "SSD": 1}.

1. Schreiben Sie die vier Funktionen. Sie fragen nichts und geben nichts
   aus (wie die berechne-Funktionen in Aufgabe 2_037), alles kommt über
   die Parameter:

   - hinzufuegen(liste, artikel, anzahl) erhöht die Anzahl von artikel
     im Dictionary liste um anzahl. Steht der Artikel noch nicht darin,
     kommt er mit dieser Anzahl dazu. Die Funktion ändert liste selbst und
     braucht kein return.
   - entnehmen(liste, artikel, anzahl) verringert die Anzahl von artikel
     um anzahl. Bleibt dabei 0 oder weniger übrig, verschwindet der
     Artikel ganz aus der Liste. Sie gibt True zurück, wenn der Artikel auf
     der Liste stand, sonst False; dann bleibt die Liste unverändert.
   - gesamtzahl(liste) gibt zurück, wie viele Teile insgesamt auf der
     Liste stehen.
   - positionen(liste) gibt eine Liste von Tupeln (artikel, anzahl)
     zurück, sortiert nach dem Artikel, so wie sorted Texte ordnet.

       liste = {}
       hinzufuegen(liste, "Patchkabel", 6)     # liste: {"Patchkabel": 6}
       hinzufuegen(liste, "SSD", 2)
       hinzufuegen(liste, "Patchkabel", 4)     # liste: {"Patchkabel": 10, "SSD": 2}
       entnehmen(liste, "SSD", 1)              →  True
       entnehmen(liste, "Maus", 1)             →  False
       gesamtzahl(liste)                       →  11
       positionen(liste)                       →  [("Patchkabel", 10), ("SSD", 1)]

2. Schreiben Sie darunter das Hauptprogramm. Es zeigt dieses Menü:

       ==============================
                MATERIALLISTE
       ==============================
       1 – Material hinzufügen
       2 – Material entnehmen
       3 – Liste anzeigen
       0 – Programm beenden

   und liest die Auswahl mit input ein. Nach jeder Aktion erscheint das
   Menü wieder, bis jemand 0 wählt. Bei jeder anderen Eingabe gibt es einen
   Hinweis und das Menü erneut. Die Liste ist zu Beginn leer und bleibt
   über alle Menüdurchläufe erhalten.

   - Bei 1 fragt das Programm nach Artikel und Anzahl und ruft hinzufuegen
     auf.
   - Bei 2 fragt es nach Artikel und Anzahl und ruft entnehmen auf. Stand
     der Artikel nicht auf der Liste, gibt es einen Hinweis aus, in dem der
     Artikel genannt wird.
   - Bei 3 gibt es jede Position in einer Zeile „Artikel: Anzahl“ aus, in
     der Reihenfolge von positionen, und darunter eine Zeile, die mit
     „Gesamt“ beginnt und die Gesamtzahl nennt. Ist die Liste leer, gibt es
     stattdessen einen Satz mit dem Wort „leer“ aus.

   Mit den Eingaben 1, Patchkabel, 6, 1, SSD, 2, 1, Patchkabel, 4, 2, SSD,
   1, 3 und 0 zeigt die Liste:

       Patchkabel: 10
       SSD: 1
       Gesamt: 11 Teile

Wie die Hinweise genau lauten, entscheiden Sie.

Grenzen: Ein Artikel ist ein nicht leerer Text mit höchstens 30 Zeichen
ohne Doppelpunkt; Groß- und Kleinschreibung zählt („SSD“ und „ssd“ sind
verschiedene Artikel). Die Anzahl ist eine ganze Zahl mit
1 ≤ anzahl ≤ 1000, die Eingaben dafür sind gültig. Ein Programmlauf hat
höchstens 1000 Aktionen. Die Menüauswahl kann ein beliebiger Text sein.

Hintergrund: Hier fügen Sie Bekanntes zu einem kleinen Programm mit
Zustand zusammen. Das Menü ist eine while-Schleife wie in Aufgabe 2_037.
Der Zustand ist das Dictionary: Legen Sie es einmal vor der Schleife an
(liste = {}); legten Sie es in der Schleife an, finge jeder Durchlauf mit
einer leeren Liste an. Eine Funktion, die das Dictionary bekommt, ändert
dasselbe Objekt, das das Hauptprogramm hat (Aufgabe 2_019); darum braucht
hinzufuegen kein return. Zum Hochzählen mit get und Standardwert siehe
Aufgabe 2_026. Neu ist nur das Entfernen eines Schlüssels:

    del liste["SSD"]        # Schlüssel und Wert sind weg

Vorher prüfen Sie mit "SSD" in liste, ob er da ist, sonst gibt es einen
KeyError. sorted(liste.items()) liefert die Paare (Schlüssel, Wert) nach
dem Schlüssel sortiert.

Tipp: Testen Sie jede Funktion zuerst für sich, etwa mit
print(positionen({"SSD": 1, "Kabel": 3})), bevor Sie das Menü bauen.
"""


def hinzufuegen(liste, artikel, anzahl):
    """Erhöht die Anzahl von artikel in liste um anzahl; ein neuer Artikel kommt dazu."""
    liste[artikel] = liste.get(artikel, 0) + anzahl


def entnehmen(liste, artikel, anzahl):
    """Verringert die Anzahl von artikel; gibt False zurück, wenn er nicht auf der Liste steht."""
    if artikel not in liste:
        return False
    rest = liste[artikel] - anzahl
    if rest > 0:
        liste[artikel] = rest
    else:
        del liste[artikel]
    return True


def gesamtzahl(liste):
    """Gibt zurück, wie viele Teile insgesamt auf der Liste stehen."""
    summe = 0
    for anzahl in liste.values():
        summe = summe + anzahl
    return summe


def positionen(liste):
    """Gibt die Tupel (artikel, anzahl) nach dem Artikel sortiert zurück."""
    return sorted(liste.items())


liste = {}
auswahl = ""
while auswahl != "0":
    print("=" * 30)
    print("MATERIALLISTE".center(30))
    print("=" * 30)
    print("1 – Material hinzufügen")
    print("2 – Material entnehmen")
    print("3 – Liste anzeigen")
    print("0 – Programm beenden")
    auswahl = input("Ihre Auswahl: ")
    if auswahl == "1":
        artikel = input("Artikel: ")
        anzahl = int(input("Anzahl: "))
        hinzufuegen(liste, artikel, anzahl)
    elif auswahl == "2":
        artikel = input("Artikel: ")
        anzahl = int(input("Anzahl: "))
        if not entnehmen(liste, artikel, anzahl):
            print(f"{artikel} steht nicht auf der Liste.")
    elif auswahl == "3":
        if liste:
            for artikel, anzahl in positionen(liste):
                print(f"{artikel}: {anzahl}")
            print(f"Gesamt: {gesamtzahl(liste)} Teile")
        else:
            print("Die Materialliste ist leer.")
    elif auswahl != "0":
        print("Ungültige Auswahl. Bitte geben Sie 1, 2, 3 oder 0 ein.")


# Idee: Das Dictionary liste wird einmal vor der Menüschleife angelegt und ist der ganze Zustand des
# Programms. hinzufuegen setzt liste[artikel] = liste.get(artikel, 0) + anzahl, entnehmen prüft zuerst
# mit in, rechnet den Rest aus und löscht den Schlüssel mit del, wenn nichts übrig bleibt.
# gesamtzahl summiert liste.values(), positionen ist sorted(liste.items()). Das Hauptprogramm ist
# ein Menü wie in Aufgabe 2_037 und ruft nur diese Funktionen auf.
#
# Anderer Weg: In hinzufuegen mit if artikel in liste: ... else: liste[artikel] = anzahl statt get;
# gesamtzahl als sum(liste.values()); in entnehmen liste.pop(artikel) statt del. Die Anzeige kann
# auch über sorted(liste) laufen und die Anzahl mit liste[artikel] holen.
#
# Typische Fehler: liste = {} in die Schleife schreiben (dann ist die Liste nach jeder Aktion leer),
# liste[artikel] = anzahl ohne Aufaddieren, eine Anzahl 0 oder eine negative Anzahl stehen lassen,
# liste[artikel] ohne vorherige Prüfung lesen (KeyError bei unbekannten Artikeln), in den Funktionen
# print statt return, die Auswahl mit int(input()) lesen (dann stürzt „abc“ ab).
