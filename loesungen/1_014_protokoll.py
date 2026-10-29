# Musterlösung, automatisch erzeugt aus lehrkraft/muster/1_014_protokoll.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 1_014_protokoll

"""Aufgabe 1_014 – Protokoll schwärzen                            Stufe 1 ★☆☆☆☆

Der IT-Support einer Firma schickt ein Störungsprotokoll an einen externen
Dienstleister. Nach dem Grundsatz der Datensparsamkeit soll der Dienstleister
nicht erfahren, wer die Störung gemeldet hat. Deshalb wird der Name im
Protokoll überall durch *** ersetzt; man sagt, er wird geschwärzt. Damit
man sieht, ob das geklappt hat, zeigt das Programm auch an, wie oft der
Name vorkam und ob im geschwärzten Text noch ein @ steht, also
wahrscheinlich eine E-Mail-Adresse, die man von Hand entfernen muss.

Das Programm fragt schon nach dem Protokoll und dem Namen und gibt das
Ergebnis aus. Ergänzen Sie die drei Zeilen, die die Variablen anzahl,
geschwaerzt und mit_adresse füllen. Bei den Eingaben "Meier meldet:
Drucker defekt. Meier bittet um Rückruf an meier@firma.de" und "Meier"
soll das Programm ausgeben:

    Der Name kam 2-mal vor.
    Geschwärzt: *** meldet: Drucker defekt. *** bittet um Rückruf an meier@firma.de
    Noch ein @ im Text: True

Grenzen: Das Protokoll ist ein Text aus 1 bis 300 Zeichen, der Name ein Text
aus 1 bis 30 Zeichen.

Hintergrund: Drei weitere Werkzeuge für Texte: text.count("a") zählt, wie
oft "a" in text vorkommt. text.replace("alt", "neu") liefert einen neuen
Text, in dem jedes "alt" durch "neu" ersetzt ist; text selbst bleibt
unverändert. Und "a" in text ist True, wenn "a" irgendwo in text steht,
sonst False. True und False sind keine Texte, sondern Wahrheitswerte (mehr
dazu in Aufgabe 1_016). Alle drei unterscheiden Groß- und Kleinschreibung: In der
E-Mail-Adresse meier@firma.de steht "meier" klein, das zählt also nicht als
"Meier".

Tipp: Zählen Sie den Namen im ursprünglichen Protokoll, nicht im
geschwärzten Text.
"""

protokoll = input("Protokoll: ")
name = input("Name: ")

anzahl = protokoll.count(name)
geschwaerzt = protokoll.replace(name, "***")
mit_adresse = "@" in geschwaerzt

print(f"Der Name kam {anzahl}-mal vor.")
print("Geschwärzt:", geschwaerzt)
print("Noch ein @ im Text:", mit_adresse)


# Idee: protokoll.count(name) zählt im ursprünglichen Protokoll, protokoll.replace(name, "***") liefert
# den geschwärzten Text, und "@" in geschwaerzt prüft, ob danach noch ein @ übrig ist.
# Anderer Weg: die Anzahl hinterher aus dem geschwärzten Text bestimmen, geschwaerzt.count("***") – das
# stimmt aber nur, wenn im Protokoll nicht schon vorher *** stand, und ein Test prüft genau diesen Fall.
# Typische Fehler: im geschwärzten Text zählen (dann ist der Name schon weg: 0-mal), das @ im
# ursprünglichen Protokoll suchen (dann zählt auch ein @ im Namen mit) oder replace aufrufen, ohne das
# Ergebnis zu speichern.
