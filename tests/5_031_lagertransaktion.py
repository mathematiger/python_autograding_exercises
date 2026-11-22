# Automatisch erzeugt aus lehrkraft/muster/5_031_lagertransaktion.py - nicht von Hand ändern.
# vorlage-hash: 7b2beaf565748666
# text-hash: 8de2fd699234db2a
# thema: fehler
# inhalt: contextmanager mit Fehlerpfad

def lauf(tabelle, block):
    """Führt block(tab) in einer Transaktion aus.

    Gibt (protokoll, herausgekommene Ausnahme oder None, Wert hinter as) zurück.
    """
    protokoll = []
    hinter_as = []
    try:
        with transaktion(tabelle, protokoll) as tab:
            hinter_as.append(tab)
            block(tab)
    except Exception as fehler:
        return protokoll, fehler, hinter_as[0] if hinter_as else None
    return protokoll, None, hinter_as[0] if hinter_as else None


def wirf(ausnahme):
    """Löst die Ausnahme aus; für Lambdas, in denen raise nicht erlaubt ist."""
    raise ausnahme


def aendern_und(fehler):
    """Ein Block, der den Bestand verändert, einen Artikel löscht und einen anlegt, dann fehler auslöst (oder nicht)."""

    def block(tab):
        """Verändert tab und löst danach eventuell fehler aus."""
        tab["A-1"] = 99
        del tab["B-2"]
        tab["NEU"] = 1
        if fehler is not None:
            raise fehler

    return block


def vergleich_import(tabelle, lieferungen):
    """Vergleichslösung ohne Kontextmanager: prüft jede Lieferung an einer Kopie."""
    uebernommen = 0
    protokoll = []
    for lieferung in lieferungen:
        kopie = dict(tabelle)
        protokoll.append("BEGIN")
        gueltig = True
        for artikel, menge in lieferung:
            kopie[artikel] = kopie.get(artikel, 0) + menge
            if kopie[artikel] < 0:
                gueltig = False
                break
        if gueltig:
            tabelle.clear()
            tabelle.update(kopie)
            uebernommen += 1
            protokoll.append("COMMIT")
        else:
            protokoll.append("ROLLBACK")
    return uebernommen, protokoll


# transaktion ohne Fehler: BEGIN, COMMIT, die Änderung bleibt
lager = {"A-1": 5, "B-2": 0}
protokoll, fehler, tab = lauf(lager, lambda tab: tab.update({"A-1": 4}))
assert (protokoll, fehler, lager) == (["BEGIN", "COMMIT"], None, {"A-1": 4, "B-2": 0}), (
    f"Ein Block, der A-1 auf 4 setzt, ergibt Protokoll {protokoll!r}, Ausnahme {fehler!r} und Lager {lager!r}; "
    "erwartet war ['BEGIN', 'COMMIT'], None und {'A-1': 4, 'B-2': 0}."
)

# transaktion gibt die Tabelle selbst an as weiter
lager = {"A-1": 5}
protokoll, fehler, tab = lauf(lager, lambda tab: None)
assert tab is lager, f"Hinter as steht {tab!r}, erwartet war das Dictionary tabelle selbst.\nTipp: yield tabelle."

# transaktion mit Abbruch: zurückrollen und die Ausnahme schlucken
lager = {"A-1": 5, "B-2": 0}
protokoll, fehler, tab = lauf(lager, aendern_und(Abbruch("zu wenig")))
assert (protokoll, fehler) == (["BEGIN", "ROLLBACK"], None), (
    f"Bei Abbruch im Block ergibt sich Protokoll {protokoll!r} und Ausnahme {fehler!r}; erwartet war "
    "['BEGIN', 'ROLLBACK'] und keine Ausnahme.\nTipp: Fangen Sie Abbruch am yield mit except ab und lösen Sie ihn nicht neu aus."
)

# Nach Abbruch ist der alte Inhalt wieder da, auch gelöschte und neue Artikel
lager = {"A-1": 5, "B-2": 0}
lauf(lager, aendern_und(Abbruch("zu wenig")))
assert lager == {"A-1": 5, "B-2": 0}, (
    f"Nach Abbruch ist das Lager {lager!r}, erwartet war wieder {{'A-1': 5, 'B-2': 0}}.\n"
    "Tipp: Sichern Sie vor dem yield eine Kopie, dict(tabelle), und setzen Sie mit clear() und update() zurück."
)

# transaktion mit einem anderen Fehler: zurückrollen und die Ausnahme weiterlaufen lassen
lager = {"A-1": 5, "B-2": 0}
ausloeser = ValueError("Menge kaputt")
protokoll, fehler, tab = lauf(lager, aendern_und(ausloeser))
assert (protokoll, fehler, lager) == (["BEGIN", "ROLLBACK"], ausloeser, {"A-1": 5, "B-2": 0}), (
    f"Bei ValueError im Block ergibt sich Protokoll {protokoll!r}, Ausnahme {fehler!r} und Lager {lager!r}; erwartet "
    "war ['BEGIN', 'ROLLBACK'], derselbe ValueError und {'A-1': 5, 'B-2': 0}.\n"
    "Tipp: Nach dem Zurücksetzen löst raise ohne Argument die Ausnahme erneut aus."
)

# Auch ein KeyError läuft weiter, wird aber zurückgerollt
lager = {"A-1": 5}
protokoll, fehler, tab = lauf(lager, lambda tab: [tab.update({"A-1": 0}), tab["fehlt"]])
assert protokoll == ["BEGIN", "ROLLBACK"] and isinstance(fehler, KeyError) and lager == {"A-1": 5}, (
    f"Bei KeyError im Block ergibt sich Protokoll {protokoll!r}, Ausnahme {fehler!r} und Lager {lager!r}; erwartet "
    "war ['BEGIN', 'ROLLBACK'], ein KeyError und {'A-1': 5}."
)

# Zurückgesetzt wird dasselbe Dictionary-Objekt
lager = {"A-1": 5, "B-2": 0}
referenz = lager
lauf(lager, aendern_und(Abbruch("x")))
assert referenz is lager and referenz == {"A-1": 5, "B-2": 0}, (
    f"Nach dem Zurückrollen sieht eine vorher gemerkte Referenz {referenz!r}, erwartet war {{'A-1': 5, 'B-2': 0}}.\n"
    "Tipp: tabelle = sicherung ändert nur die lokale Variable; ändern Sie das Dictionary selbst mit clear() und update()."
)

# Ein Fehler vor jeder Änderung: ROLLBACK, alles bleibt
lager = {"A-1": 5}
protokoll, fehler, tab = lauf(lager, lambda tab: wirf(RuntimeError("sofort")))
assert protokoll == ["BEGIN", "ROLLBACK"] and isinstance(fehler, RuntimeError) and lager == {"A-1": 5}, (
    f"Bei RuntimeError ganz am Anfang ergibt sich Protokoll {protokoll!r}, Ausnahme {fehler!r} und Lager {lager!r}."
)

# Ein leeres Lager bleibt nach Abbruch leer
lager = {}
lauf(lager, lambda tab: [tab.update({"X": 3}), wirf(Abbruch("x"))])
assert lager == {}, f"Ein leeres Lager ist nach Abbruch {lager!r}, erwartet war {{}}."

# transaktion ist mit contextlib.contextmanager geschrieben: auch als Dekorator wiederverwendbar
lager = {"A-1": 0}
protokoll = []
try:
    @transaktion(lager, protokoll)
    def nachbestellen():
        """Erhöht den Bestand von A-1 um 5."""
        lager["A-1"] += 5

    nachbestellen()
    nachbestellen()
    ergebnis = (protokoll, lager)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == (["BEGIN", "COMMIT", "BEGIN", "COMMIT"], {"A-1": 10}), (
    f"@transaktion(lager, protokoll) über einer Funktion, die zweimal aufgerufen wird, ergibt {ergebnis!r}; erwartet war "
    "(['BEGIN', 'COMMIT', 'BEGIN', 'COMMIT'], {'A-1': 10}).\nTipp: Schreiben Sie transaktion als Generatorfunktion mit "
    "@contextmanager, dann ist jeder Aufruf ein frischer Kontextmanager und zugleich ein Dekorator."
)

# Verschachtelte Transaktionen: die innere rollt nur ihren Teil zurück
lager = {"A-1": 5}
protokoll = []
try:
    with transaktion(lager, protokoll):
        lager["A-1"] = 4
        with transaktion(lager, protokoll):
            lager["A-1"] = -1
            raise Abbruch("innen")
        lager["B-2"] = 1
    ergebnis = (protokoll, lager)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == (["BEGIN", "BEGIN", "ROLLBACK", "COMMIT"], {"A-1": 4, "B-2": 1}), (
    f"Bei einer inneren Transaktion mit Abbruch ergibt sich {ergebnis!r}; erwartet war "
    "(['BEGIN', 'BEGIN', 'ROLLBACK', 'COMMIT'], {'A-1': 4, 'B-2': 1})."
)

# importiere im Beispiel
lager = {"A-1": 5, "B-2": 0}
protokoll = []
ergebnis = importiere(lager, protokoll, [[("A-1", -2), ("B-2", 3)], [("A-1", -9)], [("C-3", 1)]])
assert (ergebnis, lager, protokoll) == (2, {"A-1": 3, "B-2": 3, "C-3": 1}, ["BEGIN", "COMMIT", "BEGIN", "ROLLBACK", "BEGIN", "COMMIT"]), (
    f"importiere im Beispiel ergibt {ergebnis!r}, Lager {lager!r} und Protokoll {protokoll!r}; erwartet war 2, "
    "{'A-1': 3, 'B-2': 3, 'C-3': 1} und ['BEGIN', 'COMMIT', 'BEGIN', 'ROLLBACK', 'BEGIN', 'COMMIT']."
)

# importiere rollt eine Lieferung ganz zurück, auch Buchungen vor der fehlerhaften
lager = {"A-1": 1}
protokoll = []
ergebnis = importiere(lager, protokoll, [[("NEU", 4), ("A-1", 2), ("A-1", -4)]])
assert (ergebnis, lager) == (0, {"A-1": 1}), (
    f"Eine Lieferung, deren letzte Buchung A-1 auf -1 bringt, ergibt {ergebnis!r} und Lager {lager!r}; erwartet war 0 "
    "und {'A-1': 1}.\nTipp: Lösen Sie Abbruch innerhalb des with-Blocks aus; dann rollt transaktion alles zurück."
)

# importiere: genau 0 ist erlaubt, erst unter 0 wird abgebrochen
lager = {"A-1": 3}
protokoll = []
ergebnis = importiere(lager, protokoll, [[("A-1", -3)], [("B-2", 0)]])
assert (ergebnis, lager) == (2, {"A-1": 0, "B-2": 0}), (
    f"importiere mit [('A-1', -3)] und [('B-2', 0)] ergibt {ergebnis!r} und Lager {lager!r}; erwartet war 2 und "
    "{'A-1': 0, 'B-2': 0}."
)

# importiere ohne Lieferungen und mit leerer Lieferung
lager = {"A-1": 3}
protokoll = []
ergebnis = [importiere(lager, protokoll, []), importiere(lager, protokoll, [[]])]
assert (ergebnis, protokoll, lager) == ([0, 1], ["BEGIN", "COMMIT"], {"A-1": 3}), (
    f"importiere ohne Lieferungen und mit einer leeren Lieferung ergibt {ergebnis!r}, Protokoll {protokoll!r}; "
    "erwartet war [0, 1] und ['BEGIN', 'COMMIT']."
)

# importiere: ein anderer Fehler bricht den Import ab, frühere Lieferungen bleiben
lager = {"A-1": 3}
protokoll = []
try:
    importiere(lager, protokoll, [[("A-1", 1)], [("B-2", 2), ("A-1", "fünf")], [("C-3", 1)]])
    fehler = None
except Exception as gefangen:
    fehler = gefangen
assert isinstance(fehler, TypeError) and lager == {"A-1": 4} and protokoll == ["BEGIN", "COMMIT", "BEGIN", "ROLLBACK"], (
    f"Bei einer Menge 'fünf' in der zweiten Lieferung ergibt sich Ausnahme {fehler!r}, Lager {lager!r} und Protokoll "
    f"{protokoll!r}; erwartet war ein TypeError, {{'A-1': 4}} und ['BEGIN', 'COMMIT', 'BEGIN', 'ROLLBACK']."
)

# Die Ausgabe des Programms
erwartet = "2\n{'A-1': 3, 'B-2': 3, 'C-3': 1}\n['BEGIN', 'COMMIT', 'BEGIN', 'ROLLBACK', 'BEGIN', 'COMMIT']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Importe
zufall = Zufall(5031)
for runde in range(200):
    start = {f"A-{nummer}": zufall.randint(0, 5) for nummer in range(zufall.randint(0, 4))}
    lieferungen = [
        [(f"A-{zufall.randint(0, 5)}", zufall.randint(-4, 4)) for _ in range(zufall.randint(0, 4))]
        for _ in range(zufall.randint(0, 6))
    ]
    lager = dict(start)
    protokoll = []
    ergebnis = importiere(lager, protokoll, lieferungen)
    erwartet_lager = dict(start)
    erwartet_anzahl, erwartet_protokoll = vergleich_import(erwartet_lager, lieferungen)
    assert (ergebnis, lager, protokoll) == (erwartet_anzahl, erwartet_lager, erwartet_protokoll), (
        f"importiere({start}, …, {lieferungen}) ergibt {ergebnis!r}, Lager {lager!r} und Protokoll {protokoll!r}; "
        f"erwartet war {erwartet_anzahl}, {erwartet_lager!r} und {erwartet_protokoll!r}."
    )

# Obere Grenze: 10 000 Artikel, 1000 Lieferungen mit zusammen 100 000 Buchungen
start = {f"A-{nummer}": 50 for nummer in range(10000)}
lieferungen = [[(f"A-{zufall.randrange(10000)}", zufall.randint(-30, 20)) for _ in range(100)] for _ in range(1000)]
lager = dict(start)
protokoll = []
ergebnis = importiere(lager, protokoll, lieferungen)
erwartet_lager = dict(start)
erwartet_anzahl, erwartet_protokoll = vergleich_import(erwartet_lager, lieferungen)
assert (ergebnis, lager == erwartet_lager, len(protokoll)) == (erwartet_anzahl, True, 2000), (
    f"Bei 1000 Lieferungen ergibt importiere {ergebnis!r} übernommene (erwartet {erwartet_anzahl}), "
    f"das Lager stimmt: {lager == erwartet_lager}, das Protokoll hat {len(protokoll)} Einträge (erwartet 2000)."
)
