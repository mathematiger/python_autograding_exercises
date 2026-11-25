# Automatisch erzeugt aus lehrkraft/muster/3_077_guthabenbuch.py - nicht von Hand ändern.
# vorlage-hash: f5a7dbdcc10f8a13
# text-hash: 2fb6db7070dd5c60
# thema: programmaufbau
# inhalt: Kleines Projekt: Guthabenbuch

import os
import tempfile

ORDNER = tempfile.mkdtemp(prefix="aufgabe_3077_")
zaehler = [0]


def neuer_pfad():
    """Ein Pfad zu einer Datei, die es noch nicht gibt."""
    zaehler[0] += 1
    return os.path.join(ORDNER, f"guthaben_{zaehler[0]}.txt")


def inhalt_von(pfad):
    """Der Inhalt der Datei als Text, oder eine Beschreibung, warum er fehlt."""
    try:
        with open(pfad, encoding="utf-8") as datei:
            return datei.read()
    except FileNotFoundError:
        return "(Die Datei gibt es nicht.)"
    except UnicodeDecodeError:
        return "(Die Datei ist nicht in UTF-8 gespeichert.)"


def schreibe_selbst(pfad, text):
    """Legt die Datei mit genau diesem Text an."""
    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write(text)


def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def fehlerart(funktion, *argumente):
    """Ruft funktion auf und gibt den Namen der Ausnahme zurück, ohne Ausnahme None."""
    try:
        funktion(*argumente)
    except Exception as fehler:
        return type(fehler).__name__
    return None


def daten(buchung):
    """Die Attribute einer Buchung als Tupel, auch wenn welche fehlen."""
    return tuple(getattr(buchung, name, "(fehlt)") for name in ("monat", "art", "betrag"))


def alle_daten(buch):
    """Die Daten aller Buchungen eines Buchs als Liste."""
    return [daten(buchung) for buchung in getattr(buch, "buchungen", [])]


def beispielbuch():
    """Das Buch aus dem Beispiel der Aufgabe."""
    buch = Guthabenbuch("Kanzlei Berg")
    buch.einzahlen("2026-01", 500)
    buch.abbuchen("2026-01", 120)
    buch.abbuchen("2026-02", 120)
    return buch


BEISPIEL_DATEI = "Kanzlei Berg\n2026-01;einzahlung;500\n2026-01;abbuchung;120\n2026-02;abbuchung;120\n"

# Buchung: die drei Attribute
ergebnis = wert_von(lambda: daten(Buchung("2026-01", "einzahlung", 500)))
assert ergebnis == ("2026-01", "einzahlung", 500), (
    f'Buchung("2026-01", "einzahlung", 500) hat monat, art, betrag = {ergebnis!r}, erwartet war '
    "('2026-01', 'einzahlung', 500).\nTipp: Legen Sie in __init__ self.monat, self.art und self.betrag an."
)

# Buchung.wert: eine Einzahlung erhöht das Guthaben
ergebnis = wert_von(lambda: Buchung("2026-01", "einzahlung", 500).wert())
assert ergebnis == 500, f'Buchung("2026-01", "einzahlung", 500).wert() ergibt {ergebnis!r}, erwartet war 500.'

# Buchung.wert: eine Abbuchung verringert es
ergebnis = wert_von(lambda: Buchung("2026-02", "abbuchung", 120).wert())
assert ergebnis == -120, (
    f'Buchung("2026-02", "abbuchung", 120).wert() ergibt {ergebnis!r}, erwartet war -120.\n'
    "Tipp: Bei einer Abbuchung ist der Wert -self.betrag."
)

# Buchung.als_zeile: die Zeile für die Datei
ergebnis = wert_von(lambda: Buchung("2026-01", "abbuchung", 120).als_zeile())
assert ergebnis == "2026-01;abbuchung;120", (
    f'Buchung("2026-01", "abbuchung", 120).als_zeile() ergibt {ergebnis!r}, erwartet war "2026-01;abbuchung;120".\n'
    'Tipp: f"{self.monat};{self.art};{self.betrag}", ohne Leerzeichen und ohne Zeilenumbruch.'
)

# Buchung.als_zeile: eine andere Buchung (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: Buchung("2025-12", "einzahlung", 75).als_zeile())
assert ergebnis == "2025-12;einzahlung;75", (
    f'Buchung("2025-12", "einzahlung", 75).als_zeile() ergibt {ergebnis!r}, erwartet war "2025-12;einzahlung;75".'
)

# Buchung: eine unbekannte Art löst ValueError aus
ergebnis = fehlerart(Buchung, "2026-01", "gutschrift", 50)
assert ergebnis == "ValueError", (
    f'Buchung("2026-01", "gutschrift", 50) löst {ergebnis or "keine Ausnahme"} aus, erwartet war ValueError.\n'
    'Tipp: Erlaubt sind nur "einzahlung" und "abbuchung"; prüfen Sie art in __init__ und lösen Sie sonst '
    "raise ValueError(...) aus."
)

# Buchung: der Betrag 0 löst ValueError aus
ergebnis = fehlerart(Buchung, "2026-01", "einzahlung", 0)
assert ergebnis == "ValueError", (
    f'Buchung("2026-01", "einzahlung", 0) löst {ergebnis or "keine Ausnahme"} aus, erwartet war ValueError: '
    "Der Betrag muss größer als 0 sein."
)

# Buchung: ein negativer Betrag löst ValueError aus
ergebnis = fehlerart(Buchung, "2026-01", "abbuchung", -120)
assert ergebnis == "ValueError", (
    f'Buchung("2026-01", "abbuchung", -120) löst {ergebnis or "keine Ausnahme"} aus, erwartet war ValueError.'
)

# Buchung: 1 Euro ist erlaubt
ergebnis = wert_von(lambda: Buchung("2026-01", "abbuchung", 1).wert())
assert ergebnis == -1, f'Buchung("2026-01", "abbuchung", 1).wert() ergibt {ergebnis!r}, erwartet war -1.'

# buchung_aus_zeile: eine Zeile wird zur Buchung, der Betrag zur Zahl
ergebnis = wert_von(lambda: daten(buchung_aus_zeile("2026-02;abbuchung;120")))
assert ergebnis == ("2026-02", "abbuchung", 120), (
    f'buchung_aus_zeile("2026-02;abbuchung;120") hat monat, art, betrag = {ergebnis!r}, erwartet war '
    "('2026-02', 'abbuchung', 120).\nTipp: Zerlegen Sie mit split(\";\") und machen Sie den Betrag mit int(...) "
    "zur Zahl."
)

# buchung_aus_zeile: das Gegenstück zu als_zeile
ergebnis = wert_von(lambda: buchung_aus_zeile(Buchung("2024-07", "einzahlung", 999999).als_zeile()).als_zeile())
assert ergebnis == "2024-07;einzahlung;999999", (
    "buchung_aus_zeile(b.als_zeile()).als_zeile() für b = Buchung('2024-07', 'einzahlung', 999999) ergibt "
    f"{ergebnis!r}, erwartet war '2024-07;einzahlung;999999'."
)

# buchung_aus_zeile: zu wenige Felder lösen ValueError aus
ergebnis = fehlerart(buchung_aus_zeile, "2026-02;abbuchung")
assert ergebnis == "ValueError", (
    f'buchung_aus_zeile("2026-02;abbuchung") löst {ergebnis or "keine Ausnahme"} aus, erwartet war ValueError.\n'
    "Tipp: monat, art, betrag = zeile.split(\";\") löst ihn bei falscher Feldzahl schon selbst aus."
)

# buchung_aus_zeile: zu viele Felder lösen ValueError aus
ergebnis = fehlerart(buchung_aus_zeile, "2026-02;abbuchung;120;bar")
assert ergebnis == "ValueError", (
    f'buchung_aus_zeile("2026-02;abbuchung;120;bar") löst {ergebnis or "keine Ausnahme"} aus, erwartet war ValueError.'
)

# buchung_aus_zeile: ein Betrag, der keine ganze Zahl ist, löst ValueError aus
ergebnis = [fehlerart(buchung_aus_zeile, "2026-02;abbuchung;zwölf"), fehlerart(buchung_aus_zeile, "2026-02;abbuchung;12.5")]
assert ergebnis == ["ValueError", "ValueError"], (
    f'buchung_aus_zeile mit Betrag "zwölf" und "12.5" löst {ergebnis!r} aus (None heißt: keine Ausnahme), erwartet war '
    "beide Male ValueError.\nTipp: int(...) löst ihn selbst aus; benutzen Sie nicht float."
)

# buchung_aus_zeile: eine falsche Art oder ein Betrag 0 in der Zeile löst ValueError aus
ergebnis = [fehlerart(buchung_aus_zeile, "2026-02;gutschrift;5"), fehlerart(buchung_aus_zeile, "2026-02;einzahlung;0")]
assert ergebnis == ["ValueError", "ValueError"], (
    f'buchung_aus_zeile("2026-02;gutschrift;5") und buchung_aus_zeile("2026-02;einzahlung;0") lösen {ergebnis!r} aus, '
    "erwartet war beide Male ValueError.\nTipp: Bauen Sie die Buchung mit Buchung(...), dann prüft __init__ die Regeln."
)

# Guthabenbuch: ein neues Buch ist leer
ergebnis = wert_von(lambda: (Guthabenbuch("Kanzlei Berg").kunde, Guthabenbuch("Kanzlei Berg").buchungen))
assert ergebnis == ("Kanzlei Berg", []), (
    f'Guthabenbuch("Kanzlei Berg") hat kunde, buchungen = {ergebnis!r}, erwartet war ("Kanzlei Berg", []).'
)

# Guthabenbuch: ein neues Buch hat 0 Euro Guthaben
ergebnis = wert_von(lambda: Guthabenbuch("Kanzlei Berg").guthaben())
assert ergebnis == 0, f'Guthabenbuch("Kanzlei Berg").guthaben() ergibt {ergebnis!r}, erwartet war 0.'

# buchen: eine Einzahlung wird angehängt
buch = Guthabenbuch("Kanzlei Berg")
einzahlung = Buchung("2026-01", "einzahlung", 500)
wert_von(buch.buchen, einzahlung)
assert getattr(buch, "buchungen", None) == [einzahlung], (
    f"Nach buch.buchen(einzahlung) ist buch.buchungen {getattr(buch, 'buchungen', '(fehlt)')!r}, erwartet war "
    "eine Liste mit genau diesem Buchungsobjekt."
)

# guthaben: die Summe der Werte
ergebnis = wert_von(buch.guthaben)
assert ergebnis == 500, (
    f"Nach dem Buchen einer Einzahlung über 500 Euro ergibt guthaben() {ergebnis!r}, erwartet war 500.\n"
    "Tipp: Addieren Sie buchung.wert() für alle Buchungen in self.buchungen."
)

# einzahlen und abbuchen: das Beispiel aus der Aufgabe
ergebnis = wert_von(lambda: beispielbuch().guthaben())
assert ergebnis == 260, (
    f"Im Beispiel (500 einzahlen, zweimal 120 abbuchen) ergibt guthaben() {ergebnis!r}, erwartet war 260.\n"
    'Tipp: einzahlen baut Buchung(monat, "einzahlung", betrag) und gibt sie an self.buchen.'
)

# einzahlen und abbuchen legen Buchungen in der richtigen Reihenfolge an
ergebnis = wert_von(lambda: alle_daten(beispielbuch()))
erwartet = [("2026-01", "einzahlung", 500), ("2026-01", "abbuchung", 120), ("2026-02", "abbuchung", 120)]
assert ergebnis == erwartet, f"Im Beispiel sind die Buchungen\n{ergebnis!r},\nerwartet war\n{erwartet!r}."

# Das Programm gibt das Beispiel aus
assert vergleichbar(AUSGABE) == vergleichbar("260\n2026-01;abbuchung;120"), (
    f'Erwartete Ausgabe: "260" und "2026-01;abbuchung;120" – Ihr Programm: "{AUSGABE}"'
)

# abbuchen: mehr als das Guthaben löst ValueError aus
buch = beispielbuch()
ergebnis = fehlerart(buch.abbuchen, "2026-03", 300)
assert ergebnis == "ValueError", (
    f"Bei 260 Euro Guthaben löst abbuchen('2026-03', 300) {ergebnis or 'keine Ausnahme'} aus, erwartet war ValueError.\n"
    "Tipp: Prüfen Sie in buchen, ob self.guthaben() + buchung.wert() kleiner als 0 wäre."
)

# abbuchen: nach dem ValueError bleibt alles, wie es war
assert wert_von(buch.guthaben) == 260 and len(buch.buchungen) == 3, (
    f"Nach dem abgelehnten abbuchen('2026-03', 300) ist das Guthaben {wert_von(buch.guthaben)!r} bei "
    f"{len(buch.buchungen)} Buchungen, erwartet waren weiter 260 Euro bei 3 Buchungen.\n"
    "Tipp: Erst prüfen, dann anhängen."
)

# abbuchen: genau das ganze Guthaben ist erlaubt
buch = beispielbuch()
ergebnis = [fehlerart(buch.abbuchen, "2026-03", 260), wert_von(buch.guthaben)]
assert ergebnis == [None, 0], (
    f"Bei 260 Euro Guthaben ergibt abbuchen('2026-03', 260) die Ausnahme {ergebnis[0]!r} und danach das Guthaben "
    f"{ergebnis[1]!r}; erwartet waren keine Ausnahme (None) und 0.\nTipp: Nur ein Minus ist verboten, 0 Euro nicht."
)

# abbuchen: von einem leeren Buch geht nichts
buch = Guthabenbuch("Neukunde")
ergebnis = fehlerart(buch.abbuchen, "2026-01", 1)
assert ergebnis == "ValueError" and wert_von(buch.guthaben) == 0, (
    f"Auf einem neuen Buch löst abbuchen('2026-01', 1) {ergebnis or 'keine Ausnahme'} aus und das Guthaben ist "
    f"{wert_von(buch.guthaben)!r}; erwartet waren ValueError und 0."
)

# einzahlen: der Betrag 0 löst ValueError aus und ändert nichts
buch = beispielbuch()
ergebnis = fehlerart(buch.einzahlen, "2026-03", 0)
assert ergebnis == "ValueError" and len(buch.buchungen) == 3, (
    f"einzahlen('2026-03', 0) löst {ergebnis or 'keine Ausnahme'} aus, danach hat das Buch {len(buch.buchungen)} "
    "Buchungen; erwartet waren ValueError und weiter 3 Buchungen.\nTipp: Bauen Sie die Buchung mit Buchung(...), "
    "dann prüft schon __init__ den Betrag."
)

# abbuchen: ein negativer Betrag ist keine heimliche Einzahlung
buch = beispielbuch()
ergebnis = fehlerart(buch.abbuchen, "2026-03", -1000)
assert ergebnis == "ValueError" and wert_von(buch.guthaben) == 260, (
    f"abbuchen('2026-03', -1000) löst {ergebnis or 'keine Ausnahme'} aus, das Guthaben ist danach "
    f"{wert_von(buch.guthaben)!r}; erwartet waren ValueError und weiter 260."
)

# Zwei Bücher sind unabhängig
erstes = Guthabenbuch("Kanzlei Berg")
zweites = Guthabenbuch("Praxis Yilmaz")
wert_von(erstes.einzahlen, "2026-01", 100)
ergebnis = [wert_von(zweites.guthaben), len(getattr(zweites, "buchungen", []))]
assert ergebnis == [0, 0], (
    f"Nach einer Einzahlung ins erste Buch hat das zweite Guthaben und Anzahl Buchungen {ergebnis!r}, erwartet war "
    "[0, 0].\nTipp: Legen Sie die Liste in __init__ auf self an, nicht in der Klasse."
)

# speichern: die Zeilen der Datei im Beispiel (ohne Rücksicht auf Leerzeichen)
pfad = neuer_pfad()
fehler = wert_von(beispielbuch().speichern, pfad)
zeilen = [zeile.strip() for zeile in inhalt_von(pfad).splitlines() if zeile.strip()]
assert zeilen == BEISPIEL_DATEI.splitlines(), (
    f"Nach speichern(pfad) im Beispiel enthält die Datei\n{inhalt_von(pfad)!r}\nerwartet war\n{BEISPIEL_DATEI!r}"
    + (f"\nIhr Aufruf endete mit {fehler}" if fehler else "")
    + '\nTipp: with open(pfad, "w", encoding="utf-8") as datei:, dann erst der Kunde, dann buchung.als_zeile() je Zeile.'
)

# speichern: jede Zeile endet mit genau einem Zeilenumbruch
assert inhalt_von(pfad) == BEISPIEL_DATEI, (
    f"Nach speichern(pfad) im Beispiel enthält die Datei\n{inhalt_von(pfad)!r}\nerwartet war genau\n{BEISPIEL_DATEI!r}\n"
    'Tipp: write hängt keinen Zeilenumbruch an; schreiben Sie "\\n" selbst ans Ende jeder Zeile.'
)

# speichern: ein Buch ohne Buchungen, mit Umlauten im Namen
pfad = neuer_pfad()
wert_von(Guthabenbuch("Bäckerei Öztürk").speichern, pfad)
assert inhalt_von(pfad) == "Bäckerei Öztürk\n", (
    f"Guthabenbuch('Bäckerei Öztürk').speichern(pfad) schreibt {inhalt_von(pfad)!r}, erwartet war 'Bäckerei Öztürk\\n'.\n"
    'Tipp: Geben Sie beim Öffnen encoding="utf-8" an, und auch die Kundenzeile endet mit "\\n".'
)

# speichern: ein alter Inhalt wird ersetzt
pfad = neuer_pfad()
schreibe_selbst(pfad, "Alt\n2020-01;einzahlung;5\n")
buch = Guthabenbuch("Neu")
wert_von(buch.einzahlen, "2026-05", 42)
wert_von(buch.speichern, pfad)
assert inhalt_von(pfad) == "Neu\n2026-05;einzahlung;42\n", (
    f"Nach speichern auf eine Datei mit altem Inhalt enthält sie {inhalt_von(pfad)!r}, erwartet war "
    "'Neu\\n2026-05;einzahlung;42\\n'.\nTipp: Der Modus \"w\" leert die Datei; jede Zeile endet mit \"\\n\"."
)

# lade_guthabenbuch: Kunde und Guthaben aus der Beispieldatei
pfad = neuer_pfad()
schreibe_selbst(pfad, BEISPIEL_DATEI)
buch = wert_von(lade_guthabenbuch, pfad)
ergebnis = wert_von(lambda: (buch.kunde, buch.guthaben()))
assert ergebnis == ("Kanzlei Berg", 260), (
    f"lade_guthabenbuch auf der Beispieldatei ergibt Kunde und Guthaben {ergebnis!r}, erwartet war "
    "('Kanzlei Berg', 260).\nTipp: Die erste Zeile ist der Kunde (ohne Zeilenumbruch), jede weitere Zeile wird mit "
    "buchung_aus_zeile zur Buchung und mit buch.buchen(...) gebucht."
)

# lade_guthabenbuch: die Buchungen sind Buchung-Objekte mit den Daten der Datei
ergebnis = wert_von(lambda: [isinstance(b, Buchung) for b in buch.buchungen] + alle_daten(buch))
erwartet = [True, True, True, ("2026-01", "einzahlung", 500), ("2026-01", "abbuchung", 120), ("2026-02", "abbuchung", 120)]
assert ergebnis == erwartet, (
    f"Nach lade_guthabenbuch auf der Beispieldatei sind die Buchungen {ergebnis!r}, erwartet waren drei Buchung-"
    f"Objekte mit {erwartet[3:]!r}."
)

# Speichern und Laden ergibt dasselbe Buch
pfad = neuer_pfad()
original = Guthabenbuch("Stadtwerke Süd")
for monat, betrag in [("2026-01", 1000), ("2026-02", -300), ("2026-03", -300), ("2026-03", 50), ("2026-04", -450)]:
    if betrag > 0:
        wert_von(original.einzahlen, monat, betrag)
    else:
        wert_von(original.abbuchen, monat, -betrag)
wert_von(original.speichern, pfad)
geladen = wert_von(lade_guthabenbuch, pfad)
ergebnis = wert_von(lambda: (geladen.kunde, geladen.guthaben(), alle_daten(geladen)))
erwartet = ("Stadtwerke Süd", 0, alle_daten(original))
assert ergebnis == erwartet, f"Speichern und wieder Laden ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}."

# lade_guthabenbuch: eine Datei nur mit dem Kunden
pfad = neuer_pfad()
schreibe_selbst(pfad, "Praxis Yilmaz\n")
ergebnis = wert_von(lambda: (lade_guthabenbuch(pfad).kunde, lade_guthabenbuch(pfad).guthaben()))
assert ergebnis == ("Praxis Yilmaz", 0), (
    f"lade_guthabenbuch auf einer Datei mit nur 'Praxis Yilmaz\\n' ergibt {ergebnis!r}, erwartet war ('Praxis Yilmaz', 0)."
)

# lade_guthabenbuch: eine Abbuchung ins Minus in der Datei löst ValueError aus
pfad = neuer_pfad()
schreibe_selbst(pfad, "Kanzlei Berg\n2026-01;einzahlung;100\n2026-01;abbuchung;120\n")
ergebnis = fehlerart(lade_guthabenbuch, pfad)
assert ergebnis == "ValueError", (
    f"Eine Datei mit 100 Euro Einzahlung und 120 Euro Abbuchung ergibt bei lade_guthabenbuch "
    f"{ergebnis or 'keine Ausnahme'}, erwartet war ValueError.\nTipp: Buchen Sie jede Zeile mit buch.buchen(...), statt "
    "sie direkt an die Liste anzuhängen; dann gilt die Regel „kein Minus“ auch beim Laden."
)

# lade_guthabenbuch: fehlerhafte Zeilen lösen ValueError aus
fehlerhaft = ["2026-01;gutschrift;100", "2026-01;einzahlung", "2026-01;einzahlung;hundert", "2026-01;einzahlung;-5"]
ergebnis = []
for zeile in fehlerhaft:
    pfad = neuer_pfad()
    schreibe_selbst(pfad, f"Kanzlei Berg\n{zeile}\n")
    ergebnis.append(fehlerart(lade_guthabenbuch, pfad))
assert ergebnis == ["ValueError"] * 4, (
    f"Dateien mit den Buchungszeilen {fehlerhaft} ergeben bei lade_guthabenbuch {ergebnis!r} (None heißt: keine "
    "Ausnahme), erwartet war jedes Mal ValueError."
)

# lade_guthabenbuch: eine fehlende Datei meldet FileNotFoundError
ergebnis = fehlerart(lade_guthabenbuch, os.path.join(ORDNER, "gibt_es_nicht.txt"))
assert ergebnis == "FileNotFoundError", (
    f"lade_guthabenbuch auf einer Datei, die es nicht gibt, ergibt {ergebnis or 'keine Ausnahme'}, erwartet war "
    "FileNotFoundError.\nTipp: Fangen Sie den Fehler nicht ab; der Aufrufer soll merken, dass die Datei fehlt."
)

zufall = Zufall(3077)

# Viele zufällige Buchungsfolgen, gespeichert und wieder geladen
for versuch in range(60):
    buch = Guthabenbuch(f"Kunde {versuch}")
    stand = 0
    erwartet = []
    aufrufe = []
    for _ in range(zufall.randint(0, 15)):
        monat = f"2026-{zufall.randint(1, 12):02d}"
        art = zufall.choice(["einzahlen", "abbuchen", "abbuchen"])
        betrag = zufall.choice([zufall.randint(-5, 5), zufall.randint(1, 500), stand])
        aufrufe.append(f"{art}({monat!r}, {betrag})")
        ausnahme = fehlerart(getattr(buch, art), monat, betrag)
        if art == "einzahlen":
            erlaubt = betrag > 0
        else:
            erlaubt = 0 < betrag <= stand
        assert (ausnahme is None) == erlaubt, (
            f"Nach {', '.join(aufrufe)}: beim letzten Aufruf erwartet {'keine Ausnahme' if erlaubt else 'ValueError'}, "
            f"bekommen {ausnahme or 'keine Ausnahme'}."
        )
        if erlaubt:
            stand += betrag if art == "einzahlen" else -betrag
            erwartet.append((monat, "einzahlung" if art == "einzahlen" else "abbuchung", betrag))
    ergebnis = (wert_von(buch.guthaben), alle_daten(buch))
    assert ergebnis == (stand, erwartet), (
        f"Nach {', '.join(aufrufe) or 'keinem Aufruf'} ergibt das Buch Guthaben und Buchungen\n{ergebnis!r},\n"
        f"erwartet war\n{(stand, erwartet)!r}."
    )
    pfad = neuer_pfad()
    wert_von(buch.speichern, pfad)
    geladen = wert_von(lade_guthabenbuch, pfad)
    ergebnis = wert_von(lambda: (geladen.kunde, geladen.guthaben(), alle_daten(geladen)))
    assert ergebnis == (f"Kunde {versuch}", stand, erwartet), (
        f"Nach {', '.join(aufrufe) or 'keinem Aufruf'}, speichern und lade_guthabenbuch ergibt sich\n{ergebnis!r},\n"
        f"erwartet war\n{(f'Kunde {versuch}', stand, erwartet)!r}."
    )

# Obere Grenze: 1000 Buchungen speichern und laden
buch = Guthabenbuch("Großkunde")
for nummer in range(500):
    wert_von(buch.einzahlen, f"2026-{nummer % 12 + 1:02d}", 1_000_000)
    wert_von(buch.abbuchen, f"2026-{nummer % 12 + 1:02d}", 999_999)
pfad = neuer_pfad()
wert_von(buch.speichern, pfad)
geladen = wert_von(lade_guthabenbuch, pfad)
ergebnis = wert_von(lambda: (geladen.guthaben(), len(geladen.buchungen), len(inhalt_von(pfad).splitlines())))
assert ergebnis == (500, 1000, 1001), (
    f"Ein Buch mit je 500 Einzahlungen über 1 000 000 und Abbuchungen über 999 999 Euro ergibt nach Speichern und "
    f"Laden Guthaben, Buchungen und Dateizeilen {ergebnis!r}, erwartet war (500, 1000, 1001)."
)
