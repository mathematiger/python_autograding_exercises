# Automatisch erzeugt aus lehrkraft/muster/4_080_fehleranalyse.py - nicht von Hand ändern.
# vorlage-hash: 4542f9294a4d71ed
# text-hash: 2047edd8ca9cd070
# thema: funktionen
# inhalt: veränderliche Standardwerte

def rufe(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, Ausnahme oder None)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


def absturz(fehler):
    """Ergänzt eine Meldung um die aufgetretene Ausnahme."""
    return f"\nDie Funktion löst {type(fehler).__name__}: {fehler} aus." if fehler is not None else ""


def vergleich_hoechste(tabelle):
    """Vergleichslösung: sortiert stabil absteigend nach RPZ und nimmt den ersten Eintrag."""
    return sorted(tabelle, key=lambda eintrag: -eintrag[1])[0]


def kurz(tabelle):
    """Zeigt kurze Tabellen ganz, lange nur mit ihrer Länge."""
    return repr(tabelle) if len(tabelle) <= 6 else f"<Tabelle mit {len(tabelle)} Einträgen>"


TIPP_NONE = (
    "\nTipp: Legen Sie die neue Liste im Rumpf an: if tabelle is None: tabelle = []. Ein Standardwert wie [] "
    "oder eine Liste außerhalb der Funktion entsteht nur einmal und wird von allen Aufrufen geteilt."
)

# erfasse: das erste Beispiel
ergebnis, fehler = rufe(erfasse, "Sensor liefert keine Werte", 8, 3, 6)
assert ergebnis == [("Sensor liefert keine Werte", 144)], (
    f"erfasse('Sensor liefert keine Werte', 8, 3, 6) ergibt {ergebnis!r}, erwartet war "
    "[('Sensor liefert keine Werte', 144)]: eine neue Liste mit dem Tupel (fehlerart, 8 · 3 · 6)." + absturz(fehler)
    + (TIPP_NONE if isinstance(ergebnis, list) and len(ergebnis) > 1 else "")
)

# erfasse: andere Werte (nicht fest hinschreiben!)
ergebnis, fehler = rufe(erfasse, "Festplatte voll", 7, 2, 3)
assert ergebnis == [("Festplatte voll", 42)], (
    f"erfasse('Festplatte voll', 7, 2, 3) ergibt {ergebnis!r}, erwartet war [('Festplatte voll', 42)]."
    + absturz(fehler)
)

# erfasse: eine übergebene Tabelle wird ergänzt und zurückgegeben
tabelle = [("Sensor liefert keine Werte", 144)]
ergebnis, fehler = rufe(erfasse, "Zeitstempel falsch", 4, 5, 7, tabelle)
assert ergebnis is tabelle and tabelle == [("Sensor liefert keine Werte", 144), ("Zeitstempel falsch", 140)], (
    f"Nach erfasse('Zeitstempel falsch', 4, 5, 7, tabelle) ist tabelle {tabelle!r} und die Rückgabe {ergebnis!r}; "
    "erwartet war, dass tabelle selbst um ('Zeitstempel falsch', 140) ergänzt und zurückgegeben wird." + absturz(fehler)
)

# erfasse: zwei Aufrufe ohne Tabelle beginnen je eine neue Liste
erstes, fehler = rufe(erfasse, "Sensor liefert keine Werte", 8, 3, 6)
zweites, zweiter_fehler = rufe(erfasse, "Zeitstempel falsch", 4, 5, 7)
assert zweites == [("Zeitstempel falsch", 140)] and erstes == [("Sensor liefert keine Werte", 144)], (
    f"Zwei Aufrufe von erfasse ohne tabelle ergeben {erstes!r} und {zweites!r}; erwartet waren zwei getrennte "
    "Listen mit je einem Eintrag." + absturz(fehler or zweiter_fehler) + TIPP_NONE
)

# erfasse: auch nach vielen Aufrufen beginnt ein Aufruf ohne Tabelle leer
for nummer in range(5):
    rufe(erfasse, f"Fehler {nummer}", 1, 1, 1)
ergebnis, fehler = rufe(erfasse, "Netzteil fällt aus", 10, 1, 2)
assert ergebnis == [("Netzteil fällt aus", 20)], (
    f"Nach mehreren Aufrufen ergibt erfasse('Netzteil fällt aus', 10, 1, 2) {ergebnis!r}, erwartet war "
    "[('Netzteil fällt aus', 20)]." + absturz(fehler) + TIPP_NONE
)

# erfasse: eine übergebene leere Liste wird selbst gefüllt
tabelle = []
ergebnis, fehler = rufe(erfasse, "Zeitstempel falsch", 4, 5, 7, tabelle)
assert tabelle == [("Zeitstempel falsch", 140)] and ergebnis is tabelle, (
    f"Nach tabelle = [] und erfasse('Zeitstempel falsch', 4, 5, 7, tabelle) ist tabelle {tabelle!r}, erwartet war "
    "[('Zeitstempel falsch', 140)], und die Rückgabe soll tabelle selbst sein." + absturz(fehler)
    + "\nTipp: tabelle = tabelle or [] ersetzt auch eine übergebene leere Liste durch eine neue, denn [] gilt als "
    "falsch. Prüfen Sie mit is None."
)

# erfasse: kleinste und größte RPZ
ergebnis, fehler = rufe(erfasse, "Tippfehler im Hostnamen", 1, 1, 1)
groesste, zweiter_fehler = rufe(erfasse, "Datenverlust unbemerkt", 10, 10, 10)
assert ergebnis == [("Tippfehler im Hostnamen", 1)] and groesste == [("Datenverlust unbemerkt", 1000)], (
    f"erfasse(..., 1, 1, 1) ergibt {kurz(ergebnis or [])} und erfasse(..., 10, 10, 10) ergibt {kurz(groesste or [])}; erwartet waren "
    "die RPZ 1 und 1000." + absturz(fehler or zweiter_fehler)
)

# erfasse: der Standardwert der Funktion bleibt None
assert erfasse.__defaults__ == (None,), (
    f"erfasse.__defaults__ ist {erfasse.__defaults__!r}, erwartet war (None,). Lassen Sie den vorgegebenen "
    "Funktionskopf mit tabelle=None stehen."
)

# neue_analyse: das Beispiel
ergebnis, fehler = rufe(neue_analyse, "Monitoring")
erwartet = {"system": "Monitoring", "beteiligte": ["Betrieb"], "eintraege": []}
assert ergebnis is not None and dict(ergebnis) == erwartet, (
    f"neue_analyse('Monitoring') ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
)

# neue_analyse: andere Beteiligte (nicht fest hinschreiben!)
ergebnis, fehler = rufe(neue_analyse, "Backup", ("Betrieb", "Entwicklung", "Datenschutz"))
erwartet = {"system": "Backup", "beteiligte": ["Betrieb", "Entwicklung", "Datenschutz"], "eintraege": []}
assert ergebnis == erwartet, (
    f"neue_analyse('Backup', ('Betrieb', 'Entwicklung', 'Datenschutz')) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    + absturz(fehler)
)

# neue_analyse: beteiligte ist eine Liste, auch wenn ein Tupel übergeben wird
ergebnis, fehler = rufe(neue_analyse, "Monitoring")
assert ergebnis is not None and isinstance(ergebnis.get("beteiligte"), list), (
    f"neue_analyse('Monitoring')['beteiligte'] ist {ergebnis and ergebnis.get('beteiligte')!r}, erwartet war die "
    "Liste ['Betrieb'], damit man später Namen anhängen kann.\nTipp: list(beteiligte) macht aus dem Tupel eine "
    "neue Liste." + absturz(fehler)
)

# neue_analyse: ohne Beteiligte
ergebnis, fehler = rufe(neue_analyse, "Druckdienst", ())
erwartet = {"system": "Druckdienst", "beteiligte": [], "eintraege": []}
assert ergebnis == erwartet, f"neue_analyse('Druckdienst', ()) ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(
    fehler
)

# neue_analyse: zwei Analysen haben getrennte Listen eintraege
erste, fehler = rufe(neue_analyse, "Monitoring")
zweite, zweiter_fehler = rufe(neue_analyse, "Backup")
if fehler is None and zweiter_fehler is None:
    erste["eintraege"].append(("Sensor liefert keine Werte", 144))
assert zweite is not None and zweite["eintraege"] == [], (
    f"Nach erste['eintraege'].append(...) hat auch die zweite Analyse die eintraege {zweite and zweite['eintraege']!r}, "
    "erwartet war []. Beide teilen sich eine Liste.\nTipp: Schreiben Sie [] direkt in das Dictionary, das "
    "neue_analyse zurückgibt; dann entsteht bei jedem Aufruf eine neue Liste." + absturz(fehler or zweiter_fehler)
)

# neue_analyse: zwei Analysen haben getrennte Listen beteiligte
erste, fehler = rufe(neue_analyse, "Monitoring")
zweite, zweiter_fehler = rufe(neue_analyse, "Backup")
if fehler is None and zweiter_fehler is None and isinstance(erste["beteiligte"], list):
    erste["beteiligte"].append("Entwicklung")
assert zweite is not None and zweite["beteiligte"] == ["Betrieb"], (
    "Nach erste['beteiligte'].append('Entwicklung') hat die zweite Analyse die Beteiligten "
    f"{zweite and zweite['beteiligte']!r}, erwartet war ['Betrieb']." + absturz(fehler or zweiter_fehler)
)

# neue_analyse: eine übergebene Liste wird nicht geteilt
namen = ["Betrieb", "Entwicklung"]
ergebnis, fehler = rufe(neue_analyse, "Monitoring", namen)
if fehler is None:
    ergebnis["beteiligte"].append("Qualitätssicherung")
assert namen == ["Betrieb", "Entwicklung"], (
    f"Nach neue_analyse('Monitoring', namen) und einem append an ['beteiligte'] ist namen {namen!r}, erwartet war "
    "['Betrieb', 'Entwicklung']: Die Analyse soll eine eigene Liste haben.\nTipp: list(beteiligte) legt eine neue "
    "Liste an, auch wenn beteiligte schon eine Liste ist." + absturz(fehler)
)

# neue_analyse: spätere Analysen beginnen wieder mit den Standardwerten
for system in ["Monitoring", "Backup", "Druckdienst"]:
    analyse, fehler = rufe(neue_analyse, system)
    if fehler is None:
        analyse["beteiligte"].append("Entwicklung")
        analyse["eintraege"].append(("Fehler", 1))
ergebnis, fehler = rufe(neue_analyse, "Mailserver")
erwartet = {"system": "Mailserver", "beteiligte": ["Betrieb"], "eintraege": []}
assert ergebnis == erwartet and neue_analyse.__defaults__ == (("Betrieb",),), (
    f"Nach drei veränderten Analysen ergibt neue_analyse('Mailserver') {ergebnis!r}, erwartet war {erwartet!r}; "
    f"neue_analyse.__defaults__ ist {neue_analyse.__defaults__!r}." + absturz(fehler)
)

# hoechste_rpz: das Beispiel
TABELLE = [("Sensor liefert keine Werte", 144), ("Zeitstempel falsch", 140), ("Alarm-Mail landet im Spam", 180)]
ergebnis, fehler = rufe(hoechste_rpz, list(TABELLE))
assert ergebnis == ("Alarm-Mail landet im Spam", 180), (
    f"hoechste_rpz({TABELLE!r}) ergibt {ergebnis!r}, erwartet war ('Alarm-Mail landet im Spam', 180)."
    + absturz(fehler)
)

# hoechste_rpz: die höchste RPZ steht vorn (nicht fest hinschreiben!)
tabelle = [("Netzteil fällt aus", 200), ("Festplatte voll", 42), ("Zeitstempel falsch", 140)]
ergebnis, fehler = rufe(hoechste_rpz, list(tabelle))
assert ergebnis == ("Netzteil fällt aus", 200), (
    f"hoechste_rpz({tabelle!r}) ergibt {ergebnis!r}, erwartet war ('Netzteil fällt aus', 200)." + absturz(fehler)
)

# hoechste_rpz: bei Gleichstand das vordere Tupel
tabelle = [("Festplatte voll", 42), ("Lüfter laut", 90), ("Kabel locker", 90)]
ergebnis, fehler = rufe(hoechste_rpz, list(tabelle))
assert ergebnis == ("Lüfter laut", 90), (
    f"hoechste_rpz({tabelle!r}) ergibt {ergebnis!r}, erwartet war ('Lüfter laut', 90): Bei gleicher RPZ zählt "
    "das vordere Tupel.\nTipp: Ersetzen Sie den bisher besten Eintrag nur bei einer echt größeren RPZ." + absturz(fehler)
)

# hoechste_rpz: eine Tabelle mit einem Eintrag
ergebnis, fehler = rufe(hoechste_rpz, [("Tippfehler im Hostnamen", 1)])
assert ergebnis == ("Tippfehler im Hostnamen", 1), (
    f"hoechste_rpz([('Tippfehler im Hostnamen', 1)]) ergibt {ergebnis!r}, erwartet war ('Tippfehler im Hostnamen', 1)."
    + absturz(fehler)
)

# hoechste_rpz: eine nicht leere Tabelle ignoriert standard
ergebnis, fehler = rufe(hoechste_rpz, list(TABELLE), ("keine", 0))
assert ergebnis == ("Alarm-Mail landet im Spam", 180), (
    f"hoechste_rpz(tabelle, ('keine', 0)) ergibt {ergebnis!r}, erwartet war ('Alarm-Mail landet im Spam', 180): "
    "standard gilt nur für eine leere Tabelle." + absturz(fehler)
)

# hoechste_rpz: leere Tabelle mit einem Standardwert
ergebnis, fehler = rufe(hoechste_rpz, [], ("keine Fehlerart", 0))
assert ergebnis == ("keine Fehlerart", 0), (
    f"hoechste_rpz([], ('keine Fehlerart', 0)) ergibt {ergebnis!r}, erwartet war ('keine Fehlerart', 0)."
    + absturz(fehler)
)

# hoechste_rpz: leere Tabelle ohne Standardwert löst ValueError aus
ergebnis, fehler = rufe(hoechste_rpz, [])
assert isinstance(fehler, ValueError), (
    f"hoechste_rpz([]) soll einen ValueError auslösen, ergibt aber {ergebnis!r}"
    + (f" bzw. löst {type(fehler).__name__} aus." if fehler else ".")
    + "\nTipp: if standard is FEHLT: raise ValueError(...)"
)

# hoechste_rpz: leere Tabelle mit standard=None gibt None zurück
ergebnis, fehler = rufe(hoechste_rpz, [], None)
assert fehler is None and ergebnis is None, (
    f"hoechste_rpz([], None) soll None zurückgeben, löst aber {type(fehler).__name__}: {fehler} aus.\n"
    "Tipp: None ist hier ein erlaubter Standardwert. Prüfen Sie nicht standard is None, sondern standard is FEHLT."
    if fehler
    else f"hoechste_rpz([], None) ergibt {ergebnis!r}, erwartet war None."
)

# hoechste_rpz verändert die Tabelle nicht
tabelle = list(TABELLE)
rufe(hoechste_rpz, tabelle)
assert tabelle == TABELLE, f"hoechste_rpz hat die Tabelle verändert, sie ist jetzt {tabelle!r}, erwartet war {TABELLE!r}."

# 300 zufällige Analysen: erfasse und hoechste_rpz
zufall = Zufall(4080)
for _ in range(300):
    tabelle = None
    erwartet = []
    for nummer in range(zufall.randint(1, 8)):
        b, a, e = zufall.randint(1, 10), zufall.randint(1, 10), zufall.randint(1, 10)
        if nummer == 0:
            tabelle, fehler = rufe(erfasse, f"Fehlerart {nummer}", b, a, e)
        else:
            ergebnis, fehler = rufe(erfasse, f"Fehlerart {nummer}", b, a, e, tabelle)
        erwartet.append((f"Fehlerart {nummer}", b * a * e))
        assert tabelle == erwartet, (
            f"Nach erfasse(..., {b}, {a}, {e}) ist die Tabelle {kurz(tabelle or [])}, erwartet war {erwartet!r}."
            + absturz(fehler)
        )
    ergebnis, fehler = rufe(hoechste_rpz, list(erwartet))
    assert ergebnis == vergleich_hoechste(erwartet), (
        f"hoechste_rpz({erwartet!r}) ergibt {ergebnis!r}, erwartet war {vergleich_hoechste(erwartet)!r}."
        + absturz(fehler)
    )

# Obere Grenze: 100 000 Einträge erfassen und den höchsten finden
tabelle = erfasse("F0", 1, 1, 1)
for nummer in range(1, 100000):
    erfasse(f"F{nummer}", nummer % 10 + 1, nummer % 7 + 1, nummer % 9 + 1, tabelle)
erwartet = vergleich_hoechste(tabelle)
ergebnis, fehler = rufe(hoechste_rpz, tabelle)
assert len(tabelle) == 100000 and ergebnis == erwartet, (
    f"Mit 100 000 erfassten Einträgen hat die Tabelle {len(tabelle)} Einträge und hoechste_rpz ergibt {ergebnis!r}, "
    f"erwartet waren 100 000 Einträge und {erwartet!r}." + absturz(fehler)
)
