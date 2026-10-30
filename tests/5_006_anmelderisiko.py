# Automatisch erzeugt aus lehrkraft/muster/5_006_anmelderisiko.py - nicht von Hand ändern.
# vorlage-hash: de90903b308c6c1e
# text-hash: 5ffcf4d417c40b67
# thema: datenanalyse
# inhalt: pandas: apply gegen vektorisiert

def tabelle(konten, fehlversuche, laender, stunden, index=None):
    """Baut ein DataFrame der Anmeldungen aus vier Listen, auf Wunsch mit eigenem Index."""
    return pd.DataFrame(
        {"konto": konten, "fehlversuche": fehlversuche, "land": laender, "stunde": stunden},
        index=index,
    )


def beschreibe(ergebnis):
    """Zeigt eine Series für die Fehlermeldung als Werte und Index."""
    if isinstance(ergebnis, pd.Series):
        return f"Series mit den Werten {ergebnis.tolist()} und dem Index {ergebnis.index.tolist()}"
    return repr(ergebnis)


def stimmt(ergebnis, werte, index):
    """True, wenn ergebnis eine Series ganzer Zahlen mit diesen Werten und diesem Index ist."""
    return (
        isinstance(ergebnis, pd.Series)
        and ergebnis.tolist() == werte
        and ergebnis.index.tolist() == index
        and pd.api.types.is_integer_dtype(ergebnis)
    )


def beispiel():
    """Liefert die Anmeldungen aus der Aufgabe."""
    return tabelle(["kaya", "nowak", "kaya", "admin"], [0, 3, 1, 7], ["DE", "DE", "BR", "DE"], [9, 3, 14, 2])


# risiko_mit_apply aus dem Beispiel
ergebnis = risiko_mit_apply(beispiel())
assert stimmt(ergebnis, [0, 50, 40, 90], [0, 1, 2, 3]), (
    f"risiko_mit_apply(anmeldungen) ergibt {beschreibe(ergebnis)}, erwartet waren die Werte [0, 50, 40, 90] "
    "mit dem Index [0, 1, 2, 3].\nTipp: anmeldungen.apply(risiko_zeile, axis=1) ruft risiko_zeile für jede Zeile auf."
)

# risiko_vektorisiert aus dem Beispiel
ergebnis = risiko_vektorisiert(beispiel())
assert stimmt(ergebnis, [0, 50, 40, 90], [0, 1, 2, 3]), (
    f"risiko_vektorisiert(anmeldungen) ergibt {beschreibe(ergebnis)}, erwartet waren die Werte [0, 50, 40, 90] "
    "mit dem Index [0, 1, 2, 3] als ganze Zahlen."
)

# Jede Regel für sich, auch an den Grenzen der Stunde
faelle = tabelle(
    ["a", "b", "c", "d", "e", "f", "g"],
    [0, 1, 0, 0, 0, 1000, 2],
    ["DE", "DE", "US", "DE", "DE", "FR", "AT"],
    [12, 12, 12, 5, 6, 0, 23],
)
erwartet = [0, 10, 30, 20, 0, 10050, 50]
for funktion in [risiko_mit_apply, risiko_vektorisiert]:
    ergebnis = funktion(faelle)
    assert stimmt(ergebnis, erwartet, list(range(7))), (
        f"{funktion.__name__} ergibt für fehlversuche [0, 1, 0, 0, 0, 1000, 2], land "
        "['DE', 'DE', 'US', 'DE', 'DE', 'FR', 'AT'] und stunde [12, 12, 12, 5, 6, 0, 23] "
        f"{beschreibe(ergebnis)}, erwartet waren die Werte {erwartet}.\n"
        "Tipp: Die 20 Punkte gibt es für die Stunden 0 bis 5, also stunde < 6."
    )

# Der Index bleibt erhalten, auch wenn er nicht bei 0 anfängt
gefiltert = tabelle(["x", "y", "z"], [2, 0, 1], ["DE", "PL", "DE"], [1, 8, 9], index=[17, 3, 250])
for funktion in [risiko_mit_apply, risiko_vektorisiert]:
    ergebnis = funktion(gefiltert)
    assert stimmt(ergebnis, [40, 30, 10], [17, 3, 250]), (
        f"{funktion.__name__} ergibt für ein DataFrame mit dem Index [17, 3, 250] {beschreibe(ergebnis)}, "
        "erwartet waren die Werte [40, 30, 10] mit demselben Index [17, 3, 250].\n"
        "Tipp: np.where liefert ein Array ohne Index; rechnen Sie direkt mit den Spalten oder geben Sie "
        "index=anmeldungen.index an."
    )

# Eine einzige Anmeldung
einzeln = tabelle(["root"], [0], ["DE"], [0])
for funktion in [risiko_mit_apply, risiko_vektorisiert]:
    ergebnis = funktion(einzeln)
    assert stimmt(ergebnis, [20], [0]), f"{funktion.__name__} ergibt für eine Anmeldung um 0 Uhr {beschreibe(ergebnis)}, erwartet [20]."

# Das DataFrame bleibt unverändert
anmeldungen = beispiel()
risiko_mit_apply(anmeldungen)
risiko_vektorisiert(anmeldungen)
verdaechtige_konten(anmeldungen, 0)
assert anmeldungen.equals(beispiel()), (
    "Nach den Auswertungen hat sich das DataFrame anmeldungen verändert; es soll so bleiben, wie es war.\n"
    f"Spalten jetzt: {list(anmeldungen.columns)}"
)

# verdaechtige_konten aus dem Beispiel und an verschiedenen Schwellen
for schwelle, erwartet in [(50, ["admin", "nowak"]), (40, ["admin", "kaya", "nowak"]), (0, ["admin", "kaya", "nowak"]), (91, []), (90, ["admin"])]:
    ergebnis = verdaechtige_konten(beispiel(), schwelle)
    assert ergebnis == erwartet, (
        f"verdaechtige_konten(anmeldungen, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Ein Konto zählt ab schwelle Punkten (>=), jedes Konto nur einmal, alphabetisch sortiert."
    )

# verdaechtige_konten gibt eine Python-Liste zurück
ergebnis = verdaechtige_konten(beispiel(), 40)
assert type(ergebnis) is list, (
    f"verdaechtige_konten(anmeldungen, 40) ergibt ein Objekt vom Typ {type(ergebnis).__name__}, erwartet war eine Liste."
)

# 200 zufällige Protokolle, verglichen mit einer Rechnung ohne pandas
zufall = Zufall(5006)
for _ in range(200):
    anzahl = zufall.randint(1, 8)
    konten = [zufall.choice(["kaya", "nowak", "admin", "lena"]) for _ in range(anzahl)]
    fehlversuche = [zufall.choice([0, 0, 1, 2, zufall.randint(0, 1000)]) for _ in range(anzahl)]
    laender = [zufall.choice(["DE", "DE", "AT", "US"]) for _ in range(anzahl)]
    stunden = [zufall.choice([5, 6, zufall.randint(0, 23)]) for _ in range(anzahl)]
    index = zufall.sample(range(1000), anzahl)
    schwelle = zufall.choice([0, 20, 30, 50, zufall.randint(0, 10100)])
    punkte = []
    for fehler, land, stunde in zip(fehlversuche, laender, stunden):
        punkte.append(10 * fehler + (0 if land == "DE" else 30) + (20 if stunde <= 5 else 0))
    erwartet_konten = sorted({konto for konto, wert in zip(konten, punkte) if wert >= schwelle})
    df = tabelle(konten, fehlversuche, laender, stunden, index=index)
    ergebnisse = (risiko_mit_apply(df), risiko_vektorisiert(df), verdaechtige_konten(df, schwelle))
    assert stimmt(ergebnisse[0], punkte, index) and stimmt(ergebnisse[1], punkte, index) and ergebnisse[2] == erwartet_konten, (
        f"Bei konto = {konten}, fehlversuche = {fehlversuche}, land = {laender}, stunde = {stunden}, "
        f"Index {index} und schwelle = {schwelle}:\n"
        f"  risiko_mit_apply: {beschreibe(ergebnisse[0])}\n"
        f"  risiko_vektorisiert: {beschreibe(ergebnisse[1])}\n"
        f"  erwartet waren die Werte {punkte}\n"
        f"  verdaechtige_konten: {ergebnisse[2]!r}, erwartet {erwartet_konten}"
    )

# risiko_mit_apply ruft risiko_zeile für jede Zeile auf
klein = tabelle(["k"] * 200, list(range(200)), ["DE", "US"] * 100, [3, 12] * 100)
ergebnis, schritte = zaehle_schritte(risiko_mit_apply, klein)
assert stimmt(ergebnis, [10 * nummer + (0 if nummer % 2 == 0 else 30) + (20 if nummer % 2 == 0 else 0) for nummer in range(200)], list(range(200))) and schritte >= 600, (
    f"risiko_mit_apply braucht bei 200 Zeilen {schritte} ausgeführte Zeilen; erwartet waren mindestens 600, "
    "weil risiko_zeile für jede Zeile laufen soll.\n"
    "Tipp: Diese Fassung soll zum Vergleich apply(risiko_zeile, axis=1) benutzen."
)

# An der oberen Grenze vektorisiert: 100 000 Anmeldungen ohne Python-Code pro Zeile
nummern = list(range(100000))
gross = tabelle(
    [f"konto{nummer % 997}" for nummer in nummern],
    [nummer % 1001 for nummer in nummern],
    ["DE" if nummer % 3 else "CN" for nummer in nummern],
    [nummer % 24 for nummer in nummern],
    index=[nummer * 2 for nummer in nummern],
)
erwartet_punkte = (
    gross["fehlversuche"].to_numpy() * 10
    + (gross["land"].to_numpy() != "DE") * 30
    + (gross["stunde"].to_numpy() < 6) * 20
).tolist()
punkte, schritte_punkte = zaehle_schritte(risiko_vektorisiert, gross)
konten, schritte_konten = zaehle_schritte(verdaechtige_konten, gross, 10050)
erwartet_konten = sorted({gross["konto"].iloc[nummer] for nummer in range(100000) if erwartet_punkte[nummer] >= 10050})
assert stimmt(punkte, erwartet_punkte, gross.index.tolist()) and konten == erwartet_konten, (
    "Bei 100 000 Anmeldungen stimmen die Ergebnisse von risiko_vektorisiert oder verdaechtige_konten(…, 10050) "
    f"nicht; verdaechtige_konten ergibt {konten!r}, erwartet war {erwartet_konten}."
)
assert schritte_punkte <= 10 and schritte_konten <= 15, (
    f"Bei 100 000 Anmeldungen brauchen risiko_vektorisiert und verdaechtige_konten {schritte_punkte} und "
    f"{schritte_konten} ausgeführte Zeilen, erwartet waren höchstens 10 und 15.\n"
    "Tipp: apply oder eine Schleife führen für jede Zeile Python-Code aus. Rechnen Sie mit ganzen Spalten, "
    'etwa (anmeldungen["land"] != "DE") * 30.'
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[0, 50, 40, 90]\n[0, 50, 40, 90]\n['admin', 'nowak']"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
