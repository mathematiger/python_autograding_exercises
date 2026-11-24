# Automatisch erzeugt aus lehrkraft/muster/3_068_integrationsplan.py - nicht von Hand ändern.
# vorlage-hash: 3267829948e8d566
# text-hash: a463eece7c3ddc58
# thema: algorithmen
# inhalt: Wege im Gitter zählen

BEISPIEL = ["....", ".#..", "...#", "...."]
BEISPIEL_TABELLE = [[1, 1, 1, 1], [1, 0, 1, 2], [1, 1, 2, 0], [1, 2, 4, 4]]


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(wert):
    """Kürzt lange Werte für Meldungen."""
    text = repr(wert)
    if len(text) <= 300:
        return text
    return text[:200] + " …"


def als_bild(raster):
    """Zeigt ein Raster Zeile für Zeile, damit man es in der Meldung lesen kann."""
    if len(raster) > 12 or len(raster[0]) > 40:
        return f"<Raster mit {len(raster)} Zeilen und {len(raster[0])} Spalten>"
    return "\n".join("    " + zeile for zeile in raster)


def anzahl_erwartet(raster, erwartet, hinweis=""):
    """Prüft reihenfolgen(raster); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(reihenfolgen, list(raster))
    text = f"reihenfolgen für das Raster\n{als_bild(raster)}\nergibt {kurz(ergebnis)}, erwartet war {erwartet}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Anzahl mit return zurück."
    return ergebnis == erwartet, text + hinweis


def tabelle_erwartet(raster, erwartet, hinweis=""):
    """Prüft tabelle(raster); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(tabelle, list(raster))
    text = f"tabelle für das Raster\n{als_bild(raster)}\nergibt {kurz(ergebnis)},\nerwartet war {erwartet}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Tabelle mit return zurück."
    return ergebnis == erwartet, text + hinweis


def zaehle_durchprobieren(raster, a=0, b=0):
    """Langsame Vergleichslösung: läuft rekursiv jeden Weg einzeln ab."""
    if raster[a][b] == "#":
        return 0
    if a == len(raster) - 1 and b == len(raster[0]) - 1:
        return 1
    anzahl = 0
    if a + 1 < len(raster):
        anzahl = anzahl + zaehle_durchprobieren(raster, a + 1, b)
    if b + 1 < len(raster[0]):
        anzahl = anzahl + zaehle_durchprobieren(raster, a, b + 1)
    return anzahl


def zaehle_spaltenweise(raster):
    """Vergleichslösung anders herum: Spalte für Spalte, mit nur einer Spalte Speicher."""
    zeilen = len(raster)
    spalte = [0] * zeilen
    for b in range(len(raster[0])):
        for a in range(zeilen):
            if raster[a][b] == "#":
                spalte[a] = 0
            elif a == 0 and b == 0:
                spalte[a] = 1
            elif a > 0:
                spalte[a] = spalte[a] + spalte[a - 1]
    return spalte[-1]


def binomial(n, k):
    """Berechnet n über k ohne Bibliothek: so viele Wege hat ein Raster ohne Sperre."""
    ergebnis = 1
    for i in range(1, k + 1):
        ergebnis = ergebnis * (n - k + i) // i
    return ergebnis


def zufallsraster(zufall, zeilen, spalten, anteil):
    """Erzeugt ein Raster, in dem jedes Feld mit Wahrscheinlichkeit anteil gesperrt ist."""
    raster = []
    for _ in range(zeilen):
        zeile = ""
        for _ in range(spalten):
            zeile = zeile + ("#" if zufall.random() < anteil else ".")
        raster.append(zeile)
    return raster


# tabelle: das Beispiel aus der Aufgabe
stimmt, text = tabelle_erwartet(BEISPIEL, BEISPIEL_TABELLE)
assert stimmt, text

# reihenfolgen: das Beispiel aus der Aufgabe
stimmt, text = anzahl_erwartet(BEISPIEL, 4)
assert stimmt, text

# reihenfolgen: das zweite Beispiel, zwei Zeilen ohne Sperre
stimmt, text = anzahl_erwartet(["...", "..."], 3)
assert stimmt, text

# reihenfolgen: ein anderes Raster (nicht fest hinschreiben!)
stimmt, text = anzahl_erwartet(["...", "...", "..."], 6, "\nTipp: Jedes Feld ist die Summe aus dem Feld darüber und dem links daneben.")
assert stimmt, text

# reihenfolgen: Sperre in der Mitte
stimmt, text = anzahl_erwartet(["...", ".#.", "..."], 2, "\nTipp: Ein gesperrtes Feld bekommt 0, damit kein Weg darüber weiterläuft.")
assert stimmt, text

# tabelle: ein Raster mit mehr Spalten als Zeilen
stimmt, text = tabelle_erwartet(["..#..", "....."], [[1, 1, 0, 0, 0], [1, 2, 2, 2, 2]])
assert stimmt, text

# tabelle: hinter einem # in der obersten Zeile kommt man nicht mehr hin
stimmt, text = tabelle_erwartet(
    [".#..", "....", "...."], [[1, 0, 0, 0], [1, 1, 1, 1], [1, 2, 3, 4]],
    "\nTipp: In der obersten Zeile kommt man nur von links an ein Feld. Ist links 0, ist es auch 0, nicht 1.",
)
assert stimmt, text

# tabelle: unter einem # in der linken Spalte kommt man nicht mehr hin
stimmt, text = tabelle_erwartet(
    ["...", "#..", "..."], [[1, 1, 1], [0, 1, 2], [0, 1, 3]],
    "\nTipp: In der linken Spalte kommt man nur von oben an ein Feld. Ist oben 0, ist es auch 0, nicht 1.",
)
assert stimmt, text

# reihenfolgen: nur eine Zeile
stimmt, text = anzahl_erwartet(["......"], 1)
assert stimmt, text

# reihenfolgen: nur eine Spalte
stimmt, text = anzahl_erwartet([".", ".", ".", "."], 1)
assert stimmt, text

# reihenfolgen: eine Zeile mit Sperre
stimmt, text = anzahl_erwartet(["..#.."], 0)
assert stimmt, text

# reihenfolgen: Start gesperrt
stimmt, text = anzahl_erwartet(["#..", "...", "..."], 0, "\nTipp: Der Start bekommt nur dann 1, wenn er frei ist.")
assert stimmt, text

# reihenfolgen: Ziel gesperrt
stimmt, text = anzahl_erwartet(["...", "...", "..#"], 0, "\nTipp: Auch das Ziel bekommt 0, wenn es gesperrt ist.")
assert stimmt, text

# reihenfolgen: ein einziges freies Feld (Start ist Ziel)
stimmt, text = anzahl_erwartet(["."], 1, "\nTipp: Ist der Start schon das Ziel, gibt es genau einen Weg: den leeren.")
assert stimmt, text

# reihenfolgen: ein einziges gesperrtes Feld
stimmt, text = anzahl_erwartet(["#"], 0)
assert stimmt, text

# reihenfolgen: eine Mauer quer durchs Raster, kein Weg kommt durch
stimmt, text = anzahl_erwartet(["...#", "..#.", ".#..", "#..."], 0)
assert stimmt, text

# reihenfolgen: nur ein Umweg bleibt frei
stimmt, text = anzahl_erwartet([".###", ".#..", "...#", "##.."], 1)
assert stimmt, text

# tabelle: jede Zeile ist eine eigene Liste
ergebnis = wert_von(tabelle, ["...", "...", "..."])
getrennt = isinstance(ergebnis, list) and len(ergebnis) == 3 and ergebnis[0] is not ergebnis[1] and ergebnis[1] is not ergebnis[2]
assert getrennt, (
    f'tabelle(["...", "...", "..."]) ergibt {kurz(ergebnis)}: Die Zeilen sind dieselbe Liste.\n'
    "Tipp: [[0] * spalten] * zeilen enthält dieselbe Zeile mehrmals. Legen Sie jede Zeile neu an: "
    "[[0] * spalten for _ in range(zeilen)]."
)

# 300 zufällige kleine Raster, verglichen mit dem Ablaufen jedes einzelnen Wegs
zufall = Zufall(3068)
for _ in range(300):
    raster = zufallsraster(zufall, zufall.randint(1, 6), zufall.randint(1, 6), zufall.choice([0, 0.15, 0.3, 0.5]))
    stimmt, text = anzahl_erwartet(raster, zaehle_durchprobieren(raster))
    assert stimmt, text

# Laufzeit: viermal so viele Felder brauchen nur etwa viermal so viele Schritte
proben = []
for groesse in [20, 40]:
    raster = ["." * groesse] * groesse
    ergebnis, schritte = zaehle_schritte(reihenfolgen, raster)
    proben.append((ergebnis == binomial(2 * groesse - 2, groesse - 1), max(schritte, 1)))
schritte_klein = proben[0][1]
schritte_gross = proben[1][1]
assert proben[0][0] and proben[1][0] and schritte_gross <= 6 * schritte_klein, (
    f"reihenfolgen braucht für 20 × 20 Felder {schritte_klein} Schritte, für 40 × 40 {schritte_gross}, also "
    f"{schritte_gross / schritte_klein:.1f}-mal so viele (oder das Ergebnis stimmt nicht). Bei O(Zeilen · Spalten) "
    "wären es etwa 4-mal so viele.\n"
    "Tipp: Berechnen Sie jedes Feld genau einmal aus den Feldern darüber und links daneben, statt Wege abzulaufen."
)

# Obere Grenze: 300 × 300 Felder ohne Sperre
stimmt, text = anzahl_erwartet(["." * 300] * 300, binomial(598, 299))
assert stimmt, text

# Obere Grenze: 300 × 300 Felder mit zufälligen Sperren
raster = zufallsraster(zufall, 300, 300, 0.05)
raster[0] = "." + raster[0][1:]
raster[-1] = raster[-1][:-1] + "."
stimmt, text = anzahl_erwartet(raster, zaehle_spaltenweise(raster))
assert stimmt, text
