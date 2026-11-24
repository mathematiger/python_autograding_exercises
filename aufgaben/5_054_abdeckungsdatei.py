"""Aufgabe 5_054 – Abdeckungsdatei                               Stufe 5 ★★★★★

Ein Team entwickelt die Firmware eines Steuergeräts in C. Beim Testen
misst ein Werkzeug die Codeabdeckung (Coverage): wie viele Zeilen jeder
C-Funktion die Tests wirklich ausgeführt haben. Das Werkzeug schreibt
das Ergebnis in eine Binärdatei, deren Aufbau in der
Schnittstellenbeschreibung des Werkzeugs festgelegt ist. Ein neues
Auswertungsskript in Python soll diese Dateien lesen und, wenn ein
Testlauf nachgemeldet wird, einzelne Werte direkt in der Datei
korrigieren können. Laut Schnittstellenbeschreibung gilt, alle Zahlen
vorzeichenlos und in Little-Endian-Byte-Reihenfolge (niedrigstes Byte
zuerst):

- Kopf, 8 Bytes: die Kennung b"COVR" (4 Bytes), die Formatversion
  (2 Bytes) und die Anzahl n der Funktionen (2 Bytes),
- danach n Datensätze zu je 8 Bytes: die Nummer der Funktion
  (4 Bytes), die Zahl ihrer Zeilen (2 Bytes) und die Zahl der
  abgedeckten Zeilen (2 Bytes).

Schreiben Sie mit dem Modul struct und mit memoryview vier Funktionen:

- `lies_kopf(daten)` gibt das Tupel (version, anzahl) zurück. Ist daten
  kürzer als 8 Bytes oder ist die Kennung nicht b"COVR", löst sie einen
  ValueError aus.
- `lies_funktionen(daten)` gibt die Liste der Datensätze als Tupel
  (nummer, zeilen, abgedeckt) in der Reihenfolge der Datei zurück. Ist
  der Kopf ungültig oder ist daten nicht genau 8 + 8 · anzahl Bytes lang,
  löst sie einen ValueError aus.
- `datensatzbereich(daten)` gibt eine memoryview auf die Bytes ab
  Position 8 zurück, ohne sie zu kopieren.
- `setze_abgedeckt(puffer, index, abgedeckt)` bekommt eine gültige Datei
  als bytearray und trägt im Datensatz mit dem Index index (0 ist der
  erste) die neue Zahl abgedeckter Zeilen direkt in puffer ein. Sie gibt
  nichts zurück. Gibt es diesen Datensatz nicht, löst sie einen
  IndexError aus, auch bei negativem index.

    daten = BEISPIEL          (die vorgegebenen 32 Bytes unten)
    lies_kopf(daten)          →  (2, 3)
    lies_funktionen(daten)    →  [(4711, 120, 96), (4712, 35, 35), (5003, 300, 0)]
    bereich = datensatzbereich(daten)
    len(bereich), bereich[0]  →  (24, 103)      (103 = 0x67, das erste Byte von 4711)
    puffer = bytearray(daten)
    setze_abgedeckt(puffer, 2, 180)
    lies_funktionen(puffer)[2]   →  (5003, 300, 180)
    lies_kopf(b"COV")            →  ValueError

Grenzen: daten ist bytes oder ein bytearray mit 0 bis 8 + 8 · 65 535
Bytes; die Version ist 0 bis 65 535, anzahl 0 bis 65 535, die Nummer
einer Funktion 0 bis 2**32 - 1, zeilen und abgedeckt 0 bis 65 535.
puffer in setze_abgedeckt ist eine gültige Datei als bytearray, index
eine ganze Zahl von -100 bis 70 000, abgedeckt 0 bis 65 535.

Hintergrund: In Aufgabe 5_053 haben Sie Felder aus Text (Ziffern und
Buchstaben) in einen Datensatz fester Breite geschrieben. Die meisten
Binärformate speichern Zahlen aber nicht als Ziffern, sondern direkt
als Bytes: Die Zahl 4711 ist hexadezimal 0x1267 und belegt in 4 Bytes
entweder 67 12 00 00 (Little-Endian, niedrigstes Byte zuerst, so
arbeiten x86- und ARM-Prozessoren) oder 00 00 12 67 (Big-Endian, auch
„Netzwerk-Byte-Reihenfolge“, so stehen Zahlen in IP-Paketköpfen). Von
Hand ginge das mit int.from_bytes(daten[8:12], "little"). Für ganze
Datensätze gibt es das Modul struct: Ein Formattext beschreibt, wie die
Bytes aufgeteilt sind.

    import struct

    struct.pack("<IHH", 4711, 120, 96)   # b'g\\x12\\x00\\x00x\\x00`\\x00', 8 Bytes
    struct.unpack("<IHH", b"g\\x12\\x00\\x00x\\x00`\\x00")   # (4711, 120, 96)
    struct.calcsize("<IHH")              # 8

Das erste Zeichen legt die Byte-Reihenfolge fest: "<" Little-Endian,
">" oder "!" Big-Endian. Danach steht je Feld ein Buchstabe, davor
optional eine Anzahl: B ist eine vorzeichenlose Zahl in 1 Byte
(0 bis 255), H in 2 Bytes, I in 4, Q in 8; die Kleinbuchstaben b, h, i,
q sind dieselben Größen mit Vorzeichen. f und d sind Kommazahlen in 4
bzw. 8 Bytes, "4s" sind 4 Bytes, die als bytes herauskommen, und x ist
ein Füllbyte, das übersprungen wird. Liest man mit der falschen
Byte-Reihenfolge, kommt kein Fehler, sondern Unsinn heraus: Die Anzahl
03 00 ist mit "<H" gelesen 3, mit ">H" aber 768. Ohne eines der Zeichen
am Anfang (oder mit "@") nimmt struct die Reihenfolge und die
Ausrichtung des eigenen Rechners; dann schiebt es Füllbytes ein,
calcsize("BI") ist 8 statt 5. Für Dateiformate gibt man die
Reihenfolge darum immer an.

Für Dateien, die aus vielen Teilen bestehen, gibt es Varianten, die
nicht erst einen Ausschnitt verlangen:

    struct.unpack_from("<4sHH", daten, 0)   # liest ab Position 0, Rest egal
    struct.iter_unpack("<IHH", rest)        # Iterator: ein Tupel je 8 Bytes
    struct.pack_into("<H", puffer, 30, 180) # schreibt in ein bytearray ab Position 30

unpack verlangt genau die passende Länge, unpack_from mindestens so
viele Bytes ab der Position, iter_unpack eine Länge, die ein Vielfaches
der Datensatzgröße ist. Passt es nicht, lösen alle drei struct.error
aus. Das ist keine Unterart von ValueError; wer einen ValueError
verspricht, prüft die Länge vorher oder fängt struct.error ab und löst
einen ValueError aus (Aufgabe 3_029).

Ein Ausschnitt daten[8:] kopiert alle Bytes ab Position 8 in ein neues
Objekt. Bei einer Datei von einigen Megabytes, die man nur durchlesen
will, ist das unnötig. memoryview(daten) ist eine Sicht auf denselben
Speicher: Ausschnitte einer memoryview sind wieder Sichten, es wird
nichts kopiert. struct, bytes(...), int.from_bytes und die meisten
anderen Funktionen nehmen eine memoryview genauso wie bytes.

    sicht = memoryview(daten)
    rest = sicht[8:]          # keine Kopie
    rest.obj is daten         # True: das Objekt, auf das die Sicht zeigt
    len(rest), rest[0]        # wie bei bytes: Länge und ein Byte als Zahl
    rest.tobytes()            # erst hier entsteht eine Kopie
    rest.cast("H")            # dieselben Bytes als Folge von 2-Byte-Zahlen

Zeigt die memoryview auf ein bytearray, ist sie beschreibbar, und jede
Änderung über die Sicht steht danach im bytearray, und umgekehrt. Über
bytes ist sie nur lesbar. cast deutet die Bytes in der Reihenfolge des
eigenen Rechners und verlangt, dass die Länge aufgeht; für Datensätze
mit verschiedenen Feldern bleibt struct das richtige Werkzeug.

Tipp: Der Datensatz mit dem Index i beginnt bei Position 8 + 8 · i,
seine abgedeckten Zeilen stehen 6 Bytes weiter.
"""

import struct

# Die Beispieldatei aus der Aufgabe, Byte für Byte in Hexadezimal
BEISPIEL = bytes.fromhex("434f5652 0200 0300  67120000 7800 6000  68120000 2300 2300  8b130000 2c01 0000")
KOPF = "<4sHH"
DATENSATZ = "<IHH"


def lies_kopf(daten):
    """Gibt (version, anzahl) aus dem Kopf zurück; ValueError bei zu kurzen Daten oder falscher Kennung."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lies_funktionen(daten):
    """Gibt die Datensätze als Liste von Tupeln (nummer, zeilen, abgedeckt) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def datensatzbereich(daten):
    """Gibt eine memoryview auf die Bytes ab Position 8 zurück, ohne zu kopieren."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def setze_abgedeckt(puffer, index, abgedeckt):
    """Trägt die Zahl abgedeckter Zeilen im Datensatz index direkt in das bytearray puffer ein."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(lies_kopf(BEISPIEL))
print(lies_funktionen(BEISPIEL))
puffer = bytearray(BEISPIEL)
setze_abgedeckt(puffer, 2, 180)
print(lies_funktionen(puffer)[2])
