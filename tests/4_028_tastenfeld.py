# Automatisch erzeugt aus lehrkraft/muster/4_028_tastenfeld.py - nicht von Hand ändern.
# vorlage-hash: 6643dc4940185808
# text-hash: e5b388116d60a8db
# thema: funktionen
# inhalt: functools.partial

def druecke(folge, anzeige=None):
    """Baut ein Tastenfeld, tippt die Beschriftungen aus folge an und gibt die Anzeige als Text zurück."""
    if anzeige is None:
        anzeige = []
    tasten = baue_tastenfeld(anzeige)
    for beschriftung in folge:
        tasten[beschriftung]()
    return "".join(anzeige)


# Das Beispiel aus der Aufgabe
ergebnis = druecke(["4", "2", "7", "←", "9"])
assert ergebnis == "429", (
    f"Nach den Tasten 4, 2, 7, ←, 9 zeigt die Anzeige {ergebnis!r}, erwartet war '429'.\n"
    "Tipp: Kommt überall dieselbe Ziffer heraus, steckt ein lambda in der Schleife dahinter; partial(tippe, anzeige, "
    "ziffer) merkt sich den Wert der Ziffer in jedem Durchlauf."
)

# Jede Zifferntaste tippt ihre eigene Ziffer
ergebnisse = {ziffer: druecke([ziffer]) for ziffer in "0123456789"}
falsch = {ziffer: wert for ziffer, wert in ergebnisse.items() if wert != ziffer}
assert not falsch, (
    f"Diese Tasten tippen die falsche Ziffer (Taste: Anzeige): {falsch}.\n"
    "Tipp: Ein lambda in der Schleife liest ziffer erst beim Antippen, dann hat sie ihren letzten Wert."
)

# Das Tastenfeld hat genau die zwölf Tasten, alle als partial-Objekte
anzeige = []
tasten = baue_tastenfeld(anzeige)
erwartet = set("0123456789") | {"C", "←"}
assert isinstance(tasten, dict) and set(tasten) == erwartet, (
    f"baue_tastenfeld soll ein Dictionary mit den Schlüsseln {sorted(erwartet)} liefern; bekommen "
    f"{sorted(tasten) if isinstance(tasten, dict) else tasten!r}."
)

# Alle Tasten sind partial-Objekte
keine = sorted(name for name, taste in tasten.items() if not isinstance(taste, partial))
assert not keine, f"Diese Tasten sind keine partial-Objekte: {keine}. Bauen Sie jede mit partial(...)."

# Die Tasten rufen die vorgegebenen Funktionen auf
gefunden = {name: tasten[name].func for name in ["7", "C", "←"]}
erwartet = {"7": tippe, "C": loesche, "←": zurueck}
assert gefunden == erwartet, (
    f"Die Tasten 7, C und ← rufen {[funktion.__name__ for funktion in gefunden.values()]} auf, erwartet war "
    "['tippe', 'loesche', 'zurueck'].\nTipp: Das erste Argument von partial ist die Funktion, die aufgerufen werden soll."
)

# C löscht, ← entfernt das letzte Zeichen, auch auf leerer Anzeige ohne Fehler
ergebnis = (druecke(["1", "2", "C", "3"]), druecke(["←", "5", "←", "←", "6"]), druecke(["8", "C", "C"]))
assert ergebnis == ("3", "6", ""), (
    f"Die Folgen 1 2 C 3, ← 5 ← ← 6 und 8 C C ergeben {ergebnis!r}, erwartet war ('3', '6', '')."
)

# Die Tasten verändern genau die übergebene Liste
anzeige = ["9"]
ergebnis = druecke(["1"], anzeige)
assert anzeige == ["9", "1"], (
    f"Mit anzeige = ['9'] und Taste 1 ist die Liste danach {anzeige!r}, erwartet war ['9', '1'].\n"
    "Tipp: Die Tasten sollen die übergebene Liste verändern, keine Kopie."
)

# Höchstens sechs Stellen
ergebnis = druecke(list("12345678"))
assert ergebnis == "123456", f"Nach acht Ziffern zeigt die Anzeige {ergebnis!r}, erwartet war '123456' (höchstens 6 Stellen)."

# Zwei Tastenfelder mit eigenen Anzeigen stören sich nicht
links, rechts = [], []
tasten_links, tasten_rechts = baue_tastenfeld(links), baue_tastenfeld(rechts)
tasten_links["1"]()
tasten_rechts["2"]()
tasten_links["3"]()
assert (links, rechts) == (["1", "3"], ["2"]), (
    f"Zwei Tastenfelder: links 1, 3 und rechts 2 ergeben {links!r} und {rechts!r}, erwartet war ['1', '3'] und ['2']."
)

# pruefer_fuer aus dem Beispiel
pruefer = pruefer_fuer({"pin": (4, 6), "raum": (1, 3)})
ergebnis = (pruefer["pin"]("429"), pruefer["pin"]("4290"), pruefer["raum"]("B12"), pruefer["raum"]("B123"))
assert ergebnis == (False, True, True, False), (
    f'pin mit "429", "4290" und raum mit "B12", "B123" ergeben {ergebnis!r}, erwartet war (False, True, True, False).'
)

# Die Prüfer sind partial-Objekte mit den Grenzen als Schlüsselwörtern
pruefer = pruefer_fuer({"pin": (4, 6)})
eintrag = pruefer["pin"]
assert isinstance(eintrag, partial) and eintrag.func is pruefe_laenge and eintrag.keywords == {"minimum": 4, "maximum": 6}, (
    "pruefer_fuer({'pin': (4, 6)})['pin'] soll partial(pruefe_laenge, minimum=4, maximum=6) sein; bekommen "
    f"{eintrag!r}."
)

# Grenzen inklusive, minimum gleich maximum und 0
pruefer = pruefer_fuer({"plz": (5, 5), "kommentar": (0, 1000)})
ergebnis = [pruefer["plz"](text) for text in ["3309", "33098", "330981"]] + [pruefer["kommentar"](""), pruefer["kommentar"]("x" * 1000), pruefer["kommentar"]("x" * 1001)]
assert ergebnis == [False, True, False, True, True, False], (
    f'plz (5, 5) mit 4, 5, 6 Zeichen und kommentar (0, 1000) mit 0, 1000, 1001 Zeichen ergeben {ergebnis}, '
    "erwartet war [False, True, False, True, True, False]."
)

# Keine Felder
ergebnis = pruefer_fuer({})
assert ergebnis == {}, f"pruefer_fuer({{}}) ergibt {ergebnis!r}, erwartet war {{}}."

# partial wird benutzt
assert verwendet("partial"), "Bauen Sie Tasten und Prüfer mit functools.partial."

# 300 zufällige Tastenfolgen gegen eine Nachrechnung
zufall = Zufall(4028)
TASTEN = list("0123456789") + ["C", "←", "←"]
for _ in range(300):
    folge = [zufall.choice(TASTEN) for _ in range(zufall.randint(0, 12))]
    erwartet = []
    for beschriftung in folge:
        if beschriftung == "C":
            erwartet = []
        elif beschriftung == "←":
            erwartet = erwartet[:-1]
        elif len(erwartet) < 6:
            erwartet = erwartet + [beschriftung]
    ergebnis = druecke(folge)
    assert ergebnis == "".join(erwartet), (
        f"Nach den Tasten {' '.join(folge)} zeigt die Anzeige {ergebnis!r}, erwartet war {''.join(erwartet)!r}."
    )

# 100 zufällige Feldlisten
for _ in range(100):
    laengen = {}
    for nummer in range(zufall.randint(0, 6)):
        minimum = zufall.randint(0, 10)
        laengen[f"feld{nummer}"] = (minimum, zufall.randint(minimum, 12))
    pruefer = pruefer_fuer(dict(laengen))
    assert set(pruefer) == set(laengen), f"pruefer_fuer({laengen}) liefert die Felder {sorted(pruefer)}, erwartet {sorted(laengen)}."
    for feld, (minimum, maximum) in laengen.items():
        text = "a" * zufall.randint(0, 14)
        ergebnis = pruefer[feld](text)
        erwartet = minimum <= len(text) and not len(text) > maximum
        assert ergebnis == erwartet, (
            f"Feld {feld} mit Grenzen ({minimum}, {maximum}) und einem Text mit {len(text)} Zeichen ergibt "
            f"{ergebnis!r}, erwartet war {erwartet}."
        )

# Obere Grenze: 50 Felder
laengen = {f"feld{nummer}": (nummer * 10, nummer * 20) for nummer in range(50)}
pruefer = pruefer_fuer(laengen)
ergebnis = [pruefer[f"feld{nummer}"]("x" * (nummer * 15)) for nummer in range(50)]
assert ergebnis == [True] * 50 and pruefer["feld49"]("x" * 981) is False, (
    "Bei 50 Feldern stimmt mindestens ein Prüfer nicht: Für feld<n> mit Grenzen (10·n, 20·n) muss ein Text mit "
    f"15·n Zeichen passen; bekommen {ergebnis}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "429\nFalse True"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
