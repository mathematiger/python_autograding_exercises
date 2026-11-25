# Automatisch erzeugt aus lehrkraft/muster/3_076_meldungstexte.py - nicht von Hand ändern.
# vorlage-hash: 932482124c22397d
# text-hash: 110ea9943186397d
# thema: texte_zahlen
# inhalt: Textstatistik: Wörter, Satzlängen

import math


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def als_paare(ergebnis):
    """Macht aus einer Liste von Paaren (auch als Listen geschrieben) eine Liste von Tupeln, sonst bleibt ergebnis."""
    if not isinstance(ergebnis, list):
        return ergebnis
    paare = []
    for eintrag in ergebnis:
        if isinstance(eintrag, (tuple, list)):
            paare.append(tuple(eintrag))
        else:
            paare.append(eintrag)
    return paare


def ungefaehr(a, b):
    """Prüft, ob a eine Zahl ist und bis auf Rundungsfehler gleich b."""
    return isinstance(a, (int, float)) and not isinstance(a, bool) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def vergleich_woerter(text):
    """Vergleichslösung: liest den Text Zeichen für Zeichen und schneidet Satzzeichen am Rand selbst ab."""
    liste = []
    for stueck in text.split():
        anfang, ende = 0, len(stueck)
        while anfang < ende and stueck[anfang] in SATZZEICHEN:
            anfang += 1
        while ende > anfang and stueck[ende - 1] in SATZZEICHEN:
            ende -= 1
        if anfang < ende:
            liste.append(stueck[anfang:ende].lower())
    return liste


def vergleich_saetze(text):
    """Vergleichslösung: sammelt Zeichen bis zum nächsten Satzende."""
    laengen, satz = [], ""
    for zeichen in text + ".":
        if zeichen in SATZENDE:
            if vergleich_woerter(satz):
                laengen.append(len(vergleich_woerter(satz)))
            satz = ""
        else:
            satz += zeichen
    return laengen


def vergleich_haeufigste(meldungen, anzahl):
    """Vergleichslösung: zählt mit list.count und wählt dann der Reihe nach das beste Paar."""
    alle = [wort for meldung in meldungen for wort in vergleich_woerter(meldung) if wort not in FUELLWOERTER]
    uebrig = {wort: alle.count(wort) for wort in set(alle)}
    ergebnis = []
    while uebrig and len(ergebnis) < anzahl:
        bestes = min(uebrig, key=lambda wort: (-uebrig[wort], wort))
        ergebnis.append((bestes, uebrig.pop(bestes)))
    return ergebnis


MELDUNGEN = [
    "Das WLAN im Besprechungsraum ist sehr langsam. Videokonferenzen brechen ab!",
    "Kein WLAN im Lager. Der Drucker ist auch nicht erreichbar.",
    "WLAN langsam, VPN bricht ab. Bitte prüfen!",
]

# woerter: ein Text ohne Satzzeichen in Kleinbuchstaben
ergebnis = wert_von(woerter, "switch im keller blinkt")
assert ergebnis == ["switch", "im", "keller", "blinkt"], (
    f'woerter("switch im keller blinkt") ergibt {ergebnis!r}, erwartet war ["switch", "im", "keller", "blinkt"].\n'
    "Tipp: text.split() zerlegt den Text an den Leerzeichen."
)

# woerter: alles in Kleinbuchstaben
ergebnis = wert_von(woerter, "Switch im Keller BLINKT")
assert ergebnis == ["switch", "im", "keller", "blinkt"], (
    f'woerter("Switch im Keller BLINKT") ergibt {ergebnis!r}, erwartet war ["switch", "im", "keller", "blinkt"].\n'
    "Tipp: lower() macht alle Buchstaben klein."
)

# woerter: Satzzeichen am Wortende fallen weg
ergebnis = wert_von(woerter, "Router weg, Netz langsam.")
assert ergebnis == ["router", "weg", "netz", "langsam"], (
    f'woerter("Router weg, Netz langsam.") ergibt {ergebnis!r}, erwartet war ["router", "weg", "netz", "langsam"].\n'
    "Tipp: wort.strip(SATZZEICHEN) entfernt Satzzeichen am Anfang und am Ende."
)

# woerter: das Beispiel aus der Aufgabe, auch Klammern und Doppelpunkt
ergebnis = wert_von(woerter, "Bitte prüfen: (VPN) bricht ab!")
assert ergebnis == ["bitte", "prüfen", "vpn", "bricht", "ab"], (
    f'woerter("Bitte prüfen: (VPN) bricht ab!") ergibt {ergebnis!r}, erwartet war '
    '["bitte", "prüfen", "vpn", "bricht", "ab"].\nTipp: Benutzen Sie alle Zeichen aus SATZZEICHEN beim Abschneiden.'
)

# woerter: Anführungszeichen und mehrere Satzzeichen hintereinander
ergebnis = wert_von(woerter, 'Meldung "Kein Zugriff"?! Wieso...')
assert ergebnis == ["meldung", "kein", "zugriff", "wieso"], (
    f"woerter('Meldung \"Kein Zugriff\"?! Wieso...') ergibt {ergebnis!r}, erwartet war "
    '["meldung", "kein", "zugriff", "wieso"].'
)

# woerter: Bindestriche und Ziffern bleiben im Wort
ergebnis = wert_von(woerter, "WLAN-Router in Raum 2-14 (Port 8).")
assert ergebnis == ["wlan-router", "in", "raum", "2-14", "port", "8"], (
    f'woerter("WLAN-Router in Raum 2-14 (Port 8).") ergibt {ergebnis!r}, erwartet war '
    '["wlan-router", "in", "raum", "2-14", "port", "8"].\nTipp: Nur Satzzeichen am Rand fallen weg, nichts in der Mitte.'
)

# woerter: Zeilenumbrüche und mehrere Leerzeichen trennen auch
ergebnis = wert_von(woerter, "  Drucker\n\noffline   seit gestern ")
assert ergebnis == ["drucker", "offline", "seit", "gestern"], (
    f'woerter("  Drucker\\n\\noffline   seit gestern ") ergibt {ergebnis!r}, erwartet war '
    '["drucker", "offline", "seit", "gestern"].\nTipp: split() ohne Argument trennt an jedem Leerraum.'
)

# woerter: Satzzeichen allein sind kein Wort
ergebnis = wert_von(woerter, "Netz weg ... ( ) !")
assert ergebnis == ["netz", "weg"], (
    f'woerter("Netz weg ... ( ) !") ergibt {ergebnis!r}, erwartet war ["netz", "weg"].\n'
    "Tipp: Bleibt nach dem Abschneiden ein leerer Text übrig, ist es kein Wort."
)

# woerter: ein leerer Text hat keine Wörter
ergebnis = wert_von(woerter, "")
assert ergebnis == [], f'woerter("") ergibt {ergebnis!r}, erwartet war [].'

# haeufigste_woerter: die drei häufigsten Wörter im Beispiel (Reihenfolge noch egal)
ergebnis = als_paare(wert_von(haeufigste_woerter, MELDUNGEN, 3))
assert isinstance(ergebnis, list) and sorted(ergebnis) == [("ab", 2), ("langsam", 2), ("wlan", 3)], (
    f"haeufigste_woerter(meldungen, 3) ergibt {ergebnis!r}, erwartet waren die Paare ('wlan', 3), ('ab', 2) und "
    "('langsam', 2).\nTipp: Zählen Sie wie in Aufgabe 2_025 mit einem Dictionary und lassen Sie die Wörter aus "
    "FUELLWOERTER weg."
)

# haeufigste_woerter: das häufigste zuerst, bei Gleichstand alphabetisch
ergebnis = als_paare(wert_von(haeufigste_woerter, MELDUNGEN, 5))
erwartet = [("wlan", 3), ("ab", 2), ("langsam", 2), ("besprechungsraum", 1), ("brechen", 1)]
assert ergebnis == erwartet, (
    f"haeufigste_woerter(meldungen, 5) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}.\n"
    "Tipp: sorted(zaehler.items(), key=lambda paar: (-paar[1], paar[0])) und dann die ersten anzahl Paare."
)

# haeufigste_woerter: Füllwörter fallen weg, auch großgeschrieben
meldungen = ["Das Netz ist weg. Das ist nicht gut!", "DAS NETZ IST WEG!!!"]
ergebnis = als_paare(wert_von(haeufigste_woerter, meldungen, 10))
assert ergebnis == [("netz", 2), ("weg", 2), ("gut", 1)], (
    f"haeufigste_woerter({meldungen}, 10) ergibt {ergebnis!r}, erwartet war [('netz', 2), ('weg', 2), ('gut', 1)].\n"
    "Tipp: Prüfen Sie erst nach dem Kleinschreiben, ob ein Wort in FUELLWOERTER steht."
)

# haeufigste_woerter: andere Meldungen (nicht fest hinschreiben!)
meldungen = ["Access-Point im Flur aus.", "Flur: Access-Point aus? Access-Point neu starten!", "Drucker aus."]
ergebnis = als_paare(wert_von(haeufigste_woerter, meldungen, 3))
assert ergebnis == [("access-point", 3), ("aus", 3), ("flur", 2)], (
    f"haeufigste_woerter({meldungen}, 3) ergibt {ergebnis!r}, erwartet war "
    "[('access-point', 3), ('aus', 3), ('flur', 2)]."
)

# haeufigste_woerter: weniger verschiedene Wörter als anzahl
ergebnis = als_paare(wert_von(haeufigste_woerter, ["VPN langsam, VPN weg."], 10))
assert ergebnis == [("vpn", 2), ("langsam", 1), ("weg", 1)], (
    f"haeufigste_woerter(['VPN langsam, VPN weg.'], 10) ergibt {ergebnis!r}, erwartet war "
    "[('vpn', 2), ('langsam', 1), ('weg', 1)]."
)

# haeufigste_woerter: anzahl 0 ergibt eine leere Liste
ergebnis = wert_von(haeufigste_woerter, MELDUNGEN, 0)
assert ergebnis == [], f"haeufigste_woerter(meldungen, 0) ergibt {ergebnis!r}, erwartet war []."

# haeufigste_woerter: nur Füllwörter
ergebnis = wert_von(haeufigste_woerter, ["Das ist es nicht."], 3)
assert ergebnis == [], f"haeufigste_woerter(['Das ist es nicht.'], 3) ergibt {ergebnis!r}, erwartet war []."

# haeufigste_woerter: keine Meldungen
ergebnis = wert_von(haeufigste_woerter, [], 3)
assert ergebnis == [], f"haeufigste_woerter([], 3) ergibt {ergebnis!r}, erwartet war []."

# satzlaengen: das Beispiel aus der Aufgabe
ergebnis = wert_von(satzlaengen, MELDUNGEN[0])
assert ergebnis == [7, 3], (
    f"satzlaengen({MELDUNGEN[0]!r}) ergibt {ergebnis!r}, erwartet war [7, 3].\n"
    'Tipp: Machen Sie aus "!" und "?" Punkte, teilen Sie mit split(".") und zählen Sie die Wörter jedes Stücks.'
)

# satzlaengen: ein anderer Text, Füllwörter zählen mit (nicht fest hinschreiben!)
ergebnis = wert_von(satzlaengen, MELDUNGEN[1])
assert ergebnis == [4, 6], (
    f"satzlaengen({MELDUNGEN[1]!r}) ergibt {ergebnis!r}, erwartet war [4, 6].\n"
    "Tipp: In satzlaengen zählen alle Wörter, auch die Füllwörter."
)

# satzlaengen: Komma und Doppelpunkt beenden keinen Satz
ergebnis = wert_von(satzlaengen, "Hinweis: Netz langsam, Drucker weg, Telefon geht.")
assert ergebnis == [7], (
    f'satzlaengen("Hinweis: Netz langsam, Drucker weg, Telefon geht.") ergibt {ergebnis!r}, erwartet war [7].'
)

# satzlaengen: auch Wörter nach dem letzten Satzende bilden einen Satz
ergebnis = wert_von(satzlaengen, "Netz weg? Seit 9 Uhr")
assert ergebnis == [2, 3], (
    f'satzlaengen("Netz weg? Seit 9 Uhr") ergibt {ergebnis!r}, erwartet war [2, 3].\n'
    "Tipp: Das letzte Stück nach dem letzten Satzende gehört auch dazu, wenn es Wörter hat."
)

# satzlaengen: mehrere Satzzeichen hintereinander ergeben keine leeren Sätze
ergebnis = wert_von(satzlaengen, "Netz weg?? Wirklich?! Seit Stunden...")
assert ergebnis == [2, 1, 2], (
    f'satzlaengen("Netz weg?? Wirklich?! Seit Stunden...") ergibt {ergebnis!r}, erwartet war [2, 1, 2].\n'
    "Tipp: Überspringen Sie Stücke ohne Wörter."
)

# satzlaengen: Zeilenumbrüche und Satzzeichen ohne Wort
ergebnis = wert_von(satzlaengen, "Drucker\noffline (seit gestern).\n\n ( ) .")
assert ergebnis == [4], f'satzlaengen("Drucker\\noffline (seit gestern).\\n\\n ( ) .") ergibt {ergebnis!r}, erwartet war [4].'

# satzlaengen: ein leerer Text hat keine Sätze
ergebnis = wert_von(satzlaengen, "")
assert ergebnis == [], f'satzlaengen("") ergibt {ergebnis!r}, erwartet war [].'

# mittlere_satzlaenge: das Beispiel aus der Aufgabe
ergebnis = wert_von(mittlere_satzlaenge, MELDUNGEN)
assert ungefaehr(ergebnis, 4.5), (
    f"mittlere_satzlaenge(meldungen) ergibt {ergebnis!r}, erwartet war 4.5 (27 Wörter in 6 Sätzen).\n"
    "Tipp: Sammeln Sie die Satzlängen aller Meldungen und teilen Sie ihre Summe durch ihre Anzahl."
)

# mittlere_satzlaenge: Mittel über alle Sätze, nicht über die Meldungen
meldungen = ["Netz weg. Kein Zugriff auf Laufwerk. Hilfe!", "WLAN langsam."]
ergebnis = wert_von(mittlere_satzlaenge, meldungen)
assert ungefaehr(ergebnis, 2.25), (
    f"mittlere_satzlaenge({meldungen}) ergibt {ergebnis!r}, erwartet war 2.25 (9 Wörter in 4 Sätzen).\n"
    "Tipp: Jeder Satz zählt gleich, egal aus welcher Meldung er kommt; mitteln Sie nicht erst je Meldung."
)

# mittlere_satzlaenge: eine einzige Meldung
ergebnis = wert_von(mittlere_satzlaenge, ["Server antwortet nicht"])
assert ungefaehr(ergebnis, 3), f"mittlere_satzlaenge(['Server antwortet nicht']) ergibt {ergebnis!r}, erwartet war 3."

# mittlere_satzlaenge: ohne Meldungen 0
ergebnis = wert_von(mittlere_satzlaenge, [])
assert ungefaehr(ergebnis, 0), (
    f"mittlere_satzlaenge([]) ergibt {ergebnis!r}, erwartet war 0.\n"
    "Tipp: Gibt es keinen Satz, würde die Division durch 0 scheitern; prüfen Sie das vorher."
)

# mittlere_satzlaenge: Meldungen ohne einen einzigen Satz ergeben 0
ergebnis = wert_von(mittlere_satzlaenge, ["", "?!"])
assert ungefaehr(ergebnis, 0), (
    f"mittlere_satzlaenge(['', '?!']) ergibt {ergebnis!r}, erwartet war 0.\n"
    "Tipp: Zählen Sie die Sätze, nicht die Meldungen; gibt es keinen Satz, würde die Division durch 0 scheitern."
)

zufall = Zufall(3076)
WORTSCHATZ = ["WLAN", "wlan", "VPN", "Drucker", "Flur", "Port-8", "Raum", "3", "langsam", "weg", "das", "Ist", "NICHT", "öde", "ß"]
RAENDER = ["", "", "", ",", ".", "!", "?", "...", "?!", ":", ")", '"']


def zufallstext():
    """Ein zufälliger Meldungstext aus WORTSCHATZ mit Satzzeichen am Wortrand."""
    teile = []
    for _ in range(zufall.randint(0, 12)):
        vorn = zufall.choice(["", "", "", "(", '"'])
        teile.append(vorn + zufall.choice(WORTSCHATZ) + zufall.choice(RAENDER))
    return zufall.choice([" ", "  ", "\n"]).join(teile)


# Viele zufällige Texte
for _ in range(300):
    text = zufallstext()
    ergebnis = wert_von(woerter, text)
    erwartet = vergleich_woerter(text)
    assert ergebnis == erwartet, f"woerter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    ergebnis = wert_von(satzlaengen, text)
    erwartet = vergleich_saetze(text)
    assert ergebnis == erwartet, f"satzlaengen({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Viele zufällige Listen von Meldungen
for _ in range(100):
    meldungen = [zufallstext() for _ in range(zufall.randint(0, 5))]
    anzahl = zufall.randint(0, 8)
    ergebnis = als_paare(wert_von(haeufigste_woerter, meldungen, anzahl))
    erwartet = vergleich_haeufigste(meldungen, anzahl)
    assert ergebnis == erwartet, f"haeufigste_woerter({meldungen}, {anzahl}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}."
    ergebnis = wert_von(mittlere_satzlaenge, meldungen)
    laengen = [laenge for meldung in meldungen for laenge in vergleich_saetze(meldung)]
    erwartet = sum(laengen) / len(laengen) if laengen else 0
    assert ungefaehr(ergebnis, erwartet), f"mittlere_satzlaenge({meldungen}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Obere Grenze: 10 000 Meldungen mit zusammen 100 000 Wörtern
woerterbuch = [f"geraet{nummer}" for nummer in range(3000)] + sorted(FUELLWOERTER)
meldungen = []
for _ in range(10_000):
    satz = " ".join(zufall.choice(woerterbuch) for _ in range(9))
    meldungen.append(satz.capitalize() + zufall.choice([".", "!", "?"]) + " Bitte!")
ergebnis = als_paare(wert_von(haeufigste_woerter, meldungen, 100_000))
zaehlung = {}
for meldung in meldungen:
    for wort in meldung.lower().replace(".", " ").replace("!", " ").replace("?", " ").split():
        if wort not in FUELLWOERTER:
            zaehlung[wort] = zaehlung.get(wort, 0) + 1
erwartet = sorted(zaehlung.items(), key=lambda paar: (-paar[1], paar[0]))
assert ergebnis == erwartet, (
    f"Bei 10 000 Meldungen mit 100 000 Wörtern ergibt haeufigste_woerter(…, 100000) {str(ergebnis)[:150]}, "
    f"erwartet war {str(erwartet)[:150]}."
)

# Obere Grenze: mittlere Satzlänge von 10 000 Meldungen
ergebnis = wert_von(mittlere_satzlaenge, meldungen)
assert ungefaehr(ergebnis, 5), (
    f"Jede der 10 000 Meldungen hat einen Satz mit 9 Wörtern und einen mit 1 Wort; mittlere_satzlaenge ergibt "
    f"{ergebnis!r}, erwartet war 5."
)
