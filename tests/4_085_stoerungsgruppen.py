# Automatisch erzeugt aus lehrkraft/muster/4_085_stoerungsgruppen.py - nicht von Hand ändern.
# vorlage-hash: f62341511a58e291
# text-hash: 22d3a5e499ec958a
# thema: datenstrukturen
# inhalt: Union-Find mit Pfadkompression

TICKETS = ["T-1", "T-2", "T-3", "T-4", "T-5"]


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def kette_von_hand(laenge):
    """Baut eine Gruppe als lange Kette K0 → K1 → … → K<laenge>, ohne die Methoden der SuS."""
    namen = [f"K{nummer}" for nummer in range(laenge + 1)]
    gruppen = Stoerungsgruppen(namen + ["X"])
    for kind, eltern in zip(namen, namen[1:]):
        gruppen.eltern[kind] = eltern
        gruppen.groesse.pop(kind, None)
    gruppen.groesse[namen[-1]] = laenge + 1
    gruppen.anzahl = 2
    return gruppen, namen


def wurzel_von_hand(gruppen, ticket):
    """Folgt den Eltern bis zur Wurzel, ohne etwas zu verändern; liefert (Wurzel, Tiefe)."""
    tiefe = 0
    while gruppen.eltern[ticket] != ticket and tiefe <= 200_000:
        ticket = gruppen.eltern[ticket]
        tiefe += 1
    return ticket, tiefe


class Vergleich:
    """Vergleichslösung: jede Gruppe als Menge, beim Vereinigen werden die Mengen zusammengelegt."""

    def __init__(self, tickets):
        """Jedes Ticket in seiner eigenen Menge."""
        self.menge_von = {ticket: {ticket} for ticket in tickets}

    def verknuepfe(self, a, b):
        """Legt die Mengen von a und b zusammen; False, wenn es schon dieselbe war."""
        if self.menge_von[a] is self.menge_von[b]:
            return False
        neu = self.menge_von[a] | self.menge_von[b]
        for ticket in neu:
            self.menge_von[ticket] = neu
        return True

    def anzahl(self):
        """Anzahl der verschiedenen Mengen."""
        return len({id(menge) for menge in self.menge_von.values()})


# finde: am Anfang ist jedes Ticket seine eigene Wurzel
gruppen = Stoerungsgruppen(TICKETS)
ergebnis, fehler = rufe(lambda: [gruppen.finde(ticket) for ticket in TICKETS])
assert ergebnis == TICKETS, f"Am Anfang ergibt finde für {TICKETS} {ergebnis!r}, erwartet war {TICKETS!r}." + absturz(fehler)

# finde: folgt den Eltern bis zur Wurzel
gruppen = Stoerungsgruppen(TICKETS)
gruppen.eltern.update({"T-2": "T-1", "T-3": "T-2"})
ergebnis, fehler = rufe(lambda: (gruppen.finde("T-3"), gruppen.finde("T-2"), gruppen.finde("T-4")))
assert ergebnis == ("T-1", "T-1", "T-4"), (
    f"Mit eltern T-3 → T-2 → T-1 ergibt finde für T-3, T-2 und T-4 {ergebnis!r}, erwartet war ('T-1', 'T-1', 'T-4').\n"
    "Tipp: Folgen Sie self.eltern, bis Sie bei einem Ticket ankommen, das auf sich selbst zeigt." + absturz(fehler)
)

# finde: Pfadkompression hängt jedes Ticket auf dem Weg direkt an die Wurzel
gruppen, namen = kette_von_hand(300)
ergebnis, fehler = rufe(lambda: gruppen.finde("K0"))
nicht_umgehaengt = [name for name in namen[:-1] if gruppen.eltern[name] != namen[-1]]
assert ergebnis == "K300" and not nicht_umgehaengt, (
    f"In der Kette K0 → K1 → … → K300 ergibt finde('K0') {ergebnis!r}; erwartet war 'K300'. Danach zeigen noch "
    f"{len(nicht_umgehaengt)} Tickets nicht direkt auf die Wurzel, z. B. {nicht_umgehaengt[:3]}." + absturz(fehler)
    + "\nTipp: Gehen Sie den Weg nach dem Finden der Wurzel ein zweites Mal und setzen Sie jedes self.eltern[…] auf "
    "die Wurzel."
)

# finde: Pfadkompression lässt andere Gruppen in Ruhe
gruppen, namen = kette_von_hand(50)
rufe(lambda: gruppen.finde("K10"))
assert gruppen.eltern["X"] == "X" and gruppen.eltern["K5"] == "K6" and gruppen.eltern["K10"] == "K50", (
    "Nach finde('K10') in der Kette K0 → … → K50 soll K10 direkt auf K50 zeigen, K5 weiter auf K6 (es lag nicht auf "
    f"dem Weg) und X auf sich selbst; es zeigen K10 auf {gruppen.eltern['K10']!r}, K5 auf {gruppen.eltern['K5']!r} "
    f"und X auf {gruppen.eltern['X']!r}."
)

# verknuepfe: das Beispiel, zwei Gruppen werden eine
gruppen = Stoerungsgruppen(TICKETS)
ergebnis, fehler = rufe(lambda: gruppen.verknuepfe("T-2", "T-1"))
wurzeln = (wurzel_von_hand(gruppen, "T-1")[0], wurzel_von_hand(gruppen, "T-2")[0])
assert ergebnis is True and wurzeln[0] == wurzeln[1], (
    f"verknuepfe('T-2', 'T-1') gibt {ergebnis!r} zurück, danach haben T-1 und T-2 die Wurzeln {wurzeln}; erwartet "
    "war True und dieselbe Wurzel.\nTipp: Suchen Sie beide Wurzeln mit finde und hängen Sie die eine unter die andere."
    + absturz(fehler)
)

# verknuepfe: schon in derselben Gruppe ergibt False
gruppen = Stoerungsgruppen(TICKETS)
ergebnis, fehler = rufe(lambda: (gruppen.verknuepfe("T-2", "T-1"), gruppen.verknuepfe("T-3", "T-2"), gruppen.verknuepfe("T-1", "T-3")))
assert ergebnis == (True, True, False), (
    f"Die drei verknuepfe-Aufrufe aus dem Beispiel ergeben {ergebnis!r}, erwartet war (True, True, False)."
    + absturz(fehler)
)

# verknuepfe: ein Ticket mit sich selbst ergibt False
gruppen = Stoerungsgruppen(TICKETS)
ergebnis, fehler = rufe(lambda: gruppen.verknuepfe("T-4", "T-4"))
assert ergebnis is False and gruppen.anzahl == 5, (
    f"verknuepfe('T-4', 'T-4') ergibt {ergebnis!r}, danach ist anzahl {gruppen.anzahl!r}; erwartet war False und 5."
    + absturz(fehler)
)

# verknuepfe: die anzahl sinkt nur bei einer echten Vereinigung
gruppen = Stoerungsgruppen(TICKETS)
rufe(lambda: (gruppen.verknuepfe("T-2", "T-1"), gruppen.verknuepfe("T-3", "T-2"), gruppen.verknuepfe("T-1", "T-3")))
assert gruppen.anzahl == 3, (
    f"Nach den drei Aufrufen aus dem Beispiel ist anzahl {gruppen.anzahl!r}, erwartet war 3.\n"
    "Tipp: Ziehen Sie 1 ab, wenn zwei verschiedene Gruppen vereinigt werden, sonst nicht."
)

# verknuepfe: bei gleicher Größe kommt die Wurzel von b unter die von a
gruppen = Stoerungsgruppen(TICKETS)
rufe(lambda: gruppen.verknuepfe("T-2", "T-1"))
assert gruppen.eltern["T-1"] == "T-2" and gruppen.eltern["T-2"] == "T-2" and gruppen.groesse.get("T-2") == 2, (
    "Nach verknuepfe('T-2', 'T-1') soll T-1 auf T-2 zeigen und groesse['T-2'] 2 sein; es zeigen T-1 auf "
    f"{gruppen.eltern['T-1']!r}, T-2 auf {gruppen.eltern['T-2']!r}, groesse['T-2'] ist {gruppen.groesse.get('T-2')!r}."
)

# verknuepfe: die kleinere Gruppe kommt unter die größere
gruppen = Stoerungsgruppen(TICKETS)
rufe(lambda: (gruppen.verknuepfe("T-1", "T-2"), gruppen.verknuepfe("T-1", "T-3"), gruppen.verknuepfe("T-4", "T-1")))
assert gruppen.eltern["T-4"] == "T-1" and gruppen.groesse.get("T-1") == 4, (
    "Die Gruppe von T-1 hat drei Tickets, T-4 ist allein. Nach verknuepfe('T-4', 'T-1') soll T-4 unter T-1 hängen "
    f"und groesse['T-1'] 4 sein; T-4 zeigt auf {gruppen.eltern['T-4']!r}, groesse['T-1'] ist "
    f"{gruppen.groesse.get('T-1')!r}.\nTipp: Vergleichen Sie self.groesse der beiden Wurzeln und addieren Sie die "
    "kleinere Größe zur größeren."
)

# verknuepfe: Bäume bleiben flach, auch wenn immer ein neues Ticket an die Gruppe kommt
namen = [f"T-{nummer}" for nummer in range(2000)]
vorwaerts, rueckwaerts = Stoerungsgruppen(namen), Stoerungsgruppen(namen)
_, fehler = rufe(lambda: [vorwaerts.verknuepfe(namen[nummer], namen[nummer + 1]) for nummer in range(1999)])
_, zweiter_fehler = rufe(lambda: [rueckwaerts.verknuepfe(namen[nummer + 1], namen[nummer]) for nummer in range(1999)])
tiefe = max(wurzel_von_hand(gruppen, name)[1] for gruppen in (vorwaerts, rueckwaerts) for name in namen)
eine_gruppe = all(len({wurzel_von_hand(gruppen, name)[0] for name in namen}) == 1 for gruppen in (vorwaerts, rueckwaerts))
assert fehler is None and zweiter_fehler is None and eine_gruppe and tiefe <= 11, (
    ("" if eine_gruppe else "Danach sind nicht alle 2000 Tickets in einer Gruppe. ") +
    "Nach verknuepfe(T-0, T-1), verknuepfe(T-1, T-2), … verknuepfe(T-1998, T-1999) oder denselben Aufrufen mit "
    f"vertauschten Argumenten ist der längste Weg zu einer Wurzel {tiefe} Schritte lang; mit Vereinigen nach Größe "
    "wären es höchstens 11 (log₂ 2000)." + absturz(fehler or zweiter_fehler)
    + "\nTipp: Hängen Sie die Wurzel der kleineren Gruppe unter die der größeren, nicht immer a unter b."
)

# gleiche_ursache: das Beispiel
gruppen = Stoerungsgruppen(TICKETS)
gruppen.eltern.update({"T-1": "T-2", "T-3": "T-2"})
ergebnis, fehler = rufe(lambda: (gruppen.gleiche_ursache("T-3", "T-1"), gruppen.gleiche_ursache("T-3", "T-4")))
assert ergebnis == (True, False), (
    f"gleiche_ursache('T-3', 'T-1') und gleiche_ursache('T-3', 'T-4') ergeben {ergebnis!r}, erwartet war (True, False)."
    + absturz(fehler) + "\nTipp: Vergleichen Sie die Wurzeln, nicht die Eltern."
)

# gleiche_ursache: über mehrere Ebenen
gruppen, namen = kette_von_hand(20)
ergebnis, fehler = rufe(lambda: (gruppen.gleiche_ursache("K0", "K19"), gruppen.gleiche_ursache("X", "K3")))
assert ergebnis == (True, False), (
    f"In der Kette K0 → … → K20 ergeben gleiche_ursache('K0', 'K19') und gleiche_ursache('X', 'K3') {ergebnis!r}, "
    "erwartet war (True, False)." + absturz(fehler)
)

# tickets_der_gruppe: das Beispiel
gruppen = Stoerungsgruppen(TICKETS)
gruppen.eltern.update({"T-1": "T-2", "T-3": "T-2"})
ergebnis, fehler = rufe(lambda: gruppen.tickets_der_gruppe("T-3"))
assert ergebnis == ["T-1", "T-2", "T-3"], (
    f"tickets_der_gruppe('T-3') ergibt {ergebnis!r}, erwartet war ['T-1', 'T-2', 'T-3'].\n"
    "Tipp: Sammeln Sie alle Tickets, deren Wurzel die Wurzel von ticket ist, und sortieren Sie." + absturz(fehler)
)

# tickets_der_gruppe: ein Ticket allein
gruppen = Stoerungsgruppen(TICKETS)
ergebnis, fehler = rufe(lambda: gruppen.tickets_der_gruppe("T-5"))
assert ergebnis == ["T-5"], f"tickets_der_gruppe('T-5') ergibt {ergebnis!r}, erwartet war ['T-5']." + absturz(fehler)

# anzahl_stoerungen: das Beispiel
gruppen = Stoerungsgruppen(TICKETS)
gruppen.anzahl = 3
ergebnis, fehler = rufe(gruppen.anzahl_stoerungen)
assert ergebnis == 3, f"anzahl_stoerungen() ergibt {ergebnis!r}, wenn self.anzahl 3 ist; erwartet war 3." + absturz(fehler)

# anzahl_stoerungen: ein einziges Ticket
ergebnis, fehler = rufe(Stoerungsgruppen(["T-9"]).anzahl_stoerungen)
assert ergebnis == 1, f"anzahl_stoerungen() mit einem Ticket ergibt {ergebnis!r}, erwartet war 1." + absturz(fehler)

zufall = Zufall(4085)

# Viele zufällige Verknüpfungen im Vergleich mit Mengen
for _ in range(80):
    namen = [f"T-{nummer}" for nummer in range(zufall.randint(1, 30))]
    gruppen, vergleich = Stoerungsgruppen(namen), Vergleich(namen)
    protokoll = []
    for _ in range(zufall.randint(0, 40)):
        a, b = zufall.choice(namen), zufall.choice(namen)
        protokoll.append(f"verknuepfe({a!r}, {b!r})")
        ergebnis, fehler = rufe(lambda: gruppen.verknuepfe(a, b))
        erwartet = vergleich.verknuepfe(a, b)
        assert ergebnis == erwartet, (
            f"Mit {len(namen)} Tickets nach {', '.join(protokoll)} gibt der letzte Aufruf {ergebnis!r} zurück, "
            f"erwartet war {erwartet!r}." + absturz(fehler)
        )
    a, b = zufall.choice(namen), zufall.choice(namen)
    ergebnis, fehler = rufe(lambda: (gruppen.gleiche_ursache(a, b), gruppen.tickets_der_gruppe(a), gruppen.anzahl_stoerungen()))
    erwartet = (vergleich.menge_von[a] is vergleich.menge_von[b], sorted(vergleich.menge_von[a]), vergleich.anzahl())
    assert ergebnis == erwartet, (
        f"Mit {len(namen)} Tickets nach {', '.join(protokoll)} ergeben gleiche_ursache({a!r}, {b!r}), "
        f"tickets_der_gruppe({a!r}) und anzahl_stoerungen() {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
    )


def viele_verknuepfungen(anzahl):
    """Verknüpft anzahl Tickets in zufälliger Reihenfolge und fragt danach oft nach."""
    namen = [f"T-{nummer}" for nummer in range(anzahl)]
    gruppen = Stoerungsgruppen(namen)
    reihenfolge = Zufall(anzahl)
    for _ in range(anzahl):
        gruppen.verknuepfe(reihenfolge.choice(namen), reihenfolge.choice(namen))
    treffer = 0
    for _ in range(anzahl):
        treffer += gruppen.gleiche_ursache(reihenfolge.choice(namen), reihenfolge.choice(namen))
    return gruppen.anzahl_stoerungen(), treffer


# Laufzeit: fast O(1) je Aufruf
_, schritte_klein = zaehle_schritte(viele_verknuepfungen, 2000)
_, schritte_gross = zaehle_schritte(viele_verknuepfungen, 8000)
assert schritte_gross <= 6 * schritte_klein, (
    f"2000 Tickets brauchen {schritte_klein} Schritte, 8000 brauchen {schritte_gross}; bei fast O(1) je Aufruf wäre "
    "es etwa das Vierfache. Ihre Lösung wächst schneller.\nTipp: Vereinigen Sie nach Größe und hängen Sie in finde "
    "den Weg direkt an die Wurzel; nummerieren Sie keine ganzen Gruppen um."
)

# Obere Grenze: 100000 Tickets
namen = [f"T-{nummer}" for nummer in range(100_000)]
gruppen = Stoerungsgruppen(namen)


def gross():
    """Verknüpft alle Tickets paarweise zu Ketten und fragt nach."""
    for nummer in range(0, 100_000, 2):
        gruppen.verknuepfe(namen[nummer], namen[nummer + 1])
    for nummer in range(0, 99_998, 4):
        gruppen.verknuepfe(namen[nummer + 3], namen[nummer])
    return gruppen.anzahl_stoerungen(), gruppen.gleiche_ursache("T-0", "T-3"), gruppen.gleiche_ursache("T-0", "T-4")


ergebnis, fehler = rufe(gross)
assert ergebnis == (25_000, True, False), (
    f"Mit 100000 Tickets ergibt das {ergebnis!r}, erwartet war (25000, True, False)." + absturz(fehler)
)
