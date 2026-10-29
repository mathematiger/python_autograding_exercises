# Automatisch erzeugt aus lehrkraft/muster/5_004_nachbarn.py - nicht von Hand ändern.
# vorlage-hash: 59cbc7a23bf46f82
# text-hash: 15ba0ddb206eed55
# thema: klassen
# inhalt: `__slots__`

# Das Beispiel aus der Aufgabe
punkte = [Messpunkt(1, 1, "normal"), Messpunkt(2, 1, "normal"), Messpunkt(8, 9, "defekt"), GewichteterPunkt(3, 2, "defekt", 3)]
ergebnis = (klassifiziere(punkte, 2, 2, 1), klassifiziere(punkte, 2, 2, 3))
assert ergebnis == ("normal", "defekt"), (
    f"Für das Beispiel aus der Aufgabe ergeben klassifiziere(punkte, 2, 2, 1) und klassifiziere(punkte, 2, 2, 3) "
    f"{ergebnis!r}, erwartet war ('normal', 'defekt')."
)

# Ein Messpunkt hat kein __dict__
punkt = Messpunkt(1, 2, "normal")
assert not hasattr(punkt, "__dict__"), (
    f"Ein Messpunkt hat noch ein __dict__: {getattr(punkt, '__dict__', None)!r}.\n"
    'Tipp: __slots__ = ("x", "y", "klasse") im Klassenkörper von Messpunkt.'
)

# Die Attribute eines Messpunkts lassen sich weiter lesen und ändern
punkt = Messpunkt(1, 2, "normal")
punkt.klasse = "defekt"
punkt.x = 4.5
assert (punkt.x, punkt.y, punkt.klasse) == (4.5, 2, "defekt"), (
    f"Nach Messpunkt(1, 2, 'normal'), klasse = 'defekt' und x = 4.5 sind x, y, klasse "
    f"{(punkt.x, punkt.y, punkt.klasse)!r}, erwartet war (4.5, 2, 'defekt')."
)

# Ein Tippfehler im Attributnamen löst einen AttributeError aus
punkt = Messpunkt(1, 2, "normal")
try:
    punkt.klase = "defekt"
    fehler = None
except AttributeError as ausnahme:
    fehler = ausnahme
assert fehler is not None, (
    'punkt.klase = "defekt" (mit Tippfehler) muss bei einem Messpunkt einen AttributeError auslösen.'
)

# Ein gewichteter Punkt hat auch kein __dict__
punkt = GewichteterPunkt(1, 2, "defekt", 2.5)
assert not hasattr(punkt, "__dict__"), (
    "Ein GewichteterPunkt hat noch ein __dict__. Eine Unterklasse ohne eigenes __slots__ bekommt wieder eines.\n"
    'Tipp: __slots__ = ("gewicht",) im Klassenkörper von GewichteterPunkt.'
)

# Ein gewichteter Punkt hat x, y, klasse und gewicht, aber kein anderes Attribut
punkt = GewichteterPunkt(1, 2, "defekt", 2.5)
punkt.gewicht = 4
try:
    punkt.farbe = "rot"
    fehler = None
except AttributeError as ausnahme:
    fehler = ausnahme
werte = (punkt.x, punkt.y, punkt.klasse, punkt.gewicht, punkt.stimme())
assert fehler is not None and werte == (1, 2, "defekt", 4, 4), (
    f"GewichteterPunkt(1, 2, 'defekt', 2.5) mit gewicht = 4 hat x, y, klasse, gewicht, stimme() = {werte!r}, "
    f"erwartet war (1, 2, 'defekt', 4, 4); punkt.farbe = 'rot' muss einen AttributeError auslösen "
    f"({'ist passiert' if fehler else 'ist nicht passiert'})."
)

# GewichteterPunkt nennt in __slots__ nur das neue Attribut
slots = GewichteterPunkt.__dict__.get("__slots__", ())
namen = {slots} if isinstance(slots, str) else set(slots)
assert namen == {"gewicht"}, (
    f"GewichteterPunkt.__slots__ ist {slots!r}, erwartet war nur ('gewicht',).\n"
    "Tipp: x, y und klasse erbt GewichteterPunkt schon von Messpunkt; sie noch einmal zu nennen, belegt den Platz doppelt."
)

# klassifiziere mit k = 1 nimmt den nächsten Punkt (nicht fest hinschreiben!)
punkte = [Messpunkt(0, 0, "normal"), Messpunkt(10, 10, "defekt"), Messpunkt(-5, 3, "warnung")]
for x, y, erwartet in [(1, 1, "normal"), (9, 7, "defekt"), (-4, 4, "warnung"), (-1.5, 0.5, "normal")]:
    ergebnis = klassifiziere(punkte, x, y, 1)
    assert ergebnis == erwartet, f"klassifiziere(punkte, {x}, {y}, 1) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Mehrheit unter den k nächsten, Gewichte zählen
punkte = [
    Messpunkt(0, 0, "normal"),
    Messpunkt(1, 0, "normal"),
    GewichteterPunkt(0, 1, "defekt", 1.5),
    Messpunkt(5, 5, "defekt"),
    Messpunkt(6, 5, "defekt"),
]
for k, erwartet in [(1, "normal"), (2, "normal"), (3, "normal"), (4, "defekt"), (5, "defekt")]:
    ergebnis = klassifiziere(punkte, 0, 0, k)
    assert ergebnis == erwartet, (
        f"Bei Punkten normal (0, 0), normal (1, 0), defekt (0, 1) mit Gewicht 1.5, defekt (5, 5), defekt (6, 5) ergibt "
        f"klassifiziere(punkte, 0, 0, {k}) {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Zählen Sie mit punkt.stimme(), nicht mit 1 pro Punkt."
    )

# Gleichstand: die Klasse mit dem nächsten Punkt gewinnt
punkte = [Messpunkt(3, 0, "defekt"), Messpunkt(1, 0, "normal"), Messpunkt(-2, 0, "defekt"), Messpunkt(0, 2, "normal")]
ergebnis = klassifiziere(punkte, 0, 0, 4)
assert ergebnis == "normal", (
    f"Bei je 2 Stimmen für normal und defekt ergibt klassifiziere {ergebnis!r}, erwartet war 'normal', weil der "
    "nächste Punkt (1, 0) normal ist."
)

# Gleicher Abstand: der Punkt weiter vorn in der Liste gilt als näher
punkte = [Messpunkt(0, 1, "defekt"), Messpunkt(1, 0, "normal"), Messpunkt(0, -1, "normal"), Messpunkt(-1, 0, "defekt")]
for k, erwartet in [(1, "defekt"), (2, "defekt"), (3, "normal"), (4, "defekt")]:
    ergebnis = klassifiziere(punkte, 0, 0, k)
    assert ergebnis == erwartet, (
        f"Alle vier Punkte haben den Abstand 1 zu (0, 0); klassifiziere(punkte, 0, 0, {k}) ergibt {ergebnis!r}, "
        f"erwartet war {erwartet!r}, weil die ersten {k} Punkte der Liste als die nächsten gelten."
    )


# Vergleichslösung: Punkte nach (Abstand, Position) auswählen, Stimmen getrennt zählen
def klassifiziere_langsam(punkte, x, y, k):
    """Wählt k-mal den nächsten noch freien Punkt aus und zählt danach die Stimmen."""
    frei = list(range(len(punkte)))
    gewaehlt = []
    for _ in range(k):
        bester = frei[0]
        for nummer in frei:
            if punkte[nummer].abstand_quadrat(x, y) < punkte[bester].abstand_quadrat(x, y):
                bester = nummer
        frei.remove(bester)
        gewaehlt.append(punkte[bester])
    klassen = []
    for punkt in gewaehlt:
        if punkt.klasse not in klassen:
            klassen.append(punkt.klasse)
    summen = [sum(p.stimme() for p in gewaehlt if p.klasse == klasse) for klasse in klassen]
    return klassen[summen.index(max(summen))]


# Viele zufällige Punktmengen mit ganzzahligen Gewichten
zufall = Zufall(5004)
for _ in range(300):
    punkte = []
    for _ in range(zufall.randint(1, 12)):
        px, py = zufall.randint(-5, 5), zufall.randint(-5, 5)
        klasse = zufall.choice(["normal", "defekt", "warnung"])
        if zufall.random() < 0.3:
            punkte.append(GewichteterPunkt(px, py, klasse, zufall.randint(1, 4)))
        else:
            punkte.append(Messpunkt(px, py, klasse))
    x, y = zufall.randint(-6, 6), zufall.randint(-6, 6)
    k = zufall.randint(1, len(punkte))
    erwartet = klassifiziere_langsam(punkte, x, y, k)
    ergebnis = klassifiziere(punkte, x, y, k)
    beschreibung = ", ".join(
        f"{p.klasse} ({p.x}, {p.y})" + (f" Gewicht {p.gewicht}" if isinstance(p, GewichteterPunkt) else "")
        for p in punkte
    )
    assert ergebnis == erwartet, (
        f"Bei den Punkten {beschreibung} ergibt klassifiziere(punkte, {x}, {y}, {k}) {ergebnis!r}, erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 2000 Punkte an den Rändern des Wertebereichs
punkte = [Messpunkt(-(10**4) + nummer, 10**4, "normal" if nummer % 3 else "defekt") for nummer in range(2000)]
punkte.append(GewichteterPunkt(10**4, -(10**4), "warnung", 0.5))
punkte = punkte[1:]
for x, y, k, erwartet in [(-(10**4), 10**4, 1, "normal"), (-(10**4), 10**4, 2000, "normal"), (10**4, -(10**4), 1, "warnung")]:
    ergebnis = klassifiziere(punkte, x, y, k)
    assert ergebnis == erwartet, (
        f"Bei 2000 Punkten an den Rändern ergibt klassifiziere(punkte, {x}, {y}, {k}) {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Die Ausgabe des Programms stimmt
assert AUSGABE == "normal\ndefekt", f"Erwartete Ausgabe:\nnormal\ndefekt\nIhr Programm:\n{AUSGABE}"
