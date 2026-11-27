# Automatisch erzeugt aus lehrkraft/muster/3_046_artikelexport.py - nicht von Hand ändern.
# vorlage-hash: ba706c59cd265075
# text-hash: c27abe8ef5ae009a
# thema: texte_zahlen
# inhalt: Textdatei zeilenweise lesen

import os
import tempfile

BEISPIEL = (
    "artikelnummer;bezeichnung;preis\n"
    "A-1001;USB-Kabel;4.99\n"
    "A-1002;;12.50\n"
    "A-1003;Maus;19.90\n"
    "\n"
    "A-1004;Tastatur\n"
    "A-1005;Headset;39.00;Restposten\n"
)


def mit_datei(inhalt, funktion):
    """Schreibt inhalt in eine temporäre Datei, ruft funktion(pfad) auf und räumt danach auf.

    Ein Fehler wird als Text zurückgegeben.
    """
    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, "artikel.txt")
        with open(pfad, "w", encoding="utf-8", newline="") as datei:
            datei.write(inhalt)
        try:
            return funktion(pfad)
        except Exception as fehler:
            return f"{type(fehler).__name__}: {fehler}"


def vergleich_zeilen(inhalt):
    """Vergleichslösung: zerlegt den Text an jedem Zeilenumbruch."""
    zeilen = inhalt.split("\n")
    if zeilen[-1] == "":
        zeilen.pop()
    return zeilen


def vergleich_export(inhalt):
    """Vergleichslösung: prüft jede Zeile ohne enumerate und ohne all."""
    gueltig = 0
    fehlerhaft = []
    zeilen = vergleich_zeilen(inhalt)
    for stelle in range(1, len(zeilen)):
        if zeilen[stelle].strip() == "":
            continue
        felder = [feld.strip() for feld in zeilen[stelle].split(";")]
        if len(felder) == 3 and "" not in felder:
            gueltig += 1
        else:
            fehlerhaft.append(stelle + 1)
    return (gueltig, fehlerhaft)


def meldung(name, inhalt, ergebnis, erwartet, tipp=""):
    """Fehlermeldung mit dem Dateiinhalt, dem Ergebnis und dem erwarteten Wert."""
    return f"Für die Datei\n{inhalt!r}\nergibt {name}(pfad) {ergebnis!r}, erwartet war {erwartet!r}.{tipp}"


# lies_zeilen im Beispiel: die Datei wird gelesen, die erste Zeile ist die Kopfzeile
ergebnis = mit_datei(BEISPIEL, lies_zeilen)
assert isinstance(ergebnis, list) and len(ergebnis) > 0 and ergebnis[0].strip() == "artikelnummer;bezeichnung;preis", (
    meldung("lies_zeilen", BEISPIEL, ergebnis, vergleich_zeilen(BEISPIEL))
    + '\nTipp: with open(pfad, encoding="utf-8") as datei: öffnet die Datei, for zeile in datei: liefert die Zeilen.'
)

# lies_zeilen im Beispiel: alle Zeilen ohne Zeilenumbruch
assert ergebnis == vergleich_zeilen(BEISPIEL), meldung(
    "lies_zeilen", BEISPIEL, ergebnis, vergleich_zeilen(BEISPIEL), '\nTipp: zeile.rstrip("\\n") entfernt den Zeilenumbruch am Ende.'
)

# lies_zeilen mit einer anderen Datei, letzte Zeile ohne Zeilenumbruch (nicht fest hinschreiben!)
inhalt = "artikelnummer;bezeichnung;preis\nB-7;Monitor;149.00\nB-8;Dockingstation;89.90"
ergebnis = mit_datei(inhalt, lies_zeilen)
assert ergebnis == vergleich_zeilen(inhalt), meldung("lies_zeilen", inhalt, ergebnis, vergleich_zeilen(inhalt))

# lies_zeilen: Umlaute werden richtig gelesen
inhalt = "artikelnummer;bezeichnung;preis\nC-1;Lötstation;59.00\nC-2;Kühlpaste;7.49\n"
ergebnis = mit_datei(inhalt, lies_zeilen)
assert ergebnis == vergleich_zeilen(inhalt), meldung(
    "lies_zeilen", inhalt, ergebnis, vergleich_zeilen(inhalt), '\nTipp: Geben Sie beim Öffnen encoding="utf-8" an.'
)

# lies_zeilen: nur die Kopfzeile
inhalt = "artikelnummer;bezeichnung;preis\n"
ergebnis = mit_datei(inhalt, lies_zeilen)
assert ergebnis == ["artikelnummer;bezeichnung;preis"], meldung("lies_zeilen", inhalt, ergebnis, ["artikelnummer;bezeichnung;preis"])

# lies_zeilen: Leerzeichen am Rand und leere Zeilen bleiben erhalten
inhalt = "artikelnummer;bezeichnung;preis\n  D-1;Beamer;399.00  \n\n   \nD-2;Leinwand;120.00\n"
ergebnis = mit_datei(inhalt, lies_zeilen)
assert ergebnis == vergleich_zeilen(inhalt), meldung(
    "lies_zeilen", inhalt, ergebnis, vergleich_zeilen(inhalt), '\nTipp: strip() entfernt auch Leerzeichen; rstrip("\\n") nur den Zeilenumbruch.'
)

# lies_zeilen: eine fehlende Datei löst FileNotFoundError aus
try:
    lies_zeilen(os.path.join(tempfile.gettempdir(), "gibt_es_nicht_3046", "artikel.txt"))
    fehlerart = "keine Ausnahme"
except Exception as fehler:
    fehlerart = type(fehler).__name__
assert fehlerart == "FileNotFoundError", (
    f"lies_zeilen für eine Datei, die es nicht gibt, ergibt {fehlerart}, erwartet war FileNotFoundError.\n"
    "Tipp: Fangen Sie den Fehler nicht ab; der Aufrufer soll merken, dass die Datei fehlt."
)

# pruefe_export im Beispiel: zwei gültige Datensätze
ergebnis = mit_datei(BEISPIEL, pruefe_export)
assert isinstance(ergebnis, tuple) and len(ergebnis) == 2 and ergebnis[0] == 2, meldung(
    "pruefe_export", BEISPIEL, ergebnis, (2, [3, 6, 7]), "\nTipp: Zerlegen Sie jede Zeile mit split(\";\") und zählen Sie die Felder."
)

# pruefe_export im Beispiel: die fehlerhaften Zeilen 3, 6 und 7
assert ergebnis == (2, [3, 6, 7]), meldung(
    "pruefe_export",
    BEISPIEL,
    ergebnis,
    (2, [3, 6, 7]),
    "\nTipp: Zählen Sie die Zeilen mit enumerate(..., start=1) wie in der Datei, auch die Kopfzeile und die leere Zeile.",
)

# pruefe_export mit einer anderen Datei (nicht fest hinschreiben!)
inhalt = "artikelnummer;bezeichnung;preis\nE-1;Router;79.00\nE-2;Switch\nE-3;Patchkabel;2.50\nE-4;Access Point;119.00\n"
ergebnis = mit_datei(inhalt, pruefe_export)
assert ergebnis == vergleich_export(inhalt), meldung("pruefe_export", inhalt, ergebnis, vergleich_export(inhalt))

# pruefe_export: die Kopfzeile zählt nicht als Datensatz
inhalt = "artikelnummer;bezeichnung;preis\nF-1;Webcam;49.00"
ergebnis = mit_datei(inhalt, pruefe_export)
assert ergebnis == (1, []), meldung("pruefe_export", inhalt, ergebnis, (1, []), "\nTipp: Überspringen Sie die erste Zeile.")

# pruefe_export: nur die Kopfzeile
inhalt = "artikelnummer;bezeichnung;preis\n"
ergebnis = mit_datei(inhalt, pruefe_export)
assert ergebnis == (0, []), meldung("pruefe_export", inhalt, ergebnis, (0, []))

# pruefe_export: ein Feld nur aus Leerzeichen ist leer
inhalt = "artikelnummer;bezeichnung;preis\nG-1;   ;5.00\nG-2;Hub; \n G-3 ; Adapter ; 3.00 \n"
ergebnis = mit_datei(inhalt, pruefe_export)
assert ergebnis == (1, [2, 3]), meldung(
    "pruefe_export", inhalt, ergebnis, (1, [2, 3]), "\nTipp: Prüfen Sie jedes Feld mit feld.strip() != \"\"."
)

# pruefe_export: Zeilen nur aus Leerraum zählen nicht
inhalt = "artikelnummer;bezeichnung;preis\n   \nH-1;Akku;29.00\n\n\t\n"
ergebnis = mit_datei(inhalt, pruefe_export)
assert ergebnis == (1, []), meldung(
    "pruefe_export", inhalt, ergebnis, (1, []), "\nTipp: Prüfen Sie zuerst mit zeile.strip() == \"\", ob die Zeile leer ist."
)

# pruefe_export: nur Semikolons und ein leeres viertes Feld sind fehlerhaft
inhalt = "artikelnummer;bezeichnung;preis\n;;\nJ-1;Kabelbinder;1.20;\n"
ergebnis = mit_datei(inhalt, pruefe_export)
assert ergebnis == (0, [2, 3]), meldung("pruefe_export", inhalt, ergebnis, (0, [2, 3]))

# pruefe_export benutzt lies_zeilen
assert verwendet("lies_zeilen"), "pruefe_export soll die Datei mit lies_zeilen(pfad) lesen, statt sie ein zweites Mal selbst zu öffnen."

# Viele zufällige Dateien
zufall = Zufall(3046)
bausteine = ["K-1", "Maus", "4.99", "", "  ", "Lüfter", "12.00", "Kabel"]
for _ in range(150):
    zeilen = ["artikelnummer;bezeichnung;preis"]
    for _ in range(zufall.randint(0, 12)):
        art = zufall.random()
        if art < 0.15:
            zeilen.append(zufall.choice(["", "   ", "\t"]))
        else:
            zeilen.append(";".join(zufall.choice(bausteine) for _ in range(zufall.choice([1, 2, 3, 3, 3, 4]))))
    inhalt = "\n".join(zeilen) + zufall.choice(["", "\n"])
    ergebnis = mit_datei(inhalt, pruefe_export)
    assert ergebnis == vergleich_export(inhalt), meldung("pruefe_export", inhalt, ergebnis, vergleich_export(inhalt))

# Obere Grenze: 100 000 Zeilen
zeilen = ["artikelnummer;bezeichnung;preis"]
for nummer in range(1, 100000):
    if nummer % 1000 == 0:
        zeilen.append(f"Z-{nummer};;1.00")
    else:
        zeilen.append(f"Z-{nummer};Artikel {nummer};{nummer % 100}.99")
inhalt = "\n".join(zeilen) + "\n"
ergebnis = mit_datei(inhalt, pruefe_export)
erwartet = vergleich_export(inhalt)
assert ergebnis == erwartet, (
    f"Bei 100 000 Zeilen ergibt pruefe_export {str(ergebnis)[:200]}, erwartet war {str(erwartet)[:200]}."
)
