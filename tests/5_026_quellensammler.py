# Automatisch erzeugt aus lehrkraft/muster/5_026_quellensammler.py - nicht von Hand ändern.
# vorlage-hash: f04c6b4cfb13b6d4
# text-hash: 5bbf0be596d91db4
# thema: fehler
# inhalt: contextlib.ExitStack

def lauf(daten):
    """Ruft sammle mit Quellen aus [(name, werte), …] auf.

    Gibt (Ergebnis oder None, herausgekommene Ausnahme oder None, protokoll) zurück.
    """
    protokoll = []
    quellen = [Datenquelle(name, werte, protokoll) for name, werte in daten]
    try:
        return sammle(quellen, protokoll), None, protokoll
    except Exception as fehler:
        return None, fehler, protokoll


def erwartetes_protokoll(daten):
    """Vergleichslösung: welches Protokoll beim Sammeln entstehen muss."""
    eintraege = []
    offen = []
    for name, werte in daten:
        if werte is None:
            eintraege.append(f"Fehler {name}")
            break
        eintraege.append(f"auf {name}")
        offen.append(name)
    for name in reversed(offen):
        eintraege.append(f"zu {name}")
    eintraege.append("Auswertung beendet")
    return eintraege


def erwartetes_ergebnis(daten):
    """Vergleichslösung: sortierte Werte, oder None, wenn eine Quelle fehlt."""
    alle = []
    for _, werte in daten:
        if werte is None:
            return None
        alle = alle + werte
    return sorted(alle)


BEISPIEL = [("WWS", [30, 12]), ("MES", [25])]

# Das Beispiel liefert die sortierten Werte
ergebnis, fehler, protokoll = lauf(BEISPIEL)
assert ergebnis == [12, 25, 30], (
    f"sammle mit WWS [30, 12] und MES [25] ergibt {ergebnis!r}"
    + (f" (Ausnahme {fehler!r})" if fehler else "")
    + ", erwartet war [12, 25, 30]."
)

# Alle Quellen werden geöffnet und wieder geschlossen
ergebnis, fehler, protokoll = lauf(BEISPIEL)
geoeffnet = [eintrag for eintrag in protokoll if eintrag.startswith("auf ")]
geschlossen = [eintrag for eintrag in protokoll if eintrag.startswith("zu ")]
assert geoeffnet == ["auf WWS", "auf MES"] and sorted(geschlossen) == ["zu MES", "zu WWS"], (
    f"Beim Beispiel ist das Protokoll {protokoll!r}; erwartet war, dass WWS und MES geöffnet und beide wieder "
    "geschlossen werden.\nTipp: stapel.enter_context(quelle) öffnet die Quelle und merkt sie zum Schließen vor."
)

# Geschlossen wird in umgekehrter Reihenfolge
ergebnis, fehler, protokoll = lauf(BEISPIEL)
geschlossen = [eintrag for eintrag in protokoll if eintrag.startswith("zu ")]
assert geschlossen == ["zu MES", "zu WWS"], f"Beim Beispiel werden die Quellen so geschlossen: {geschlossen!r}, erwartet war ['zu MES', 'zu WWS']."

# Das ganze Protokoll des Beispiels, "Auswertung beendet" ganz zum Schluss
ergebnis, fehler, protokoll = lauf(BEISPIEL)
assert protokoll == erwartetes_protokoll(BEISPIEL), (
    f"Beim Beispiel ist das Protokoll {protokoll!r}, erwartet war {erwartetes_protokoll(BEISPIEL)!r}.\n"
    "Tipp: Legen Sie den Eintrag mit stapel.callback(protokoll.append, ...) als Erstes auf den Stapel, "
    "dann wird er als Letztes ausgeführt."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar(
    "[12, 25, 30]\n['auf WWS', 'auf MES', 'zu MES', 'zu WWS', 'Auswertung beendet']"
), (
    "Erwartete Ausgabe:\n[12, 25, 30]\n['auf WWS', 'auf MES', 'zu MES', 'zu WWS', 'Auswertung beendet']\n"
    f"Ihr Programm:\n{AUSGABE}"
)

# Drei Quellen (nicht fest hinschreiben!)
daten = [("WWS", [5, 1]), ("MES", []), ("Versand", [3, 3, 9])]
ergebnis, fehler, protokoll = lauf(daten)
assert (ergebnis, protokoll) == (erwartetes_ergebnis(daten), erwartetes_protokoll(daten)), (
    f"sammle mit {daten}: erwartet {erwartetes_ergebnis(daten)!r} und Protokoll {erwartetes_protokoll(daten)!r},\n"
    f"bekommen {ergebnis!r}" + (f" (Ausnahme {fehler!r})" if fehler else "") + f" und Protokoll {protokoll!r}."
)

# Keine Quellen: leeres Ergebnis, nur der Schlusseintrag
ergebnis, fehler, protokoll = lauf([])
assert ergebnis == [] and protokoll == ["Auswertung beendet"], (
    f"sammle([], protokoll) ergibt {ergebnis!r}" + (f" (Ausnahme {fehler!r})" if fehler else "")
    + f" mit Protokoll {protokoll!r}, erwartet war [] mit Protokoll ['Auswertung beendet']."
)

# Eine nicht erreichbare Quelle: der ConnectionError kommt heraus
daten = [("WWS", [5]), ("MES", None), ("Versand", [1])]
ergebnis, fehler, protokoll = lauf(daten)
assert isinstance(fehler, ConnectionError), (
    f"sammle mit {daten} (MES nicht erreichbar) muss einen ConnectionError weiterlaufen lassen; "
    f"bekommen: Ergebnis {ergebnis!r}, Ausnahme {fehler!r}."
)

# Bei einer nicht erreichbaren Quelle werden die schon geöffneten geschlossen
daten = [("WWS", [5]), ("Lager", [2]), ("MES", None), ("Versand", [1])]
ergebnis, fehler, protokoll = lauf(daten)
if protokoll[:-1] == erwartetes_protokoll(daten)[:-1]:
    hinweis = (
        'Tipp: "Auswertung beendet" fehlt, wenn der ConnectionError den Block verlässt. Mit '
        "stapel.callback(...) wird es auch dann ausgeführt."
    )
else:
    hinweis = "Tipp: Öffnen Sie alle Quellen innerhalb von with ExitStack() as stapel: mit stapel.enter_context(quelle)."
assert protokoll == erwartetes_protokoll(daten), (
    f"sammle mit {daten} (MES nicht erreichbar): erwartet Protokoll {erwartetes_protokoll(daten)!r}, "
    f"bekommen {protokoll!r}.\n{hinweis}"
)

# Die erste Quelle ist nicht erreichbar
daten = [("WWS", None), ("MES", [1])]
ergebnis, fehler, protokoll = lauf(daten)
assert isinstance(fehler, ConnectionError) and protokoll == erwartetes_protokoll(daten), (
    f"sammle mit {daten}: erwartet ConnectionError und Protokoll {erwartetes_protokoll(daten)!r}, "
    f"bekommen Ausnahme {fehler!r} und Protokoll {protokoll!r}."
)

# Ein ExitStack wird benutzt
assert verwendet("ExitStack") and verwendet("enter_context"), (
    "Öffnen Sie die Quellen mit with ExitStack() as stapel: und stapel.enter_context(quelle)."
)

# Viele zufällige Quellenlisten
zufall = Zufall(5026)
for runde in range(300):
    daten = []
    for nummer in range(zufall.randint(0, 6)):
        if zufall.random() < 0.12:
            werte = None
        else:
            werte = [zufall.randint(0, 10**6) for _ in range(zufall.randint(0, 5))]
        daten.append((f"Q{nummer}", werte))
    ergebnis, fehler, protokoll = lauf(daten)
    erwartet = erwartetes_ergebnis(daten)
    fehler_ok = isinstance(fehler, ConnectionError) if erwartet is None else fehler is None
    assert ergebnis == erwartet and fehler_ok and protokoll == erwartetes_protokoll(daten), (
        f"sammle mit {daten}:\n  erwartet {erwartet!r}"
        + (" mit ConnectionError" if erwartet is None else "")
        + f", Protokoll {erwartetes_protokoll(daten)!r}\n  bekommen {ergebnis!r}, Ausnahme {fehler!r}, Protokoll {protokoll!r}"
    )

# Obere Grenze: 200 Quellen mit zusammen 100 000 Werten
daten = [(f"Q{nummer}", [zufall.randint(0, 10**6) for _ in range(500)]) for nummer in range(200)]
ergebnis, fehler, protokoll = lauf(daten)
assert ergebnis == erwartetes_ergebnis(daten) and protokoll == erwartetes_protokoll(daten), (
    f"sammle mit 200 Quellen zu je 500 Werten: erwartet 100000 sortierte Werte und {len(erwartetes_protokoll(daten))} "
    f"Protokolleinträge, bekommen {'kein Ergebnis' if ergebnis is None else f'{len(ergebnis)} Werte'}"
    + (f" (Ausnahme {fehler!r})" if fehler else "") + f" und {len(protokoll)} Protokolleinträge."
)
