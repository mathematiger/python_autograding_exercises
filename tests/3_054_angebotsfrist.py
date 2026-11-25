# Automatisch erzeugt aus lehrkraft/muster/3_054_angebotsfrist.py - nicht von Hand ändern.
# vorlage-hash: a7748ce1c3e617f8
# text-hash: f80118314b60eefa
# thema: texte_zahlen
# inhalt: Datum zerlegen und prüfen

import ast
import datetime
import re

ANGEBOTE = [
    ("Nordtech", "30.11.2026"),
    ("Bürowelt", "20.11.2026"),
    ("Kabelkönig", "31.11.2026"),
    ("Datafix", "23.11.2026"),
]


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_datum(text):
    """Vergleichslösung mit regulärem Ausdruck und datetime.date, also anders als verlangt."""
    treffer = re.fullmatch(r"(\d\d)\.(\d\d)\.(\d\d\d\d)", text.strip())
    if treffer is None:
        return None
    tag, monat, jahr = (int(teil) for teil in treffer.groups())
    if not 1900 <= jahr <= 2099:
        return None
    try:
        datetime.date(jahr, monat, tag)
    except ValueError:
        return None
    return (tag, monat, jahr)


def vergleich_gueltig(angebote, heute):
    """Vergleichslösung für noch_gueltig über datetime.date."""
    tag, monat, jahr = vergleich_datum(heute)
    stichtag = datetime.date(jahr, monat, tag)
    namen = []
    for name, text in angebote:
        datum = vergleich_datum(text)
        if datum is not None and datetime.date(datum[2], datum[1], datum[0]) >= stichtag:
            namen.append(name)
    return namen


def meldung_datum(text, hinweis=""):
    """Prüft zerlege_datum für einen Text; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(zerlege_datum, text)
    erwartet = vergleich_datum(text)
    return ergebnis == erwartet, f"zerlege_datum({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"


def zufallstext(zufall):
    """Erzeugt einen Text, der oft ein gültiges Datum ist und sonst knapp daneben liegt."""
    tag = zufall.randint(0, 32)
    monat = zufall.randint(0, 13)
    jahr = zufall.choice([1899, 1900, 1999, 2000, 2023, 2024, 2025, 2026, 2099, 2100])
    text = f"{tag:02d}.{monat:02d}.{jahr}"
    art = zufall.randint(0, 9)
    if art == 0:
        text = f"{tag}.{monat}.{jahr}"
    elif art == 1:
        stelle = zufall.randint(0, len(text) - 1)
        text = text[:stelle] + zufall.choice(" -/+a,") + text[stelle + 1 :]
    elif art == 2:
        text = zufall.choice(["", " ", "  "]) + text + zufall.choice(["", " ", "  "])
    return text


# Das Beispiel wird zerlegt
ergebnis = wert_von(zerlege_datum, "27.11.2026")
assert ergebnis == (27, 11, 2026), (
    f"zerlege_datum('27.11.2026') ergibt {ergebnis!r}, erwartet war (27, 11, 2026).\n"
    "Tipp: Zerlegen Sie mit split('.') und wandeln Sie jeden Teil mit int() um, in der Reihenfolge Tag, Monat, Jahr."
)

# Ein zweites Datum mit führenden Nullen (nicht fest hinschreiben!)
ergebnis = wert_von(zerlege_datum, "01.02.2027")
assert ergebnis == (1, 2, 2027), (
    f"zerlege_datum('01.02.2027') ergibt {ergebnis!r}, erwartet war (1, 2, 2027) mit ganzen Zahlen, nicht Texten."
)

# Leerzeichen am Rand sind erlaubt
ergebnis = wert_von(zerlege_datum, " 01.02.2027 ")
assert ergebnis == (1, 2, 2027), (
    f"zerlege_datum(' 01.02.2027 ') ergibt {ergebnis!r}, erwartet war (1, 2, 2027).\n"
    "Tipp: Entfernen Sie zuerst mit strip() die Leerzeichen am Rand."
)

# Andere Trennzeichen sind ungültig
for text in ["2026-11-27", "27/11/2026", "27,11,2026"]:
    stimmt, text = meldung_datum(text, "\nTipp: Prüfen Sie, ob an den Stellen 2 und 5 ein Punkt steht.")
    assert stimmt, text

# Einstellige Tage und Monate sind ungültig
for text in ["1.12.2026", "01.1.2026", "1.1.2026"]:
    stimmt, text = meldung_datum(text, "\nTipp: Das Datum muss genau 10 Zeichen lang sein.")
    assert stimmt, text

# Zweistellige Jahre und zu viele Ziffern sind ungültig
for text in ["27.11.26", "27.11.20266", "027.11.2026"]:
    stimmt, text = meldung_datum(text)
    assert stimmt, text

# Buchstaben statt Ziffern sind ungültig
for text in ["2a.11.2026", "27.11.20x6", "TT.MM.JJJJ"]:
    stimmt, text = meldung_datum(text, "\nTipp: Prüfen Sie jeden Teil mit isdigit(), bevor Sie int() aufrufen.")
    assert stimmt, text

# Vorzeichen und Leerzeichen im Inneren sind ungültig, obwohl int() sie annimmt
for text in ["+1.12.2026", "01. 2.2026", "-1.12.2026", "01.12. 2026"]:
    stimmt, text = meldung_datum(
        text, "\nTipp: int(' 2') und int('+1') klappen; prüfen Sie deshalb vorher mit isdigit(), ob nur Ziffern dastehen."
    )
    assert stimmt, text

# Monat 0 und 13 gibt es nicht
for text in ["15.00.2026", "15.13.2026"]:
    stimmt, text = meldung_datum(text, "\nTipp: Der Monat liegt zwischen 1 und 12.")
    assert stimmt, text

# Tag 0 und der 32. gibt es nicht
for text in ["00.05.2026", "32.05.2026"]:
    stimmt, text = meldung_datum(text)
    assert stimmt, text

# Monate mit 30 Tagen
for text in ["30.04.2026", "31.04.2026", "31.11.2026"]:
    stimmt, text = meldung_datum(text, "\nTipp: Vergleichen Sie den Tag mit tage_im_monat(jahr, monat).")
    assert stimmt, text

# Der 29. Februar nur im Schaltjahr
for text in ["29.02.2024", "29.02.2026", "29.02.2000", "29.02.1900"]:
    stimmt, text = meldung_datum(text, "\nTipp: tage_im_monat beachtet das Schaltjahr; rufen Sie es mit dem Jahr auf.")
    assert stimmt, text

# Jahre an den Rändern 1900 und 2099
for text in ["01.01.1900", "31.12.2099", "31.12.1899", "01.01.2100"]:
    stimmt, text = meldung_datum(text, "\nTipp: Das Jahr liegt zwischen 1900 und 2099, beide eingeschlossen.")
    assert stimmt, text

# Leerer Text und nur Leerzeichen
for text in ["", "   "]:
    stimmt, text = meldung_datum(text)
    assert stimmt, text

# noch_gueltig: das Beispiel
ergebnis = wert_von(noch_gueltig, ANGEBOTE, "23.11.2026")
assert ergebnis == ["Nordtech", "Datafix"], (
    f"noch_gueltig(angebote, '23.11.2026') ergibt {ergebnis!r}, erwartet war ['Nordtech', 'Datafix'].\n"
    "Tipp: Ein Angebot, das heute endet, gilt noch (>=); Kabelkönig hat den ungültigen 31.11."
)

# noch_gueltig: über Monats- und Jahresgrenzen richtig vergleichen
angebote = [("A", "05.01.2027"), ("B", "28.12.2026"), ("C", "01.12.2026"), ("D", "30.11.2026")]
ergebnis = wert_von(noch_gueltig, angebote, "01.12.2026")
assert ergebnis == ["A", "B", "C"], (
    f"noch_gueltig({angebote}, '01.12.2026') ergibt {ergebnis!r}, erwartet war ['A', 'B', 'C'].\n"
    "Tipp: Vergleichen Sie Tupel in der Reihenfolge (jahr, monat, tag), nicht (tag, monat, jahr)."
)

# noch_gueltig: leere Liste und nur ungültige Daten
for angebote in [[], [("X", "31.02.2026"), ("Y", "morgen")]]:
    ergebnis = wert_von(noch_gueltig, angebote, "23.11.2026")
    assert ergebnis == [], f"noch_gueltig({angebote}, '23.11.2026') ergibt {ergebnis!r}, erwartet war []."

# Die Ausgabe des Programms
erwartet = "(27, 11, 2026)\n['Nordtech', 'Datafix']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Texte
zufall = Zufall(3054)
for _ in range(3000):
    stimmt, text = meldung_datum(zufallstext(zufall))
    assert stimmt, text

# Viele zufällige Angebotslisten
for _ in range(200):
    angebote = [(f"H{nummer}", zufallstext(zufall)) for nummer in range(zufall.randint(0, 8))]
    heute = zufall.choice(["01.01.1900", "23.11.2026", "29.02.2024", "31.12.2099", "15.06.2025"])
    ergebnis = wert_von(noch_gueltig, angebote, heute)
    erwartet = vergleich_gueltig(angebote, heute)
    assert ergebnis == erwartet, f"noch_gueltig({angebote}, {heute!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 10 000 Angebote
angebote = [(f"H{nummer}", zufallstext(zufall)) for nummer in range(10000)]
assert wert_von(noch_gueltig, angebote, "23.11.2026") == vergleich_gueltig(angebote, "23.11.2026"), (
    "Bei 10 000 Angeboten stimmt das Ergebnis von noch_gueltig nicht."
)



def importiert_datetime():
    """Prüft am Syntaxbaum des Programms, ob es das Modul datetime importiert."""
    with open(__file__, encoding="utf-8-sig") as datei:
        baum = ast.parse(datei.read())
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            for eintrag in knoten.names:
                if eintrag.name.split(".")[0] == "datetime":
                    return True
        if isinstance(knoten, ast.ImportFrom) and knoten.module == "datetime":
            return True
    return False


# Ohne das Modul datetime
assert not verwendet("datetime") and not importiert_datetime(), "Ihr Code verwendet datetime. Prüfen Sie das Datum mit split, isdigit und int."
