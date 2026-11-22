# Automatisch erzeugt aus lehrkraft/muster/5_036_altgeraete.py - nicht von Hand ändern.
# vorlage-hash: f3577c38b94bccf9
# text-hash: d01dab5c00785750
# thema: klassen
# inhalt: Hash-Vertrag, frozen dataclass

import dataclasses


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ausnahme_von(aufruf):
    """Führt den Aufruf aus und gibt den Namen der ausgelösten Ausnahme zurück, sonst "keine Ausnahme"."""
    try:
        aufruf()
    except Exception as fehler:
        return type(fehler).__name__
    return "keine Ausnahme"


def setze(objekt, name, wert):
    """Weist objekt.name = wert zu (für ausnahme_von)."""
    setattr(objekt, name, wert)


def meldungen_aus(tripel):
    """Baut aus (hersteller, seriennummer, zustand)-Tripeln eine Liste von Altgeräten."""
    return [Altgeraet(hersteller, nummer, zustand) for hersteller, nummer, zustand in tripel]


def vergleich_zustand(tripel):
    """Vergleichslösung: Paare (hersteller, seriennummer) → letzter Zustand, ohne die Klassen der SuS."""
    ergebnis = {}
    for hersteller, nummer, zustand in tripel:
        ergebnis[(hersteller, nummer)] = zustand
    return ergebnis


def als_paare(zustaende):
    """Macht aus einem Dictionary Geraetekennung → Zustand eine Liste von ((hersteller, seriennummer), zustand)."""
    if not isinstance(zustaende, dict):
        return zustaende
    return [((kennung.hersteller, kennung.seriennummer), zustand) for kennung, zustand in zustaende.items()]


def erste_zustaende(tripel):
    """Vergleichslösung: je Gerät der Zustand der ersten Meldung."""
    ergebnis = {}
    for hersteller, nummer, zustand in tripel:
        ergebnis.setdefault((hersteller, nummer), zustand)
    return ergebnis


def bestand_als_dict(menge):
    """Macht aus einer Menge von Altgeräten ein Dictionary (hersteller, seriennummer) → zustand."""
    if not isinstance(menge, (set, frozenset)):
        return menge
    return {(geraet.kennung.hersteller, geraet.kennung.seriennummer): geraet.zustand for geraet in menge}


# Geraetekennung: zwei Kennungen mit denselben Werten sind gleich und haben denselben Hashwert
k1 = wert_von(lambda: Geraetekennung("Lenovo", "PF-1234"))
k2 = wert_von(lambda: Geraetekennung(hersteller="Lenovo", seriennummer="PF-1234"))
assert wert_von(lambda: k1 == k2 and hash(k1) == hash(k2)) is True, (
    f"Geraetekennung(\"Lenovo\", \"PF-1234\") ergibt {k1!r}; zwei solche Kennungen sollten gleich und hashbar sein.\n"
    "Tipp: @dataclass(frozen=True) über der Klasse und die Felder hersteller: str und seriennummer: str."
)

# Geraetekennung ist eine Datenklasse mit frozen=True: Zuweisung löst FrozenInstanceError aus
assert dataclasses.is_dataclass(Geraetekennung) and ausnahme_von(lambda: setze(k1, "seriennummer", "X")) == "FrozenInstanceError", (
    f"k.seriennummer = \"X\" ergibt {ausnahme_von(lambda: setze(k1, 'seriennummer', 'X'))}, erwartet war FrozenInstanceError.\n"
    "Tipp: frozen=True verbietet Zuweisungen nach dem Erzeugen."
)

# Geraetekennung: verschiedene Seriennummer oder anderer Hersteller sind ungleich
assert wert_von(lambda: Geraetekennung("Lenovo", "PF-1234") != Geraetekennung("Lenovo", "PF-9999")) is True and wert_von(
    lambda: Geraetekennung("HP", "PF-1234") != Geraetekennung("Lenovo", "PF-1234")
) is True, "Kennungen mit anderer Seriennummer oder anderem Hersteller sollten ungleich sein."

# Altgeraet: kennung liefert die Geraetekennung, zustand das Attribut
a = wert_von(lambda: Altgeraet("Lenovo", "PF-1234", "ungeprüft"))
assert wert_von(lambda: (a.kennung, a.zustand)) == (Geraetekennung("Lenovo", "PF-1234"), "ungeprüft"), (
    f"Für a = Altgeraet(\"Lenovo\", \"PF-1234\", \"ungeprüft\") ergibt (a.kennung, a.zustand) "
    f"{wert_von(lambda: (a.kennung, a.zustand))!r},\nerwartet war (Geraetekennung(hersteller='Lenovo', seriennummer='PF-1234'), 'ungeprüft')."
)

# Altgeraet: gleiche Kennung heißt gleich, auch bei anderem Zustand
c = wert_von(lambda: Altgeraet("Lenovo", "PF-1234", "Display defekt"))
assert wert_von(lambda: a == c) is True, (
    f"Altgeraet(\"Lenovo\", \"PF-1234\", \"ungeprüft\") == Altgeraet(\"Lenovo\", \"PF-1234\", \"Display defekt\") ergibt "
    f"{wert_von(lambda: a == c)!r}, erwartet war True.\nTipp: Vergleichen Sie in __eq__ nur die Kennungen."
)

# Altgeraet: andere Kennung heißt ungleich, auch bei gleichem Zustand
b = wert_von(lambda: Altgeraet("Dell", "CN-0815", "ungeprüft"))
assert wert_von(lambda: a != b) is True and wert_von(lambda: a == Altgeraet("Lenovo", "PF-1235", "ungeprüft")) is False, (
    "Altgeräte mit verschiedener Kennung sollten ungleich sein, auch wenn der Zustand gleich ist."
)

# Altgeraet: gleiche Altgeräte haben denselben Hashwert (der Vertrag)
assert wert_von(lambda: hash(a) == hash(c)) is True, (
    f"hash(a) == hash(c) ergibt {wert_von(lambda: hash(a) == hash(c))!r} für zwei gleiche Altgeräte, erwartet war True.\n"
    "Tipp: Eine Klasse mit __eq__ ohne __hash__ ist unhashbar; berechnen Sie den Hash nur aus der Kennung."
)

# Altgeraet: der Hashwert bleibt gleich, wenn sich der Zustand ändert
d = Altgeraet("Fujitsu", "FJ-77", "ungeprüft")
vorher = wert_von(lambda: hash(d))
d.zustand = "gut"
assert isinstance(vorher, int) and wert_von(lambda: hash(d)) == vorher, (
    f"hash(d) ist vor dem Ändern des Zustands {vorher!r} und danach {wert_von(lambda: hash(d))!r}; er darf sich nicht ändern.\n"
    "Tipp: Nehmen Sie den Zustand nicht in den Hash auf."
)

# Altgeraet: ein Gerät bleibt in der Menge auffindbar, wenn sich der Zustand ändert
e = Altgeraet("Lenovo", "PF-5555", "ungeprüft")
lager = wert_von(lambda: {e})
e.zustand = "Akku schwach"
assert wert_von(lambda: e in lager and Altgeraet("Lenovo", "PF-5555", "egal") in lager) is True, (
    "Nach e.zustand = \"Akku schwach\" ist e nicht mehr in der Menge {e} zu finden, oder ein gleiches Altgerät nicht.\n"
    "Tipp: Gleichheit und Hash dürfen nur von der Kennung abhängen."
)

# Altgeraet: der Zustand lässt sich ändern
e.zustand = "verkauft"
assert e.zustand == "verkauft", f"Nach e.zustand = \"verkauft\" ist e.zustand {e.zustand!r}."

# Altgeraet: die Kennung lässt sich nicht neu setzen
fehlerart = ausnahme_von(lambda: setze(e, "kennung", Geraetekennung("HP", "1")))
assert fehlerart == "AttributeError" and wert_von(lambda: e.kennung) == Geraetekennung("Lenovo", "PF-5555"), (
    f"e.kennung = Geraetekennung(\"HP\", \"1\") ergibt {fehlerart}, erwartet war AttributeError, und die Kennung sollte bleiben.\n"
    "Tipp: Speichern Sie die Kennung in self._kennung und liefern Sie sie über eine property ohne Setter."
)

# Altgeraet: der Vergleich mit etwas anderem gibt NotImplemented zurück
ergebnis = wert_von(lambda: a.__eq__("Lenovo PF-1234"))
assert ergebnis is NotImplemented, (
    f"a.__eq__(\"Lenovo PF-1234\") ergibt {ergebnis!r}, erwartet war NotImplemented.\n"
    "Tipp: if not isinstance(other, Altgeraet): return NotImplemented"
)

# Altgeraet: dadurch ist der Vergleich mit einem Text einfach False, auch mit einer Kennung
assert wert_von(lambda: a == "Lenovo PF-1234") is False and wert_von(lambda: a == Geraetekennung("Lenovo", "PF-1234")) is False, (
    f"a == \"Lenovo PF-1234\" ergibt {wert_von(lambda: a == 'Lenovo PF-1234')!r}, "
    f"a == Geraetekennung(...) {wert_von(lambda: a == Geraetekennung('Lenovo', 'PF-1234'))!r}; erwartet war beide Male False."
)

# bestand im Beispiel: zwei Geräte
meldungen = meldungen_aus([("Lenovo", "PF-1234", "ungeprüft"), ("Dell", "CN-0815", "Akku schwach"), ("Lenovo", "PF-1234", "Display defekt")])
ergebnis = wert_von(lambda: bestand(meldungen))
assert isinstance(ergebnis, (set, frozenset)) and len(ergebnis) == 2, (
    f"bestand([a, b, c]) ergibt {ergebnis!r}, erwartet war eine Menge mit 2 Altgeräten.\nTipp: set(meldungen) benutzt __hash__ und __eq__."
)

# bestand im Beispiel: es bleibt jeweils die erste Meldung
erwartet = {("Lenovo", "PF-1234"): "ungeprüft", ("Dell", "CN-0815"): "Akku schwach"}
assert bestand_als_dict(ergebnis) == erwartet, (
    f"bestand([a, b, c]) ergibt {ergebnis!r}; erwartet waren die Meldungen mit den Zuständen {erwartet!r}.\n"
    "Tipp: Eine Menge behält beim Einfügen eines gleichen Elements das alte."
)

# bestand mit anderen Meldungen (nicht fest hinschreiben!)
tripel = [("HP", "5CG-1", "gut"), ("HP", "5CG-2", "gut"), ("HP", "5CG-1", "defekt"), ("Apple", "C02-9", "gut"), ("HP", "5CG-2", "gut")]
ergebnis = wert_von(lambda: bestand(meldungen_aus(tripel)))
assert bestand_als_dict(ergebnis) == erste_zustaende(tripel), (
    f"bestand für {tripel} ergibt {ergebnis!r}, erwartet waren die Geräte {erste_zustaende(tripel)!r}."
)

# bestand: dieselbe Seriennummer bei verschiedenen Herstellern sind zwei Geräte
tripel = [("Dell", "123", "gut"), ("Acer", "123", "gut")]
ergebnis = wert_von(lambda: bestand(meldungen_aus(tripel)))
assert bestand_als_dict(ergebnis) == erste_zustaende(tripel), (
    f"bestand für {tripel} ergibt {ergebnis!r}; erwartet waren zwei Geräte."
)

# bestand: keine Meldungen
ergebnis = wert_von(lambda: bestand([]))
assert isinstance(ergebnis, (set, frozenset)) and len(ergebnis) == 0, f"bestand([]) ergibt {ergebnis!r}, erwartet war eine leere Menge."

# aktueller_zustand im Beispiel
meldungen = meldungen_aus([("Lenovo", "PF-1234", "ungeprüft"), ("Dell", "CN-0815", "Akku schwach"), ("Lenovo", "PF-1234", "Display defekt")])
ergebnis = wert_von(lambda: aktueller_zustand(meldungen))
erwartet = {Geraetekennung("Lenovo", "PF-1234"): "Display defekt", Geraetekennung("Dell", "CN-0815"): "Akku schwach"}
assert ergebnis == erwartet, (
    f"aktueller_zustand([a, b, c]) ergibt {ergebnis!r},\nerwartet war {erwartet!r}.\n"
    "Tipp: zustaende[geraet.kennung] = geraet.zustand überschreibt mit jeder späteren Meldung."
)

# aktueller_zustand: Reihenfolge der ersten Meldung
assert isinstance(ergebnis, dict) and [paar[0] for paar in als_paare(ergebnis)] == [("Lenovo", "PF-1234"), ("Dell", "CN-0815")], (
    f"aktueller_zustand([a, b, c]) hat die Schlüssel in der Reihenfolge {list(ergebnis)!r}; zuerst sollte Lenovo stehen."
)

# aktueller_zustand mit anderen Meldungen (nicht fest hinschreiben!)
tripel = [("HP", "5CG-1", "ungeprüft"), ("Apple", "C02-9", "ungeprüft"), ("HP", "5CG-1", "gut"), ("HP", "5CG-1", "verkauft")]
ergebnis = wert_von(lambda: aktueller_zustand(meldungen_aus(tripel)))
assert als_paare(ergebnis) == list(vergleich_zustand(tripel).items()), (
    f"aktueller_zustand für {tripel} ergibt {ergebnis!r},\nerwartet waren die Paare {list(vergleich_zustand(tripel).items())!r}."
)

# aktueller_zustand: die Schlüssel sind Geraetekennungen
assert isinstance(ergebnis, dict) and all(isinstance(kennung, Geraetekennung) for kennung in ergebnis), (
    f"Die Schlüssel von aktueller_zustand sind {[type(kennung).__name__ for kennung in ergebnis]!r}, erwartet waren Geraetekennung."
)

# aktueller_zustand: keine Meldungen
ergebnis = wert_von(lambda: aktueller_zustand([]))
assert ergebnis == {}, f"aktueller_zustand([]) ergibt {ergebnis!r}, erwartet war {{}}."

# Viele zufällige Meldungen
zufall = Zufall(5036)
hersteller = ["Lenovo", "Dell", "HP", "Apple"]
zustaende = ["ungeprüft", "gut", "Akku schwach", "Display defekt", "verkauft"]
for _ in range(200):
    tripel = [(zufall.choice(hersteller), f"SN-{zufall.randint(1, 6)}", zufall.choice(zustaende)) for _ in range(zufall.randint(0, 12))]
    ergebnis = wert_von(lambda: bestand(meldungen_aus(tripel)))
    assert bestand_als_dict(ergebnis) == erste_zustaende(tripel), f"bestand für {tripel} ergibt {ergebnis!r}."
    ergebnis = wert_von(lambda: aktueller_zustand(meldungen_aus(tripel)))
    assert als_paare(ergebnis) == list(vergleich_zustand(tripel).items()), f"aktueller_zustand für {tripel} ergibt {ergebnis!r}."

# Laufzeit: bestand braucht O(n) Schritte (viermal so viele Meldungen, höchstens etwa viermal so viele Schritte)
klein = meldungen_aus([("Dell", f"SN-{nummer % 140}", "gut") for nummer in range(200)])
gross = meldungen_aus([("Dell", f"SN-{nummer % 560}", "gut") for nummer in range(800)])
_, schritte_klein = zaehle_schritte(bestand, klein)
_, schritte_gross = zaehle_schritte(bestand, gross)
assert schritte_gross <= 6 * max(schritte_klein, 1) + 50, (
    f"bestand braucht für 200 Meldungen {schritte_klein} Schritte, für 800 aber {schritte_gross}; bei O(n) wären es etwa viermal so viele.\n"
    "Tipp: Eine Menge findet ein gleiches Element über den Hash, ohne alle anderen zu vergleichen; vergleichen Sie nicht jede Meldung mit jeder."
)

# Laufzeit: aktueller_zustand braucht O(n) Schritte
_, schritte_klein = zaehle_schritte(aktueller_zustand, klein)
_, schritte_gross = zaehle_schritte(aktueller_zustand, gross)
assert schritte_gross <= 6 * max(schritte_klein, 1) + 50, (
    f"aktueller_zustand braucht für 200 Meldungen {schritte_klein} Schritte, für 800 aber {schritte_gross}; bei O(n) wären es etwa viermal so viele."
)

# Obere Grenze: 100 000 Meldungen
tripel = [(zufall.choice(hersteller), f"SN-{zufall.randint(1, 30000)}", zufall.choice(zustaende)) for _ in range(100000)]
meldungen = meldungen_aus(tripel)
ergebnis = wert_von(lambda: bestand(meldungen))
assert bestand_als_dict(ergebnis) == erste_zustaende(tripel), "Bei 100 000 Meldungen stimmt bestand nicht."
# Obere Grenze: aktueller_zustand bei 100 000 Meldungen
ergebnis = wert_von(lambda: aktueller_zustand(meldungen))
assert als_paare(ergebnis) == list(vergleich_zustand(tripel).items()), "Bei 100 000 Meldungen stimmt aktueller_zustand nicht."
