# Automatisch erzeugt aus lehrkraft/muster/5_013_pruefregeln.py - nicht von Hand ändern.
# vorlage-hash: 7eceeee712da1a48
# text-hash: 2aded114e263f328
# thema: klassen
# inhalt: Eigene Metaklasse

def definiere(name, basen, namensraum):
    """Definiert eine Klasse wie eine class-Anweisung; gibt (klasse, None) oder (None, TypeError) zurück."""
    try:
        return Pruefmeta(name, basen, dict(namensraum)), None
    except TypeError as fehler:
        return None, fehler


def neue_wurzel(pflicht=("kennung", "pruefe")):
    """Erzeugt eine frische Wurzel mit eigenem Verzeichnis."""
    klasse, fehler = definiere("Wurzel", (), {"pflicht": pflicht})
    assert fehler is None, f"Eine Wurzel ohne kennung und pruefe darf keinen Fehler auslösen, bekommen: {fehler!r}"
    return klasse


def pruefe_ok(self, wert):
    """Eine Prüfmethode, die immer ok liefert."""
    return "ok"


# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Kaputt fehlt: kennung, pruefe\n1 CpuLast\n{'cpu': 'warnung'}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Eine Wurzel wird nicht geprüft und hat ein leeres Verzeichnis
wurzel = neue_wurzel()
assert len(wurzel) == 0 and list(wurzel) == [], (
    f"Eine neue Wurzel soll ein leeres Verzeichnis haben; len ergibt {len(wurzel)}, list {list(wurzel)!r}."
)

# len zählt die eingetragenen Regeln
wurzel = neue_wurzel()
klassen = []
for kennung in ["temp", "cpu", "ram"]:
    klasse, fehler = definiere(kennung.title(), (wurzel,), {"kennung": kennung, "pruefe": pruefe_ok})
    klassen.append(klasse)
anzahl = len(wurzel)
assert anzahl == 3, (
    f"Nach den drei Regeln temp, cpu und ram ergibt len(wurzel) {anzahl!r}, erwartet war 3.\n"
    "Tipp: Tragen Sie jede Regel in __new__ in das Verzeichnis ihrer Wurzel ein; __len__ gibt dessen Länge zurück."
)

# wurzel[kennung] liefert die Regel mit dieser Kennung
regel = wurzel["cpu"]
assert regel is klassen[1], f"wurzel['cpu'] ergibt {regel!r}, erwartet war {klassen[1]!r}."

# Regeln werden in der Reihenfolge der Definition eingetragen
ergebnis = (list(wurzel), len(wurzel), wurzel["cpu"])
assert ergebnis == (klassen, 3, klassen[1]), (
    f"Nach den Regeln temp, cpu und ram ergeben list(wurzel), len(wurzel) und wurzel['cpu'] {ergebnis!r}; "
    f"erwartet war ({klassen!r}, 3, {klassen[1]!r}).\nTipp: Ein Dictionary von der Kennung auf die Klasse behält "
    "die Reihenfolge des Eintragens."
)

# Auch über eine Regel erreicht man das Verzeichnis ihrer Wurzel
assert len(klassen[0]) == 3 and klassen[2]["temp"] is klassen[0], (
    "len(Regel) und Regel['temp'] sollen auf dem Verzeichnis der Wurzel arbeiten; "
    f"len(klassen[0]) ergibt {len(klassen[0])}."
)

# Unbekannte Kennung: KeyError
try:
    wurzel["disk"]
    gefangen = None
except KeyError as fehler:
    gefangen = fehler
assert gefangen is not None, "wurzel['disk'] soll einen KeyError auslösen, wenn es keine Regel mit dieser Kennung gibt."

# Fehlende Namen: TypeError mit Klassennamen und allen fehlenden Namen
wurzel = neue_wurzel(("kennung", "pruefe", "einheit"))
for namensraum, fehlend in [({}, ["kennung", "pruefe", "einheit"]), ({"kennung": "x", "pruefe": pruefe_ok}, ["einheit"])]:
    klasse, fehler = definiere("Unvollstaendig", (wurzel,), namensraum)
    meldung = str(fehler) if fehler else ""
    assert fehler is not None and vergleichbar("Unvollstaendig") in vergleichbar(meldung) and all(vergleichbar(name) in vergleichbar(meldung) for name in fehlend), (
        f"Eine Regel Unvollstaendig mit {sorted(namensraum)} soll bei pflicht ('kennung', 'pruefe', 'einheit') einen "
        f"TypeError mit dem Klassennamen und {fehlend} auslösen; bekommen: {fehler!r}."
    )

# Abgelehnte Regeln werden nicht eingetragen
assert len(wurzel) == 0, f"Abgelehnte Regeln dürfen nicht eingetragen werden; len(wurzel) ist {len(wurzel)}."

# Geerbte Namen zählen
wurzel = neue_wurzel(("kennung", "pruefe", "einheit"))
basis, fehler1 = definiere("Basis", (wurzel,), {"kennung": "basis", "pruefe": pruefe_ok, "einheit": "%"})
kind, fehler2 = definiere("Kind", (basis,), {"kennung": "kind"})
assert fehler1 is None and fehler2 is None and list(wurzel) == [basis, kind], (
    f"Eine Regel Kind, die pruefe und einheit von Basis erbt, soll gültig sein; Fehler: {fehler1!r}, {fehler2!r}, "
    f"Verzeichnis: {list(wurzel)!r}.\nTipp: Prüfen Sie mit hasattr auf der fertigen Klasse, nicht im namensraum."
)

# Eine geerbte Kennung ist schon vergeben
enkel, fehler = definiere("Enkel", (kind,), {})
assert fehler is not None and enkel is None and len(wurzel) == 2, (
    f"Eine Regel Enkel ohne eigene kennung erbt 'kind', das schon vergeben ist; erwartet war ein TypeError und zwei "
    f"Regeln im Verzeichnis, bekommen: {fehler!r} und len(wurzel) = {len(wurzel)}."
)

# Eine kennung, die kein nicht leerer Text ist, löst TypeError aus
wurzel = neue_wurzel()
for namensraum, beschreibung in [
    ({"kennung": "", "pruefe": pruefe_ok}, "kennung ''"),
    ({"kennung": 7, "pruefe": pruefe_ok}, "kennung 7"),
    ({"kennung": None, "pruefe": pruefe_ok}, "kennung None"),
]:
    klasse, fehler = definiere("Falsch", (wurzel,), namensraum)
    assert fehler is not None, f"Eine Regel mit {beschreibung} soll einen TypeError auslösen, wurde aber angenommen."

# Ein pruefe, das nicht aufrufbar ist, löst TypeError aus
klasse, fehler = definiere("Falsch", (wurzel,), {"kennung": "x", "pruefe": "ok"})
assert fehler is not None, (
    "Eine Regel mit pruefe = 'ok' soll einen TypeError auslösen, wurde aber angenommen.\n"
    "Tipp: callable(getattr(klasse, 'pruefe', None)) prüft, ob man pruefe aufrufen kann."
)

# Abgelehnte ungültige Regeln werden nicht eingetragen
assert len(wurzel) == 0, f"Abgelehnte Regeln dürfen nicht eingetragen werden; len(wurzel) ist {len(wurzel)}."

# Doppelte Kennung in derselben Wurzel: TypeError
erste = neue_wurzel()
zweite = neue_wurzel()
a, fehler_a = definiere("A", (erste,), {"kennung": "cpu", "pruefe": pruefe_ok})
b, fehler_b = definiere("B", (zweite,), {"kennung": "cpu", "pruefe": pruefe_ok})
c, fehler_c = definiere("C", (erste,), {"kennung": "cpu", "pruefe": pruefe_ok})
assert fehler_a is None and fehler_c is not None and erste["cpu"] is a, (
    "Eine zweite Regel 'cpu' in derselben Wurzel soll einen TypeError auslösen, die erste bleibt eingetragen; "
    f"Fehler bei der ersten: {fehler_a!r}, bei der zweiten: {fehler_c!r}."
)

# Getrennte Wurzeln haben getrennte Verzeichnisse
assert fehler_a is None and fehler_b is None and fehler_c is not None and erste["cpu"] is a and zweite["cpu"] is b, (
    "In zwei Wurzeln darf je eine Regel 'cpu' heißen, eine zweite 'cpu' in derselben Wurzel nicht; "
    f"Fehler: {fehler_a!r}, {fehler_b!r}, {fehler_c!r}.\nTipp: Jede Wurzel braucht ihr eigenes Verzeichnis, angelegt in __new__."
)

# Mit einer leeren Pflichtliste geht jede gültige kennung durch
wurzel = neue_wurzel(())
klasse, fehler = definiere("Frei", (wurzel,), {"kennung": "frei", "pruefe": pruefe_ok})
assert fehler is None and len(wurzel) == 1, f"Bei pflicht () soll eine Regel mit kennung und pruefe gelten; Fehler: {fehler!r}."

# Die Objekte der Regeln haben die Methoden der Metaklasse nicht
try:
    len(CpuLast())
    hat_len = True
except TypeError:
    hat_len = False
assert not hat_len and isinstance(CpuLast, Pruefmeta), (
    "len(CpuLast()) soll ein TypeError sein, weil __len__ zur Metaklasse gehört und nur für Klassen gilt."
)

# Viele zufällige Regeln
zufall = Zufall(5013)
for _ in range(100):
    wurzel = neue_wurzel()
    erwartet = []
    kennungen = set()
    for nummer in range(zufall.randint(0, 12)):
        kennung = zufall.choice(["cpu", "ram", "disk", "temp", "", 3])
        mit_pruefe = zufall.random() < 0.85
        namensraum = {"kennung": kennung}
        if mit_pruefe:
            namensraum["pruefe"] = pruefe_ok
        klasse, fehler = definiere(f"R{nummer}", (wurzel,), namensraum)
        gueltig = isinstance(kennung, str) and kennung != "" and mit_pruefe and kennung not in kennungen
        if gueltig:
            kennungen.add(kennung)
            erwartet.append(klasse)
        assert (fehler is None) == gueltig, (
            f"Regel R{nummer} mit kennung {kennung!r}, pruefe {'vorhanden' if mit_pruefe else 'fehlt'}, bisher vergeben "
            f"{sorted(kennungen)}: erwartet {'kein' if gueltig else 'ein'} TypeError, bekommen {fehler!r}."
        )
    assert list(wurzel) == erwartet, f"Das Verzeichnis ist {list(wurzel)!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 10 000 Regeln in einer Wurzel
wurzel = neue_wurzel()
for nummer in range(10000):
    definiere(f"R{nummer}", (wurzel,), {"kennung": f"k{nummer}", "pruefe": pruefe_ok})
assert len(wurzel) == 10000 and wurzel["k9999"].__name__ == "R9999" and list(wurzel)[0].__name__ == "R0", (
    f"Nach 10 000 Regeln ergibt len(wurzel) {len(wurzel)}; erwartet waren 10 000, die erste R0, die letzte R9999."
)
