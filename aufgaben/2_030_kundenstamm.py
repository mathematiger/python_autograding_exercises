"""Aufgabe 2_030 – Kundenstamm                                   Stufe 2 ★★☆☆☆

Ein Versandhändler hat seine Kundendaten aus einer Dokumentendatenbank
exportiert. Dort ist jeder Kunde ein Dokument, das wie ein Dictionary
aufgebaut ist und weitere Dictionaries und Listen enthalten darf: die
Adresse als eigenes Dictionary und die Beträge aller Bestellungen als
Liste. Für eine Werbeaktion braucht das Marketing zwei Auswertungen.
Schreiben Sie zwei Funktionen, die beide eine neue Liste zurückgeben
und die Kundendaten nicht verändern:

- `kunden_in(kunden, ort)`: die Namen aller Kunden, deren Adresse im
  Ort ort liegt, in der Reihenfolge der Liste kunden.
- `grosse_bestellungen(kunden, mindestens)`: für jede Bestellung mit
  einem Betrag von mindestens mindestens Euro ein Tupel (name, betrag),
  zuerst alle Bestellungen des ersten Kunden in ihrer Reihenfolge, dann
  die des zweiten und so weiter.

    kunden = [
        {"name": "Ada Weber", "adresse": {"plz": "33098", "ort": "Paderborn"},
         "bestellungen": [120, 35, 260]},
        {"name": "Ben Kaya", "adresse": {"plz": "44135", "ort": "Dortmund"},
         "bestellungen": []},
        {"name": "Cem Ott", "adresse": {"plz": "33100", "ort": "Paderborn"},
         "bestellungen": [99, 100]},
    ]
    kunden_in(kunden, "Paderborn")       →  ["Ada Weber", "Cem Ott"]
    grosse_bestellungen(kunden, 100)     →  [("Ada Weber", 120), ("Ada Weber", 260),
                                             ("Cem Ott", 100)]

Grenzen: 0 ≤ len(kunden) ≤ 10 000. Jeder Kunde hat genau die Schlüssel
"name" (nicht leerer Text), "adresse" (ein Dictionary mit den Schlüsseln
"plz" und "ort", beides nicht leere Texte) und "bestellungen" (eine
Liste mit 0 bis 100 ganzen Zahlen von 1 bis 10**6). Namen dürfen
doppelt vorkommen. ort ist ein nicht leerer Text, mindestens eine ganze
Zahl von 1 bis 10**6. Groß- und Kleinschreibung zählt: "paderborn" ist
ein anderer Ort als "Paderborn".

Hintergrund: Datenstrukturen lassen sich ineinander schachteln: Eine
Liste kann Dictionaries enthalten, ein Dictionary wieder Dictionaries
oder Listen. Man greift dann Stufe für Stufe hinein, von außen nach
innen, und liest den Ausdruck von links nach rechts:

    kunde = kunden[0]                  # das erste Dictionary der Liste
    kunde["adresse"]                   →  {"plz": "33098", "ort": "Paderborn"}
    kunde["adresse"]["ort"]            →  "Paderborn"
    kunde["bestellungen"][-1]          →  260
    kunden[0]["adresse"]["plz"]        →  "33098"   (alles in einem Ausdruck)

Zum Filtern geht man mit for durch die äußere Liste und prüft mit if
einen inneren Wert. Liegt in jedem Element noch eine Liste, braucht man
eine zweite Schleife darin. Die neue Liste baut man mit append auf;
die Dictionaries selbst bleiben dabei unberührt.
"""


def kunden_in(kunden, ort):
    """Gibt die Namen der Kunden zurück, deren Adresse im Ort ort liegt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def grosse_bestellungen(kunden, mindestens):
    """Gibt (name, betrag) für jede Bestellung mit betrag >= mindestens zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kunden = [
    {"name": "Ada Weber", "adresse": {"plz": "33098", "ort": "Paderborn"}, "bestellungen": [120, 35, 260]},
    {"name": "Ben Kaya", "adresse": {"plz": "44135", "ort": "Dortmund"}, "bestellungen": []},
    {"name": "Cem Ott", "adresse": {"plz": "33100", "ort": "Paderborn"}, "bestellungen": [99, 100]},
]
print(kunden_in(kunden, "Paderborn"))
print(grosse_bestellungen(kunden, 100))
