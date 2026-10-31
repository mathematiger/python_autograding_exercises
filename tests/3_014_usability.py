# Automatisch erzeugt aus lehrkraft/muster/3_014_usability.py - nicht von Hand ändern.
# vorlage-hash: f5c9a5fa6e24a828
# text-hash: fe0296261f9b23ce
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

# Andere Testläufe
for zeiten_liste, erfolg_liste, mittel, laengste in [
    ([10, 20, 30, 40], [False, True, False, True], 30.0, 40),
    ([3600], [True], 3600.0, 3600),
    ([1, 1, 2], [True, True, True], 4 / 3, 2),
]:
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = (mittel_erfolgreich(zeiten_test, erfolg_test), laengste_erfolgreich(zeiten_test, erfolg_test))
    assert ergebnis[0] is not None and abs(ergebnis[0] - mittel) < 1e-9 and ergebnis[1] == laengste, (
        f"Bei zeiten = {zeiten_liste} und erfolgreich = {erfolg_liste} ergeben mittel_erfolgreich und "
        f"laengste_erfolgreich {ergebnis!r}, erwartet war ({mittel!r}, {laengste})."
    )

# Niemand war erfolgreich: None
zeiten_test, erfolg_test = arrays([50, 70], [False, False])
try:
    ergebnis = (mittel_erfolgreich(zeiten_test, erfolg_test), laengste_erfolgreich(zeiten_test, erfolg_test))
except ValueError as fehler:
    ergebnis = fehler
assert ergebnis == (None, None), (
    f"Bei zeiten = [50, 70] und erfolgreich = [False, False] ergeben mittel_erfolgreich und laengste_erfolgreich "
    f"{ergebnis!r}, erwartet war (None, None).\n"
    "Tipp: Ein leeres Array hat kein Maximum und keinen Mittelwert; prüfen Sie vorher, ob etwas ausgewählt wurde."
)

# Keine Testpersonen: 0 und None
zeiten_test, erfolg_test = arrays([], [])
try:
    ergebnis = (
        anzahl_ueber(zeiten_test, 0),
        mittel_erfolgreich(zeiten_test, erfolg_test),
        laengste_erfolgreich(zeiten_test, erfolg_test),
    )
except ValueError as fehler:
    ergebnis = fehler
assert ergebnis == (0, None, None), (
    f"Bei leeren Arrays ergeben anzahl_ueber(…, 0), mittel_erfolgreich und laengste_erfolgreich {ergebnis!r}, "
    "erwartet war (0, None, None)."
)

# Die Arrays bleiben unverändert
zeiten_test, erfolg_test = arrays([95, 240, 61], [True, False, True])
anzahl_ueber(zeiten_test, 100)
mittel_erfolgreich(zeiten_test, erfolg_test)
laengste_erfolgreich(zeiten_test, erfolg_test)
assert zeiten_test.tolist() == [95, 240, 61] and erfolg_test.tolist() == [True, False, True], (
    f"Nach den Auswertungen sind die Arrays {zeiten_test.tolist()} und {erfolg_test.tolist()}, "
    "erwartet war, dass sie unverändert bleiben."
)

# 300 zufällige Testläufe, verglichen mit einer Rechnung über Listen
zufall = Zufall(3014)
for _ in range(300):
    anzahl = zufall.randint(0, 10)
    zeiten_liste = [zufall.choice([zufall.randint(1, 3600), zufall.randint(50, 70)]) for _ in range(anzahl)]
    erfolg_liste = [zufall.random() < 0.5 for _ in range(anzahl)]
    grenze = zufall.choice([zufall.randint(0, 3600), zufall.randint(50, 70), 0, 3600])
    erfolgreiche = [zeit for zeit, erfolg in zip(zeiten_liste, erfolg_liste) if erfolg]
    erwartet = (
        len([zeit for zeit in zeiten_liste if zeit > grenze]),
        sum(erfolgreiche) / len(erfolgreiche) if erfolgreiche else None,
        max(erfolgreiche) if erfolgreiche else None,
    )
    zeiten_test, erfolg_test = arrays(zeiten_liste, erfolg_liste)
    ergebnis = (
        anzahl_ueber(zeiten_test, grenze),
        mittel_erfolgreich(zeiten_test, erfolg_test),
        laengste_erfolgreich(zeiten_test, erfolg_test),
    )
    gleich = ergebnis[0] == erwartet[0] and ergebnis[2] == erwartet[2]
    if erwartet[1] is None:
        gleich = gleich and ergebnis[1] is None
    else:
        gleich = gleich and ergebnis[1] is not None and abs(ergebnis[1] - erwartet[1]) < 1e-9
    assert gleich, (
        f"Bei zeiten = {zeiten_liste}, erfolgreich = {erfolg_liste} und grenze = {grenze} ergeben anzahl_ueber, "
        f"mittel_erfolgreich und laengste_erfolgreich {ergebnis!r}, erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 100 000 Testpersonen
zeiten_gross = (np.arange(100000, dtype=np.int64) % 3600) + 1
erfolg_gross = np.arange(100000) % 2 == 0
anzahl, schritte_anzahl = zaehle_schritte(anzahl_ueber, zeiten_gross, 3000)
mittel, schritte_mittel = zaehle_schritte(mittel_erfolgreich, zeiten_gross, erfolg_gross)
laengste, schritte_laengste = zaehle_schritte(laengste_erfolgreich, zeiten_gross, erfolg_gross)
erwartet_anzahl = int((zeiten_gross > 3000).sum())
erwartet_mittel = float(zeiten_gross[::2].mean())
assert anzahl == erwartet_anzahl and abs(mittel - erwartet_mittel) < 1e-6 and laengste == 3599, (
    f"Bei 100 000 Testpersonen ergeben die drei Funktionen {anzahl!r}, {mittel!r} und {laengste!r}, "
    f"erwartet waren {erwartet_anzahl}, {erwartet_mittel} und 3599."
)

# Ohne Python-Schleife: höchstens 10 ausgeführte Zeilen bei 100 000 Testpersonen
schritte = (schritte_anzahl, schritte_mittel, schritte_laengste)
assert max(schritte) <= 10, (
    f"Bei 100 000 Testpersonen brauchen anzahl_ueber, mittel_erfolgreich und laengste_erfolgreich {schritte} "
    "ausgeführte Zeilen, erwartet waren je höchstens 10.\n"
    "Tipp: Lassen Sie numpy rechnen: (zeiten > grenze).sum() zählt ohne Schleife."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "3\n112.0\n180"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
