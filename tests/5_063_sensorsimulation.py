# Automatisch erzeugt aus lehrkraft/muster/5_063_sensorsimulation.py - nicht von Hand ändern.
# vorlage-hash: 7a17bd9a19c6c6e6
# text-hash: b9f430b7bd5f011e
# thema: programmaufbau
# inhalt: Ereignisgesteuerte Simulation

BEISPIEL = [(10, [(4, "s1"), (8, "s1")]), (20, [(12, "s1"), (15, "s2")]), (30, [(30, "s2")])]


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    if fehler and "not an iterator" in fehler:
        return f"\nDer Aufruf löst {fehler} aus.\nTipp: lauf muss ein Generator sein, also yield enthalten."
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


class Wecker:
    """Ein Testgerät, das nacheinander die Wartezeiten aus wartezeiten liefert und mitschreibt, wann es dran war."""

    def __init__(self, name, wartezeiten, protokoll):
        """Merkt sich Name, Wartezeiten und die gemeinsame Protokollliste."""
        self.name = name
        self.wartezeiten = wartezeiten
        self.protokoll = protokoll

    def lauf(self, sim):
        """Schreibt (jetzt, name) ins Protokoll und wartet jeweils die nächste Wartezeit."""
        for wartezeit in self.wartezeiten:
            self.protokoll.append((sim.jetzt, self.name))
            yield wartezeit
        self.protokoll.append((sim.jetzt, self.name + " fertig"))


def wecker_lauf(endzeit, *geraete):
    """Startet für jedes Paar (name, wartezeiten) einen Wecker, lässt bis endzeit laufen; liefert (protokoll, jetzt)."""
    protokoll = []
    sim = Simulation(endzeit)
    for name, wartezeiten in geraete:
        sim.starte(Wecker(name, wartezeiten, protokoll))
    sim.laufe()
    return protokoll, sim.jetzt


def wecker_vergleich(endzeit, geraete):
    """Vergleichslösung für wecker_lauf: eine einfache Liste, aus der jedes Mal das Minimum geholt wird."""
    protokoll = []
    offen = []
    zaehler = 0
    for name, wartezeiten in geraete:
        offen.append((0, zaehler, name, list(wartezeiten), 0))
        zaehler += 1
    while offen and min(offen)[0] <= endzeit:
        zeit, _, name, wartezeiten, schritt = min(offen)
        offen.remove(min(offen))
        if schritt < len(wartezeiten):
            protokoll.append((zeit, name))
            offen.append((zeit + wartezeiten[schritt], zaehler, name, wartezeiten, schritt + 1))
            zaehler += 1
        else:
            protokoll.append((zeit, name + " fertig"))
    return protokoll


def uploads_vergleich(knoten, takt, endzeit):
    """Vergleichslösung für simuliere ohne Simulation: berechnet Sendezeiten und Upload-Zeiten direkt.

    Bei gleicher Zeit wurde früher eingeplant, wer das längere Intervall hat (bei gleichem Intervall
    das Gateway vor den Knoten, die Knoten in ihrer Reihenfolge).
    """
    nachrichten = []
    for stelle, (name, intervall, batterie, verbrauch) in enumerate(knoten):
        for nummer in range(1, min(batterie // verbrauch, endzeit // intervall) + 1):
            zeit = nummer * intervall
            if zeit % takt == 0 and intervall > takt:
                upload = zeit
            else:
                upload = (zeit // takt + 1) * takt
            nachrichten.append((upload, zeit, -intervall, stelle, name))
    nachrichten.sort()
    uploads = []
    for upload, zeit, _, _, name in nachrichten:
        if upload > endzeit:
            break
        if not uploads or uploads[-1][0] != upload:
            uploads.append((upload, []))
        uploads[-1][1].append((zeit, name))
    return uploads


def beispiel():
    """Baut das Beispiel aus dem Aufgabentext und lässt es laufen; liefert (gateway, s1, s2, sim)."""
    gateway = Gateway("gateway", takt=10)
    s1 = Sensorknoten("s1", intervall=4, batterie=10, verbrauch=3, gateway=gateway)
    s2 = Sensorknoten("s2", intervall=15, batterie=100, verbrauch=1, gateway=gateway)
    sim = Simulation(endzeit=30)
    sim.starte(gateway)
    sim.starte(s1)
    sim.starte(s2)
    sim.laufe()
    return gateway, s1, s2, sim


# Ereignis: früher kommt vor später
ergebnis, fehler = rufe(lambda: (Ereignis(3, 9, None) < Ereignis(5, 1, None), Ereignis(5, 1, None) < Ereignis(3, 9, None)))
assert ergebnis == (True, False), (
    f"Ereignis(3, 9, …) < Ereignis(5, 1, …) und umgekehrt ergeben {ergebnis!r}, erwartet war (True, False): "
    "zuerst wird nach zeit verglichen.\nTipp: @dataclass(order=True) vergleicht die Felder in der Reihenfolge, in der "
    "sie in der Klasse stehen." + absturz(fehler)
)

# Ereignis: bei gleicher Zeit entscheidet die nummer
ergebnis, fehler = rufe(lambda: (Ereignis(5, 1, None) < Ereignis(5, 2, None), Ereignis(5, 2, None) < Ereignis(5, 1, None)))
assert ergebnis == (True, False), (
    f"Ereignis(5, 1, …) < Ereignis(5, 2, …) und umgekehrt ergeben {ergebnis!r}, erwartet war (True, False)." + absturz(fehler)
)

# Ereignis: der Generator wird nie verglichen
def leer():
    """Ein Generator ohne Werte für den Vergleichstest."""
    yield from ()


ergebnis, fehler = rufe(lambda: (Ereignis(5, 1, leer()) <= Ereignis(5, 1, leer()), Ereignis(5, 1, leer()) == Ereignis(5, 1, leer())))
assert ergebnis == (True, True), (
    f"Zwei Ereignisse mit zeit 5, nummer 1 und verschiedenen Generatoren ergeben bei <= und == {ergebnis!r}, erwartet "
    "war (True, True).\nTipp: ablauf: … = field(compare=False) nimmt das Feld vom Vergleich aus; Generatoren lassen "
    "sich nicht ordnen." + absturz(fehler)
)

# Geraet: Sensorknoten, Gateway und eigene Klassen erfüllen das Protokoll ohne Vererbung
ergebnis, fehler = rufe(lambda: (
    isinstance(Gateway("g", 5), Geraet),
    isinstance(Sensorknoten("s", 1, 1, 1, Gateway("g", 5)), Geraet),
    isinstance(Wecker("w", [], []), Geraet),
))
assert ergebnis == (True, True, True), (
    f"isinstance(…, Geraet) ergibt für ein Gateway, einen Sensorknoten und eine Klasse mit name und lauf {ergebnis!r}, "
    "erwartet war (True, True, True).\nTipp: Schreiben Sie in den Rumpf von Geraet die Annotation name: str und eine "
    "Methode lauf(self, sim) mit ... als Rumpf." + absturz(fehler)
)

# Geraet: ohne name oder ohne lauf ist es kein Gerät
class NurLauf:
    """Hat lauf, aber keinen name."""

    def lauf(self, sim):
        """Liefert nichts."""
        yield from ()


class NurName:
    """Hat name, aber kein lauf."""

    name = "nur name"


ergebnis, fehler = rufe(lambda: (isinstance(NurLauf(), Geraet), isinstance(NurName(), Geraet), isinstance("text", Geraet)))
assert ergebnis == (False, False, False), (
    f"isinstance(…, Geraet) ergibt für ein Objekt nur mit lauf, eines nur mit name und einen Text {ergebnis!r}, "
    "erwartet war (False, False, False): Ein Gerät braucht beides." + absturz(fehler)
)

# Simulation: ein Gerät wird nach seinen Wartezeiten wieder aufgeweckt
ergebnis, fehler = rufe(lambda: wecker_lauf(100, ("w", [3, 5, 2])))
assert ergebnis is not None and ergebnis[0] == [(0, "w"), (3, "w"), (8, "w"), (10, "w fertig")], (
    f"Ein Gerät mit den Wartezeiten 3, 5, 2 ist zu den Zeiten {ergebnis[0] if ergebnis else None} drangekommen, "
    "erwartet war [(0, 'w'), (3, 'w'), (8, 'w'), (10, 'w fertig')].\nTipp: starte plant den Generator für jetzt "
    "ein; laufe setzt jetzt auf die Zeit des Ereignisses und plant ihn für jetzt + Wartezeit neu ein." + absturz(fehler)
)

# Simulation: ein fertiges Gerät (StopIteration) wird nicht neu eingeplant
ergebnis, fehler = rufe(lambda: wecker_lauf(100, ("kurz", [1]), ("lang", [4, 4])))
assert ergebnis is not None and ergebnis[0] == [(0, "kurz"), (0, "lang"), (1, "kurz fertig"), (4, "lang"), (8, "lang fertig")], (
    f"Zwei Geräte mit den Wartezeiten [1] und [4, 4] ergeben das Protokoll {ergebnis[0] if ergebnis else None}, "
    "erwartet war [(0, 'kurz'), (0, 'lang'), (1, 'kurz fertig'), (4, 'lang'), (8, 'lang fertig')].\n"
    "Tipp: Fangen Sie StopIteration ab und planen Sie dieses Gerät dann nicht neu ein." + absturz(fehler)
)

# Simulation: das früheste Ereignis zuerst, auch wenn es später eingeplant wurde
ergebnis, fehler = rufe(lambda: wecker_lauf(100, ("langsam", [9]), ("schnell", [2, 2, 2])))
assert ergebnis is not None and ergebnis[0] == [
    (0, "langsam"), (0, "schnell"), (2, "schnell"), (4, "schnell"), (6, "schnell fertig"), (9, "langsam fertig"),
], (
    f"Zwei Geräte mit den Wartezeiten [9] und [2, 2, 2] ergeben das Protokoll {ergebnis[0] if ergebnis else None}, "
    "erwartet war der Zeit nach [(0, 'langsam'), (0, 'schnell'), (2, 'schnell'), (4, 'schnell'), "
    "(6, 'schnell fertig'), (9, 'langsam fertig')].\nTipp: Nehmen Sie mit heapq.heappop immer das kleinste Ereignis "
    "heraus." + absturz(fehler)
)

# Simulation: Ereignisse genau zur endzeit laufen noch, spätere nicht; danach ist jetzt = endzeit
ergebnis, fehler = rufe(lambda: wecker_lauf(10, ("w", [4, 6, 1]), ("x", [11])))
assert ergebnis == ([(0, "w"), (0, "x"), (4, "w"), (10, "w")], 10), (
    f"Mit endzeit 10 und Geräten mit den Wartezeiten [4, 6, 1] und [11] ergeben Protokoll und jetzt {ergebnis!r}, "
    "erwartet war ([(0, 'w'), (0, 'x'), (4, 'w'), (10, 'w')], 10): Das Ereignis zur Zeit 10 läuft noch, die zu den "
    "Zeiten 11 nicht." + absturz(fehler)
)

# Simulation: endzeit 0 und eine Simulation ohne Geräte
ergebnis, fehler = rufe(lambda: (wecker_lauf(0, ("w", [1])), wecker_lauf(25)))
assert ergebnis == (([(0, "w")], 0), ([], 25)), (
    f"wecker_lauf mit endzeit 0 und einem Gerät sowie mit endzeit 25 ohne Geräte ergibt {ergebnis!r}, erwartet war "
    "(([(0, 'w')], 0), ([], 25)): Auch ohne Ereignisse steht jetzt am Ende auf endzeit." + absturz(fehler)
)

# Simulation: bei gleicher Zeit in der Reihenfolge des Einplanens
ergebnis, fehler = rufe(lambda: wecker_lauf(100, ("a", [5, 5]), ("b", [10]), ("c", [5, 0, 5])))
assert ergebnis is not None and ergebnis[0] == [
    (0, "a"), (0, "b"), (0, "c"), (5, "a"), (5, "c"), (5, "c"), (10, "b fertig"), (10, "a fertig"), (10, "c fertig"),
], (
    f"Drei Geräte a, b, c mit den Wartezeiten [5, 5], [10] und [5, 0, 5] ergeben das Protokoll "
    f"{ergebnis[0] if ergebnis else None},\nerwartet war [(0, 'a'), (0, 'b'), (0, 'c'), (5, 'a'), (5, 'c'), (5, 'c'), "
    "(10, 'b fertig'), (10, 'a fertig'), (10, 'c fertig')]: Zur Zeit 10 kommt b zuerst, weil es schon zur Zeit 0 "
    "eingeplant wurde.\nTipp: nummer = next(self.zaehler) bei jedem plane, nicht einmal je Gerät." + absturz(fehler)
)

# Simulation: verwendet heapq für die Warteschlange
assert verwendet("heappush") and verwendet("heappop"), (
    "Ihr Programm ruft " + ("heapq.heappop" if verwendet("heappush") else "heapq.heappush") + " nicht auf. Die "
    "Warteschlange soll ein Heap sein: heappush in plane, heappop in laufe (siehe Hintergrund)."
)

# Sensorknoten: sendet alle intervall Sekunden an das Gateway
gateway = Gateway("gateway", 1000)


def nur_knoten():
    """Lässt einen Sensorknoten ohne laufendes Gateway bis 20 laufen; liefert den Puffer."""
    sim = Simulation(20)
    sim.starte(Sensorknoten("t1", 6, 100, 1, gateway))
    sim.laufe()
    return gateway.puffer


ergebnis, fehler = rufe(nur_knoten)
assert ergebnis == [(6, "t1"), (12, "t1"), (18, "t1")], (
    f"Ein Sensorknoten mit intervall 6 bis endzeit 20 hat dem Gateway {ergebnis!r} übergeben, erwartet war "
    "[(6, 't1'), (12, 't1'), (18, 't1')].\nTipp: Erst yield self.intervall, danach senden; die Zeit steht in sim.jetzt."
    + absturz(fehler)
)

# Sensorknoten: hört auf, wenn die Batterie nicht mehr reicht
gateway = Gateway("gateway", 1000)
knoten = Sensorknoten("t2", 5, 11, 4, gateway)


def bis_batterie_leer():
    """Lässt einen Knoten mit Batterie 11 und Verbrauch 4 bis 100 laufen; liefert (Puffer, Restbatterie)."""
    sim = Simulation(100)
    sim.starte(knoten)
    sim.laufe()
    return gateway.puffer, knoten.batterie


ergebnis, fehler = rufe(bis_batterie_leer)
assert ergebnis == ([(5, "t2"), (10, "t2")], 3), (
    f"Ein Knoten mit batterie 11, verbrauch 4 und intervall 5 sendet bis endzeit 100 {ergebnis[0] if ergebnis else None} "
    f"und hat danach batterie {ergebnis[1] if ergebnis else None}; erwartet waren [(5, 't2'), (10, 't2')] und 3: "
    "Mit 3 reicht es nicht mehr für eine Nachricht." + absturz(fehler)
)

# Sensorknoten: genau so viel Batterie wie eine Nachricht kostet, und zu wenig von Anfang an
gateway = Gateway("gateway", 1000)


def knapp():
    """Startet einen Knoten mit batterie = verbrauch und einen mit batterie 0; liefert den Puffer und beide Batterien."""
    sim = Simulation(100)
    genau, leer = Sensorknoten("genau", 7, 4, 4, gateway), Sensorknoten("leer", 3, 0, 1, gateway)
    sim.starte(genau)
    sim.starte(leer)
    sim.laufe()
    return gateway.puffer, genau.batterie, leer.batterie


ergebnis, fehler = rufe(knapp)
assert ergebnis == ([(7, "genau")], 0, 0), (
    f"Ein Knoten mit batterie 4 und verbrauch 4 und einer mit batterie 0 ergeben {ergebnis!r}, erwartet war "
    "([(7, 'genau')], 0, 0): Der erste sendet genau einmal, der zweite nie." + absturz(fehler)
)

# Gateway: lädt im Takt hoch, aber nur, wenn der Puffer nicht leer ist
gateway = Gateway("gateway", 10)


def nur_gateway():
    """Füllt den Puffer, lässt das Gateway bis 35 laufen; liefert (uploads, puffer)."""
    gateway.empfange((1, "a"))
    gateway.empfange((2, "b"))
    sim = Simulation(35)
    sim.starte(gateway)
    sim.laufe()
    return gateway.uploads, gateway.puffer


ergebnis, fehler = rufe(nur_gateway)
assert ergebnis == ([(10, [(1, "a"), (2, "b")])], []), (
    f"Ein Gateway mit takt 10 und zwei Nachrichten im Puffer ergibt bis endzeit 35 uploads und puffer {ergebnis!r}, "
    "erwartet war ([(10, [(1, 'a'), (2, 'b')])], []): Zu den Zeiten 20 und 30 ist der Puffer leer, dann wird nichts "
    "hochgeladen." + absturz(fehler)
)

# Das Beispiel: Uploads des Gateways
ergebnis, fehler = rufe(beispiel)
assert ergebnis is not None and ergebnis[0].uploads == BEISPIEL, (
    f"Im Beispiel ergibt gateway.uploads\n{ergebnis[0].uploads if ergebnis else None!r},\nerwartet war\n{BEISPIEL!r}."
    + ("\nTipp: Nach dem Hochladen einen neuen leeren Puffer beginnen (self.puffer = []), nicht den hochgeladenen "
       "leeren." if ergebnis and ergebnis[0].uploads and not ergebnis[0].uploads[0][1] else "")
    + absturz(fehler)
)

# Das Beispiel: Batterien und Uhr am Ende
ergebnis, fehler = rufe(beispiel)
zustand = None if ergebnis is None else (ergebnis[1].batterie, ergebnis[2].batterie, ergebnis[3].jetzt)
assert zustand == (1, 98, 30), f"Im Beispiel ergeben s1.batterie, s2.batterie und sim.jetzt {zustand!r}, erwartet war (1, 98, 30)." + absturz(fehler)

# simuliere: das Beispiel
ergebnis, fehler = rufe(lambda: simuliere([("s1", 4, 10, 3), ("s2", 15, 100, 1)], 10, 30))
assert ergebnis == BEISPIEL, (
    f"simuliere([('s1', 4, 10, 3), ('s2', 15, 100, 1)], 10, 30) ergibt\n{ergebnis!r},\nerwartet war\n{BEISPIEL!r}."
    + ("\nTipp: Prüfen Sie, ob Sie zuerst das Gateway und dann die Knoten starten und ob Ereignisse genau zur "
          "endzeit noch laufen." if ergebnis and ergebnis != BEISPIEL else "")
    + absturz(fehler)
)

# Gleichzeitige Ereignisse: gleiches Intervall wie der Takt, das Gateway wurde zuerst gestartet
ergebnis, fehler = rufe(lambda: simuliere([("t", 10, 100, 1)], 10, 30))
assert ergebnis == [(20, [(10, "t")]), (30, [(20, "t")])], (
    f"simuliere([('t', 10, 100, 1)], 10, 30) ergibt {ergebnis!r}, erwartet war [(20, [(10, 't')]), (30, [(20, 't')])]: "
    "Gateway und Knoten werden immer zur selben Zeit eingeplant, das Gateway zuerst, also lädt es zur Zeit 10 hoch, "
    "bevor die Nachricht von 10 da ist." + absturz(fehler)
)

# simuliere: keine Knoten, endzeit 0
ergebnis, fehler = rufe(lambda: (simuliere([], 5, 100), simuliere([("s", 1, 10, 1)], 5, 0)))
assert ergebnis == ([], []), f"simuliere([], 5, 100) und simuliere([('s', 1, 10, 1)], 5, 0) ergeben {ergebnis!r}, erwartet war ([], [])." + absturz(fehler)

zufall = Zufall(5063)

# Viele zufällige Geräte mit Wartezeiten im Vergleich mit einer einfachen Warteschlange
for _ in range(200):
    geraete = [(f"g{nummer}", [zufall.randint(0, 6) for _ in range(zufall.randint(0, 5))]) for nummer in range(zufall.randint(0, 5))]
    endzeit = zufall.randint(0, 25)
    ergebnis, fehler = rufe(lambda: wecker_lauf(endzeit, *geraete))
    erwartet = (wecker_vergleich(endzeit, geraete), endzeit)
    assert ergebnis == erwartet, (
        f"Mit endzeit {endzeit} und Geräten mit den Wartezeiten {dict(geraete)} ergeben Protokoll und jetzt\n"
        f"{ergebnis!r},\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Viele zufällige Knoten und Takte für simuliere
for _ in range(200):
    knoten = [
        (f"s{nummer}", zufall.randint(1, 12), zufall.randint(0, 30), zufall.randint(1, 8))
        for nummer in range(zufall.randint(0, 5))
    ]
    takt = zufall.randint(1, 12)
    endzeit = zufall.randint(0, 60)
    ergebnis, fehler = rufe(lambda: simuliere(knoten, takt, endzeit))
    erwartet = uploads_vergleich(knoten, takt, endzeit)
    assert ergebnis == erwartet, (
        f"simuliere({knoten}, {takt}, {endzeit}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Obere Grenze: 1000 Knoten und etwa 100000 Ereignisse
knoten = [(f"s{nummer}", 25 + nummer % 300, 10**6, 1 + nummer % 7) for nummer in range(1000)]
ergebnis, fehler = rufe(lambda: simuliere(knoten, 997, 10_000))
erwartet = uploads_vergleich(knoten, 997, 10_000)
assert ergebnis == erwartet, (
    f"simuliere mit 1000 Knoten bis endzeit 10000 ergibt {None if ergebnis is None else len(ergebnis)} Uploads mit "
    f"{None if ergebnis is None else sum(len(teil) for _, teil in ergebnis)} Nachrichten, erwartet waren {len(erwartet)} "
    f"Uploads mit {sum(len(teil) for _, teil in erwartet)} Nachrichten." + absturz(fehler)
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar(f"{BEISPIEL}\n1 98 30\n{BEISPIEL}"), (
    f"Ihr Programm gibt\n{AUSGABE}\naus, erwartet war\n{BEISPIEL}\n1 98 30\n{BEISPIEL}"
)
