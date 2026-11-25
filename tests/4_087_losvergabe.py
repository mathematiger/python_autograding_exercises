# Automatisch erzeugt aus lehrkraft/muster/4_087_losvergabe.py - nicht von Hand ändern.
# vorlage-hash: f2f839ca4cc3f74e
# text-hash: 96d2fb5fffc7f8f2
# thema: algorithmen
# inhalt: Backtracking mit Abschneiden

import copy
import functools

LOSE = ["Hardware", "Verkabelung", "Wartung", "Schulung"]
ANGEBOTE = {
    "Hardware": {"Nordtech": 52000, "Datenwerk": 49000},
    "Verkabelung": {"Nordtech": 18000, "Kabelprofi": 21000, "Datenwerk": 19500},
    "Wartung": {"Datenwerk": 12000, "Servicepunkt": 15000},
    "Schulung": {"Servicepunkt": 4000, "Datenwerk": 3500, "Nordtech": 5000},
}
KAPAZITAET = {"Nordtech": 2, "Datenwerk": 2, "Kabelprofi": 1, "Servicepunkt": 1}
BESTE = {"Hardware": "Datenwerk", "Verkabelung": "Nordtech", "Wartung": "Datenwerk", "Schulung": "Servicepunkt"}


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def mangel(lose, angebote, kapazitaet, ergebnis):
    """Beschreibt, was an einem Ergebnis (kosten, vergabe) nicht stimmt, oder gibt None zurück."""
    if not isinstance(ergebnis, tuple) or len(ergebnis) != 2 or not isinstance(ergebnis[1], dict):
        return "Erwartet war ein Paar (kosten, vergabe) mit einem Dictionary vergabe."
    kosten, vergabe = ergebnis
    if sorted(vergabe) != sorted(lose):
        return f"vergabe enthält die Lose {sorted(vergabe)}, erwartet waren genau {sorted(lose)}."
    for los, anbieter in vergabe.items():
        if anbieter not in angebote[los]:
            return f"{los!r} geht an {anbieter!r}, der dafür kein Angebot abgegeben hat."
    for anbieter, anzahl in kapazitaet.items():
        bekommen = [los for los in vergabe if vergabe[los] == anbieter]
        if len(bekommen) > anzahl:
            return f"{anbieter!r} bekommt {bekommen}, darf aber höchstens {anzahl} Lose übernehmen."
    summe = sum(angebote[los][anbieter] for los, anbieter in vergabe.items())
    if kosten != summe:
        return f"kosten ist {kosten!r}, die Preise der Vergabe ergeben aber zusammen {summe}."
    return None


def vergleich(lose, angebote, kapazitaet):
    """Vergleichslösung: dynamische Programmierung über (Los, schon vergebene Lose je Anbieter)."""
    anbieter_liste = sorted(kapazitaet)

    @functools.lru_cache(maxsize=None)
    def rest(i, belegt):
        """Kleinste Kosten für die Lose ab i, wenn belegt[j] Lose an anbieter_liste[j] gehen; None, wenn unmöglich."""
        if i == len(lose):
            return 0
        bestes = None
        for anbieter, preis in angebote[lose[i]].items():
            j = anbieter_liste.index(anbieter)
            if belegt[j] < kapazitaet[anbieter]:
                danach = rest(i + 1, belegt[:j] + (belegt[j] + 1,) + belegt[j + 1:])
                if danach is not None and (bestes is None or preis + danach < bestes):
                    bestes = preis + danach
        return bestes

    return rest(0, (0,) * len(anbieter_liste))


def abweichung(lose, angebote, kapazitaet, ergebnis, fehler):
    """Vergleicht ein Ergebnis mit der Vergleichslösung; beschreibt den Fehler oder gibt None zurück."""
    erwartet = vergleich(lose, angebote, kapazitaet)
    if fehler is not None:
        return f"Der Aufruf löst {fehler} aus."
    if erwartet is None:
        return None if ergebnis is None else "Erwartet war None, weil es keine vollständige Vergabe gibt."
    if ergebnis is None:
        return f"Es gibt aber eine vollständige Vergabe, die günstigste kostet {erwartet}."
    problem = mangel(lose, angebote, kapazitaet, ergebnis)
    if problem is None and ergebnis[0] != erwartet:
        problem = f"Die Vergabe kostet {ergebnis[0]}, es geht aber für {erwartet}."
    return problem


def zufallsausschreibung(zufall, anzahl_lose, anzahl_anbieter, max_kapazitaet):
    """Erzeugt eine zufällige Ausschreibung (lose, angebote, kapazitaet)."""
    anbieter = [f"Firma {nummer}" for nummer in range(anzahl_anbieter)]
    lose = [f"Los {nummer}" for nummer in range(anzahl_lose)]
    angebote = {}
    for los in lose:
        bieter = zufall.sample(anbieter, zufall.randint(1, min(4, anzahl_anbieter)))
        angebote[los] = {name: zufall.randint(1, 1000) for name in bieter}
    kapazitaet = {name: zufall.randint(0, max_kapazitaet) for name in anbieter}
    return lose, angebote, kapazitaet


# untergrenzen: das Beispiel
ergebnis, fehler = rufe(lambda: untergrenzen(LOSE, ANGEBOTE))
assert ergebnis == [82500, 33500, 15500, 3500, 0], (
    f"untergrenzen(lose, angebote) im Beispiel ergibt {ergebnis!r}, erwartet war [82500, 33500, 15500, 3500, 0].\n"
    "Tipp: Rechnen Sie von hinten nach vorn: Stelle i ist Stelle i + 1 plus der billigste Preis von lose[i]."
    + absturz(fehler)
)

# untergrenzen: andere Lose (nicht fest hinschreiben!)
angebote = {"Server": {"A": 700, "B": 650}, "Lizenzen": {"B": 90}, "Netz": {"A": 300, "C": 310}}
ergebnis, fehler = rufe(lambda: untergrenzen(["Lizenzen", "Server", "Netz"], angebote))
assert ergebnis == [1040, 950, 300, 0], (
    f"untergrenzen(['Lizenzen', 'Server', 'Netz'], {angebote}) ergibt {ergebnis!r}, erwartet war [1040, 950, 300, 0]."
    + absturz(fehler)
)

# untergrenzen: keine Lose
ergebnis, fehler = rufe(lambda: untergrenzen([], {}))
assert ergebnis == [0], f"untergrenzen([], {{}}) ergibt {ergebnis!r}, erwartet war [0]." + absturz(fehler)

# sackgasse: das Beispiel, Wartung findet niemanden mehr
frei = {"Nordtech": 2, "Datenwerk": 0, "Kabelprofi": 1, "Servicepunkt": 0}
ergebnis, fehler = rufe(lambda: sackgasse(LOSE, 2, ANGEBOTE, frei))
assert ergebnis is True, (
    f"sackgasse(lose, 2, angebote, {frei}) ergibt {ergebnis!r}, erwartet war True: Wartung hat nur Angebote von "
    "Datenwerk und Servicepunkt, und beide sind voll." + absturz(fehler)
)

# sackgasse: jedes restliche Los hat noch jemanden
frei = {"Nordtech": 2, "Datenwerk": 0, "Kabelprofi": 1, "Servicepunkt": 0}
ergebnis, fehler = rufe(lambda: sackgasse(LOSE, 3, ANGEBOTE, frei))
assert ergebnis is False, (
    f"sackgasse(lose, 3, angebote, {frei}) ergibt {ergebnis!r}, erwartet war False: Die Schulung kann noch an Nordtech."
    + absturz(fehler)
)

# sackgasse: am Anfang mit voller Kapazität
ergebnis, fehler = rufe(lambda: sackgasse(LOSE, 0, ANGEBOTE, dict(KAPAZITAET)))
assert ergebnis is False, f"sackgasse(lose, 0, angebote, kapazitaet) ergibt {ergebnis!r}, erwartet war False." + absturz(fehler)

# sackgasse: Lose vor ab zählen nicht mehr
frei = {"Nordtech": 0, "Datenwerk": 0, "Kabelprofi": 0, "Servicepunkt": 1}
ergebnis, fehler = rufe(lambda: (sackgasse(LOSE, 0, ANGEBOTE, frei), sackgasse(LOSE, 2, ANGEBOTE, frei)))
assert ergebnis == (True, False), (
    f"Mit frei = {frei} ergeben sackgasse(lose, 0, …) und sackgasse(lose, 2, …) {ergebnis!r}, erwartet war "
    "(True, False): Hardware und Verkabelung sind schon vergeben, wenn ab 2 ist; Wartung und Schulung können noch an "
    "Servicepunkt.\nTipp: Sehen Sie nur die Lose lose[ab:] an." + absturz(fehler)
)

# sackgasse: alle Lose vergeben, also keine Sackgasse
frei = {"Nordtech": 0, "Datenwerk": 0, "Kabelprofi": 0, "Servicepunkt": 0}
ergebnis, fehler = rufe(lambda: sackgasse(LOSE, 4, ANGEBOTE, frei))
assert ergebnis is False, (
    f"sackgasse(lose, 4, angebote, {frei}) ergibt {ergebnis!r}, erwartet war False: Es ist kein Los mehr übrig."
    + absturz(fehler)
)

# guenstigste_vergabe: die Kosten im Beispiel
ergebnis, fehler = rufe(lambda: guenstigste_vergabe(LOSE, copy.deepcopy(ANGEBOTE), dict(KAPAZITAET)))
kosten = ergebnis[0] if isinstance(ergebnis, tuple) and ergebnis else ergebnis
assert kosten == 83000, (
    f"guenstigste_vergabe im Beispiel ergibt {ergebnis!r}; erwartet waren die Kosten 83000.\n"
    "Tipp: Das billigste Angebot für jedes Los (82500) geht nicht, weil Datenwerk dann drei Lose bekäme." + absturz(fehler)
)

# guenstigste_vergabe: die Vergabe im Beispiel
ergebnis, fehler = rufe(lambda: guenstigste_vergabe(LOSE, copy.deepcopy(ANGEBOTE), dict(KAPAZITAET)))
assert isinstance(ergebnis, tuple) and len(ergebnis) == 2 and ergebnis[1] == BESTE, (
    f"guenstigste_vergabe im Beispiel ergibt {ergebnis!r}, erwartet war (83000, {BESTE!r}).\n"
    "Tipp: Speichern Sie eine Kopie von vergabe (dict(vergabe)), denn die Suche ändert vergabe danach weiter."
    + absturz(fehler)
)

# guenstigste_vergabe: ein Anbieter darf nicht mehr Lose bekommen, als seine Kapazität erlaubt
angebote = {"Monitore": {"Bildpunkt": 300, "Nordtech": 400}, "Drucker": {"Bildpunkt": 200, "Nordtech": 260}}
kapazitaet = {"Bildpunkt": 1, "Nordtech": 2}
ergebnis, fehler = rufe(lambda: guenstigste_vergabe(["Monitore", "Drucker"], angebote, kapazitaet))
erwartet = (560, {"Monitore": "Bildpunkt", "Drucker": "Nordtech"})
assert ergebnis == erwartet, (
    f"Bei angebote = {angebote} und kapazitaet = {kapazitaet} ergibt guenstigste_vergabe {ergebnis!r}, erwartet war "
    f"{erwartet!r}: Bildpunkt darf nur ein Los übernehmen." + absturz(fehler)
)

# guenstigste_vergabe: keine vollständige Vergabe möglich
kapazitaet = {"Nordtech": 1, "Datenwerk": 1, "Kabelprofi": 0, "Servicepunkt": 1}
ergebnis, fehler = rufe(lambda: guenstigste_vergabe(LOSE, copy.deepcopy(ANGEBOTE), kapazitaet))
assert fehler is None and ergebnis is None, (
    f"Mit kapazitaet = {kapazitaet} ergibt guenstigste_vergabe {ergebnis!r}, erwartet war None: Hardware und "
    "Verkabelung belegen Nordtech und Datenwerk, die Wartung bekommt Servicepunkt, und für die Schulung bleibt "
    "niemand." + absturz(fehler)
)

# guenstigste_vergabe: ein Los, für das nur ausgeschlossene Anbieter geboten haben
angebote = {"Wartung": {"Servicepunkt": 15000}, "Schulung": {"Nordtech": 5000}}
ergebnis, fehler = rufe(lambda: guenstigste_vergabe(["Wartung", "Schulung"], angebote, {"Servicepunkt": 0, "Nordtech": 1}))
assert fehler is None and ergebnis is None, (
    f"Bei angebote = {angebote} und kapazitaet = {{'Servicepunkt': 0, 'Nordtech': 1}} ergibt guenstigste_vergabe "
    f"{ergebnis!r}, erwartet war None: Kapazität 0 heißt, Servicepunkt bekommt nichts." + absturz(fehler)
)

# guenstigste_vergabe: keine Lose kosten nichts
ergebnis, fehler = rufe(lambda: guenstigste_vergabe([], {}, {"Nordtech": 2}))
assert ergebnis == (0, {}), f"guenstigste_vergabe([], {{}}, {{'Nordtech': 2}}) ergibt {ergebnis!r}, erwartet war (0, {{}})." + absturz(fehler)

# guenstigste_vergabe: angebote und kapazitaet bleiben unverändert
angebote, kapazitaet = copy.deepcopy(ANGEBOTE), dict(KAPAZITAET)
rufe(lambda: guenstigste_vergabe(LOSE, angebote, kapazitaet))
assert angebote == ANGEBOTE and kapazitaet == KAPAZITAET, (
    f"Nach guenstigste_vergabe ist kapazitaet {kapazitaet!r} (vorher {KAPAZITAET!r}) und angebote "
    f"{'verändert' if angebote != ANGEBOTE else 'unverändert'}.\nTipp: Rechnen Sie mit einer Kopie, etwa "
    "frei = dict(kapazitaet)."
)

zufall = Zufall(4087)

# Viele zufällige Ausschreibungen im Vergleich mit einer anderen Lösung
for _ in range(150):
    lose, angebote, kapazitaet = zufallsausschreibung(zufall, zufall.randint(0, 6), zufall.randint(1, 5), 3)
    ergebnis, fehler = rufe(lambda: guenstigste_vergabe(lose, copy.deepcopy(angebote), dict(kapazitaet)))
    problem = abweichung(lose, angebote, kapazitaet, ergebnis, fehler)
    assert problem is None, f"guenstigste_vergabe({lose}, {angebote}, {kapazitaet}) ergibt {ergebnis!r}.\n{problem}"

# Laufzeit: Zweige, die nicht billiger werden können, abschneiden
zufall = Zufall(8)
lose = [f"Los {nummer}" for nummer in range(8)]
angebote = {los: {f"Firma {nummer}": zufall.randint(100, 1000) for nummer in range(4)} for los in lose}
kapazitaet = {f"Firma {nummer}": 3 for nummer in range(4)}
ergebnis, schritte = zaehle_schritte(guenstigste_vergabe, lose, angebote, kapazitaet)
erwartet = vergleich(lose, angebote, kapazitaet)
assert isinstance(ergebnis, tuple) and ergebnis[0] == erwartet and schritte <= 12_000, (
    f"Acht Lose mit je vier Angeboten, jede Firma höchstens drei Lose: guenstigste_vergabe ergibt die Kosten "
    f"{ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis!r} (erwartet {erwartet}) und braucht {schritte} "
    "Schritte; erlaubt sind 12000. Ohne Abschneiden sieht die Suche fast alle 4**8 = 65536 Vergaben an.\n"
    "Tipp: Brechen Sie ab, sobald kosten + untergrenzen[i] >= bisher beste Kosten ist, und probieren Sie die "
    "billigsten Angebote zuerst."
)

# Laufzeit: auch gleich teure Zweige abschneiden (>= statt >)
lose = [f"Los {nummer}" for nummer in range(8)]
angebote = {los: {firma: 500 for firma in "ABCD"} for los in lose}
ergebnis, schritte = zaehle_schritte(guenstigste_vergabe, lose, angebote, {firma: 2 for firma in "ABCD"})
assert isinstance(ergebnis, tuple) and ergebnis[0] == 4000 and schritte <= 5000, (
    f"Acht Lose, vier Firmen bieten jedes für 500 Euro, jede Firma höchstens zwei Lose: guenstigste_vergabe ergibt "
    f"{ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis!r} (erwartet 4000) und braucht {schritte} Schritte; "
    "erlaubt sind 5000.\nTipp: Schon die erste Vergabe ist so billig wie die Untergrenze; brechen Sie auch ab, wenn "
    "ein Zweig nur gleich teuer werden kann (>=, nicht >)."
)

# Laufzeit: Sackgassen früh erkennen
lose = [f"Los {nummer}" for nummer in range(9)]
angebote = {los: {"A": 50, "B": 50, "C": 50} for los in lose}
angebote["Los 0"] = {"X": 10, "A": 20}
angebote["Los 8"] = {"X": 10}
kapazitaet = {"X": 1, "A": 9, "B": 9, "C": 9}
ergebnis, schritte = zaehle_schritte(guenstigste_vergabe, lose, angebote, kapazitaet)
assert isinstance(ergebnis, tuple) and ergebnis[0] == 380 and schritte <= 5000, (
    f"Neun Lose; Los 0 geht am billigsten an X, aber X darf nur ein Los übernehmen und ist der einzige Anbieter für "
    f"Los 8. guenstigste_vergabe ergibt {ergebnis[0] if isinstance(ergebnis, tuple) else ergebnis!r} (erwartet 380) "
    f"und braucht {schritte} Schritte; erlaubt sind 5000.\nTipp: Prüfen Sie bei jedem Aufruf mit sackgasse, ob ein "
    "späteres Los niemanden mehr findet. Sonst probiert die Suche nach Los 0 → X alle Vergaben von Los 1 bis 7 durch. "
    "Hier kosten viele Vergaben gleich viel; brechen Sie auch ab, wenn die Kosten das bisher Beste nur erreichen (>=)."
)

# Obere Grenze: zwölf Lose mit je vier Angeboten
zufall = Zufall(12)
firmen = [f"Firma {nummer}" for nummer in range(6)]
lose = [f"Los {nummer}" for nummer in range(12)]
for _ in range(5):
    angebote = {los: {name: zufall.randint(1, 10**6) for name in zufall.sample(firmen, 4)} for los in lose}
    kapazitaet = {name: zufall.randint(1, 4) for name in firmen}
    ergebnis, fehler = rufe(lambda: guenstigste_vergabe(lose, angebote, kapazitaet))
    problem = abweichung(lose, angebote, kapazitaet, ergebnis, fehler)
    assert problem is None, (
        f"Bei zwölf Losen mit kapazitaet = {kapazitaet} und angebote = {angebote} ergibt guenstigste_vergabe "
        f"{ergebnis!r}.\n{problem}"
    )
