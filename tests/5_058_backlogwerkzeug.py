# Automatisch erzeugt aus lehrkraft/muster/5_058_backlogwerkzeug.py - nicht von Hand ändern.
# vorlage-hash: 615e9ebaa75d1941
# text-hash: a34f27e7f4090ef1
# thema: algorithmen
# inhalt: Kosten eingebauter Operationen

import ast
import inspect


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def vergleich_offen(backlog, erledigt):
    """Vergleichslösung: über ein Dictionary statt einer Menge."""
    fertig = dict.fromkeys(erledigt)
    return [kennung for kennung in backlog if kennung not in fertig]


def vergleich_plan(eingaenge):
    """Vergleichslösung: die dringenden rückwärts, dann die normalen vorwärts."""
    dringende = [kennung for kennung, dringend in eingaenge if dringend]
    normale = [kennung for kennung, dringend in eingaenge if not dringend]
    return dringende[::-1] + normale


def vergleich_bericht(aufgaben):
    """Vergleichslösung: Zeilen mit format und join."""
    return "".join("{}: {} ({} SP)\n".format(*aufgabe) for aufgabe in aufgaben)


def kommt_vor(funktion, pruefung):
    """Prüft im Quelltext von funktion, ob ein Knoten des Syntaxbaums pruefung erfüllt."""
    try:
        baum = ast.parse(inspect.getsource(funktion).strip())
    except (OSError, TypeError, SyntaxError):
        return False
    return any(pruefung(knoten) for knoten in ast.walk(baum))


def ruft_methode(name):
    """Liefert eine Prüfung für kommt_vor: ein Aufruf der Methode name."""
    return lambda knoten: isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Attribute) and knoten.func.attr == name


def ist_erweiterte_zuweisung(knoten):
    """Prüfung für kommt_vor: += oder eine andere erweiterte Zuweisung."""
    return isinstance(knoten, ast.AugAssign)


def kennungen(anzahl, praefix="A"):
    """Erzeugt anzahl verschiedene Kennungen."""
    return [f"{praefix}-{nummer}" for nummer in range(anzahl)]


# offene_aufgaben: das Beispiel
ergebnis, fehler = rufe(lambda: offene_aufgaben(["A-1", "A-2", "A-3", "A-4"], ["A-3", "A-1"]))
assert ergebnis == ["A-2", "A-4"], f"offene_aufgaben(['A-1', 'A-2', 'A-3', 'A-4'], ['A-3', 'A-1']) ergibt {ergebnis!r}, erwartet war ['A-2', 'A-4']." + absturz(fehler)

# offene_aufgaben: die Reihenfolge von backlog bleibt
ergebnis, fehler = rufe(lambda: offene_aufgaben(["C-9", "A-1", "B-5", "A-2"], ["A-1"]))
assert ergebnis == ["C-9", "B-5", "A-2"], (
    f"offene_aufgaben(['C-9', 'A-1', 'B-5', 'A-2'], ['A-1']) ergibt {ergebnis!r}, erwartet war ['C-9', 'B-5', 'A-2'] "
    "in der Reihenfolge von backlog.\nTipp: Eine Menge eignet sich zum Nachschauen, aber gehen Sie backlog der Reihe "
    "nach durch, statt mit Mengen zu rechnen." + absturz(fehler)
)

# offene_aufgaben: erledigte Kennungen, die nicht im Backlog stehen, stören nicht
ergebnis, fehler = rufe(lambda: offene_aufgaben(["A-1", "A-2"], ["X-7", "A-2", "X-8"]))
assert ergebnis == ["A-1"], f"offene_aufgaben(['A-1', 'A-2'], ['X-7', 'A-2', 'X-8']) ergibt {ergebnis!r}, erwartet war ['A-1']." + absturz(fehler)

# offene_aufgaben: leere Listen
ergebnis, fehler = rufe(lambda: (offene_aufgaben([], ["A-1"]), offene_aufgaben(["A-1"], []), offene_aufgaben([], [])))
assert ergebnis == ([], ["A-1"], []), f"offene_aufgaben mit leeren Listen ergibt {ergebnis!r}, erwartet war ([], ['A-1'], [])." + absturz(fehler)

# offene_aufgaben: jede Kennung in erledigt wird nur einmal gelesen
backlog = kennungen(2000)
erledigt = Zaehlliste(kennungen(1000))
ergebnis, fehler = rufe(lambda: offene_aufgaben(backlog, erledigt))
assert ergebnis == backlog[1000:] and erledigt.lesezugriffe <= 2 * 1000, (
    f"offene_aufgaben mit 2000 Kennungen im Backlog und 1000 erledigten liest {erledigt.lesezugriffe} Einträge aus "
    "erledigt; erwartet waren höchstens 2000. x in erledigt geht bei jeder Kennung die ganze Liste durch: "
    "O(n · m).\nTipp: Machen Sie aus erledigt einmal vorab eine Menge." + absturz(fehler)
)

# offene_aufgaben: auch backlog wird nur einmal durchlaufen
backlog = Zaehlliste(kennungen(3000))
ergebnis, fehler = rufe(lambda: offene_aufgaben(backlog, ["A-5"]))
assert ergebnis is not None and len(ergebnis) == 2999 and backlog.lesezugriffe <= 2 * 3000, (
    f"offene_aufgaben mit 3000 Kennungen im Backlog liest {backlog.lesezugriffe} Einträge aus backlog; erwartet waren "
    "höchstens 6000." + absturz(fehler)
)

# einplanen: das Beispiel
eingaenge = [("A-1", False), ("A-2", True), ("A-3", False), ("A-4", True)]
ergebnis, fehler = rufe(lambda: einplanen(eingaenge))
assert ergebnis == ["A-4", "A-2", "A-1", "A-3"], (
    f"einplanen({eingaenge}) ergibt {ergebnis!r}, erwartet war ['A-4', 'A-2', 'A-1', 'A-3']: A-4 kam als letzte "
    "dringende Aufgabe und steht ganz vorn." + absturz(fehler)
)

# einplanen: gibt eine Liste zurück, keine deque
ergebnis, fehler = rufe(lambda: einplanen([("B-1", True), ("B-2", False)]))
assert type(ergebnis) is list and ergebnis == ["B-1", "B-2"], (
    f"einplanen([('B-1', True), ('B-2', False)]) ergibt {ergebnis!r}, erwartet war die Liste ['B-1', 'B-2'].\n"
    "Tipp: Machen Sie am Ende mit list(...) aus der deque eine Liste." + absturz(fehler)
)

# einplanen: nur normale oder nur dringende Aufgaben
ergebnis, fehler = rufe(lambda: (einplanen([("C-1", False), ("C-2", False)]), einplanen([("C-1", True), ("C-2", True), ("C-3", True)])))
assert ergebnis == (["C-1", "C-2"], ["C-3", "C-2", "C-1"]), (
    f"einplanen nur mit normalen und nur mit dringenden Aufgaben ergibt {ergebnis!r}, erwartet war "
    "(['C-1', 'C-2'], ['C-3', 'C-2', 'C-1'])." + absturz(fehler)
)

# einplanen: keine Eingänge
ergebnis, fehler = rufe(lambda: einplanen([]))
assert ergebnis == [], f"einplanen([]) ergibt {ergebnis!r}, erwartet war []." + absturz(fehler)

# einplanen: mit deque statt insert
benutzt_insert = kommt_vor(einplanen, ruft_methode("insert"))
benutzt_appendleft = kommt_vor(einplanen, lambda knoten: isinstance(knoten, ast.Attribute) and knoten.attr == "appendleft")
assert benutzt_appendleft and not benutzt_insert, (
    "einplanen " + ("ruft insert auf" if benutzt_insert else "benutzt nicht appendleft einer deque")
    + ". insert(0, …) verschiebt jedes Mal alle bisherigen Einträge (O(n)); eine deque fügt mit appendleft in O(1) "
    "vorn an."
)

# bericht: das Beispiel
ergebnis, fehler = rufe(lambda: bericht([("A-1", "Login", 3), ("A-2", "Export", 5)]))
assert ergebnis == "A-1: Login (3 SP)\nA-2: Export (5 SP)\n", (
    f"bericht([('A-1', 'Login', 3), ('A-2', 'Export', 5)]) ergibt {ergebnis!r}, erwartet war "
    "'A-1: Login (3 SP)\\nA-2: Export (5 SP)\\n'." + absturz(fehler)
)

# bericht: auch die letzte Zeile endet mit einem Zeilenumbruch
ergebnis, fehler = rufe(lambda: bericht([("B-7", "Suche verbessern", 8)]))
assert ergebnis == "B-7: Suche verbessern (8 SP)\n", (
    f"bericht([('B-7', 'Suche verbessern', 8)]) ergibt {ergebnis!r}, erwartet war 'B-7: Suche verbessern (8 SP)\\n'.\n"
    "Tipp: \"\\n\".join(zeilen) setzt den Umbruch nur zwischen die Zeilen; hängen Sie ihn an jede Zeile." + absturz(fehler)
)

# bericht: keine Aufgaben ergeben einen leeren Text
ergebnis, fehler = rufe(lambda: bericht([]))
assert ergebnis == "", f"bericht([]) ergibt {ergebnis!r}, erwartet war ''." + absturz(fehler)

# bericht: mit join statt +=
benutzt_join = kommt_vor(bericht, ruft_methode("join"))
benutzt_plus_gleich = kommt_vor(bericht, ist_erweiterte_zuweisung)
assert benutzt_join and not benutzt_plus_gleich, (
    "bericht " + ("benutzt +=" if benutzt_plus_gleich else "ruft nicht join auf")
    + ". Jedes += auf einen Text kopiert den bisherigen Text; sammeln Sie die Zeilen und fügen Sie sie mit "
    "\"\".join(...) einmal zusammen."
)

zufall = Zufall(5058)

# Viele zufällige Eingaben im Vergleich
for _ in range(100):
    alle = kennungen(zufall.randint(0, 30), zufall.choice("ABC"))
    backlog = zufall.sample(alle, zufall.randint(0, len(alle)))
    erledigt = [zufall.choice(alle + ["X-1"]) for _ in range(zufall.randint(0, 20))] if alle else []
    eingaenge = [(kennung, zufall.random() < 0.4) for kennung in backlog]
    aufgaben = [(kennung, zufall.choice(["Login", "Export", "Suche", "PDF-Druck"]), zufall.randint(0, 100)) for kennung in backlog]
    ergebnis, fehler = rufe(lambda: (offene_aufgaben(backlog, erledigt), einplanen(eingaenge), bericht(aufgaben)))
    erwartet = (vergleich_offen(backlog, erledigt), vergleich_plan(eingaenge), vergleich_bericht(aufgaben))
    assert ergebnis == erwartet, (
        f"Mit backlog {backlog}, erledigt {erledigt} und eingaenge {eingaenge} ergeben die drei Funktionen\n"
        f"{ergebnis!r},\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Laufzeit: einplanen braucht O(n) Schritte
_, schritte_klein = zaehle_schritte(einplanen, [(kennung, True) for kennung in kennungen(1000)])
ergebnis, schritte_gross = zaehle_schritte(einplanen, [(kennung, True) for kennung in kennungen(4000)])
assert ergebnis == kennungen(4000)[::-1] and schritte_gross <= 5 * schritte_klein + 50, (
    f"einplanen braucht für 1000 Aufgaben {schritte_klein} Schritte, für 4000 {schritte_gross}; bei O(n) wäre es etwa "
    "das Vierfache."
)

# Obere Grenze: 200000 Kennungen in offene_aufgaben
backlog = kennungen(200_000)
erledigt = kennungen(200_000)[::2]
ergebnis, fehler = rufe(lambda: offene_aufgaben(backlog, erledigt))
assert ergebnis == backlog[1::2], f"offene_aufgaben mit 200000 Kennungen ergibt {str(ergebnis)[:80]}…, erwartet waren die 100000 ungeraden." + absturz(fehler)

# Obere Grenze: ein Bericht mit 200000 Zeilen
aufgaben = [(kennung, "Aufgabe", nummer % 101) for nummer, kennung in enumerate(kennungen(200_000))]
ergebnis, fehler = rufe(lambda: bericht(aufgaben))
assert ergebnis == vergleich_bericht(aufgaben), f"bericht mit 200000 Aufgaben ergibt einen falschen Text: {str(ergebnis)[:80]}…" + absturz(fehler)

# Obere Grenze: 200000 dringende Aufgaben einplanen (mit insert(0, …) dauert das sehr lange)
eingaenge = [(kennung, True) for kennung in kennungen(200_000)]
ergebnis, fehler = rufe(lambda: einplanen(eingaenge))
assert ergebnis == kennungen(200_000)[::-1], f"einplanen mit 200000 dringenden Aufgaben ergibt {str(ergebnis)[:80]}…" + absturz(fehler)
