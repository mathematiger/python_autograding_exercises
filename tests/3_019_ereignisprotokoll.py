# Automatisch erzeugt aus lehrkraft/muster/3_019_ereignisprotokoll.py - nicht von Hand ändern.
# vorlage-hash: 9e091e57189ef3f6
# text-hash: 1dc9047f86e7ab3f
# thema: kontrollfluss
# inhalt: Set Comprehension

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt zurück, ob die Funktion eine Set Comprehension und ob sie eine for-/while-Anweisung enthält."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False, False
    mit_comprehension = False
    mit_schleife = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.SetComp):
            mit_comprehension = True
        if isinstance(knoten, (ast.For, ast.While)):
            mit_schleife = True
    return mit_comprehension, mit_schleife


def beispiel():
    """Baut das Protokoll aus der Aufgabe neu."""
    return [
        (101, "eingang"), (102, "eingang"), (101, "pruefung"),
        (103, "eingang"), (101, "abschluss"), (102, "pruefung"),
        (102, "rueckfrage"), (102, "pruefung"),
    ]


# schritte aus dem Beispiel
protokoll = beispiel()
ergebnis = schritte(protokoll)
erwartet = {"eingang", "pruefung", "abschluss", "rueckfrage"}
assert ergebnis == erwartet, (
    f"schritte(protokoll) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Packen Sie jedes Tupel in fall, schritt aus und sammeln Sie nur schritt in einer Menge."
)

# faelle_mit aus dem Beispiel
ergebnis = faelle_mit(protokoll, "pruefung")
assert ergebnis == {101, 102}, (
    f'faelle_mit(protokoll, "pruefung") ergibt {ergebnis!r}, erwartet war {{101, 102}}.\n'
    "Tipp: Fall 102 wurde zweimal geprüft, kommt in der Menge aber nur einmal vor."
)

# offene_faelle aus dem Beispiel
ergebnis = offene_faelle(protokoll)
assert ergebnis == {102, 103}, (
    f"offene_faelle(protokoll) ergibt {ergebnis!r}, erwartet war {{102, 103}}.\n"
    'Tipp: Gesucht sind alle Fälle minus die Fälle mit "abschluss"; ein Fall mit "eingang" ist deshalb nicht automatisch offen.'
)

# Alle drei geben Mengen zurück
arten = [type(schritte(protokoll)), type(faelle_mit(protokoll, "eingang")), type(offene_faelle(protokoll))]
assert arten == [set, set, set], (
    f"Die drei Funktionen geben {[art.__name__ for art in arten]} zurück, erwartet waren drei Mengen (set).\n"
    "Tipp: {… for … in …} baut eine Menge, […] eine Liste."
)

# Ein Schritt, der nicht vorkommt
ergebnis = faelle_mit(protokoll, "zahlung")
assert ergebnis == set(), f'faelle_mit(protokoll, "zahlung") ergibt {ergebnis!r}, erwartet war die leere Menge set().'

# Ein leeres Protokoll
ergebnis = (schritte([]), faelle_mit([], "eingang"), offene_faelle([]))
assert ergebnis == (set(), set(), set()), (
    f'schritte([]), faelle_mit([], "eingang") und offene_faelle([]) ergeben {ergebnis!r}; '
    "erwartet waren dreimal leere Mengen set()."
)

# Andere Protokolle (nicht fest hinschreiben!)
for eintraege, offen in [
    ([(7, "abschluss")], set()),
    ([(7, "eingang"), (8, "abschluss"), (7, "abschluss")], set()),
    ([(5, "eingang"), (5, "eingang")], {5}),
    ([(10**9, "pruefung"), (1, "abschluss")], {10**9}),
]:
    ergebnis = offene_faelle(eintraege)
    assert ergebnis == offen, f"offene_faelle({eintraege}) ergibt {ergebnis!r}, erwartet war {offen!r}."

# Ein Schritt, der nur ähnlich heißt, zählt nicht
eintraege = [(1, "abschlussvorbereitung"), (2, "abschluss"), (3, "vorabschluss")]
ergebnis = (faelle_mit(eintraege, "abschluss"), offene_faelle(eintraege))
assert ergebnis == ({2}, {1, 3}), (
    f"Bei {eintraege} ergeben faelle_mit(…, 'abschluss') und offene_faelle {ergebnis!r}, erwartet waren {{2}} und {{1, 3}}.\n"
    "Tipp: Vergleichen Sie den Schritt mit ==, nicht mit in."
)

# Das Protokoll bleibt unverändert
protokoll = beispiel()
schritte(protokoll)
faelle_mit(protokoll, "pruefung")
offene_faelle(protokoll)
assert protokoll == beispiel(), f"Nach den Aufrufen ist das Protokoll {protokoll!r}; es soll unverändert bleiben."

# schritte benutzt eine Set Comprehension, keine Schleife
mit_comprehension, mit_schleife = bauweise(schritte)
assert mit_comprehension and not mit_schleife, (
    "schritte soll mit einer Set Comprehension {… for … in …} arbeiten, ohne for- oder "
    f"while-Anweisung; gefunden: Set Comprehension {'ja' if mit_comprehension else 'nein'}, "
    f"Schleife {'ja' if mit_schleife else 'nein'}."
)

# faelle_mit benutzt eine Set Comprehension, keine Schleife
mit_comprehension, mit_schleife = bauweise(faelle_mit)
assert mit_comprehension and not mit_schleife, (
    "faelle_mit soll mit einer Set Comprehension {… for … in …} arbeiten, ohne for- oder "
    f"while-Anweisung; gefunden: Set Comprehension {'ja' if mit_comprehension else 'nein'}, "
    f"Schleife {'ja' if mit_schleife else 'nein'}."
)

# offene_faelle benutzt eine Set Comprehension, keine Schleife
mit_comprehension, mit_schleife = bauweise(offene_faelle)
assert mit_comprehension and not mit_schleife, (
    "offene_faelle soll mit einer Set Comprehension {… for … in …} arbeiten, ohne for- oder "
    f"while-Anweisung; gefunden: Set Comprehension {'ja' if mit_comprehension else 'nein'}, "
    f"Schleife {'ja' if mit_schleife else 'nein'}."
)


# Vergleichslösungen mit Schleifen und Dictionaries
def ergebnisse_von_hand(eintraege, gesucht):
    """Berechnet alle drei Ergebnisse mit einer gewöhnlichen Schleife."""
    alle_schritte = set()
    mit_gesucht = set()
    abgeschlossen = {}
    for fall, schritt in eintraege:
        alle_schritte.add(schritt)
        if schritt == gesucht:
            mit_gesucht.add(fall)
        abgeschlossen[fall] = abgeschlossen.get(fall, False) or schritt == "abschluss"
    offen = set()
    for fall, fertig in abgeschlossen.items():
        if not fertig:
            offen.add(fall)
    return alle_schritte, mit_gesucht, offen


SCHRITTE = ["eingang", "pruefung", "rueckfrage", "zahlung", "abschluss"]


def zufaellige_protokolle():
    """Liefert 300 zufällige Paare (eintraege, gesucht), bei jedem Aufruf dieselben."""
    zufall = Zufall(3019)
    paare = []
    for _ in range(300):
        faelle = zufall.sample(range(1, 50), zufall.randint(0, 5))
        eintraege = [(zufall.choice(faelle), zufall.choice(SCHRITTE)) for _ in range(zufall.randint(0, 12) if faelle else 0)]
        paare.append((eintraege, zufall.choice(SCHRITTE)))
    return paare


# schritte bei 300 zufälligen Protokollen
for eintraege, gesucht in zufaellige_protokolle():
    alle_schritte, mit_gesucht, offen = ergebnisse_von_hand(eintraege, gesucht)
    ergebnis = schritte(eintraege)
    assert ergebnis == alle_schritte, (
        f"Für das Protokoll {eintraege} ergibt schritte {ergebnis!r}, erwartet war {alle_schritte!r}."
    )

# faelle_mit bei 300 zufälligen Protokollen
for eintraege, gesucht in zufaellige_protokolle():
    alle_schritte, mit_gesucht, offen = ergebnisse_von_hand(eintraege, gesucht)
    ergebnis = faelle_mit(eintraege, gesucht)
    assert ergebnis == mit_gesucht, (
        f"Für das Protokoll {eintraege} ergibt faelle_mit(…, {gesucht!r}) {ergebnis!r}, erwartet war {mit_gesucht!r}."
    )

# offene_faelle bei 300 zufälligen Protokollen
for eintraege, gesucht in zufaellige_protokolle():
    alle_schritte, mit_gesucht, offen = ergebnisse_von_hand(eintraege, gesucht)
    ergebnis = offene_faelle(eintraege)
    assert ergebnis == offen, (
        f"Für das Protokoll {eintraege} ergibt offene_faelle {ergebnis!r}, erwartet war {offen!r}."
    )

# An der oberen Grenze: 100 000 Einträge zu 20 000 Fällen; die letzten 2000 Einträge schließen jeden
# dritten ihrer Fälle ab
eintraege = []
for nummer in range(100000):
    fall = (nummer * 7) % 20000 + 10**9 - 20000
    schritt = "abschluss" if nummer >= 98000 and fall % 3 == 0 else SCHRITTE[nummer % 4]
    eintraege.append((fall, schritt))
alle_schritte, mit_gesucht, offen = ergebnisse_von_hand(eintraege, "zahlung")
ergebnis = (schritte(eintraege), faelle_mit(eintraege, "zahlung"), offene_faelle(eintraege))
assert ergebnis == (alle_schritte, mit_gesucht, offen), (
    f"Bei 100 000 Einträgen liefern schritte {len(ergebnis[0])}, faelle_mit {len(ergebnis[1])} und offene_faelle "
    f"{len(ergebnis[2])} Werte; erwartet waren {len(alle_schritte)}, {len(mit_gesucht)} und {len(offen)}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['abschluss', 'eingang', 'pruefung', 'rueckfrage']\n[101, 102]\n[102, 103]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
