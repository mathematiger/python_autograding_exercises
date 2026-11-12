# Automatisch erzeugt aus lehrkraft/muster/2_024_fehlversuche.py - nicht von Hand ändern.
# vorlage-hash: 8a955dba1650d247
# text-hash: 54f3b0a077bbc47f
# thema: datenstrukturen
# inhalt: Übung: Listen

def beispiel():
    """Baut die Beispieldaten aus der Aufgabe neu."""
    return ["mkoch", "aberg", "tlang"], [[0, 2, 0, 1, 0], [7, 0, 0, 12, 1], [0, 0, 3, 0, 0]]


# tagessummen aus dem Beispiel
benutzer, versuche = beispiel()
ergebnis = tagessummen(versuche)
assert ergebnis == [7, 2, 3, 13, 1], (
    f"tagessummen(versuche) aus dem Beispiel ergibt {ergebnis!r}, erwartet war [7, 2, 3, 13, 1].\n"
    "Tipp: Gesucht sind die Summen der Spalten (je Tag), nicht die der Zeilen (je Benutzer)."
)

# auffaellig aus dem Beispiel
ergebnis = auffaellig(benutzer, versuche, 2)
erwartet = [("aberg", 1), ("aberg", 4), ("tlang", 3)]
assert ergebnis == erwartet, (
    f"auffaellig(benutzer, versuche, 2) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Zählen Sie die Tage ab 1 (enumerate(zeile, start=1)) und sortieren Sie das Ergebnis mit sorted."
)

# Genau grenze Fehlversuche sind noch nicht auffällig
ergebnis = auffaellig(["a"], [[2, 3, 1]], 2)
assert ergebnis == [("a", 2)], (
    f"auffaellig(['a'], [[2, 3, 1]], 2) ergibt {ergebnis!r}, erwartet war [('a', 2)].\n"
    "Tipp: Auffällig ist nur, wer mehr als grenze Fehlversuche hat, also anzahl > grenze."
)

# Grenze 0: jeder Tag mit mindestens einem Fehlversuch
ergebnis = auffaellig(["zora", "ben"], [[0, 1], [1, 0]], 0)
assert ergebnis == [("ben", 1), ("zora", 2)], (
    f"auffaellig(['zora', 'ben'], [[0, 1], [1, 0]], 0) ergibt {ergebnis!r}, erwartet war [('ben', 1), ('zora', 2)].\n"
    "Tipp: Die Liste ist nach Namen sortiert, nicht in der Reihenfolge der Benutzer."
)

# Andere Werte (nicht fest hinschreiben!)
ergebnis = (tagessummen([[4]]), tagessummen([[1, 2], [3, 4], [5, 6]]), tagessummen([[1000] * 31]))
assert ergebnis == ([4], [9, 12], [1000] * 31), (
    f"tagessummen([[4]]), tagessummen([[1, 2], [3, 4], [5, 6]]) und tagessummen([[1000] * 31]) ergeben {ergebnis!r}; "
    "erwartet waren [4], [9, 12] und 31-mal 1000."
)

# Ohne Benutzer
try:
    ergebnis = (tagessummen([]), auffaellig([], [], 0))
except IndexError as fehler:
    ergebnis = fehler
assert ergebnis == ([], []), (
    f"Ohne Benutzer ergeben tagessummen([]) und auffaellig([], [], 0) {ergebnis!r}, erwartet war ([], []).\n"
    "Tipp: Ohne Zeilen gibt es kein versuche[0]; prüfen Sie zuerst, ob die Liste leer ist."
)

# Niemand ist auffällig
ergebnis = auffaellig(["a", "b"], [[1000, 0], [5, 1000]], 1000)
assert ergebnis == [], f"auffaellig(['a', 'b'], [[1000, 0], [5, 1000]], 1000) ergibt {ergebnis!r}, erwartet war []."

# Die Listen bleiben unverändert
benutzer, versuche = beispiel()
tagessummen(versuche)
auffaellig(benutzer, versuche, 0)
assert (benutzer, versuche) == beispiel(), (
    f"Nach den Aufrufen sind benutzer {benutzer!r} und versuche {versuche!r}; beide sollen unverändert bleiben.\n"
    "Tipp: Sammeln Sie die Summen in einer neuen Liste und sortieren Sie mit sorted statt mit sort."
)


# Vergleichslösungen mit Indizes und einer Suche nach dem kleinsten Tupel
def tagessummen_von_hand(versuche):
    """Summiert jede Spalte über die Indizes."""
    if len(versuche) == 0:
        return []
    return [sum(versuche[i][j] for i in range(len(versuche))) for j in range(len(versuche[0]))]


def auffaellig_von_hand(benutzer, versuche, grenze):
    """Geht die Namen alphabetisch durch und darin die Tage der Reihe nach."""
    ergebnis = []
    for name in sorted(benutzer):
        zeile = versuche[benutzer.index(name)]
        for j in range(len(zeile)):
            if zeile[j] > grenze:
                ergebnis.append((name, j + 1))
    return ergebnis


# 300 zufällige Wochen
zufall = Zufall(2024)
for _ in range(300):
    namen = ["".join(zufall.choice("abcdefgh") for _ in range(zufall.randint(1, 3))) for _ in range(zufall.randint(0, 6))]
    namen = list(dict.fromkeys(namen))
    tage = zufall.randint(1, 7)
    tabelle = [[zufall.choice([0, 0, 1, 2, 5, 1000]) for _ in range(tage)] for _ in namen]
    grenze = zufall.choice([0, 1, 2, 5, 1000])
    ergebnis = tagessummen(tabelle)
    erwartet = tagessummen_von_hand(tabelle)
    assert ergebnis == erwartet, f"tagessummen({tabelle}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = auffaellig(namen, tabelle, grenze)
    erwartet = auffaellig_von_hand(namen, tabelle, grenze)
    assert ergebnis == erwartet, f"auffaellig({namen}, {tabelle}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 1000 Benutzer, 31 Tage
namen = [f"nutzer{chr(97 + nummer % 26)}{chr(97 + nummer // 26 % 26)}{chr(97 + nummer // 676)}" for nummer in range(1000)]
tabelle = [[(nummer * 31 + tag) * 37 % 1001 for tag in range(31)] for nummer in range(1000)]
ergebnis = tagessummen(tabelle)
erwartet = tagessummen_von_hand(tabelle)
liste = auffaellig(namen, tabelle, 990)
erwartete_liste = auffaellig_von_hand(namen, tabelle, 990)
assert ergebnis == erwartet and liste == erwartete_liste, (
    f"Bei 1000 Benutzern und 31 Tagen beginnt tagessummen mit {ergebnis[:3]} (erwartet {erwartet[:3]}), und auffaellig "
    f"liefert {len(liste)} Einträge, die ersten {liste[:2]} (erwartet {len(erwartete_liste)}, die ersten {erwartete_liste[:2]})."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[7, 2, 3, 13, 1]\n[('aberg', 1), ('aberg', 4), ('tlang', 3)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
