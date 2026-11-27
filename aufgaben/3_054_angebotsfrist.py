"""Aufgabe 3_054 – Angebotsfrist                                 Stufe 3 ★★★☆☆

Für neue Notebooks holt die IT-Abteilung Angebote bei mehreren Händlern
ein. Jedes Angebot gilt nur bis zu einem bestimmten Tag, danach darf der
Händler den Preis ändern. Die Kolleginnen und Kollegen tragen die
Angebote von Hand in eine Liste ein, als Paare (händler, gültig_bis),
das Datum als Text in der Form TT.MM.JJJJ. Beim Eintippen passieren
Fehler: vertauschte Zahlen, ein fehlender Punkt, der 31. April.

Schreiben Sie zwei Funktionen:

- `zerlege_datum(text)` gibt das Tupel (tag, monat, jahr) aus drei
  ganzen Zahlen zurück, wenn text ein gültiges Datum in der Form
  TT.MM.JJJJ ist, sonst None. Leerzeichen am Anfang und am Ende sind
  erlaubt. Gültig heißt: genau zwei Ziffern, ein Punkt, zwei Ziffern,
  ein Punkt, vier Ziffern; das Jahr liegt zwischen 1900 und 2099, der
  Monat zwischen 1 und 12, und den Tag gibt es in diesem Monat.
- `noch_gueltig(angebote, heute)` gibt die Händler der Angebote zurück,
  deren Datum gültig ist und nicht vor heute liegt, in der Reihenfolge
  der Liste. Angebote mit ungültigem Datum fallen weg.

    zerlege_datum("27.11.2026")      →  (27, 11, 2026)
    zerlege_datum(" 01.02.2027 ")    →  (1, 2, 2027)
    zerlege_datum("31.04.2026")      →  None      (der April hat 30 Tage)
    zerlege_datum("1.12.2026")       →  None      (Tag nur einstellig)
    zerlege_datum("2026-11-27")      →  None

    angebote = [("Nordtech", "30.11.2026"), ("Bürowelt", "20.11.2026"),
                ("Kabelkönig", "31.11.2026"), ("Datafix", "23.11.2026")]
    noch_gueltig(angebote, "23.11.2026")  →  ["Nordtech", "Datafix"]

Die Funktion tage_im_monat aus Aufgabe 2_051 ist vorgegeben. Benutzen
Sie nicht das Modul datetime.

Grenzen: text hat 0 bis 30 Zeichen aus dem ASCII-Zeichensatz (Ziffern,
Buchstaben, Satzzeichen, Leerzeichen). angebote hat 0 bis 10 000 Paare,
heute ist ein gültiges Datum in der Form TT.MM.JJJJ.

Hintergrund: Ein Text, der von Menschen kommt, wird in zwei Schritten
gelesen. Erst prüft man die Form: Ist er genau so aufgebaut wie
verlangt? text.strip() entfernt Leerzeichen am Rand (Aufgabe 1_013),
len(text) zählt die Zeichen, text[2] ist das dritte Zeichen (Aufgabe 1_011),
und text.split(".") zerlegt an den Punkten (Aufgabe 2_015) in eine Liste von
Teilen. Ob ein Teil nur aus Ziffern besteht, sagt teil.isdigit() (Aufgabe
3_016). Das ist nötig, denn int() ist großzügig: int(" 5"), int("+5") und
int("-5") klappen alle, obwohl " 5" keine zwei Ziffern sind. Erst wenn die
Form stimmt, wandelt man mit int() um und prüft im zweiten Schritt den
Inhalt: Gibt es diesen Monat, gibt es diesen Tag?

    teile = "07.03.2026".split(".")    →  ["07", "03", "2026"]
    teile[0].isdigit()                 →  True
    int(teile[0])                      →  7

Zwei Daten vergleicht man am einfachsten als Tupel in der Reihenfolge
(jahr, monat, tag): Python vergleicht Tupel Element für Element, wie
bei den Sortierschlüsseln in Aufgabe 3_027. (2026, 11, 30) >=
(2026, 11, 23) ist also True, (2026, 10, 31) >= (2026, 11, 1) False.

Tipp: Geben Sie bei jedem Formfehler sofort None zurück (frühes
return), dann bleibt die Funktion übersichtlich.
"""


def ist_schaltjahr(jahr):
    """Gibt True zurück, wenn jahr ein Schaltjahr ist."""
    return (jahr % 4 == 0 and jahr % 100 != 0) or jahr % 400 == 0


def tage_im_monat(jahr, monat):
    """Gibt die Zahl der Tage des Monats zurück (Monat 1 bis 12)."""
    if monat == 2:
        if ist_schaltjahr(jahr):
            return 29
        return 28
    if monat in [4, 6, 9, 11]:
        return 30
    return 31


def zerlege_datum(text):
    """Gibt (tag, monat, jahr) für ein gültiges Datum TT.MM.JJJJ zurück, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def noch_gueltig(angebote, heute):
    """Gibt die Händler zurück, deren Datum gültig ist und nicht vor heute liegt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


angebote = [
    ("Nordtech", "30.11.2026"),
    ("Bürowelt", "20.11.2026"),
    ("Kabelkönig", "31.11.2026"),
    ("Datafix", "23.11.2026"),
]
print(zerlege_datum("27.11.2026"))
print(noch_gueltig(angebote, "23.11.2026"))
