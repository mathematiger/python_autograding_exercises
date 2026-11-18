# Automatisch erzeugt aus lehrkraft/muster/5_026_prozessquellen.py - nicht von Hand ändern.
# vorlage-hash: 3b93b40ca8396d51
# text-hash: 8c1cd7f7319f24ec
# thema: fehler
# inhalt: contextlib.ExitStack

class KaputteMessquelle(Messquelle):
    """Eine Quelle, die sich öffnen lässt, aber beim Lesen scheitert."""

    def lies(self):
        """Scheitert immer mit einem OSError."""
        raise OSError(f"{self.name}: Lesefehler")


def auswerten(quellen, protokoll):
    """Ruft durchlaufzeiten auf; liefert (Ergebnis, angekommene Ausnahme oder None)."""
    try:
        return durchlaufzeiten(quellen, protokoll), None
    except Exception as ausnahme:
        return None, ausnahme


def erwartetes_protokoll(namen, geoeffnet):
    """Protokoll, wenn die ersten geoeffnet Quellen aufgehen: auf …, dann zu … rückwärts, dann das Ende."""
    auf = [f"auf {name}" for name in namen[:geoeffnet]]
    zu = [f"zu {name}" for name in reversed(namen[:geoeffnet])]
    return auf + zu + ["Auswertung beendet"]


def durchlauf_von_hand(dauern_je_quelle):
    """Vergleichslösung: summiert Fall für Fall mit Indizes."""
    if not dauern_je_quelle:
        return []
    summen = []
    for fall in range(len(dauern_je_quelle[0])):
        summe = 0
        for dauern in dauern_je_quelle:
            summe = summe + dauern[fall]
        summen.append(summe)
    return summen


BEISPIEL_PROTOKOLL = ["auf Prüfen", "auf Packen", "zu Packen", "zu Prüfen", "Auswertung beendet"]

# Das Beispiel: die Durchlaufzeiten zweier Fälle
protokoll = []
quellen = [Messquelle("Prüfen", [5, 3], protokoll), Messquelle("Packen", [12, 20], protokoll)]
ergebnis, fehler = auswerten(quellen, protokoll)
assert fehler is None and ergebnis == [17, 23], (
    f"durchlaufzeiten für Prüfen [5, 3] und Packen [12, 20] ergibt {ergebnis!r}"
    + (f" mit der Ausnahme {type(fehler).__name__}: {fehler}" if fehler else "")
    + ", erwartet war [17, 23].\nTipp: Eine Quelle muss geöffnet sein (stapel.enter_context(quelle)), bevor lies() geht."
)

# Drei Quellen mit anderen Werten (nicht fest hinschreiben!)
protokoll = []
quellen = [
    Messquelle("Prüfen", [1, 2, 3], protokoll),
    Messquelle("Kommissionieren", [10, 20, 30], protokoll),
    Messquelle("Verpacken", [100, 200, 300], protokoll),
]
ergebnis, fehler = auswerten(quellen, protokoll)
assert fehler is None and ergebnis == [111, 222, 333], (
    f"durchlaufzeiten für drei Quellen [1, 2, 3], [10, 20, 30], [100, 200, 300] ergibt {ergebnis!r}"
    + (f" mit der Ausnahme {type(fehler).__name__}: {fehler}" if fehler else "")
    + ", erwartet war [111, 222, 333]."
)

# Alle Quellen werden geöffnet und wieder geschlossen
protokoll = []
quellen = [Messquelle("Prüfen", [5, 3], protokoll), Messquelle("Packen", [12, 20], protokoll)]
auswerten(quellen, protokoll)
geoeffnet = sorted(eintrag for eintrag in protokoll if eintrag.startswith("auf "))
geschlossen = sorted(eintrag for eintrag in protokoll if eintrag.startswith("zu "))
assert geoeffnet == ["auf Packen", "auf Prüfen"] and geschlossen == ["zu Packen", "zu Prüfen"], (
    f"Im Beispiel soll jede Quelle einmal geöffnet und einmal geschlossen werden; Protokoll: {protokoll!r}.\n"
    "Tipp: enter_context sorgt dafür, dass der ExitStack beim Verlassen __exit__ jeder Quelle aufruft."
)

# Geöffnet in der Reihenfolge der Liste, geschlossen rückwärts
protokoll = []
quellen = [Messquelle("Prüfen", [5, 3], protokoll), Messquelle("Packen", [12, 20], protokoll)]
auswerten(quellen, protokoll)
ohne_ende = [eintrag for eintrag in protokoll if eintrag != "Auswertung beendet"]
assert ohne_ende == BEISPIEL_PROTOKOLL[:-1], (
    f"Im Beispiel erwartet das Protokoll (ohne den Abschluss) {BEISPIEL_PROTOKOLL[:-1]!r}, bekommen {ohne_ende!r}."
)

# "Auswertung beendet" steht ganz am Ende
protokoll = []
quellen = [Messquelle("Prüfen", [5, 3], protokoll), Messquelle("Packen", [12, 20], protokoll)]
auswerten(quellen, protokoll)
if "Auswertung beendet" in protokoll and protokoll[-1] != "Auswertung beendet":
    hinweis = (
        "\nTipp: Der ExitStack arbeitet rückwärts. Registrieren Sie den callback als Erstes, dann läuft er "
        "nach dem Schließen aller Quellen."
    )
else:
    hinweis = ""
assert protokoll == BEISPIEL_PROTOKOLL, f"Im Beispiel erwartet das Protokoll {BEISPIEL_PROTOKOLL!r}, bekommen {protokoll!r}.{hinweis}"

# Eine Quelle lässt sich nicht öffnen: die schon offenen werden geschlossen, der Fehler kommt an
protokoll = []
quellen = [
    Messquelle("Prüfen", [1], protokoll),
    Messquelle("Packen", [2], protokoll),
    Messquelle("Versand", [3], protokoll, defekt=True),
    Messquelle("Rechnung", [4], protokoll),
]
ergebnis, fehler = auswerten(quellen, protokoll)
erwartet = erwartetes_protokoll(["Prüfen", "Packen", "Versand", "Rechnung"], 2)
assert isinstance(fehler, ConnectionError) and protokoll == erwartet, (
    f"Ist die dritte von vier Quellen defekt, erwartet: ConnectionError beim Aufrufer und das Protokoll "
    f"{erwartet!r}; bekommen: {fehler!r} und {protokoll!r}.\n"
    "Tipp: Öffnen Sie die Quellen innerhalb des with ExitStack() und fangen Sie den Fehler nicht selbst ab."
)

# lies() scheitert: alle Quellen werden geschlossen, der Fehler kommt an
protokoll = []
quellen = [
    Messquelle("Prüfen", [1], protokoll),
    KaputteMessquelle("Packen", [2], protokoll),
    Messquelle("Versand", [3], protokoll),
]
ergebnis, fehler = auswerten(quellen, protokoll)
erwartet = erwartetes_protokoll(["Prüfen", "Packen", "Versand"], 3)
assert isinstance(fehler, OSError) and protokoll == erwartet, (
    f"Scheitert lies() bei der zweiten Quelle, erwartet: OSError beim Aufrufer und das Protokoll {erwartet!r}; "
    f"bekommen: {fehler!r} und {protokoll!r}."
)

# Die Ausnahme kommt unverändert an
protokoll = []
quellen = [Messquelle("Prüfen", [1], protokoll, defekt=True)]
ergebnis, fehler = auswerten(quellen, protokoll)
assert type(fehler) is ConnectionError and str(fehler) == "Prüfen nicht erreichbar", (
    f"Bei einer defekten Quelle soll genau ihr ConnectionError('Prüfen nicht erreichbar') ankommen; bekommen: {fehler!r}.\n"
    "Tipp: Fangen Sie die Ausnahme nicht ab und lösen Sie keine andere aus."
)

# Die erste Quelle ist defekt: nichts zu schließen, aber der Abschluss steht da
protokoll = []
quellen = [Messquelle("Prüfen", [1], protokoll, defekt=True), Messquelle("Packen", [2], protokoll)]
ergebnis, fehler = auswerten(quellen, protokoll)
assert isinstance(fehler, ConnectionError) and protokoll == ["Auswertung beendet"], (
    f"Ist schon die erste Quelle defekt, erwartet: ConnectionError und das Protokoll ['Auswertung beendet']; "
    f"bekommen: {fehler!r} und {protokoll!r}.\n"
    "Tipp: Registrieren Sie den callback vor dem Öffnen der ersten Quelle."
)

# Keine Quellen: leere Liste
protokoll = []
ergebnis, fehler = auswerten([], protokoll)
assert fehler is None and ergebnis == [] and protokoll == ["Auswertung beendet"], (
    f"durchlaufzeiten([], protokoll) ergibt {ergebnis!r}"
    + (f" mit {type(fehler).__name__}: {fehler}" if fehler else "")
    + f" und das Protokoll {protokoll!r}; erwartet war [] und ['Auswertung beendet']."
)

# Quellen ohne Fälle: leere Liste
protokoll = []
quellen = [Messquelle("Prüfen", [], protokoll), Messquelle("Packen", [], protokoll)]
ergebnis, fehler = auswerten(quellen, protokoll)
assert fehler is None and ergebnis == [], f"Zwei Quellen ohne Fälle ergeben {ergebnis!r}, erwartet war []."

# Eine einzige Quelle
protokoll = []
ergebnis, fehler = auswerten([Messquelle("Prüfen", [7, 0, 9], protokoll)], protokoll)
assert fehler is None and ergebnis == [7, 0, 9] and protokoll == erwartetes_protokoll(["Prüfen"], 1), (
    f"Eine einzige Quelle [7, 0, 9] ergibt {ergebnis!r} mit dem Protokoll {protokoll!r}; erwartet war [7, 0, 9] "
    f"und {erwartetes_protokoll(['Prüfen'], 1)!r}."
)

# Nach der Auswertung ist keine Quelle mehr offen
protokoll = []
quellen = [Messquelle(f"Schritt {nummer}", [nummer], protokoll) for nummer in range(5)]
auswerten(quellen, protokoll)
offen = [quelle.name for quelle in quellen if quelle.offen]
assert offen == [], f"Nach durchlaufzeiten sind diese Quellen noch offen: {offen}."

# Ein ExitStack wird benutzt
assert verwendet("ExitStack"), "Benutzen Sie contextlib.ExitStack, um die Quellen zu öffnen und zu schließen."

# Viele zufällige Auswertungen, manche mit defekten oder kaputten Quellen
zufall = Zufall(5026)
for runde in range(300):
    anzahl = zufall.randint(0, 6)
    faelle = zufall.randint(0, 5)
    protokoll = []
    namen = [f"Schritt {nummer}" for nummer in range(anzahl)]
    dauern = [[zufall.randint(0, 100) for _ in range(faelle)] for _ in range(anzahl)]
    art = zufall.choice(["gut", "gut", "defekt", "kaputt"]) if anzahl > 0 else "gut"
    stelle = zufall.randrange(anzahl) if anzahl > 0 else 0
    quellen = []
    for nummer in range(anzahl):
        if art == "defekt" and nummer == stelle:
            quellen.append(Messquelle(namen[nummer], dauern[nummer], protokoll, defekt=True))
        elif art == "kaputt" and nummer == stelle:
            quellen.append(KaputteMessquelle(namen[nummer], dauern[nummer], protokoll))
        else:
            quellen.append(Messquelle(namen[nummer], dauern[nummer], protokoll))
    ergebnis, fehler = auswerten(quellen, protokoll)
    beschreibung = f"{anzahl} Quellen mit {dauern}" + (f", Quelle {stelle} {art}" if art != "gut" else "")
    if art == "gut":
        erwartet = (durchlauf_von_hand(dauern), None, erwartetes_protokoll(namen, anzahl))
    elif art == "defekt":
        erwartet = (None, "ConnectionError", erwartetes_protokoll(namen, stelle))
    else:
        erwartet = (None, "OSError", erwartetes_protokoll(namen, anzahl))
    bekommen = (ergebnis, type(fehler).__name__ if fehler else None, protokoll)
    assert bekommen == erwartet, (
        f"Bei {beschreibung}: erwartet Ergebnis {erwartet[0]!r}, Ausnahme {erwartet[1]}, Protokoll {erwartet[2]!r}; "
        f"bekommen {bekommen[0]!r}, {bekommen[1]}, {bekommen[2]!r}."
    )

# Obere Grenze: 100 Quellen mit je 1000 Fällen bis 10**6
protokoll = []
dauern = [[(quelle * 7919 + fall * 104729) % 1_000_001 for fall in range(1000)] for quelle in range(100)]
namen = [f"Q{nummer}" for nummer in range(100)]
quellen = [Messquelle(namen[nummer], dauern[nummer], protokoll) for nummer in range(100)]
ergebnis, fehler = auswerten(quellen, protokoll)
erwartet = durchlauf_von_hand(dauern)
assert fehler is None and ergebnis == erwartet and protokoll == erwartetes_protokoll(namen, 100), (
    f"Bei 100 Quellen mit je 1000 Fällen erwartet {len(erwartet)} Durchlaufzeiten, die ersten {erwartet[:2]}; "
    f"bekommen {ergebnis[:2] if ergebnis else ergebnis!r}"
    + (f" mit {type(fehler).__name__}: {fehler}" if fehler else "")
    + f"; Protokoll mit {len(protokoll)} Einträgen (erwartet 201)."
)

# Die Ausgabe des Programms stimmt
erwartet = f"[17, 23]\n{BEISPIEL_PROTOKOLL}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"
