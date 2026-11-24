# Automatisch erzeugt aus lehrkraft/muster/4_074_ereignisschlange.py - nicht von Hand ändern.
# vorlage-hash: 421daf01ac3b0008
# text-hash: 46a524bd804af16f
# thema: datenstrukturen
# inhalt: heapq und Prioritätswarteschlange

BEISPIEL = [("Speichern", 120), ("Suche", 870), ("Menü öffnen", 35), ("Bericht", 870), ("Export", 1450), ("Tippen", 12)]


class ZuVieleVergleiche(Exception):
    """Bricht einen Laufzeittest ab, sobald eine Lösung weit über der erlaubten Zahl von Vergleichen liegt."""


class Gezaehlt(int):
    """Eine ganze Zahl, die jeden Vergleich mit <, <=, >, >=, == und != mitzählt."""

    vergleiche = 0
    abbruch = None

    @classmethod
    def zaehle(cls):
        """Zählt einen Vergleich und bricht ab, wenn die Abbruchgrenze überschritten ist."""
        cls.vergleiche += 1
        if cls.abbruch is not None and cls.vergleiche > cls.abbruch:
            raise ZuVieleVergleiche(f"mehr als {cls.abbruch} Vergleiche")

    def __lt__(self, anderes):
        """Zählt und vergleicht wie int."""
        Gezaehlt.zaehle()
        return int.__lt__(self, anderes)

    def __le__(self, anderes):
        """Zählt und vergleicht wie int."""
        Gezaehlt.zaehle()
        return int.__le__(self, anderes)

    def __gt__(self, anderes):
        """Zählt und vergleicht wie int."""
        Gezaehlt.zaehle()
        return int.__gt__(self, anderes)

    def __ge__(self, anderes):
        """Zählt und vergleicht wie int."""
        Gezaehlt.zaehle()
        return int.__ge__(self, anderes)

    def __eq__(self, anderes):
        """Zählt und vergleicht wie int."""
        Gezaehlt.zaehle()
        return int.__eq__(self, anderes)

    def __ne__(self, anderes):
        """Zählt und vergleicht wie int."""
        Gezaehlt.zaehle()
        return int.__ne__(self, anderes)

    __hash__ = int.__hash__


def zaehle_vergleiche(funktion, abbruch):
    """Ruft funktion() auf und gibt die Zahl der Vergleiche zwischen Gezaehlt-Zahlen zurück (None bei Abbruch)."""
    Gezaehlt.vergleiche = 0
    Gezaehlt.abbruch = abbruch
    try:
        funktion()
        return Gezaehlt.vergleiche
    except ZuVieleVergleiche:
        return None
    finally:
        Gezaehlt.abbruch = None


def vergleich_langsamste(protokoll, k):
    """Vergleichslösung: stabil nach Dauer absteigend sortieren und die ersten k nehmen."""
    return sorted(protokoll, key=lambda eintrag: -eintrag[1])[:k]


def abarbeiten(schlange):
    """Holt alle Ereignisse mit naechstes heraus, bis ist_leer True ist (höchstens 200 000)."""
    ergebnis = []
    while not schlange.ist_leer() and len(ergebnis) < 200_000:
        ergebnis.append(schlange.naechstes())
    return ergebnis


def fehler_bei(funktion):
    """Ruft funktion() auf und gibt die Ausnahme zurück oder None, wenn keine kam."""
    try:
        funktion()
    except Exception as ausnahme:
        return ausnahme
    return None


# langsamste: das Beispiel
ergebnis = langsamste(list(BEISPIEL), 3)
assert ergebnis == [("Export", 1450), ("Suche", 870), ("Bericht", 870)], (
    f"langsamste(protokoll, 3) ergibt {ergebnis!r},\nerwartet war [('Export', 1450), ('Suche', 870), ('Bericht', 870)].\n"
    "Tipp: heapq.nlargest(k, protokoll, key=lambda eintrag: eintrag[1])."
)

# langsamste: ein anderes Protokoll, k = 1
ergebnis = langsamste([("Login", 300), ("Filter", 2200), ("Drucken", 950)], 1)
assert ergebnis == [("Filter", 2200)], (
    f"langsamste([('Login', 300), ('Filter', 2200), ('Drucken', 950)], 1) ergibt {ergebnis!r}, "
    "erwartet war [('Filter', 2200)]."
)

# langsamste: der langsamste zuerst
protokoll = [("a", 5), ("b", 40), ("c", 20), ("d", 30), ("e", 10)]
ergebnis = langsamste(list(protokoll), 4)
assert ergebnis == [("b", 40), ("d", 30), ("c", 20), ("e", 10)], (
    f"langsamste({protokoll}, 4) ergibt {ergebnis!r},\nerwartet war [('b', 40), ('d', 30), ('c', 20), ('e', 10)]: "
    "die größte Dauer zuerst.\nTipp: nlargest liefert die größten absteigend, nsmallest die kleinsten aufsteigend."
)

# langsamste: nach der Dauer, nicht nach dem Namen
protokoll = [("Zoom", 10), ("Ablage", 99), ("Menü", 50)]
ergebnis = langsamste(list(protokoll), 2)
assert ergebnis == [("Ablage", 99), ("Menü", 50)], (
    f"langsamste({protokoll}, 2) ergibt {ergebnis!r}, erwartet war [('Ablage', 99), ('Menü', 50)].\n"
    "Tipp: Tupel werden zuerst nach dem Namen verglichen; vergleichen Sie mit key=lambda eintrag: eintrag[1] nur die Dauer."
)

# langsamste: bei gleicher Dauer der frühere zuerst
protokoll = [("x", 7), ("Suche", 80), ("Bericht", 80), ("Anmelden", 80), ("y", 3)]
ergebnis = langsamste(list(protokoll), 2)
assert ergebnis == [("Suche", 80), ("Bericht", 80)], (
    f"langsamste({protokoll}, 2) ergibt {ergebnis!r}, erwartet war [('Suche', 80), ('Bericht', 80)]: "
    "bei gleicher Dauer der frühere Eintrag zuerst.\n"
    "Tipp: nlargest mit key ist stabil; wer selbst Tupel in einen Heap legt, braucht die Position als zweites Element."
)

# langsamste: k = 0 ergibt eine leere Liste
ergebnis = langsamste(list(BEISPIEL), 0)
assert ergebnis == [], f"langsamste(protokoll, 0) ergibt {ergebnis!r}, erwartet war []."

# langsamste: weniger als k Einträge
protokoll = [("a", 3), ("b", 9)]
ergebnis = langsamste(list(protokoll), 5)
assert ergebnis == [("b", 9), ("a", 3)], (
    f"langsamste({protokoll}, 5) ergibt {ergebnis!r}, erwartet war [('b', 9), ('a', 3)]: alle Einträge, sortiert."
)

# langsamste: leeres Protokoll
ergebnis = langsamste([], 3)
assert ergebnis == [], f"langsamste([], 3) ergibt {ergebnis!r}, erwartet war []."

# langsamste: Dauer 0 zählt mit
protokoll = [("a", 0), ("b", 0), ("c", 1)]
ergebnis = langsamste(list(protokoll), 3)
assert ergebnis == [("c", 1), ("a", 0), ("b", 0)], (
    f"langsamste({protokoll}, 3) ergibt {ergebnis!r}, erwartet war [('c', 1), ('a', 0), ('b', 0)]."
)

# langsamste: das Protokoll bleibt unverändert
protokoll = list(BEISPIEL)
langsamste(protokoll, 3)
assert protokoll == BEISPIEL, (
    f"Nach langsamste(protokoll, 3) ist das Protokoll {protokoll!r}, erwartet war es unverändert.\n"
    "Tipp: Entfernen oder sortieren Sie nicht in der übergebenen Liste."
)

# Ereignisschlange: das Beispiel
schlange = Ereignisschlange()
schlange.einreihen({"art": "neuzeichnen", "bereich": "liste"}, 2)
schlange.einreihen({"art": "taste", "zeichen": "a"}, 0)
schlange.einreihen({"art": "zeitgeber", "name": "autosave"}, 1)
schlange.einreihen({"art": "klick", "x": 40, "y": 12}, 0)
ergebnis = [schlange.naechstes() for _ in range(4)]
erwartet = [
    {"art": "taste", "zeichen": "a"},
    {"art": "klick", "x": 40, "y": 12},
    {"art": "zeitgeber", "name": "autosave"},
    {"art": "neuzeichnen", "bereich": "liste"},
]
assert ergebnis == erwartet, (
    f"Viermal naechstes() nach dem Beispiel ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}.\n"
    "Tipp: Legen Sie Tupel (prioritaet, laufende_nummer, ereignis) mit heapq.heappush in eine Liste."
)

# Ereignisschlange: die kleinste Priorität zuerst
schlange = Ereignisschlange()
for prioritaet in [5, 3, 9, 0, 7]:
    schlange.einreihen({"p": prioritaet}, prioritaet)
ergebnis = [schlange.naechstes()["p"] for _ in range(5)]
assert ergebnis == [0, 3, 5, 7, 9], (
    f"Nach einreihen mit den Prioritäten 5, 3, 9, 0, 7 liefert naechstes() die Prioritäten {ergebnis}, "
    "erwartet war [0, 3, 5, 7, 9]: kleiner ist dringender."
)

# Ereignisschlange: gleiche Priorität in Eingangsreihenfolge
schlange = Ereignisschlange()
for zeichen in "zebra":
    schlange.einreihen({"zeichen": zeichen}, 0)
ergebnis = "".join(schlange.naechstes()["zeichen"] for _ in range(5))
assert ergebnis == "zebra", (
    f"Fünf Tasten z, e, b, r, a mit derselben Priorität kommen als {ergebnis!r} heraus, erwartet war 'zebra'.\n"
    "Tipp: Eine laufende Nummer im Tupel hinter der Priorität hält die Eingangsreihenfolge fest."
)

# Ereignisschlange: Dictionaries mit gleicher Priorität lösen keinen TypeError aus
schlange = Ereignisschlange()
fehler = fehler_bei(lambda: [schlange.einreihen({"art": "klick", "x": x}, 1) for x in [30, 10, 20]])
ergebnis = None if fehler else [schlange.naechstes()["x"] for _ in range(3)]
assert fehler is None and ergebnis == [30, 10, 20], (
    "Drei Klicks mit Priorität 1 einreihen und herausholen: "
    f"{'Ausnahme ' + repr(fehler) if fehler else 'Reihenfolge ' + str(ergebnis)}, erwartet war die Reihenfolge [30, 10, 20].\n"
    "Tipp: Mit Tupeln (prioritaet, ereignis) vergleicht Python bei gleicher Priorität die Dictionaries, und das "
    "geht nicht. Eine laufende Nummer dazwischen ist nie doppelt."
)

# Ereignisschlange: vorschau zeigt das nächste, ohne es zu entfernen
schlange = Ereignisschlange()
schlange.einreihen({"art": "neuzeichnen"}, 2)
schlange.einreihen({"art": "taste"}, 0)
erste, zweite = schlange.vorschau(), schlange.vorschau()
danach = schlange.naechstes()
assert erste == zweite == danach == {"art": "taste"}, (
    f"vorschau() ergibt {erste!r}, nochmals {zweite!r}, dann naechstes() {danach!r}; "
    "erwartet war dreimal {'art': 'taste'}.\nTipp: heap[0] ist das kleinste Element, ohne etwas zu entfernen."
)

# Ereignisschlange: ist_leer
schlange = Ereignisschlange()
vorher = schlange.ist_leer()
schlange.einreihen({"art": "taste"}, 0)
mittendrin = schlange.ist_leer()
schlange.naechstes()
nachher = schlange.ist_leer()
assert (vorher, mittendrin, nachher) == (True, False, True), (
    f"ist_leer() ergibt neu {vorher!r}, mit einem Ereignis {mittendrin!r}, nach naechstes() {nachher!r}; "
    "erwartet war True, False, True."
)

# Ereignisschlange: naechstes bei leerer Schlange löst IndexError aus
schlange = Ereignisschlange()
fehler = fehler_bei(schlange.naechstes)
assert isinstance(fehler, IndexError), (
    f"naechstes() bei leerer Schlange löst {fehler!r} aus, erwartet war ein IndexError."
)

# Ereignisschlange: vorschau bei leerer Schlange löst IndexError aus
schlange = Ereignisschlange()
schlange.einreihen({"art": "taste"}, 0)
schlange.naechstes()
fehler = fehler_bei(schlange.vorschau)
assert isinstance(fehler, IndexError), (
    f"vorschau() bei leerer Schlange (nach einreihen und naechstes) löst {fehler!r} aus, erwartet war ein IndexError.\n"
    "Tipp: heap[0] einer leeren Liste löst ihn schon selbst aus; prüfen Sie aber, ob die Liste leer ist."
)

# Ereignisschlange: einreihen und naechstes abwechselnd
schlange = Ereignisschlange()
schlange.einreihen({"n": "A"}, 1)
schlange.einreihen({"n": "B"}, 1)
erstes = schlange.naechstes()["n"]
schlange.einreihen({"n": "C"}, 1)
schlange.einreihen({"n": "D"}, 0)
rest = [schlange.naechstes()["n"] for _ in range(3)]
assert [erstes] + rest == ["A", "D", "B", "C"], (
    "einreihen A(1), B(1), naechstes, einreihen C(1), D(0), dreimal naechstes: "
    f"Reihenfolge {[erstes] + rest}, erwartet war ['A', 'D', 'B', 'C'].\n"
    "Tipp: Die laufende Nummer muss weiterzählen, auch wenn zwischendurch Ereignisse entnommen werden; "
    "len(heap) ist dafür nicht geeignet."
)

# Ereignisschlange: zwei Schlangen sind unabhängig
erste_schlange = Ereignisschlange()
zweite_schlange = Ereignisschlange()
erste_schlange.einreihen({"art": "taste"}, 0)
assert zweite_schlange.ist_leer(), (
    "Nach einreihen in eine Schlange ist eine zweite, neue Schlange nicht leer.\n"
    "Tipp: Legen Sie die Liste in __init__ als self.heap = [] an, nicht in der Klasse."
)

# Die Ausgabe des Programms
erwartet = (
    "[('Export', 1450), ('Suche', 870), ('Bericht', 870)]\n"
    "{'art': 'taste', 'zeichen': 'a'}\n{'art': 'klick', 'x': 40, 'y': 12}\n"
    "{'art': 'zeitgeber', 'name': 'autosave'}\n{'art': 'neuzeichnen', 'bereich': 'liste'}"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Protokolle
zufall = Zufall(4074)
for _ in range(300):
    protokoll = [(f"aktion{i}", zufall.randint(0, 30)) for i in range(zufall.randint(0, 25))]
    k = zufall.randint(0, 30)
    ergebnis = langsamste(list(protokoll), k)
    erwartet = vergleich_langsamste(protokoll, k)
    assert ergebnis == erwartet, f"langsamste({protokoll}, {k})\nergibt {ergebnis!r},\nerwartet war {erwartet!r}."

# Viele zufällige Folgen von einreihen und naechstes
zufall = Zufall(40740)
for _ in range(200):
    schlange = Ereignisschlange()
    wartend = []
    nummer = 0
    schritte = []
    for _ in range(zufall.randint(1, 30)):
        if wartend and zufall.random() < 0.4:
            schritte.append("naechstes()")
            erwartet = min(wartend, key=lambda eintrag: (eintrag[0], eintrag[1]["nr"]))
            wartend.remove(erwartet)
            ergebnis = schlange.naechstes()
            assert ergebnis == erwartet[1], (
                f"Nach {', '.join(schritte)}\nliefert das letzte naechstes() {ergebnis!r}, erwartet war {erwartet[1]!r}."
            )
        else:
            prioritaet = zufall.randint(0, 9)
            ereignis = {"nr": nummer}
            nummer += 1
            schritte.append(f"einreihen({ereignis}, {prioritaet})")
            schlange.einreihen(ereignis, prioritaet)
            wartend.append((prioritaet, ereignis))

# Laufzeit: langsamste sortiert nicht das ganze Protokoll
zufall = Zufall(47)
n = 100_000
protokoll = [(f"a{i}", Gezaehlt(zufall.randint(0, 60_000))) for i in range(n)]
vergleiche = zaehle_vergleiche(lambda: langsamste(protokoll, 20), abbruch=10 * n)
assert vergleiche is not None and vergleiche <= 5 * n, (
    f"langsamste mit n = {n} Einträgen und k = 20 braucht "
    f"{'mehr als ' + str(10 * n) if vergleiche is None else vergleiche} Vergleiche der Dauern, "
    f"erlaubt sind höchstens {5 * n} (O(n log k)).\n"
    "Tipp: Ganz sortieren braucht etwa n·log2(n) ≈ 17·n Vergleiche, k-mal das Maximum suchen k·n. heapq.nlargest "
    "vergleicht fast jeden Eintrag nur einmal mit dem kleinsten der bisher k größten."
)

# Laufzeit: einreihen und naechstes brauchen O(log m) Vergleiche
zufall = Zufall(4007)
m = 2000
prioritaeten = [Gezaehlt(zufall.randint(0, 9)) for _ in range(m)]


def fuellen_und_leeren():
    """Reiht m Ereignisse ein und holt sie alle wieder heraus."""
    schlange = Ereignisschlange()
    for nummer, prioritaet in enumerate(prioritaeten):
        schlange.einreihen({"nr": nummer}, prioritaet)
    abarbeiten(schlange)


vergleiche = zaehle_vergleiche(fuellen_und_leeren, abbruch=300_000)
assert vergleiche is not None and vergleiche <= 150_000, (
    f"{m}-mal einreihen und {m}-mal naechstes brauchen "
    f"{'mehr als 300000' if vergleiche is None else vergleiche} Vergleiche der Prioritäten, "
    "erlaubt sind höchstens 150000 (O(m log m)).\n"
    "Tipp: Nach jedem Einfügen sortieren oder bei jedem naechstes mit min suchen kostet O(m) Vergleiche je Aufruf; "
    "heappush und heappop brauchen nur O(log m)."
)

# Obere Grenze: langsamste bei 200 000 Einträgen und k = 1000
zufall = Zufall(474)
protokoll = [(f"a{i}", zufall.randint(0, 60_000)) for i in range(200_000)]
ergebnis = langsamste(list(protokoll), 1000)
erwartet = vergleich_langsamste(protokoll, 1000)
assert ergebnis == erwartet, (
    f"Bei 200 000 Einträgen und k = 1000 weicht das Ergebnis ab: {len(ergebnis)} Einträge, "
    f"die ersten drei {ergebnis[:3]!r}, erwartet {erwartet[:3]!r}."
)

# Obere Grenze: 100 000 Ereignisse
zufall = Zufall(4744)
schlange = Ereignisschlange()
prioritaeten = [zufall.randint(0, 9) for _ in range(100_000)]
for nummer, prioritaet in enumerate(prioritaeten):
    schlange.einreihen({"nr": nummer}, prioritaet)
ergebnis = [ereignis["nr"] for ereignis in abarbeiten(schlange)]
erwartet = sorted(range(100_000), key=lambda nummer: prioritaeten[nummer])
assert ergebnis == erwartet, (
    f"Bei 100 000 Ereignissen kommen {len(ergebnis)} heraus, die ersten fünf Nummern {ergebnis[:5]}, "
    f"erwartet {erwartet[:5]}."
)
