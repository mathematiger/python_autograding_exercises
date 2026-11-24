# Automatisch erzeugt aus lehrkraft/muster/4_084_prozesskette.py - nicht von Hand ändern.
# vorlage-hash: 0f8483501c226780
# text-hash: 3984baf3740f6fbb
# thema: datenstrukturen
# inhalt: Verkettete Liste mit Iterator

BEISPIEL = [("Annahme", 5), ("Diagnose", 20), ("Reparatur", 45)]


def von_hand(paare):
    """Baut eine Kette ohne die Methoden der SuS, indem es die Schritte selbst verknüpft."""
    kette = Prozesskette()
    vorher = None
    for name, dauer in paare:
        schritt = Schritt(name, dauer)
        if vorher is None:
            kette.erster = schritt
        else:
            vorher.naechster = schritt
        vorher = schritt
    kette.letzter = vorher
    kette.anzahl = len(paare)
    return kette


def ablesen(kette):
    """Liest die Kette über die Zeiger ab, ohne __iter__ der SuS; bricht nach 200 000 Schritten ab (Kreis)."""
    paare = []
    aktuell = kette.erster
    while aktuell is not None and len(paare) <= 200_000:
        paare.append((aktuell.name, aktuell.dauer))
        aktuell = aktuell.naechster
    return paare


def stimmig(kette):
    """Prüft, ob erster, letzter und anzahl zu den Zeigern passen; liefert einen Fehlertext oder None."""
    paare = ablesen(kette)
    if kette.anzahl != len(paare):
        return f"anzahl ist {kette.anzahl!r}, in der Kette stehen aber {len(paare)} Schritte."
    if not paare:
        if kette.erster is not None or kette.letzter is not None:
            return "Die Kette ist leer, aber erster oder letzter ist nicht None."
        return None
    if kette.letzter is None or kette.letzter.naechster is not None or kette.letzter.name != paare[-1][0]:
        name = getattr(kette.letzter, "name", None)
        return f"letzter zeigt auf {name!r}, der letzte Schritt der Kette ist aber {paare[-1][0]!r}."
    return None


def fehler_bei(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Ausnahme oder None)."""
    try:
        return aufruf(), None
    except Exception as ausnahme:
        return None, ausnahme


def absturz(ausnahme):
    """Ergänzt eine Meldung um die Ausnahme, falls es eine gab."""
    return f"\nDer Aufruf löst {type(ausnahme).__name__}: {ausnahme} aus." if ausnahme else ""


# anhaengen: der erste Schritt in einer leeren Kette
kette = Prozesskette()
_, ausnahme = fehler_bei(lambda: kette.anhaengen("Annahme", 5))
assert ablesen(kette) == [("Annahme", 5)] and kette.letzter is kette.erster, (
    f"Nach anhaengen('Annahme', 5) an eine leere Kette ist erster {getattr(kette.erster, 'name', None)!r} und letzter "
    f"{getattr(kette.letzter, 'name', None)!r}; erwartet war beide Male derselbe Schritt 'Annahme'." + absturz(ausnahme)
    + "\nTipp: Ist die Kette leer, wird der neue Schritt erster und letzter zugleich."
)

# anhaengen: das Beispiel, drei Schritte in dieser Reihenfolge
kette = Prozesskette()
_, ausnahme = fehler_bei(lambda: [kette.anhaengen(name, dauer) for name, dauer in BEISPIEL])
assert ablesen(kette) == BEISPIEL, (
    f"Nach dreimal anhaengen steht in der Kette {ablesen(kette)!r}, erwartet war {BEISPIEL!r}." + absturz(ausnahme)
    + "\nTipp: Hängen Sie den neuen Schritt an self.letzter an (self.letzter.naechster = neu) und setzen Sie dann "
    "self.letzter = neu."
)

# anhaengen: letzter und anzahl stimmen
kette = Prozesskette()
_, ausnahme = fehler_bei(lambda: [kette.anhaengen(name, dauer) for name, dauer in BEISPIEL])
problem = stimmig(kette)
assert problem is None and len(ablesen(kette)) == 3, f"Nach dreimal anhaengen: {problem or ablesen(kette)}" + absturz(ausnahme)

# __len__ gibt die Anzahl zurück
ergebnis, ausnahme = fehler_bei(lambda: (len(von_hand(BEISPIEL)), len(von_hand([]))))
assert ergebnis == (3, 0), f"len() ergibt für drei Schritte und eine leere Kette {ergebnis!r}, erwartet war (3, 0)." + absturz(ausnahme)

# __iter__: das Beispiel
ergebnis, ausnahme = fehler_bei(lambda: list(von_hand(BEISPIEL)))
assert ergebnis == BEISPIEL, (
    f"list(kette) ergibt {ergebnis!r}, erwartet war {BEISPIEL!r}." + absturz(ausnahme)
    + "\nTipp: Beginnen Sie bei self.erster, liefern Sie mit yield (aktuell.name, aktuell.dauer) und gehen Sie mit "
    "aktuell = aktuell.naechster weiter, bis aktuell None ist."
)

# __iter__: die leere Kette liefert nichts
ergebnis, ausnahme = fehler_bei(lambda: list(von_hand([])))
assert ergebnis == [], f"list() einer leeren Kette ergibt {ergebnis!r}, erwartet war []." + absturz(ausnahme)

# __iter__ ist eine Generatormethode, jedes for beginnt von vorn
kette = von_hand(BEISPIEL)
ergebnis, ausnahme = fehler_bei(lambda: (type(iter(kette)).__name__, list(kette), list(kette)))
assert ergebnis == ("generator", BEISPIEL, BEISPIEL), (
    f"iter(kette) ist vom Typ {ergebnis and ergebnis[0]!r} und zwei Durchläufe ergeben {ergebnis and ergebnis[1:]!r}; "
    "erwartet war ein Generator und beide Male die ganze Kette." + absturz(ausnahme)
)

# durchlaufzeit: die Summe der Dauern
ergebnis, ausnahme = fehler_bei(von_hand(BEISPIEL).durchlaufzeit)
assert ergebnis == 70, f"durchlaufzeit() ergibt {ergebnis!r}, erwartet war 5 + 20 + 45 = 70." + absturz(ausnahme)

# durchlaufzeit: leere Kette
ergebnis, ausnahme = fehler_bei(von_hand([]).durchlaufzeit)
assert ergebnis == 0, f"durchlaufzeit() einer leeren Kette ergibt {ergebnis!r}, erwartet war 0." + absturz(ausnahme)

# einfuegen_nach: das Beispiel, in der Mitte
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: kette.einfuegen_nach("Diagnose", "Datensicherung", 30))
erwartet = [("Annahme", 5), ("Diagnose", 20), ("Datensicherung", 30), ("Reparatur", 45)]
assert ablesen(kette) == erwartet, (
    f"Nach einfuegen_nach('Diagnose', 'Datensicherung', 30) steht in der Kette {ablesen(kette)!r}, erwartet war "
    f"{erwartet!r}." + absturz(ausnahme)
    + "\nTipp: Erst neu.naechster = aktuell.naechster, dann aktuell.naechster = neu; andersherum geht der Rest verloren."
)

# einfuegen_nach: anzahl stimmt danach
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: kette.einfuegen_nach("Annahme", "Sichtprüfung", 3))
problem = stimmig(kette)
assert problem is None and ablesen(kette)[1] == ("Sichtprüfung", 3), (
    f"Nach einfuegen_nach('Annahme', 'Sichtprüfung', 3): {problem or ablesen(kette)}" + absturz(ausnahme)
)

# einfuegen_nach: hinter dem letzten Schritt wird der neue der letzte
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: kette.einfuegen_nach("Reparatur", "Funktionstest", 15))
problem = stimmig(kette)
assert problem is None and ablesen(kette)[-1] == ("Funktionstest", 15), (
    f"Nach einfuegen_nach hinter dem letzten Schritt: {problem or ablesen(kette)}" + absturz(ausnahme)
    + "\nTipp: Fügen Sie hinter self.letzter ein, muss self.letzter auf den neuen Schritt zeigen."
)

# einfuegen_nach: danach anhaengen hängt hinter den neuen letzten Schritt
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: (kette.einfuegen_nach("Reparatur", "Funktionstest", 15), kette.anhaengen("Rückgabe", 5)))
erwartet = BEISPIEL + [("Funktionstest", 15), ("Rückgabe", 5)]
assert ablesen(kette) == erwartet, (
    f"Nach einfuegen_nach hinter 'Reparatur' und anhaengen('Rückgabe', 5) steht in der Kette {ablesen(kette)!r}, "
    f"erwartet war {erwartet!r}." + absturz(ausnahme)
)

# einfuegen_nach: unbekannter Vorgänger löst KeyError aus und ändert nichts
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: kette.einfuegen_nach("Lackierung", "Trocknen", 60))
assert isinstance(ausnahme, KeyError) and ablesen(kette) == BEISPIEL and kette.anzahl == 3, (
    f"einfuegen_nach('Lackierung', …) löst {type(ausnahme).__name__ if ausnahme else 'nichts'} aus, danach steht in "
    f"der Kette {ablesen(kette)!r} mit anzahl {kette.anzahl!r}; erwartet war KeyError und eine unveränderte Kette.\n"
    "Tipp: Suchen Sie zuerst den Vorgänger und ändern Sie erst danach etwas."
)

# einfuegen_nach: in einer leeren Kette gibt es keinen Vorgänger
kette = von_hand([])
_, ausnahme = fehler_bei(lambda: kette.einfuegen_nach("Annahme", "Diagnose", 20))
assert isinstance(ausnahme, KeyError) and stimmig(kette) is None and kette.anzahl == 0, (
    f"einfuegen_nach in einer leeren Kette löst {type(ausnahme).__name__ if ausnahme else 'nichts'} aus; "
    "erwartet war KeyError, und die Kette bleibt leer."
)

# entfernen: ein Schritt in der Mitte, gibt die Dauer zurück
kette = von_hand(BEISPIEL)
ergebnis, ausnahme = fehler_bei(lambda: kette.entfernen("Diagnose"))
erwartet = [("Annahme", 5), ("Reparatur", 45)]
assert ergebnis == 20 and ablesen(kette) == erwartet, (
    f"entfernen('Diagnose') gibt {ergebnis!r} zurück, danach steht in der Kette {ablesen(kette)!r}; erwartet war 20 "
    f"und {erwartet!r}." + absturz(ausnahme)
    + "\nTipp: Laufen Sie mit vorher und aktuell durch die Kette und setzen Sie vorher.naechster = aktuell.naechster."
)

# entfernen: anzahl stimmt danach
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: kette.entfernen("Diagnose"))
problem = stimmig(kette)
assert problem is None and len(ablesen(kette)) == 2, f"Nach entfernen('Diagnose'): {problem or ablesen(kette)}" + absturz(ausnahme)

# entfernen: das Beispiel, der erste Schritt
kette = von_hand(BEISPIEL)
ergebnis, ausnahme = fehler_bei(lambda: kette.entfernen("Annahme"))
problem = stimmig(kette)
assert ergebnis == 5 and problem is None and ablesen(kette) == BEISPIEL[1:], (
    f"entfernen('Annahme') gibt {ergebnis!r} zurück, danach: {problem or ablesen(kette)}; erwartet war 5 und "
    f"{BEISPIEL[1:]!r}." + absturz(ausnahme)
    + "\nTipp: Hat der Schritt keinen Vorgänger, wird sein Nachfolger der neue self.erster."
)

# entfernen: der letzte Schritt, danach zeigt letzter auf den Vorgänger
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: (kette.entfernen("Reparatur"), kette.anhaengen("Rückgabe", 5)))
erwartet = [("Annahme", 5), ("Diagnose", 20), ("Rückgabe", 5)]
assert ablesen(kette) == erwartet and stimmig(kette) is None, (
    f"Nach entfernen('Reparatur') und anhaengen('Rückgabe', 5) steht in der Kette {ablesen(kette)!r}, erwartet war "
    f"{erwartet!r}." + absturz(ausnahme)
    + "\nTipp: Entfernen Sie den letzten Schritt, muss self.letzter auf seinen Vorgänger zeigen."
)

# entfernen: der einzige Schritt, danach ist die Kette leer
kette = von_hand([("Annahme", 5)])
_, ausnahme = fehler_bei(lambda: kette.entfernen("Annahme"))
problem = stimmig(kette)
assert problem is None and ablesen(kette) == [], f"Nach entfernen des einzigen Schritts: {problem or ablesen(kette)}" + absturz(ausnahme)

# entfernen: und danach wieder anhaengen
kette = von_hand([("Annahme", 5)])
_, ausnahme = fehler_bei(lambda: (kette.entfernen("Annahme"), kette.anhaengen("Diagnose", 20)))
assert ablesen(kette) == [("Diagnose", 20)] and stimmig(kette) is None, (
    f"Nach entfernen des einzigen Schritts und anhaengen('Diagnose', 20) steht in der Kette {ablesen(kette)!r}, "
    "erwartet war [('Diagnose', 20)]." + absturz(ausnahme)
)

# entfernen: unbekannter Name löst KeyError aus und ändert nichts
kette = von_hand(BEISPIEL)
_, ausnahme = fehler_bei(lambda: kette.entfernen("Lackierung"))
assert isinstance(ausnahme, KeyError) and ablesen(kette) == BEISPIEL and stimmig(kette) is None, (
    f"entfernen('Lackierung') löst {type(ausnahme).__name__ if ausnahme else 'nichts'} aus, danach steht in der "
    f"Kette {ablesen(kette)!r}; erwartet war KeyError und eine unveränderte Kette."
)

# entfernen: in einer leeren Kette
kette = von_hand([])
_, ausnahme = fehler_bei(lambda: kette.entfernen("Annahme"))
assert isinstance(ausnahme, KeyError) and stimmig(kette) is None, (
    f"entfernen in einer leeren Kette löst {type(ausnahme).__name__ if ausnahme else 'nichts'} aus; erwartet war KeyError."
)

# Das Beispiel aus der Aufgabe von Anfang bis Ende
kette = Prozesskette()


def beispiel():
    """Spielt das Beispiel aus dem Aufgabentext durch."""
    for name, dauer in BEISPIEL:
        kette.anhaengen(name, dauer)
    kette.einfuegen_nach("Diagnose", "Datensicherung", 30)
    return list(kette), kette.entfernen("Annahme"), len(kette), kette.durchlaufzeit()


ergebnis, ausnahme = fehler_bei(beispiel)
erwartet = ([("Annahme", 5), ("Diagnose", 20), ("Datensicherung", 30), ("Reparatur", 45)], 5, 3, 95)
assert ergebnis == erwartet, f"Das Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(ausnahme)

# Die Schritte stehen nur in der Kette, nicht zusätzlich in einer Liste oder einem Dictionary
kette = Prozesskette()
_, ausnahme = fehler_bei(lambda: [kette.anhaengen(name, dauer) for name, dauer in BEISPIEL])
sammlungen = [name for name, wert in vars(kette).items() if isinstance(wert, (list, dict, set, tuple))]
assert not sammlungen, (
    f"Ihre Kette speichert zusätzlich {sammlungen}. Verknüpfen Sie die Schritte nur über naechster und merken Sie "
    "sich erster und letzter."
)

zufall = Zufall(4084)

# Viele zufällige Änderungen im Vergleich mit einer Python-Liste
for runde in range(60):
    kette = Prozesskette()
    vergleich = []
    protokoll = []
    nummer = 0
    for _ in range(zufall.randint(0, 25)):
        art = zufall.choice(["anhaengen", "anhaengen", "einfuegen", "entfernen", "entfernen_fehlt"])
        nummer += 1
        name, dauer = f"S{nummer}", zufall.randint(0, 10_000)
        if art == "anhaengen" or not vergleich and art == "einfuegen":
            protokoll.append(f"anhaengen({name!r}, {dauer})")
            _, ausnahme = fehler_bei(lambda: kette.anhaengen(name, dauer))
            vergleich.append((name, dauer))
        elif art == "einfuegen":
            stelle = zufall.randrange(len(vergleich))
            protokoll.append(f"einfuegen_nach({vergleich[stelle][0]!r}, {name!r}, {dauer})")
            _, ausnahme = fehler_bei(lambda: kette.einfuegen_nach(vergleich[stelle][0], name, dauer))
            vergleich.insert(stelle + 1, (name, dauer))
        elif art == "entfernen" and vergleich:
            stelle = zufall.randrange(len(vergleich))
            protokoll.append(f"entfernen({vergleich[stelle][0]!r})")
            ergebnis, ausnahme = fehler_bei(lambda: kette.entfernen(vergleich[stelle][0]))
            assert ergebnis == vergleich[stelle][1], (
                f"Nach {', '.join(protokoll)} gibt der letzte Aufruf {ergebnis!r} zurück, erwartet war "
                f"{vergleich[stelle][1]!r}." + absturz(ausnahme)
            )
            vergleich.pop(stelle)
        else:
            protokoll.append(f"entfernen('fehlt') → KeyError")
            _, ausnahme = fehler_bei(lambda: kette.entfernen("fehlt"))
            assert isinstance(ausnahme, KeyError), f"Nach {', '.join(protokoll)}: kein KeyError."
            ausnahme = None
        problem = stimmig(kette)
        assert ausnahme is None and ablesen(kette) == vergleich and problem is None, (
            f"Nach {', '.join(protokoll)} steht in der Kette {ablesen(kette)!r}, erwartet war {vergleich!r}. "
            f"{problem or ''}" + absturz(ausnahme)
        )
    ergebnis, ausnahme = fehler_bei(lambda: (list(kette), len(kette), kette.durchlaufzeit()))
    erwartet = (vergleich, len(vergleich), sum(dauer for _, dauer in vergleich))
    assert ergebnis == erwartet, (
        f"Nach {', '.join(protokoll)} ergeben list(kette), len(kette) und durchlaufzeit() {ergebnis!r}, erwartet war "
        f"{erwartet!r}." + absturz(ausnahme)
    )


def haenge_an(anzahl):
    """Hängt anzahl Schritte an eine neue Kette."""
    kette = Prozesskette()
    for nummer in range(anzahl):
        kette.anhaengen(f"S{nummer}", 1)
    return kette


# Laufzeit: anhaengen braucht O(1), egal wie lang die Kette ist
klein, schritte_klein = zaehle_schritte(haenge_an, 500)
gross, schritte_gross = zaehle_schritte(haenge_an, 2000)
assert len(ablesen(klein)) == 500 and len(ablesen(gross)) == 2000 and schritte_gross <= 5 * schritte_klein + 100, (
    f"500 Schritte anzuhängen braucht {schritte_klein} Schritte, 2000 anzuhängen {schritte_gross}. Bei O(1) je "
    "anhaengen wäre es etwa das Vierfache, Ihre Lösung wächst schneller.\n"
    "Tipp: Laufen Sie nicht bis zum Ende der Kette, sondern hängen Sie an self.letzter an."
)

# Laufzeit: __len__ braucht O(1)
kette = von_hand([(f"S{nummer}", 1) for nummer in range(10_000)])
ergebnis, schritte = zaehle_schritte(len, kette)
_, schritte_methode = zaehle_schritte(kette.__len__)
assert ergebnis == 10_000 and schritte_methode <= 5, (
    f"len(kette) mit 10000 Schritten ergibt {ergebnis!r} und braucht {schritte_methode} Schritte; erwartet waren "
    "10000 und höchstens 5 Schritte.\nTipp: Geben Sie self.anzahl zurück, statt die Kette abzuzählen."
)

# Obere Grenze: 100000 Schritte anhängen, vorn einfügen und durchlaufen
kette = von_hand([])


def gross():
    """Hängt 100000 Schritte an, fügt vorn einen ein, entfernt den ersten und den letzten."""
    for nummer in range(100_000):
        kette.anhaengen(f"S{nummer}", nummer % 7)
    kette.einfuegen_nach("S0", "neu", 3)
    kette.entfernen("S0")
    return len(kette), kette.durchlaufzeit(), next(iter(kette))


ergebnis, ausnahme = fehler_bei(gross)
erwartet = (100_000, sum(nummer % 7 for nummer in range(1, 100_000)) + 3, ("neu", 3))
assert ergebnis == erwartet, f"Mit 100000 Schritten ergibt das {ergebnis!r}, erwartet war {erwartet!r}." + absturz(ausnahme)
