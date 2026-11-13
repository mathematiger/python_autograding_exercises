# Automatisch erzeugt aus lehrkraft/muster/2_024_fehlversuche.py - nicht von Hand ändern.
# vorlage-hash: 8a955dba1650d247
# text-hash: de4772495561a578
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

# Andere Werte (nicht fest hinschreiben!)
ergebnis = (tagessummen([[4]]), tagessummen([[1, 2], [3, 4], [5, 6]]), tagessummen([[1000] * 31]))
assert ergebnis == ([4], [9, 12], [1000] * 31), (
    f"tagessummen([[4]]), tagessummen([[1, 2], [3, 4], [5, 6]]) und tagessummen([[1000] * 31]) ergeben {ergebnis!r}; "
    "erwartet waren [4], [9, 12] und 31-mal 1000."
)



def als_tupel(eintraege):
    """Macht aus Einträgen, die Listen sind, Tupel, damit erst der Inhalt und später die Form geprüft wird."""
    if not isinstance(eintraege, list):
        return eintraege
    return [tuple(eintrag) if isinstance(eintrag, list) else eintrag for eintrag in eintraege]


def tipp_auffaellig(ergebnis, erwartet, mit_gleichen):
    """Sucht zum falschen Ergebnis von auffaellig den Tipp, der zum Fehlerbild passt; sonst ""."""
    if not isinstance(ergebnis, list):
        return "\nTipp: Geben Sie eine Liste von Tupeln (name, tag) zurück."
    eintraege = als_tupel(ergebnis)
    ab_eins = [(eintrag[0], eintrag[1] + 1) for eintrag in eintraege if isinstance(eintrag, tuple) and len(eintrag) == 2]
    if sorted(ab_eins) == erwartet:
        return "\nTipp: Zählen Sie die Tage ab 1 (enumerate(zeile, start=1))."
    if sorted(eintraege) == mit_gleichen:
        return "\nTipp: Auffällig ist nur, wer mehr als grenze Fehlversuche hat, also anzahl > grenze."
    if sorted(eintraege) == erwartet:
        return "\nTipp: Die Einträge stimmen; sortieren Sie das Ergebnis mit sorted nach Namen und Tag."
    return ""


# auffaellig findet die richtigen Einträge (Reihenfolge und ob Tupel oder Liste zählen hier noch nicht)
benutzer, versuche = beispiel()
ergebnis = auffaellig(benutzer, versuche, 2)
erwartet = [("aberg", 1), ("aberg", 4), ("tlang", 3)]
mit_gleichen = [("aberg", 1), ("aberg", 4), ("mkoch", 2), ("tlang", 3)]
assert isinstance(ergebnis, list) and sorted(als_tupel(ergebnis)) == erwartet, (
    f"auffaellig(benutzer, versuche, 2) ergibt {ergebnis!r}, erwartet waren die Einträge {erwartet}."
    + tipp_auffaellig(ergebnis, erwartet, mit_gleichen)
)

# auffaellig aus dem Beispiel (ob Tupel oder Liste, zählt hier noch nicht)
benutzer, versuche = beispiel()
ergebnis = auffaellig(benutzer, versuche, 2)
assert als_tupel(ergebnis) == erwartet, (
    f"auffaellig(benutzer, versuche, 2) ergibt {ergebnis!r}, erwartet war {erwartet}."
    + tipp_auffaellig(ergebnis, erwartet, mit_gleichen)
)

# Jeder Eintrag ist ein Tupel (name, tag)
benutzer, versuche = beispiel()
ergebnis = auffaellig(benutzer, versuche, 2)
assert ergebnis == erwartet, (
    f"auffaellig(benutzer, versuche, 2) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
    "Tipp: Jeder Eintrag soll ein Tupel sein, keine Liste: treffer.append((name, tag)) mit doppelten runden Klammern."
)

# Genau grenze Fehlversuche sind noch nicht auffällig
ergebnis = auffaellig(["a"], [[2, 3, 1]], 2)
assert als_tupel(ergebnis) == [("a", 2)], (
    f"auffaellig(['a'], [[2, 3, 1]], 2) ergibt {ergebnis!r}, erwartet war [('a', 2)].\n"
    "Tipp: Auffällig ist nur, wer mehr als grenze Fehlversuche hat, also anzahl > grenze."
)

# Die Liste ist nach Namen sortiert, nicht in der Reihenfolge der Benutzer
ergebnis = auffaellig(["zora", "ben"], [[5, 0], [0, 5]], 2)
assert als_tupel(ergebnis) == [("ben", 2), ("zora", 1)], (
    f"auffaellig(['zora', 'ben'], [[5, 0], [0, 5]], 2) ergibt {ergebnis!r}, erwartet war [('ben', 2), ('zora', 1)].\n"
    "Tipp: Die Liste ist nach Namen sortiert, nicht in der Reihenfolge der Benutzer; sortieren Sie das Ergebnis mit sorted."
)

# Grenze 0: jeder Tag mit mindestens einem Fehlversuch
ergebnis = auffaellig(["ben", "zora"], [[1, 0], [0, 1]], 0)
assert als_tupel(ergebnis) == [("ben", 1), ("zora", 2)], (
    f"auffaellig(['ben', 'zora'], [[1, 0], [0, 1]], 0) ergibt {ergebnis!r}, erwartet war [('ben', 1), ('zora', 2)].\n"
    "Tipp: Schon ein Fehlversuch ist mehr als 0."
)

# tagessummen ohne Benutzer
try:
    ergebnis = tagessummen([])
except IndexError as fehler:
    ergebnis = fehler
assert ergebnis == [], (
    f"tagessummen([]) ergibt {ergebnis!r}, erwartet war [].\n"
    "Tipp: Ohne Zeilen gibt es kein versuche[0]; prüfen Sie zuerst, ob die Liste leer ist."
)

# auffaellig ohne Benutzer
ergebnis = auffaellig([], [], 0)
assert ergebnis == [], f"auffaellig([], [], 0) ergibt {ergebnis!r}, erwartet war []."

# Niemand ist auffällig
ergebnis = auffaellig(["a", "b"], [[1000, 0], [5, 1000]], 1000)
assert ergebnis == [], f"auffaellig(['a', 'b'], [[1000, 0], [5, 1000]], 1000) ergibt {ergebnis!r}, erwartet war []."

# Die Listen bleiben unverändert
benutzer, versuche = beispiel()
tagessummen(versuche)
auffaellig(benutzer, versuche, 0)
assert (benutzer, versuche) == beispiel(), (
    f"Nach den Aufrufen sind benutzer {benutzer!r} und versuche {versuche!r}; beide sollen unverändert bleiben.\n"
    "Tipp: Sammeln Sie die Summen in einer neuen Liste und sortieren Sie die Ergebnisliste, nicht benutzer selbst."
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


# 300 zufällige Zeiträume für tagessummen
zufall = Zufall(2024)
for _ in range(300):
    namen = ["".join(zufall.choice("abcdefgh") for _ in range(zufall.randint(1, 3))) for _ in range(zufall.randint(0, 6))]
    namen = list(dict.fromkeys(namen))
    tage = zufall.randint(1, 7)
    tabelle = [[zufall.choice([0, 0, 1, 2, 5, 1000]) for _ in range(tage)] for _ in namen]
    grenze = zufall.choice([0, 1, 2, 5, 1000])
    erwartet = tagessummen_von_hand(tabelle)
    vorher = str(tabelle)
    ergebnis = tagessummen(tabelle)
    assert ergebnis == erwartet, f"tagessummen({vorher}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige Zeiträume für auffaellig
zufall = Zufall(2024)
for _ in range(300):
    namen = ["".join(zufall.choice("abcdefgh") for _ in range(zufall.randint(1, 3))) for _ in range(zufall.randint(0, 6))]
    namen = list(dict.fromkeys(namen))
    tage = zufall.randint(1, 7)
    tabelle = [[zufall.choice([0, 0, 1, 2, 5, 1000]) for _ in range(tage)] for _ in namen]
    grenze = zufall.choice([0, 1, 2, 5, 1000])
    erwartet = auffaellig_von_hand(namen, tabelle, grenze)
    vorher = f"{namen}, {tabelle}"
    ergebnis = auffaellig(namen, tabelle, grenze)
    assert als_tupel(ergebnis) == erwartet, f"auffaellig({vorher}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: tagessummen bei 1000 Benutzern und 31 Tagen
namen = [f"nutzer{chr(97 + nummer % 26)}{chr(97 + nummer // 26 % 26)}{chr(97 + nummer // 676)}" for nummer in range(1000)]
tabelle = [[(nummer * 31 + tag) * 37 % 1001 for tag in range(31)] for nummer in range(1000)]
ergebnis = tagessummen(tabelle)
erwartet = tagessummen_von_hand(tabelle)
assert ergebnis == erwartet, (
    f"Bei 1000 Benutzern und 31 Tagen beginnt tagessummen mit {ergebnis[:3]}, erwartet war {erwartet[:3]}."
)

# An der oberen Grenze: auffaellig bei 1000 Benutzern und 31 Tagen
liste = auffaellig(namen, tabelle, 990)
erwartete_liste = auffaellig_von_hand(namen, tabelle, 990)
assert als_tupel(liste) == erwartete_liste, (
    f"Bei 1000 Benutzern und 31 Tagen liefert auffaellig {len(liste)} Einträge, die ersten {liste[:2]}; "
    f"erwartet waren {len(erwartete_liste)}, die ersten {erwartete_liste[:2]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[7, 2, 3, 13, 1]\n[('aberg', 1), ('aberg', 4), ('tlang', 3)]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
