# Automatisch erzeugt aus lehrkraft/muster/2_028_menuepunkte.py - nicht von Hand ändern.
# vorlage-hash: acb37a1a2d011fa3
# text-hash: b22aba3c2aabffe4
# thema: datenstrukturen
# inhalt: Mengen

def beispiel():
    """Baut die beiden Klicklisten aus dem Beispiel neu."""
    return [["Datei", "Rechnung", "Datei", "Hilfe"], ["Rechnung", "Export", "Datei", "Rechnung"]]


MENUE = ["Datei", "Export", "Hilfe", "Rechnung", "Steuern", "Vorlagen"]

# angeklickt aus dem Beispiel
protokolle = beispiel()
ergebnis = angeklickt(protokolle[0])
assert ergebnis == ["Datei", "Hilfe", "Rechnung"], (
    f"angeklickt({beispiel()[0]}) ergibt {ergebnis!r}, erwartet war ['Datei', 'Hilfe', 'Rechnung'].\n"
    "Tipp: set(klicks) entfernt die Doppelten, sorted(...) macht daraus eine sortierte Liste."
)

# von_allen aus dem Beispiel
ergebnis = von_allen(protokolle)
assert ergebnis == ["Datei", "Rechnung"], (
    f"von_allen({beispiel()}) ergibt {ergebnis!r}, erwartet war ['Datei', 'Rechnung'].\n"
    "Tipp: Gesucht ist der Schnitt der Mengen aller Personen: menge & set(klicks)."
)

# ungenutzt aus dem Beispiel
ergebnis = ungenutzt(MENUE, protokolle)
assert ergebnis == ["Steuern", "Vorlagen"], (
    f"ungenutzt({MENUE}, {beispiel()}) ergibt {ergebnis!r}, erwartet war ['Steuern', 'Vorlagen'].\n"
    "Tipp: Sammeln Sie mit | alle benutzten Punkte und ziehen Sie sie mit - von der Menge des Menüs ab."
)

# Die Listen bleiben unverändert
assert protokolle == beispiel(), f"Nach den Aufrufen sind die Klicklisten {protokolle!r}; sie sollen unverändert bleiben."

# Die Ergebnisse sind Listen
ergebnisse = [angeklickt(["a"]), von_allen([["a"]]), ungenutzt(["a"], [[]])]
typen = [type(ergebnis).__name__ for ergebnis in ergebnisse]
assert typen == ["list", "list", "list"], (
    f"Die drei Funktionen geben {typen} zurück, erwartet war jeweils eine Liste.\n"
    "Tipp: sorted(menge) gibt eine sortierte Liste zurück."
)

# Andere Werte (nicht fest hinschreiben!), Groß- und Kleinschreibung zählt
protokolle = [["datei", "Datei", "Suche"], ["Suche", "Datei", "Suche"], ["Suche", "Datei", "Optionen"]]
ergebnis = (angeklickt(protokolle[0]), von_allen(protokolle), ungenutzt(["Datei", "datei", "Suche", "Optionen", "Neu"], protokolle))
erwartet = (["Datei", "Suche", "datei"], ["Datei", "Suche"], ["Neu"])
assert ergebnis == erwartet, (
    f"Für {protokolle} ergeben angeklickt(der ersten Liste), von_allen und ungenutzt {ergebnis!r}, erwartet war {erwartet!r}."
)

# Randfälle: keine Klicks, eine einzige Person, eine Person ohne Klicks
for aufruf, ergebnis, erwartet in [
    ("angeklickt([])", angeklickt([]), []),
    ("von_allen([['b', 'a', 'b']])", von_allen([["b", "a", "b"]]), ["a", "b"]),
    ("von_allen([['a'], []])", von_allen([["a"], []]), []),
    ("von_allen([[]])", von_allen([[]]), []),
    ("ungenutzt(['a', 'b'], [[]])", ungenutzt(["a", "b"], [[]]), ["a", "b"]),
    ("ungenutzt(['a'], [['a'], ['x']])", ungenutzt(["a"], [["a"], ["x"]]), []),
    ("ungenutzt(['a', 'b'], [['b'], ['a']])", ungenutzt(["a", "b"], [["b"], ["a"]]), []),
]:
    assert ergebnis == erwartet, f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Punkte, die nicht im Menü stehen, kommen in ungenutzt nicht vor
ergebnis = ungenutzt(["Datei"], [["Alt", "Datei"], ["Uralt"]])
assert ergebnis == [], (
    f"ungenutzt(['Datei'], [['Alt', 'Datei'], ['Uralt']]) ergibt {ergebnis!r}, erwartet war [].\n"
    "Tipp: Gefragt sind nur Menüpunkte aus menue; ziehen Sie die benutzten von set(menue) ab, nicht umgekehrt."
)


# Vergleichslösungen ohne Mengen: mit Listen und in
def ohne_doppelte(liste):
    """Gibt die sortierte Liste ohne Doppelte zurück, ganz ohne set."""
    ergebnis = []
    for wert in sorted(liste):
        if not ergebnis or ergebnis[-1] != wert:
            ergebnis.append(wert)
    return ergebnis


def von_allen_von_hand(protokolle):
    """Behält die Punkte der ersten Person, die auch bei allen anderen vorkommen."""
    return [punkt for punkt in ohne_doppelte(protokolle[0]) if all(punkt in klicks for klicks in protokolle)]


def ungenutzt_von_hand(menue, protokolle):
    """Behält die Menüpunkte, die in keiner Klickliste vorkommen."""
    return [punkt for punkt in ohne_doppelte(menue) if not any(punkt in klicks for klicks in protokolle)]


# 300 zufällige Usability-Tests
zufall = Zufall(2028)
punkte = ["Datei", "datei", "Export", "Hilfe", "Rechnung", "Steuern", "X"]
for _ in range(300):
    protokolle = [[zufall.choice(punkte) for _ in range(zufall.randint(0, 8))] for _ in range(zufall.randint(1, 4))]
    menue = zufall.sample(punkte, zufall.randint(1, 7))
    kopie = [list(klicks) for klicks in protokolle]
    ergebnis = (angeklickt(protokolle[0]), von_allen(protokolle), ungenutzt(menue, protokolle))
    erwartet = (ohne_doppelte(kopie[0]), von_allen_von_hand(kopie), ungenutzt_von_hand(menue, kopie))
    assert ergebnis == erwartet and protokolle == kopie, (
        f"Für die Klicklisten {kopie} und das Menü {menue} ergeben angeklickt(der ersten Liste), von_allen und "
        f"ungenutzt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Daten an der oberen Grenze: 1000 Personen mit zusammen 100 000 Klicks, Menü mit 1000 Punkten
menue = [f"Punkt {nummer:04d}" for nummer in range(1000)]
protokolle = [[f"Punkt {(person * 7 + klick * 13) % 1100:04d}" for klick in range(100)] for person in range(1000)]
for klicks in protokolle:
    klicks.append("Punkt 0000")
gross = [f"Punkt {(nummer * 31) % 1000:04d}" for nummer in range(100000)]

# Vergleich über ein Dictionary, das zu jedem Punkt die Personen zählt, die ihn benutzt haben
personen_je_punkt = {}
for klicks in protokolle:
    for punkt in dict.fromkeys(klicks):
        personen_je_punkt[punkt] = personen_je_punkt.get(punkt, 0) + 1
gemeinsam = sorted(punkt for punkt, anzahl in personen_je_punkt.items() if anzahl == len(protokolle))
erwartet = (1000, gemeinsam, len([punkt for punkt in menue if punkt not in personen_je_punkt]))

# An der oberen Grenze: 1000 Personen mit zusammen 100 000 Klicks, Menü mit 1000 Punkten
ergebnis = (len(angeklickt(gross)), von_allen(protokolle), len(ungenutzt(menue, protokolle)))
assert ergebnis == erwartet, (
    f"An der oberen Grenze ergeben len(angeklickt(...)), von_allen(...) und len(ungenutzt(...)) {ergebnis!r}, "
    f"erwartet war {erwartet!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['Datei', 'Hilfe', 'Rechnung']\n['Datei', 'Rechnung']\n['Steuern', 'Vorlagen']"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
