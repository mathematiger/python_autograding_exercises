# Automatisch erzeugt aus lehrkraft/muster/5_023_wahrheitswert.py - nicht von Hand ändern.
# vorlage-hash: 1087af61ac727ff1
# text-hash: 65c946ba8cdd31a9
# thema: klassen
# inhalt: __bool__ und __len__

def versuche(funktion):
    """Ruft funktion() auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(), None
    except Exception as fehler:
        return None, fehler


def liste_mit(offen, geschlossen):
    """Baut eine Ticketliste mit diesen offenen und geschlossenen Nummern."""
    neue = Ticketliste()
    for nummer in offen:
        neue.oeffnen(nummer)
    for nummer in geschlossen:
        neue.schliessen(nummer)
    return neue


def sla_mit(frist, zielprozent, dauern):
    """Baut eine SlaAuswertung mit diesen Dauern."""
    neue = SlaAuswertung(frist, zielprozent)
    for dauer in dauern:
        neue.erfassen(dauer)
    return neue


# Ticketliste: len zählt die Tickets
ergebnis, fehler = versuche(lambda: len(liste_mit([101, 102, 103], [])))
assert ergebnis == 3, f"Drei offene Tickets: len(liste) ergibt {ergebnis!r} {fehler or ''}, erwartet war 3."

# Ticketliste: geschlossene Tickets zählen nicht mit
ergebnis, fehler = versuche(lambda: len(liste_mit([101, 102], [101])))
assert ergebnis == 1, (
    f"oeffnen(101), oeffnen(102), schliessen(101): len(liste) ergibt {ergebnis!r} {fehler or ''}, erwartet war 1.\n"
    "Tipp: Zählen Sie nur die Einträge in self._status, deren Wert \"offen\" ist."
)

# Ticketliste: dieselbe Nummer zweimal geöffnet ist ein Ticket, wieder geöffnet zählt es erneut
liste_test = liste_mit([7, 7, 8], [8])
liste_test.oeffnen(8)
liste_test.schliessen(9)
ergebnis, fehler = versuche(lambda: len(liste_test))
assert ergebnis == 2, (
    "oeffnen(7), oeffnen(7), oeffnen(8), schliessen(8), oeffnen(8), schliessen(9): "
    f"len(liste) ergibt {ergebnis!r} {fehler or ''}, erwartet waren 2 offene Tickets (7 und 8)."
)

# Ticketliste: mit offenen Tickets ist die Liste wahr
ergebnis, fehler = versuche(lambda: (bool(liste_mit([5], [])), "ja" if liste_mit([5, 6], [6]) else "nein"))
assert ergebnis == (True, "ja"), (
    f"Mit offenen Tickets erwartet bool(liste) True und if liste: wahr; bekommen {ergebnis!r} {fehler or ''}."
)

# Ticketliste: ohne offene Tickets ist die Liste falsch, auch wenn geschlossene darin stehen
ergebnis, fehler = versuche(lambda: (bool(Ticketliste()), not liste_mit([5, 6], [5, 6]), bool(liste_mit([], [3]))))
assert ergebnis == (False, True, False), (
    "Leere Liste, alle geschlossen, nur schliessen(3): erwartet bool False, not liste True, bool False; "
    f"bekommen {ergebnis!r} {fehler or ''}.\nTipp: Ohne __bool__ fragt Python __len__; zählt Ihr __len__ nur offene Tickets?"
)

# Ticketliste: kein eigenes __bool__, Python nimmt __len__
assert "__bool__" not in vars(Ticketliste), (
    "Ticketliste soll kein __bool__ haben: Der Wahrheitswert ergibt sich schon aus __len__ (0 heißt falsch). "
    "Ein __bool__, das len(self) > 0 wiederholt, wäre doppelte Logik."
)

# SlaAuswertung: len zählt die erfassten Tickets
ergebnis, fehler = versuche(lambda: (len(sla_mit(8, 90, [2, 5, 12])), len(sla_mit(8, 90, [1] * 7))))
assert ergebnis == (3, 7), f"len nach 3 und nach 7 erfassten Dauern ergibt {ergebnis!r} {fehler or ''}, erwartet war (3, 7)."

# SlaAuswertung: das Beispiel, 2 von 3 in der Frist reicht bei 90 % nicht
ergebnis, fehler = versuche(lambda: bool(sla_mit(8, 90, [2, 5, 12])))
assert ergebnis is False, (
    f"SlaAuswertung(8, 90) mit den Dauern 2, 5, 12: bool ergibt {ergebnis!r} {fehler or ''}, erwartet war False "
    "(nur 2 von 3, also 67 %, sind in der Frist)."
)

# SlaAuswertung: alle in der Frist ist eingehalten
ergebnis, fehler = versuche(lambda: bool(sla_mit(8, 90, [2, 5, 7])))
assert ergebnis is True, f"SlaAuswertung(8, 90) mit den Dauern 2, 5, 7: bool ergibt {ergebnis!r} {fehler or ''}, erwartet war True."

# SlaAuswertung: __bool__ liefert genau True oder False
ergebnis, fehler = versuche(lambda: sla_mit(8, 50, [2, 12]).__bool__())
assert type(ergebnis) is bool, (
    f"__bool__() ergibt {ergebnis!r} {fehler or ''}; erwartet war genau True oder False, sonst bricht bool() mit einem "
    "TypeError ab.\nTipp: Geben Sie das Ergebnis eines Vergleichs zurück, etwa 100 * in_frist >= ..."
)

# SlaAuswertung: ohne erfasste Tickets wahr, obwohl len 0 ist
ergebnis, fehler = versuche(lambda: (len(SlaAuswertung(8, 90)), bool(SlaAuswertung(8, 90))))
assert ergebnis == (0, True), (
    f"Neue SlaAuswertung(8, 90): erwartet len 0 und bool True, bekommen {ergebnis!r} {fehler or ''}.\n"
    "Tipp: Ohne Tickets ist nichts verletzt. Mit __bool__ fragt Python __len__ gar nicht; teilen Sie nicht durch "
    "len(self), dann gibt es auch keinen ZeroDivisionError."
)

# SlaAuswertung: eine Dauer genau gleich der Frist ist eingehalten
ergebnis, fehler = versuche(lambda: bool(sla_mit(8, 100, [8, 8.0, 3])))
assert ergebnis is True, (
    f"SlaAuswertung(8, 100) mit den Dauern 8, 8.0, 3: bool ergibt {ergebnis!r} {fehler or ''}, erwartet war True.\n"
    "Tipp: Eine Dauer genau gleich der Frist zählt als eingehalten (dauer <= frist)."
)

# SlaAuswertung: genau die Zielquote reicht (9 von 10 bei 90 %)
ergebnis, fehler = versuche(lambda: bool(sla_mit(8, 90, [1] * 9 + [9])))
assert ergebnis is True, (
    f"SlaAuswertung(8, 90) mit 9 Dauern in der Frist und einer darüber: bool ergibt {ergebnis!r} {fehler or ''}, "
    "erwartet war True (genau 90 % reichen).\nTipp: Vergleichen Sie mit >= und ohne Kommazahlen: 100 * in_frist >= zielprozent * anzahl."
)

# SlaAuswertung: knapp darunter reicht nicht (8 von 9 bei 90 %)
ergebnis, fehler = versuche(lambda: bool(sla_mit(8, 90, [1] * 8 + [9])))
assert ergebnis is False, (
    f"SlaAuswertung(8, 90) mit 8 von 9 Dauern in der Frist (88,9 %): bool ergibt {ergebnis!r} {fehler or ''}, erwartet war False."
)

# SlaAuswertung: Ziel 0 % ist immer erfüllt, Ziel 100 % verträgt keinen Verstoß
ergebnis, fehler = versuche(lambda: (bool(sla_mit(1, 0, [500, 10000])), bool(sla_mit(720, 100, [0, 720, 720.5]))))
assert ergebnis == (True, False), (
    "SlaAuswertung(1, 0) mit 500 und 10000 sowie SlaAuswertung(720, 100) mit 0, 720, 720.5: "
    f"erwartet (True, False), bekommen {ergebnis!r} {fehler or ''}."
)

# SlaAuswertung in Bedingungen: if, not, and
gut = sla_mit(8, 50, [1, 20])
schlecht = sla_mit(8, 51, [1, 20])
ergebnis, fehler = versuche(lambda: ("gut" if gut else "schlecht", not schlecht, bool(gut and schlecht)))
assert ergebnis == ("gut", True, False), (
    "Mit den Dauern 1 und 20 bei Frist 8: Ziel 50 % ist eingehalten, Ziel 51 % nicht. Erwartet "
    f"('gut', True, False) für if, not und and; bekommen {ergebnis!r} {fehler or ''}."
)

# Viele zufällige Abläufe für beide Klassen
zufall = Zufall(5023)
for runde in range(300):
    liste_test = Ticketliste()
    offen = set()
    schritte = []
    for _ in range(zufall.randint(0, 12)):
        nummer = zufall.randint(1, 6)
        if zufall.random() < 0.6:
            liste_test.oeffnen(nummer)
            offen.add(nummer)
            schritte.append(f"oeffnen({nummer})")
        else:
            liste_test.schliessen(nummer)
            offen.discard(nummer)
            schritte.append(f"schliessen({nummer})")
    ergebnis, fehler = versuche(lambda: (len(liste_test), bool(liste_test)))
    assert ergebnis == (len(offen), len(offen) > 0), (
        f"Ticketliste nach {', '.join(schritte) or 'nichts'}: erwartet (len, bool) = ({len(offen)}, {len(offen) > 0}), "
        f"bekommen {ergebnis!r} {fehler or ''}."
    )
    frist = zufall.randint(1, 20)
    ziel = zufall.randint(0, 100)
    dauern = [zufall.choice([zufall.randint(0, 30), zufall.uniform(0, 30)]) for _ in range(zufall.randint(0, 8))]
    # Vergleichslösung über Anteile mit Brüchen statt Zählen
    eingehalten = [dauer for dauer in dauern if not dauer > frist]
    erwartet = (len(dauern), not dauern or len(eingehalten) / len(dauern) * 100 >= ziel - 1e-9)
    ergebnis, fehler = versuche(lambda: (len(sla_mit(frist, ziel, dauern)), bool(sla_mit(frist, ziel, dauern))))
    assert ergebnis == erwartet, (
        f"SlaAuswertung({frist}, {ziel}) mit den Dauern {dauern}: erwartet (len, bool) = {erwartet}, "
        f"bekommen {ergebnis!r} {fehler or ''}."
    )

# Obere Grenze: 100 000 Tickets, jedes zweite geschlossen
gross = Ticketliste()
for nummer in range(1, 100001):
    gross.oeffnen(nummer * 10000)
for nummer in range(2, 100001, 2):
    gross.schliessen(nummer * 10000)
ergebnis, fehler = versuche(lambda: (len(gross), bool(gross)))
assert ergebnis == (50000, True), f"100 000 Tickets, jedes zweite geschlossen: erwartet (50000, True), bekommen {ergebnis!r} {fehler or ''}."

# Obere Grenze: 100 000 Dauern, davon 90 000 genau an der Frist
gross_sla = sla_mit(720, 90, [720] * 90000 + [10000] * 10000)
ergebnis, fehler = versuche(lambda: (len(gross_sla), bool(gross_sla)))
assert ergebnis == (100000, True), (
    f"100 000 Dauern, davon 90 000 genau an der Frist: erwartet (100000, True), bekommen {ergebnis!r} {fehler or ''}."
)

# Obere Grenze: 89 999 von 100 000 in der Frist sind knapp unter 90 %
knapp_sla = sla_mit(720, 90, [720] * 89999 + [10000] * 10001)
ergebnis, fehler = versuche(lambda: bool(knapp_sla))
assert ergebnis is False, (
    f"100 000 Dauern, davon 89 999 in der Frist (89,999 %), Ziel 90 %: bool ergibt {ergebnis!r} {fehler or ''}, "
    "erwartet war False.\nTipp: Rechnen Sie genau: 100 * in_frist >= zielprozent * anzahl."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("1 True\n3 False"), f'Erwartete Ausgabe:\n1 True\n3 False\nIhr Programm:\n{AUSGABE}'
