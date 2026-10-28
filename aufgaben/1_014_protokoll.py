"""Aufgabe 1_014 – Protokoll schwärzen                            Stufe 1 ★☆☆☆☆

Der IT-Support einer Firma schickt ein Störungsprotokoll an einen externen
Dienstleister. Nach dem Datenschutz darf der Dienstleister nicht erfahren,
wer die Störung gemeldet hat. Deshalb wird der Name im
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
sonst False. Alle drei unterscheiden Groß- und Kleinschreibung: In der
E-Mail-Adresse meier@firma.de steht "meier" klein, das zählt also nicht als
"Meier".

Tipp: Zählen Sie den Namen im ursprünglichen Protokoll, nicht im
geschwärzten Text.
"""

protokoll = input("Protokoll: ")
name = input("Name: ")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

print(f"Der Name kam {anzahl}-mal vor.")
print("Geschwärzt:", geschwaerzt)
print("Noch ein @ im Text:", mit_adresse)
