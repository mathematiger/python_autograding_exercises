# Automatisch erzeugt aus lehrkraft/muster/4_014_patchstand.py - nicht von Hand ändern.
# vorlage-hash: 837cda54315c135b
# text-hash: aec130537d71d437
# thema: klassen
# inhalt: dataclass: frozen, order, `__post_init__`

import dataclasses

# Version ist eine Datenklasse mit genau diesen Feldern in dieser Reihenfolge
felder = [feld.name for feld in dataclasses.fields(Version)] if dataclasses.is_dataclass(Version) else None
assert felder == ["major", "minor", "patch"], (
    f"Version soll eine Datenklasse mit den Feldern major, minor, patch sein; gefunden: {felder}.\n"
    "Tipp: Schreiben Sie @dataclass(...) über die Klasse und die Felder mit Typangabe in den Klassenkörper."
)

# Felder anlegen und lesen, patch hat den Standardwert 0
v = Version(2, 10, 1)
ohne_patch = Version(3, 4)
ergebnis = (v.major, v.minor, v.patch, ohne_patch.patch, str(v))
assert ergebnis == (2, 10, 1, 0, "2.10.1"), (
    f"Version(2, 10, 1) hat major, minor, patch {ergebnis[:3]}, str ergibt {ergebnis[4]!r}, Version(3, 4).patch "
    f"ist {ergebnis[3]!r}; erwartet war (2, 10, 1), '2.10.1' und 0."
)

# Gleichheit über die Felder
assert Version(2, 1) == Version(2, 1, 0) and Version(2, 1) != Version(2, 1, 1), (
    "Version(2, 1) soll gleich Version(2, 1, 0) und ungleich Version(2, 1, 1) sein."
)

# Vergleichen wie Zahlen, nicht wie Texte
paare = [
    (Version(2, 9), Version(2, 10)),
    (Version(1, 99, 99), Version(2, 0)),
    (Version(2, 10, 1), Version(2, 10, 2)),
    (Version(0, 0, 0), Version(0, 0, 1)),
]
for kleiner, groesser in paare:
    try:
        ergebnis = (kleiner < groesser, kleiner <= groesser, groesser > kleiner, groesser >= kleiner, groesser < kleiner)
    except TypeError as fehler:
        ergebnis = fehler
    assert ergebnis == (True, True, True, True, False), (
        f"Für {kleiner!r} und {groesser!r} ergeben <, <=, >, >= und das umgekehrte < {ergebnis!r}, erwartet war "
        "(True, True, True, True, False).\nTipp: order=True im Dekorator erzeugt die Vergleiche; verglichen wird "
        "Feld für Feld in der Reihenfolge der Klasse."
    )

# Gleiche Versionen sind <= und >=, aber nicht <
v = Version(5, 5, 5)
w = Version(5, 5, 5)
assert (v <= w, v >= w, v < w, v > w) == (True, True, False, False), (
    "Für zwei gleiche Versionen 5.5.5 sollen <= und >= True sein, < und > False."
)

# Sortieren ohne key
versionen = [Version(2, 10, 1), Version(2, 9, 3), Version(10, 0), Version(2, 9)]
ergebnis = [str(version) for version in sorted(versionen)]
assert ergebnis == ["2.9.0", "2.9.3", "2.10.1", "10.0.0"], (
    f"sorted(...) ergibt {ergebnis}, erwartet war ['2.9.0', '2.9.3', '2.10.1', '10.0.0']."
)

# Versionen sind unveränderlich
v = Version(2, 10, 1)
try:
    v.patch = 2
    fehler = None
except AttributeError as ausnahme:
    fehler = ausnahme
assert fehler is not None and v.patch == 1, (
    f"v.patch = 2 soll einen FrozenInstanceError auslösen und nichts ändern; Ausnahme: {fehler!r}, patch danach: "
    f"{v.patch!r}.\nTipp: frozen=True im Dekorator."
)

# Versionen lassen sich in Mengen und als Schlüssel verwenden
try:
    menge = {Version(2, 1), Version(2, 1, 0), Version(2, 2)}
    zaehler = {Version(1, 0): "alt"}
    ergebnis = (len(menge), zaehler.get(Version(1, 0, 0)))
except TypeError as ausnahme:
    ergebnis = ausnahme
assert ergebnis == (2, "alt"), (
    f"{{Version(2, 1), Version(2, 1, 0), Version(2, 2)}} und das Nachschlagen von Version(1, 0, 0) ergeben "
    f"{ergebnis!r}, erwartet war (2, 'alt').\nTipp: Mit frozen=True bekommt die Datenklasse ein __hash__."
)

# Ungültige Felder lösen einen ValueError aus
for argumente in [(1, -1), (-1, 0), (1, 0, -1), (1.5, 0), (1, "2"), (True, 0), (1, 0, False), (1, 2.0), (-10**6, 0)]:
    try:
        Version(*argumente)
        geklappt = True
    except ValueError:
        geklappt = False
    assert not geklappt, (
        f"Version{argumente} muss einen ValueError auslösen.\n"
        "Tipp: Prüfen Sie in __post_init__ jedes der drei Felder mit type(wert) is int und wert >= 0."
    )

# Die Ränder 0 und 10**6 sind gültig
try:
    ergebnis = str(Version(0, 0, 0)) + " " + str(Version(10**6, 10**6, 10**6))
except ValueError as ausnahme:
    ergebnis = ausnahme
assert ergebnis == "0.0.0 1000000.1000000.1000000", (
    f"Version(0, 0, 0) und Version(10**6, 10**6, 10**6) sollen gültig sein; ergeben {ergebnis!r}.\n"
    "Tipp: Ungültig sind nur negative Zahlen, 0 ist erlaubt."
)

# Schlüsselwort-Argumente
v = Version(major=4, patch=7, minor=2)
assert str(v) == "4.2.7", f"Version(major=4, patch=7, minor=2) ergibt {str(v)!r}, erwartet war '4.2.7'."

# veraltet aus dem Beispiel
server = {"web01": Version(2, 9, 3), "db01": Version(2, 10, 1), "mail": Version(1, 4, 0)}
ergebnis = veraltet(server, Version(2, 10))
assert ergebnis == ["mail", "web01"], (
    f"veraltet(server, Version(2, 10)) ergibt {ergebnis!r}, erwartet war ['mail', 'web01'] (alphabetisch)."
)

# Genau die Mindestversion ist nicht veraltet; kein Server und alle Server
for mindest, erwartet in [(Version(2, 10, 1), ["mail", "web01"]), (Version(1, 4), []), (Version(3, 0), ["db01", "mail", "web01"])]:
    ergebnis = veraltet(server, mindest)
    assert ergebnis == erwartet, f"veraltet(server, {mindest!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ohne Server
assert veraltet({}, Version(1, 0)) == [], f"veraltet({{}}, Version(1, 0)) ergibt {veraltet({}, Version(1, 0))!r}, erwartet war []."

# 300 zufällige Rechenzentren, verglichen mit Tupeln
zufall = Zufall(4014)
for _ in range(300):
    server = {}
    tupel = {}
    for nummer in range(zufall.randint(0, 8)):
        zahlen = (zufall.randint(0, 3), zufall.choice([zufall.randint(0, 12), 9, 10]), zufall.randint(0, 3))
        name = zufall.choice(["web", "db", "mail", "app", "dns"]) + f"{nummer:02d}"
        server[name] = Version(*zahlen)
        tupel[name] = zahlen
    mindest = (zufall.randint(0, 3), zufall.randint(0, 12), zufall.randint(0, 3))
    erwartet = sorted(name for name, zahlen in tupel.items() if zahlen < mindest)
    ergebnis = veraltet(server, Version(*mindest))
    assert ergebnis == erwartet, (
        f"veraltet({server!r}, {Version(*mindest)!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    )
    erwartet_sortiert = sorted(tupel.values())
    ergebnis_sortiert = [(v.major, v.minor, v.patch) for v in sorted(server.values())]
    assert ergebnis_sortiert == erwartet_sortiert, (
        f"sorted({list(server.values())!r}) ergibt die Reihenfolge {ergebnis_sortiert}, erwartet war {erwartet_sortiert}."
    )

# An der oberen Grenze: 100 000 Server
server = {f"srv{nummer:06d}": Version(nummer % 3, nummer % 17, nummer % 5) for nummer in range(100000)}
ergebnis = veraltet(server, Version(1, 0))
anzahl_erwartet = len([nummer for nummer in range(100000) if nummer % 3 == 0])
assert len(ergebnis) == anzahl_erwartet and ergebnis[:2] == ["srv000000", "srv000003"] and ergebnis[-1] == "srv099999", (
    f"Bei 100 000 Servern liefert veraltet(server, Version(1, 0)) {len(ergebnis)} Namen, die ersten {ergebnis[:2]}, "
    f"erwartet waren {anzahl_erwartet} Namen, beginnend mit ['srv000000', 'srv000003']."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "['mail', 'web01']\n1.4.0, 2.9.3, 2.10.1"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
