# Automatisch erzeugt aus lehrkraft/muster/5_054_abdeckungsdatei.py - nicht von Hand ändern.
# vorlage-hash: a11400424415e12a
# text-hash: 7953d1faa96a9d77
# thema: texte_zahlen
# inhalt: struct und memoryview

def wert_von(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


def zahl(wert, breite):
    """Vergleichslösung: eine Zahl als Little-Endian-Bytes, mit Divisionsrest statt struct."""
    werte = []
    for _ in range(breite):
        werte.append(wert % 256)
        wert //= 256
    return bytes(werte)


def datei(eintraege, kennung=b"COVR", version=2, anzahl=None):
    """Baut eine Abdeckungsdatei von Hand aus (nummer, zeilen, abgedeckt)-Tupeln."""
    if anzahl is None:
        anzahl = len(eintraege)
    teile = [kennung, zahl(version, 2), zahl(anzahl, 2)]
    for nummer, zeilen, abgedeckt in eintraege:
        teile += [zahl(nummer, 4), zahl(zeilen, 2), zahl(abgedeckt, 2)]
    return b"".join(teile)


def lies_inhalt(daten):
    """Ruft lies_funktionen auf und macht aus dem Ergebnis eine Liste von Tupeln; die Form prüft ein eigener Test."""
    ergebnis, fehler = wert_von(lies_funktionen, daten)
    try:
        return [tuple(eintrag) for eintrag in ergebnis], fehler
    except Exception:
        return ergebnis, fehler


def kurz(wert):
    """Kürzt lange Werte für Meldungen."""
    text = repr(wert)
    return text if len(text) <= 120 else text[:100] + " …"


def ausnahme(fehler):
    """Beschreibt eine gefangene Ausnahme für eine Meldung."""
    return f"{type(fehler).__name__}: {fehler}" if fehler is not None else "keine Ausnahme"


EINTRAEGE = [(4711, 120, 96), (4712, 35, 35), (5003, 300, 0)]

# lies_kopf: das Beispiel
ergebnis, fehler = wert_von(lies_kopf, BEISPIEL)
assert ergebnis == (2, 3), (
    f"lies_kopf(BEISPIEL) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war (2, 3).\n"
    'Tipp: struct.unpack_from("<4sHH", daten, 0) liefert (kennung, version, anzahl).'
)

# lies_kopf: andere Werte (nicht fest hinschreiben!)
ergebnis, fehler = wert_von(lies_kopf, datei([], version=7, anzahl=0))
assert ergebnis == (7, 0), f"lies_kopf für Version 7 ohne Datensätze ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war (7, 0)."

# lies_kopf: Little-Endian, nicht Big-Endian
ergebnis, fehler = wert_von(lies_kopf, datei([(1, 1, 1)] * 2, version=258))
assert ergebnis == (258, 2), (
    f"lies_kopf für Version 258 (Bytes 02 01) mit 2 Datensätzen ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war "
    "(258, 2).\nTipp: Das Format beginnt mit \"<\" (Little-Endian); \">\" liest 02 00 als 512."
)

# lies_kopf: die größten Werte im Kopf (2 Bytes ohne Vorzeichen)
ergebnis, fehler = wert_von(lies_kopf, datei([], version=65535, anzahl=65535))
assert ergebnis == (65535, 65535), (
    f"lies_kopf für Version und Anzahl 65535 (Bytes ff ff) ergibt {ergebnis!r}, erwartet war (65535, 65535).\n"
    "Tipp: H ist ohne Vorzeichen, h mit Vorzeichen (dann wird ff ff zu -1)."
)

# lies_kopf: auch ein bytearray
ergebnis, fehler = wert_von(lies_kopf, bytearray(BEISPIEL))
assert ergebnis == (2, 3), f"lies_kopf(bytearray(BEISPIEL)) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war (2, 3)."

# lies_kopf: falsche Kennung
ergebnis, fehler = wert_von(lies_kopf, datei(EINTRAEGE, kennung=b"COVX"))
assert isinstance(fehler, ValueError), (
    f"lies_kopf mit Kennung b'COVX' ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."
)

# lies_kopf: zu kurze Daten lösen ValueError aus (struct.error ist keiner)
ergebnis, fehler = wert_von(lies_kopf, b"COV")
assert isinstance(fehler, ValueError), (
    f"lies_kopf(b'COV') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError.\n"
    "Tipp: struct.error ist keine Unterart von ValueError; prüfen Sie len(daten) vorher."
)

# lies_kopf: 7 Bytes sind zu kurz, auch wenn die Kennung stimmt
ergebnis, fehler = wert_von(lies_kopf, b"COVR\x02\x00\x03")
assert isinstance(fehler, ValueError), (
    f"lies_kopf(b'COVR\\x02\\x00\\x03') (7 Bytes) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."
)

# lies_kopf: leere Daten
ergebnis, fehler = wert_von(lies_kopf, b"")
assert isinstance(fehler, ValueError), f"lies_kopf(b'') ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war ein ValueError."

# lies_funktionen: das Beispiel
ergebnis, fehler = lies_inhalt(BEISPIEL)
assert ergebnis == EINTRAEGE, (
    f"lies_funktionen(BEISPIEL) ergibt {ergebnis!r} ({ausnahme(fehler)}),\nerwartet war {EINTRAEGE!r}.\n"
    'Tipp: struct.iter_unpack("<IHH", ...) über die Bytes ab Position 8 liefert ein Tupel je Datensatz.'
)

# lies_funktionen gibt eine Liste zurück
ergebnis, fehler = wert_von(lies_funktionen, BEISPIEL)
assert isinstance(ergebnis, list), (
    f"lies_funktionen(BEISPIEL) ergibt den Typ {type(ergebnis).__name__}, erwartet war eine Liste.\n"
    "Tipp: iter_unpack liefert einen Iterator; list(...) macht daraus eine Liste."
)

# lies_funktionen: jeder Datensatz ist ein Tupel
ergebnis, fehler = wert_von(lies_funktionen, BEISPIEL)
typen, _ = wert_von(lambda: [type(eintrag).__name__ for eintrag in ergebnis])
assert typen == ["tuple"] * 3, (
    f"Die Datensätze von lies_funktionen(BEISPIEL) haben die Typen {typen!r} ({ausnahme(fehler)}), erwartet waren "
    "drei Tupel (nummer, zeilen, abgedeckt).\nTipp: iter_unpack und unpack liefern schon Tupel; wandeln Sie sie "
    "nicht in Listen um."
)

# lies_funktionen: andere Werte, große Nummern (nicht fest hinschreiben!)
eintraege = [(2**32 - 1, 65535, 65535), (0, 0, 0), (305419896, 4660, 22136)]
ergebnis, fehler = lies_inhalt(datei(eintraege))
assert ergebnis == eintraege, (
    f"lies_funktionen für {eintraege!r} ergibt {ergebnis!r} ({ausnahme(fehler)}).\n"
    "Tipp: Die Nummer hat 4 Bytes (I), zeilen und abgedeckt je 2 (H), alle ohne Vorzeichen."
)

# lies_funktionen: auch ein bytearray
ergebnis, fehler = lies_inhalt(bytearray(BEISPIEL))
assert ergebnis == EINTRAEGE, f"lies_funktionen(bytearray(BEISPIEL)) ergibt {ergebnis!r} ({ausnahme(fehler)})."

# lies_funktionen: Datei ohne Datensätze
ergebnis, fehler = lies_inhalt(datei([]))
assert ergebnis == [], f"lies_funktionen für eine Datei ohne Datensätze ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war []."

# lies_funktionen: ein Byte zu wenig
ergebnis, fehler = wert_von(lies_funktionen, BEISPIEL[:-1])
assert isinstance(fehler, ValueError), (
    f"lies_funktionen mit 31 statt 32 Bytes ergibt {kurz(ergebnis)} ({ausnahme(fehler)}), erwartet war ein ValueError.\n"
    "Tipp: Vergleichen Sie len(daten) mit 8 + 8 * anzahl, bevor Sie lesen."
)

# lies_funktionen: ein ganzer Datensatz mehr, als der Kopf angibt
ergebnis, fehler = wert_von(lies_funktionen, datei(EINTRAEGE + [(1, 2, 3)], anzahl=3))
assert isinstance(fehler, ValueError), (
    f"lies_funktionen mit Anzahl 3 im Kopf, aber 4 Datensätzen ergibt {kurz(ergebnis)} ({ausnahme(fehler)}), "
    "erwartet war ein ValueError.\nTipp: Die Länge muss genau 8 + 8 * anzahl sein, nicht nur ein Vielfaches von 8."
)

# lies_funktionen: ein Datensatz weniger, als der Kopf angibt
ergebnis, fehler = wert_von(lies_funktionen, datei(EINTRAEGE, anzahl=4))
assert isinstance(fehler, ValueError), (
    f"lies_funktionen mit Anzahl 4 im Kopf, aber 3 Datensätzen ergibt {kurz(ergebnis)} ({ausnahme(fehler)}), "
    "erwartet war ein ValueError."
)

# lies_funktionen: falsche Kennung
ergebnis, fehler = wert_von(lies_funktionen, datei(EINTRAEGE, kennung=b"VOCR"))
assert isinstance(fehler, ValueError), (
    f"lies_funktionen mit Kennung b'VOCR' ergibt {kurz(ergebnis)} ({ausnahme(fehler)}), erwartet war ein ValueError.\n"
    "Tipp: Lesen Sie den Kopf mit lies_kopf, dann prüft er die Kennung mit."
)

# lies_funktionen: zu kurz für den Kopf
ergebnis, fehler = wert_von(lies_funktionen, b"CO")
assert isinstance(fehler, ValueError), f"lies_funktionen(b'CO') ergibt {kurz(ergebnis)} ({ausnahme(fehler)}), erwartet war ein ValueError."

# datensatzbereich: die richtigen Bytes
ergebnis, fehler = wert_von(datensatzbereich, BEISPIEL)
assert ergebnis is not None and bytes(ergebnis) == BEISPIEL[8:], (
    f"bytes(datensatzbereich(BEISPIEL)) ergibt {kurz(bytes(ergebnis)) if ergebnis is not None else None} "
    f"({ausnahme(fehler)}), erwartet war {BEISPIEL[8:]!r}."
)

# datensatzbereich gibt eine memoryview zurück
ergebnis, fehler = wert_von(datensatzbereich, BEISPIEL)
assert isinstance(ergebnis, memoryview), (
    f"datensatzbereich(BEISPIEL) ergibt den Typ {type(ergebnis).__name__}, erwartet war memoryview.\n"
    "Tipp: daten[8:] kopiert; memoryview(daten)[8:] ist eine Sicht ohne Kopie."
)

# datensatzbereich zeigt auf die übergebenen Daten selbst
puffer = bytearray(BEISPIEL)
ergebnis, fehler = wert_von(datensatzbereich, puffer)
assert isinstance(ergebnis, memoryview) and ergebnis.obj is puffer, (
    "datensatzbereich(puffer) soll eine memoryview auf puffer selbst sein (ergebnis.obj is puffer), "
    f"erhalten: {kurz(ergebnis)}.\nTipp: memoryview(bytes(daten)) oder memoryview(daten[8:]) zeigen auf eine Kopie."
)

# datensatzbereich: eine spätere Änderung am bytearray ist in der Sicht zu sehen
puffer = bytearray(BEISPIEL)
ergebnis, fehler = wert_von(datensatzbereich, puffer)
puffer[8] = 0xAB
assert ergebnis is not None and len(ergebnis) == 24 and ergebnis[0] == 0xAB, (
    "Nach puffer[8] = 0xAB soll datensatzbereich(puffer)[0] auch 171 (0xAB) sein, weil nichts kopiert wurde; "
    f"erhalten: {ergebnis[0] if ergebnis is not None and len(ergebnis) > 0 else ergebnis!r}."
)

# datensatzbereich: eine Datei ohne Datensätze ergibt eine leere Sicht
ergebnis, fehler = wert_von(datensatzbereich, datei([]))
assert ergebnis is not None and len(ergebnis) == 0 and isinstance(ergebnis, memoryview), (
    f"datensatzbereich für eine Datei ohne Datensätze ergibt {kurz(ergebnis)} ({ausnahme(fehler)}), "
    "erwartet war eine leere memoryview."
)

# setze_abgedeckt: das Beispiel
puffer = bytearray(BEISPIEL)
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, 2, 180)
erwartet = datei([(4711, 120, 96), (4712, 35, 35), (5003, 300, 180)])
assert bytes(puffer) == erwartet, (
    f"Nach setze_abgedeckt(puffer, 2, 180) ist puffer\n{bytes(puffer)!r} ({ausnahme(fehler)}),\nerwartet war\n{erwartet!r}.\n"
    'Tipp: struct.pack_into("<H", puffer, 8 + 8 * index + 6, abgedeckt)'
)

# setze_abgedeckt: der erste Datensatz, Wert mit zwei Bytes (nicht fest hinschreiben!)
puffer = bytearray(BEISPIEL)
wert_von(setze_abgedeckt, puffer, 0, 300)
erwartet = datei([(4711, 120, 300), (4712, 35, 35), (5003, 300, 0)])
assert bytes(puffer) == erwartet, (
    f"Nach setze_abgedeckt(puffer, 0, 300) ist puffer\n{bytes(puffer)!r},\nerwartet war\n{erwartet!r}.\n"
    "Tipp: 300 braucht zwei Bytes (2c 01), die Länge der Datei bleibt 32."
)

# setze_abgedeckt verändert puffer selbst und gibt nichts zurück
puffer = bytearray(BEISPIEL)
gleiches = puffer
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, 1, 0)
assert ergebnis is None and fehler is None and gleiches is puffer and bytes(puffer) == datei(
    [(4711, 120, 96), (4712, 35, 0), (5003, 300, 0)]
), (
    f"setze_abgedeckt(puffer, 1, 0) gibt {kurz(ergebnis)} zurück ({ausnahme(fehler)}), puffer ist danach "
    f"{bytes(puffer)!r}; erwartet war Rückgabe None und puffer verändert."
)

# setze_abgedeckt: der Index direkt hinter dem letzten Datensatz
puffer = bytearray(BEISPIEL)
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, 3, 1)
assert isinstance(fehler, IndexError) and bytes(puffer) == BEISPIEL, (
    f"setze_abgedeckt(puffer, 3, 1) bei 3 Datensätzen löst {ausnahme(fehler)} aus, erwartet war ein IndexError, "
    "und puffer bleibt unverändert.\nTipp: Gültig sind die Indizes 0 bis anzahl - 1."
)

# setze_abgedeckt: ein negativer Index zählt nicht von hinten
puffer = bytearray(BEISPIEL)
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, -1, 1)
assert isinstance(fehler, IndexError) and bytes(puffer) == BEISPIEL, (
    f"setze_abgedeckt(puffer, -1, 1) löst {ausnahme(fehler)} aus, puffer ist danach {bytes(puffer)!r}; "
    "erwartet war ein IndexError und puffer unverändert.\nTipp: pack_into mit einer Position vor dem Datensatzbereich "
    "würde in den Kopf schreiben; prüfen Sie 0 <= index < anzahl."
)

# setze_abgedeckt: ein Index weit hinter dem Ende
puffer = bytearray(BEISPIEL)
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, 70000, 1)
assert isinstance(fehler, IndexError), f"setze_abgedeckt(puffer, 70000, 1) löst {ausnahme(fehler)} aus, erwartet war ein IndexError."

# setze_abgedeckt: Datei ohne Datensätze
puffer = bytearray(datei([]))
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, 0, 1)
assert isinstance(fehler, IndexError) and len(puffer) == 8, (
    f"setze_abgedeckt(puffer, 0, 1) bei einer Datei ohne Datensätze löst {ausnahme(fehler)} aus, puffer hat danach "
    f"{len(puffer)} Bytes; erwartet war ein IndexError und puffer unverändert."
)

def zufallsdatei(zufall):
    """Erzeugt zufällige Einträge, eine Version und die Datei dazu; liefert (eintraege, version, daten)."""
    eintraege = [
        (zufall.randint(0, 2**32 - 1), zufall.randint(0, 65535), zufall.randint(0, 65535))
        for _ in range(zufall.randint(0, 12))
    ]
    version = zufall.randint(0, 65535)
    return eintraege, version, datei(eintraege, version=version)


zufall = Zufall(5054)
ZUFALLSDATEIEN = [zufallsdatei(zufall) for _ in range(300)]

# 300 zufällige Dateien: lies_kopf
for eintraege, version, daten in ZUFALLSDATEIEN:
    ergebnis, fehler = wert_von(lies_kopf, daten)
    assert ergebnis == (version, len(eintraege)), (
        f"lies_kopf({daten!r}) ergibt {ergebnis!r} ({ausnahme(fehler)}), erwartet war {(version, len(eintraege))!r}."
    )

# 300 zufällige Dateien: lies_funktionen
for eintraege, version, daten in ZUFALLSDATEIEN:
    ergebnis, fehler = lies_inhalt(daten)
    assert ergebnis == eintraege, (
        f"lies_funktionen({kurz(daten)}) ergibt {kurz(ergebnis)} ({ausnahme(fehler)}),\nerwartet war {eintraege!r}."
    )

# 300 zufällige Dateien: datensatzbereich
for eintraege, version, daten in ZUFALLSDATEIEN:
    sicht, fehler = wert_von(datensatzbereich, daten)
    assert sicht is not None and bytes(sicht) == daten[8:], f"datensatzbereich({kurz(daten)}) liefert falsche Bytes."

# 300 zufällige Dateien: setze_abgedeckt
for eintraege, version, daten in ZUFALLSDATEIEN:
    if eintraege:
        index = zufall.randrange(len(eintraege))
        neu = zufall.randint(0, 65535)
        puffer = bytearray(daten)
        wert_von(setze_abgedeckt, puffer, index, neu)
        nummer, zeilen, _ = eintraege[index]
        erwartet = datei(eintraege[:index] + [(nummer, zeilen, neu)] + eintraege[index + 1 :], version=version)
        assert bytes(puffer) == erwartet, (
            f"Nach setze_abgedeckt(puffer, {index}, {neu}) für {eintraege!r} ist puffer {bytes(puffer)!r}, "
            f"erwartet war {erwartet!r}."
        )

# Obere Grenze: 65 535 Datensätze
eintraege = [(zufall.randint(0, 2**32 - 1), zufall.randint(0, 65535), zufall.randint(0, 65535)) for _ in range(65535)]
daten = datei(eintraege)
ergebnis, fehler = lies_inhalt(daten)
assert ergebnis == eintraege, (
    f"lies_funktionen für 65 535 Datensätze ergibt {kurz(ergebnis)} ({ausnahme(fehler)}); "
    f"erwartet waren 65 535 Tupel, beginnend mit {eintraege[:2]!r}."
)

# Obere Grenze: setze_abgedeckt im letzten von 65 535 Datensätzen
puffer = bytearray(daten)
ergebnis, fehler = wert_von(setze_abgedeckt, puffer, 65534, 7)
assert struct.unpack_from("<H", puffer, len(puffer) - 2) == (7,) and len(puffer) == len(daten), (
    f"setze_abgedeckt(puffer, 65534, 7) ({ausnahme(fehler)}) soll die letzten zwei Bytes auf 07 00 setzen, "
    f"puffer endet aber mit {bytes(puffer[-8:])!r}."
)
