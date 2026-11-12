# Automatisch erzeugt aus lehrkraft/muster/3_025_stilregeln.py - nicht von Hand ändern.
# vorlage-hash: 4e76ca13ea8fd9ba
# text-hash: d3dd7c5dfe1f294f
# thema: funktionen
# inhalt: lambda-Ausdrücke

# Alle vier Regeln sind lambda-Ausdrücke
for name in ["zu_lang", "leerraum_am_ende", "tabulator", "schiefe_einrueckung"]:
    regel = globals().get(name)
    art = getattr(regel, "__name__", type(regel).__name__)
    assert art == "<lambda>", (
        f"{name} soll ein lambda-Ausdruck sein, gefunden: {art!r}.\n"
        f"Tipp: Schreiben Sie {name} = lambda zeile: … statt def {name}(zeile): …"
    )

# zu_lang aus dem Beispiel: Standardgrenze 79 und eigene Grenze
ergebnis = (zu_lang("x" * 80), zu_lang("x" * 80, 100))
assert ergebnis == (True, False), (
    f'zu_lang("x" * 80) und zu_lang("x" * 80, 100) ergeben {ergebnis!r}, erwartet war (True, False).\n'
    "Tipp: Geben Sie dem Parameter grenze den Standardwert 79: lambda zeile, grenze=79: …"
)

# zu_lang: genau 79 Zeichen sind erlaubt, genau grenze Zeichen auch
ergebnis = (zu_lang("y" * 79), zu_lang("abc", 3), zu_lang("abcd", 3))
assert ergebnis == (False, False, True), (
    f'zu_lang("y" * 79), zu_lang("abc", 3) und zu_lang("abcd", 3) ergeben {ergebnis!r}, erwartet war '
    "(False, False, True).\nTipp: Verboten sind nur mehr als grenze Zeichen, also len(zeile) > grenze."
)

# zu_lang: leere Zeile und Grenze 0
ergebnis = (zu_lang(""), zu_lang("", 0), zu_lang("a", 0))
assert ergebnis == (False, False, True), (
    f'zu_lang(""), zu_lang("", 0) und zu_lang("a", 0) ergeben {ergebnis!r}, erwartet war (False, False, True).'
)

# leerraum_am_ende: Leerzeichen und Tabulator am Ende, aber nicht am Anfang
faelle = [("print(1) ", True), ("print(1)\t", True), ("print(1)", False), ("  print(1)", False), ("", False),
          (" ", True), ("x \t", True)]
for zeile, erwartet in faelle:
    ergebnis = leerraum_am_ende(zeile)
    assert ergebnis == erwartet, (
        f"leerraum_am_ende({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        'Tipp: Prüfen Sie das letzte Zeichen auf " " und auf "\\t", etwa mit endswith; '
        "eine leere Zeile verstößt nicht."
    )

# tabulator: irgendwo in der Zeile
faelle = [("\tprint(1)", True), ("a = 1\t# Kommentar", True), ("a = 1", False), ("", False), ("\\t", False)]
for zeile, erwartet in faelle:
    ergebnis = tabulator(zeile)
    assert ergebnis == erwartet, (
        f"tabulator({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        'Tipp: Der Tabulator ist das eine Zeichen "\\t"; fragen Sie mit in danach.'
    )

# schiefe_einrueckung: Leerzeichen am Anfang zählen, nicht die in der Zeile
faelle = [("   return 0", True), ("        pass", False), ("x = 1", False), ("", False), (" a", True),
          ("    a  =  1", False), ("      b", True), ("\t  c", False), ("     ", True), ("    ", False)]
for zeile, erwartet in faelle:
    ergebnis = schiefe_einrueckung(zeile)
    assert ergebnis == erwartet, (
        f"schiefe_einrueckung({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        'Tipp: Die Leerzeichen am Anfang sind len(zeile) - len(zeile.lstrip(" ")); '
        "verstoßen wird, wenn diese Zahl % 4 nicht 0 ist."
    )

# befunde aus dem Beispiel
ergebnis = befunde(["def f():", "   return 1 "])
assert ergebnis == [(2, "Leerraum am Ende"), (2, "schiefe Einrückung")], (
    f'befunde(["def f():", "   return 1 "]) ergibt {ergebnis!r}, '
    'erwartet war [(2, "Leerraum am Ende"), (2, "schiefe Einrückung")].'
)


# Vergleichslösungen: Zeichen für Zeichen mit Schleifen
def zu_lang_von_hand(zeile, grenze=79):
    """Zählt die Zeichen einzeln."""
    anzahl = 0
    for _ in zeile:
        anzahl += 1
    return anzahl > grenze


def leerraum_von_hand(zeile):
    """Sieht nur das letzte Zeichen an."""
    return zeile != "" and zeile[-1] in " \t"


def tabulator_von_hand(zeile):
    """Sucht den Tabulator Zeichen für Zeichen."""
    for zeichen in zeile:
        if zeichen == "\t":
            return True
    return False


def schief_von_hand(zeile):
    """Zählt die Leerzeichen am Anfang in einer Schleife."""
    leer = 0
    while leer < len(zeile) and zeile[leer] == " ":
        leer += 1
    return leer % 4 != 0


# 500 zufällige Zeilen
zufall = Zufall(3025)
ZEICHEN = "abcxyz019_=():#'\" .,"
for _ in range(500):
    vorne = zufall.choice(["", " ", "  ", "   ", "    ", "\t", "     ", "        ", " \t "])
    mitte = "".join(zufall.choice(ZEICHEN + "\t") for _ in range(zufall.randint(0, 100)))
    hinten = zufall.choice(["", "", " ", "\t", "  "])
    zeile = (vorne + mitte + hinten)[:200]
    grenze = zufall.randint(0, 200)
    ergebnis = (zu_lang(zeile), zu_lang(zeile, grenze), leerraum_am_ende(zeile), tabulator(zeile),
                schiefe_einrueckung(zeile))
    erwartet = (zu_lang_von_hand(zeile), zu_lang_von_hand(zeile, grenze), leerraum_von_hand(zeile),
                tabulator_von_hand(zeile), schief_von_hand(zeile))
    assert ergebnis == erwartet, (
        f"Für zeile = {zeile!r} ergeben zu_lang(zeile), zu_lang(zeile, {grenze}), leerraum_am_ende, tabulator "
        f"und schiefe_einrueckung {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: Zeilen mit 200 Zeichen
lang = " " * 199 + "x"
ergebnis = (zu_lang(lang), zu_lang(lang, 200), leerraum_am_ende(lang), tabulator(lang), schiefe_einrueckung(lang))
assert ergebnis == (True, False, False, False, True), (
    f'Für " " * 199 + "x" ergeben zu_lang, zu_lang(…, 200), leerraum_am_ende, tabulator und schiefe_einrueckung '
    f"{ergebnis!r}, erwartet war (True, False, False, False, True)."
)

# befunde auf 10 000 Zeilen
zeilen = []
for nummer in range(10000):
    zeilen.append(" " * (nummer % 9) + "wert = 1" + "\t" * (nummer % 13 == 0) + "#" * (nummer % 101))
erwartet = []
for nummer, zeile in enumerate(zeilen, start=1):
    for name, regel in [("zu lang", zu_lang_von_hand), ("Leerraum am Ende", leerraum_von_hand),
                        ("Tabulator", tabulator_von_hand), ("schiefe Einrückung", schief_von_hand)]:
        if regel(zeile):
            erwartet.append((nummer, name))
ergebnis = befunde(zeilen)
assert ergebnis == erwartet, (
    f"befunde auf 10 000 Zeilen liefert {len(ergebnis)} Befunde, erwartet waren {len(erwartet)}; "
    f"die ersten erwarteten: {erwartet[:4]}, Ihre ersten: {ergebnis[:4]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[(2, 'Leerraum am Ende'), (2, 'schiefe Einrückung')]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
