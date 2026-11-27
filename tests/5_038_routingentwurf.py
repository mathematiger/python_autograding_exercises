# Automatisch erzeugt aus lehrkraft/muster/5_038_routingentwurf.py - nicht von Hand ändern.
# vorlage-hash: ba7a4879fe98d71c
# text-hash: c1ffb00f40c54f27
# thema: datenstrukturen
# inhalt: __copy__ und __deepcopy__

import copy

ROUTEN = {"10.20.0.0/16": ["192.168.0.2", "192.168.0.3"], "0.0.0.0/0": ["192.168.0.1"]}


def beispiel():
    """Die Tabelle aus dem Aufgabentext, mit zwei Einträgen im Protokoll."""
    tabelle = Routingtabelle(Router("kern-01"))
    tabelle.setze("10.20.0.0/16", ["192.168.0.2", "192.168.0.3"])
    tabelle.setze("0.0.0.0/0", ["192.168.0.1"])
    return tabelle


def kopie_von(funktion, objekt):
    """Ruft copy.copy oder copy.deepcopy auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(objekt)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def ist_tabelle(kopie, wie):
    """Liefert (ist eine Routingtabelle, Meldung), damit spätere Tests eine klare Meldung haben."""
    if isinstance(kopie, Routingtabelle):
        return True, ""
    return False, f"{wie}(tabelle) ergibt {kopie!r}, erwartet war eine neue Routingtabelle."


def zustand(tabelle):
    """Router-Name, Routen und Protokoll als Tupel zum Vergleichen."""
    return tabelle.router.name, tabelle.routen, tabelle.aenderungen


# copy.copy gibt eine neue Routingtabelle zurück
tabelle = beispiel()
flach = kopie_von(copy.copy, tabelle)
ok, text = ist_tabelle(flach, "copy.copy")
assert ok and flach is not tabelle, text or "copy.copy(tabelle) gibt die Tabelle selbst zurück, erwartet war eine neue."

# copy.copy: dieselben Routen
assert flach.routen == ROUTEN, f"copy.copy(tabelle).routen ist {flach.routen!r}, erwartet war {ROUTEN}."

# copy.copy: ein eigenes Dictionary routen
assert flach.routen is not tabelle.routen, (
    "copy.copy(tabelle).routen ist dasselbe Dictionary wie tabelle.routen.\n"
    "Tipp: dict(self.routen) oder self.routen.copy() legt ein neues Dictionary mit denselben Listen an."
)

# copy.copy: dieselben Listen der Next Hops
assert all(flach.routen[ziel] is tabelle.routen[ziel] for ziel in ROUTEN), (
    "In copy.copy(tabelle) sind die Listen der Next Hops Kopien; erwartet war eine flache Kopie mit denselben Listen."
)

# copy.copy: derselbe Router
assert flach.router is tabelle.router, "copy.copy(tabelle).router ist ein anderes Objekt; erwartet war derselbe Router."

# copy.copy: ein leeres, eigenes Protokoll
assert flach.aenderungen == [] and flach.aenderungen is not tabelle.aenderungen, (
    f"copy.copy(tabelle).aenderungen ist {flach.aenderungen!r}, erwartet war eine neue leere Liste.\n"
    "Tipp: Ohne __copy__ teilt copy.copy auch das Protokoll."
)

# copy.copy: das Original bleibt unverändert, auch wenn der Entwurf Zielnetze ändert
flach.setze("172.16.0.0/12", ["192.168.0.7"])
del flach.routen["0.0.0.0/0"]
assert zustand(tabelle) == ("kern-01", ROUTEN, ["setze 10.20.0.0/16", "setze 0.0.0.0/0"]), (
    f"Nach Änderungen am flachen Entwurf ist das Original {zustand(tabelle)!r}; es sollte unverändert sein."
)

# copy.deepcopy gibt eine neue Routingtabelle zurück
tabelle = beispiel()
tief = kopie_von(copy.deepcopy, tabelle)
ok, text = ist_tabelle(tief, "copy.deepcopy")
assert ok and tief is not tabelle, (text or "copy.deepcopy(tabelle) gibt die Tabelle selbst zurück.") + (
    "\nTipp: Ohne __deepcopy__ versucht copy.deepcopy auch den Router mit seiner Sperre zu kopieren."
)

# copy.deepcopy: dieselben Routen
assert tief.routen == ROUTEN, f"copy.deepcopy(tabelle).routen ist {tief.routen!r}, erwartet war {ROUTEN}."

# copy.deepcopy: eigene Listen der Next Hops
assert tief.routen is not tabelle.routen and all(tief.routen[ziel] is not tabelle.routen[ziel] for ziel in ROUTEN), (
    "In copy.deepcopy(tabelle) sind routen oder die Listen darin dieselben Objekte wie im Original.\n"
    "Tipp: neu.routen = copy.deepcopy(self.routen, memo)."
)

# copy.deepcopy: derselbe Router
assert tief.router is tabelle.router, (
    "copy.deepcopy(tabelle).router ist ein anderes Objekt; erwartet war derselbe Router, denn das Gerät gibt es nur einmal."
)

# copy.deepcopy: ein leeres, eigenes Protokoll
assert tief.aenderungen == [] and tief.aenderungen is not tabelle.aenderungen, (
    f"copy.deepcopy(tabelle).aenderungen ist {tief.aenderungen!r}, erwartet war eine neue leere Liste."
)

# copy.deepcopy: Änderungen am Entwurf lassen das Original in Ruhe
tief.ergaenze("0.0.0.0/0", "192.168.0.9")
tief.setze("10.20.0.0/16", [])
assert zustand(tabelle) == ("kern-01", ROUTEN, ["setze 10.20.0.0/16", "setze 0.0.0.0/0"]), (
    f"Nach Änderungen am tiefen Entwurf ist das Original {zustand(tabelle)!r}; es sollte unverändert sein."
)

# copy.deepcopy reicht memo weiter: eine Liste, die außerhalb auch vorkommt, gibt es in der Kopie einmal
tabelle = beispiel()
gemeinsam = tabelle.routen["0.0.0.0/0"]
paar = kopie_von(copy.deepcopy, [tabelle, gemeinsam])
assert isinstance(paar, list) and isinstance(paar[0], Routingtabelle) and paar[0].routen["0.0.0.0/0"] is paar[1], (
    "copy.deepcopy([tabelle, liste]), wobei liste in tabelle.routen steckt: In der Kopie sind es zwei verschiedene Listen.\n"
    "Tipp: Geben Sie memo an copy.deepcopy(self.routen, memo) weiter, statt ein neues memo anzufangen."
)

# copy.deepcopy: dieselbe Tabelle zweimal im Ganzen wird einmal kopiert
tabelle = beispiel()
paar = kopie_von(copy.deepcopy, [tabelle, tabelle])
assert isinstance(paar, list) and paar[0] is paar[1] and paar[0] is not tabelle, (
    f"copy.deepcopy([tabelle, tabelle]) ergibt {paar!r}; erwartet waren zweimal dieselbe neue Tabelle."
)

# copy.deepcopy: zwei Zielnetze mit derselben Liste behalten das auch in der Kopie
tabelle = beispiel()
tabelle.routen["10.30.0.0/16"] = tabelle.routen["10.20.0.0/16"]
tief = kopie_von(copy.deepcopy, tabelle)
assert isinstance(tief, Routingtabelle) and tief.routen["10.30.0.0/16"] is tief.routen["10.20.0.0/16"], (
    "Zeigen zwei Zielnetze auf dieselbe Liste, sollte das auch in der tiefen Kopie so sein.\n"
    "Tipp: copy.deepcopy auf das ganze Dictionary erledigt das über memo."
)

# Randfall: eine leere Tabelle
leer = Routingtabelle(Router("rand-01"))
ergebnis = [kopie_von(copy.copy, leer), kopie_von(copy.deepcopy, leer)]
assert all(isinstance(k, Routingtabelle) and zustand(k) == ("rand-01", {}, []) for k in ergebnis), (
    f"Kopien einer leeren Tabelle ergeben {ergebnis!r}, erwartet waren zwei leere Routingtabellen für rand-01."
)

# Randfall: ein Zielnetz ohne Next Hop
tabelle = Routingtabelle(Router("rand-02"))
tabelle.setze("10.0.0.0/8", [])
tief = kopie_von(copy.deepcopy, tabelle)
assert isinstance(tief, Routingtabelle) and tief.routen == {"10.0.0.0/8": []} and tief.routen["10.0.0.0/8"] is not tabelle.routen["10.0.0.0/8"], (
    f"Die tiefe Kopie einer Tabelle mit leerer Liste ergibt {getattr(tief, 'routen', tief)!r}."
)

# Die Ausgabe des Programms
erwartet = "False True []\n['192.168.0.1'] True ['ergaenze 0.0.0.0/0']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Tabellen
zufall = Zufall(5038)
for _ in range(200):
    tabelle = Routingtabelle(Router(f"r{zufall.randint(1, 9)}"))
    for _ in range(zufall.randint(0, 6)):
        ziel = f"10.{zufall.randint(0, 9)}.0.0/16"
        tabelle.setze(ziel, [f"192.168.0.{zufall.randint(1, 254)}" for _ in range(zufall.randint(0, 8))])
    vorher = copy.deepcopy(tabelle.routen)
    # erst die tiefe Kopie, denn Änderungen an den Listen der flachen erreichen auch das Original
    for funktion in [copy.deepcopy, copy.copy]:
        kopie = kopie_von(funktion, tabelle)
        assert isinstance(kopie, Routingtabelle) and kopie.routen == vorher and kopie.router is tabelle.router, (
            f"{funktion.__name__}(tabelle) mit routen {vorher} ergibt {getattr(kopie, 'routen', kopie)!r}."
        )
        assert kopie.aenderungen == [], (
            f"{funktion.__name__}(tabelle) hat das Protokoll {kopie.aenderungen!r}, erwartet war []."
        )
        for liste in kopie.routen.values():
            liste.append("x")
    assert tabelle.routen == {ziel: liste + ["x"] for ziel, liste in vorher.items()}, (
        "Nach Änderungen an den Listen beider Kopien sollte das Original nur die Änderung der flachen Kopie zeigen."
    )

# Obere Grenze: 10 000 Zielnetze mit je 8 Next Hops und 10 000 Protokolleinträgen
tabelle = Routingtabelle(Router("gross"))
for nummer in range(10000):
    tabelle.setze(f"10.{nummer // 256}.{nummer % 256}.0/24", [f"192.168.{n}.1" for n in range(8)])
tief = kopie_von(copy.deepcopy, tabelle)
assert isinstance(tief, Routingtabelle) and tief.routen == tabelle.routen and tief.aenderungen == [], (
    "Bei 10 000 Zielnetzen stimmt die tiefe Kopie nicht."
)
