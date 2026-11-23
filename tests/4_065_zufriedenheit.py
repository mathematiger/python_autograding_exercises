# Automatisch erzeugt aus lehrkraft/muster/4_065_zufriedenheit.py - nicht von Hand ändern.
# vorlage-hash: be553c6724a61d9f
# text-hash: 6eedf5305d86747a
# thema: funktionen
# inhalt: itemgetter, attrgetter, methodcaller

EINSAETZE = [Einsatz("Ada", "Meyer", 45, 2), Einsatz("Bo", "Kraus", 120, 4), Einsatz("Ada", "Lenz", 30, 4)]
ZEILEN = [{"kunde": "Meyer", "note": 2, "kommentar": "Top"}, {"kunde": "Kraus", "note": 4, "kommentar": "zu spät"}]
FELDER = ["techniker", "kunde", "minuten", "note"]


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_sortiert(einsaetze, felder):
    """Vergleichslösung: sortiert stabil nacheinander nach jedem Feld, vom letzten zum ersten."""
    ergebnis = list(einsaetze)
    for feld in reversed(felder):
        ergebnis.sort(key=lambda einsatz: getattr(einsatz, feld))
    return ergebnis


def vergleich_bereinigt(kommentare, schritte):
    """Vergleichslösung mit getattr statt methodcaller."""
    ergebnis = []
    for kommentar in kommentare:
        for name, *argumente in schritte:
            kommentar = getattr(kommentar, name)(*argumente)
        ergebnis.append(kommentar)
    return ergebnis


def zufallseinsatz(zufall):
    """Erzeugt einen Einsatz mit wenigen verschiedenen Werten, damit Gleichstände vorkommen."""
    return Einsatz(
        zufall.choice(["Ada", "Bo", "Cem"]), zufall.choice(["Meyer", "Kraus", "Lenz"]),
        zufall.choice([15, 30, 45]), zufall.randint(1, 6),
    )


# sortiert: nach einem Feld
ergebnis = wert_von(sortiert, EINSAETZE, "minuten")
erwartet = [EINSAETZE[2], EINSAETZE[0], EINSAETZE[1]]
assert ergebnis == erwartet, (
    f"sortiert(einsaetze, 'minuten') ergibt\n  {ergebnis!r}\nerwartet war\n  {erwartet!r}\n"
    "Tipp: sorted(einsaetze, key=attrgetter(...))."
)

# sortiert: das Beispiel nach zwei Feldern
ergebnis = wert_von(sortiert, EINSAETZE, "note", "minuten")
erwartet = [EINSAETZE[0], EINSAETZE[2], EINSAETZE[1]]
assert ergebnis == erwartet, (
    f"sortiert(einsaetze, 'note', 'minuten') ergibt\n  {ergebnis!r}\nerwartet war\n  {erwartet!r}\n"
    "Tipp: attrgetter(*felder) bekommt alle Namen und liefert ein Tupel, das nach allen Feldern sortiert."
)

# sortiert: nach Texten und in anderer Reihenfolge der Felder (nicht fest hinschreiben!)
ergebnis = wert_von(sortiert, EINSAETZE, "techniker", "kunde")
erwartet = [EINSAETZE[2], EINSAETZE[0], EINSAETZE[1]]
assert ergebnis == erwartet, f"sortiert(einsaetze, 'techniker', 'kunde') ergibt\n  {ergebnis!r}\nerwartet war\n  {erwartet!r}"

# sortiert: Gleichstand behält die Reihenfolge
gleich = [Einsatz("Ada", "Meyer", 30, 3), Einsatz("Bo", "Kraus", 30, 3)]
ergebnis = wert_von(sortiert, gleich, "minuten", "note")
assert ergebnis == gleich, f"sortiert({gleich!r}, 'minuten', 'note') ergibt {ergebnis!r}; die Reihenfolge sollte bleiben."

# sortiert: neue Liste, die alte bleibt
liste = list(EINSAETZE)
ergebnis = wert_von(sortiert, liste, "note")
assert liste == EINSAETZE and ergebnis is not liste, (
    "sortiert soll eine neue Liste zurückgeben und die übergebene nicht verändern; benutzen Sie sorted statt sort."
)

# sortiert benutzt attrgetter
assert verwendet("attrgetter"), "Ihr Code verwendet attrgetter nicht. Sortieren Sie mit key=attrgetter(*felder)."

# spalten: zwei Schlüssel wie im Beispiel
ergebnis = wert_von(spalten, ZEILEN, "note", "kunde")
assert ergebnis == [(2, "Meyer"), (4, "Kraus")], (
    f"spalten(zeilen, 'note', 'kunde') ergibt {ergebnis!r}, erwartet war [(2, 'Meyer'), (4, 'Kraus')].\n"
    "Tipp: itemgetter(*schluessel)(zeile) liefert die Werte als Tupel."
)

# spalten: drei Schlüssel in anderer Reihenfolge
ergebnis = wert_von(spalten, ZEILEN, "kommentar", "kunde", "note")
assert ergebnis == [("Top", "Meyer", 2), ("zu spät", "Kraus", 4)], (
    f"spalten(zeilen, 'kommentar', 'kunde', 'note') ergibt {ergebnis!r}, "
    "erwartet war [('Top', 'Meyer', 2), ('zu spät', 'Kraus', 4)]."
)

# spalten: mit einem Schlüssel trotzdem Tupel
ergebnis = wert_von(spalten, ZEILEN, "kunde")
assert ergebnis == [("Meyer",), ("Kraus",)], (
    f"spalten(zeilen, 'kunde') ergibt {ergebnis!r}, erwartet war [('Meyer',), ('Kraus',)].\n"
    "Tipp: Mit nur einem Namen liefert itemgetter den Wert selbst, kein Tupel; packen Sie ihn in (wert,)."
)

# spalten: keine Zeilen
ergebnis = wert_von(spalten, [], "kunde")
assert ergebnis == [], f"spalten([], 'kunde') ergibt {ergebnis!r}, erwartet war []."

# spalten benutzt itemgetter
assert verwendet("itemgetter"), "Ihr Code verwendet itemgetter nicht. Holen Sie die Werte mit itemgetter(*schluessel)."

# bereinigt: ein einzelner Schritt
ergebnis = wert_von(bereinigt, ["  Top ", "gut"], ("strip",))
assert ergebnis == ["Top", "gut"], (
    f"bereinigt(['  Top ', 'gut'], ('strip',)) ergibt {ergebnis!r}, erwartet war ['Top', 'gut'].\n"
    "Tipp: methodcaller(*schritt) baut aus ('strip',) eine Funktion, die strip() aufruft."
)

# bereinigt: das Beispiel mit drei Schritten
ergebnis = wert_von(bereinigt, ["  Sehr GUT ", "schnell-und-nett"], ("strip",), ("lower",), ("replace", "-", " "))
assert ergebnis == ["sehr gut", "schnell und nett"], (
    f"bereinigt mit strip, lower und replace ergibt {ergebnis!r}, erwartet war ['sehr gut', 'schnell und nett'].\n"
    "Tipp: Wenden Sie jeden Schritt auf das Ergebnis des vorigen an und reichen Sie die Argumente mit weiter."
)

# bereinigt: die Reihenfolge der Schritte zählt
ergebnis = wert_von(bereinigt, ["a-b"], ("replace", "-", "_"), ("upper",), ("replace", "A", "x"))
assert ergebnis == ["x_B"], (
    f"bereinigt(['a-b'], ('replace', '-', '_'), ('upper',), ('replace', 'A', 'x')) ergibt {ergebnis!r}, "
    "erwartet war ['x_B'].\nTipp: Die Schritte kommen in der angegebenen Reihenfolge dran."
)

# bereinigt: ohne Schritte bleiben die Kommentare, wie sie sind
ergebnis = wert_von(bereinigt, [" A ", "b"])
assert ergebnis == [" A ", "b"], f"bereinigt([' A ', 'b']) ohne Schritte ergibt {ergebnis!r}, erwartet war [' A ', 'b']."

# bereinigt: keine Kommentare
ergebnis = wert_von(bereinigt, [], ("strip",))
assert ergebnis == [], f"bereinigt([], ('strip',)) ergibt {ergebnis!r}, erwartet war []."

# bereinigt verändert die Liste nicht
kommentare = [" A ", " b "]
wert_von(bereinigt, kommentare, ("strip",))
assert kommentare == [" A ", " b "], f"Nach bereinigt ist die Liste {kommentare!r}; sie sollte unverändert bleiben."

# bereinigt benutzt methodcaller
assert verwendet("methodcaller"), "Ihr Code verwendet methodcaller nicht. Bauen Sie jeden Schritt mit methodcaller(*schritt)."

# Die Ausgabe des Programms
erwartet = (
    "\n".join(str(einsatz) for einsatz in [EINSAETZE[0], EINSAETZE[2], EINSAETZE[1]])
    + "\n[(2, 'Meyer'), (4, 'Kraus')]\n['sehr gut', 'schnell und nett']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Sortierungen
zufall = Zufall(4065)
for _ in range(300):
    einsaetze = [zufallseinsatz(zufall) for _ in range(zufall.randint(0, 8))]
    felder = zufall.sample(FELDER, zufall.randint(1, 4))
    ergebnis = wert_von(sortiert, einsaetze, *felder)
    erwartet = vergleich_sortiert(einsaetze, felder)
    assert ergebnis == erwartet, f"sortiert({einsaetze!r}, *{felder}) ergibt\n  {ergebnis!r}\nerwartet war\n  {erwartet!r}"

# Viele zufällige Spalten
for _ in range(300):
    zeilen = [{"kunde": f"K{zufall.randint(0, 9)}", "note": zufall.randint(1, 6), "minuten": zufall.randint(1, 99)}
              for _ in range(zufall.randint(0, 5))]
    schluessel = zufall.sample(["kunde", "note", "minuten"], zufall.randint(1, 3))
    ergebnis = wert_von(spalten, zeilen, *schluessel)
    erwartet = [tuple(zeile[name] for name in schluessel) for zeile in zeilen]
    assert ergebnis == erwartet, f"spalten({zeilen}, *{schluessel}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige Bereinigungen
moegliche = [("strip",), ("lower",), ("upper",), ("title",), ("replace", " ", ""), ("replace", "-", " "), ("lstrip", "x")]
for _ in range(300):
    kommentare = ["".join(zufall.choice("aB -x") for _ in range(zufall.randint(0, 8))) for _ in range(zufall.randint(0, 4))]
    schritte = [zufall.choice(moegliche) for _ in range(zufall.randint(0, 4))]
    ergebnis = wert_von(bereinigt, kommentare, *schritte)
    erwartet = vergleich_bereinigt(kommentare, schritte)
    assert ergebnis == erwartet, f"bereinigt({kommentare}, *{schritte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 100 000 Einsätze, Zeilen und Kommentare
einsaetze = [zufallseinsatz(zufall) for _ in range(100000)]
assert wert_von(sortiert, einsaetze, "note", "techniker") == vergleich_sortiert(einsaetze, ["note", "techniker"]), (
    "Bei 100 000 Einsätzen stimmt sortiert nicht."
)
zeilen = [{"kunde": "K", "note": nummer % 6 + 1} for nummer in range(100000)]
assert wert_von(spalten, zeilen, "note") == [(nummer % 6 + 1,) for nummer in range(100000)], (
    "Bei 100 000 Zeilen stimmt spalten nicht."
)
kommentare = [" Gut-gemacht "] * 100000
assert wert_von(bereinigt, kommentare, ("strip",), ("lower",)) == ["gut-gemacht"] * 100000, (
    "Bei 100 000 Kommentaren stimmt bereinigt nicht."
)
