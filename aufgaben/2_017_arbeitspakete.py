"""Aufgabe 2_017 – Arbeitspakete                                 Stufe 2 ★★☆☆☆

Ein Projekt wird in Arbeitspakete zerlegt: abgegrenzte Teilaufgaben mit
einem Kürzel, einer Bezeichnung und einer geschätzten Dauer in
Arbeitstagen. Die Projektleiterin pflegt die Pakete in einer einfachen
Textdatei, eine Zeile pro Paket, die Felder durch Semikolons getrennt.
Weil mehrere Leute die Datei bearbeiten, stehen manchmal Leerzeichen um
die Felder. Für die Projektbesprechung soll daraus eine ordentliche
Tabelle mit der Gesamtdauer werden.

Schreiben Sie die Funktion `tabelle(zeilen)`. Sie bekommt die Zeilen der
Datei als Liste von Texten und gibt die ganze Tabelle als einen Text
zurück, die Zeilen durch "\\n" getrennt, ohne sie auszugeben:

- zuerst die Kopfzeile KOPF, die schon im Code steht,
- dann für jedes Paket eine Zeile: das Kürzel linksbündig in einer Spalte
  der Breite 6, die Bezeichnung linksbündig in einer Spalte der Breite 20,
  die Tage rechtsbündig in einer Spalte der Breite 5; Leerzeichen um die
  Felder fallen weg,
- eine Bezeichnung mit mehr als 20 Zeichen wird gekürzt: die ersten 17
  Zeichen und dann "...",
- zum Schluss die Zeile mit dem Wort Summe linksbündig in einer Spalte der
  Breite 26 und der Summe aller Tage rechtsbündig in einer Spalte der
  Breite 5.

    zeilen = ["AP1;Anforderungen aufnehmen;3",
              " AP2 ; Datenbank einrichten ; 5",
              "AP3;Schnittstelle zur Buchhaltung;12"]
    print(tabelle(zeilen))

    AP    Bezeichnung          Tage
    AP1   Anforderungen auf...    3
    AP2   Datenbank einrichten    5
    AP3   Schnittstelle zur...   12
    Summe                        20

Grenzen: 0 ≤ len(zeilen) ≤ 1000. Jede Zeile hat genau zwei Semikolons.
Ohne die Leerzeichen außen ist das Kürzel 1 bis 5 Zeichen lang
(Buchstaben und Ziffern), die Bezeichnung 1 bis 40 Zeichen (ohne
Semikolon, innen auch mit Leerzeichen), und die Tage sind eine ganze
Zahl von 0 bis 99. Um jedes Feld dürfen beliebig viele Leerzeichen
stehen.

Hintergrund: Diese Aufgabe verbindet, was Sie schon kennen:

    "AP1;Test;3".split(";")         →  ["AP1", "Test", "3"]     (2_015)
    a, b, c = ["AP1", "Test", "3"]    jedes Element in eine Variable
    "  Test ".strip()               →  "Test"                   (1_013)
    int(" 3 ")                      →  3, Leerzeichen stören int nicht
    "Anforderungen"[:5]             →  "Anfor"                  (1_012)
    f"[{'ab':<5}][{42:>4}]"         →  "[ab   ][  42]"          (2_016)
    "\\n".join(["a", "b"])           →  "a\\nb"                   (2_015)

Sammeln Sie die fertigen Tabellenzeilen in einer Liste und fügen Sie
sie erst am Ende mit "\\n".join zu einem Text zusammen. Die Summe zählen
Sie in der Schleife mit, wie in Aufgabe 2_001.
"""

KOPF = "AP    Bezeichnung          Tage"


def tabelle(zeilen):
    """Gibt die Arbeitspakete aus zeilen als ausgerichtete Tabelle mit Kopf- und Summenzeile zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


zeilen = ["AP1;Anforderungen aufnehmen;3", " AP2 ; Datenbank einrichten ; 5", "AP3;Schnittstelle zur Buchhaltung;12"]
print(tabelle(zeilen))
