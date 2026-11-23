# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_048_aktionsliste.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_048_aktionsliste

r"""Aufgabe 3_048 – Aktionsliste                                  Stufe 3 ★★★☆☆

Am Ende jeder Projektbesprechung hält die Projektleiterin fest, wer bis
zum nächsten Mal was erledigt: die Aktionsliste. Ein kleines Werkzeug
soll sie in einer Textdatei ablegen, damit sie die nächste Besprechung
wieder öffnen kann. In der Datei steht eine Aktion pro Zeile, erst die
Person, dann ein Semikolon, dann die Aufgabe, und jede Zeile endet mit
einem Zeilenumbruch, auch die letzte:

    Ada;Testserver bestellen
    Bo;Pflichtenheft an den Kunden schicken

Schreiben Sie drei Funktionen, die alle den Pfad der Datei als Text
bekommen:

- `speichere_aktionen(pfad, aktionen)` bekommt eine Liste von Paaren
  (person, aufgabe) und schreibt sie in dieser Form in die Datei. Gibt
  es die Datei schon, wird ihr alter Inhalt ersetzt.
- `ergaenze_aktion(pfad, person, aufgabe)` hängt eine Aktion als neue
  Zeile hinten an die Datei an. Gibt es die Datei noch nicht, legt sie
  sie an.
- `lies_aktionen(pfad)` gibt die Aktionen der Datei als Liste von Paaren
  zurück, in ihrer Reihenfolge; leere Zeilen werden übersprungen. Gibt
  es die Datei noch nicht, ist die Liste leer.

    speichere_aktionen(pfad, [("Ada", "Testserver bestellen")])
    ergaenze_aktion(pfad, "Bo", "Pflichtenheft an den Kunden schicken")
    lies_aktionen(pfad)  →  [("Ada", "Testserver bestellen"), ("Bo", "Pflichtenheft an den Kunden schicken")]

Die Funktionen speichere_aktionen und ergaenze_aktion geben nichts
zurück. Die Tests legen einen leeren Ordner an und geben Ihnen Pfade
darin.

Grenzen: 0 bis 10 000 Aktionen. Person und Aufgabe sind nicht leere
Texte ohne Semikolon und ohne Zeilenumbruch, ohne Leerzeichen am Rand,
Umlaute kommen vor. Der Ordner, in dem die Datei liegt, existiert.

Hintergrund: Wie man eine Datei mit with und encoding="utf-8" liest,
steht in Aufgabe 3_046. Zum Schreiben gibt man open als zweites Argument
den Modus mit: "w" (write) legt die Datei an oder leert eine vorhandene,
"a" (append) hängt hinten an und legt sie an, falls es sie noch nicht
gibt. Ohne Modus gilt "r" (read). datei.write(text) schreibt genau den
Text und hängt, anders als print, keinen Zeilenumbruch an; den hängt
man selbst mit "\n" an:

    with open("notizen.txt", "w", encoding="utf-8") as datei:
        datei.write("erste Zeile\n")
        datei.write(f"{3 * 4} Punkte\n")

    with open("notizen.txt", "a", encoding="utf-8") as datei:
        datei.write("kommt hinten dazu\n")

Erst wenn with endet, ist alles sicher in der Datei. Gibt es beim Lesen
die Datei nicht, löst open einen FileNotFoundError aus; den fangen Sie
mit try/except ab wie in Aufgabe 3_030.
"""


def speichere_aktionen(pfad, aktionen):
    """Schreibt die Aktionen in die Datei und ersetzt einen alten Inhalt."""
    with open(pfad, "w", encoding="utf-8") as datei:
        for person, aufgabe in aktionen:
            datei.write(f"{person};{aufgabe}\n")


def ergaenze_aktion(pfad, person, aufgabe):
    """Hängt eine Aktion als neue Zeile an die Datei an."""
    with open(pfad, "a", encoding="utf-8") as datei:
        datei.write(f"{person};{aufgabe}\n")


def lies_aktionen(pfad):
    """Gibt die Aktionen der Datei als Liste von Paaren zurück, ohne Datei eine leere Liste."""
    aktionen = []
    try:
        with open(pfad, encoding="utf-8") as datei:
            for zeile in datei:
                zeile = zeile.rstrip("\n")
                if zeile == "":
                    continue
                person, aufgabe = zeile.split(";")
                aktionen.append((person, aufgabe))
    except FileNotFoundError:
        return []
    return aktionen



# Idee: speichere_aktionen öffnet die Datei mit dem Modus "w" (leert eine vorhandene) und schreibt für
# jedes Paar f"{person};{aufgabe}\n". ergaenze_aktion macht dasselbe für eine Zeile, aber mit "a", das
# hinten anhängt und eine fehlende Datei anlegt. lies_aktionen liest wie in Aufgabe 3_046 Zeile für
# Zeile, entfernt den Zeilenumbruch, überspringt leere Zeilen und zerlegt den Rest mit split(";") in
# ein Paar; ein FileNotFoundError wird abgefangen und ergibt [].
# Anderer Weg: in speichere_aktionen erst den ganzen Text mit "".join(...) bauen und einmal schreiben;
# lies_aktionen geht auch mit datei.read().splitlines(), und statt try/except kann man vorher mit
# os.path.exists(pfad) (Modul os, hier nicht eingeführt) fragen, ob es die Datei gibt.
# Typische Fehler: "w" in ergaenze_aktion (löscht die alten Aktionen), "\n" vergessen (alles in einer
# Zeile), Leerzeichen um das Semikolon, kein encoding (Umlaute unter Windows kaputt), die leere
# Datei bei [] nicht anlegen, oder den FileNotFoundError nicht abfangen.
# Laufzeit: O(n) für n Zeichen; jede Zeile wird einmal geschrieben bzw. gelesen.
