# Automatisch erzeugt aus lehrkraft/muster/5_021_zeitraster.py - nicht von Hand ändern.
# vorlage-hash: 994cbf225bcaa433
# text-hash: d0312aa6aeb73bcb
# thema: datenstrukturen
# inhalt: Eigene Sequenz mit Slices

def vergleich(start, anzahl, abstand):
    """Vergleichslösung: dasselbe Raster als range."""
    return range(start, start + anzahl * abstand, abstand)


def zugriff(raster, index):
    """Liefert raster[index] oder den Namen der ausgelösten Ausnahme."""
    try:
        return raster[index]
    except Exception as fehler:
        return type(fehler).__name__


def als_liste(raster, hoechstens=10000):
    """Die ersten Elemente des Rasters über den Index; bricht bei hoechstens ab statt endlos zu laufen."""
    werte = []
    for index in range(hoechstens):
        try:
            werte.append(raster[index])
        except IndexError:
            return werte
    return werte + ["…"]


BEISPIEL = (1000, 5, 60)

# Attribute und Länge
raster = Zeitraster(*BEISPIEL)
gefunden = (getattr(raster, "start", None), getattr(raster, "anzahl", None), getattr(raster, "abstand", None), len(raster))
assert gefunden == (1000, 5, 60, 5), (
    f"Zeitraster(1000, 5, 60): erwartet start, anzahl, abstand und len = (1000, 5, 60, 5), gefunden {gefunden!r}."
)

# Zugriff mit positivem Index
raster = Zeitraster(*BEISPIEL)
gefunden = [zugriff(raster, index) for index in range(5)]
assert gefunden == [1000, 1060, 1120, 1180, 1240], (
    f"Zeitraster(1000, 5, 60)[0] bis [4] ergeben {gefunden!r}, erwartet war [1000, 1060, 1120, 1180, 1240].\n"
    "Tipp: Der Zeitpunkt an Stelle i ist start + i * abstand."
)

# Zugriff mit negativem Index zählt von hinten
raster = Zeitraster(*BEISPIEL)
gefunden = [zugriff(raster, index) for index in [-1, -2, -5]]
assert gefunden == [1240, 1180, 1000], (
    f"Zeitraster(1000, 5, 60)[-1], [-2], [-5] ergeben {gefunden!r}, erwartet war [1240, 1180, 1000].\n"
    "Tipp: Zu einem negativen Index addiert man die Länge."
)

# Index außerhalb löst IndexError aus (sonst endet for nie)
raster = Zeitraster(*BEISPIEL)
gefunden = [zugriff(raster, index) for index in [5, 6, -6, 10**15]]
assert gefunden == ["IndexError"] * 4, (
    f"Zeitraster(1000, 5, 60)[5], [6], [-6], [10**15] ergeben {gefunden!r}, erwartet war jeweils ein IndexError.\n"
    "Tipp: Das geerbte __iter__ hört erst bei einem IndexError auf; ohne ihn läuft list(raster) endlos."
)

# Ein Index, der keine Zahl ist, löst TypeError aus
raster = Zeitraster(*BEISPIEL)
gefunden = [zugriff(raster, index) for index in ["2", 1.0, None]]
assert gefunden == ["TypeError"] * 3, (
    f"Zeitraster(1000, 5, 60)['2'], [1.0], [None] ergeben {gefunden!r}, erwartet war jeweils ein TypeError."
)

# Ungültige Anzahl oder Abstand 0 lösen ValueError aus
gefunden = []
for argumente in [(0, -1, 5), (0, 5, 0)]:
    try:
        Zeitraster(*argumente)
        gefunden.append("kein Fehler")
    except ValueError:
        gefunden.append("ValueError")
    except Exception as fehler:
        gefunden.append(type(fehler).__name__)
assert gefunden == ["ValueError", "ValueError"], (
    f"Zeitraster(0, -1, 5) und Zeitraster(0, 5, 0) ergeben {gefunden!r}, erwartet war jeweils ein ValueError."
)

# Sequence liefert for, list, index, count und reversed
raster = Zeitraster(*BEISPIEL)
gefunden = (isinstance(raster, Sequence), als_liste(raster), raster.index(1180), list(reversed(raster)))
assert gefunden == (True, [1000, 1060, 1120, 1180, 1240], 3, [1240, 1180, 1120, 1060, 1000]), (
    "Für Zeitraster(1000, 5, 60) erwartet isinstance(raster, Sequence), list(raster), raster.index(1180), "
    f"list(reversed(raster)) = (True, [1000, …, 1240], 3, [1240, …, 1000]), gefunden {gefunden!r}."
)

# Ein Slice liefert ein neues Zeitraster
raster = Zeitraster(*BEISPIEL)
teil = zugriff(raster, slice(1, 4))
assert isinstance(teil, Zeitraster) and als_liste(teil) == [1060, 1120, 1180], (
    f"Zeitraster(1000, 5, 60)[1:4] ergibt {teil!r} mit den Werten {als_liste(teil) if isinstance(teil, Sequence) else None!r}; "
    "erwartet war ein Zeitraster mit [1060, 1120, 1180].\n"
    "Tipp: Ist index ein slice, rechnen Sie mit index.indices(self.anzahl) die Stellen aus."
)

# Slices mit Schrittweite, rückwärts, negativen und zu großen Grenzen
raster = Zeitraster(*BEISPIEL)
fehler = []
for teil in [slice(None, None, 2), slice(None, None, -1), slice(None, None, -2), slice(-2, None), slice(-100, 100), slice(3, 1), slice(4, 0, -3), slice(10, 20)]:
    ergebnis = zugriff(raster, teil)
    erwartet = [1000, 1060, 1120, 1180, 1240][teil]
    if not isinstance(ergebnis, Zeitraster) or als_liste(ergebnis) != erwartet:
        fehler.append(f"[{teil.start}:{teil.stop}:{teil.step}] ergibt {ergebnis!r}, erwartet {erwartet}")
assert not fehler, "Bei Zeitraster(1000, 5, 60):\n  " + "\n  ".join(fehler)

# Ein Slice eines Slices
raster = Zeitraster(0, 100, 5)
teil = zugriff(zugriff(raster, slice(10, 90, 3)), slice(None, None, -4))
erwartet = list(range(0, 500, 5))[10:90:3][::-4]
assert isinstance(teil, Zeitraster) and als_liste(teil) == erwartet, (
    f"Zeitraster(0, 100, 5)[10:90:3][::-4] ergibt {teil!r}, erwartet war ein Zeitraster mit {erwartet}."
)

# in: Zeitpunkte des Rasters werden gefunden
raster = Zeitraster(*BEISPIEL)
gefunden = [zeit in raster for zeit in [1000, 1120, 1240]]
assert gefunden == [True, True, True], f"1000, 1120, 1240 in Zeitraster(1000, 5, 60) ergeben {gefunden!r}, erwartet war [True, True, True]."

# in: Zeiten zwischen den Zeitpunkten, davor und danach gehören nicht dazu
raster = Zeitraster(*BEISPIEL)
gefunden = [zeit in raster for zeit in [1121, 999, 940, 1300]]
assert gefunden == [False] * 4, (
    f"1121, 999, 940, 1300 in Zeitraster(1000, 5, 60) ergeben {gefunden!r}, erwartet war jeweils False "
    "(1300 wäre der Zeitpunkt Nummer 5, das Raster hat aber nur die Nummern 0 bis 4)."
)

# in: Werte, die keine ganze Zahl sind, gehören nicht dazu
raster = Zeitraster(*BEISPIEL)
try:
    gefunden = ["1000" in raster, 1000.5 in raster, None in raster]
except Exception as ausnahme:
    gefunden = f"{type(ausnahme).__name__}: {ausnahme}"
assert gefunden == [False, False, False], (
    f"'1000', 1000.5 und None in Zeitraster(1000, 5, 60) ergeben {gefunden!r}, erwartet war jeweils False."
)

# Rückwärts laufendes Raster mit negativem Abstand
raster = Zeitraster(50, 4, -20)
gefunden = (als_liste(raster), 10 in raster, -10 in raster, -30 in raster, 70 in raster, zugriff(raster, -1))
assert gefunden == ([50, 30, 10, -10], True, True, False, False, -10), (
    "Zeitraster(50, 4, -20): erwartet list = [50, 30, 10, -10], 10 in, -10 in, -30 in, 70 in, [-1] = "
    f"(…, True, True, False, False, -10), gefunden {gefunden!r}."
)

# Leeres Raster
raster = Zeitraster(7, 0, 3)
gefunden = (len(raster), als_liste(raster), 7 in raster, zugriff(raster, 0), als_liste(zugriff(raster, slice(None))))
assert gefunden == (0, [], False, "IndexError", []), (
    f"Zeitraster(7, 0, 3): erwartet len 0, keine Werte, 7 nicht enthalten, [0] IndexError, [:] leer; gefunden {gefunden!r}."
)

# __contains__ ist selbst geschrieben, nicht von Sequence geerbt
assert "__contains__" in vars(Zeitraster), (
    "Zeitraster soll ein eigenes __contains__ haben; das geerbte von Sequence probiert alle Stellen durch."
)

# in braucht O(1) Schritte, auch bei 10**12 Zeitpunkten
raster = Zeitraster(0, 10**12, 1)
ergebnis, schritte = zaehle_schritte(raster.__contains__, 10**12 - 1)
assert ergebnis is True and schritte <= 20, (
    f"(10**12 - 1) in Zeitraster(0, 10**12, 1) ergibt {ergebnis!r} in {schritte} Schritten; "
    "erwartet True in wenigen Schritten (O(1)).\n"
    "Tipp: Rechnen Sie aus, ob (zeit - start) ein Vielfaches von abstand ist und die Nummer im Raster liegt."
)

# Zugriff und Slice brauchen O(1) Schritte, auch bei 10**12 Zeitpunkten
raster = Zeitraster(-(10**12), 10**12, 10**6)
wert, schritte_index = zaehle_schritte(raster.__getitem__, -1)
teil, schritte_slice = zaehle_schritte(raster.__getitem__, slice(5, None, 1000))
erwartet_teil = range(-(10**12), -(10**12) + 10**18, 10**6)[5::1000]
assert (
    wert == -(10**12) + (10**12 - 1) * 10**6
    and isinstance(teil, Zeitraster)
    and len(teil) == len(erwartet_teil)
    and teil[-1] == erwartet_teil[-1]
    and schritte_index <= 20
    and schritte_slice <= 30
), (
    f"Bei Zeitraster(-10**12, 10**12, 10**6): [-1] ergibt {wert!r} in {schritte_index} Schritten, "
    f"[5::1000] ergibt {teil!r} in {schritte_slice} Schritten; erwartet {-(10**12) + (10**12 - 1) * 10**6} "
    f"und ein Zeitraster der Länge {len(erwartet_teil)}, beides in wenigen Schritten."
)

# 500 zufällige Raster mit Zugriffen, Slices und in
zufall = Zufall(5021)
fehlerfall = None
for _ in range(500):
    start = zufall.randint(-1000, 1000)
    anzahl = zufall.randint(0, 30)
    abstand = zufall.choice([-1, 1]) * zufall.randint(1, 50)
    raster = Zeitraster(start, anzahl, abstand)
    soll = vergleich(start, anzahl, abstand)
    index = zufall.randint(-35, 35)
    erwartet_index = soll[index] if -anzahl <= index < anzahl else "IndexError"
    teil = slice(zufall.choice([None, zufall.randint(-40, 40)]), zufall.choice([None, zufall.randint(-40, 40)]), zufall.choice([None, 1, -1, 2, -3, 7]))
    zeit = zufall.randint(-3000, 3000)
    bekommen = (len(raster), zugriff(raster, index), als_liste(zugriff(raster, teil)), zeit in raster)
    erwartet = (len(soll), erwartet_index, list(soll[teil]), zeit in soll)
    if bekommen != erwartet:
        fehlerfall = (raster, index, teil, zeit, bekommen, erwartet)
        break
assert fehlerfall is None, (
    f"Für {fehlerfall[0]!r} ergeben len, [{fehlerfall[1]}], "
    f"[{fehlerfall[2].start}:{fehlerfall[2].stop}:{fehlerfall[2].step}] (als Liste) und {fehlerfall[3]} in raster\n"
    f"  {fehlerfall[4]!r}\nerwartet war\n  {fehlerfall[5]!r}"
)
