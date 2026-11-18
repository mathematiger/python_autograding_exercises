# Automatisch erzeugt aus lehrkraft/muster/3_036_testreihenfolge.py - nicht von Hand ändern.
# vorlage-hash: 2debea3c36332e92
# text-hash: 7b2213cb347e57fa
# thema: algorithmen
# inhalt: Permutationen rekursiv

import ast
import inspect
import textwrap


def geordnet(reihenfolgen):
    """Bringt eine Liste von Reihenfolgen in eine feste Ordnung, damit ihre Reihenfolge egal ist."""
    return sorted(tuple(reihenfolge) for reihenfolge in reihenfolgen)


def vergleich_reihenfolgen(entwuerfe):
    """Vergleichslösung ohne Rekursion: jedes Element nacheinander an jeder Stelle einfügen."""
    reihenfolgen = [[]]
    for name in entwuerfe:
        neue = []
        for reihenfolge in reihenfolgen:
            for stelle in range(len(reihenfolge) + 1):
                neue.append(reihenfolge[:stelle] + [name] + reihenfolge[stelle:])
        reihenfolgen = neue
    return reihenfolgen


def vergleich_ohne_nachbarn(entwuerfe, a, b):
    """Vergleichslösung: prüft jedes benachbarte Paar einzeln."""
    passende = []
    for reihenfolge in vergleich_reihenfolgen(entwuerfe):
        nebeneinander = False
        for stelle in range(len(reihenfolge) - 1):
            if {reihenfolge[stelle], reihenfolge[stelle + 1]} == {a, b}:
                nebeneinander = True
        if not nebeneinander:
            passende.append(reihenfolge)
    return passende


def pruefe_reihenfolgen(entwuerfe):
    """Ruft alle_reihenfolgen(entwuerfe) auf und liefert eine Fehlerbeschreibung oder None."""
    ergebnis = alle_reihenfolgen(list(entwuerfe))
    if not isinstance(ergebnis, list) or not all(isinstance(r, list) for r in ergebnis):
        return f"alle_reihenfolgen({entwuerfe!r}) liefert {ergebnis!r}, erwartet war eine Liste von Listen."
    erwartet = geordnet(vergleich_reihenfolgen(entwuerfe))
    bekommen = geordnet(ergebnis)
    if bekommen == erwartet:
        return None
    if len(ergebnis) == len(erwartet):
        text = f"alle_reihenfolgen({entwuerfe!r}) liefert zwar {len(ergebnis)} Reihenfolgen, aber nicht die richtigen."
    else:
        text = f"alle_reihenfolgen({entwuerfe!r}) liefert {len(ergebnis)} Reihenfolgen, erwartet waren {len(erwartet)}."
    if len(set(bekommen)) < len(bekommen):
        text += "\nManche Reihenfolgen kommen mehrfach vor."
    erwartet_menge = set(erwartet)
    bekommen_menge = set(bekommen)
    falsch = [list(r) for r in bekommen if r not in erwartet_menge]
    if falsch:
        text += f"\nDiese Reihenfolgen sind falsch (ein Name fehlt oder steht doppelt): {falsch[:3]}"
    fehlend = [list(r) for r in erwartet if r not in bekommen_menge]
    if fehlend:
        text += f"\nEs fehlen zum Beispiel: {fehlend[:3]}"
    return text


def pruefe_ohne_nachbarn(entwuerfe, a, b):
    """Ruft ohne_nachbarn auf und liefert eine Fehlerbeschreibung oder None."""
    ergebnis = ohne_nachbarn(list(entwuerfe), a, b)
    aufruf = f"ohne_nachbarn({entwuerfe!r}, {a!r}, {b!r})"
    if not isinstance(ergebnis, list) or not all(isinstance(r, list) for r in ergebnis):
        return f"{aufruf} liefert {ergebnis!r}, erwartet war eine Liste von Listen."
    erwartet = geordnet(vergleich_ohne_nachbarn(entwuerfe, a, b))
    bekommen = geordnet(ergebnis)
    if bekommen == erwartet:
        return None
    text = f"{aufruf} liefert {len(ergebnis)} Reihenfolgen, erwartet waren {len(erwartet)}."
    erwartet_menge = set(erwartet)
    bekommen_menge = set(bekommen)
    falsch = [list(r) for r in bekommen if r not in erwartet_menge]
    if falsch:
        text += f"\nDiese gehören nicht dazu: {falsch[:3]}"
        text += f"\nTipp: Stehen {a!r} und {b!r} darin nebeneinander? Auch b direkt vor a zählt."
    fehlend = [list(r) for r in erwartet if r not in bekommen_menge]
    if fehlend:
        text += f"\nEs fehlen zum Beispiel: {fehlend[:3]}"
    return text


def ruft_sich_selbst_auf(funktion):
    """Prüft am Quelltext, ob funktion oder eine darin definierte Hilfsfunktion sich selbst aufruft."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    for definition in ast.walk(baum):
        if isinstance(definition, ast.FunctionDef):
            for knoten in ast.walk(definition):
                if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id == definition.name:
                    return True
    return False


# alle_reihenfolgen: das Beispiel mit zwei Entwürfen
fehler = pruefe_reihenfolgen(["Kacheln", "Liste"])
assert fehler is None, fehler

# alle_reihenfolgen: drei Entwürfe ergeben sechs Reihenfolgen (nicht fest hinschreiben!)
fehler = pruefe_reihenfolgen(["A", "B", "C"])
assert fehler is None, fehler

# alle_reihenfolgen: andere Namen, vier Entwürfe
fehler = pruefe_reihenfolgen(["Kacheln", "Liste", "Karte", "Suche"])
assert fehler is None, fehler

# alle_reihenfolgen: ein Entwurf
fehler = pruefe_reihenfolgen(["Liste"])
assert fehler is None, fehler

# alle_reihenfolgen: keine Entwürfe ergeben eine leere Reihenfolge
ergebnis = alle_reihenfolgen([])
assert ergebnis == [[]], (
    f"alle_reihenfolgen([]) liefert {ergebnis!r}, erwartet war [[]], eine Liste mit der leeren Reihenfolge.\n"
    + ("Tipp: Mit return [] als Abbruchbedingung bleibt jedes Ergebnis leer, weil die Schleife über "
       "alle_reihenfolgen(rest) nie läuft." if ergebnis == [] else "")
)

# alle_reihenfolgen: die Liste entwuerfe bleibt unverändert
entwuerfe = ["A", "B", "C", "D"]
alle_reihenfolgen(entwuerfe)
assert entwuerfe == ["A", "B", "C", "D"], (
    f"Nach alle_reihenfolgen(['A', 'B', 'C', 'D']) ist die Liste {entwuerfe}, erwartet war sie unverändert.\n"
    "Tipp: Bauen Sie den Rest mit Slicing als neue Liste, statt mit remove oder pop aus entwuerfe zu löschen."
)

# alle_reihenfolgen arbeitet rekursiv
assert ruft_sich_selbst_auf(alle_reihenfolgen), (
    "alle_reihenfolgen ruft weder sich selbst noch eine eigene innere Hilfsfunktion rekursiv auf. Lösen Sie die "
    "Aufgabe rekursiv: Für jedes Element vorne braucht man alle Reihenfolgen des Rests."
)

# itertools wird nicht benutzt
assert not verwendet("permutations"), "Ihre Lösung benutzt itertools.permutations. Bauen Sie die Reihenfolgen rekursiv selbst."

# ohne_nachbarn: das Beispiel
fehler = pruefe_ohne_nachbarn(["A", "B", "C"], "A", "B")
assert fehler is None, fehler

# ohne_nachbarn: auch b vor a zählt als nebeneinander
fehler = pruefe_ohne_nachbarn(["A", "B", "C", "D"], "C", "A")
assert fehler is None, fehler

# ohne_nachbarn: bei nur zwei Entwürfen bleibt nichts übrig
ergebnis = ohne_nachbarn(["Kacheln", "Liste"], "Kacheln", "Liste")
assert ergebnis == [], f"ohne_nachbarn(['Kacheln', 'Liste'], 'Kacheln', 'Liste') liefert {ergebnis!r}, erwartet war []."

# Viele zufällige Listen mit bis zu sechs Entwürfen
zufall = Zufall(3036)
namen = ["Kacheln", "Liste", "Karte", "Suche", "Menü", "Wischen", "Raster", "Tabs"]
for runde in range(60):
    entwuerfe = zufall.sample(namen, zufall.randint(0, 6))
    fehler = pruefe_reihenfolgen(entwuerfe)
    assert fehler is None, fehler
    if len(entwuerfe) >= 2:
        a, b = zufall.sample(entwuerfe, 2)
        fehler = pruefe_ohne_nachbarn(entwuerfe, a, b)
        assert fehler is None, fehler

# Obere Grenze: acht Entwürfe, 40 320 Reihenfolgen
fehler = pruefe_reihenfolgen(namen)
assert fehler is None, fehler

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) in (
    vergleichbar("[['Kacheln', 'Liste'], ['Liste', 'Kacheln']]"),
    vergleichbar("[['Liste', 'Kacheln'], ['Kacheln', 'Liste']]"),
), f"Erwartete Ausgabe: [['Kacheln', 'Liste'], ['Liste', 'Kacheln']] – Ihr Programm: \"{AUSGABE}\""
