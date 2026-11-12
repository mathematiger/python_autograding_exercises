# Automatisch erzeugt aus lehrkraft/muster/2_032_energiezaehler.py - nicht von Hand ändern.
# vorlage-hash: 3bab93ea5757b261
# text-hash: 941e3a1ae13179e8
# thema: datenanalyse
# inhalt: Tabelle als Liste von Dicts

def beispiel():
    """Baut die Tabelle aus dem Beispiel neu."""
    return [
        {"geraet": "Kaffeemaschine", "raum": "Kueche", "stunde": 8, "wh": 350},
        {"geraet": "Drucker", "raum": "Flur", "stunde": 8, "wh": 40},
        {"geraet": "Kaffeemaschine", "raum": "Kueche", "stunde": 9, "wh": 120},
        {"geraet": "Monitor", "raum": "Buero 1", "stunde": 9, "wh": 30},
    ]


# spalte aus dem Beispiel
daten = beispiel()
ergebnis = spalte(daten, "geraet")
erwartet = ["Kaffeemaschine", "Drucker", "Kaffeemaschine", "Monitor"]
assert ergebnis == erwartet, (
    f'spalte(<Beispiel>, "geraet") ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Hängen Sie für jede Zeile zeile[name] an; der Name der Spalte steckt in der Variablen name."
)

# Eine andere Spalte (nicht fest "geraet" hinschreiben!)
ergebnis = spalte(daten, "wh")
assert ergebnis == [350, 40, 120, 30], f'spalte(<Beispiel>, "wh") ergibt {ergebnis!r}, erwartet war [350, 40, 120, 30].'

# filtere aus dem Beispiel
ergebnis = filtere(daten, "stunde", 9)
erwartet = [beispiel()[2], beispiel()[3]]
assert ergebnis == erwartet, (
    f'filtere(<Beispiel>, "stunde", 9) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Hängen Sie die ganze Zeile an, wenn zeile[name] == wert ist."
)

# summe nach filtere aus dem Beispiel
ergebnis = summe(filtere(daten, "raum", "Kueche"), "wh")
assert ergebnis == 470, f'summe(filtere(<Beispiel>, "raum", "Kueche"), "wh") ergibt {ergebnis!r}, erwartet war 470.'

# summe über eine andere Spalte und die ganze Tabelle
ergebnis = (summe(daten, "wh"), summe(daten, "stunde"))
assert ergebnis == (540, 34), f'summe(<Beispiel>, "wh") und summe(<Beispiel>, "stunde") ergeben {ergebnis!r}, erwartet war (540, 34).'

# Die Tabelle bleibt unverändert
assert daten == beispiel(), f"Nach den Aufrufen ist die Tabelle {daten!r}, erwartet war unverändert {beispiel()!r}."

# filtere liefert eine neue Liste, auch wenn alle Zeilen passen
teil = beispiel()[:2]
ergebnis = filtere(teil, "stunde", 8)
assert ergebnis == teil and ergebnis is not teil, (
    f'filtere(<erste zwei Zeilen>, "stunde", 8) soll eine neue Liste mit beiden Zeilen liefern; bekommen {ergebnis!r}'
    f"{' (die übergebene Tabelle selbst)' if ergebnis is teil else ''}."
)

# Kein Treffer, Groß- und Kleinschreibung, Text gegen Zahl
ergebnis = (filtere(beispiel(), "raum", "Keller"), filtere(beispiel(), "raum", "kueche"), filtere(beispiel(), "stunde", "8"))
assert ergebnis == ([], [], []), (
    f'filtere nach raum "Keller", raum "kueche" und stunde "8" (Text statt Zahl) ergibt {ergebnis!r}, erwartet war ([], [], []).'
)

# Leere Tabelle
ergebnis = (spalte([], "wh"), filtere([], "raum", "Flur"), summe([], "wh"))
assert ergebnis == ([], [], 0), f'spalte, filtere und summe auf einer leeren Tabelle ergeben {ergebnis!r}, erwartet war ([], [], 0).'

# Ränder der Werte: 0 und 10**6
daten = [{"id": "a", "wh": 0}, {"id": "b", "wh": 10**6}, {"id": "c", "wh": 0}]
ergebnis = (summe(daten, "wh"), filtere(daten, "wh", 0), spalte(daten, "id"))
erwartet = (10**6, [daten[0], daten[2]], ["a", "b", "c"])
assert ergebnis == erwartet, f"Für {daten} ergeben summe, filtere(…, 'wh', 0) und spalte(…, 'id') {ergebnis!r}, erwartet war {erwartet!r}."


# Vergleichslösung: über Indizes und mit eingebauten Funktionen
def spalte_von_hand(tabelle, name):
    """Liest die Spalte über die Indizes."""
    return [tabelle[index][name] for index in range(len(tabelle))]


def filtere_von_hand(tabelle, name, wert):
    """Behält die Zeilen, deren Wert nicht verschieden ist."""
    return [tabelle[index] for index in range(len(tabelle)) if not tabelle[index][name] != wert]


# 300 zufällige Tabellen für spalte
zufall = Zufall(2032)
GERAETE = ["Drucker", "Monitor", "Kaffeemaschine", "Lampe", "Router"]
RAEUME = ["Flur", "Kueche", "Buero 1", "Buero 2"]
for _ in range(300):
    daten = []
    for _ in range(zufall.randint(0, 8)):
        daten.append({"geraet": zufall.choice(GERAETE), "raum": zufall.choice(RAEUME),
                      "stunde": zufall.randint(0, 23), "wh": zufall.randint(0, 1000)})
    vorher = repr(daten)
    name = zufall.choice(["geraet", "raum", "stunde", "wh"])
    if daten and zufall.random() < 0.7:
        wert = zufall.choice(daten)[name]
    else:
        wert = zufall.choice(GERAETE + RAEUME + [0, 8, 23])
    ergebnis = spalte(daten, name)
    erwartet = spalte_von_hand(daten, name)
    assert ergebnis == erwartet, f"spalte({daten}, {name!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    zahlspalte = zufall.choice(["stunde", "wh"])
    assert repr(daten) == vorher, f"Die Tabelle wurde verändert: vorher {vorher}, nachher {daten!r}."

# 300 zufällige Tabellen für filtere
zufall = Zufall(2032)
for _ in range(300):
    daten = []
    for _ in range(zufall.randint(0, 8)):
        daten.append({"geraet": zufall.choice(GERAETE), "raum": zufall.choice(RAEUME),
                      "stunde": zufall.randint(0, 23), "wh": zufall.randint(0, 1000)})
    vorher = repr(daten)
    name = zufall.choice(["geraet", "raum", "stunde", "wh"])
    if daten and zufall.random() < 0.7:
        wert = zufall.choice(daten)[name]
    else:
        wert = zufall.choice(GERAETE + RAEUME + [0, 8, 23])
    ergebnis = filtere(daten, name, wert)
    erwartet = filtere_von_hand(daten, name, wert)
    assert ergebnis == erwartet, f"filtere({daten}, {name!r}, {wert!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    zahlspalte = zufall.choice(["stunde", "wh"])
    assert repr(daten) == vorher, f"Die Tabelle wurde verändert: vorher {vorher}, nachher {daten!r}."

# 300 zufällige Tabellen für summe
zufall = Zufall(2032)
for _ in range(300):
    daten = []
    for _ in range(zufall.randint(0, 8)):
        daten.append({"geraet": zufall.choice(GERAETE), "raum": zufall.choice(RAEUME),
                      "stunde": zufall.randint(0, 23), "wh": zufall.randint(0, 1000)})
    vorher = repr(daten)
    name = zufall.choice(["geraet", "raum", "stunde", "wh"])
    if daten and zufall.random() < 0.7:
        wert = zufall.choice(daten)[name]
    else:
        wert = zufall.choice(GERAETE + RAEUME + [0, 8, 23])
    zahlspalte = zufall.choice(["stunde", "wh"])
    ergebnis = summe(daten, zahlspalte)
    erwartet = sum(spalte_von_hand(daten, zahlspalte))
    assert ergebnis == erwartet, f"summe({daten}, {zahlspalte!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    assert repr(daten) == vorher, f"Die Tabelle wurde verändert: vorher {vorher}, nachher {daten!r}."

# Obere Grenze: spalte bei 100 000 Zeilen
daten = [{"geraet": GERAETE[nummer % 5], "stunde": nummer % 24, "wh": nummer * 10 % (10**6 + 1)}
         for nummer in range(100000)]
ergebnis = len(spalte(daten, "wh"))
assert ergebnis == 100000, f"Bei 100 000 Zeilen ergibt len(spalte(…, 'wh')) {ergebnis!r}, erwartet war 100000."

# Obere Grenze: summe bei 100 000 Zeilen
ergebnis = summe(daten, "stunde")
erwartet = sum(nummer % 24 for nummer in range(100000))
assert ergebnis == erwartet, f"Bei 100 000 Zeilen ergibt summe(…, 'stunde') {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: summe nach filtere bei 100 000 Zeilen
ergebnis = summe(filtere(daten, "geraet", "Lampe"), "wh")
erwartet = sum(zeile["wh"] for zeile in daten if zeile["geraet"] == "Lampe")
assert ergebnis == erwartet, (
    f"Bei 100 000 Zeilen ergibt summe(filtere(…, 'geraet', 'Lampe'), 'wh') {ergebnis!r}, erwartet war {erwartet!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['Kaffeemaschine', 'Drucker', 'Kaffeemaschine', 'Monitor']\n2\n470"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
