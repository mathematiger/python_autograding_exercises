# Automatisch erzeugt aus lehrkraft/muster/1_044_lebenszykluskosten.py - nicht von Hand ändern.
# vorlage-hash: 5e17d9a587688151
# text-hash: 3d5268786da56ab8
# thema: datenstrukturen
# inhalt: Tupel bauen und auspacken

import re

EINGABEN = ["900", "45", "5"]


def ergebnis_von(*argumente):
    """Ruft kosten auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return kosten(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def erwartet(kaufpreis, strom, jahre):
    """Die erwartete Ausgabe, in Cent gerechnet, damit kein Rundungsfehler entsteht."""
    gesamt_cent = round(kaufpreis * 100) + round(strom * 100) * jahre
    return f"Gesamtkosten: {gesamt_cent / 100:.2f} Euro\nPro Jahr: {gesamt_cent / 100 / jahre:.2f} Euro"


def meldung(eingaben, ausgabe):
    """Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    kaufpreis, strom, jahre = eingaben
    soll = erwartet(float(kaufpreis), float(strom), int(jahre))
    return (
        f"Bei Kaufpreis {kaufpreis}, Strom {strom} und {jahre} Jahren erwartet:\n{soll}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}"
    )


def zahlen_in(ausgabe):
    """Die Kommazahlen in der Ausgabe, z. B. [1125.0, 225.0]."""
    return [float(zahl) for zahl in re.findall(r"-?\d+\.\d+", ausgabe)]


def passt_ungefaehr(ausgabe, kaufpreis, strom, jahre):
    """True, wenn die Ausgabe stimmt; beim Runden auf Cent darf die letzte Stelle um 1 abweichen."""
    gesamt = kaufpreis + strom * jahre
    zahlen = zahlen_in(ausgabe)
    return (
        len(zahlen) == 2
        and abs(zahlen[0] - gesamt) <= 0.0100001
        and abs(zahlen[1] - gesamt / jahre) <= 0.0100001
        and vergleichbar("Gesamtkosten") in vergleichbar(ausgabe)
    )


def nah(a, b):
    """True, wenn zwei Zahlen bis auf Rundungsfehler gleich sind."""
    return abs(a - b) < 1e-6


# kosten gibt ein Tupel aus zwei Werten zurück
ergebnis = ergebnis_von(900, 45, 5)
assert type(ergebnis) is tuple and len(ergebnis) == 2, (
    f"kosten(900, 45, 5) ergibt {ergebnis!r}, erwartet war ein Tupel aus zwei Zahlen.\n"
    "Tipp: return (gesamt, ...) gibt beide Werte in runden Klammern zurück."
    + ("\nIhre Funktion gibt nichts zurück; fehlt das return?" if ergebnis is None else "")
)

# Die Werte im Tupel stimmen: erst die Gesamtkosten, dann die Kosten pro Jahr
ergebnis = ergebnis_von(900, 45, 5)
if ergebnis == (225.0, 1125.0):
    hinweis = "\nTipp: Die Reihenfolge ist vertauscht; zuerst kommen die Gesamtkosten."
else:
    hinweis = ""
assert ergebnis == (1125.0, 225.0), f"kosten(900, 45, 5) ergibt {ergebnis!r}, erwartet war (1125.0, 225.0).{hinweis}"

# kosten mit anderen Werten (nicht fest hinschreiben!)
ergebnis = ergebnis_von(1200, 30, 4)
assert type(ergebnis) is tuple and len(ergebnis) == 2 and nah(ergebnis[0], 1320) and nah(ergebnis[1], 330), (
    f"kosten(1200, 30, 4) ergibt {ergebnis!r}, erwartet war (1320.0, 330.0).\n"
    "Tipp: Die Kosten pro Jahr sind gesamt / jahre."
)

# Die Ausgabe im Beispiel
assert vergleichbar(AUSGABE) == vergleichbar(erwartet(900, 45, 5)), meldung(["900", "45", "5"], AUSGABE)

# Ein anderes Angebot (nicht fest hinschreiben!)
eingaben = ["1499.99", "60.5", "3"]
ausgabe = starte(*eingaben)
assert vergleichbar(ausgabe) == vergleichbar(erwartet(1499.99, 60.5, 3)), meldung(eingaben, ausgabe)

# Nur ein Jahr Nutzung: Gesamtkosten und Kosten pro Jahr sind gleich
eingaben = ["700", "80", "1"]
ausgabe = starte(*eingaben)
assert vergleichbar(ausgabe) == vergleichbar(erwartet(700, 80, 1)), meldung(eingaben, ausgabe)

# Ohne Stromkosten und ohne Kaufpreis
for eingaben in [["850", "0", "4"], ["0", "120", "10"], ["0", "0", "7"]]:
    ausgabe = starte(*eingaben)
    soll = erwartet(float(eingaben[0]), float(eingaben[1]), int(eingaben[2]))
    assert vergleichbar(ausgabe) == vergleichbar(soll), meldung(eingaben, ausgabe)

# Das Tupel wird im Programm ausgepackt
assert verwendet("kosten"), "Rufen Sie im Programm die Funktion kosten(...) auf und packen Sie ihr Ergebnis aus."

# 40 zufällige Angebote
zufall = Zufall(1044)
for _ in range(40):
    kaufpreis = zufall.randint(0, 1000000) / 100
    strom = zufall.randint(0, 1000000) / 100
    jahre = zufall.randint(1, 10)
    ergebnis = ergebnis_von(kaufpreis, strom, jahre)
    gesamt = kaufpreis + strom * jahre
    assert type(ergebnis) is tuple and len(ergebnis) == 2 and nah(ergebnis[0], gesamt) and nah(ergebnis[1], gesamt / jahre), (
        f"kosten({kaufpreis}, {strom}, {jahre}) ergibt {ergebnis!r}, erwartet war ({gesamt}, {gesamt / jahre})."
    )
    eingaben = [str(kaufpreis), str(strom), str(jahre)]
    ausgabe = starte(*eingaben)
    # Liegt ein Betrag genau auf einem halben Cent, kann :.2f je nach Rechenweg auf- oder abrunden
    assert passt_ungefaehr(ausgabe, kaufpreis, strom, jahre), meldung(eingaben, ausgabe)

# Obere Grenze: teuerstes Angebot über 10 Jahre
eingaben = ["10000", "10000", "10"]
ausgabe = starte(*eingaben)
assert vergleichbar(ausgabe) == vergleichbar(erwartet(10000, 10000, 10)), meldung(eingaben, ausgabe)
