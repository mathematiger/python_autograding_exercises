"""Aufgabe 4_018 – Abfragen                                      Stufe 4 ★★★★☆

Eine Firma probiert ihre Kundenverwaltung mit Testdaten ohne
Datenbankserver aus: Eine Tabelle ist eine Liste von Dictionaries, jedes
Dictionary eine Zeile, die Schlüssel sind die Spaltennamen. Damit die Kolleginnen und Kollegen nicht
für jede Frage eine Schleife schreiben müssen, sollen drei Funktionen
nachbilden, was in SQL SELECT … FROM … WHERE … tut: Zeilen nach Bedingungen
auswählen (WHERE) und nur bestimmte Spalten behalten (SELECT).

    kunden = [
        {"nr": 1, "name": "Ada", "ort": "Bonn", "status": "aktiv"},
        {"nr": 2, "name": "Bo", "ort": "Jena", "status": "aktiv"},
        {"nr": 3, "name": "Cem", "ort": "Bonn", "status": "gesperrt"},
    ]

Vervollständigen Sie:

- `filtere(tabelle, **bedingungen)` gibt die Liste der Zeilen zurück, in
  denen jede Spalte aus bedingungen genau den angegebenen Wert hat, in der
  Reihenfolge der Tabelle. Ohne Bedingungen passen alle Zeilen. Hat eine
  Zeile eine genannte Spalte nicht, passt sie nicht.
- `waehle(tabelle, *spalten)` gibt für jede Zeile ein neues Dictionary
  zurück, das nur die genannten Spalten enthält, in der Reihenfolge von
  spalten. Ohne Spalten enthält es alle Spalten der Zeile (eine Kopie,
  etwa mit dict(zeile)).
  Fehlt eine genannte Spalte in einer Zeile, löst die Funktion einen
  ValueError aus, dessen Meldung den Spaltennamen enthält.
- `abfrage(tabelle, *spalten, **bedingungen)` filtert zuerst und wählt
  dann die Spalten aus. Sie reicht dafür ihre Argumente an filtere und
  waehle weiter, statt deren Arbeit noch einmal selbst zu machen.

    filtere(kunden, ort="Bonn")                       →  die Zeilen von Ada und Cem
    filtere(kunden, ort="Bonn", status="aktiv")       →  nur die Zeile von Ada
    waehle(kunden, "name", "nr")                      →  [{"name": "Ada", "nr": 1}, {"name": "Bo", "nr": 2},
                                                          {"name": "Cem", "nr": 3}]
    abfrage(kunden, "name", status="aktiv")           →  [{"name": "Ada"}, {"name": "Bo"}]
    waehle(kunden, "telefon")                         →  ValueError: Spalte telefon fehlt

Grenzen: tabelle hat 0 bis 100 000 Zeilen mit je 1 bis 20 Spalten. Die
Spaltennamen sind Bezeichner aus Kleinbuchstaben und Unterstrichen, aber
nie "tabelle"; die Werte sind ganze Zahlen von -10**9 bis 10**9 oder
Texte mit höchstens 50 Zeichen. Die Zeilen müssen nicht alle dieselben
Spalten haben. Es gibt 0 bis 20 Bedingungen und 0 bis 20 Spalten ohne
Wiederholung; sie dürfen Spalten nennen, die in keiner Zeile vorkommen.
Die Tabelle bleibt unverändert.

Hintergrund: Manche Funktionen sollen beliebig viele Argumente annehmen,
so wie print. Ein Stern vor einem Parameter sammelt alle übrigen
Positionsargumente in einem Tupel, zwei Sterne sammeln alle übrigen
Schlüsselwortargumente in einem Dictionary:

    def zeige(titel, *werte, **optionen):
        print(titel, werte, optionen)

    zeige("Bericht", 3, 5, trenner=";", breite=10)
    # Bericht (3, 5) {'trenner': ';', 'breite': 10}
    zeige("Leer")
    # Leer () {}

Die Namen args und kwargs sind nur üblich, nicht vorgeschrieben; es
zählen die Sterne. Die Reihenfolge in der Parameterliste ist fest: erst
die normalen Parameter, dann *werte, dann **optionen (dazwischen
können noch Nur-Schlüsselwort-Parameter stehen, Aufgabe 4_020). Bei
zeige("Bericht", titel="x") gibt es einen TypeError, weil titel schon
belegt ist; deshalb darf hier keine Spalte "tabelle" heißen.

Beim Aufruf funktionieren die Sterne umgekehrt: Sie packen ein Tupel
oder eine Liste in einzelne Positionsargumente aus und ein Dictionary in
einzelne Schlüsselwortargumente:

    werte = (3, 5)
    optionen = {"trenner": ";"}
    zeige("Bericht", *werte, **optionen)   # wie zeige("Bericht", 3, 5, trenner=";")

Damit kann eine Funktion ihre gesammelten Argumente unverändert an eine
andere weiterreichen, ohne zu wissen, welche es sind:

    def mit_titel(*args, **kwargs):
        print("== Auswertung ==")
        return zeige(*args, **kwargs)

So sind viele Hüllfunktionen gebaut, zum Beispiel Dekoratoren, die in
Aufgabe 4_022 kommen. Ohne Sterne müsste man werte als
eine Liste übergeben (zeige("Bericht", [3, 5])), und die gesammelten
Argumente kämen beim Weiterreichen als ein einziges Tupel an.
"""


def filtere(tabelle, **bedingungen):
    """Gibt die Zeilen zurück, in denen jede Spalte aus bedingungen den angegebenen Wert hat."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def waehle(tabelle, *spalten):
    """Gibt für jede Zeile ein neues Dictionary mit den genannten Spalten zurück (ohne Spalten: alle)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def abfrage(tabelle, *spalten, **bedingungen):
    """Filtert die Tabelle nach bedingungen und wählt dann die Spalten aus."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kunden = [
    {"nr": 1, "name": "Ada", "ort": "Bonn", "status": "aktiv"},
    {"nr": 2, "name": "Bo", "ort": "Jena", "status": "aktiv"},
    {"nr": 3, "name": "Cem", "ort": "Bonn", "status": "gesperrt"},
]
print(len(filtere(kunden, ort="Bonn")), len(filtere(kunden, ort="Bonn", status="aktiv")))
print(waehle(kunden, "name", "nr"))
print(abfrage(kunden, "name", status="aktiv"))
