"""Aufgabe 5_053 – Angebotsexport                                Stufe 5 ★★★★★

Der Einkauf einer Firma vergleicht die Angebote mehrerer Lieferanten für
neue Kühl- und Klimageräte im Serverraum. Die Angebotspositionen liegen
noch in einem alten Warenwirtschaftssystem, das seine Daten als Bytes in
der Kodierung cp1252 speichert, der alten Windows-Kodierung für
westeuropäische Sprachen. Das neue Auswertungswerkzeug erwartet UTF-8.
Außerdem soll der Einkauf nachverhandelte Preise direkt im alten Format
eintragen können, ohne den ganzen Datensatz neu aufzubauen.

Eine Angebotsposition im Altsystem ist ein Datensatz von genau 40 Bytes:

- Bytes 0 bis 29: der Artikelname in cp1252, rechts mit Leerzeichen
  (b" ") auf 30 Bytes aufgefüllt,
- Bytes 30 bis 38: der Preis in Cent als neun ASCII-Ziffern, vorne mit
  Nullen aufgefüllt (129 900 Cent → b"000129900"),
- Byte 39: das Prüfbyte, die Summe der Bytes 0 bis 38 modulo 256.

Schreiben Sie vier Funktionen:

- `umkodieren(daten)` bekommt bytes in cp1252 und gibt dieselben Zeichen
  als bytes in UTF-8 zurück. Enthält daten ein Byte, das in cp1252 kein
  Zeichen ist (etwa 0x81), soll der UnicodeDecodeError von decode
  durchkommen; nichts darf stillschweigend ersetzt werden.
- `neue_position(artikel, cent)` gibt einen neuen Datensatz als bytearray
  zurück. Braucht der Artikelname in cp1252 mehr als 30 Bytes oder
  enthält er ein Zeichen, das es in cp1252 nicht gibt, löst sie einen
  ValueError aus (ein UnicodeEncodeError ist schon einer).
- `lies_position(datensatz)` bekommt bytes oder ein bytearray und gibt
  das Tupel (artikel, cent) zurück, den Artikelnamen als str ohne die
  Leerzeichen zum Auffüllen. Ist der Datensatz nicht genau 40 Bytes lang
  oder stimmt das Prüfbyte nicht, löst sie einen ValueError aus. Den
  Datensatz verändert sie nicht.
- `setze_preis(datensatz, cent)` bekommt ein bytearray und trägt den
  neuen Preis direkt in diesen Datensatz ein, mit neu berechnetem
  Prüfbyte. Sie gibt nichts zurück; der Artikelname und die Länge von
  40 Bytes bleiben.

    umkodieren(b"Gr\\xfc\\xdfe 5 \\x80")     →  b"Gr\\xc3\\xbc\\xc3\\x9fe 5 \\xe2\\x82\\xac"
                                           (beides ist „Grüße 5 €“)
    satz = neue_position("Kühlgerät", 129900)
    len(satz)                             →  40
    bytes(satz[30:40])                    →  b"000129900\\x16"
    lies_position(satz)                   →  ("Kühlgerät", 129900)
    setze_preis(satz, 99900)
    lies_position(satz)                   →  ("Kühlgerät", 99900)
    neue_position("Lüfter ✓", 100)        →  ValueError (✓ gibt es in cp1252 nicht)

Grenzen: daten in umkodieren hat höchstens 10**6 Bytes und darf leer
sein. artikel ist ein nicht leerer Text mit höchstens 40 Zeichen ohne
Leerzeichen am Anfang oder Ende; cent ist eine ganze Zahl mit
0 ≤ cent ≤ 999 999 999. datensatz in lies_position ist bytes oder ein
bytearray mit 0 bis 100 Bytes; in setze_preis ist es ein gültiger
Datensatz (ein bytearray mit 40 Bytes und richtigem Prüfbyte).

Hintergrund: Ein str ist eine Folge von Zeichen, ein bytes-Objekt eine
Folge von Zahlen von 0 bis 255 (Aufgabe 4_024). Dazwischen steht immer
eine Kodierung: Sie legt fest, welche Bytes für welches Zeichen stehen.
encode macht aus Text Bytes, decode aus Bytes Text (Aufgabe 4_058):

    text = "Grüße 5 €"
    alt = text.encode("cp1252")     # b'Gr\\xfc\\xdfe 5 \\x80'
    neu = text.encode("utf-8")      # b'Gr\\xc3\\xbc\\xc3\\x9fe 5 \\xe2\\x82\\xac'
    len(text), len(alt), len(neu)   # (9, 9, 12)
    alt.decode("cp1252") == text    # True

cp1252 kennt nur 251 Zeichen, jedes ist genau ein Byte; UTF-8 kennt alle
Zeichen von Unicode und braucht dafür ein bis vier Bytes, ü zwei, € drei.
Darum ist die Länge in Bytes nicht die Länge in Zeichen, und dieselben
Bytes bedeuten je nach Kodierung etwas anderes: b"\\xfc".decode("cp1252")
ist "ü", b"\\xfc".decode("utf-8") ein UnicodeDecodeError. Umkodieren heißt
deshalb immer: mit der alten Kodierung dekodieren, mit der neuen
kodieren. Ein Byte direkt „umzurechnen“ geht nicht.

Was bei einem Byte oder Zeichen passiert, das nicht passt, regelt das
Argument errors. Voreingestellt ist "strict": ein UnicodeDecodeError
bzw. UnicodeEncodeError, beide Unterarten von ValueError. "replace"
setzt beim Dekodieren das Ersatzzeichen "\\ufffd" (�) und beim Kodieren
ein "?", "ignore" lässt es weg:

    b"A\\x81B".decode("cp1252", errors="replace")   # 'A\\ufffdB'
    "Lüfter ✓".encode("cp1252", errors="replace")   # b'L\\xfcfter ?'

Für Daten, mit denen weitergerechnet wird, ist "strict" fast immer
richtig: Ein still ersetztes Zeichen fällt erst viel später auf.

Ein einzelnes Byte ist eine Zahl, ein Ausschnitt wieder bytes:

    satz = b"AB000000042"
    satz[0]        # 65 (die Zahl für "A")
    satz[2:]       # b'000000042'
    sum(satz)      # Summe aller Byte-Werte
    b"AB".ljust(5) # b'AB   ', mit Leerzeichen aufgefüllt
    f"{42:09d}".encode("ascii")   # b'000000042'

bytes ist unveränderlich wie str: satz[0] = 66 ist ein TypeError.
bytearray ist dieselbe Folge, nur veränderlich, wie eine Liste von
Zahlen von 0 bis 255. Man erzeugt es aus bytes und kann einzelne Bytes
und ganze Ausschnitte überschreiben:

    puffer = bytearray(b"AB000000042")
    puffer[0] = 0x43                # jetzt b'CB000000042'
    puffer[2:11] = b"000000099"     # gleich lang: Länge bleibt 11
    bytes(puffer)                   # wieder unveränderliche bytes

Vorsicht bei Ausschnitten: Ist die rechte Seite kürzer oder länger, wird
der bytearray kürzer oder länger, wie bei Listen, und alle späteren
Felder rutschen. Bei Datensätzen fester Breite muss das Ersetzte also
genau so lang sein wie der Ausschnitt. Eine Funktion, die ein bytearray
verändert, gibt wie list.sort nichts zurück (Aufgabe 2_019): Der
Aufrufer sieht die Änderung an seinem eigenen Objekt.
"""


def umkodieren(daten):
    """Gibt die cp1252-kodierten Bytes daten als UTF-8-kodierte Bytes zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefbyte(datensatz):
    """Gibt das Prüfbyte zu den Bytes 0 bis 38 von datensatz zurück."""
    return sum(datensatz[:39]) % 256


def neue_position(artikel, cent):
    """Gibt einen neuen Datensatz von 40 Bytes als bytearray zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lies_position(datensatz):
    """Gibt (artikel, cent) aus einem Datensatz zurück; ValueError bei falscher Länge oder falschem Prüfbyte."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def setze_preis(datensatz, cent):
    """Trägt den Preis cent direkt in das bytearray datensatz ein und berechnet das Prüfbyte neu."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(umkodieren(b"Gr\xfc\xdfe 5 \x80"))
satz = neue_position("Kühlgerät", 129900)
print(len(satz), bytes(satz[30:40]))
print(lies_position(satz))
setze_preis(satz, 99900)
print(lies_position(satz))
