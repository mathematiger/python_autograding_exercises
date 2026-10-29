# Automatisch erzeugt aus lehrkraft/muster/2_016_codemetrik.py - nicht von Hand ändern.
# vorlage-hash: ed7acffb2aa2effa
# text-hash: af6babd4151d4f5c
# thema: texte_zahlen
# inhalt: Tabellen mit f-String-Breiten

# Das Beispiel aus der Aufgabe
ergebnis = zeile("login", 120, 8)
assert ergebnis == "login               120    8    15.0", (
    f'zeile("login", 120, 8) ergibt\n{ergebnis!r}, erwartet war\n{"login               120    8    15.0"!r}.'
)

# Weitere Module (nicht fest hinschreiben!)
for modul, zeilen_test, funktionen_test, erwartet in [
    ("datenbank", 2310, 41, "datenbank          2310   41    56.3"),
    ("hilfsfunktionen", 7, 3, "hilfsfunktionen       7    3     2.3"),
    ("api_v2", 480, 12, "api_v2              480   12    40.0"),
]:
    ergebnis = zeile(modul, zeilen_test, funktionen_test)
    if len(ergebnis) != 36:
        hinweis = f"\nTipp: Jede Zeile ist 16 + 7 + 5 + 8 = 36 Zeichen lang, Ihre hat {len(ergebnis)}."
    else:
        hinweis = ""
    assert ergebnis == erwartet, (
        f"zeile({modul!r}, {zeilen_test}, {funktionen_test}) ergibt\n{ergebnis!r}, erwartet war\n{erwartet!r}.{hinweis}"
    )

# Ohne Funktionen steht ein Strich da
for modul, zeilen_test, erwartet in [
    ("konfiguration", 95, "konfiguration        95    0       -"),
    ("leer", 0, "leer                  0    0       -"),
]:
    try:
        ergebnis = zeile(modul, zeilen_test, 0)
    except ZeroDivisionError as fehler:
        ergebnis = fehler
    assert ergebnis == erwartet, (
        f"zeile({modul!r}, {zeilen_test}, 0) ergibt\n{ergebnis!r}, erwartet war\n{erwartet!r}.\n"
        'Tipp: Ohne Funktionen kann man nicht teilen; dann kommt rechtsbündig ein "-" in die letzte Spalte.'
    )

# Die Zahlen stehen rechtsbündig, der Name linksbündig
ergebnis = zeile("x", 5, 2)
erwartet = "x                     5    2     2.5"
assert ergebnis == erwartet, (
    f'zeile("x", 5, 2) ergibt\n{ergebnis!r}, erwartet war\n{erwartet!r}.\n'
    "Tipp: {modul:<16} richtet links aus, {zeilen:>7} rechts."
)

# Zeilen pro Funktion mit genau einer Nachkommastelle
for zeilen_test, funktionen_test, erwartet_ende in [(10, 3, "     3.3"), (20, 3, "     6.7"), (0, 5, "     0.0")]:
    ergebnis = zeile("modul", zeilen_test, funktionen_test)
    assert ergebnis.endswith(erwartet_ende) and len(ergebnis) == 36, (
        f'zeile("modul", {zeilen_test}, {funktionen_test}) ergibt\n{ergebnis!r}, erwartet war eine Zeile, die auf '
        f"{erwartet_ende!r} endet.\nTipp: {{wert:>8.1f}} schreibt die Zahl mit einer Nachkommastelle in eine Spalte der Breite 8."
    )

# Ränder: Modulname mit 16 Zeichen und die größten Zahlen
for modul, zeilen_test, funktionen_test, erwartet in [
    ("abcdefghijklmnop", 99999, 999, "abcdefghijklmnop  99999  999   100.1"),
    ("abcdefghijklmnop", 99999, 1, "abcdefghijklmnop  99999    1 99999.0"),
    ("a", 0, 999, "a                     0  999     0.0"),
    ("a", 99999, 0, "a                 99999    0       -"),
]:
    ergebnis = zeile(modul, zeilen_test, funktionen_test)
    assert ergebnis == erwartet, (
        f"zeile({modul!r}, {zeilen_test}, {funktionen_test}) ergibt\n{ergebnis!r}, erwartet war\n{erwartet!r}."
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Modul            Zeilen Fkt.  Z/Fkt.\n"
    "login               120    8    15.0\n"
    "datenbank          2310   41    56.3\n"
    "konfiguration        95    0       -"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"


# Vergleichslösung: Leerzeichen von Hand zählen statt mit Breiten im f-String
def zeile_von_hand(modul, zeilen, funktionen):
    """Baut die Tabellenzeile, indem sie jede Spalte mit Leerzeichen auf ihre Breite auffüllt."""
    if funktionen == 0:
        schnitt = "-"
    else:
        schnitt = f"{zeilen / funktionen:.1f}"
    teile = [
        modul + " " * (16 - len(modul)),
        " " * (7 - len(str(zeilen))) + str(zeilen),
        " " * (5 - len(str(funktionen))) + str(funktionen),
        " " * (8 - len(schnitt)) + schnitt,
    ]
    return "".join(teile)


# 500 zufällige Module
zufall = Zufall(2015)
zeichen = "abcdefghijklmnopqrstuvwxyz_0123456789"
for _ in range(500):
    laenge = zufall.randint(1, 16)
    modul = ""
    for _ in range(laenge):
        modul = modul + zufall.choice(zeichen)
    zeilen_test = zufall.choice([zufall.randint(0, 99999), zufall.randint(0, 200)])
    funktionen_test = zufall.choice([0, zufall.randint(1, 9), zufall.randint(0, 999)])
    erwartet = zeile_von_hand(modul, zeilen_test, funktionen_test)
    ergebnis = zeile(modul, zeilen_test, funktionen_test)
    assert ergebnis == erwartet, (
        f"zeile({modul!r}, {zeilen_test}, {funktionen_test}) ergibt\n{ergebnis!r}, erwartet war\n{erwartet!r}."
    )
