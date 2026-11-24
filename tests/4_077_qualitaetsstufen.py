# Automatisch erzeugt aus lehrkraft/muster/4_077_qualitaetsstufen.py - nicht von Hand ändern.
# vorlage-hash: 1019558618fc0250
# text-hash: 91b3ea9dde9ebc68
# thema: datenstrukturen
# inhalt: bisect: Stufen und Bereiche

def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(wert):
    """Kürzt lange Listen für Meldungen."""
    text = repr(wert)
    if len(text) <= 200:
        return text
    return text[:150] + " …]"


def langsame_stufe(wert, grenzen, stufen):
    """Vergleichslösung: zählt die Grenzen, die kleiner oder gleich wert sind."""
    anzahl = 0
    for grenze in grenzen:
        if grenze <= wert:
            anzahl = anzahl + 1
    return stufen[anzahl]


def langsame_anzahl(werte, von, bis):
    """Vergleichslösung: geht alle Werte durch."""
    anzahl = 0
    for wert in werte:
        if von <= wert < bis:
            anzahl = anzahl + 1
    return anzahl


def pruefe_stufe(wert, erwartet, grenzen=GRENZEN, stufen=STUFEN, tipp=""):
    """Prüft stufe(wert, grenzen, stufen); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(stufe, wert, list(grenzen), list(stufen))
    text = f"stufe({wert!r}, {kurz(grenzen)}, {kurz(stufen)}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Stufe mit return zurück."
    elif tipp:
        text = text + "\nTipp: " + tipp
    return ergebnis == erwartet, text


def pruefe_einfuegen(werte, wert, tipp=""):
    """Prüft fuege_ein(werte, wert) an einer Kopie; liefert (stimmt, Meldung)."""
    liste = list(werte)
    erwartet_liste = sorted(werte + [wert])
    erwartet_position = len([w for w in werte if w <= wert])
    ergebnis = wert_von(fuege_ein, liste, wert)
    text = (
        f"fuege_ein({kurz(werte)}, {wert!r}) ergibt {ergebnis!r} und die Liste {kurz(liste)}, "
        f"erwartet waren Position {erwartet_position} und {kurz(erwartet_liste)}."
    )
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Position mit return zurück."
    elif tipp:
        text = text + "\nTipp: " + tipp
    return ergebnis == erwartet_position and liste == erwartet_liste, text


def pruefe_anzahl(werte, von, bis, tipp=""):
    """Prüft anzahl_im_bereich(werte, von, bis) an einer Kopie; liefert (stimmt, Meldung)."""
    erwartet = langsame_anzahl(werte, von, bis)
    ergebnis = wert_von(anzahl_im_bereich, list(werte), von, bis)
    text = f"anzahl_im_bereich({kurz(werte)}, {von!r}, {bis!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Anzahl mit return zurück."
    elif tipp:
        text = text + "\nTipp: " + tipp
    return ergebnis == erwartet, text


# stufe: das Beispiel 72.5 → "C"
stimmt, text = pruefe_stufe(72.5, "C")
assert stimmt, text

# stufe: andere Werte mitten in einer Stufe (nicht fest hinschreiben!)
stimmt, text = pruefe_stufe(60, "D")
stimmt_zwei, text_zwei = pruefe_stufe(90, "B")
assert stimmt and stimmt_zwei, text if not stimmt else text_zwei

# stufe: unter der kleinsten Grenze die erste Stufe
stimmt, text = pruefe_stufe(12, "E")
assert stimmt, text

# stufe: über der größten Grenze die letzte Stufe
stimmt, text = pruefe_stufe(99, "A", tipp="Über der letzten Grenze liegt die letzte Stufe, stufen[len(grenzen)].")
assert stimmt, text

# stufe: genau auf einer Grenze die höhere Stufe (das Beispiel 85)
stimmt, text = pruefe_stufe(
    85, "B", tipp="Ein Wert genau auf der Grenze gehört zur höheren Stufe; das liefert bisect_right, nicht bisect_left."
)
assert stimmt, text

# stufe: genau auf der kleinsten Grenze
stimmt, text = pruefe_stufe(50, "D")
assert stimmt, text

# stufe: genau auf der größten Grenze
stimmt, text = pruefe_stufe(95, "A")
assert stimmt, text

# stufe: knapp unter einer Grenze noch die niedrigere Stufe
stimmt, text = pruefe_stufe(69.99, "D")
assert stimmt, text

# stufe: der Rand 0
stimmt, text = pruefe_stufe(0, "E")
assert stimmt, text

# stufe: der Rand 100
stimmt, text = pruefe_stufe(100, "A")
assert stimmt, text

# stufe: andere Grenzen und Stufen werden benutzt, nicht GRENZEN und STUFEN
stimmt, text = pruefe_stufe(
    30, "mittel", [25, 75], ["niedrig", "mittel", "hoch"], "Benutzen Sie die Parameter grenzen und stufen."
)
assert stimmt, text

# stufe: eine Grenze bei 0 – der Wert 0 gehört schon zur zweiten Stufe
stimmt, text = pruefe_stufe(0, "geprüft", [0], ["leer", "geprüft"])
assert stimmt, text

# stufe: ohne Grenzen gibt es nur eine Stufe
stimmt, text = pruefe_stufe(42, "alle", [], ["alle"])
assert stimmt, text

# fuege_ein: das Beispiel, 70 kommt hinter die beiden 70
stimmt, text = pruefe_einfuegen(
    [40, 55, 70, 70, 88, 97], 70, "Hinter allen gleichen Werten einfügen: bisect_right bzw. insort_right."
)
assert stimmt, text

# fuege_ein: ein neuer Wert zwischen zwei anderen
stimmt, text = pruefe_einfuegen([40, 55, 70, 88, 97], 60)
assert stimmt, text

# fuege_ein: die Funktion gibt die Position zurück
liste = [10, 20, 30]
ergebnis = wert_von(fuege_ein, liste, 25)
assert ergebnis == 2, (
    f"fuege_ein([10, 20, 30], 25) ergibt {ergebnis!r}, erwartet war die Position 2."
    + ("\nTipp: insort gibt nichts zurück; bestimmen Sie die Position vorher mit bisect_right." if ergebnis is None else "")
)

# fuege_ein: die Liste selbst wird verändert, keine neue angelegt
liste = [10, 20, 30]
wert_von(fuege_ein, liste, 25)
assert liste == [10, 20, 25, 30], (
    f"Nach fuege_ein(liste, 25) mit liste = [10, 20, 30] ist liste {liste!r}, erwartet war [10, 20, 25, 30].\n"
    "Tipp: Ändern Sie die übergebene Liste mit insert (oder insort), statt eine neue zu bauen."
)

# fuege_ein: ganz vorn
stimmt, text = pruefe_einfuegen([40, 55, 70], 5)
assert stimmt, text

# fuege_ein: ganz hinten
stimmt, text = pruefe_einfuegen([40, 55, 70], 100)
assert stimmt, text

# fuege_ein: in eine leere Liste
stimmt, text = pruefe_einfuegen([], 73)
assert stimmt, text

# fuege_ein: mehrmals nacheinander bleibt die Liste sortiert
liste = []
for neu in [70, 20, 90, 20, 55, 100, 0]:
    wert_von(fuege_ein, liste, neu)
assert liste == [0, 20, 20, 55, 70, 90, 100], (
    f"Nach dem Einfügen von 70, 20, 90, 20, 55, 100, 0 in eine leere Liste ist sie {liste!r}, "
    "erwartet war [0, 20, 20, 55, 70, 90, 100]."
)

# anzahl_im_bereich: das Beispiel
stimmt, text = pruefe_anzahl([40, 55, 70, 70, 70, 88, 97], 50, 85)
assert stimmt, text

# anzahl_im_bereich: ein anderer Bereich (nicht fest hinschreiben!)
stimmt, text = pruefe_anzahl([40, 55, 70, 70, 70, 88, 97], 60, 100)
assert stimmt, text

# anzahl_im_bereich: von gehört dazu
stimmt, text = pruefe_anzahl(
    [40, 55, 70, 70, 70, 88, 97], 70, 90,
    "von gehört zum Bereich; die Werte gleich von zählen mit, darum bisect_left für von.",
)
assert stimmt, text

# anzahl_im_bereich: bis gehört nicht dazu
stimmt, text = pruefe_anzahl(
    [40, 55, 70, 70, 70, 88, 97], 50, 70,
    "bis gehört nicht mehr zum Bereich; die Werte gleich bis zählen nicht, darum bisect_left auch für bis.",
)
assert stimmt, text

# anzahl_im_bereich: leerer Bereich von == bis
stimmt, text = pruefe_anzahl([40, 55, 70, 70, 88], 70, 70)
assert stimmt, text

# anzahl_im_bereich: der ganze Bereich 0 bis 100 ohne die 100
stimmt, text = pruefe_anzahl([0, 0, 30, 100, 100], 0, 100)
assert stimmt, text

# anzahl_im_bereich: leere Liste
stimmt, text = pruefe_anzahl([], 10, 90)
assert stimmt, text

# anzahl_im_bereich: die Liste bleibt unverändert
liste = [40, 55, 70, 88]
wert_von(anzahl_im_bereich, liste, 50, 90)
assert liste == [40, 55, 70, 88], f"anzahl_im_bereich hat die Liste verändert, sie ist jetzt {liste!r}."

# Das Modul bisect wird benutzt
bisect_funktionen = ["bisect", "bisect_left", "bisect_right", "insort", "insort_left", "insort_right"]
assert any(verwendet(name) for name in bisect_funktionen), "Benutzen Sie für die Suche das Modul bisect (import bisect), wie im Hintergrund gezeigt."

# Viele zufällige Werte, verglichen mit dem Durchgehen aller Elemente
zufall = Zufall(4077)
for runde in range(400):
    grenzen = sorted(set(zufall.randint(0, 100) for _ in range(zufall.randint(0, 6))))
    stufen = [f"S{i}" for i in range(len(grenzen) + 1)]
    werte = sorted(zufall.randint(0, 100) for _ in range(zufall.randint(0, 12)))
    wert = zufall.choice(grenzen + [zufall.randint(0, 100)])
    stimmt, text = pruefe_stufe(wert, langsame_stufe(wert, grenzen, stufen), grenzen, stufen)
    assert stimmt, text
    stimmt, text = pruefe_einfuegen(werte, wert)
    assert stimmt, text
    von = zufall.choice(werte + [zufall.randint(0, 100)])
    bis = zufall.randint(von, 100)
    stimmt, text = pruefe_anzahl(werte, von, bis)
    assert stimmt, text

# Laufzeit: stufe sieht nicht jede Grenze an
grenzen = Zaehlliste([i / 10 for i in range(1000)])
stufen = Zaehlliste([f"S{i}" for i in range(1001)])
ergebnis = wert_von(stufe, 77.75, grenzen, stufen)
assert ergebnis == "S778" and grenzen.lesezugriffe <= 40, (
    f"stufe mit 1000 Grenzen ergibt {ergebnis!r} (erwartet 'S778') und liest {grenzen.lesezugriffe}-mal aus "
    "grenzen. Mit binärer Suche genügen etwa 10 Zugriffe.\nTipp: bisect.bisect_right(grenzen, wert)."
)

# Laufzeit: anzahl_im_bereich sieht bei 100 000 Werten nicht jeden an
werte = Zaehlliste(sorted(zufall.randint(0, 100) for _ in range(100000)))
erwartet = langsame_anzahl(werte.werte, 30, 60)
ergebnis = wert_von(anzahl_im_bereich, werte, 30, 60)
assert ergebnis == erwartet and werte.lesezugriffe <= 100, (
    f"anzahl_im_bereich mit 100 000 Werten ergibt {ergebnis!r} (erwartet {erwartet}) und liest "
    f"{werte.lesezugriffe}-mal aus der Liste. Mit zwei binären Suchen genügen etwa 34 Zugriffe.\n"
    "Tipp: bisect_left(werte, bis) - bisect_left(werte, von)."
)

# Obere Grenze: 2000 Werte in eine Liste mit 100 000 Werten einfügen
liste = sorted(zufall.uniform(0, 100) for _ in range(100000))
neue = [zufall.uniform(0, 100) for _ in range(2000)]
positionen_stimmen = True
for neu in neue:
    position = wert_von(fuege_ein, liste, neu)
    if not isinstance(position, int) or liste[position] != neu:
        positionen_stimmen = False
        break
assert positionen_stimmen and len(liste) == 102000 and liste == sorted(liste), (
    "Nach 2000-mal fuege_ein in eine Liste mit 100 000 Werten ist die Liste nicht sortiert, hat nicht 102 000 "
    "Werte oder eine zurückgegebene Position zeigt nicht auf den neuen Wert."
)
