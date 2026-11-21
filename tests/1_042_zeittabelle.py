# Automatisch erzeugt aus lehrkraft/muster/1_042_zeittabelle.py - nicht von Hand ändern.
# vorlage-hash: a7472553cc24315e
# text-hash: ec6c6849a96fcac5
# thema: kontrollfluss
# inhalt: Verschachtelte Schleifen

import re

EINGABEN = ["3", "4"]


def tabelle(zeilen, spalten):
    """Die erwartete Tabelle als Text, eine Zeile je Anzahl Vorgänge."""
    text_zeilen = []
    for vorgaenge in range(1, zeilen + 1):
        werte = [str(vorgaenge * minuten) for minuten in range(1, spalten + 1)]
        text_zeilen.append(" ".join(werte))
    return "\n".join(text_zeilen)


def zeilen_als_zahlen(ausgabe):
    """Zerlegt die Ausgabe in Zeilen aus Zahlen; Trennzeichen und Leerzeilen zählen nicht."""
    ergebnis = []
    for zeile in ausgabe.splitlines():
        zahlen = re.findall(r"\d+", zeile)
        if zahlen:
            ergebnis.append(zahlen)
    return ergebnis


def zu_wenige_spalten(zeilen, spalten, ausgabe):
    """Prüft, ob die Zeilen der Ausgabe nur so viele Werte haben, wie es Zeilen gibt (bis zeilen statt bis spalten)."""
    zahlen_zeilen = zeilen_als_zahlen(ausgabe)
    return len(zahlen_zeilen) == zeilen and all(len(werte) == zeilen for werte in zahlen_zeilen)


def meldung(zeilen, spalten, ausgabe):
    """Fehlermeldung mit erwarteter und tatsächlicher Tabelle."""
    return (
        f"Bei {zeilen} Zeilen und {spalten} Spalten erwartet:\n{tabelle(zeilen, spalten)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}"
    )


# Im Beispiel stehen die richtigen Zahlen in der richtigen Reihenfolge
assert vergleichbar(AUSGABE) == vergleichbar(tabelle(3, 4)), (
    meldung(3, 4, AUSGABE)
    + "\nTipp: In jeder Zelle steht vorgaenge mal Ihre innere Schleifenvariable (z. B. minuten); "
    "diese läuft von 1 bis spalten."
)

# Im Beispiel steht jede Zeile der Tabelle in einer eigenen Zeile
assert zeilen_als_zahlen(AUSGABE) == zeilen_als_zahlen(tabelle(3, 4)), (
    meldung(3, 4, AUSGABE)
    + '\nTipp: Mit print(wert, end=" ") bleiben die Werte einer Zeile nebeneinander; '
    "das print() danach beendet die Zeile."
)

# Andere Größe (nicht fest hinschreiben!)
ausgabe = starte("5", "5")
assert zeilen_als_zahlen(ausgabe) == zeilen_als_zahlen(tabelle(5, 5)), meldung(5, 5, ausgabe)

# Mehr Spalten als Zeilen: Zeilen und Spalten nicht vertauschen
ausgabe = starte("2", "6")
if zu_wenige_spalten(2, 6, ausgabe):
    hinweis = "\nTipp: Die innere Schleife läuft über die Spalten, also bis spalten, nicht bis zeilen."
else:
    hinweis = ""
assert zeilen_als_zahlen(ausgabe) == zeilen_als_zahlen(tabelle(2, 6)), meldung(2, 6, ausgabe) + hinweis

# Mehr Zeilen als Spalten
ausgabe = starte("6", "2")
assert zeilen_als_zahlen(ausgabe) == zeilen_als_zahlen(tabelle(6, 2)), meldung(6, 2, ausgabe)

# Kleinste Tabelle: eine Zeile, eine Spalte
ausgabe = starte("1", "1")
assert zeilen_als_zahlen(ausgabe) == [["1"]], meldung(1, 1, ausgabe)

# Eine Zeile mit mehreren Spalten und eine Spalte mit mehreren Zeilen
for zeilen, spalten in [(1, 7), (7, 1)]:
    ausgabe = starte(str(zeilen), str(spalten))
    assert zeilen_als_zahlen(ausgabe) == zeilen_als_zahlen(tabelle(zeilen, spalten)), meldung(zeilen, spalten, ausgabe)

# Die Werte einer Zeile sind durch Leerzeichen getrennt
ausgabe = starte("2", "3")
assert [zeile.rstrip() for zeile in ausgabe.splitlines() if zeile.strip()] == ["1 2 3", "2 4 6"], (
    meldung(2, 3, ausgabe) + '\nTipp: Genau ein Leerzeichen zwischen den Werten: print(wert, end=" ").'
)

# 30 zufällige Größen
zufall = Zufall(1042)
for _ in range(30):
    zeilen = zufall.randint(1, 12)
    spalten = zufall.randint(1, 12)
    ausgabe = starte(str(zeilen), str(spalten))
    assert zeilen_als_zahlen(ausgabe) == zeilen_als_zahlen(tabelle(zeilen, spalten)), meldung(zeilen, spalten, ausgabe)

# Obere Grenze: 12 Zeilen und 12 Spalten
ausgabe = starte("12", "12")
assert zeilen_als_zahlen(ausgabe) == zeilen_als_zahlen(tabelle(12, 12)), meldung(12, 12, ausgabe)
