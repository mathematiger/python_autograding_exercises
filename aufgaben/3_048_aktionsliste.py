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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ergaenze_aktion(pfad, person, aufgabe):
    """Hängt eine Aktion als neue Zeile an die Datei an."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lies_aktionen(pfad):
    """Gibt die Aktionen der Datei als Liste von Paaren zurück, ohne Datei eine leere Liste."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
