# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_002_begruessung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_002_begruessung

"""Aufgabe 1_002 – Begrüßung                                    Stufe 1 ★☆☆☆☆

Das Programm fragt schon nach dem Namen. Begrüßen Sie die Person mit ihrem Namen.
Gibt man Anna ein, soll das Programm ausgeben:

    Hallo Anna!

Grenzen: Der Name besteht aus 1 bis 30 Buchstaben, auch Umlaute und ß sind
möglich.

Tipp: Texte können Sie mit + zusammenfügen: "Hallo " + name
"""

name = input("Wie heißen Sie? ")

print("Hallo " + name + "!")


# Idee: Den eingegebenen Namen mit + zwischen die festen Textstücke "Hallo " und "!" hängen und das Ganze
# mit print ausgeben.
# Anderer Weg: print("Hallo", name + "!") – print setzt zwischen die beiden Teile selbst ein Leerzeichen.
# Typische Fehler: das Leerzeichen hinter "Hallo" vergessen ("HalloAnna!"), name in Anführungszeichen
# schreiben (dann steht dort wörtlich "name") oder ein Komma vor dem "!" (print setzt dann ein Leerzeichen
# davor: "Hallo Anna !").
