# Automatisch erzeugt aus lehrkraft/muster/4_030_prozessschritte.py - nicht von Hand ändern.
# vorlage-hash: e0da9dab0b2c11a3
# text-hash: d0619b95be6b5297
# thema: funktionen
# inhalt: Klassen- und Methodendekoratoren

def neu_registrieren(name):
    """Dekoriert eine neue leere Klasse mit prozessschritt(name); liefert (Klasse oder None, Ausnahme oder None)."""
    try:
        @prozessschritt(name)
        class Neu:
            """Ein Prozessschritt für die Tests."""

        return Neu, None
    except Exception as fehler:
        return None, fehler


# Der Klassendekorator gibt die Klasse selbst zurück
assert isinstance(Pruefung, type) and isinstance(Versand, type), (
    f"Nach @prozessschritt(...) ist Pruefung {Pruefung!r} und Versand {Versand!r}; erwartet waren die Klassen selbst.\n"
    "Tipp: Die innere Funktion des Dekorators muss die Klasse mit return zurückgeben."
)

# Die Klassen sind unter ihrem Namen eingetragen und kennen ihn
eintraege = {name: SCHRITTE.get(name) for name in ["pruefen", "versenden"]}
assert eintraege == {"pruefen": Pruefung, "versenden": Versand}, (
    f"SCHRITTE enthält für 'pruefen' und 'versenden' {eintraege!r}, erwartet waren die Klassen Pruefung und Versand."
)
assert getattr(Pruefung, "schrittname", None) == "pruefen" and getattr(Versand, "schrittname", None) == "versenden", (
    f"Pruefung.schrittname ist {getattr(Pruefung, 'schrittname', None)!r} und Versand.schrittname "
    f"{getattr(Versand, 'schrittname', None)!r}; erwartet waren 'pruefen' und 'versenden'."
)

# Eine weitere Klasse lässt sich eintragen (nicht fest hinschreiben!)
klasse, fehler = neu_registrieren("freigeben")
assert fehler is None and SCHRITTE.get("freigeben") is klasse and klasse.schrittname == "freigeben", (
    f"@prozessschritt('freigeben') über einer neuen Klasse: erwartet ist sie unter 'freigeben' in SCHRITTE "
    f"und hat schrittname 'freigeben'; Ausnahme: {fehler!r}, SCHRITTE: {SCHRITTE!r}."
)

# Ein schon vergebener Name löst ValueError aus, der alte Eintrag bleibt
vorher = dict(SCHRITTE)
klasse, fehler = neu_registrieren("pruefen")
assert isinstance(fehler, ValueError) and SCHRITTE == vorher and Pruefung.schrittname == "pruefen", (
    f"@prozessschritt('pruefen') ein zweites Mal soll einen ValueError auslösen und SCHRITTE nicht ändern; "
    f"Ausnahme: {fehler!r}, SCHRITTE danach: {SCHRITTE!r}.\n"
    "Tipp: Prüfen Sie zuerst, ob name schon in SCHRITTE steht, und ändern Sie erst danach etwas."
)

# Erst beim Dekorieren wird eingetragen, nicht schon bei prozessschritt(name)
prozessschritt("nur_aufgerufen")
assert "nur_aufgerufen" not in SCHRITTE, (
    "Schon prozessschritt('nur_aufgerufen') ohne Klasse hat etwas in SCHRITTE eingetragen.\n"
    "Tipp: Tragen Sie erst in der inneren Funktion ein, die die Klasse bekommt."
)

# Das Beispiel aus der Aufgabe
schritt_test = Pruefung(1000)
ergebnisse = (schritt_test.bearbeite(250), schritt_test.bearbeite(betrag=5000))
protokoll = getattr(schritt_test, "protokoll", None)
erwartet = [("bearbeite", (250,), {}, True), ("bearbeite", (), {"betrag": 5000}, False)]
assert ergebnisse == (True, False) and protokoll == erwartet, (
    "Pruefung(1000), dann bearbeite(250) und bearbeite(betrag=5000): erwartet die Ergebnisse (True, False) und das "
    f"Protokoll {erwartet!r};\nbekommen {ergebnisse!r} und {protokoll!r}."
)

# Positions- und Schlüsselwortargumente zusammen
versand = Versand()
ergebnis = versand.bearbeite("A-17", express=True)
erwartet = [("bearbeite", ("A-17",), {"express": True}, "Express")]
assert ergebnis == "Express" and getattr(versand, "protokoll", None) == erwartet, (
    f"Versand().bearbeite('A-17', express=True) ergibt {ergebnis!r} mit Protokoll {getattr(versand, 'protokoll', None)!r}; "
    f"erwartet waren 'Express' und {erwartet!r}.\nTipp: Reichen Sie *argumente und **benannte unverändert an die Methode weiter."
)

# Jedes Objekt hat sein eigenes Protokoll
erstes = Pruefung(10)
zweites = Pruefung(10)
erstes.bearbeite(5)
assert getattr(erstes, "protokoll", None) == [("bearbeite", (5,), {}, True)] and not hasattr(zweites, "protokoll"), (
    f"Nach erstes.bearbeite(5) hat erstes das Protokoll {getattr(erstes, 'protokoll', None)!r} und zweites "
    f"{getattr(zweites, 'protokoll', 'keins')!r}; erwartet waren [('bearbeite', (5,), {{}}, True)] und keins.\n"
    "Tipp: Legen Sie die Liste auf self an, nicht in der Hülle oder in der Klasse."
)

# Eine Ausnahme wird weitergereicht und nicht eingetragen
versand = Versand()
versand.bearbeite("B-1")
try:
    versand.bearbeite("")
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None and versand.protokoll == [("bearbeite", ("B-1",), {}, "Standard")], (
    "Versand().bearbeite('B-1'), dann bearbeite(''): erwartet ein ValueError aus der Methode und nur der erste Aufruf "
    f"im Protokoll; Ausnahme: {fehler!r}, Protokoll: {getattr(versand, 'protokoll', None)!r}.\n"
    "Tipp: Rufen Sie zuerst die Methode auf und tragen Sie erst danach ein; fangen Sie die Ausnahme nicht ab."
)

# Ein Protokoll aus __init__ wird weitergeführt
class MitProtokoll:
    def __init__(self):
        self.protokoll = ["angelegt"]

    @protokolliert
    def zaehle(self):
        return 3

objekt = MitProtokoll()
objekt.zaehle()
assert objekt.protokoll == ["angelegt", ("zaehle", (), {}, 3)], (
    f"Ein Objekt mit protokoll = ['angelegt'] hat nach zaehle() das Protokoll {objekt.protokoll!r}, "
    "erwartet war ['angelegt', ('zaehle', (), {}, 3)].\nTipp: Legen Sie die Liste nur an, wenn es sie noch nicht gibt."
)

# Name und Docstring bleiben erhalten
assert (Pruefung.bearbeite.__name__, Pruefung.bearbeite.__doc__) == (
    "bearbeite",
    "Gibt True zurück, wenn betrag höchstens die Grenze ist.",
), (
    f"Pruefung.bearbeite hat den Namen {Pruefung.bearbeite.__name__!r} und den Docstring {Pruefung.bearbeite.__doc__!r}; "
    "erwartet waren der Name und der Docstring der ursprünglichen Methode.\nTipp: Schreiben Sie @functools.wraps(methode) über die Hülle."
)

# Der Methodenname im Protokoll ist der der jeweiligen Methode
class Zwei:
    @protokolliert
    def erste(self, wert):
        return wert + 1

    @protokolliert
    def zweite(self):
        return None

objekt = Zwei()
objekt.erste(1)
objekt.zweite()
assert objekt.protokoll == [("erste", (1,), {}, 2), ("zweite", (), {}, None)], (
    f"Nach erste(1) und zweite() ist das Protokoll {objekt.protokoll!r}, "
    "erwartet war [('erste', (1,), {}, 2), ('zweite', (), {}, None)]."
)

# 1000 zufällige Aufrufe auf drei Objekten
zufall = Zufall(4030)
objekte = [Pruefung(zufall.randint(0, 100)) for _ in range(3)]
erwartet = [[] for _ in range(3)]
for _ in range(1000):
    nummer = zufall.randrange(3)
    betrag = zufall.randint(-50, 150)
    if zufall.random() < 0.5:
        ergebnis = objekte[nummer].bearbeite(betrag)
        erwartet[nummer].append(("bearbeite", (betrag,), {}, betrag <= objekte[nummer].grenze))
    else:
        ergebnis = objekte[nummer].bearbeite(betrag=betrag)
        erwartet[nummer].append(("bearbeite", (), {"betrag": betrag}, betrag <= objekte[nummer].grenze))
    assert ergebnis is (betrag <= objekte[nummer].grenze), (
        f"Pruefung({objekte[nummer].grenze}).bearbeite({betrag}) ergibt {ergebnis!r}."
    )
bekommen = [getattr(objekt, "protokoll", []) for objekt in objekte]
for nummer in range(3):
    assert bekommen[nummer] == erwartet[nummer], (
        f"Nach 1000 zufälligen Aufrufen auf drei Objekten weicht das Protokoll von Objekt {nummer} ab: "
        f"{len(bekommen[nummer])} statt {len(erwartet[nummer])} Einträge, die letzten: {bekommen[nummer][-2:]!r}, "
        f"erwartet: {erwartet[nummer][-2:]!r}."
    )

# Obere Grenze: 10 000 Aufrufe auf einem Objekt
viel = Pruefung(5000)
for betrag in range(10000):
    viel.bearbeite(betrag)
assert len(viel.protokoll) == 10000 and viel.protokoll[-1] == ("bearbeite", (9999,), {}, False), (
    f"Nach 10 000 Aufrufen hat das Protokoll {len(viel.protokoll)} Einträge, der letzte {viel.protokoll[-1]!r}; "
    "erwartet waren 10 000 Einträge, der letzte ('bearbeite', (9999,), {}, False)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[('bearbeite', (250,), {}, True), ('bearbeite', (), {'betrag': 5000}, False)]\nTrue pruefen"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm gibt aus:\n{AUSGABE}"
