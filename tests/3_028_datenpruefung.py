# Automatisch erzeugt aus lehrkraft/muster/3_028_datenpruefung.py - nicht von Hand ändern.
# vorlage-hash: fa6d18d86bba99d0
# text-hash: 94ef01e931195507
# thema: funktionen
# inhalt: Funktionen als Argumente

def beispiel():
    """Baut die Kunden aus dem Beispiel neu."""
    return [{"name": "  ada  LANG", "plz": "33098"}, {"name": "ben", "plz": "3310"}]


REGELN = [("plz fünfstellig", lambda z: len(z["plz"]) == 5), ("name vorhanden", lambda z: z["name"] != "")]

# kette aus dem Beispiel
ergebnis = kette("  ada  LANG", [str.strip, str.title])
assert ergebnis == "Ada  Lang", (
    f'kette("  ada  LANG", [str.strip, str.title]) ergibt {ergebnis!r}, erwartet war "Ada  Lang".\n'
    "Tipp: Rufen Sie jede Funktion der Liste mit dem bisherigen Ergebnis auf: wert = schritt(wert)."
)

# Die Reihenfolge der Schritte zählt
ergebnis = (kette(-3, [abs, str, len]), kette(-3, [str, len]), kette(5, [lambda x: x + 1, lambda x: x * 10]))
assert ergebnis == (1, 2, 60), (
    f"kette(-3, [abs, str, len]), kette(-3, [str, len]) und kette(5, [x + 1, x * 10]) ergeben {ergebnis!r}, "
    "erwartet war (1, 2, 60).\nTipp: Die erste Funktion der Liste kommt zuerst dran, ihr Ergebnis geht an die nächste."
)

# Ohne Schritte bleibt der Wert, wie er ist
ergebnis = (kette(" x ", []), kette(0, []))
assert ergebnis == (" x ", 0), f'kette(" x ", []) und kette(0, []) ergeben {ergebnis!r}, erwartet war (" x ", 0).'

# bereinige_spalte aus dem Beispiel
daten = beispiel()
ergebnis = bereinige_spalte(daten, "name", [str.strip, str.title])
erwartet = [{"name": "Ada  Lang", "plz": "33098"}, {"name": "Ben", "plz": "3310"}]
assert ergebnis == erwartet, f'bereinige_spalte(<Beispiel>, "name", [str.strip, str.title]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# Die Zeilen und ihre Dictionaries bleiben unverändert
assert daten == beispiel(), (
    f"Nach bereinige_spalte sind die Zeilen {daten!r}, erwartet war unverändert {beispiel()!r}.\n"
    "Tipp: Kopieren Sie jede Zeile mit dict(zeile) und ändern Sie nur die Kopie."
)

# Eine andere Spalte (nicht fest "name" hinschreiben!)
ergebnis = bereinige_spalte(beispiel(), "plz", [lambda p: p.rjust(5, "0")])
erwartet = [{"name": "  ada  LANG", "plz": "33098"}, {"name": "ben", "plz": "03310"}]
assert ergebnis == erwartet, f'bereinige_spalte(<Beispiel>, "plz", [mit Nullen auffüllen]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.'

# verstoesse aus dem Beispiel
ergebnis = verstoesse(beispiel(), REGELN)
assert ergebnis == [(2, "plz fünfstellig")], (
    f"verstoesse(<Beispiel>, <Regeln>) ergibt {ergebnis!r}, erwartet war [(2, 'plz fünfstellig')].\n"
    "Tipp: Eine Regel liefert True, wenn die Zeile in Ordnung ist; gemeldet wird, wenn sie False liefert. "
    "Die Zeilen zählen ab 1."
)

# Mehrere Verstöße: nach Zeile, innerhalb der Zeile in Regelreihenfolge
daten = [{"name": "", "plz": "1"}, {"name": "Eva", "plz": "12345"}, {"name": "", "plz": "99999"}]
ergebnis = verstoesse(daten, REGELN)
erwartet = [(1, "plz fünfstellig"), (1, "name vorhanden"), (3, "name vorhanden")]
assert ergebnis == erwartet, f"verstoesse({daten}, <Regeln>) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Regeln in anderer Reihenfolge ändern die Reihenfolge innerhalb einer Zeile
ergebnis = verstoesse(daten[:1], REGELN[::-1])
assert ergebnis == [(1, "name vorhanden"), (1, "plz fünfstellig")], (
    f"verstoesse mit umgedrehten Regeln ergibt {ergebnis!r}, erwartet war [(1, 'name vorhanden'), (1, 'plz fünfstellig')]."
)

# Leere Zeilen und keine Regeln
ergebnis = (bereinige_spalte([], "name", [str.strip]), verstoesse([], REGELN), verstoesse(beispiel(), []))
assert ergebnis == ([], [], []), (
    f"bereinige_spalte([], …), verstoesse([], …) und verstoesse(<Beispiel>, []) ergeben {ergebnis!r}, erwartet war ([], [], [])."
)

# Jede Regel bekommt die ganze Zeile, also auch mehrere Spalten zugleich
regel = [("plz passt zum Ort", lambda z: z["ort"] != "Paderborn" or z["plz"].startswith("33"))]
daten = [{"ort": "Paderborn", "plz": "33098"}, {"ort": "Paderborn", "plz": "44135"}, {"ort": "Bonn", "plz": "53111"}]
ergebnis = verstoesse(daten, regel)
assert ergebnis == [(2, "plz passt zum Ort")], f"verstoesse({daten}, [plz passt zum Ort]) ergibt {ergebnis!r}, erwartet war [(2, 'plz passt zum Ort')]."


# Vergleichslösungen: rekursiv und über Indizes
def kette_von_hand(wert, schritte):
    """Wendet die erste Funktion an und den Rest rekursiv."""
    if not schritte:
        return wert
    return kette_von_hand(schritte[0](wert), schritte[1:])


def verstoesse_von_hand(zeilen, regeln):
    """Prüft erst alle Regeln für alle Zeilen und sortiert dann nach Zeile und Regelnummer."""
    gefunden = []
    for regelnummer in range(len(regeln)):
        for index in range(len(zeilen)):
            if not regeln[regelnummer][1](zeilen[index]):
                gefunden.append((index + 1, regelnummer, regeln[regelnummer][0]))
    gefunden.sort()
    return [(nummer, name) for nummer, _, name in gefunden]


SCHRITTE = [("strip", str.strip), ("lower", str.lower), ("upper", str.upper), ("title", str.title),
            ("ohne Leerzeichen", lambda t: t.replace(" ", "")), ("x davor", lambda t: "x" + t)]
ALLE_REGELN = [("nicht leer", lambda z: z["wert"] != ""), ("kurz", lambda z: len(z["wert"]) <= 4),
               ("ohne Ziffer", lambda z: not any(zeichen.isdigit() for zeichen in z["wert"])),
               ("Kennung gerade", lambda z: z["id"] % 2 == 0)]

# 300 zufällige Tabellen, Schritte und Regeln
zufall = Zufall(3028)
for _ in range(300):
    daten = []
    for nummer in range(zufall.randint(0, 6)):
        text = "".join(zufall.choice("ab Z1") for _ in range(zufall.randint(0, 6)))
        daten.append({"id": zufall.randint(0, 9), "wert": text})
    vorher = repr(daten)
    schritte = zufall.sample(SCHRITTE, zufall.randint(0, 4))
    funktionen = [funktion for _, funktion in schritte]
    regeln = zufall.sample(ALLE_REGELN, zufall.randint(0, 4))
    namen = [name for name, _ in schritte]
    ergebnis = bereinige_spalte(daten, "wert", funktionen)
    erwartet = [{"id": zeile["id"], "wert": kette_von_hand(zeile["wert"], funktionen)} for zeile in daten]
    assert ergebnis == erwartet, (
        f'bereinige_spalte({daten}, "wert", <Schritte {namen}>) ergibt {ergebnis!r}, erwartet war {erwartet!r}.'
    )
    ergebnis = verstoesse(daten, regeln)
    erwartet = verstoesse_von_hand(daten, regeln)
    assert ergebnis == erwartet, (
        f"verstoesse({daten}, <Regeln {[name for name, _ in regeln]}>) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )
    assert repr(daten) == vorher, f"Die Zeilen wurden verändert: vorher {vorher}, nachher {daten!r}."

# Obere Grenze: 10 000 Zeilen, 10 Schritte und 10 Regeln
daten = [{"id": nummer, "wert": f" Kunde {nummer} "} for nummer in range(10000)]
zehn_schritte = [str.strip, str.lower, str.upper, str.lower, str.title, str.strip, str.upper, str.lower, str.title, str.swapcase]
zehn_regeln = [(f"Regel {nummer}", lambda z, teiler=nummer + 2: z["id"] % teiler != 0) for nummer in range(10)]
ergebnis = (bereinige_spalte(daten, "wert", zehn_schritte)[-1], len(verstoesse(daten, zehn_regeln)))
erwartet = ({"id": 9999, "wert": "kUNDE 9999"}, len(verstoesse_von_hand(daten, zehn_regeln)))
assert ergebnis == erwartet, (
    f"Bei 10 000 Zeilen ergeben die letzte bereinigte Zeile und die Anzahl der Verstöße {ergebnis!r}, erwartet war {erwartet!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Ada  Lang\n[{'name': 'Ada  Lang', 'plz': '33098'}, {'name': 'Ben', 'plz': '3310'}]\n[(2, 'plz fünfstellig')]"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
