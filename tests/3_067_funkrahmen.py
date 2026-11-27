# Automatisch erzeugt aus lehrkraft/muster/3_067_funkrahmen.py - nicht von Hand ändern.
# vorlage-hash: 61717898c5d262cf
# text-hash: 7058f26dc5104ab5
# thema: algorithmen
# inhalt: Möglichkeiten zählen mit Tabelle

def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except RecursionError:
        return "RecursionError (zu viele verschachtelte Aufrufe)"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def kurz(wert):
    """Kürzt lange Werte für Meldungen."""
    text = repr(wert)
    if len(text) <= 200:
        return text
    if isinstance(wert, list):
        return f"<Liste mit {len(wert)} Einträgen, beginnend mit {wert[:5]!r}>"
    if isinstance(wert, int):
        return f"<Zahl mit {len(str(wert))} Stellen>"
    return text[:200] + " …"


def alle_folgen(n, groessen):
    """Langsame Vergleichslösung: zählt alle Folgen einzeln durch Ausprobieren auf."""
    offen = [0]
    gefunden = 0
    while offen:
        summe = offen.pop()
        if summe == n:
            gefunden = gefunden + 1
            continue
        for groesse in groessen:
            if summe + groesse <= n:
                offen.append(summe + groesse)
    return gefunden


def vergleich_tabelle(n, groessen):
    """Vergleichslösung anders herum: verteilt jede Anzahl nach vorn auf k + g."""
    anzahl = [0] * (n + 1)
    anzahl[0] = 1
    for k in range(n + 1):
        for groesse in set(groessen):
            if k + groesse <= n:
                anzahl[k + groesse] += anzahl[k]
    return anzahl


def tabelle_meldung(n, groessen, erwartet, tipp=""):
    """Prüft rahmen_tabelle(n, groessen); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(rahmen_tabelle, n, list(groessen))
    text = f"rahmen_tabelle({n}, {groessen!r}) ergibt {kurz(ergebnis)}, erwartet war {kurz(erwartet)}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Liste mit return zurück."
    elif isinstance(ergebnis, list) and isinstance(erwartet, list):
        if len(ergebnis) != len(erwartet):
            text = text + f"\nDie Liste soll n + 1 = {len(erwartet)} Einträge haben (für 0 bis n Byte), sie hat {len(ergebnis)}."
        else:
            for k in range(len(erwartet)):
                if ergebnis[k] != erwartet[k]:
                    text = text + f"\nDer erste falsche Eintrag ist anzahl[{k}] = {kurz(ergebnis[k])}, erwartet {kurz(erwartet[k])}."
                    break
    if tipp:
        text = text + "\nTipp: " + tipp
    return ergebnis == erwartet, text


def folgen_meldung(n, groessen, erwartet, tipp=""):
    """Prüft rahmenfolgen(n, groessen); liefert (stimmt, Meldung)."""
    ergebnis = wert_von(rahmenfolgen, n, list(groessen))
    text = f"rahmenfolgen({n}, {groessen!r}) ergibt {kurz(ergebnis)}, erwartet war {kurz(erwartet)}."
    if ergebnis is None:
        text = text + "\nTipp: Geben Sie die Anzahl mit return zurück."
    if tipp:
        text = text + "\nTipp: " + tipp
    return ergebnis == erwartet, text


# rahmen_tabelle: das Beispiel
stimmt, text = tabelle_meldung(7, [2, 3], [1, 0, 1, 1, 1, 2, 2, 3])
assert stimmt, text

# rahmen_tabelle: die Liste hat n + 1 Einträge und beginnt mit 1
ergebnis = wert_von(rahmen_tabelle, 6, [1, 4])
assert isinstance(ergebnis, list) and len(ergebnis) == 7 and ergebnis[0] == 1, (
    f"rahmen_tabelle(6, [1, 4]) ergibt {kurz(ergebnis)}; erwartet war eine Liste mit 7 Einträgen "
    "(für 0 bis 6 Byte), deren erster Eintrag 1 ist.\n"
    "Tipp: anzahl = [0] * (n + 1) und dann anzahl[0] = 1, denn für 0 Byte gibt es genau eine Folge, die leere."
)

# rahmen_tabelle: andere Größen (nicht fest hinschreiben!)
stimmt, text = tabelle_meldung(6, [1, 4], [1, 1, 1, 1, 2, 3, 4])
assert stimmt, text

# rahmen_tabelle: mit 1 und 2 entstehen die Fibonacci-Zahlen
stimmt, text = tabelle_meldung(
    8, [1, 2], [1, 1, 2, 3, 5, 8, 13, 21, 34],
    "anzahl[k] ist die Summe von anzahl[k - g] für jede Größe g, die nicht größer als k ist.",
)
assert stimmt, text

# rahmen_tabelle: die Reihenfolge der Größen ist egal
stimmt, text = tabelle_meldung(7, [3, 2], [1, 0, 1, 1, 1, 2, 2, 3])
assert stimmt, text

# rahmen_tabelle: Größen über n kommen nicht vor
stimmt, text = tabelle_meldung(
    3, [2, 10], [1, 0, 1, 0],
    "Prüfen Sie g <= k, bevor Sie auf anzahl[k - g] zugreifen; ein negativer Index zählt in Python von hinten.",
)
assert stimmt, text

# rahmen_tabelle: n = 0 ergibt [1]
stimmt, text = tabelle_meldung(0, [2, 3], [1])
assert stimmt, text

# rahmenfolgen: das Beispiel
stimmt, text = folgen_meldung(7, [2, 3], 3)
assert stimmt, text

# rahmenfolgen: weitere Werte aus der Aufgabe
stimmt, text = folgen_meldung(4, [1, 2], 5)
assert stimmt, text

# rahmenfolgen: n lässt sich nicht zerlegen
stimmt, text = folgen_meldung(1, [2, 3], 0)
assert stimmt, text

# rahmenfolgen: andere Größen (nicht fest hinschreiben!)
stimmt, text = folgen_meldung(10, [1, 3, 5], 47)
assert stimmt, text

# rahmenfolgen: 0 Byte ergeben eine Folge
stimmt, text = folgen_meldung(0, [5], 1, "Für 0 Byte gibt es genau eine Folge, die leere.")
assert stimmt, text

# rahmenfolgen: eine einzige Größe
stimmt, text = folgen_meldung(12, [4], 1)
assert stimmt, text

# rahmenfolgen: die Größe 1 allein ergibt immer genau eine Folge
stimmt, text = folgen_meldung(9, [1], 1)
assert stimmt, text

# rahmen_tabelle: die Liste groessen bleibt unverändert
groessen = [3, 1, 2]
wert_von(rahmen_tabelle, 5, groessen)
assert groessen == [3, 1, 2], (
    f"rahmen_tabelle hat die übergebene Liste groessen verändert, sie ist jetzt {groessen!r}."
)

# Laufzeit: doppelt so viele Byte brauchen nur etwa doppelt so viele Schritte
_, schritte_12 = zaehle_schritte(rahmenfolgen, 12, [1, 2])
_, schritte_24 = zaehle_schritte(rahmenfolgen, 24, [1, 2])
schritte_12 = max(schritte_12, 1)
assert schritte_24 <= 4 * schritte_12, (
    f"rahmenfolgen braucht für n = 12 {schritte_12} Schritte, für n = 24 {schritte_24}, also "
    f"{schritte_24 / schritte_12:.1f}-mal so viele. Bei O(n · k) wären es etwa 2-mal so viele.\n"
    "Tipp: Rechnet rahmenfolgen jede Folge einzeln oder rekursiv ohne Merker, wächst die Zahl der Schritte "
    "exponentiell. Füllen Sie die Tabelle von unten, jeden Eintrag anzahl[k] genau einmal."
)

# Viele zufällige Eingaben, verglichen mit dem Aufzählen aller Folgen
zufall = Zufall(3067)
for runde in range(300):
    groessen = zufall.sample(range(1, 9), zufall.randint(1, 4))
    n = zufall.randint(0, 16)
    stimmt, text = folgen_meldung(n, groessen, alle_folgen(n, groessen))
    assert stimmt, text

# Viele zufällige Tabellen, verglichen mit einer anders gefüllten Tabelle
for runde in range(100):
    groessen = zufall.sample(range(1, 60), zufall.randint(1, 20))
    n = zufall.randint(0, 200)
    stimmt, text = tabelle_meldung(n, groessen, vergleich_tabelle(n, groessen))
    assert stimmt, text

# Laufzeit: jeder Eintrag der Tabelle wird nur einmal berechnet
_, schritte_klein = zaehle_schritte(rahmenfolgen, 200, [1, 2, 3])
_, schritte_gross = zaehle_schritte(rahmenfolgen, 800, [1, 2, 3])
schritte_klein = max(schritte_klein, 1)
assert schritte_gross <= 6 * schritte_klein, (
    f"rahmenfolgen braucht für n = 200 {schritte_klein} Schritte, für n = 800 {schritte_gross}, also "
    f"{schritte_gross / schritte_klein:.1f}-mal so viele. Bei O(n · k) wären es etwa 4-mal so viele.\n"
    "Tipp: Berechnen Sie jeden Eintrag anzahl[k] einmal aus den schon bekannten kleineren Einträgen."
)

# Obere Grenze: n = 5000 mit der Größe 1 (rekursiv wären das 5000 offene Aufrufe)
groessen = [1, 2, 5]
stimmt, text = folgen_meldung(
    5000, groessen, vergleich_tabelle(5000, groessen)[5000],
    "Rekursion stößt bei n = 5000 an das Rekursionslimit; füllen Sie die Tabelle mit einer Schleife von unten.",
)
assert stimmt, text

# Obere Grenze: 20 Größen bis 1000
groessen = zufall.sample(range(1, 1001), 20)
stimmt, text = folgen_meldung(5000, groessen, vergleich_tabelle(5000, groessen)[5000])
assert stimmt, text
