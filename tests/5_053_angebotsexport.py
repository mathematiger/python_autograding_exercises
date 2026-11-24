# Automatisch erzeugt aus lehrkraft/muster/5_053_angebotsexport.py - nicht von Hand ändern.
# vorlage-hash: 3cc3e9ced7e067ef
# text-hash: 77b2dabcee1dc328
# thema: texte_zahlen
# inhalt: bytes und bytearray

# Alle Bytes, die in cp1252 ein Zeichen sind (0x81, 0x8D, 0x8F, 0x90 und 0x9D sind keins)
CP1252 = [wert for wert in range(256) if wert not in (0x81, 0x8D, 0x8F, 0x90, 0x9D)]
ZEICHEN = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -äöüÄÖÜß€éèçñ°µ"


def wert_von(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


def kurz(wert):
    """Kürzt lange bytes für Meldungen."""
    text = repr(wert)
    return text if len(text) <= 120 else text[:100] + f" … ({len(wert)} Bytes)"


def satz_von_hand(artikel, cent):
    """Vergleichslösung: baut den Datensatz Byte für Byte als Liste von Zahlen."""
    werte = list(artikel.encode("cp1252"))
    while len(werte) < 30:
        werte.append(32)
    for ziffer in str(cent).rjust(9, "0"):
        werte.append(ord(ziffer))
    werte.append(sum(werte) % 256)
    return bytes(werte)


def meldung_satz(artikel, cent, ergebnis, fehler):
    """Baut die Meldung, wenn neue_position nicht den erwarteten Datensatz liefert."""
    aufruf = f"neue_position({artikel!r}, {cent})"
    erwartet = satz_von_hand(artikel, cent)
    if fehler is not None:
        return f"{aufruf} löst {type(fehler).__name__}: {fehler} aus, erwartet war bytearray({erwartet!r})."
    text = f"{aufruf} ergibt {ergebnis!r},\nerwartet war bytearray({erwartet!r})."
    if ergebnis is not None and len(ergebnis) != 40:
        text = text + f"\nIhr Datensatz hat {len(ergebnis)} Bytes statt 40."
    return text


def ein_fehler(funktion, *argumente):
    """Liefert die Ausnahme, die funktion(*argumente) auslöst, oder None."""
    return wert_von(funktion, *argumente)[1]


# umkodieren: das Beispiel aus der Aufgabe
ergebnis, fehler = wert_von(umkodieren, b"Gr\xfc\xdfe 5 \x80")
erwartet = b"Gr\xc3\xbc\xc3\x9fe 5 \xe2\x82\xac"
assert ergebnis == erwartet, (
    f"umkodieren(b'Gr\\xfc\\xdfe 5 \\x80') ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    + (f"\nDie Funktion löst {type(fehler).__name__}: {fehler} aus." if fehler else "")
    + "\nTipp: Erst mit decode(\"cp1252\") zu Text, dann mit encode(\"utf-8\") zu Bytes."
)

# umkodieren: anderer Text (nicht fest hinschreiben!)
text = "Klimagerät Größe XL, 1.299,00 €"
ergebnis, fehler = wert_von(umkodieren, text.encode("cp1252"))
assert ergebnis == text.encode("utf-8"), (
    f"umkodieren({text.encode('cp1252')!r}) ergibt {ergebnis!r}, erwartet war {text.encode('utf-8')!r} ({text!r})."
)

# umkodieren gibt bytes zurück, nicht str
ergebnis, fehler = wert_von(umkodieren, b"Kabel")
assert isinstance(ergebnis, bytes), (
    f"umkodieren(b'Kabel') ergibt {ergebnis!r} vom Typ {type(ergebnis).__name__}, erwartet war b'Kabel' (bytes).\n"
    "Tipp: decode liefert einen str; erst encode(\"utf-8\") macht daraus wieder bytes."
)

# umkodieren: leere Bytes
ergebnis, fehler = wert_von(umkodieren, b"")
assert ergebnis == b"", f"umkodieren(b'') ergibt {ergebnis!r}, erwartet war b''."

# umkodieren: ein Byte, das in cp1252 kein Zeichen ist, wird nicht ersetzt
ergebnis, fehler = wert_von(umkodieren, b"Preis \x81 99")
assert isinstance(fehler, UnicodeDecodeError), (
    f"umkodieren(b'Preis \\x81 99') ergibt {ergebnis!r}"
    + (f" bzw. löst {type(fehler).__name__} aus" if fehler else "")
    + ", erwartet war ein UnicodeDecodeError.\nTipp: Lassen Sie errors weg (\"strict\"), statt \"replace\" oder \"ignore\"."
)

# neue_position: das Beispiel, Länge 40
ergebnis, fehler = wert_von(neue_position, "Kühlgerät", 129900)
assert ergebnis is not None and len(ergebnis) == 40, meldung_satz("Kühlgerät", 129900, ergebnis, fehler)

# neue_position: Artikelname in cp1252, mit Leerzeichen aufgefüllt
assert ergebnis is not None and bytes(ergebnis[:30]) == "Kühlgerät".encode("cp1252").ljust(30), (
    meldung_satz("Kühlgerät", 129900, ergebnis, fehler)
    + "\nTipp: Bytes 0 bis 29 sind der Name in cp1252 (ü ist ein Byte), mit b\" \" aufgefüllt: name.ljust(30)."
)

# neue_position: Preis als neun Ziffern mit führenden Nullen
assert ergebnis is not None and bytes(ergebnis[30:39]) == b"000129900", (
    meldung_satz("Kühlgerät", 129900, ergebnis, fehler) + "\nTipp: f\"{cent:09d}\".encode(\"ascii\")"
)

# neue_position: das Prüfbyte
assert ergebnis is not None and bytes(ergebnis) == satz_von_hand("Kühlgerät", 129900), (
    meldung_satz("Kühlgerät", 129900, ergebnis, fehler)
    + "\nTipp: Byte 39 ist sum(datensatz[:39]) % 256, die Funktion pruefbyte rechnet es aus."
)

# neue_position gibt ein bytearray zurück
assert isinstance(ergebnis, bytearray), (
    f"neue_position('Kühlgerät', 129900) ergibt den Typ {type(ergebnis).__name__}, erwartet war bytearray, "
    "damit setze_preis den Datensatz später verändern kann.\nTipp: bytearray(...) macht aus bytes ein bytearray."
)

# neue_position: andere Werte (nicht fest hinschreiben!)
ergebnis, fehler = wert_von(neue_position, "Split-Klimaanlage 3,5 kW", 7)
assert ergebnis is not None and bytes(ergebnis) == satz_von_hand("Split-Klimaanlage 3,5 kW", 7), meldung_satz(
    "Split-Klimaanlage 3,5 kW", 7, ergebnis, fehler
)

# neue_position: ein Name mit genau 30 Bytes passt
name = "Präzisionsklimagerät 19 Zoll X"
ergebnis, fehler = wert_von(neue_position, name, 999999999)
assert ergebnis is not None and bytes(ergebnis) == satz_von_hand(name, 999999999), (
    meldung_satz(name, 999999999, ergebnis, fehler) + "\nTipp: 30 Bytes sind erlaubt, erst 31 sind zu viel."
)

# neue_position: Preis 0
ergebnis, fehler = wert_von(neue_position, "Muster", 0)
assert ergebnis is not None and bytes(ergebnis) == satz_von_hand("Muster", 0), meldung_satz("Muster", 0, ergebnis, fehler)

# neue_position: ein Name mit 31 Bytes ist zu lang
fehler = ein_fehler(neue_position, "Präzisionsklimagerät 19 Zoll XL", 100)
assert isinstance(fehler, ValueError), (
    "neue_position('Präzisionsklimagerät 19 Zoll XL', 100) (31 Bytes) soll einen ValueError auslösen"
    + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
)

# neue_position: zählt Bytes in cp1252 (ein € ist dort ein Byte, in UTF-8 drei)
name = "€" * 30
ergebnis, fehler = wert_von(neue_position, name, 100)
assert ergebnis is not None and bytes(ergebnis) == satz_von_hand(name, 100), (
    meldung_satz(name, 100, ergebnis, fehler)
    + "\nTipp: Zählen Sie die Bytes von artikel.encode(\"cp1252\"), nicht die von UTF-8."
)

# neue_position: ein Zeichen, das es in cp1252 nicht gibt
fehler = ein_fehler(neue_position, "Lüfter ✓", 100)
assert isinstance(fehler, ValueError), (
    "neue_position('Lüfter ✓', 100) soll einen ValueError auslösen, weil es ✓ in cp1252 nicht gibt"
    + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
    + "\nTipp: encode(\"cp1252\") ohne errors löst dann selbst einen UnicodeEncodeError aus."
)

# lies_position: das Beispiel
ergebnis, fehler = wert_von(lies_position, satz_von_hand("Kühlgerät", 129900))
assert ergebnis == ("Kühlgerät", 129900), (
    f"lies_position({satz_von_hand('Kühlgerät', 129900)!r}) ergibt {ergebnis!r}, erwartet war ('Kühlgerät', 129900)."
    + (f"\nDie Funktion löst {type(fehler).__name__}: {fehler} aus." if fehler else "")
)

# lies_position: andere Werte, auch mit einem bytearray (nicht fest hinschreiben!)
satz = bytearray(satz_von_hand("Kältemittel R32 €-Preis", 4250))
ergebnis, fehler = wert_von(lies_position, satz)
assert ergebnis == ("Kältemittel R32 €-Preis", 4250), (
    f"lies_position(bytearray({bytes(satz)!r})) ergibt {ergebnis!r}, erwartet war ('Kältemittel R32 €-Preis', 4250)."
    + (f"\nDie Funktion löst {type(fehler).__name__}: {fehler} aus." if fehler else "")
    + "\nTipp: Den Namen mit decode(\"cp1252\") lesen und die Leerzeichen am Ende entfernen."
)

# lies_position: der Name ist ein str, der Preis eine Zahl
ergebnis, fehler = wert_von(lies_position, satz_von_hand("Kühlgerät", 129900))
assert ergebnis is not None and isinstance(ergebnis[0], str) and isinstance(ergebnis[1], int), (
    f"lies_position ergibt {ergebnis!r}, erwartet war ein str und ein int: ('Kühlgerät', 129900)."
)

# lies_position: ein Name mit 30 Bytes, ohne Auffüllen
name = "Präzisionsklimagerät 19 Zoll X"
ergebnis, fehler = wert_von(lies_position, satz_von_hand(name, 1))
assert ergebnis == (name, 1), f"lies_position für {name!r} ergibt {ergebnis!r}, erwartet war {(name, 1)!r}."

# lies_position: ein falsches Prüfbyte
satz = bytearray(satz_von_hand("Kühlgerät", 129900))
satz[31] = ord("9")
fehler = ein_fehler(lies_position, satz)
assert isinstance(fehler, ValueError), (
    f"lies_position({bytes(satz)!r}) soll einen ValueError auslösen, weil der Preis verändert wurde und das "
    f"Prüfbyte nicht mehr passt" + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
)

# lies_position: ein falsches Prüfbyte bei richtigen Daten
satz = bytearray(satz_von_hand("Kühlgerät", 129900))
satz[39] = (satz[39] + 1) % 256
fehler = ein_fehler(lies_position, satz)
assert isinstance(fehler, ValueError), (
    f"lies_position({bytes(satz)!r}) soll einen ValueError auslösen, weil Byte 39 nicht die Summe der Bytes 0 bis 38 "
    "modulo 256 ist" + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
)

# lies_position: zu kurzer Datensatz (39 Bytes)
fehler = ein_fehler(lies_position, satz_von_hand("Kühlgerät", 129900)[:39])
assert isinstance(fehler, ValueError), (
    "lies_position mit 39 Bytes soll einen ValueError auslösen"
    + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
    + "\nTipp: Prüfen Sie len(datensatz) zuerst."
)

# lies_position: zu langer Datensatz (41 Bytes)
fehler = ein_fehler(lies_position, satz_von_hand("Kühlgerät", 129900) + b" ")
assert isinstance(fehler, ValueError), (
    "lies_position mit 41 Bytes soll einen ValueError auslösen"
    + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
)

# lies_position: leerer Datensatz
fehler = ein_fehler(lies_position, b"")
assert isinstance(fehler, ValueError), (
    "lies_position(b'') soll einen ValueError auslösen"
    + (f", löst aber {type(fehler).__name__} aus." if fehler else ", löst aber keinen aus.")
)

# lies_position verändert den Datensatz nicht
satz = bytearray(satz_von_hand("Kühlgerät", 129900))
wert_von(lies_position, satz)
assert bytes(satz) == satz_von_hand("Kühlgerät", 129900), (
    f"lies_position hat den übergebenen Datensatz verändert, er ist jetzt {bytes(satz)!r}."
)

# setze_preis: das Beispiel
satz = bytearray(satz_von_hand("Kühlgerät", 129900))
ergebnis, fehler = wert_von(setze_preis, satz, 99900)
assert bytes(satz[30:39]) == b"000099900", (
    f"Nach setze_preis(satz, 99900) ist satz {bytes(satz)!r}, erwartet war {satz_von_hand('Kühlgerät', 99900)!r}."
    + (f"\nDie Funktion löst {type(fehler).__name__}: {fehler} aus." if fehler else "")
    + "\nTipp: Überschreiben Sie den Ausschnitt datensatz[30:39] mit neun Ziffern."
)

# setze_preis: Länge 40 und Artikelname bleiben (neun Ziffern, auch bei kleinem Preis)
satz = bytearray(satz_von_hand("Kühlgerät", 129900))
wert_von(setze_preis, satz, 42)
assert len(satz) == 40 and bytes(satz[:30]) == satz_von_hand("Kühlgerät", 42)[:30], (
    f"Nach setze_preis(satz, 42) hat satz {len(satz)} Bytes: {bytes(satz)!r}, erwartet waren 40: "
    f"{satz_von_hand('Kühlgerät', 42)!r}.\nTipp: Ersetzt man einen Ausschnitt durch kürzere Bytes, wird der bytearray "
    "kürzer. f\"{cent:09d}\" hat immer neun Ziffern."
)

# setze_preis: das Prüfbyte wird neu berechnet
satz = bytearray(satz_von_hand("Kühlgerät", 129900))
wert_von(setze_preis, satz, 42)
assert bytes(satz) == satz_von_hand("Kühlgerät", 42), (
    f"Nach setze_preis(satz, 42) ist satz {bytes(satz)!r}, erwartet war {satz_von_hand('Kühlgerät', 42)!r}.\n"
    "Tipp: Nach dem neuen Preis stimmt das alte Prüfbyte nicht mehr; setzen Sie datensatz[39] neu."
)

# setze_preis verändert den Datensatz selbst und gibt nichts zurück
satz = bytearray(satz_von_hand("Lüfter", 500))
ergebnis, fehler = wert_von(setze_preis, satz, 650)
assert ergebnis is None and bytes(satz) == satz_von_hand("Lüfter", 650), (
    f"setze_preis(satz, 650) gibt {kurz(ergebnis)} zurück, satz ist danach {bytes(satz)!r}; erwartet war: Rückgabe "
    f"None und satz verändert zu {satz_von_hand('Lüfter', 650)!r}.\n"
    "Tipp: Ändern Sie das übergebene bytearray mit datensatz[...] = ..., statt ein neues zurückzugeben."
)

# setze_preis: dasselbe Objekt, nicht nur ein neues mit demselben Namen
satz = bytearray(satz_von_hand("Lüfter", 500))
gleiches = satz
wert_von(setze_preis, satz, 0)
assert gleiches is satz and bytes(gleiches) == satz_von_hand("Lüfter", 0), (
    f"Nach setze_preis(satz, 0) ist satz {bytes(gleiches)!r}, erwartet war {satz_von_hand('Lüfter', 0)!r}."
)

# 300 zufällige Datensätze: neue_position, lies_position und setze_preis
zufall = Zufall(5053)
for _ in range(300):
    artikel = "".join(zufall.choice(ZEICHEN) for _ in range(zufall.randint(1, 30))).strip() or "X"
    cent = zufall.randint(0, 999_999_999)
    ergebnis, fehler = wert_von(neue_position, artikel, cent)
    assert ergebnis is not None and bytes(ergebnis) == satz_von_hand(artikel, cent), meldung_satz(
        artikel, cent, ergebnis, fehler
    )
    gelesen, fehler = wert_von(lies_position, bytes(ergebnis))
    assert gelesen == (artikel, cent), (
        f"lies_position({satz_von_hand(artikel, cent)!r}) ergibt {gelesen!r}, erwartet war {(artikel, cent)!r}."
    )
    neu = zufall.randint(0, 999_999_999)
    wert_von(setze_preis, ergebnis, neu)
    assert bytes(ergebnis) == satz_von_hand(artikel, neu), (
        f"Nach setze_preis(neue_position({artikel!r}, {cent}), {neu}) ist der Datensatz {bytes(ergebnis)!r}, "
        f"erwartet war {satz_von_hand(artikel, neu)!r}."
    )

# 300 zufällige Texte: umkodieren
for _ in range(300):
    daten = bytes(zufall.choice(CP1252) for _ in range(zufall.randint(0, 50)))
    ergebnis, fehler = wert_von(umkodieren, daten)
    assert ergebnis == daten.decode("cp1252").encode("utf-8"), (
        f"umkodieren({daten!r}) ergibt {kurz(ergebnis)}, erwartet war {daten.decode('cp1252').encode('utf-8')!r}."
    )

# Obere Grenze: umkodieren mit 10**6 Bytes
daten = bytes(zufall.choices(CP1252, k=10**6))
ergebnis, fehler = wert_von(umkodieren, daten)
erwartet = daten.decode("cp1252").encode("utf-8")
assert ergebnis == erwartet, (
    f"umkodieren mit 10**6 Bytes ergibt {kurz(ergebnis)}, erwartet waren {len(erwartet)} Bytes beginnend mit "
    f"{erwartet[:20]!r}."
)
