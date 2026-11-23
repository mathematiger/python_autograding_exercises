r"""Aufgabe 3_051 – Ticketexport                                  Stufe 3 ★★★☆☆

Der IT-Service einer Firma arbeitet mit einem Ticketsystem. Für jedes
Ticket ist je nach Priorität eine Lösungsfrist vereinbart (SLA, Service
Level Agreement): bei hoch 4 Stunden, bei mittel 24, bei niedrig 72.
Jeden Morgen exportiert das System die offenen Tickets als CSV-Text.
Weil im Betreff oft Kommas stehen, setzt das System solche Felder in
Anführungszeichen; ein Anführungszeichen im Betreff wird verdoppelt:

    nummer,betreff,prioritaet,stunden
    1041,"Drucker 2. OG, Papierstau",mittel,30
    1042,VPN bricht ab,hoch,2
    1043,"Passwort vergessen, Konto gesperrt",hoch,6
    1044,"Monitor zeigt ""kein Bild"" an",niedrig,80

stunden sagt, wie lange das Ticket schon offen ist. Schreiben Sie zwei
Funktionen, die den CSV-Text bekommen:

- `felder(text)` gibt alle nicht leeren Zeilen als Listen ihrer Felder
  zurück, die Kopfzeile eingeschlossen, ohne die Anführungszeichen des
  CSV-Formats.
- `ueberfaellige(text)` gibt die Tickets zurück, die schon länger offen
  sind als ihre Frist, als Paare (nummer, betreff) in der Reihenfolge
  des Textes. Die Fristen stehen in FRISTEN.

    felder(text)[1]      →  ["1041", "Drucker 2. OG, Papierstau", "mittel", "30"]
    felder(text)[4][1]   →  'Monitor zeigt "kein Bild" an'
    ueberfaellige(text)  →  [("1041", "Drucker 2. OG, Papierstau"),
                             ("1043", "Passwort vergessen, Konto gesperrt"),
                             ("1044", 'Monitor zeigt "kein Bild" an')]

Je nach Version des Ticketsystems stehen die Spalten in einer anderen
Reihenfolge; verlassen Sie sich in ueberfaellige also auf die Kopfzeile.
Zerlegen Sie die Zeilen nicht selbst mit split, sondern mit dem Modul
csv.

Grenzen: Der Text beginnt mit der Kopfzeile aus genau den Spalten
nummer, betreff, prioritaet und stunden in beliebiger Reihenfolge.
Danach kommen 0 bis 10 000 Tickets; dazwischen und am Ende können leere
Zeilen stehen. Die Zeilen sind durch "\n" getrennt, die letzte kann mit
oder ohne "\n" enden. nummer und betreff sind nicht leere Texte ohne
Zeilenumbruch; im Betreff kommen Kommas, Anführungszeichen und Umlaute
vor. prioritaet ist hoch, mittel oder niedrig, stunden eine ganze Zahl
von 0 bis 10 000.

Hintergrund: In Aufgabe 3_050 haben Sie CSV mit split(",") zerlegt. Das
geht schief, sobald ein Feld selbst ein Komma enthält. Das Modul csv
kennt die Regeln des Formats: Ein Feld in Anführungszeichen darf Kommas
enthalten, und "" darin steht für ein einzelnes Anführungszeichen.
csv.reader bekommt etwas, das Zeilen liefert, und gibt jede Zeile als
Liste von Texten zurück; eine leere Zeile wird zur leeren Liste:

    import csv
    import io

    text = 'name,ort\n"Meier, Ada",Köln\n'
    for zeile in csv.reader(io.StringIO(text)):
        print(zeile)              # ['name', 'ort'], dann ['Meier, Ada', 'Köln']

io.StringIO(text) macht aus einem Text etwas, das sich wie eine
geöffnete Datei lesen lässt. Eine echte Datei öffnet man für csv mit
open(pfad, encoding="utf-8") wie in Aufgabe 3_046, aber zusätzlich mit
newline="" (warum, zeigt die nächste Aufgabe).
csv.DictReader liest die Kopfzeile selbst und gibt jede weitere Zeile
als Dictionary Spaltenname → Wert zurück; leere Zeilen überspringt er:

    for zeile in csv.DictReader(io.StringIO(text)):
        print(zeile["ort"])       # Köln

Alle Werte sind Texte; Zahlen wandeln Sie selbst mit int um.
"""

import csv
import io

FRISTEN = {"hoch": 4, "mittel": 24, "niedrig": 72}  # Lösungsfrist in Stunden


def felder(text):
    """Gibt alle nicht leeren Zeilen des CSV-Texts als Listen ihrer Felder zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ueberfaellige(text):
    """Gibt die Paare (nummer, betreff) der Tickets zurück, die länger als ihre Frist offen sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


text = (
    "nummer,betreff,prioritaet,stunden\n"
    '1041,"Drucker 2. OG, Papierstau",mittel,30\n'
    "1042,VPN bricht ab,hoch,2\n"
    '1043,"Passwort vergessen, Konto gesperrt",hoch,6\n'
    '1044,"Monitor zeigt ""kein Bild"" an",niedrig,80\n'
)
print(felder(text)[1])
print(ueberfaellige(text))
