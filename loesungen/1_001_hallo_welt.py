# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_001_hallo_welt.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_001_hallo_welt

"""Aufgabe 1_001 – Hallo Welt                                   Stufe 1 ★☆☆☆☆

Sie haben auf einem neuen Arbeitsplatzrechner Python eingerichtet und
prüfen mit einem ersten kleinen Programm, ob alles läuft. Lassen Sie Ihr
Programm genau diesen Text ausgeben:

    Hallo Welt!

Hintergrund: print(...) gibt aus, was in den Klammern steht. Ein Text steht
in Anführungszeichen, damit Python ihn nicht für einen Befehl hält; die
Anführungszeichen selbst erscheinen nicht in der Ausgabe. Groß- und
Kleinschreibung, Leerzeichen und Satzzeichen müssen genau stimmen.

Tipp: Mit print("...") geben Sie Text auf dem Bildschirm aus.
"""

print("Hallo Welt!")


# Idee: print gibt den Text in den Anführungszeichen aus, die Anführungszeichen selbst erscheinen nicht.
# Anderer Weg: den Text zuerst in einer Variablen speichern, text = "Hallo Welt!", und dann print(text).
# Typische Fehler: Anführungszeichen vergessen (dann bricht Python mit einem SyntaxError ab), Tippfehler
# wie "Hallo welt!" oder ein fehlendes Ausrufezeichen. Die Prüfung vergleicht Zeichen für Zeichen.
