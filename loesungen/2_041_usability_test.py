# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_041_usability_test.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_041_usability_test

"""Aufgabe 2_041 – Usability-Test                                Stufe 2 ★★☆☆☆

Ein Team hat die Eingabemasken einer neuen Bestell-App von
Testpersonen ausprobieren lassen. Bei einem Usability-Test bekommt jede
Person kleine Aufgaben („Anmelden“, „Artikel suchen“ …) und das Team
notiert, wie viele Sekunden sie gebraucht hat und wie oft sie sich
verklickt hat. Die Notizen liegen als Tabelle vor, eine Liste von
Dictionaries mit einer Zeile je Person und Aufgabe:

    protokoll = [
        {"person": "P1", "aufgabe": "Anmelden", "sekunden": 35, "fehlklicks": 1},
        {"person": "P1", "aufgabe": "Suchen", "sekunden": 80, "fehlklicks": 4},
        {"person": "P2", "aufgabe": "Anmelden", "sekunden": 25, "fehlklicks": 0},
        {"person": "P2", "aufgabe": "Suchen", "sekunden": 62, "fehlklicks": 2},
        {"person": "P3", "aufgabe": "Anmelden", "sekunden": 40, "fehlklicks": 0},
    ]

Das Team möchte für jede Aufgabe wissen, wie viel Zeit alle Personen
zusammen gebraucht haben, und auch andere Spalten so auswerten.
Schreiben Sie zwei Funktionen, die ein neues Dictionary zurückgeben
und die Tabelle nicht verändern:

- `summe_je(tabelle, gruppe, spalte)`: für jeden Wert, der in der
  Spalte gruppe vorkommt, die Summe der Spalte spalte über alle Zeilen
  mit diesem Wert.
- `anzahl_je(tabelle, gruppe)`: für jeden Wert der Spalte gruppe, in
  wie vielen Zeilen er vorkommt.

Die Schlüssel stehen in beiden Dictionaries in der Reihenfolge, in der
sie zum ersten Mal in der Tabelle vorkommen.

    summe_je(protokoll, "aufgabe", "sekunden")   →  {"Anmelden": 100, "Suchen": 142}
    summe_je(protokoll, "person", "fehlklicks")  →  {"P1": 5, "P2": 2, "P3": 0}
    anzahl_je(protokoll, "aufgabe")              →  {"Anmelden": 3, "Suchen": 2}

Das Programm unten gibt damit die durchschnittliche Zeit je Aufgabe
aus.

Grenzen: 0 ≤ len(tabelle) ≤ 100 000. Alle Zeilen haben dieselben
Schlüssel, gruppe und spalte sind immer Schlüssel davon. In der Spalte
gruppe stehen Texte, in der Spalte spalte ganze Zahlen von 0 bis
10**6. Groß- und Kleinschreibung zählt. Ihre Lösung soll die Tabelle
nur einmal durchlaufen, also O(n) Schritte brauchen.

Hintergrund: Gruppieren heißt: Zeilen mit demselben Wert in einer
Spalte zusammenfassen und für jede Gruppe eine Kennzahl ausrechnen.
Datenbanken (GROUP BY) und Bibliotheken wie pandas (Stufe 3) können
das fertig, aber von Hand ist es nur ein Dictionary (Aufgabe 2_025):
Der Wert der Gruppe ist der Schlüssel, die Summe bisher der Wert. Für
jede Zeile holt man die bisherige Summe mit get und dem Standardwert 0
(Aufgabe 2_026) und schreibt die neue Summe zurück:

    summen = {}
    for zeile in tabelle:
        schluessel = zeile[gruppe]
        summen[schluessel] = summen.get(schluessel, 0) + zeile[spalte]

Ein Dictionary merkt sich die Reihenfolge, in der seine Schlüssel
angelegt wurden. Wie bei Tabellen als Liste von Dicts (Aufgabe 2_032)
stecken die Namen der Spalten in Variablen, darum funktioniert die
Funktion für jede Spalte. Gruppiert man für jede Gruppe neu über die
ganze Tabelle, dauert es bei vielen verschiedenen Gruppen viel länger:
Das Dictionary schafft es in einem einzigen Durchlauf.
"""


def summe_je(tabelle, gruppe, spalte):
    """Gibt zu jedem Wert der Spalte gruppe die Summe der Spalte spalte zurück."""
    summen = {}
    for zeile in tabelle:
        schluessel = zeile[gruppe]
        summen[schluessel] = summen.get(schluessel, 0) + zeile[spalte]
    return summen


def anzahl_je(tabelle, gruppe):
    """Gibt zu jedem Wert der Spalte gruppe die Anzahl der Zeilen zurück."""
    anzahlen = {}
    for zeile in tabelle:
        schluessel = zeile[gruppe]
        anzahlen[schluessel] = anzahlen.get(schluessel, 0) + 1
    return anzahlen


protokoll = [
    {"person": "P1", "aufgabe": "Anmelden", "sekunden": 35, "fehlklicks": 1},
    {"person": "P1", "aufgabe": "Suchen", "sekunden": 80, "fehlklicks": 4},
    {"person": "P2", "aufgabe": "Anmelden", "sekunden": 25, "fehlklicks": 0},
    {"person": "P2", "aufgabe": "Suchen", "sekunden": 62, "fehlklicks": 2},
    {"person": "P3", "aufgabe": "Anmelden", "sekunden": 40, "fehlklicks": 0},
]
zeiten = summe_je(protokoll, "aufgabe", "sekunden")
anzahlen = anzahl_je(protokoll, "aufgabe")
for aufgabe in zeiten:
    print(f"{aufgabe}: im Schnitt {zeiten[aufgabe] / anzahlen[aufgabe]:.1f} Sekunden")


# Idee: Ein leeres Dictionary anlegen und die Tabelle einmal durchgehen. Für jede Zeile ist zeile[gruppe] der
# Schlüssel; summen.get(schluessel, 0) liefert die bisherige Summe (0 beim ersten Mal), dazu kommt zeile[spalte].
# anzahl_je ist dasselbe, nur kommt jedes Mal 1 dazu statt des Werts.
#
# Anderer Weg: mit if schluessel in summen: … else: summen[schluessel] = … statt get. Oder zuerst alle
# verschiedenen Gruppen sammeln und für jede die Tabelle neu durchlaufen; das braucht bei g Gruppen g
# Durchläufe, also O(n · g) statt O(n) Schritte, und ist bei vielen Gruppen viel zu langsam.
#
# Typische Fehler: summen[schluessel] = zeile[spalte] (überschreibt statt zu addieren, nur der letzte Wert
# bleibt), summen[schluessel] += … ohne vorheriges Anlegen (KeyError beim ersten Vorkommen), zeile["gruppe"]
# mit Anführungszeichen oder das Dictionary außerhalb der Funktion anlegen (dann wächst es von Aufruf zu Aufruf).
