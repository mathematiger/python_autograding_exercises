# Automatisch erzeugt aus lehrkraft/muster/3_002_binaere_suche.py - nicht von Hand ändern.
# vorlage-hash: 41c01cd387726257
# thema: algorithmen
# inhalt: Binäre Suche

# Element in der Mitte und daneben wird gefunden
for gesucht, erwartet in [(15, 2), (23, 3), (8, 1)]:
    ergebnis = binaere_suche([3, 8, 15, 23, 42], gesucht)
    assert ergebnis == erwartet, f"binaere_suche([3, 8, 15, 23, 42], {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Erstes und letztes Element werden gefunden
for gesucht, erwartet in [(3, 0), (42, 4)]:
    ergebnis = binaere_suche([3, 8, 15, 23, 42], gesucht)
    assert ergebnis == erwartet, (
        f"binaere_suche([3, 8, 15, 23, 42], {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Der Bereich reicht von 0 bis len(liste) - 1, und die Schleife läuft, solange links <= rechts."
    )

# Nicht vorhandene Werte ergeben -1, auch kleiner oder größer als alle
for gesucht in [10, 1, 50, 24]:
    ergebnis = binaere_suche([3, 8, 15, 23, 42], gesucht)
    assert ergebnis == -1, f"binaere_suche([3, 8, 15, 23, 42], {gesucht}) ergibt {ergebnis!r}, erwartet war -1."

# Leere Liste und Liste mit einem Element
for liste, gesucht, erwartet in [([], 5, -1), ([7], 7, 0), ([7], 3, -1), ([7], 9, -1)]:
    ergebnis = binaere_suche(liste, gesucht)
    assert ergebnis == erwartet, f"binaere_suche({liste}, {gesucht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Jede Nummer in einer längeren Liste wird gefunden
regal = list(range(0, 300, 3))
for index in range(len(regal)):
    ergebnis = binaere_suche(regal, regal[index])
    assert ergebnis == index, f"In list(range(0, 300, 3)) ergibt die Suche nach {regal[index]} {ergebnis!r}, erwartet war {index}."


# Diese Liste zählt, wie oft die Funktion ein Element ansieht
class Zaehlliste:
    """Sortierte Liste, die mitzählt, wie oft auf ein Element zugegriffen wird."""

    def __init__(self, werte):
        """Speichert die Werte und setzt den Zähler auf 0."""
        self.werte = werte
        self.zugriffe = 0

    def __len__(self):
        """Gibt die Anzahl der Werte zurück, ohne mitzuzählen."""
        return len(self.werte)

    def __getitem__(self, index):
        """Gibt den Wert an index zurück und zählt den Zugriff."""
        self.zugriffe += 1
        return self.werte[index]


# Bei 1000 Einträgen reichen wenige Zugriffe (binäre statt linearer Suche)
messliste = Zaehlliste(list(range(1000)))
for gesucht in [0, 499, 998, 999, 1000, -1]:
    binaere_suche(messliste, gesucht)
assert messliste.zugriffe <= 6 * 25, (
    f"Für sechs Suchen in einer Liste mit 1000 Einträgen hat Ihre Funktion {messliste.zugriffe} Elemente angesehen, "
    "erlaubt sind höchstens 150 (etwa 20 pro Suche).\n"
    "Tipp: Halbieren Sie den Suchbereich in jedem Schritt, statt alle Elemente durchzugehen."
)
