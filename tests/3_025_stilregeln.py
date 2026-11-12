# Automatisch erzeugt aus lehrkraft/muster/3_025_stilregeln.py - nicht von Hand ändern.
# vorlage-hash: 4e76ca13ea8fd9ba
# text-hash: d3dd7c5dfe1f294f
# thema: funktionen
# inhalt: lambda-Ausdrücke

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

# leerraum_am_ende: Leerzeichen am Ende, aber nicht am Anfang
faelle = [("print(1) ", True), ("print(1)", False), ("  print(1)", False), (" ", True)]
for zeile, erwartet in faelle:
    ergebnis = leerraum_am_ende(zeile)
    assert ergebnis == erwartet, (
        f"leerraum_am_ende({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        'Tipp: Prüfen Sie das letzte Zeichen auf " ", etwa mit endswith.'
    )

# leerraum_am_ende: auch ein Tabulator am Ende
faelle = [("print(1)\t", True), ("x \t", True)]
for zeile, erwartet in faelle:
    ergebnis = leerraum_am_ende(zeile)
    assert ergebnis == erwartet, (
        f"leerraum_am_ende({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        'Tipp: Prüfen Sie das letzte Zeichen auch auf "\\t".'
    )

# leerraum_am_ende: alle Fälle, auch eine leere Zeile
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

# schiefe_einrueckung aus dem Beispiel und weitere Einrückungen
faelle = [("   return 0", True), ("        pass", False), ("x = 1", False), (" a", True), ("      b", True)]
for zeile, erwartet in faelle:
    ergebnis = schiefe_einrueckung(zeile)
    assert ergebnis == erwartet, (
        f"schiefe_einrueckung({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        'Tipp: Die Leerzeichen am Anfang sind len(zeile) - len(zeile.lstrip(" ")); '
        "verstoßen wird, wenn diese Zahl % 4 nicht 0 ist."
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

# zu_lang ist ein lambda-Ausdruck
art = getattr(zu_lang, "__name__", type(zu_lang).__name__)
assert art == "<lambda>", (
    f"zu_lang soll ein lambda-Ausdruck sein, gefunden: {art!r}.\n"
    "Tipp: Schreiben Sie zu_lang = lambda zeile: … statt def zu_lang(zeile): …"
)

# leerraum_am_ende ist ein lambda-Ausdruck
art = getattr(leerraum_am_ende, "__name__", type(leerraum_am_ende).__name__)
assert art == "<lambda>", (
    f"leerraum_am_ende soll ein lambda-Ausdruck sein, gefunden: {art!r}.\n"
    "Tipp: Schreiben Sie leerraum_am_ende = lambda zeile: … statt def leerraum_am_ende(zeile): …"
)

# tabulator ist ein lambda-Ausdruck
art = getattr(tabulator, "__name__", type(tabulator).__name__)
assert art == "<lambda>", (
    f"tabulator soll ein lambda-Ausdruck sein, gefunden: {art!r}.\n"
    "Tipp: Schreiben Sie tabulator = lambda zeile: … statt def tabulator(zeile): …"
)

# schiefe_einrueckung ist ein lambda-Ausdruck
art = getattr(schiefe_einrueckung, "__name__", type(schiefe_einrueckung).__name__)
assert art == "<lambda>", (
    f"schiefe_einrueckung soll ein lambda-Ausdruck sein, gefunden: {art!r}.\n"
    "Tipp: Schreiben Sie schiefe_einrueckung = lambda zeile: … statt def schiefe_einrueckung(zeile): …"
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


ZEICHEN = "abcxyz019_=():#'\" .,"


def zufaellige_zeilen():
    """Liefert 500 zufällige Paare (zeile, grenze), bei jedem Aufruf dieselben."""
    zufall = Zufall(3025)
    paare = []
    for _ in range(500):
        vorne = zufall.choice(["", " ", "  ", "   ", "    ", "\t", "     ", "        ", " \t "])
        mitte = "".join(zufall.choice(ZEICHEN + "\t") for _ in range(zufall.randint(0, 100)))
        hinten = zufall.choice(["", "", " ", "\t", "  "])
        paare.append(((vorne + mitte + hinten)[:200], zufall.randint(0, 200)))
    return paare


# zu_lang bei 500 zufälligen Zeilen
for zeile, grenze in zufaellige_zeilen():
    ergebnis = (zu_lang(zeile), zu_lang(zeile, grenze))
    erwartet = (zu_lang_von_hand(zeile), zu_lang_von_hand(zeile, grenze))
    assert ergebnis == erwartet, (
        f"Für zeile = {zeile!r} ergeben zu_lang(zeile) und zu_lang(zeile, {grenze}) {ergebnis!r}, erwartet war {erwartet!r}."
    )

# leerraum_am_ende bei 500 zufälligen Zeilen
for zeile, grenze in zufaellige_zeilen():
    ergebnis = leerraum_am_ende(zeile)
    erwartet = leerraum_von_hand(zeile)
    assert ergebnis == erwartet, f"leerraum_am_ende({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# tabulator bei 500 zufälligen Zeilen
for zeile, grenze in zufaellige_zeilen():
    ergebnis = tabulator(zeile)
    erwartet = tabulator_von_hand(zeile)
    assert ergebnis == erwartet, f"tabulator({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# schiefe_einrueckung bei 500 zufälligen Zeilen
for zeile, grenze in zufaellige_zeilen():
    ergebnis = schiefe_einrueckung(zeile)
    erwartet = schief_von_hand(zeile)
    assert ergebnis == erwartet, f"schiefe_einrueckung({zeile!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

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
