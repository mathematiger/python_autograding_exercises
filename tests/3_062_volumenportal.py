# Automatisch erzeugt aus lehrkraft/muster/3_062_volumenportal.py - nicht von Hand ändern.
# vorlage-hash: a3e5592bba7d6c9b
# text-hash: e7ae2ea5d647d0d3
# thema: algorithmen
# inhalt: Präfixsummen, Bereichssummen

WERTE = [120, 80, 0, 300, 45, 60, 210, 15]
PRAEFIX = [0, 120, 200, 200, 500, 545, 605, 815, 830]


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Listen auf; ein Fehler wird als Text zurückgegeben."""
    kopien = [list(argument) if isinstance(argument, list) else argument for argument in argumente]
    try:
        return funktion(*kopien)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(wert):
    """Kürzt lange Listen für Meldungen."""
    text = repr(wert)
    return text if len(text) <= 200 else f"<Liste mit {len(wert)} Einträgen>" if isinstance(wert, list) else text[:150] + " …"


def vergleich(werte, anfragen):
    """Vergleichslösung: summiert jeden Zeitraum einzeln (langsam, aber offensichtlich richtig)."""
    return [sum(werte[von:bis]) for von, bis in anfragen]


def meldung(funktion, argumente, erwartet, hinweis=""):
    """Prüft funktion(*argumente) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, *argumente)
    gezeigt = ", ".join(kurz(argument) for argument in argumente)
    text = f"{funktion.__name__}({gezeigt}) ergibt {kurz(ergebnis)}, erwartet war {kurz(erwartet)}.{hinweis}"
    return ergebnis == erwartet, text


def zufallsanfragen(zufall, laenge, anzahl):
    """Erzeugt Zeiträume (von, bis) mit 0 ≤ von ≤ bis ≤ laenge."""
    anfragen = []
    for _ in range(anzahl):
        von, bis = sorted((zufall.randint(0, laenge), zufall.randint(0, laenge)))
        anfragen.append((von, bis))
    return anfragen


# praefixsummen: das Beispiel
stimmt, text = meldung(
    praefixsummen, [WERTE], PRAEFIX,
    "\nTipp: Beginnen Sie mit [0] und hängen Sie nach jedem Wert die laufende Summe an.",
)
assert stimmt, text

# praefixsummen: andere Werte (nicht fest hinschreiben!)
stimmt, text = meldung(praefixsummen, [[3, 1, 4, 1, 5]], [0, 3, 4, 8, 9, 14])
assert stimmt, text

# praefixsummen: ein Eintrag mehr als werte, vorn die 0
ergebnis = wert_von(praefixsummen, [7, 7])
assert isinstance(ergebnis, list) and len(ergebnis) == 3 and ergebnis[0] == 0, (
    f"praefixsummen([7, 7]) ergibt {ergebnis!r}, erwartet war [0, 7, 14]: ein Eintrag mehr als werte, "
    "und p[0] ist 0, die Summe von null Werten."
)

# praefixsummen: Minuten ohne Übertragung
stimmt, text = meldung(praefixsummen, [[0, 0, 5, 0]], [0, 0, 0, 5, 5])
assert stimmt, text

# praefixsummen: keine Messwerte
stimmt, text = meldung(praefixsummen, [[]], [0], "\nTipp: Auch ohne Werte enthält p die 0 für die leere Summe.")
assert stimmt, text

# volumen: das Beispiel
stimmt, text = meldung(volumen, [PRAEFIX, 2, 5], 345, "\nTipp: p[bis] - p[von].")
assert stimmt, text

# volumen: ein anderer Zeitraum
stimmt, text = meldung(volumen, [PRAEFIX, 5, 7], 270)
assert stimmt, text

# volumen: ab der ersten Minute
stimmt, text = meldung(volumen, [PRAEFIX, 0, 3], 200)
assert stimmt, text

# volumen: bis zur letzten Minute
stimmt, text = meldung(
    volumen, [PRAEFIX, 6, 8], 225,
    "\nTipp: bis gehört nicht mehr dazu; werte[6:8] sind die Minuten 6 und 7, also p[8] - p[6].",
)
assert stimmt, text

# volumen: eine einzige Minute
stimmt, text = meldung(volumen, [PRAEFIX, 3, 4], 300)
assert stimmt, text

# volumen: leerer Zeitraum
stimmt, text = meldung(volumen, [PRAEFIX, 4, 4], 0)
assert stimmt, text

# volumen: ohne Schleife, nur zwei Zugriffe auf die Präfixsummen
liste = Zaehlliste(list(range(0, 200001, 2)))
try:
    ergebnis = volumen(liste, 0, 100000)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == 200000 and liste.lesezugriffe <= 2, (
    f"volumen(p, 0, 100000) ergibt {ergebnis!r} (erwartet 200000) mit {liste.lesezugriffe} Zugriffen auf p; "
    "erwartet waren höchstens 2.\nTipp: Die Summe eines Zeitraums ist p[bis] - p[von], ganz ohne Schleife."
)

# beantworte: das Beispiel
stimmt, text = meldung(beantworte, [WERTE, [(0, 8), (3, 4), (2, 2)]], [830, 300, 0])
assert stimmt, text

# beantworte: andere Zeiträume in ihrer Reihenfolge
stimmt, text = meldung(beantworte, [WERTE, [(5, 7), (0, 1), (1, 3), (7, 8)]], [270, 120, 80, 15])
assert stimmt, text

# beantworte: keine Anfragen
stimmt, text = meldung(beantworte, [WERTE, []], [])
assert stimmt, text

# beantworte: keine Messwerte, nur leere Zeiträume
stimmt, text = meldung(beantworte, [[], [(0, 0), (0, 0)]], [0, 0])
assert stimmt, text

# beantworte benutzt praefixsummen
aufrufe = []
eigene_praefixsummen = praefixsummen


def praefixsummen(werte):
    """Zählt die Aufrufe und reicht sie an die eigene Funktion weiter."""
    aufrufe.append(len(werte))
    return eigene_praefixsummen(werte)


try:
    beantworte(list(WERTE), [(0, 8), (3, 4), (2, 2)])
except Exception:
    pass
praefixsummen = eigene_praefixsummen
assert len(aufrufe) == 1, (
    f"beantworte hat praefixsummen {len(aufrufe)}-mal aufgerufen; erwartet war genau einmal, vor der Schleife "
    "über die Anfragen."
)

# Die Ausgabe des Programms
erwartet = "[0, 120, 200, 200, 500, 545, 605, 815, 830]\n345\n[830, 300, 0]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Messreihen
zufall = Zufall(3062)
for _ in range(300):
    werte = [zufall.randint(0, zufall.choice([5, 100000])) for _ in range(zufall.randint(0, 15))]
    anfragen = zufallsanfragen(zufall, len(werte), zufall.randint(0, 6))
    stimmt, text = meldung(beantworte, [werte, anfragen], vergleich(werte, anfragen))
    assert stimmt, text

# Laufzeit: beantworte liest jeden Messwert nur wenige Male
werte = [zufall.randint(0, 100000) for _ in range(3000)]
anfragen = [(zufall.randint(0, 100), zufall.randint(2900, 3000)) for _ in range(3000)]
liste = Zaehlliste(werte)
try:
    ergebnis = beantworte(liste, anfragen)
except Exception as fehler:
    ergebnis = f"{type(fehler).__name__}: {fehler}"
assert ergebnis == vergleich(werte, anfragen) and liste.lesezugriffe <= 2 * len(werte) + 10, (
    f"beantworte für 3000 Werte und 3000 lange Zeiträume braucht {liste.lesezugriffe} Zugriffe auf werte, "
    f"erlaubt sind {2 * len(werte) + 10} (O(n + q)); jede Anfrage einzeln zu summieren kostet etwa neun Millionen.\n"
    "Tipp: Rechnen Sie die Präfixsummen einmal vor der Schleife aus und beantworten Sie jede Anfrage mit volumen."
)

# Obere Grenze: 100 000 Werte und 100 000 Anfragen
werte = [zufall.randint(0, 100000) for _ in range(100000)]
anfragen = zufallsanfragen(zufall, len(werte), 100000)
ergebnis = wert_von(beantworte, werte, anfragen)
praefix = [0]
for wert in werte:
    praefix.append(praefix[-1] + wert)
erwartet = [praefix[bis] - praefix[von] for von, bis in anfragen]
assert ergebnis == erwartet, (
    f"Bei 100 000 Werten und 100 000 Anfragen stimmt beantworte nicht: erste Abweichung bei Anfrage "
    f"{next((i for i in range(len(erwartet)) if not isinstance(ergebnis, list) or i >= len(ergebnis) or ergebnis[i] != erwartet[i]), '?')}"
    f", Ergebnis {kurz(ergebnis)}."
)
