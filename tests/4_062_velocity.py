# Automatisch erzeugt aus lehrkraft/muster/4_062_velocity.py - nicht von Hand ändern.
# vorlage-hash: b53cf64cd81e2978
# text-hash: 3efca1f62465eec1
# thema: datenstrukturen
# inhalt: deque mit maxlen und rotate

import math
from collections import deque

TEAMS = ["Web", "App", "Daten", "Netz"]


def mit_sprints(punkte, fenster=3):
    """Ein Velocity-Objekt, das die Sprints schon abgeschlossen hat."""
    v = Velocity(fenster)
    for wert in punkte:
        v.abschliessen(wert)
    return v


def aufruf(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def fehler_von(funktion, *argumente):
    """Ruft die Funktion auf und gibt die Ausnahme zurück, oder None, wenn keine kam."""
    try:
        funktion(*argumente)
    except Exception as fehler:
        return fehler
    return None


def erwartete_reihe(teams, schritte):
    """Vergleichslösung mit Slicing: das Team an Stelle schritte % len kommt nach vorn."""
    stelle = schritte % len(teams)
    return teams[stelle:] + teams[:stelle]


def erwartete_prognose(punkte, fenster, restpunkte):
    """Vergleichslösung ohne deque: nimmt die letzten fenster Werte mit Slicing."""
    letzte = punkte[-fenster:]
    if restpunkte == 0:
        return 0
    return -(-restpunkte * len(letzte) // sum(letzte))


def als_liste(wert):
    """Macht aus einer deque eine Liste, damit der Inhalt unabhängig von der Form verglichen wird."""
    if isinstance(wert, deque):
        return list(wert)
    return wert


# verlauf im Beispiel: nur die letzten drei Sprints
v = mit_sprints([21, 30, 18, 27])
ergebnis = aufruf(v.verlauf)
assert isinstance(ergebnis, (list, deque)) and list(ergebnis) == [30, 18, 27], (
    f"Nach den Sprints 21, 30, 18, 27 ergibt verlauf() {ergebnis!r}, erwartet war [30, 18, 27].\n"
    "Tipp: Mit deque(maxlen=fenster) fällt der älteste Wert von selbst heraus."
)

# letzte ist eine deque mit maxlen fenster
v = Velocity(5)
letzte = getattr(v, "letzte", None)
assert isinstance(letzte, deque) and letzte.maxlen == 5, (
    f"Velocity(5).letzte ist {letzte!r}, erwartet war deque([], maxlen=5).\n"
    "Tipp: self.letzte = deque(maxlen=fenster) in __init__."
)

# verlauf gibt eine Liste zurück, keine deque
ergebnis = aufruf(mit_sprints([1, 2]).verlauf)
assert type(ergebnis) is list and ergebnis == [1, 2], (
    f"verlauf() ergibt {ergebnis!r}, erwartet war die Liste [1, 2].\nTipp: list(self.letzte)."
)

# verlauf vor dem Füllen des Fensters
ergebnis = aufruf(mit_sprints([], 3).verlauf)
assert isinstance(ergebnis, (list, deque)) and list(ergebnis) == [], f"Ohne Sprints ergibt verlauf() {ergebnis!r}, erwartet war []."

# durchschnitt im Beispiel
ergebnis = aufruf(mit_sprints([21, 30, 18, 27]).durchschnitt)
assert isinstance(ergebnis, (int, float)) and math.isclose(ergebnis, 25.0), (
    f"Nach 21, 30, 18, 27 ergibt durchschnitt() {ergebnis!r}, erwartet war 25.0 (aus 30, 18, 27)."
)

# durchschnitt mit anderem Fenster (nicht fest hinschreiben!)
ergebnis = aufruf(mit_sprints([10, 20, 31, 40, 50], 2).durchschnitt)
assert isinstance(ergebnis, (int, float)) and math.isclose(ergebnis, 45.0), (
    f"Velocity(2) nach 10, 20, 31, 40, 50 ergibt durchschnitt() {ergebnis!r}, erwartet war 45.0.\n"
    "Tipp: Teilen Sie durch die Zahl der gespeicherten Sprints, nicht durch die Zahl aller Sprints."
)

# durchschnitt, solange das Fenster noch nicht voll ist
ergebnis = aufruf(mit_sprints([12, 15]).durchschnitt)
assert isinstance(ergebnis, (int, float)) and math.isclose(ergebnis, 13.5), (
    f"Nach nur zwei Sprints 12 und 15 ergibt durchschnitt() {ergebnis!r}, erwartet war 13.5.\n"
    "Tipp: Teilen Sie durch len(self.letzte), nicht durch das Fenster."
)

# durchschnitt ohne Sprint: ValueError
fehler = fehler_von(Velocity().durchschnitt)
assert isinstance(fehler, ValueError), (
    f"durchschnitt() ohne Sprint löst {fehler!r} aus, erwartet war ein ValueError.\n"
    "Tipp: Prüfen Sie len(self.letzte) == 0 und lösen Sie mit raise ValueError(...) aus."
)

# sprints_bis_fertig im Beispiel
ergebnis = aufruf(mit_sprints([21, 30, 18, 27]).sprints_bis_fertig, 60)
assert ergebnis == 3, (
    f"sprints_bis_fertig(60) ergibt bei Durchschnitt 25 {ergebnis!r}, erwartet war 3 (60 / 25 = 2.4, aufgerundet).\n"
    "Tipp: Aufrunden mit -(-a // b)."
)

# sprints_bis_fertig geht genau auf
ergebnis = aufruf(mit_sprints([20, 20, 20]).sprints_bis_fertig, 60)
assert ergebnis == 3, f"Bei Durchschnitt 20 ergibt sprints_bis_fertig(60) {ergebnis!r}, erwartet war 3, nicht 4."

# sprints_bis_fertig gibt eine ganze Zahl zurück
ergebnis = aufruf(mit_sprints([7, 9]).sprints_bis_fertig, 17)
assert ergebnis == 3 and isinstance(ergebnis, int), (
    f"Bei Durchschnitt 8 ergibt sprints_bis_fertig(17) {ergebnis!r}, erwartet war die ganze Zahl 3."
)

# sprints_bis_fertig rechnet genau: Durchschnitt 13 / 3, 65 Restpunkte sind genau 15 Sprints
ergebnis = aufruf(mit_sprints([4, 4, 5]).sprints_bis_fertig, 65)
assert ergebnis == 15, (
    f"Nach 4, 4, 5 ergibt sprints_bis_fertig(65) {ergebnis!r}, erwartet war 15 (65 · 3 / 13 = 15 genau).\n"
    "Tipp: 65 / (13 / 3) ist als Kommazahl 15.000000000000002; rechnen Sie mit -(-restpunkte * anzahl // summe)."
)

# sprints_bis_fertig: nichts mehr offen
ergebnis = aufruf(mit_sprints([0, 0]).sprints_bis_fertig, 0)
assert ergebnis == 0, f"Mit 0 Restpunkten ergibt sprints_bis_fertig(0) {ergebnis!r}, erwartet war 0, auch bei Velocity 0."

# sprints_bis_fertig ohne Sprint: ValueError
fehler = fehler_von(Velocity().sprints_bis_fertig, 10)
assert isinstance(fehler, ValueError), f"sprints_bis_fertig(10) ohne Sprint löst {fehler!r} aus, erwartet war ein ValueError."

# sprints_bis_fertig ohne Sprint: ValueError, auch bei 0 Restpunkten
fehler = fehler_von(Velocity().sprints_bis_fertig, 0)
assert isinstance(fehler, ValueError), (
    f"sprints_bis_fertig(0) ohne Sprint löst {fehler!r} aus, erwartet war ein ValueError.\n"
    "Tipp: Prüfen Sie zuerst, ob es überhaupt einen Sprint gibt, und erst danach die Restpunkte."
)

# sprints_bis_fertig bei Durchschnitt 0: ValueError statt ZeroDivisionError
fehler = fehler_von(mit_sprints([0, 0, 0]).sprints_bis_fertig, 10)
assert isinstance(fehler, ValueError), (
    f"sprints_bis_fertig(10) bei Velocity 0 löst {fehler!r} aus, erwartet war ein ValueError.\n"
    "Tipp: Prüfen Sie den Durchschnitt vor dem Teilen."
)

# nach_release im Beispiel: ein Schritt vor
ergebnis = aufruf(nach_release, list(TEAMS), 1)
assert ergebnis == ["App", "Daten", "Netz", "Web"], (
    f"nach_release(teams, 1) ergibt {ergebnis!r}, erwartet war ['App', 'Daten', 'Netz', 'Web'].\n"
    "Tipp: deque(teams), dann rotate; rotate(1) dreht nach rechts, das Weiterrücken nach vorn ist rotate(-1)."
)

# nach_release im Beispiel: ein Schritt zurück
ergebnis = aufruf(nach_release, list(TEAMS), -1)
assert ergebnis == ["Netz", "Web", "App", "Daten"], f"nach_release(teams, -1) ergibt {ergebnis!r}, erwartet war ['Netz', 'Web', 'App', 'Daten']."

# nach_release im Beispiel: mehr Schritte als Teams
ergebnis = aufruf(nach_release, list(TEAMS), 6)
assert ergebnis == ["Daten", "Netz", "Web", "App"], f"nach_release(teams, 6) ergibt {ergebnis!r}, erwartet war ['Daten', 'Netz', 'Web', 'App']."

# nach_release gibt eine Liste zurück und lässt teams unverändert
teams = list(TEAMS)
ergebnis = aufruf(nach_release, teams, 2)
assert type(ergebnis) is list and teams == TEAMS, (
    f"nach_release(teams, 2) ergibt {ergebnis!r} und teams ist danach {teams}; erwartet war eine neue Liste, teams unverändert."
)

# nach_release: Randfall 0 Schritte
ergebnis = aufruf(nach_release, list(TEAMS), 0)
assert ergebnis == TEAMS, f"nach_release(teams, 0) ergibt {ergebnis!r}, erwartet war {TEAMS}."

# nach_release: Randfall ein einziges Team
ergebnis = aufruf(nach_release, ["Web"], -7)
assert ergebnis == ["Web"], f"nach_release(['Web'], -7) ergibt {ergebnis!r}, erwartet war ['Web']."

# nach_release benutzt rotate
assert verwendet("rotate"), "Ihr Code verwendet rotate nicht. Drehen Sie eine deque mit rotate."

# Die Ausgabe des Programms
erwartet = "[30, 18, 27] 25.0 3\n['App', 'Daten', 'Netz', 'Web'] ['Netz', 'Web', 'App', 'Daten'] ['Daten', 'Netz', 'Web', 'App']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Sprintfolgen
zufall = Zufall(4062)
for _ in range(300):
    fenster = zufall.randint(1, 6)
    punkte = [zufall.randint(0, 50) for _ in range(zufall.randint(1, 10))]
    restpunkte = zufall.randint(0, 300)
    v = mit_sprints(punkte, fenster)
    assert als_liste(aufruf(v.verlauf)) == punkte[-fenster:], f"Velocity({fenster}) nach {punkte}: verlauf() ergibt {aufruf(v.verlauf)!r}."
    if sum(punkte[-fenster:]) == 0 and restpunkte > 0:
        assert isinstance(fehler_von(v.sprints_bis_fertig, restpunkte), ValueError), (
            f"Velocity({fenster}) nach {punkte}: sprints_bis_fertig({restpunkte}) sollte einen ValueError auslösen."
        )
    else:
        erwartet = erwartete_prognose(punkte, fenster, restpunkte)
        ergebnis = aufruf(v.sprints_bis_fertig, restpunkte)
        assert ergebnis == erwartet, (
            f"Velocity({fenster}) nach {punkte}: sprints_bis_fertig({restpunkte}) ergibt {ergebnis!r}, erwartet war {erwartet}."
        )

# Viele zufällige Reihen und Schritte
for _ in range(300):
    teams = [f"T{nummer}" for nummer in range(zufall.randint(1, 8))]
    schritte = zufall.randint(-20, 20)
    ergebnis = aufruf(nach_release, list(teams), schritte)
    assert ergebnis == erwartete_reihe(teams, schritte), (
        f"nach_release({teams}, {schritte}) ergibt {ergebnis!r}, erwartet war {erwartete_reihe(teams, schritte)}."
    )

# Obere Grenze: 100 000 Sprints, Fenster 20
punkte = [zufall.randint(0, 500) for _ in range(100000)]
v = mit_sprints(punkte, 20)
assert als_liste(aufruf(v.verlauf)) == punkte[-20:], "Nach 100 000 Sprints mit Fenster 20 stimmt verlauf() nicht."
assert len(getattr(v, "letzte", [])) == 20, "Nach 100 000 Sprints sollte letzte nur 20 Werte enthalten."

# Obere Grenze: 1000 Teams und sehr große Schritte
teams = [f"Team{nummer}" for nummer in range(1000)]
for schritte in [10**9, -(10**9), 999, -1001]:
    ergebnis = aufruf(nach_release, list(teams), schritte)
    assert ergebnis == erwartete_reihe(teams, schritte), f"Bei 1000 Teams stimmt nach_release(teams, {schritte}) nicht."
