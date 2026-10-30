# Automatisch erzeugt aus lehrkraft/muster/4_013_leitungsauslastung.py - nicht von Hand ändern.
# vorlage-hash: 94b382d275726fda
# text-hash: a26506773b127515
# thema: datenanalyse
# inhalt: numpy: Achsen und Broadcasting

def beispiel():
    """Liefert frische Kopien von verkehr und bandbreite aus der Aufgabe."""
    return np.array([[200, 850, 400], [90, 100, 95]], dtype=np.int64), np.array([1000, 100], dtype=np.int64)


def gleich(ergebnis, erwartet):
    """True, wenn ergebnis ein numpy-Array ist, das bis auf Rundungsfehler die verschachtelte Liste erwartet hat."""
    if not isinstance(ergebnis, np.ndarray):
        return False
    soll = np.array(erwartet, dtype=float)
    return ergebnis.shape == soll.shape and bool(np.allclose(ergebnis, soll, rtol=0, atol=1e-9))


def als_liste(ergebnis):
    """Zeigt ein Ergebnis für die Fehlermeldung als Liste, falls es ein Array ist."""
    if isinstance(ergebnis, np.ndarray):
        return f"array({ergebnis.tolist()})"
    return repr(ergebnis)


verkehr, bandbreite = beispiel()

# spitzen: eine Zahl pro Leitung
ergebnis = spitzen(verkehr)
assert gleich(ergebnis, [850, 100]), (
    f"spitzen(verkehr) ergibt {als_liste(ergebnis)}, erwartet war array([850, 100]), der höchste Wert jeder Zeile.\n"
    "Tipp: Mit axis=0 bekommen Sie eine Zahl pro Spalte, mit axis=1 eine Zahl pro Zeile."
)

# stundenmittel: eine Zahl pro Stunde
ergebnis = stundenmittel(verkehr)
assert gleich(ergebnis, [145.0, 475.0, 247.5]), (
    f"stundenmittel(verkehr) ergibt {als_liste(ergebnis)}, erwartet war array([145., 475., 247.5]), der "
    "Mittelwert jeder Spalte.\nTipp: Achse 0 läuft die Zeilen hinunter; mean(axis=0) fasst sie zusammen."
)

# auslastung: Bandbreite je Zeile, nicht je Spalte
try:
    ergebnis = auslastung(verkehr, bandbreite)
except ValueError as fehler:
    ergebnis = fehler
assert gleich(ergebnis, [[20.0, 85.0, 40.0], [90.0, 100.0, 95.0]]), (
    f"auslastung(verkehr, bandbreite) ergibt {als_liste(ergebnis)}, erwartet war "
    "array([[20., 85., 40.], [90., 100., 95.]]).\n"
    "Tipp: bandbreite hat die Form (2,) und passt so nur zu den Spalten. Als Spalte der Form (2, 1), "
    "bandbreite[:, np.newaxis], wird sie je Zeile verrechnet."
)

# auslastung bei einem quadratischen Array: hier passen auch die falschen Formen, rechnen aber falsch
verkehr_quadrat = np.array([[10, 20, 30], [10, 20, 30], [10, 20, 30]], dtype=np.int64)
bandbreite_quadrat = np.array([10, 100, 1000], dtype=np.int64)
ergebnis = auslastung(verkehr_quadrat, bandbreite_quadrat)
erwartet = [[100.0, 200.0, 300.0], [10.0, 20.0, 30.0], [1.0, 2.0, 3.0]]
assert gleich(ergebnis, erwartet), (
    f"Bei drei Leitungen und drei Stunden ergibt auslastung({verkehr_quadrat.tolist()}, "
    f"{bandbreite_quadrat.tolist()}) {als_liste(ergebnis)}, erwartet war array({erwartet}).\n"
    "Tipp: Ohne np.newaxis teilt numpy jede Spalte durch eine andere Bandbreite, nicht jede Zeile."
)

# ueberlastet aus dem Beispiel; über schwelle heißt echt größer
for schwelle, erwartet in [(90, [1]), (80, [0, 1]), (99, [1]), (100, []), (0, [0, 1]), (1000, [])]:
    ergebnis = ueberlastet(verkehr, bandbreite, schwelle)
    assert ergebnis == erwartet, (
        f"ueberlastet(verkehr, bandbreite, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Eine Leitung zählt, wenn ihre Auslastung in mindestens einer Stunde größer als die Schwelle ist."
    )

# ueberlastet gibt eine Python-Liste von ganzen Zahlen zurück
ergebnis = ueberlastet(verkehr, bandbreite, 80)
assert type(ergebnis) is list and all(type(nummer) is int for nummer in ergebnis), (
    f"ueberlastet(verkehr, bandbreite, 80) ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, "
    "erwartet war die Python-Liste [0, 1].\nTipp: .tolist() macht aus einem Array eine Liste."
)

# Eine Leitung, eine Stunde
verkehr_klein = np.array([[0]], dtype=np.int64)
bandbreite_klein = np.array([1], dtype=np.int64)
ergebnis = (
    als_liste(spitzen(verkehr_klein)),
    als_liste(stundenmittel(verkehr_klein)),
    als_liste(auslastung(verkehr_klein, bandbreite_klein)),
    ueberlastet(verkehr_klein, bandbreite_klein, 0),
)
assert ergebnis == ("array([0])", "array([0.0])", "array([[0.0]])", []), (
    f"Bei verkehr = [[0]] und bandbreite = [1] ergeben spitzen, stundenmittel, auslastung und ueberlastet(…, 0) "
    f"{ergebnis}, erwartet war ('array([0])', 'array([0.0])', 'array([[0.0]])', [])."
)

# Verkehr über der Bandbreite
verkehr_stau = np.array([[100000]], dtype=np.int64)
ergebnis = auslastung(verkehr_stau, np.array([1], dtype=np.int64))
assert gleich(ergebnis, [[10**7]]) and ueberlastet(verkehr_stau, np.array([1]), 1000) == [0], (
    f"Bei 100 000 Mbit/s auf einer Leitung mit 1 Mbit/s ergibt auslastung {als_liste(ergebnis)}, "
    "erwartet war array([[10000000.]]), und die Leitung ist überlastet."
)

# Die Eingaben bleiben unverändert
verkehr, bandbreite = beispiel()
spitzen(verkehr)
stundenmittel(verkehr)
auslastung(verkehr, bandbreite)
ueberlastet(verkehr, bandbreite, 50)
assert verkehr.tolist() == beispiel()[0].tolist() and bandbreite.tolist() == beispiel()[1].tolist(), (
    f"Nach den Auswertungen sind verkehr und bandbreite {verkehr.tolist()} und {bandbreite.tolist()}, "
    "erwartet war, dass sie unverändert bleiben."
)

# 300 zufällige Netze, verglichen mit einer Rechnung über verschachtelte Listen
zufall = Zufall(4013)
for _ in range(300):
    leitungen = zufall.randint(1, 6)
    stunden = zufall.choice([leitungen, zufall.randint(1, 6)])
    werte = [[zufall.choice([0, zufall.randint(0, 200), zufall.randint(0, 10**5)]) for _ in range(stunden)] for _ in range(leitungen)]
    breiten = [zufall.choice([1, 100, zufall.randint(1, 10**5)]) for _ in range(leitungen)]
    schwelle = zufall.choice([0, 50, 100, zufall.randint(0, 1000)])
    while any(wert * 100 == schwelle * breiten[i] for i, zeile in enumerate(werte) for wert in zeile):
        # Genau auf der Schwelle hängt das Ergebnis vom Rundungsfehler der Kommazahl ab: 7 / 100 * 100
        # ist 7.000000000000001. Dann wird eine andere Schwelle gewählt.
        schwelle = zufall.randint(0, 1000)
    erwartet_spitzen = [max(zeile) for zeile in werte]
    erwartet_mittel = [sum(zeile[s] for zeile in werte) / leitungen for s in range(stunden)]
    erwartet_last = [[wert * 100 / breiten[i] for wert in zeile] for i, zeile in enumerate(werte)]
    # Ganzzahlig verglichen, damit Rundungsfehler bei Auslastung genau an der Schwelle nichts verfälschen
    erwartet_ueber = [i for i, zeile in enumerate(werte) if any(wert * 100 > schwelle * breiten[i] for wert in zeile)]
    verkehr_test = np.array(werte, dtype=np.int64)
    bandbreite_test = np.array(breiten, dtype=np.int64)
    try:
        ergebnis = (
            spitzen(verkehr_test),
            stundenmittel(verkehr_test),
            auslastung(verkehr_test, bandbreite_test),
            ueberlastet(verkehr_test, bandbreite_test, schwelle),
        )
    except ValueError as fehler:
        ergebnis = (fehler, fehler, fehler, fehler)
    richtig = (
        gleich(ergebnis[0], erwartet_spitzen),
        gleich(ergebnis[1], erwartet_mittel),
        gleich(ergebnis[2], erwartet_last),
        ergebnis[3] == erwartet_ueber,
    )
    assert all(richtig), (
        f"Bei verkehr = {werte}, bandbreite = {breiten} und schwelle = {schwelle}:\n"
        f"  spitzen: {als_liste(ergebnis[0])}, erwartet {erwartet_spitzen}\n"
        f"  stundenmittel: {als_liste(ergebnis[1])}, erwartet {erwartet_mittel}\n"
        f"  auslastung: {als_liste(ergebnis[2])}, erwartet {erwartet_last}\n"
        f"  ueberlastet: {ergebnis[3]!r}, erwartet {erwartet_ueber}"
    )

# An der oberen Grenze ohne Python-Schleife: 1000 Leitungen, 168 Stunden
verkehr_gross = (np.arange(1000 * 168, dtype=np.int64).reshape(1000, 168) * 7) % 100001
bandbreite_gross = np.arange(1, 1001, dtype=np.int64) * 100
messungen = [
    zaehle_schritte(spitzen, verkehr_gross),
    zaehle_schritte(stundenmittel, verkehr_gross),
    zaehle_schritte(auslastung, verkehr_gross, bandbreite_gross),
    zaehle_schritte(ueberlastet, verkehr_gross, bandbreite_gross, 1000),
]
erwartet_ueber = np.flatnonzero((verkehr_gross * 100 > 1000 * bandbreite_gross[:, None]).any(axis=1)).tolist()
richtig = (
    gleich(messungen[0][0], verkehr_gross.max(axis=1)),
    gleich(messungen[1][0], verkehr_gross.mean(axis=0)),
    gleich(messungen[2][0], verkehr_gross / bandbreite_gross[:, None] * 100),
    messungen[3][0] == erwartet_ueber,
)
assert all(richtig), (
    "Bei 1000 Leitungen und 168 Stunden stimmen nicht alle Ergebnisse; richtig sind "
    f"(spitzen, stundenmittel, auslastung, ueberlastet): {richtig}."
)
schritte = tuple(schritte for _, schritte in messungen)
assert max(schritte) <= 12, (
    f"Bei 1000 Leitungen und 168 Stunden brauchen spitzen, stundenmittel, auslastung und ueberlastet {schritte} "
    "ausgeführte Zeilen, erwartet waren je höchstens 12.\n"
    "Tipp: Mit axis und Broadcasting rechnet numpy alles auf einmal, ohne Schleife über Leitungen oder Stunden."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[850, 100]\n[145.0, 475.0, 247.5]\n[[20.0, 85.0, 40.0], [90.0, 100.0, 95.0]]\n[1]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
