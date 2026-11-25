# Automatisch erzeugt aus lehrkraft/muster/3_048_aktionsliste.py - nicht von Hand ändern.
# vorlage-hash: 5f35b438219f4ac1
# text-hash: 666a60db79d79869
# thema: texte_zahlen
# inhalt: Textdatei schreiben und anhängen

import os
import shutil
import tempfile

ORDNER = tempfile.mkdtemp(prefix="aufgabe_3048_")
BEISPIEL = [("Ada", "Testserver bestellen"), ("Bo", "Pflichtenheft an den Kunden schicken")]
zaehler = [0]


def neuer_pfad():
    """Ein Pfad zu einer Datei, die es noch nicht gibt."""
    zaehler[0] += 1
    return os.path.join(ORDNER, f"aktionen_{zaehler[0]}.txt")


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


def als_text(aktionen):
    """Vergleichslösung: so soll die Datei aussehen."""
    text = ""
    for person, aufgabe in aktionen:
        text = text + person + ";" + aufgabe + "\n"
    return text


def aufruf(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def meldung_datei(aufruf_text, pfad, erwartet, tipp=""):
    """Fehlermeldung mit dem tatsächlichen und dem erwarteten Inhalt der Datei."""
    return f"Nach {aufruf_text} enthält die Datei\n{inhalt_von(pfad)!r}\nerwartet war\n{erwartet!r}{tipp}"


# speichere_aktionen im Beispiel: die Datei enthält die beiden Aktionen (Zeilen ohne Rücksicht auf Leerzeichen am Rand)
pfad = neuer_pfad()
fehler = aufruf(speichere_aktionen, pfad, BEISPIEL)
zeilen = [zeile.strip() for zeile in inhalt_von(pfad).splitlines() if zeile.strip()]
assert zeilen == ["Ada;Testserver bestellen", "Bo;Pflichtenheft an den Kunden schicken"], (
    meldung_datei("speichere_aktionen(pfad, BEISPIEL)", pfad, als_text(BEISPIEL))
    + (f"\nIhr Aufruf endete mit {fehler}" if fehler else "")
    + '\nTipp: with open(pfad, "w", encoding="utf-8") as datei: und datei.write(f"{person};{aufgabe}\\n").'
)

# speichere_aktionen im Beispiel: genau diese Form, jede Zeile mit Zeilenumbruch am Ende
assert inhalt_von(pfad) == als_text(BEISPIEL), meldung_datei(
    "speichere_aktionen(pfad, BEISPIEL)", pfad, als_text(BEISPIEL),
    '\nTipp: write hängt keinen Zeilenumbruch an; schreiben Sie "\\n" selbst ans Ende jeder Zeile, aber keine Leerzeichen um das Semikolon.',
)

# speichere_aktionen gibt nichts zurück
pfad = neuer_pfad()
ergebnis = aufruf(speichere_aktionen, pfad, BEISPIEL)
assert ergebnis is None, f"speichere_aktionen(pfad, BEISPIEL) ergibt {ergebnis!r}, erwartet war None."

# speichere_aktionen mit anderen Aktionen (nicht fest hinschreiben!)
pfad = neuer_pfad()
aktionen = [("Cem", "Sprint planen"), ("Dana", "Risiken bewerten"), ("Cem", "Protokoll, Teil 2, verteilen")]
aufruf(speichere_aktionen, pfad, aktionen)
assert inhalt_von(pfad) == als_text(aktionen), meldung_datei(f"speichere_aktionen(pfad, {aktionen})", pfad, als_text(aktionen))

# speichere_aktionen: Umlaute werden in UTF-8 gespeichert
pfad = neuer_pfad()
aktionen = [("Jörg", "Prüfplan für die Abnahme überarbeiten"), ("Özlem", "Größe der Datenbank schätzen")]
aufruf(speichere_aktionen, pfad, aktionen)
assert inhalt_von(pfad) == als_text(aktionen), meldung_datei(
    f"speichere_aktionen(pfad, {aktionen})", pfad, als_text(aktionen), '\nTipp: Geben Sie beim Öffnen encoding="utf-8" an.'
)

# speichere_aktionen ersetzt den alten Inhalt
pfad = neuer_pfad()
schreibe_selbst(pfad, "Alt;soll verschwinden\nAlt;auch das\n")
aufruf(speichere_aktionen, pfad, [("Ada", "Server neu starten")])
assert inhalt_von(pfad) == "Ada;Server neu starten\n", meldung_datei(
    "speichere_aktionen(pfad, [('Ada', 'Server neu starten')]) auf einer Datei mit altem Inhalt", pfad,
    "Ada;Server neu starten\n", '\nTipp: Der Modus "w" leert die Datei, "a" hängt nur an.',
)

# speichere_aktionen mit einer leeren Liste legt eine leere Datei an
pfad = neuer_pfad()
aufruf(speichere_aktionen, pfad, [])
assert inhalt_von(pfad) == "", meldung_datei("speichere_aktionen(pfad, [])", pfad, "", "\nTipp: Auch ohne Aktionen wird die Datei geöffnet und damit angelegt.")

# ergaenze_aktion hängt hinten an
pfad = neuer_pfad()
schreibe_selbst(pfad, "Ada;Testserver bestellen\n")
aufruf(ergaenze_aktion, pfad, "Bo", "Pflichtenheft an den Kunden schicken")
assert inhalt_von(pfad) == als_text(BEISPIEL), meldung_datei(
    "ergaenze_aktion(pfad, 'Bo', 'Pflichtenheft an den Kunden schicken')", pfad, als_text(BEISPIEL),
    '\nTipp: Öffnen Sie die Datei mit dem Modus "a".',
)

# ergaenze_aktion mehrmals hintereinander, mit anderen Werten (nicht fest hinschreiben!)
pfad = neuer_pfad()
schreibe_selbst(pfad, "Ada;Testserver bestellen\n")
aufruf(ergaenze_aktion, pfad, "Emil", "Backup prüfen")
aufruf(ergaenze_aktion, pfad, "Fatma", "Kunden anrufen")
erwartet = "Ada;Testserver bestellen\nEmil;Backup prüfen\nFatma;Kunden anrufen\n"
assert inhalt_von(pfad) == erwartet, meldung_datei("zwei Aufrufen von ergaenze_aktion", pfad, erwartet)

# ergaenze_aktion legt eine fehlende Datei an
pfad = neuer_pfad()
fehler = aufruf(ergaenze_aktion, pfad, "Gül", "Raum buchen")
assert inhalt_von(pfad) == "Gül;Raum buchen\n", (
    meldung_datei("ergaenze_aktion(pfad, 'Gül', 'Raum buchen') ohne vorhandene Datei", pfad, "Gül;Raum buchen\n")
    + (f"\nIhr Aufruf endete mit {fehler}" if fehler else "")
)

# lies_aktionen im Beispiel
pfad = neuer_pfad()
schreibe_selbst(pfad, als_text(BEISPIEL))
ergebnis = aufruf(lies_aktionen, pfad)
assert ergebnis == BEISPIEL, (
    f"Für die Datei {als_text(BEISPIEL)!r} ergibt lies_aktionen(pfad) {ergebnis!r}, erwartet war {BEISPIEL!r}.\n"
    'Tipp: Entfernen Sie mit rstrip("\\n") den Zeilenumbruch, zerlegen Sie mit split(";") und hängen Sie das Paar als Tupel an.'
)

# lies_aktionen mit einer anderen Datei, die leere Zeilen enthält
pfad = neuer_pfad()
schreibe_selbst(pfad, "Hanna;Angebot einholen\n\nIgor;Termin mit dem Kunden\n\n")
ergebnis = aufruf(lies_aktionen, pfad)
erwartet = [("Hanna", "Angebot einholen"), ("Igor", "Termin mit dem Kunden")]
assert ergebnis == erwartet, (
    f"Für eine Datei mit leeren Zeilen ergibt lies_aktionen {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Überspringen Sie Zeilen, die nach dem Entfernen des Zeilenumbruchs leer sind."
)

# lies_aktionen: die letzte Zeile ohne Zeilenumbruch
pfad = neuer_pfad()
schreibe_selbst(pfad, "Hanna;Angebot einholen\nIgor;Termin mit dem Kunden")
ergebnis = aufruf(lies_aktionen, pfad)
assert ergebnis == erwartet, f"Für eine Datei ohne Zeilenumbruch am Ende ergibt lies_aktionen {ergebnis!r}, erwartet war {erwartet!r}."

# lies_aktionen: eine leere Datei
pfad = neuer_pfad()
schreibe_selbst(pfad, "")
ergebnis = aufruf(lies_aktionen, pfad)
assert ergebnis == [], f"Für eine leere Datei ergibt lies_aktionen {ergebnis!r}, erwartet war []."

# lies_aktionen: ohne Datei eine leere Liste
ergebnis = aufruf(lies_aktionen, neuer_pfad())
assert ergebnis == [], (
    f"Für eine Datei, die es nicht gibt, ergibt lies_aktionen {ergebnis!r}, erwartet war [].\n"
    "Tipp: Fangen Sie den FileNotFoundError mit try/except ab und geben Sie dann [] zurück."
)

# Zusammen: speichern, ergänzen und wieder lesen ergibt dieselben Aktionen
pfad = neuer_pfad()
aufruf(speichere_aktionen, pfad, [("Ada", "Testserver bestellen")])
aufruf(ergaenze_aktion, pfad, "Bo", "Pflichtenheft an den Kunden schicken")
ergebnis = aufruf(lies_aktionen, pfad)
assert ergebnis == BEISPIEL, f"Speichern, Ergänzen und Lesen wie im Beispiel ergibt {ergebnis!r}, erwartet war {BEISPIEL!r}."

# Viele zufällige Aktionslisten
zufall = Zufall(3048)
personen = ["Ada", "Bo", "Jörg", "Özlem", "Mia Sophie"]
aufgaben = ["Server bestellen", "Kunden anrufen", "Prüfplan, Version 2", "Größe schätzen", "Tests schreiben"]
for _ in range(60):
    aktionen = [(zufall.choice(personen), zufall.choice(aufgaben)) for _ in range(zufall.randint(0, 8))]
    zusatz = [(zufall.choice(personen), zufall.choice(aufgaben)) for _ in range(zufall.randint(0, 3))]
    pfad = neuer_pfad()
    aufruf(speichere_aktionen, pfad, aktionen)
    for person, aufgabe in zusatz:
        aufruf(ergaenze_aktion, pfad, person, aufgabe)
    assert inhalt_von(pfad) == als_text(aktionen + zusatz), meldung_datei(
        f"speichere_aktionen(pfad, {aktionen}) und ergaenze_aktion für {zusatz}", pfad, als_text(aktionen + zusatz)
    )
    ergebnis = aufruf(lies_aktionen, pfad)
    assert ergebnis == aktionen + zusatz, f"lies_aktionen ergibt {ergebnis!r}, erwartet war {aktionen + zusatz!r}."

# Obere Grenze: 10 000 Aktionen
aktionen = [(f"Person {nummer}", f"Aufgabe {nummer}") for nummer in range(10000)]
pfad = neuer_pfad()
aufruf(speichere_aktionen, pfad, aktionen)
ergebnis = aufruf(lies_aktionen, pfad)
assert ergebnis == aktionen, f"Bei 10 000 Aktionen ergibt lies_aktionen {str(ergebnis)[:200]} …, erwartet waren alle 10 000 Paare."

shutil.rmtree(ORDNER, ignore_errors=True)  # aufräumen
