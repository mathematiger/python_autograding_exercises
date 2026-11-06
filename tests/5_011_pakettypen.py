# Automatisch erzeugt aus lehrkraft/muster/5_011_pakettypen.py - nicht von Hand ändern.
# vorlage-hash: de5f5b7161db8589
# text-hash: 96f5314779a4bb08
# thema: klassen
# inhalt: Klassen mit type() erzeugen

import ast
import inspect
import textwrap


def ausnahme_bei(aufruf):
    """Führt aufruf() aus und gibt die ausgelöste Ausnahme zurück, oder None, wenn keine kam."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


def bauweise(funktion):
    """Gibt zurück, ob die Funktion type() mit drei Argumenten aufruft und ob sie eine class-Anweisung enthält."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False, True
    mit_type = False
    mit_class = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id == "type":
            mit_type = mit_type or len(knoten.args) == 3
        if isinstance(knoten, ast.ClassDef):
            mit_class = True
    return mit_type, mit_class


# erzeuge_typ liefert eine Unterklasse von Arbeitspaket mit dem gegebenen Namen
Test = erzeuge_typ("Test", 80, ["umgebung", "modul"])
ergebnis = (isinstance(Test, type), isinstance(Test, type) and issubclass(Test, Arbeitspaket), getattr(Test, "__name__", None))
assert ergebnis == (True, True, "Test"), (
    f"erzeuge_typ('Test', 80, ['umgebung', 'modul']) liefert {Test!r}; erwartet war eine Klasse namens Test, "
    "die von Arbeitspaket erbt.\nTipp: type('Test', (Arbeitspaket,), {…}) – die Oberklassen stehen in einem Tupel."
)

# Klassenattribute
ergebnis = (Test.stundensatz, Test.pflichtangaben)
assert ergebnis == (80, ("umgebung", "modul")), (
    f"Test.stundensatz und Test.pflichtangaben sind {ergebnis!r}, erwartet war (80, ('umgebung', 'modul')).\n"
    "Tipp: Beide gehören in das Dictionary, das type als drittes Argument bekommt; pflichtangaben als tuple(...)."
)

# Objekte der neuen Klasse: Kosten, Darstellung, Pflichtangaben
paket = Test("Lasttest", 12, umgebung="staging", modul="login")
ergebnis = (paket.kosten(), repr(paket))
assert ergebnis == (960, "Test('Lasttest', 12)"), (
    f"Ein Test-Paket 'Lasttest' mit 12 Stunden hat kosten() und repr {ergebnis!r}, erwartet war (960, \"Test('Lasttest', 12)\").\n"
    "Tipp: Eine Methode im Dictionary ist eine gewöhnliche Funktion mit self als erstem Parameter, unter dem Schlüssel '__repr__'."
)
fehler = ausnahme_bei(lambda: Test("Lasttest", 12, modul="login"))
assert isinstance(fehler, ValueError) and "umgebung" in str(fehler), (
    f"Test('Lasttest', 12, modul='login') muss einen ValueError wegen der fehlenden Pflichtangabe umgebung auslösen; "
    f"bekommen: {fehler!r}.\nTipp: Das __init__ von Arbeitspaket prüft self.pflichtangaben; überschreiben Sie es nicht."
)

# Der Name in repr kommt aus der Klasse
Entwicklung = erzeuge_typ("Entwicklung", 95, [])
ergebnis = (repr(Entwicklung("API", 3)), Entwicklung("API", 3).kosten(), Entwicklung.pflichtangaben)
assert ergebnis == ("Entwicklung('API', 3)", 285, ()), (
    f"Für erzeuge_typ('Entwicklung', 95, []) ergeben repr, kosten() und pflichtangaben {ergebnis!r}; "
    "erwartet war (\"Entwicklung('API', 3)\", 285, ())."
)

# Jeder Aufruf erzeugt eine eigene Klasse, Stundensatz 0 ist erlaubt
Test2 = erzeuge_typ("Test", 0, [])
ergebnis = (Test2 is Test, Test2.stundensatz, Test.stundensatz, Test2("x", 5).kosten())
assert ergebnis == (False, 0, 80, 0), (
    f"Ein zweites erzeuge_typ('Test', 0, []) ergibt: dieselbe Klasse {ergebnis[0]}, stundensatz {ergebnis[1]!r}, "
    f"die erste Klasse hat noch {ergebnis[2]!r}, kosten() {ergebnis[3]!r}; erwartet war eine neue Klasse mit 0, "
    "die erste behält 80.\nTipp: Setzen Sie die Attribute in der neuen Klasse, nicht in Arbeitspaket."
)
assert Arbeitspaket.stundensatz == 0 and Arbeitspaket.pflichtangaben == (), (
    f"Arbeitspaket hat jetzt stundensatz {Arbeitspaket.stundensatz!r} und pflichtangaben {Arbeitspaket.pflichtangaben!r}; "
    "die Oberklasse soll unverändert bleiben."
)

# Eine spätere Änderung an der Liste ändert die Klasse nicht
liste = ["raum"]
Verkabelung = erzeuge_typ("Verkabelung", 70, liste)
liste.append("dose")
assert Verkabelung.pflichtangaben == ("raum",) and liste == ["raum", "dose"], (
    f"Nach liste.append('dose') hat Verkabelung.pflichtangaben {Verkabelung.pflichtangaben!r}, erwartet war ('raum',).\n"
    "Tipp: tuple(pflichtangaben) macht eine eigene, unveränderliche Kopie."
)

# Ungültige Namen und negativer Stundensatz
for name, stundensatz, falsch in [("", 10, None), ("Netz Umbau", 10, "Netz Umbau"), ("3D", 10, "3D"), ("Doku", -1, "-1"), ("Doku", -10**6, str(-10**6))]:
    fehler = ausnahme_bei(lambda: erzeuge_typ(name, stundensatz, []))
    assert isinstance(fehler, ValueError) and (falsch is None or falsch in str(fehler)), (
        f"erzeuge_typ({name!r}, {stundensatz}, []) muss einen ValueError auslösen"
        f"{'' if falsch is None else f', dessen Meldung {falsch!r} enthält'}; bekommen: {fehler!r}.\n"
        "Tipp: Prüfen Sie name.isidentifier() und stundensatz < 0, bevor Sie die Klasse bauen."
    )

# erzeuge_typ benutzt type() mit drei Argumenten, keine class-Anweisung
mit_type, mit_class = bauweise(erzeuge_typ)
assert mit_type and not mit_class, (
    "erzeuge_typ soll die Klasse mit type(name, (Arbeitspaket,), {…}) erzeugen, ohne class-Anweisung; "
    f"gefunden: type() mit drei Argumenten {'ja' if mit_type else 'nein'}, class {'ja' if mit_class else 'nein'}."
)

# typen_aus aus dem Beispiel
konfiguration = [
    {"name": "Entwicklung", "stundensatz": 95, "pflicht": ["modul"]},
    {"name": "Test", "stundensatz": 80, "pflicht": ["umgebung", "modul"]},
]
typen = typen_aus(konfiguration)
ergebnis = [(name, klasse.__name__, klasse.stundensatz, klasse.pflichtangaben) for name, klasse in typen.items()]
erwartet = [("Entwicklung", "Entwicklung", 95, ("modul",)), ("Test", "Test", 80, ("umgebung", "modul"))]
assert ergebnis == erwartet, (
    f"typen_aus(konfiguration) aus dem Beispiel liefert (Name, Klassenname, stundensatz, pflichtangaben) {ergebnis}, "
    f"erwartet war {erwartet}.\nTipp: Rufen Sie für jeden Eintrag erzeuge_typ(eintrag['name'], eintrag['stundensatz'], eintrag['pflicht']) auf."
)

# Pakete der Klassen aus typen_aus funktionieren
paket = typen["Test"]("Lasttest", 12, umgebung="staging", modul="login")
assert (paket.kosten(), repr(paket), isinstance(paket, Arbeitspaket)) == (960, "Test('Lasttest', 12)", True), (
    f"Ein Paket der Klasse typen['Test'] hat kosten() {paket.kosten()!r} und repr {paket!r}; erwartet waren 960 und Test('Lasttest', 12)."
)

# Leere Konfiguration und doppelter Name
fehler = ausnahme_bei(lambda: typen_aus([{"name": "Test", "stundensatz": 1, "pflicht": []}, {"name": "Test", "stundensatz": 2, "pflicht": []}]))
ergebnis = typen_aus([])
assert ergebnis == {} and isinstance(fehler, ValueError) and "Test" in str(fehler), (
    f"typen_aus([]) ergibt {ergebnis!r} (erwartet {{}}); eine Konfiguration mit zweimal 'Test' muss einen ValueError "
    f"mit 'Test' in der Meldung auslösen, bekommen: {fehler!r}."
)

# typen_aus meldet ungültige Einträge wie erzeuge_typ
fehler = ausnahme_bei(lambda: typen_aus([{"name": "Gut", "stundensatz": 1, "pflicht": []}, {"name": "Doku", "stundensatz": -5, "pflicht": []}]))
assert isinstance(fehler, ValueError) and "-5" in str(fehler), (
    f"typen_aus mit einem Eintrag mit stundensatz -5 muss den ValueError von erzeuge_typ durchlassen; bekommen: {fehler!r}."
)

# Die Konfiguration bleibt unverändert
assert konfiguration == [
    {"name": "Entwicklung", "stundensatz": 95, "pflicht": ["modul"]},
    {"name": "Test", "stundensatz": 80, "pflicht": ["umgebung", "modul"]},
], f"Nach typen_aus ist die Konfiguration {konfiguration!r}; sie soll unverändert bleiben."


# Vergleichslösung mit einer class-Anweisung in einer Funktion
def typ_von_hand(name, stundensatz, pflichtangaben):
    """Baut die erwartete Klasse mit class und setzt den Namen danach."""

    class Neu(Arbeitspaket):
        pass

    Neu.__name__ = name
    Neu.stundensatz = stundensatz
    Neu.pflichtangaben = tuple(pflichtangaben)
    return Neu


# 300 zufällige Pakettypen und Pakete
zufall = Zufall(5011)
ANGABEN = ["modul", "umgebung", "raum", "kunde", "version"]
for _ in range(300):
    name = zufall.choice(["Test", "Doku", "Abnahme", "Typ_" + str(zufall.randint(0, 99))])
    stundensatz = zufall.randint(0, 200)
    pflicht = zufall.sample(ANGABEN, zufall.randint(0, 3))
    vorlage = typ_von_hand(name, stundensatz, pflicht)
    klasse = erzeuge_typ(name, stundensatz, list(pflicht))
    stunden = zufall.randint(0, 40)
    angaben = {angabe: "x" for angabe in pflicht if zufall.random() < 0.8}
    fehlt = [angabe for angabe in pflicht if angabe not in angaben]
    fehler = ausnahme_bei(lambda: klasse("Paket", stunden, **angaben))
    eigenschaften = (klasse.__name__, klasse.stundensatz, klasse.pflichtangaben, issubclass(klasse, Arbeitspaket))
    erwartet = (vorlage.__name__, vorlage.stundensatz, vorlage.pflichtangaben, True)
    assert eigenschaften == erwartet, (
        f"erzeuge_typ({name!r}, {stundensatz}, {pflicht}) ergibt eine Klasse mit Name, stundensatz, pflichtangaben, "
        f"Unterklasse von Arbeitspaket {eigenschaften}, erwartet war {erwartet}."
    )
    if fehlt:
        assert isinstance(fehler, ValueError) and fehlt[0] in str(fehler), (
            f"{name}('Paket', {stunden}, **{angaben}) muss wegen der fehlenden Angabe {fehlt[0]} einen ValueError auslösen; bekommen: {fehler!r}."
        )
    else:
        paket = klasse("Paket", stunden, **angaben)
        ergebnis = (paket.kosten(), repr(paket))
        assert fehler is None and ergebnis == (stunden * stundensatz, f"{name}('Paket', {stunden})"), (
            f"Ein Paket {name}('Paket', {stunden}, **{angaben}) mit stundensatz {stundensatz} hat kosten() und repr {ergebnis!r}, "
            f"erwartet war ({stunden * stundensatz}, \"{name}('Paket', {stunden})\")."
        )

# An der oberen Grenze: 1000 Pakettypen mit je 20 Pflichtangaben
konfiguration = [
    {"name": f"Typ{nummer}", "stundensatz": nummer * 1000, "pflicht": [f"angabe{k}" for k in range(20)]}
    for nummer in range(1000)
]
typen = typen_aus(konfiguration)
letzter = typen.get("Typ999")
assert len(typen) == 1000 and list(typen)[:2] == ["Typ0", "Typ1"] and letzter is not None and letzter.stundensatz == 999000 and len(letzter.pflichtangaben) == 20, (
    f"typen_aus mit 1000 Einträgen liefert {len(typen)} Klassen, die ersten Namen {list(typen)[:2]}; "
    f"erwartet waren 1000, von Typ0 bis Typ999, Typ999 mit stundensatz 999000 und 20 Pflichtangaben."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "960 Test('Lasttest', 12)\nTest ('umgebung', 'modul') True"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
