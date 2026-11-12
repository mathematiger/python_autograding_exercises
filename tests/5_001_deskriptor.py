# Automatisch erzeugt aus lehrkraft/muster/5_001_deskriptor.py - nicht von Hand ändern.
# vorlage-hash: 2e5bb16722e1f1f5
# text-hash: 70913981522a45c2
# thema: klassen
# inhalt: Deskriptoren

# Werte werden gespeichert und gelesen
r = Rechteck(3, 4)
assert (r.breite, r.hoehe, r.flaeche()) == (3, 4, 12), (
    f"Nach Rechteck(3, 4) erwartet breite=3, hoehe=4, flaeche()=12, gefunden: {r.breite!r}, {r.hoehe!r}, {r.flaeche()!r}."
)

# Zuweisung nach dem Erzeugen wirkt
r = Rechteck(3, 4)
r.breite = 5
assert r.flaeche() == 20, f"Nach r.breite = 5 ergibt flaeche() {r.flaeche()!r}, erwartet war 20."

# Jede Instanz hat ihre eigenen Werte (Wert nicht im Deskriptor speichern!)
a = Rechteck(1, 2)
b = Rechteck(10, 20)
assert (a.breite, b.breite) == (1, 10), (
    f"Zwei Rechtecke teilen sich den Wert: a.breite={a.breite!r}, b.breite={b.breite!r}, erwartet 1 und 10.\n"
    "Tipp: Speichern Sie den Wert in objekt.__dict__, nicht in self."
)

# Der Deskriptor kennt seinen Namen aus __set_name__ und speichert unter ihm im __dict__
r = Rechteck(3, 4)
gespeichert = dict(vars(r))
assert gespeichert.get("breite") == 3 and gespeichert.get("hoehe") == 4, (
    "Positiv soll sich in __set_name__ den Attributnamen merken und den Wert in __set__ unter genau diesem "
    f"Namen im __dict__ des Objekts ablegen; nach Rechteck(3, 4) erwartet breite 3 und hoehe 4 in r.__dict__, "
    f"gefunden: {gespeichert!r}."
)

# Zugriff über die Klasse liefert den Deskriptor selbst
assert isinstance(Rechteck.breite, Positiv), (
    f"Rechteck.breite soll das Positiv-Objekt liefern, wenn objekt None ist; gefunden: {Rechteck.breite!r}."
)

# Ungültige Werte lösen ValueError mit dem Attributnamen aus, der alte Wert bleibt
r = Rechteck(3, 4)
for wert in [0, -1, -2.5, "5", None]:
    try:
        r.hoehe = wert
        meldung = None
        andere = None
    except ValueError as ausnahme:
        meldung = str(ausnahme)
        andere = None
    except TypeError as ausnahme:
        meldung = None
        andere = ausnahme
    assert meldung is not None and vergleichbar("hoehe") in vergleichbar(meldung) and r.hoehe == 4, (
        f"r.hoehe = {wert!r} muss einen ValueError auslösen, dessen Meldung 'hoehe' enthält, "
        f"und hoehe bei 4 lassen; Meldung: {meldung!r}, hoehe danach: {r.hoehe!r}"
        + (f", stattdessen kam {andere!r}.\nTipp: Prüfen Sie zuerst, ob wert eine Zahl ist (int oder float, nicht bool)." if andere else ".")
        + ("\nTipp: Prüfen Sie zuerst und speichern Sie erst danach." if meldung is not None and r.hoehe != 4 else "")
    )

# Ein nie gesetzter Wert löst AttributeError aus, kein KeyError
leer = Rechteck.__new__(Rechteck)
try:
    ergebnis = (hasattr(leer, "breite"), getattr(leer, "hoehe", "fehlt"))
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == (False, "fehlt"), (
    "Für ein Rechteck, dessen breite und hoehe nie gesetzt wurden, sollen hasattr(r, 'breite') False und "
    f"getattr(r, 'hoehe', 'fehlt') 'fehlt' ergeben; bekommen: {ergebnis!r}.\n"
    "Tipp: Fehlt der Name in objekt.__dict__, lösen Sie in __get__ einen AttributeError aus."
)

# Positive Kommazahlen sind erlaubt
r = Rechteck(2.5, 2)
assert r.flaeche() == 5.0, f"Rechteck(2.5, 2).flaeche() ergibt {r.flaeche()!r}, erwartet war 5.0."

# Derselbe Deskriptor funktioniert in einer anderen Klasse
class Kreis:
    radius = Positiv()

    def __init__(self, radius):
        self.radius = radius

k = Kreis(7)
try:
    k.radius = -1
    meldung = None
except ValueError as ausnahme:
    meldung = str(ausnahme)
assert k.radius == 7 and vars(k).get("radius") == 7 and meldung is not None and vergleichbar("radius") in vergleichbar(meldung), (
    "Positiv muss unverändert auch in der Klasse Kreis als radius funktionieren: erwartet k.radius == 7, "
    "k.__dict__['radius'] == 7 und bei k.radius = -1 ein ValueError mit 'radius' in der Meldung; "
    f"gefunden: k.radius = {k.radius!r}, k.__dict__ = {vars(k)!r}, Meldung: {meldung!r}."
)

# Ungültiger Wert im Konstruktor wird ebenfalls abgefangen
try:
    Rechteck(3, 0)
    geklappt = True
except ValueError:
    geklappt = False
assert not geklappt, "Rechteck(3, 0) muss einen ValueError auslösen, weil hoehe 0 nicht positiv ist."

# Werte an den Rändern der Grenzen
r = Rechteck(10**9, 1e-9)
r.breite = 1
ergebnis = (r.breite, r.hoehe)
try:
    r.hoehe = -(10**9)
    meldung = None
except ValueError as ausnahme:
    meldung = str(ausnahme)
assert ergebnis == (1, 1e-9) and meldung is not None and r.hoehe == 1e-9, (
    "Rechteck(10**9, 1e-9), dann breite = 1 und hoehe = -10**9: erwartet (breite, hoehe) = (1, 1e-9) und ein ValueError, "
    f"bekommen {ergebnis!r} und Meldung {meldung!r}, hoehe danach {r.hoehe!r}."
)

# Viele zufällige Zuweisungen an mehrere Rechtecke: gültige Werte kommen an, ungültige lösen ValueError aus
zufall = Zufall(5001)
fehlerfall = None
rechtecke = [Rechteck(1, 1) for _ in range(3)]
erwartet = [{"breite": 1, "hoehe": 1} for _ in range(3)]
schritte = []
for versuch in range(1000):
    nummer = zufall.randrange(3)
    name = zufall.choice(["breite", "hoehe"])
    wert = zufall.choice([
        zufall.randint(-5, 5), zufall.randint(-10**9, 10**9), zufall.uniform(-2, 2),
        zufall.choice([1e-9, -1e-9, 0.0, "3", "", None]),
    ])
    schritte = (schritte + [f"r{nummer}.{name} = {wert!r}"])[-4:]
    gueltig = type(wert) in (int, float) and wert > 0
    try:
        setattr(rechtecke[nummer], name, wert)
        meldung = None
    except ValueError as ausnahme:
        meldung = str(ausnahme)
    if gueltig:
        erwartet[nummer][name] = wert
    bekommen = [{"breite": r.breite, "hoehe": r.hoehe} for r in rechtecke]
    if (meldung is None) != gueltig or (meldung is not None and vergleichbar(name) not in vergleichbar(meldung)) or bekommen != erwartet:
        fehlerfall = (schritte, gueltig, meldung, erwartet, bekommen)
        break
assert fehlerfall is None, (
    f"Nach den letzten Zuweisungen {'; '.join(fehlerfall[0])} (r0 bis r2 sind drei Rechtecke):\n"
    f"  beim letzten Schritt erwartet {'kein ValueError' if fehlerfall[1] else 'ein ValueError mit dem Attributnamen'}, "
    f"Meldung: {fehlerfall[2]!r}\n"
    f"  Werte erwartet {fehlerfall[3]}\n  bekommen       {fehlerfall[4]}"
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("12"), f'Erwartete Ausgabe: "12" – Ihr Programm: "{AUSGABE}"'
