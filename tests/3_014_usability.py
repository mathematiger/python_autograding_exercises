# Automatisch erzeugt aus lehrkraft/muster/3_014_usability.py - nicht von Hand ändern.
# vorlage-hash: f5c9a5fa6e24a828
# text-hash: e47e8a0eea40c77e
# thema: datenanalyse
# inhalt: numpy: Masken, sum, mean, max

def arrays(zeiten_liste, erfolg_liste):
    """Macht aus zwei Listen die Arrays zeiten (int64) und erfolgreich (bool)."""
    return np.array(zeiten_liste, dtype=np.int64), np.array(erfolg_liste, dtype=bool)


zeiten, erfolgreich = arrays([95, 240, 61, 180, 300], [True, False, True, True, False])

# anzahl_ueber aus dem Beispiel
ergebnis = anzahl_ueber(zeiten, 120)
assert ergebnis == 3, f"anzahl_ueber({zeiten.tolist()}, 120) ergibt {ergebnis!r}, erwartet war 3."

# anzahl_ueber mit anderen Grenzen (nicht fest hinschreiben!); genau grenze zählt nicht mit
for grenze, erwartet in [(180, 2), (179, 3), (300, 0), (0, 5), (61, 4)]:
    ergebnis = anzahl_ueber(zeiten, grenze)
    assert ergebnis == erwartet, (
        f"anzahl_ueber({zeiten.tolist()}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Gezählt werden nur Zeiten, die größer als die Grenze sind, nicht gleich."
    )

# mittel_erfolgreich aus dem Beispiel
ergebnis = mittel_erfolgreich(zeiten, erfolgreich)
assert ergebnis is not None and abs(ergebnis - 112.0) < 1e-9, (
    f"mittel_erfolgreich(...) ergibt für das Beispiel {ergebnis!r}, erwartet war 112.0 = (95 + 61 + 180) / 3.\n"
    "Tipp: Wählen Sie mit zeiten[erfolgreich] nur die erfolgreichen Zeiten aus, dann .mean()."
)

# laengste_erfolgreich aus dem Beispiel: 240 und 300 zählen nicht, die waren nicht erfolgreich
ergebnis = laengste_erfolgreich(zeiten, erfolgreich)
assert ergebnis == 180, (
    f"laengste_erfolgreich(...) ergibt für das Beispiel {ergebnis!r}, erwartet war 180; "
    "240 und 300 Sekunden gehören zu Testpersonen, die es nicht geschafft haben."
)

ANDERE_LAEUFE = [
    ([10, 20, 30, 40], [False, True, False, True], 30.0, 40),
    ([3600], [True], 3600.0, 3600),
    ([1, 1, 2], [True, True, True], 4 / 3, 2),
]

# Andere Testläufe: mittel_erfolgreich
for zeiten_liste, erfolg_liste, mittel, _ in ANDERE_LAEUFE:
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = mittel_erfolgreich(zeiten_test, erfolg_test)
    assert ergebnis is not None and abs(ergebnis - mittel) < 1e-9, (
        f"Bei zeiten = {zeiten_liste} und erfolgreich = {erfolg_liste} ergibt mittel_erfolgreich {ergebnis!r}, "
        f"erwartet war {mittel!r}."
    )

# Andere Testläufe: laengste_erfolgreich
for zeiten_liste, erfolg_liste, _, laengste in ANDERE_LAEUFE:
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = laengste_erfolgreich(zeiten_test, erfolg_test)
    assert ergebnis == laengste, (
        f"Bei zeiten = {zeiten_liste} und erfolgreich = {erfolg_liste} ergibt laengste_erfolgreich {ergebnis!r}, "
        f"erwartet war {laengste}."
    )


def ergebnis_oder_fehler(funktion, *argumente):
    """Ruft funktion(*argumente) auf; liefert bei einem ValueError die Ausnahme statt eines Ergebnisses."""
    try:
        return funktion(*argumente)
    except ValueError as fehler:
        return fehler


TIPP_LEER = "Tipp: Ein leeres Array hat kein Maximum und keinen Mittelwert; prüfen Sie vorher, ob etwas ausgewählt wurde."

# Niemand war erfolgreich: mittel_erfolgreich ergibt None
zeiten_test, erfolg_test = arrays([50, 70], [False, False])
ergebnis = ergebnis_oder_fehler(mittel_erfolgreich, zeiten_test, erfolg_test)
assert ergebnis is None, (
    f"Bei zeiten = [50, 70] und erfolgreich = [False, False] ergibt mittel_erfolgreich {ergebnis!r}, erwartet war None.\n"
    + TIPP_LEER
)

# Niemand war erfolgreich: laengste_erfolgreich ergibt None
ergebnis = ergebnis_oder_fehler(laengste_erfolgreich, zeiten_test, erfolg_test)
assert ergebnis is None, (
    f"Bei zeiten = [50, 70] und erfolgreich = [False, False] ergibt laengste_erfolgreich {ergebnis!r}, erwartet war None.\n"
    + TIPP_LEER
)

# Keine Testpersonen: anzahl_ueber ergibt 0
zeiten_test, erfolg_test = arrays([], [])
ergebnis = ergebnis_oder_fehler(anzahl_ueber, zeiten_test, 0)
assert ergebnis == 0, f"Bei leeren Arrays ergibt anzahl_ueber(…, 0) {ergebnis!r}, erwartet war 0."

# Keine Testpersonen: mittel_erfolgreich ergibt None
ergebnis = ergebnis_oder_fehler(mittel_erfolgreich, zeiten_test, erfolg_test)
assert ergebnis is None, f"Bei leeren Arrays ergibt mittel_erfolgreich {ergebnis!r}, erwartet war None."

# Keine Testpersonen: laengste_erfolgreich ergibt None
ergebnis = ergebnis_oder_fehler(laengste_erfolgreich, zeiten_test, erfolg_test)
assert ergebnis is None, f"Bei leeren Arrays ergibt laengste_erfolgreich {ergebnis!r}, erwartet war None."

# Die Arrays bleiben unverändert
zeiten_test, erfolg_test = arrays([95, 240, 61], [True, False, True])
anzahl_ueber(zeiten_test, 100)
mittel_erfolgreich(zeiten_test, erfolg_test)
laengste_erfolgreich(zeiten_test, erfolg_test)
assert zeiten_test.tolist() == [95, 240, 61] and erfolg_test.tolist() == [True, False, True], (
    f"Nach den Auswertungen sind die Arrays {zeiten_test.tolist()} und {erfolg_test.tolist()}, "
    "erwartet war, dass sie unverändert bleiben."
)

# 300 zufällige Testläufe, verglichen mit einer Rechnung über Listen: anzahl_ueber
zufall = Zufall(3014)
zufaellige = []
for _ in range(300):
    anzahl = zufall.randint(0, 10)
    zeiten_liste = [zufall.choice([zufall.randint(1, 3600), zufall.randint(50, 70)]) for _ in range(anzahl)]
    erfolg_liste = [zufall.random() < 0.5 for _ in range(anzahl)]
    grenze = zufall.choice([zufall.randint(0, 3600), zufall.randint(50, 70), 0, 3600])
    zufaellige.append((zeiten_liste, erfolg_liste, grenze))
for zeiten_liste, erfolg_liste, grenze in zufaellige:
    erwartet = len([zeit for zeit in zeiten_liste if zeit > grenze])
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = anzahl_ueber(zeiten_test, grenze)
    assert ergebnis == erwartet, (
        f"Bei zeiten = {zeiten_liste} und grenze = {grenze} ergibt anzahl_ueber {ergebnis!r}, erwartet war {erwartet}."
    )

# Dieselben 300 zufälligen Testläufe: mittel_erfolgreich
for zeiten_liste, erfolg_liste, grenze in zufaellige:
    erfolgreiche = [zeit for zeit, erfolg in zip(zeiten_liste, erfolg_liste) if erfolg]
    erwartet = sum(erfolgreiche) / len(erfolgreiche) if erfolgreiche else None
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = mittel_erfolgreich(zeiten_test, erfolg_test)
    if erwartet is None:
        gleich = ergebnis is None
    else:
        gleich = ergebnis is not None and abs(ergebnis - erwartet) < 1e-9
    assert gleich, (
        f"Bei zeiten = {zeiten_liste} und erfolgreich = {erfolg_liste} ergibt mittel_erfolgreich {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )

# Dieselben 300 zufälligen Testläufe: laengste_erfolgreich
for zeiten_liste, erfolg_liste, grenze in zufaellige:
    erfolgreiche = [zeit for zeit, erfolg in zip(zeiten_liste, erfolg_liste) if erfolg]
    erwartet = max(erfolgreiche) if erfolgreiche else None
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = laengste_erfolgreich(zeiten_test, erfolg_test)
    assert ergebnis == erwartet, (
        f"Bei zeiten = {zeiten_liste} und erfolgreich = {erfolg_liste} ergibt laengste_erfolgreich {ergebnis!r}, "
        f"erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 2000 Testpersonen bei anzahl_ueber
zeiten_gross = np.arange(2000, dtype=np.int64) + 1
erfolg_gross = np.arange(2000) % 2 == 0
anzahl, schritte_anzahl = zaehle_schritte(anzahl_ueber, zeiten_gross, 1500)
erwartet_anzahl = int((zeiten_gross > 1500).sum())
assert anzahl == erwartet_anzahl, f"Bei 2000 Testpersonen ergibt anzahl_ueber {anzahl!r}, erwartet war {erwartet_anzahl}."

# An der oberen Grenze: 2000 Testpersonen bei mittel_erfolgreich
mittel, schritte_mittel = zaehle_schritte(mittel_erfolgreich, zeiten_gross, erfolg_gross)
erwartet_mittel = float(zeiten_gross[::2].mean())
assert abs(mittel - erwartet_mittel) < 1e-6, (
    f"Bei 2000 Testpersonen ergibt mittel_erfolgreich {mittel!r}, erwartet war {erwartet_mittel}."
)

# An der oberen Grenze: 2000 Testpersonen bei laengste_erfolgreich
laengste, schritte_laengste = zaehle_schritte(laengste_erfolgreich, zeiten_gross, erfolg_gross)
assert laengste == 1999, f"Bei 2000 Testpersonen ergibt laengste_erfolgreich {laengste!r}, erwartet war 1999."


def schritte_meldung(name, schritte):
    """Baut die Meldung für eine Funktion, die zu viele Zeilen ausführt."""
    return (
        f"Bei 2000 Testpersonen braucht {name} {schritte} ausgeführte Zeilen, erwartet waren höchstens 10.\n"
        "Tipp: Lassen Sie numpy rechnen: (zeiten > grenze).sum() zählt ohne Schleife."
    )


# anzahl_ueber ohne Python-Schleife: höchstens 10 ausgeführte Zeilen bei 2000 Testpersonen
assert schritte_anzahl <= 10, schritte_meldung("anzahl_ueber", schritte_anzahl)

# mittel_erfolgreich ohne Python-Schleife: höchstens 10 ausgeführte Zeilen bei 2000 Testpersonen
assert schritte_mittel <= 10, schritte_meldung("mittel_erfolgreich", schritte_mittel)

# laengste_erfolgreich ohne Python-Schleife: höchstens 10 ausgeführte Zeilen bei 2000 Testpersonen
assert schritte_laengste <= 10, schritte_meldung("laengste_erfolgreich", schritte_laengste)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "3\n112.0\n180"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
