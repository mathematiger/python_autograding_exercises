# Automatisch erzeugt aus lehrkraft/muster/2_058_stammkunden.py - nicht von Hand ändern.
# vorlage-hash: 782306ae25897143
# text-hash: df8b97d2dd776212
# thema: algorithmen
# inhalt: Schleifen-Invariante, Wertetabelle

BEISPIEL = [104, 104, 117, 120, 120, 120, 131, 131]
RICHTIGE_TABELLE = [
    (104, 1, 1), (104, 2, 2), (117, 1, 2), (120, 1, 2),
    (120, 2, 2), (120, 3, 3), (131, 1, 3), (131, 2, 3),
]


def wert_von(funktion, nummern):
    """Ruft funktion mit einer Kopie von nummern auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(list(nummern))
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def spalte(tabelle, stelle):
    """Gibt eine Spalte der Tabelle zurück; Zeilen, die keine Dreiertupel sind, ergeben None."""
    werte = []
    for zeile in tabelle:
        if isinstance(zeile, (tuple, list)) and len(zeile) == 3:
            werte.append(zeile[stelle])
        else:
            werte.append(None)
    return werte


def erste_abweichung(tabelle, stelle):
    """Gibt die Nummer der ersten Zeile zurück, deren Spalte stelle falsch ist, oder None."""
    eigene = spalte(tabelle, stelle)
    richtige = spalte(RICHTIGE_TABELLE, stelle)
    for nummer in range(len(richtige)):
        if nummer >= len(eigene) or eigene[nummer] != richtige[nummer]:
            return nummer
    return None


def zaehle_kunden(nummern):
    """Vergleichslösung: zählt jede Nummer in einem Dictionary statt über Serien."""
    anzahl = {}
    for nummer in nummern:
        anzahl[nummer] = anzahl.get(nummer, 0) + 1
    return anzahl


def vergleich_serie(nummern):
    """Vergleichslösung für laengste_serie."""
    anzahl = zaehle_kunden(nummern)
    return max(anzahl.values()) if anzahl else 0


def vergleich_kunde(nummern):
    """Vergleichslösung für stammkunde: die kleinste Nummer mit der größten Anzahl."""
    anzahl = zaehle_kunden(nummern)
    if not anzahl:
        return None
    meiste = max(anzahl.values())
    return min(nummer for nummer in anzahl if anzahl[nummer] == meiste)


def meldung(funktion, nummern, erwartet, hinweis=""):
    """Prüft funktion(nummern) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, nummern)
    gezeigt = nummern if len(nummern) <= 20 else f"<{len(nummern)} Nummern>"
    text = f"{funktion.__name__}({gezeigt}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"
    return ergebnis == erwartet, text


def zufallsnummern(zufall, kunden, hoechstens):
    """Erzeugt eine sortierte Liste, in der jeder Kunde 1 bis hoechstens Bestellungen hat."""
    nummern = []
    for nummer in sorted(zufall.sample(range(1, 1000001), kunden)):
        nummern.extend([nummer] * zufall.randint(1, hoechstens))
    return nummern


# TABELLE: eine Zeile je Wert des Beispiels
assert isinstance(TABELLE, list) and len(TABELLE) == 8, (
    f"TABELLE hat {len(TABELLE) if isinstance(TABELLE, list) else TABELLE!r} Zeilen, erwartet waren 8, "
    "eine je Wert des Beispiels.\nTipp: TABELLE = [(104, 1, 1), (104, 2, 2), (117, 1, 2), …]"
)

# TABELLE: die erste Spalte ist der gelesene Wert
zeile = erste_abweichung(TABELLE, 0)
assert zeile is None, (
    f"In Zeile {zeile + 1 if zeile is not None else ''} von TABELLE stimmt der Wert nicht: "
    f"{TABELLE[zeile] if zeile is not None and zeile < len(TABELLE) else '(fehlt)'}.\n"
    f"Die Werte sind der Reihe nach {BEISPIEL}; jede Zeile ist ein Tupel (wert, aktuell, laengste)."
)

# TABELLE: aktuell ist die Länge der laufenden Serie
zeile = erste_abweichung(TABELLE, 1)
assert zeile is None, (
    f"In Zeile {zeile + 1 if zeile is not None else ''} von TABELLE stimmt aktuell nicht: "
    f"{TABELLE[zeile] if zeile is not None and zeile < len(TABELLE) else '(fehlt)'}.\n"
    "Tipp: Ist der Wert gleich dem vorigen, wird aktuell um 1 größer, sonst beginnt eine neue Serie mit 1."
)

# TABELLE: laengste ist die längste Serie bisher
zeile = erste_abweichung(TABELLE, 2)
assert zeile is None, (
    f"In Zeile {zeile + 1 if zeile is not None else ''} von TABELLE stimmt laengste nicht: "
    f"{TABELLE[zeile] if zeile is not None and zeile < len(TABELLE) else '(fehlt)'}.\n"
    "Tipp: laengste ist die längste Serie unter allen bisher gelesenen Werten; sie wird nie kleiner."
)

# laengste_serie: das Beispiel
stimmt, text = meldung(laengste_serie, BEISPIEL, 3, "\nTipp: Gehen Sie Ihre Schleife Zeile für Zeile mit TABELLE durch.")
assert stimmt, text

# laengste_serie: andere Nummern (nicht fest hinschreiben!)
stimmt, text = meldung(laengste_serie, [5, 5, 5, 5, 9], 4)
assert stimmt, text

# laengste_serie: die längste Serie steht am Anfang
stimmt, text = meldung(
    laengste_serie, [7, 7, 7, 8, 9, 9], 3,
    "\nTipp: Eine neue Serie beginnt mit aktuell = 1; laengste darf dabei nicht kleiner werden.",
)
assert stimmt, text

# laengste_serie: die längste Serie steht am Ende
stimmt, text = meldung(
    laengste_serie, [1, 2, 2, 3, 3, 3], 3,
    "\nTipp: Vergleichen Sie aktuell in jedem Durchlauf mit laengste, nicht erst, wenn eine neue Serie beginnt.",
)
assert stimmt, text

# laengste_serie: alle Nummern verschieden
stimmt, text = meldung(laengste_serie, [10, 20, 30, 40], 1)
assert stimmt, text

# laengste_serie: alle Nummern gleich
stimmt, text = meldung(laengste_serie, [42, 42, 42], 3)
assert stimmt, text

# laengste_serie: eine einzige Bestellung
stimmt, text = meldung(laengste_serie, [1000000], 1, "\nTipp: Auch der erste Wert beginnt eine Serie der Länge 1.")
assert stimmt, text

# laengste_serie: keine Bestellungen
stimmt, text = meldung(laengste_serie, [], 0)
assert stimmt, text

# stammkunde: das Beispiel
stimmt, text = meldung(
    stammkunde, BEISPIEL, 120,
    "\nTipp: Merken Sie sich in einer weiteren Variable den Wert, wenn laengste größer wird.",
)
assert stimmt, text

# stammkunde: andere Nummern
stimmt, text = meldung(stammkunde, [5, 9, 9, 9, 9, 12, 12], 9)
assert stimmt, text

# stammkunde: bei Gleichstand die kleinste Nummer
stimmt, text = meldung(
    stammkunde, [3, 3, 8, 8], 3,
    "\nTipp: Übernehmen Sie einen neuen Kunden nur, wenn seine Serie echt länger ist (> statt >=).",
)
assert stimmt, text

# stammkunde: der fleißigste Kunde steht am Ende
stimmt, text = meldung(stammkunde, [1, 2, 2], 2)
assert stimmt, text

# stammkunde: alle Nummern verschieden
stimmt, text = meldung(stammkunde, [10, 20, 30], 10)
assert stimmt, text

# stammkunde: eine einzige Bestellung
stimmt, text = meldung(stammkunde, [77], 77)
assert stimmt, text

# stammkunde: keine Bestellungen
stimmt, text = meldung(stammkunde, [], None, "\nTipp: Beginnen Sie mit bester = None.")
assert stimmt, text

# Die Funktionen verändern nummern nicht
nummern = list(BEISPIEL)
try:
    laengste_serie(nummern)
    stammkunde(nummern)
except Exception:
    pass
assert nummern == BEISPIEL, f"Nach den Aufrufen ist nummern {nummern}; die Liste sollte unverändert bleiben."

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("3\n120"), f"Erwartete Ausgabe:\n3\n120\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(2058)
faelle = []
for _ in range(300):
    faelle.append(zufallsnummern(zufall, zufall.randint(0, 8), zufall.randint(1, 5)))

# laengste_serie: viele zufällige Exporte
for nummern in faelle:
    stimmt, text = meldung(laengste_serie, nummern, vergleich_serie(nummern))
    assert stimmt, text

# stammkunde: dieselben zufälligen Exporte
for nummern in faelle:
    stimmt, text = meldung(stammkunde, nummern, vergleich_kunde(nummern))
    assert stimmt, text

# Obere Grenze: 100 000 Bestellungen, laengste_serie liest jeden Eintrag nur wenige Male
nummern = zufallsnummern(zufall, 1500, 200)[:100000]
liste = Zaehlliste(nummern)
try:
    ergebnis = laengste_serie(liste)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
erwartet = vergleich_serie(nummern)
if ergebnis != erwartet:
    text = f"Bei {len(nummern)} Bestellungen ergibt laengste_serie {ergebnis!r}, erwartet war {erwartet}."
    if "AttributeError" in str(ergebnis):
        text += (
            "\nTipp: Die Tests geben hier eine Liste, die Zugriffe zählt und keine Methoden wie count kennt. "
            "count liest die ganze Liste für jeden Eintrag; gehen Sie die Liste einmal mit einer Schleife durch."
        )
else:
    text = (
        f"laengste_serie braucht bei {len(nummern)} Bestellungen {liste.lesezugriffe} Zugriffe auf die Liste; "
        f"erlaubt sind {2 * len(nummern) + 5}, etwa zwei je Eintrag.\n"
        "Tipp: Eine einzige Schleife, die sich den vorigen Wert merkt, statt count oder einer zweiten Schleife."
    )
assert ergebnis == erwartet and liste.lesezugriffe <= 2 * len(nummern) + 5, text

# Obere Grenze: stammkunde bei 100 000 Bestellungen
liste = Zaehlliste(nummern)
try:
    ergebnis = stammkunde(liste)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
erwartet = vergleich_kunde(nummern)
erlaubt = 2 * len(nummern) + vergleich_serie(nummern) + 5
if ergebnis != erwartet:
    text = f"Bei {len(nummern)} Bestellungen ergibt stammkunde {ergebnis!r}, erwartet war {erwartet}."
    if "AttributeError" in str(ergebnis):
        text += (
            "\nTipp: Die Tests geben hier eine Liste, die Zugriffe zählt und keine Methoden wie count kennt. "
            "count liest die ganze Liste für jeden Eintrag; gehen Sie die Liste einmal mit einer Schleife durch."
        )
else:
    text = (
        f"stammkunde braucht bei {len(nummern)} Bestellungen {liste.lesezugriffe} Zugriffe auf die Liste; "
        f"erlaubt sind {erlaubt}, etwa zwei je Eintrag.\n"
        "Tipp: Eine einzige Schleife, die sich den vorigen Wert und den bisher besten Kunden merkt."
    )
assert ergebnis == erwartet and liste.lesezugriffe <= erlaubt, text
