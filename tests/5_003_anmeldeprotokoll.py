# Automatisch erzeugt aus lehrkraft/muster/5_003_anmeldeprotokoll.py - nicht von Hand ändern.
# vorlage-hash: f8be0a2f8ea6a5c4
# thema: datenanalyse
# inhalt: numpy: Views, Kopien, Fancy Indexing

def beispiel():
    """Liefert eine frische Kopie des Protokolls aus der Aufgabe."""
    return np.array(
        [
            [0, 3, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 0, 2],
            [5, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 8, 0, 0],
        ],
        dtype=np.int64,
    )


# wochenausschnitt liefert die richtigen Spalten
protokoll = beispiel()
ausschnitt = wochenausschnitt(protokoll, 1)
erwartet = protokoll[:, 7:14].tolist()
assert isinstance(ausschnitt, np.ndarray) and ausschnitt.tolist() == erwartet, (
    f"wochenausschnitt(protokoll, 1) ergibt\n{ausschnitt!r}\nerwartet waren die Spalten 7 bis 13:\n{erwartet}"
)

# Woche 0 sind die Tage 0 bis 6
ausschnitt = wochenausschnitt(protokoll, 0)
erwartet = protokoll[:, 0:7].tolist()
assert isinstance(ausschnitt, np.ndarray) and ausschnitt.tolist() == erwartet, (
    f"wochenausschnitt(protokoll, 0) ergibt\n{ausschnitt!r}\nerwartet waren die Spalten 0 bis 6:\n{erwartet}"
)

# wochenausschnitt ist ein View: eine Korrektur kommt im Protokoll an
protokoll = beispiel()
ausschnitt = wochenausschnitt(protokoll, 1)
ausschnitt[0, 0] = 0
ausschnitt[2, 4] = 0
assert np.shares_memory(ausschnitt, protokoll) and protokoll[0, 7] == 0 and protokoll[2, 11] == 0, (
    "Nach ausschnitt = wochenausschnitt(protokoll, 1), ausschnitt[0, 0] = 0 und ausschnitt[2, 4] = 0 sollen "
    f"protokoll[0, 7] und protokoll[2, 11] 0 sein; sie sind {protokoll[0, 7]} und {protokoll[2, 11]}.\n"
    "Tipp: Slicing mit Doppelpunkt (protokoll[:, start:ende]) liefert einen View, eine Liste von Spalten oder "
    ".copy() dagegen eine Kopie."
)

# zuruecksetzen setzt die Zeilen im Protokoll selbst auf 0
protokoll = beispiel()
ergebnis = zuruecksetzen(protokoll, [0, 1])
erwartet = [[0] * 14, [0] * 14, beispiel()[2].tolist()]
assert protokoll.tolist() == erwartet, (
    f"Nach zuruecksetzen(protokoll, [0, 1]) ist protokoll\n{protokoll!r}\nerwartet war\n{np.array(erwartet)!r}\n"
    "Tipp: zeilen = protokoll[konten] ist eine Kopie, Änderungen daran kommen nicht an. Schreiben Sie direkt "
    "protokoll[konten] = 0."
)

# zuruecksetzen gibt nichts zurück
assert ergebnis is None, f"zuruecksetzen soll nichts zurückgeben, sondern protokoll ändern; es gibt {ergebnis!r} zurück."

# zuruecksetzen mit Konten in beliebiger Reihenfolge und mit leerer Liste
for konten in [[2, 0], [1], []]:
    protokoll = beispiel()
    zuruecksetzen(protokoll, konten)
    erwartet = beispiel()
    for konto in konten:
        erwartet[konto] = 0
    assert protokoll.tolist() == erwartet.tolist(), (
        f"Nach zuruecksetzen(protokoll, {konten}) ist protokoll\n{protokoll!r}\nerwartet war\n{erwartet!r}"
    )

# bereinigte_kopie setzt die Zeilen in der Kopie auf 0
protokoll = beispiel()
bericht = bereinigte_kopie(protokoll, [2])
erwartet = beispiel()
erwartet[2] = 0
assert isinstance(bericht, np.ndarray) and bericht.tolist() == erwartet.tolist(), (
    f"bereinigte_kopie(protokoll, [2]) ergibt\n{bericht!r}\nerwartet war\n{erwartet!r}"
)

# bereinigte_kopie lässt das Protokoll unverändert und teilt keinen Speicher
protokoll = beispiel()
bericht = bereinigte_kopie(protokoll, [0, 2])
bericht[1, 0] = 77
assert protokoll.tolist() == beispiel().tolist() and not np.shares_memory(bericht, protokoll), (
    "Nach bericht = bereinigte_kopie(protokoll, [0, 2]) und bericht[1, 0] = 77 soll protokoll unverändert sein; "
    f"es ist\n{protokoll!r}\nTipp: kopie = protokoll und kopie = protokoll[:] sind keine Kopien. "
    "Nehmen Sie protokoll.copy()."
)

# bereinigte_kopie mit leerer Liste ist eine unabhängige Kopie
protokoll = beispiel()
bericht = bereinigte_kopie(protokoll, [])
assert bericht.tolist() == protokoll.tolist() and not np.shares_memory(bericht, protokoll), (
    "bereinigte_kopie(protokoll, []) soll eine unveränderte, aber unabhängige Kopie liefern; "
    f"gleich: {bericht.tolist() == protokoll.tolist()}, teilt Speicher: {np.shares_memory(bericht, protokoll)}."
)

# Ein Protokoll ohne Konten
leer = np.zeros((0, 14), dtype=np.int64)
ergebnis = (wochenausschnitt(leer, 1).shape, bereinigte_kopie(leer, []).shape)
zuruecksetzen(leer, [])
assert ergebnis == ((0, 7), (0, 14)), (
    f"Bei einem Protokoll der Form (0, 14) ergeben wochenausschnitt(…, 1) und bereinigte_kopie(…, []) die Formen "
    f"{ergebnis}, erwartet war ((0, 7), (0, 14))."
)

# Viele zufällige Protokolle, verglichen mit einer Rechnung über Listen
zufall = Zufall(5003)
for _ in range(200):
    konten_anzahl = zufall.randint(0, 8)
    tage = 7 * zufall.randint(1, 6)
    werte = [[zufall.choice([0, 0, 0, zufall.randint(0, 10**6)]) for _ in range(tage)] for _ in range(konten_anzahl)]
    woche = zufall.randrange(tage // 7)
    konten = zufall.sample(range(konten_anzahl), zufall.randint(0, konten_anzahl))
    bereinigt = [[0] * tage if nummer in konten else list(zeile) for nummer, zeile in enumerate(werte)]

    protokoll = np.array(werte, dtype=np.int64).reshape(konten_anzahl, tage)
    ausschnitt = wochenausschnitt(protokoll, woche).tolist()
    woche_erwartet = [zeile[7 * woche : 7 * woche + 7] for zeile in werte]
    kopie = bereinigte_kopie(protokoll, konten)
    unveraendert = protokoll.tolist() == werte
    zuruecksetzen(protokoll, konten)
    bekommen = (ausschnitt, kopie.tolist(), unveraendert, protokoll.tolist())
    erwartet = (woche_erwartet, bereinigt, True, bereinigt)
    assert bekommen == erwartet, (
        f"Bei einem Protokoll mit {konten_anzahl} Konten und {tage} Tagen, woche = {woche}, konten = {konten}:\n"
        f"  wochenausschnitt richtig: {bekommen[0] == erwartet[0]}\n"
        f"  bereinigte_kopie richtig: {bekommen[1] == erwartet[1]}\n"
        f"  Protokoll nach bereinigte_kopie unverändert: {bekommen[2]}\n"
        f"  zuruecksetzen richtig: {bekommen[3] == erwartet[3]}"
    )

# An der oberen Grenze ohne Python-Schleife: 1000 Konten, 364 Tage
gross = np.arange(1000 * 364, dtype=np.int64).reshape(1000, 364) % 1000
konten = list(range(999, -1, -2))
_, schritte_kopie = zaehle_schritte(bereinigte_kopie, gross, konten)
_, schritte_ausschnitt = zaehle_schritte(wochenausschnitt, gross, 51)
_, schritte_zurueck = zaehle_schritte(zuruecksetzen, gross, konten)
schritte = (schritte_ausschnitt, schritte_zurueck, schritte_kopie)
assert max(schritte) <= 10 and gross[1].sum() == 0 and gross[0].sum() == (np.arange(364) % 1000).sum(), (
    f"Bei 1000 Konten, 364 Tagen und 500 Konten in konten brauchen wochenausschnitt, zuruecksetzen und "
    f"bereinigte_kopie {schritte} ausgeführte Zeilen, erwartet waren je höchstens 10.\n"
    "Tipp: Lassen Sie numpy die Arbeit machen: protokoll[konten] = 0 setzt alle Zeilen auf einmal."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Nach der Korrektur: 0\nBericht: 0 Protokoll: 12\nSumme nach dem Zurücksetzen: 12"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
