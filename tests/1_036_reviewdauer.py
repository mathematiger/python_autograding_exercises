# Automatisch erzeugt aus lehrkraft/muster/1_036_reviewdauer.py - nicht von Hand ändern.
# vorlage-hash: e652a50a743ce1eb
# text-hash: 808112ed072fc514
# thema: funktionen
# inhalt: Funktion mehrfach aufrufen

import ast

EINGABEN = ["120", "40"]


def minuten(zeilen):
    """Rechnet die Faustregel im Test nach, ohne die Funktion des Programms zu benutzen."""
    return 10 + (zeilen // 20) * 3 + (zeilen % 20) * 3 // 20


def erwartete_ausgabe(a, b):
    """Baut die erwartete Ausgabe für die Zeilenzahlen a und b."""
    return (
        f"Datei A: {minuten(a)} Minuten\nDatei B: {minuten(b)} Minuten\n"
        f"Beides in einem Review: {minuten(a + b)} Minuten"
    )


def hinweis_zu(ausgabe, a, b):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if minuten(a) + minuten(b) != minuten(a + b) and f"Review: {minuten(a) + minuten(b)} Minuten" in ausgabe:
        return (
            "\nTipp: Für das gemeinsame Review rufen Sie reviewminuten(gesamt) auf. dauer_a + dauer_b "
            "zählt die 10 Minuten Einarbeitung doppelt."
        )
    return ""


def meldung(a, b, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei den Eingaben {a} und {b} erwartet:\n{erwartete_ausgabe(a, b)}\nIhr Programm gibt aus:\n{ausgabe}"
        f"{hinweis_zu(ausgabe, a, b)}"
    )


# Im Beispiel: Datei A dauert 28 Minuten
assert vergleichbar("Datei A: 28 Minuten") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 120 und 40 erwartet die Zeile "Datei A: 28 Minuten" – Ihr Programm gibt aus:\n{AUSGABE}\n'
    "Tipp: dauer_a = reviewminuten(datei_a)"
)

# Im Beispiel: Datei B dauert 16 Minuten
assert vergleichbar("Datei B: 16 Minuten") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 120 und 40 erwartet die Zeile "Datei B: 16 Minuten" – Ihr Programm gibt aus:\n{AUSGABE}\n'
    "Tipp: Rufen Sie reviewminuten ein zweites Mal auf, diesmal mit datei_b."
)

# Im Beispiel: das gemeinsame Review dauert 34 Minuten
assert vergleichbar("Beides in einem Review: 34 Minuten") in vergleichbar(AUSGABE), (
    f'Bei den Eingaben 120 und 40 erwartet die Zeile "Beides in einem Review: 34 Minuten" – Ihr Programm gibt aus:\n'
    f"{AUSGABE}{hinweis_zu(AUSGABE, 120, 40)}"
)

# Das ganze Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(120, 40)), meldung(120, 40, AUSGABE)

# Andere Zeilenzahlen (nicht fest hinschreiben!)
ausgabe = starte("300", "75")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(300, 75)), meldung(300, 75, ausgabe)

# Die Dateien vertauscht
ausgabe = starte("40", "120")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(40, 120)), (
    meldung(40, 120, ausgabe) + "\nTipp: dauer_a gehört zu datei_a, dauer_b zu datei_b."
)

# Keine geänderten Zeilen: nur die Einarbeitung
ausgabe = starte("0", "0")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(0, 0)), meldung(0, 0, ausgabe)

# Knapp unter und genau bei 20 Zeilen
ausgabe = starte("19", "20")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(19, 20)), meldung(19, 20, ausgabe)

# Die Funktion reviewminuten wird aufgerufen
assert verwendet("reviewminuten"), (
    "Rufen Sie die vorgegebene Funktion reviewminuten(...) auf, statt die Formel neu hinzuschreiben."
)


def aufrufe_von_reviewminuten():
    """Zählt, wie oft im Programm reviewminuten(...) aufgerufen wird."""
    with open(__file__, encoding="utf-8-sig") as datei:
        baum = ast.parse(datei.read())
    anzahl = 0
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call) and isinstance(knoten.func, ast.Name) and knoten.func.id == "reviewminuten":
            anzahl = anzahl + 1
    return anzahl


# Alle drei Dauern kommen aus reviewminuten
anzahl_aufrufe = aufrufe_von_reviewminuten()
assert anzahl_aufrufe >= 3, (
    f"Ihr Programm ruft reviewminuten {anzahl_aufrufe}-mal auf, erwartet waren drei Aufrufe "
    "(für dauer_a, dauer_b und dauer_gesamt).\n"
    "Tipp: Schreiben Sie die Formel nicht ab, sondern rufen Sie jedes Mal die Funktion auf."
)

# 40 zufällige Zeilenzahlen
zufall = Zufall(1036)
for _ in range(40):
    a = zufall.randint(0, 5000)
    b = zufall.choice([zufall.randint(0, 5000), zufall.randint(0, 40)])
    ausgabe = starte(str(a), str(b))
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(a, b)), meldung(a, b, ausgabe)

# Obere Grenze: zweimal 5000 Zeilen
ausgabe = starte("5000", "5000")
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(5000, 5000)), meldung(5000, 5000, ausgabe)
