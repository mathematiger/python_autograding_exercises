# Automatisch erzeugt aus lehrkraft/muster/4_089_inventur.py - nicht von Hand ändern.
# vorlage-hash: b6f9b8760c98a14f
# text-hash: 4006ca60569ffb64
# thema: programmaufbau
# inhalt: Projekt: Lager mit Inventur

import dataclasses
import enum


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def ausnahme_von(aufruf):
    """Führt aufruf() aus und gibt die ausgelöste Ausnahme zurück, oder None."""
    try:
        aufruf()
    except Exception as fehler:
        return fehler
    return None


def name_von(fehler):
    """Name der Ausnahmeklasse oder „keine Ausnahme“ für Meldungen."""
    return "keine Ausnahme" if fehler is None else f"{type(fehler).__name__}: {fehler}"


def von_hand(bestaende):
    """Baut ein Lager mit den Beständen {nummer: bestand}, ohne die Buchungsmethoden der SuS."""
    lager = Lager()
    for nummer, bestand in bestaende.items():
        lager.artikel[nummer] = Artikel(nummer, f"Artikel {nummer}", bestand)
    return lager


def bestaende(lager):
    """Liest die Bestände aller Artikel aus."""
    return {nummer: artikel.bestand for nummer, artikel in lager.artikel.items()}


def journal_als_tupel(lager):
    """Liest das Journal als Liste von (nummer, Name der Buchungsart, menge)."""
    return [(buchung.nummer, getattr(buchung.art, "name", buchung.art), buchung.menge) for buchung in lager.journal]


def zaehle_mit(lager, eintraege, abbruch=None):
    """Führt eine Inventur mit den eintraegen durch; abbruch wird im Block ausgelöst. Gibt die Ausnahme zurück oder None."""
    try:
        with lager.inventur() as zaehlung:
            zaehlung.update(eintraege)
            if abbruch is not None:
                raise abbruch
    except Exception as fehler:
        return fehler
    return None


START = {"SW-24": 7, "AP-6": 0, "PK-3": 200}

# Buchungsart: eine Aufzählung mit ZUGANG, ABGANG und INVENTUR
mitglieder = [mitglied.name for mitglied in Buchungsart] if isinstance(Buchungsart, enum.EnumMeta) else None
assert issubclass(Buchungsart, enum.Enum) and sorted(mitglieder) == ["ABGANG", "INVENTUR", "ZUGANG"], (
    f"Buchungsart hat die Mitglieder {mitglieder!r}; erwartet war eine Unterklasse von Enum mit ZUGANG, ABGANG und "
    "INVENTUR.\nTipp: class Buchungsart(Enum): und darin ZUGANG = \"Zugang\" usw."
)

# Artikel: eine Datenklasse mit nummer, bezeichnung und bestand
felder = [feld.name for feld in dataclasses.fields(Artikel)] if dataclasses.is_dataclass(Artikel) else None
assert felder == ["nummer", "bezeichnung", "bestand"], (
    f"Artikel hat die Felder {felder!r}, erwartet waren ['nummer', 'bezeichnung', 'bestand'] in dieser Reihenfolge."
)

# Artikel: bestand hat den Standardwert 0
artikel, fehler = rufe(lambda: Artikel("SW-24", "Switch 24 Ports"))
assert artikel is not None and (artikel.nummer, artikel.bezeichnung, artikel.bestand) == ("SW-24", "Switch 24 Ports", 0), (
    f"Artikel('SW-24', 'Switch 24 Ports') ergibt {artikel!r}, erwartet war bestand 0." + absturz(fehler)
)

# Buchung: eine Datenklasse mit nummer, art und menge
felder = [feld.name for feld in dataclasses.fields(Buchung)] if dataclasses.is_dataclass(Buchung) else None
assert felder == ["nummer", "art", "menge"], (
    f"Buchung hat die Felder {felder!r}, erwartet waren ['nummer', 'art', 'menge'] in dieser Reihenfolge."
)

# Buchung: unveränderlich und vergleichbar
buchung, fehler = rufe(lambda: Buchung("PK-3", Buchungsart.ZUGANG, 5))
geaendert = ausnahme_von(lambda: setattr(buchung, "menge", 6))
assert isinstance(geaendert, dataclasses.FrozenInstanceError) and buchung == Buchung("PK-3", Buchungsart.ZUGANG, 5), (
    f"buchung.menge = 6 ergibt {name_von(geaendert)}; erwartet war dataclasses.FrozenInstanceError.\n"
    "Tipp: @dataclass(frozen=True) über class Buchung." + absturz(fehler)
)

# Fehler: alle Lagerfehler erben von LagerFehler
fehlend = [klasse.__name__ for klasse in (UnbekannterArtikel, BestandZuGering, LagerGesperrt) if not issubclass(klasse, LagerFehler)]
assert issubclass(LagerFehler, Exception) and not fehlend, f"Diese Klassen erben nicht von LagerFehler: {fehlend}."

# UnbekannterArtikel: speichert die Nummer
fehler, problem = rufe(lambda: UnbekannterArtikel("FW-1"))
assert getattr(fehler, "nummer", None) == "FW-1", (
    f"UnbekannterArtikel('FW-1') hat nummer {getattr(fehler, 'nummer', None)!r}; "
    "erwartet war nummer 'FW-1'.\nTipp: super().__init__(meldung) und "
    "self.nummer = nummer" + absturz(problem)
)

# BestandZuGering: speichert Nummer, Bestand und Menge
fehler, problem = rufe(lambda: BestandZuGering("AP-6", 2, 5))
werte = tuple(getattr(fehler, name, None) for name in ("nummer", "bestand", "menge"))
assert werte == ("AP-6", 2, 5), (
    f"BestandZuGering('AP-6', 2, 5) hat nummer, bestand und menge {werte!r}; "
    "erwartet war ('AP-6', 2, 5)." + absturz(problem)
)

# Fehler: beide geben eine verständliche Meldung als Text an Exception weiter
unbekannt, _ = rufe(lambda: UnbekannterArtikel("FW-1"))
zu_gering, _ = rufe(lambda: BestandZuGering("AP-6", 2, 5))
argumente = (getattr(unbekannt, "args", None), getattr(zu_gering, "args", None))
assert all(
    isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], str) for args in argumente
) and vergleichbar(str(unbekannt)) != vergleichbar("FW-1"), (
    f"Exception bekommt von UnbekannterArtikel('FW-1') die Argumente {argumente[0]!r} und von "
    f"BestandZuGering('AP-6', 2, 5) die Argumente {argumente[1]!r}; erwartet war jeweils genau ein Text, der in Worten "
    "sagt, was schiefging, etwa ('Den Artikel FW-1 gibt es nicht',).\nTipp: Rufen Sie in __init__ "
    "super().__init__(meldung) mit einem f-String auf."
)

# _artikel: findet einen vorhandenen Artikel
lager = von_hand(START)
ergebnis, fehler = rufe(lambda: lager._artikel("PK-3"))
assert ergebnis is lager.artikel["PK-3"], f"_artikel('PK-3') ergibt {ergebnis!r}, erwartet war der Artikel PK-3." + absturz(fehler)

# _artikel: eine unbekannte Nummer löst UnbekannterArtikel aus
fehler = ausnahme_von(lambda: von_hand(START)._artikel("FW-1"))
assert isinstance(fehler, UnbekannterArtikel) and getattr(fehler, "nummer", None) == "FW-1", (
    f"_artikel('FW-1') ergibt {name_von(fehler)}, erwartet war UnbekannterArtikel mit nummer 'FW-1'."
)

# zugang: erhöht den Bestand
lager = von_hand(START)
_, fehler = rufe(lambda: lager.zugang("SW-24", 5))
assert bestaende(lager) == dict(START, **{"SW-24": 12}), (
    f"Nach zugang('SW-24', 5) bei Bestand 7 sind die Bestände {bestaende(lager)!r}, erwartet war SW-24 mit 12."
    + absturz(fehler)
)

# zugang: schreibt eine Buchung ins Journal
lager = von_hand(START)
rufe(lambda: (lager.zugang("SW-24", 5), lager.zugang("AP-6", 2)))
erwartet = [Buchung("SW-24", Buchungsart.ZUGANG, 5), Buchung("AP-6", Buchungsart.ZUGANG, 2)]
assert lager.journal == erwartet, f"Nach zugang('SW-24', 5) und zugang('AP-6', 2) ist das Journal {lager.journal!r}, erwartet war {erwartet!r}."

# abgang: senkt den Bestand und bucht eine negative Menge
lager = von_hand(START)
_, fehler = rufe(lambda: lager.abgang("PK-3", 30))
assert lager.artikel["PK-3"].bestand == 170 and lager.journal == [Buchung("PK-3", Buchungsart.ABGANG, -30)], (
    f"Nach abgang('PK-3', 30) bei Bestand 200 ist der Bestand {lager.artikel['PK-3'].bestand!r} und das Journal "
    f"{lager.journal!r}; erwartet war 170 und [Buchung('PK-3', Buchungsart.ABGANG, -30)]." + absturz(fehler)
    + "\nTipp: Die menge der Buchung ist die Änderung des Bestands, beim Abgang also -menge."
)

# abgang: den ganzen Bestand entnehmen ist erlaubt
lager = von_hand(START)
_, fehler = rufe(lambda: lager.abgang("SW-24", 7))
assert fehler is None and lager.artikel["SW-24"].bestand == 0, (
    f"abgang('SW-24', 7) bei Bestand 7 soll klappen und 0 übrig lassen; Bestand danach {lager.artikel['SW-24'].bestand!r}."
    + absturz(fehler)
)

# abgang: mehr als da ist löst BestandZuGering aus und ändert nichts
lager = von_hand(START)
fehler = ausnahme_von(lambda: lager.abgang("SW-24", 8))
werte = tuple(getattr(fehler, name, None) for name in ("nummer", "bestand", "menge"))
assert isinstance(fehler, BestandZuGering) and werte == ("SW-24", 7, 8) and bestaende(lager) == START and lager.journal == [], (
    f"abgang('SW-24', 8) bei Bestand 7 ergibt {name_von(fehler)} mit nummer, bestand, menge {werte!r}; danach sind "
    f"die Bestände {bestaende(lager)!r} und das Journal {lager.journal!r}. Erwartet war BestandZuGering mit "
    "('SW-24', 7, 8) und keine Änderung.\nTipp: Erst prüfen, dann ändern."
)

# zugang und abgang: unbekannte Nummer löst UnbekannterArtikel aus und ändert nichts
lager = von_hand(START)
fehler = (ausnahme_von(lambda: lager.zugang("FW-1", 2)), ausnahme_von(lambda: lager.abgang("FW-1", 2)))
assert all(isinstance(einzeln, UnbekannterArtikel) for einzeln in fehler) and lager.journal == [] and "FW-1" not in lager.artikel, (
    f"zugang('FW-1', 2) und abgang('FW-1', 2) ergeben {name_von(fehler[0])} und {name_von(fehler[1])}; danach ist "
    f"das Journal {lager.journal!r}. Erwartet war zweimal UnbekannterArtikel und ein leeres Journal."
)

# inventur: der with-Block bekommt ein leeres Dictionary
lager = von_hand(START)
zaehlung, fehler = None, None
try:
    with lager.inventur() as zaehlung:
        pass
except Exception as ausnahme:
    fehler = f"{type(ausnahme).__name__}: {ausnahme}"
assert zaehlung == {} and isinstance(zaehlung, dict), (
    f"with lager.inventur() as zaehlung: liefert zaehlung = {zaehlung!r}, erwartet war ein leeres Dictionary.\n"
    "Tipp: yield zaehlung im Kontextmanager." + absturz(fehler)
)

# inventur: das Beispiel, Bestände werden auf das Ist gesetzt
lager = von_hand(START)
fehler = zaehle_mit(lager, {"SW-24": 6, "PK-3": 212, "AP-6": 0})
assert bestaende(lager) == {"SW-24": 6, "AP-6": 0, "PK-3": 212}, (
    f"Nach der Inventur aus dem Beispiel sind die Bestände {bestaende(lager)!r}, erwartet war "
    "{'SW-24': 6, 'AP-6': 0, 'PK-3': 212}.\nTipp: Erst nach dem yield, also wenn der with-Block fertig ist, steht die "
    "Zählung im Dictionary." + absturz(fehler and f"{type(fehler).__name__}: {fehler}")
)

# inventur: die Differenzen stehen nach Nummer sortiert im Journal
lager = von_hand(START)
zaehle_mit(lager, {"SW-24": 6, "PK-3": 212, "AP-6": 0})
erwartet = [("PK-3", "INVENTUR", 12), ("SW-24", "INVENTUR", -1)]
assert journal_als_tupel(lager) == erwartet, (
    f"Nach der Inventur aus dem Beispiel enthält das Journal {journal_als_tupel(lager)!r}, erwartet war {erwartet!r}: "
    "eine Buchung je Abweichung (ist - soll), nach Nummer sortiert, keine für AP-6, wo alles stimmt."
)

# inventur: nicht gezählte Artikel bleiben unverändert
lager = von_hand(START)
zaehle_mit(lager, {"AP-6": 3})
assert bestaende(lager) == {"SW-24": 7, "AP-6": 3, "PK-3": 200} and journal_als_tupel(lager) == [("AP-6", "INVENTUR", 3)], (
    f"Nach einer Inventur, die nur AP-6 mit 3 zählt, sind die Bestände {bestaende(lager)!r} und das Journal "
    f"{journal_als_tupel(lager)!r}; erwartet war nur AP-6 auf 3 mit einer Buchung +3."
)

# inventur: während der Zählung sind Buchungen gesperrt
lager = von_hand(START)
im_block = []
try:
    with lager.inventur():
        im_block.append(ausnahme_von(lambda: lager.zugang("AP-6", 4)))
        im_block.append(ausnahme_von(lambda: lager.abgang("PK-3", 1)))
except Exception:
    pass
assert len(im_block) == 2 and all(isinstance(fehler, LagerGesperrt) for fehler in im_block) and bestaende(lager) == START, (
    f"zugang und abgang während der Inventur ergeben {[name_von(fehler) for fehler in im_block]}; erwartet war "
    f"zweimal LagerGesperrt, und die Bestände sollen gleich bleiben (sie sind {bestaende(lager)!r}).\nTipp: "
    "Setzen Sie beim Betreten self.gesperrt = True und prüfen Sie es in zugang und abgang."
)

# inventur: danach ist das Lager wieder frei
lager = von_hand(START)
zaehle_mit(lager, {"SW-24": 6})
fehler = ausnahme_von(lambda: lager.zugang("SW-24", 1))
assert fehler is None and lager.artikel["SW-24"].bestand == 7, (
    f"Nach der Inventur ergibt zugang('SW-24', 1) {name_von(fehler)}, der Bestand ist "
    f"{lager.artikel['SW-24'].bestand!r}; erwartet war keine Ausnahme und Bestand 7."
)

# inventur: eine zweite Inventur während der ersten löst LagerGesperrt aus
lager = von_hand(START)
zweite = None
try:
    with lager.inventur():
        zweite = zaehle_mit(lager, {})
except Exception:
    pass
assert isinstance(zweite, LagerGesperrt), f"Eine zweite Inventur während der ersten ergibt {name_von(zweite)}, erwartet war LagerGesperrt."

# inventur: eine zweite Inventur hebt die Sperre der ersten nicht auf
lager = von_hand(START)
noch_gesperrt = None
try:
    with lager.inventur():
        zaehle_mit(lager, {})
        noch_gesperrt = ausnahme_von(lambda: lager.zugang("AP-6", 1))
except Exception:
    pass
assert isinstance(noch_gesperrt, LagerGesperrt), (
    f"Nach einem abgelehnten zweiten inventur() innerhalb der ersten ergibt zugang {name_von(noch_gesperrt)}, "
    "erwartet war weiterhin LagerGesperrt.\nTipp: Prüfen Sie die Sperre, bevor Sie in den try-Block gehen; sonst gibt "
    "das finally der abgelehnten Inventur die Sperre frei."
)

# inventur: eine Ausnahme im with-Block fliegt weiter, gebucht wird nichts
lager = von_hand(START)
fehler = zaehle_mit(lager, {"SW-24": 1, "PK-3": 1}, abbruch=KeyError("Zählliste unvollständig"))
assert isinstance(fehler, KeyError) and bestaende(lager) == START and lager.journal == [], (
    f"Bricht der with-Block mit KeyError ab, kommt außen {name_von(fehler)} an; die Bestände sind "
    f"{bestaende(lager)!r}, das Journal {lager.journal!r}. Erwartet war der KeyError und keine Änderung."
)

# inventur: nach einer Ausnahme im with-Block ist das Lager wieder frei
lager = von_hand(START)
zaehle_mit(lager, {"SW-24": 1}, abbruch=KeyError("Zählliste unvollständig"))
fehler = ausnahme_von(lambda: lager.zugang("SW-24", 1))
assert fehler is None and lager.artikel["SW-24"].bestand == 8, (
    f"Nach einer abgebrochenen Inventur ergibt zugang('SW-24', 1) {name_von(fehler)}; erwartet war keine Ausnahme.\n"
    "Tipp: Geben Sie die Sperre in einem finally frei."
)

# inventur: eine unbekannte Nummer in der Zählung bucht gar nichts
lager = von_hand(START)
fehler = zaehle_mit(lager, {"SW-24": 1, "AP-6": 5, "XX-9": 4})
assert isinstance(fehler, UnbekannterArtikel) and getattr(fehler, "nummer", None) == "XX-9" and bestaende(lager) == START and lager.journal == [], (
    f"Eine Zählung mit der unbekannten Nummer XX-9 ergibt {name_von(fehler)}; danach sind die Bestände "
    f"{bestaende(lager)!r} und das Journal {lager.journal!r}. Erwartet war UnbekannterArtikel mit nummer 'XX-9' und "
    "keine Änderung, auch nicht an SW-24 und AP-6.\nTipp: Prüfen Sie erst alle Nummern, dann buchen Sie."
)

# inventur: auch nach einer unbekannten Nummer ist das Lager wieder frei
lager = von_hand(START)
zaehle_mit(lager, {"XX-9": 4})
fehler = ausnahme_von(lambda: lager.abgang("PK-3", 1))
assert fehler is None and lager.artikel["PK-3"].bestand == 199, (
    f"Nach einer Inventur mit unbekannter Nummer ergibt abgang('PK-3', 1) {name_von(fehler)}; erwartet war keine Ausnahme."
)

# Das Beispiel aus dem Aufgabentext von anlegen bis Inventur
lager = Lager()
_, fehler = rufe(lambda: [lager.anlegen(nummer, "Teil") for nummer in ("SW-24", "AP-6", "PK-3")])
_, fehler = rufe(lambda: (lager.zugang("SW-24", 10), lager.zugang("PK-3", 200), lager.abgang("SW-24", 3)))
abgelehnt = (ausnahme_von(lambda: lager.abgang("AP-6", 1)), ausnahme_von(lambda: lager.zugang("FW-1", 2)))
inventur = zaehle_mit(lager, {"SW-24": 6, "PK-3": 212, "AP-6": 0})
erwartet = [("SW-24", "ZUGANG", 10), ("PK-3", "ZUGANG", 200), ("SW-24", "ABGANG", -3), ("PK-3", "INVENTUR", 12), ("SW-24", "INVENTUR", -1)]
assert (
    isinstance(abgelehnt[0], BestandZuGering) and isinstance(abgelehnt[1], UnbekannterArtikel) and inventur is None
    and journal_als_tupel(lager) == erwartet
), (
    f"Im Beispiel ergeben abgang('AP-6', 1) {name_von(abgelehnt[0])} und zugang('FW-1', 2) {name_von(abgelehnt[1])}, "
    f"die Inventur {name_von(inventur)}, und das Journal ist\n{journal_als_tupel(lager)!r},\nerwartet war "
    f"BestandZuGering, UnbekannterArtikel, keine Ausnahme und\n{erwartet!r}." + absturz(fehler)
)


class Vergleich:
    """Vergleichslösung: Bestände als Dictionary, Journal als Liste von Tupeln."""

    def __init__(self, nummern):
        """Alle Artikel mit Bestand 0."""
        self.bestand = {nummer: 0 for nummer in nummern}
        self.journal = []

    def buche(self, art, nummer, menge):
        """Gibt den Namen der erwarteten Ausnahme zurück oder None und bucht, wenn alles passt."""
        if nummer not in self.bestand:
            return "UnbekannterArtikel"
        aenderung = menge if art == "ZUGANG" else -menge
        if self.bestand[nummer] + aenderung < 0:
            return "BestandZuGering"
        self.bestand[nummer] += aenderung
        self.journal.append((nummer, art, aenderung))
        return None

    def inventur(self, zaehlung, abbruch):
        """Gibt den Namen der erwarteten Ausnahme zurück oder None und bucht die Differenzen."""
        if abbruch:
            return "KeyError"
        if any(nummer not in self.bestand for nummer in zaehlung):
            return "UnbekannterArtikel"
        for nummer in sorted(zaehlung):
            if zaehlung[nummer] != self.bestand[nummer]:
                self.journal.append((nummer, "INVENTUR", zaehlung[nummer] - self.bestand[nummer]))
                self.bestand[nummer] = zaehlung[nummer]
        return None


zufall = Zufall(4089)

# Viele zufällige Buchungen und Inventuren im Vergleich mit einer einfachen Nachrechnung
for _ in range(60):
    nummern = [f"A-{nummer}" for nummer in range(zufall.randint(1, 6))]
    lager, vergleich = Lager(), Vergleich(nummern)
    for nummer in nummern:
        lager.anlegen(nummer, "Teil")
    protokoll = []
    for _ in range(zufall.randint(1, 25)):
        nummer = zufall.choice(nummern + ["X-1"])
        if zufall.random() < 0.8:
            art, menge = zufall.choice(["ZUGANG", "ABGANG"]), zufall.randint(1, 20)
            protokoll.append(f"{art.lower()}({nummer!r}, {menge})")
            methode = lager.zugang if art == "ZUGANG" else lager.abgang
            fehler, erwartet = ausnahme_von(lambda: methode(nummer, menge)), vergleich.buche(art, nummer, menge)
        else:
            zaehlung = {zufall.choice(nummern + ["X-1"]): zufall.randint(0, 20) for _ in range(zufall.randint(0, 4))}
            abbruch = zufall.random() < 0.2
            protokoll.append(f"inventur mit {zaehlung}" + (" und Ausnahme im Block" if abbruch else ""))
            fehler = zaehle_mit(lager, zaehlung, KeyError("Abbruch") if abbruch else None)
            erwartet = vergleich.inventur(zaehlung, abbruch)
        bekommen = None if fehler is None else type(fehler).__name__
        assert bekommen == erwartet and bestaende(lager) == vergleich.bestand and journal_als_tupel(lager) == vergleich.journal, (
            f"Nach {', '.join(protokoll)}:\nbeim letzten Schritt kam {bekommen or 'keine Ausnahme'} (erwartet "
            f"{erwartet or 'keine Ausnahme'}), die Bestände sind {bestaende(lager)!r} (erwartet {vergleich.bestand!r}), "
            f"das Journal ist\n{journal_als_tupel(lager)!r},\nerwartet war\n{vergleich.journal!r}."
        )

# Obere Grenze: 10000 Artikel, 100000 Buchungen und eine große Inventur
zufall = Zufall(100_000)
lager = Lager()
nummern = [f"HW-{nummer:05d}" for nummer in range(10_000)]
for nummer in nummern:
    lager.anlegen(nummer, "Teil")


def viele_buchungen():
    """Bucht 100000 Zugänge und Abgänge und zählt danach alle Artikel."""
    soll = dict.fromkeys(nummern, 0)
    for schritt in range(100_000):
        nummer = nummern[schritt % 10_000]
        if schritt < 50_000 or soll[nummer] < 3:
            lager.zugang(nummer, 5)
            soll[nummer] += 5
        else:
            lager.abgang(nummer, 3)
            soll[nummer] -= 3
    with lager.inventur() as zaehlung:
        for nummer in nummern:
            zaehlung[nummer] = soll[nummer] + (1 if nummer.endswith("7") else 0)
    return soll


soll, fehler = rufe(viele_buchungen)
inventurbuchungen = [buchung for buchung in lager.journal if getattr(buchung.art, "name", None) == "INVENTUR"]
assert fehler is None and len(lager.journal) == 101_000 and len(inventurbuchungen) == 1000 and all(
    lager.artikel[nummer].bestand == soll[nummer] + (1 if nummer.endswith("7") else 0) for nummer in nummern
), (
    f"Nach 100000 Buchungen und einer Inventur über 10000 Artikel, bei der jeder zehnte einen mehr hat, stehen "
    f"{len(lager.journal)} Buchungen im Journal, davon {len(inventurbuchungen)} Inventurbuchungen; erwartet waren "
    "101000 und 1000, und alle Bestände sollen dem Ist entsprechen." + absturz(fehler)
)
