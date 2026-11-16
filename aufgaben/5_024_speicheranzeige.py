"""Aufgabe 5_024 – Speicheranzeige                               Stufe 5 ★★★★★

Ein Monitoring-Werkzeug überwacht den Arbeitsspeicher und die
Festplatten mehrerer Server. Die Messwerte kommen als Anzahl Bytes,
etwa 8053063680, und sind so kaum lesbar. In Berichten, Warnmeldungen
und auf dem Dashboard sollen sie in passenden Einheiten erscheinen,
mal mit mehr, mal mit weniger Nachkommastellen, und das direkt in
f-Strings, so wie man es von Zahlen mit :.2f kennt. Die Einheiten
zählen in Schritten von 1024: 1 KiB (Kibibyte) sind 1024 Bytes,
1 MiB sind 1024 KiB, dann GiB und TiB. Vervollständigen Sie die
Klasse `Speicher`:

- `__init__(self, anzahl_bytes)` speichert die Anzahl Bytes im
  Attribut `anzahl_bytes`.
- `__format__(self, format_spec)` versteht eine format_spec aus einer
  optionalen Genauigkeit (ein Punkt und eine Ziffer, z. B. .2) und
  einer optionalen Einheit (B, KiB, MiB, GiB oder TiB), in dieser
  Reihenfolge. Das Ergebnis ist die Zahl in dieser Einheit mit so
  vielen Nachkommastellen, ein Leerzeichen und die Einheit. Ohne
  Genauigkeit gilt eine Nachkommastelle. Ohne Einheit wird die
  größte Einheit genommen, in der die Zahl mindestens 1 ist (unter
  1024 Bytes also B). In der Einheit B steht immer eine ganze Zahl
  ohne Nachkommastellen, auch wenn eine Genauigkeit angegeben ist.
  Jede andere format_spec löst einen ValueError aus.
- `__str__(self)` liefert dasselbe wie format mit leerer format_spec.

Außerdem soll `belegung(name, belegt, gesamt)` mit zwei
Speicher-Objekten eine Zeile wie unten liefern: belegt mit einer
Nachkommastelle in GiB, gesamt ohne Nachkommastellen in GiB.

    ram = Speicher(8053063680)
    f"{ram}"           →  "7.5 GiB"
    f"{ram:.2}"        →  "7.50 GiB"
    f"{ram:.0MiB}"     →  "7680 MiB"
    f"{ram:B}"         →  "8053063680 B"
    f"{Speicher(1536):.3KiB}"   →  "1.500 KiB"
    f"{Speicher(500)}"          →  "500 B"
    f"{ram:MB}"        →  ValueError
    belegung("web01", ram, Speicher(16 * 1024**3))
        →  "web01: 7.5 GiB von 16 GiB belegt"

Grenzen: anzahl_bytes ist eine ganze Zahl von 0 bis 2**60. Die
Genauigkeit ist genau eine Ziffer von 0 bis 9. Groß- und
Kleinschreibung der Einheit zählt (kib ist ungültig). Gerundet wird
wie bei format(zahl, ".2f").

Hintergrund: Ein f-String wie f"{wert:.2f}" ruft im Hintergrund
format(wert, ".2f") auf, und das wiederum
type(wert).__format__(wert, ".2f"). Alles hinter dem Doppelpunkt ist
die format_spec, ein gewöhnlicher Text, den die Klasse des Werts
selbst auslegt. Deshalb versteht float ".2f", int "08b" (Binärzahl
mit 8 Stellen), datetime "%d.%m.%Y" und str ">10" (rechtsbündig auf
10 Zeichen): Jede Klasse hat ihre eigene kleine Formatsprache. Auch
"{:.2f}".format(wert) und format(wert, ".2f") landen bei __format__.

Eine eigene Klasse kann sich so eine Sprache ausdenken, indem sie
`__format__(self, format_spec)` schreibt; die Methode muss einen Text
zurückgeben. Ohne sie erbt die Klasse object.__format__, das nur die
leere format_spec erlaubt (dann kommt str(self) heraus) und sonst
einen TypeError auslöst. Typisch ist, die eigene Sprache zu zerlegen
und für die Zahl an die fertige Formatierung von float weiterzugeben:

    class Temperatur:
        def __init__(self, celsius):
            self.celsius = celsius

        def __format__(self, format_spec):
            if format_spec.endswith("F"):
                zahl = self.celsius * 9 / 5 + 32
                return format(zahl, format_spec[:-1] or ".1f") + " °F"
            return format(self.celsius, format_spec or ".1f") + " °C"

    f"{Temperatur(21.5)}"        →  "21.5 °C"
    f"{Temperatur(21.5):.0fF}"   →  "71 °F"

Zum Zerlegen eignen sich Textmethoden wie startswith, endswith und
Slicing, oder ein regulärer Ausdruck mit re.fullmatch, der auf die
ganze format_spec passen muss. Eine unbekannte format_spec sollte, wie
bei den eingebauten Typen, einen ValueError auslösen, statt
stillschweigend irgendetwas auszugeben. Die Breite und Ausrichtung
ganzer Felder gehört übrigens nicht in diese Sprache: Wer die Zeile
ausrichten will, formatiert das Ergebnis noch einmal als Text,
f"{f'{ram:.1GiB}':>12}".
"""

import re

EINHEITEN = ["B", "KiB", "MiB", "GiB", "TiB"]


class Speicher:
    """Eine Speichermenge in Bytes, die sich in f-Strings mit Einheit formatieren lässt."""

    def __init__(self, anzahl_bytes):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __format__(self, format_spec):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __str__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def belegung(name, belegt, gesamt):
    """Gibt eine Zeile wie "web01: 7.5 GiB von 16 GiB belegt" zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


ram = Speicher(8053063680)
print(f"{ram} | {ram:.2} | {ram:.0MiB} | {ram:B}")
print(belegung("web01", ram, Speicher(16 * 1024**3)))
