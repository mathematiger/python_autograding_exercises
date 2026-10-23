# Automatisch erzeugt aus lehrkraft/muster/5_001_deskriptor.py - nicht von Hand ändern.
# vorlage-hash: 1f4e1fb892dfed05

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

# Der Deskriptor kennt seinen Namen aus __set_name__
assert getattr(Rechteck.__dict__["breite"], "name", None) == "breite", (
    "Positiv muss sich in __set_name__ den Attributnamen unter self.name merken; "
    f"gefunden: {getattr(Rechteck.__dict__['breite'], 'name', None)!r}."
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
    except ValueError as ausnahme:
        meldung = str(ausnahme)
    assert meldung is not None and "hoehe" in meldung and r.hoehe == 4, (
        f"r.hoehe = {wert!r} muss einen ValueError auslösen, dessen Meldung 'hoehe' enthält, "
        f"und hoehe bei 4 lassen; Meldung: {meldung!r}, hoehe danach: {r.hoehe!r}."
    )

# Positive Kommazahlen sind erlaubt
r = Rechteck(2.5, 2)
assert r.flaeche() == 5.0, f"Rechteck(2.5, 2).flaeche() ergibt {r.flaeche()!r}, erwartet war 5.0."

# Derselbe Deskriptor funktioniert in einer anderen Klasse
class Kreis:
    radius = Positiv()

    def __init__(self, radius):
        self.radius = radius

assert Kreis(7).radius == 7 and Kreis.__dict__["radius"].name == "radius", (
    "Positiv muss unverändert auch in der Klasse Kreis als radius funktionieren."
)

# Ungültiger Wert im Konstruktor wird ebenfalls abgefangen
try:
    Rechteck(3, 0)
    geklappt = True
except ValueError:
    geklappt = False
assert not geklappt, "Rechteck(3, 0) muss einen ValueError auslösen, weil hoehe 0 nicht positiv ist."

# Die Ausgabe des Programms stimmt
assert AUSGABE == "12", f'Erwartete Ausgabe: "12" – Ihr Programm: "{AUSGABE}"'
