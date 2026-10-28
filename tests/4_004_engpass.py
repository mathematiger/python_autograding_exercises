# Automatisch erzeugt aus lehrkraft/muster/4_004_engpass.py - nicht von Hand ändern.
# vorlage-hash: 3ce4fcc5cf85683a
# thema: klassen
# inhalt: `__lt__` und `total_ordering`

# Ein kürzerer Schritt ist kleiner als ein längerer
try:
    kleiner = Prozessschritt("Erfassen", 5) < Prozessschritt("Prüfen", 12)
    fehler = None
except TypeError as ausnahme:
    kleiner = None
    fehler = ausnahme
assert fehler is None and kleiner is True, (
    'Prozessschritt("Erfassen", 5) < Prozessschritt("Prüfen", 12) ergibt '
    f"{kleiner!r} bzw. löst {fehler!r} aus, erwartet war True.\n"
    "Tipp: Schreiben Sie die Methode __lt__ und vergleichen Sie darin zuerst die Dauer."
)

# Die Dauer entscheidet, nicht der Name (nicht nur Namen vergleichen!)
for links, rechts, erwartet in [
    (Prozessschritt("Zählen", 3), Prozessschritt("Archivieren", 20), True),
    (Prozessschritt("Archivieren", 20), Prozessschritt("Zählen", 3), False),
    (Prozessschritt("Prüfen", 12), Prozessschritt("Erfassen", 5), False),
    (Prozessschritt("Packen", 9), Prozessschritt("Packen", 10), True),
]:
    ergebnis = links < rechts
    assert ergebnis is erwartet, f"{links!r} < {rechts!r} ergibt {ergebnis!r}, erwartet war {erwartet}."

# Bei gleicher Dauer entscheidet der Name
for links, rechts, erwartet in [
    (Prozessschritt("Prüfen", 12), Prozessschritt("Verpacken", 12), True),
    (Prozessschritt("Verpacken", 12), Prozessschritt("Prüfen", 12), False),
]:
    ergebnis = links < rechts
    assert ergebnis is erwartet, (
        f"{links!r} < {rechts!r} ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Vergleichen Sie Tupel: (self.dauer, self.name) < (other.dauer, other.name)."
    )

# Ein Schritt ist nicht kleiner als er selbst
schritt = Prozessschritt("Prüfen", 12)
ergebnis = schritt < Prozessschritt("Prüfen", 12)
assert ergebnis is False, (
    f'Prozessschritt("Prüfen", 12) < Prozessschritt("Prüfen", 12) ergibt {ergebnis!r}, erwartet war False.\n'
    "Tipp: Benutzen Sie in __lt__ das echte Kleiner-Zeichen <, nicht <=."
)

# Gleiche Schritte sind gleich, verschiedene nicht
gleich = Prozessschritt("Prüfen", 12) == Prozessschritt("Prüfen", 12)
verschieden = [
    Prozessschritt("Prüfen", 12) == Prozessschritt("Prüfen", 13),
    Prozessschritt("Prüfen", 12) == Prozessschritt("Packen", 12),
]
assert gleich is True and verschieden == [False, False], (
    f'Prozessschritt("Prüfen", 12) == Prozessschritt("Prüfen", 12) ergibt {gleich!r} (erwartet True); '
    f"Vergleiche mit anderer Dauer bzw. anderem Namen ergeben {verschieden} (erwartet [False, False])."
)

# total_ordering erzeugt <=, > und >=
try:
    a = Prozessschritt("Erfassen", 5)
    b = Prozessschritt("Prüfen", 12)
    ergebnisse = [a <= b, b <= a, a <= Prozessschritt("Erfassen", 5), b > a, a > b, b >= a, a >= b]
    fehler = None
except TypeError as ausnahme:
    ergebnisse = None
    fehler = ausnahme
assert ergebnisse == [True, False, True, True, False, True, False], (
    "Für a = Erfassen (5) und b = Prüfen (12) sollen a <= b, b <= a, a <= a, b > a, a > b, b >= a, a >= b "
    f"die Werte [True, False, True, True, False, True, False] ergeben; Ergebnis: {ergebnisse!r}, Ausnahme: {fehler!r}.\n"
    "Tipp: Setzen Sie @functools.total_ordering in die Zeile direkt über class Prozessschritt."
)

# sorted sortiert nach Dauer und bei gleicher Dauer nach Name
schritte = [
    Prozessschritt("Prüfen", 12),
    Prozessschritt("Erfassen", 5),
    Prozessschritt("Verpacken", 12),
    Prozessschritt("Versenden", 8),
    Prozessschritt("Kommissionieren", 12),
]
erwartet = [
    Prozessschritt("Erfassen", 5),
    Prozessschritt("Versenden", 8),
    Prozessschritt("Kommissionieren", 12),
    Prozessschritt("Prüfen", 12),
    Prozessschritt("Verpacken", 12),
]
ergebnis = sorted(schritte)
assert ergebnis == erwartet, f"sorted(...) ergibt\n{ergebnis}\nerwartet war\n{erwartet}"

# max findet den Engpass, min den schnellsten Schritt
schritte = [Prozessschritt("Erfassen", 4), Prozessschritt("Prüfen", 15), Prozessschritt("Versenden", 7)]
engpass = max(schritte)
schnellster = min(schritte)
assert engpass == Prozessschritt("Prüfen", 15) and schnellster == Prozessschritt("Erfassen", 4), (
    f"max(...) ergibt {engpass!r} (erwartet Prozessschritt('Prüfen', 15)), "
    f"min(...) ergibt {schnellster!r} (erwartet Prozessschritt('Erfassen', 4))."
)

# Vergleiche mit anderen Typen: == ergibt False, < löst TypeError aus
gleich = Prozessschritt("Erfassen", 5) == ("Erfassen", 5)
try:
    Prozessschritt("Erfassen", 5) < 5
    typfehler = False
except TypeError:
    typfehler = True
assert gleich is False and typfehler, (
    f'Prozessschritt("Erfassen", 5) == ("Erfassen", 5) ergibt {gleich!r} (erwartet False), '
    f'und Prozessschritt("Erfassen", 5) < 5 löst {"einen" if typfehler else "keinen"} TypeError aus (erwartet: einen).\n'
    "Tipp: Prüfen Sie mit isinstance(other, Prozessschritt) und geben Sie sonst NotImplemented zurück."
)

# __eq__ und __lt__ geben bei fremden Objekten NotImplemented zurück
ergebnisse = [Prozessschritt("Erfassen", 5).__eq__(5), Prozessschritt("Erfassen", 5).__lt__(5)]
assert ergebnisse == [NotImplemented, NotImplemented], (
    f'Prozessschritt("Erfassen", 5).__eq__(5) und .__lt__(5) ergeben {ergebnisse!r}, '
    "erwartet war beide Male NotImplemented."
)

# Dauer an den Rändern der Grenzen und als Kommazahl
schritte = [Prozessschritt("Prüfen", 10000), Prozessschritt("Warten", 0), Prozessschritt("Packen", 7.5), Prozessschritt("Erfassen", 7)]
ergebnis = sorted(schritte)
erwartet = [Prozessschritt("Warten", 0), Prozessschritt("Erfassen", 7), Prozessschritt("Packen", 7.5), Prozessschritt("Prüfen", 10000)]
assert ergebnis == erwartet, f"sorted({schritte}) ergibt\n{ergebnis}\nerwartet war\n{erwartet}"

# Viele zufällige Paare: alle sechs Vergleiche stimmen mit dem Vergleich der Tupel (dauer, name) überein
zufall = Zufall(4004)
fehlerfall = None
for versuch in range(1000):
    a = (zufall.choice(["Erfassen", "Prüfen", "Packen"]), zufall.randint(0, 6) / 2)
    b = (zufall.choice(["Erfassen", "Prüfen", "Packen"]), zufall.randint(0, 6) / 2)
    x, y = Prozessschritt(*a), Prozessschritt(*b)
    ta, tb = (a[1], a[0]), (b[1], b[0])
    bekommen = [x == y, x != y, x < y, x <= y, x > y, x >= y]
    erwartet = [ta == tb, ta != tb, ta < tb, ta <= tb, ta > tb, ta >= tb]
    if bekommen != erwartet:
        fehlerfall = f"Für a = {x!r} und b = {y!r} ergeben a == b, a != b, a < b, a <= b, a > b, a >= b\n{bekommen}, erwartet war\n{erwartet}."
        break
assert fehlerfall is None, fehlerfall

# Viele zufällige Listen: sorted(schritte) ordnet wie sorted über die Tupel (dauer, name)
zufall = Zufall(40042)
fehlerfall = None
for versuch in range(200):
    daten = [(zufall.choice("ABCDE"), zufall.randint(0, 10)) for _ in range(versuch // 10)]  # erst kurze Listen, damit die Meldung klein bleibt
    ergebnis = [(s.name, s.dauer) for s in sorted(Prozessschritt(name, dauer) for name, dauer in daten)]
    erwartet = sorted(daten, key=lambda paar: (paar[1], paar[0]))
    if ergebnis != erwartet:
        fehlerfall = f"sorted() über die Schritte {daten} ergibt\n{ergebnis}\nerwartet war\n{erwartet}"
        break
assert fehlerfall is None, fehlerfall

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[Prozessschritt('Erfassen', 5), Prozessschritt('Versenden', 8), "
    "Prozessschritt('Prüfen', 12), Prozessschritt('Verpacken', 12)]\n"
    "Engpass: Prozessschritt('Verpacken', 12)"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
