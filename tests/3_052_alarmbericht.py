# Automatisch erzeugt aus lehrkraft/muster/3_052_alarmbericht.py - nicht von Hand ändern.
# vorlage-hash: bf95387ab8213aaf
# text-hash: 76c8dac120133ebb
# thema: texte_zahlen
# inhalt: csv.writer und DictWriter

import csv
import os
import tempfile

ORDNER = tempfile.mkdtemp(prefix="aufgabe_3052_")
BEISPIEL = [{"zeit": "03:12", "server": "db01", "meldung": "RAM 97 %, Swap aktiv", "notiz": "Ada ruft an"}]


def neuer_pfad(name):
    """Ein Pfad im Testordner, an dem noch keine Datei liegt."""
    pfad = os.path.join(ORDNER, name)
    if os.path.exists(pfad):
        os.remove(pfad)
    return pfad


def schreibe_und_lies(funktion, name, daten):
    """Ruft die Funktion auf und liest die Datei mit csv.reader; liefert die Zeilen oder den Fehler als Text."""
    pfad = neuer_pfad(name)
    try:
        funktion(pfad, daten)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"
    if not os.path.exists(pfad):
        return "(keine Datei angelegt)"
    with open(pfad, encoding="utf-8", newline="") as datei:
        return list(csv.reader(datei))


def roher_text(name):
    """Der Inhalt der Datei im Testordner, wie er auf der Platte steht."""
    with open(os.path.join(ORDNER, name), encoding="utf-8", newline="") as datei:
        return datei.read()


def erwartete_messwerte(messwerte):
    """Vergleichslösung: so liest csv.reader die Datei mit den Messwerten zurück."""
    return [["server", "metrik", "wert"]] + [[server, metrik, str(wert)] for server, metrik, wert in messwerte]


def erwartete_alarme(alarme):
    """Vergleichslösung: so liest csv.reader die Datei mit den Alarmen zurück."""
    return [["zeit", "server", "meldung"]] + [[a["zeit"], a["server"], a["meldung"]] for a in alarme]


def pruefe(funktion, erwartung, daten, hinweis=""):
    """Schreibt die Daten und vergleicht, was csv.reader zurückliest; liefert (stimmt, Meldung)."""
    zeilen = schreibe_und_lies(funktion, "test.csv", daten)
    erwartet = erwartung(daten)
    text = f"{funktion.__name__}(pfad, {daten!r})\nDatei mit csv.reader gelesen: {zeilen!r}\nerwartet: {erwartet!r}"
    return zeilen == erwartet, text + hinweis


# schreibe_messwerte legt eine Datei an
zeilen = schreibe_und_lies(schreibe_messwerte, "messwerte.csv", [("web01", "cpu", 93.5)])
assert isinstance(zeilen, list), (
    f"schreibe_messwerte(pfad, [('web01', 'cpu', 93.5)]) ergibt: {zeilen}\n"
    'Tipp: with open(pfad, "w", encoding="utf-8", newline="") as datei: und darin csv.writer(datei).'
)

# schreibe_messwerte: Kopfzeile und eine Zeile
stimmt, text = pruefe(schreibe_messwerte, erwartete_messwerte, [("web01", "cpu", 93.5)])
assert stimmt, text + "\nTipp: Zuerst writerow(['server', 'metrik', 'wert']), dann writerows(messwerte)."

# schreibe_messwerte: mehrere Zeilen mit anderen Werten (nicht fest hinschreiben!)
messwerte = [("db01", "ram", 71), ("db02", "ram", 12.25), ("mail01", "disk", 100000)]
stimmt, text = pruefe(schreibe_messwerte, erwartete_messwerte, messwerte)
assert stimmt, text

# schreibe_messwerte: Randfall ohne Messwerte, nur die Kopfzeile
stimmt, text = pruefe(schreibe_messwerte, erwartete_messwerte, [])
assert stimmt, text

# schreibe_messwerte ersetzt eine vorhandene Datei
pfad = neuer_pfad("ersetzen.csv")
try:
    schreibe_messwerte(pfad, [("alt01", "cpu", 1), ("alt02", "cpu", 2)])
    schreibe_messwerte(pfad, [("neu01", "ram", 3)])
    with open(pfad, encoding="utf-8", newline="") as datei:
        zeilen = list(csv.reader(datei))
except Exception as fehler:
    zeilen = f"{type(fehler).__name__}: {fehler}"
assert zeilen == [["server", "metrik", "wert"], ["neu01", "ram", "3"]], (
    f"Nach zwei Aufrufen von schreibe_messwerte mit demselben Pfad steht in der Datei {zeilen!r},\n"
    "erwartet war nur der Inhalt des zweiten Aufrufs.\nTipp: Modus \"w\" ersetzt, \"a\" hängt an."
)

# schreibe_alarme im Beispiel: drei Spalten, die Notiz fehlt
zeilen = schreibe_und_lies(schreibe_alarme, "alarme.csv", BEISPIEL)
assert isinstance(zeilen, list) and len(zeilen) == 2 and len(zeilen[1]) == 3, (
    f"Für das Beispiel liest csv.reader aus Ihrer Datei {zeilen!r},\n"
    "erwartet waren zwei Zeilen mit je drei Feldern.\n"
    "Tipp: Ein ValueError mit „fields not in fieldnames“ heißt: extrasaction=\"ignore\" fehlt."
)

# schreibe_alarme im Beispiel: das Komma in der Meldung bleibt in einem Feld
stimmt, text = pruefe(schreibe_alarme, erwartete_alarme, BEISPIEL)
assert stimmt, text + "\nTipp: csv.DictWriter(datei, fieldnames=SPALTEN, extrasaction=\"ignore\"), dann writeheader()."

# schreibe_alarme im Beispiel: in der Datei steht die Meldung in Anführungszeichen
text = roher_text("test.csv")
assert '03:12,db01,"RAM 97 %, Swap aktiv"' in text, (
    f"In Ihrer Datei steht:\n{text}\nerwartet war die Zeile 03:12,db01,\"RAM 97 %, Swap aktiv\".\n"
    "Tipp: csv.writer und csv.DictWriter setzen die Anführungszeichen selbst."
)

# schreibe_alarme mit anderen Alarmen (nicht fest hinschreiben!)
alarme = [
    {"zeit": "00:01", "server": "web02", "meldung": "CPU 99 %"},
    {"zeit": "04:30", "server": "fs01", "meldung": 'Platte "D:" fast voll', "notiz": "-", "ticket": "1077"},
]
stimmt, text = pruefe(schreibe_alarme, erwartete_alarme, alarme)
assert stimmt, text

# schreibe_alarme: die Spalten in der Reihenfolge von SPALTEN, auch wenn das Dictionary anders sortiert ist
alarme = [{"meldung": "Ping fehlt", "server": "vpn01", "zeit": "05:55"}]
stimmt, text = pruefe(schreibe_alarme, erwartete_alarme, alarme)
assert stimmt, text

# schreibe_alarme: Randfall ohne Alarme, nur die Kopfzeile
stimmt, text = pruefe(schreibe_alarme, erwartete_alarme, [])
assert stimmt, text

# schreibe_alarme ersetzt eine vorhandene Datei
pfad = neuer_pfad("ersetzen.csv")
try:
    schreibe_alarme(pfad, [{"zeit": "01:00", "server": "alt01", "meldung": "alt"}] * 3)
    schreibe_alarme(pfad, [])
    with open(pfad, encoding="utf-8", newline="") as datei:
        zeilen = list(csv.reader(datei))
except Exception as fehler:
    zeilen = f"{type(fehler).__name__}: {fehler}"
assert zeilen == [SPALTEN], f"Nach schreibe_alarme(pfad, []) über einer alten Datei steht darin {zeilen!r}, erwartet war [{SPALTEN}]."

# Die Funktionen geben nichts zurück
pfad = neuer_pfad("rueckgabe.csv")
ergebnisse = [schreibe_messwerte(pfad, []), schreibe_alarme(pfad, [])]
assert ergebnisse == [None, None], f"Die Funktionen geben {ergebnisse} zurück, erwartet war nichts (None)."

# Die Ausgabe des Programms
erwartet = 'zeit,server,meldung\n03:12,db01,"RAM 97 %, Swap aktiv"'
assert AUSGABE.replace("\r", "") == erwartet, f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

zufall = Zufall(3052)
dateien = []
woerter = ["CPU", "RAM", "Lüfter", "laut", ",", '"', "100 %", "Störung, kritisch", "'", ";"]
for _ in range(100):
    messwerte = []
    alarme = []
    for nummer in range(zufall.randint(0, 6)):
        wert = zufall.choice([zufall.randint(0, 100000), zufall.randint(0, 10000) / 100])
        messwerte.append((f"srv{nummer}", zufall.choice(["cpu", "ram", "disk"]), wert))
        alarm = {"zeit": f"{zufall.randint(0, 23):02}:{zufall.randint(0, 59):02}", "server": f"srv{nummer}"}
        alarm["meldung"] = " ".join(zufall.choice(woerter) for _ in range(zufall.randint(1, 5)))
        for zusatz in zufall.sample(["notiz", "ticket", "quelle"], zufall.randint(0, 3)):
            alarm[zusatz] = "x, y"
        alarme.append(alarm)
    dateien.append((messwerte, alarme))

# Viele zufällige Dateien mit Kommas, Anführungszeichen und Umlauten: schreibe_messwerte
for messwerte, alarme in dateien:
    stimmt, text = pruefe(schreibe_messwerte, erwartete_messwerte, messwerte)
    assert stimmt, text

# Viele zufällige Dateien mit Kommas, Anführungszeichen und Umlauten: schreibe_alarme
for messwerte, alarme in dateien:
    stimmt, text = pruefe(schreibe_alarme, erwartete_alarme, alarme)
    assert stimmt, text

# Obere Grenze: 10 000 Alarme
alarme = [{"zeit": "12:00", "server": f"srv{n}", "meldung": f"Meldung {n}, Teil \"{n % 9}\"", "notiz": "-"} for n in range(10000)]
zeilen = schreibe_und_lies(schreibe_alarme, "gross.csv", alarme)
assert zeilen == erwartete_alarme(alarme), "Bei 10 000 Alarmen stimmt die Datei nicht."
