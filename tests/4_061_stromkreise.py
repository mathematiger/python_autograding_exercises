# Automatisch erzeugt aus lehrkraft/muster/4_061_stromkreise.py - nicht von Hand ändern.
# vorlage-hash: e4bf80db62c91bb7
# text-hash: b809e005c9e8ef0f
# thema: datenstrukturen
# inhalt: namedtuple und NamedTuple

def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_auslastung(watt_liste, ampere, spannung):
    """Vergleichslösung: die ungerundete Auslastung in Prozent."""
    return sum(watt_liste) * 100 / (ampere * spannung)


def passt_gerundet(ergebnis, genau):
    """True, wenn ergebnis eine auf eine Stelle gerundete Zahl ist, die höchstens 0.05 von genau abweicht."""
    if not isinstance(ergebnis, (int, float)) or isinstance(ergebnis, bool):
        return False
    return abs(ergebnis * 10 - round(ergebnis * 10)) < 1e-6 and abs(ergebnis - genau) <= 0.05 + 1e-9


# Verbraucher hat die Felder name und watt
db = wert_von(lambda: Verbraucher("db-01", 450))
assert wert_von(lambda: (db.name, db.watt)) == ("db-01", 450), (
    f"Verbraucher(\"db-01\", 450) ergibt {db!r}, erwartet war Verbraucher(name='db-01', watt=450).\n"
    'Tipp: Verbraucher = namedtuple("Verbraucher", ["name", "watt"]).'
)

# Verbraucher ist ein Tupel: Stelle, Auspacken, Gleichheit mit einem gewöhnlichen Tupel
assert isinstance(db, tuple) and db[1] == 450 and db == ("db-01", 450), (
    f"Verbraucher(\"db-01\", 450) ergibt {db!r}; erwartet war ein Tupel, das gleich (\"db-01\", 450) ist."
)

# Verbraucher hat genau diese Felder in dieser Reihenfolge, auch mit Schlüsselwörtern
assert wert_von(lambda: Verbraucher._fields) == ("name", "watt") and wert_von(lambda: Verbraucher(watt=90, name="sw")) == ("sw", 90), (
    f"Verbraucher._fields ist {wert_von(lambda: Verbraucher._fields)!r}, erwartet war ('name', 'watt')."
)

# Verbraucher ist unveränderlich
try:
    db.watt = 999
    fehlerart = "keine Ausnahme"
except Exception as fehler:
    fehlerart = type(fehler).__name__
assert fehlerart == "AttributeError", (
    f"db.watt = 999 ergibt {fehlerart}, erwartet war AttributeError: ein benanntes Tupel ist unveränderlich."
)

# Stromkreis mit Standardspannung 230
kreis = wert_von(lambda: Stromkreis("A1", 16))
assert wert_von(lambda: (kreis.name, kreis.ampere, kreis.spannung)) == ("A1", 16, 230), (
    f"Stromkreis(\"A1\", 16) ergibt {kreis!r}, erwartet war Stromkreis(name='A1', ampere=16, spannung=230).\n"
    "Tipp: Schreiben Sie in den Klassenkörper name: str, ampere: int und spannung: int = 230."
)

# Stromkreis ist ein Tupel mit genau diesen Feldern
assert isinstance(kreis, tuple) and Stromkreis._fields == ("name", "ampere", "spannung") and kreis == ("A1", 16, 230), (
    f"Stromkreis._fields ist {Stromkreis._fields!r}, erwartet war ('name', 'ampere', 'spannung')."
)

# Stromkreis mit anderer Spannung als Schlüsselwort
anderer = wert_von(lambda: Stromkreis("B2", ampere=32, spannung=400))
assert anderer == ("B2", 32, 400), f"Stromkreis(\"B2\", ampere=32, spannung=400) ergibt {anderer!r}, erwartet war ('B2', 32, 400)."

# max_watt im Beispiel
ergebnis = wert_von(lambda: kreis.max_watt())
assert ergebnis == 3680, (
    f"Stromkreis(\"A1\", 16).max_watt() ergibt {ergebnis!r}, erwartet war 3680.\n"
    "Tipp: Eine Methode in der Klasse mit self: return self.spannung * self.ampere."
)

# max_watt mit anderen Werten (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: Stromkreis("B2", 32, 400).max_watt())
assert ergebnis == 12800, f"Stromkreis(\"B2\", 32, 400).max_watt() ergibt {ergebnis!r}, erwartet war 12800."

# lies_verbraucher im Beispiel
ergebnis = wert_von(lambda: lies_verbraucher(["db-01;450", "web-01;320", "switch-01;90"]))
assert ergebnis == [("db-01", 450), ("web-01", 320), ("switch-01", 90)], (
    f"lies_verbraucher([\"db-01;450\", \"web-01;320\", \"switch-01;90\"]) ergibt {ergebnis!r},\n"
    "erwartet war [Verbraucher(name='db-01', watt=450), Verbraucher(name='web-01', watt=320), Verbraucher(name='switch-01', watt=90)].\n"
    'Tipp: name, watt = zeile.split(";") und dann Verbraucher(name, int(watt)).'
)

# lies_verbraucher liefert Verbraucher-Tupel, keine gewöhnlichen
assert all(isinstance(eintrag, Verbraucher) for eintrag in ergebnis), (
    f"lies_verbraucher liefert {[type(eintrag).__name__ for eintrag in ergebnis]}, erwartet waren Verbraucher-Tupel.\n"
    "Tipp: Bauen Sie jeden Eintrag mit Verbraucher(...)."
)

# lies_verbraucher: keine Zeilen
ergebnis = wert_von(lambda: lies_verbraucher([]))
assert ergebnis == [], f"lies_verbraucher([]) ergibt {ergebnis!r}, erwartet war []."

# auslastung im Beispiel
server = [Verbraucher("db-01", 450), Verbraucher("web-01", 320), Verbraucher("switch-01", 90)]
ergebnis = wert_von(lambda: auslastung(Stromkreis("A1", 16), server))
assert ergebnis == 23.4, (
    f"auslastung(Stromkreis(\"A1\", 16), server) ergibt {ergebnis!r}, erwartet war 23.4 (860 von 3680 Watt).\n"
    "Tipp: Summe der watt geteilt durch kreis.max_watt(), mal 100, mit round(..., 1)."
)

# auslastung mit anderem Stromkreis und anderen Geräten (nicht fest hinschreiben!)
geraete = [Verbraucher("gpu-01", 2400), Verbraucher("gpu-02", 2400), Verbraucher("san-01", 1300)]
ergebnis = wert_von(lambda: auslastung(Stromkreis("C3", 32, 400), geraete))
assert passt_gerundet(ergebnis, vergleich_auslastung([2400, 2400, 1300], 32, 400)), (
    f"auslastung(Stromkreis(\"C3\", 32, 400), {geraete}) ergibt {ergebnis!r}, erwartet war 47.7."
)

# auslastung: überlastet, über 100 Prozent
ergebnis = wert_von(lambda: auslastung(Stromkreis("D4", 10), [Verbraucher("usv-01", 2500), Verbraucher("klima", 900)]))
assert passt_gerundet(ergebnis, vergleich_auslastung([2500, 900], 10, 230)), (
    f"auslastung bei 3400 Watt an 10 A ergibt {ergebnis!r}, erwartet war 147.8."
)

# auslastung: ganz ohne Geräte
ergebnis = wert_von(lambda: auslastung(Stromkreis("D4", 10), []))
assert ergebnis == 0, f"auslastung ohne Geräte ergibt {ergebnis!r}, erwartet war 0."

# aufgeruestet im Beispiel
kreis = Stromkreis("A1", 16)
ergebnis = wert_von(lambda: aufgeruestet(kreis, 32))
assert ergebnis == ("A1", 32, 230) and isinstance(ergebnis, Stromkreis), (
    f"aufgeruestet(Stromkreis(\"A1\", 16), 32) ergibt {ergebnis!r}, erwartet war Stromkreis(name='A1', ampere=32, spannung=230).\n"
    "Tipp: kreis._replace(ampere=ampere) baut ein neues Tupel mit einem anderen Wert."
)

# aufgeruestet behält die Spannung und lässt den alten Stromkreis unverändert
kreis = Stromkreis("B2", 16, 400)
ergebnis = wert_von(lambda: aufgeruestet(kreis, 25))
assert ergebnis == ("B2", 25, 400) and kreis == ("B2", 16, 400), (
    f"aufgeruestet(Stromkreis(\"B2\", 16, 400), 25) ergibt {ergebnis!r} und der alte ist {kreis!r}; "
    "erwartet waren Stromkreis('B2', 25, 400) und der unveränderte alte."
)

# Viele zufällige Geräteliste und Stromkreise
zufall = Zufall(4061)
for _ in range(200):
    watt_liste = [zufall.randint(1, 5000) for _ in range(zufall.randint(0, 10))]
    zeilen = [f"geraet-{nummer};{watt}" for nummer, watt in enumerate(watt_liste)]
    ampere = zufall.randint(1, 63)
    spannung = zufall.choice([100, 110, 230, 400])
    geraete = wert_von(lambda: lies_verbraucher(zeilen))
    assert geraete == [(f"geraet-{nummer}", watt) for nummer, watt in enumerate(watt_liste)], (
        f"lies_verbraucher({zeilen}) ergibt {geraete!r}."
    )
    ergebnis = wert_von(lambda: auslastung(Stromkreis("Z", ampere, spannung), geraete))
    genau = vergleich_auslastung(watt_liste, ampere, spannung)
    assert passt_gerundet(ergebnis, genau), (
        f"auslastung(Stromkreis('Z', {ampere}, {spannung}), {geraete}) ergibt {ergebnis!r}, erwartet war {round(genau, 1)}."
    )

# Obere Grenze: 10 000 Zeilen
zeilen = [f"knoten-{nummer};{nummer % 5000 + 1}" for nummer in range(10000)]
geraete = wert_von(lambda: lies_verbraucher(zeilen))
ergebnis = wert_von(lambda: auslastung(Stromkreis("gross", 63, 400), geraete))
genau = vergleich_auslastung([nummer % 5000 + 1 for nummer in range(10000)], 63, 400)
assert isinstance(geraete, list) and len(geraete) == 10000 and passt_gerundet(ergebnis, genau), (
    f"Bei 10 000 Geräten ergibt auslastung {ergebnis!r}, erwartet war {round(genau, 1)}."
)
