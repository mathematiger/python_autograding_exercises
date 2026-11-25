# Automatisch erzeugt aus lehrkraft/muster/3_049_datenbanklog.py - nicht von Hand ändern.
# vorlage-hash: aad6c7f81b499315
# text-hash: 8b7cb1e18a1ced14
# thema: texte_zahlen
# inhalt: Übung: Logdatei auswerten

import os
import shutil
import tempfile

ORDNER = tempfile.mkdtemp(prefix="aufgabe_3049_")
BEISPIEL = (
    "2026-11-20 08:00:01 INFO Datenbank gestartet\n"
    "2026-11-20 08:15:02 WARN Langsame Abfrage: 2.4 s\n"
    "2026-11-20 08:15:09 INFO Sicherung begonnen\n"
    "2026-11-20 08:20:44 ERROR Verbindung abgelehnt: zu viele Clients\n"
    "kaputte Zeile\n"
    "2026-11-20 08:21:00 WARN Langsame Abfrage: 3.1 s\n"
    "2026-11-20 08:30:12 INFO Sicherung beendet\n"
    "\n"
    "2026-11-20 08:31:00 DEBUG Puffer geleert\n"
)
BERICHT_BEISPIEL = "INFO: 3\nWARN: 2\nERROR: 1\nUngültige Zeilen: 2\n"
GRADE = ["ERROR", "WARN", "INFO"]
zaehler = [0]


def neuer_pfad(name):
    """Ein neuer Pfad im Testordner, den es noch nicht gibt."""
    zaehler[0] += 1
    return os.path.join(ORDNER, f"{zaehler[0]}_{name}")


def logdatei(inhalt):
    """Legt eine Logdatei mit genau diesem Inhalt an und gibt ihren Pfad zurück."""
    pfad = neuer_pfad("db.log")
    with open(pfad, "w", encoding="utf-8", newline="") as datei:
        datei.write(inhalt)
    return pfad


def inhalt_von(pfad):
    """Der Inhalt der Datei als Text, oder eine Beschreibung, warum er fehlt."""
    try:
        with open(pfad, encoding="utf-8") as datei:
            return datei.read()
    except FileNotFoundError:
        return "(Die Datei gibt es nicht.)"
    except UnicodeDecodeError:
        return "(Die Datei ist nicht in UTF-8 gespeichert.)"


def aufruf(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_zaehlung(inhalt):
    """Vergleichslösung: zerlegt den Text selbst, ohne Datei."""
    zaehlung = {"ERROR": 0, "WARN": 0, "INFO": 0, "ungueltig": 0}
    for zeile in inhalt.split("\n"):
        if zeile.strip() == "":
            continue
        teile = zeile.split()
        if len(teile) > 2 and teile[2] in ("ERROR", "WARN", "INFO"):
            zaehlung[teile[2]] = zaehlung[teile[2]] + 1
        else:
            zaehlung["ungueltig"] = zaehlung["ungueltig"] + 1
    return zaehlung


def vergleich_bericht(zaehlung):
    """Vergleichslösung: sucht dreimal den Schweregrad mit der größten Anzahl."""
    uebrig = list(GRADE)
    text = ""
    while uebrig:
        bester = uebrig[0]
        for grad in uebrig:
            if zaehlung[grad] > zaehlung[bester]:
                bester = grad
        text += f"{bester}: {zaehlung[bester]}\n"
        uebrig.remove(bester)
    return text + f"Ungültige Zeilen: {zaehlung['ungueltig']}\n"


def bericht_zu(zaehlung):
    """Ruft schreibe_bericht mit einem neuen Pfad auf und gibt den Inhalt der Datei zurück."""
    pfad = neuer_pfad("bericht.txt")
    fehler = aufruf(schreibe_bericht, pfad, dict(zaehlung))
    if isinstance(fehler, str):
        return f"(Abbruch: {fehler})"
    return inhalt_von(pfad)


def kurz(inhalt):
    """Der Inhalt einer Logdatei für Meldungen, bei langen Dateien gekürzt."""
    if len(inhalt) > 600:
        return repr(inhalt[:600]) + " …"
    return repr(inhalt)


def meldung_zaehlung(inhalt, ergebnis, tipp=""):
    """Fehlermeldung für zaehle_eintraege."""
    return f"Für die Logdatei\n{kurz(inhalt)}\nergibt zaehle_eintraege {ergebnis!r},\nerwartet war {vergleich_zaehlung(inhalt)!r}.{tipp}"


def meldung_bericht(zaehlung, inhalt, tipp=""):
    """Fehlermeldung für schreibe_bericht."""
    return f"Nach schreibe_bericht(pfad, {zaehlung}) enthält die Datei\n{inhalt!r}\nerwartet war\n{vergleich_bericht(zaehlung)!r}{tipp}"


# zaehle_eintraege im Beispiel: ein Dictionary mit den vier Schlüsseln
ergebnis = aufruf(zaehle_eintraege, logdatei(BEISPIEL))
assert isinstance(ergebnis, dict) and sorted(ergebnis) == ["ERROR", "INFO", "WARN", "ungueltig"], meldung_zaehlung(
    BEISPIEL, ergebnis, '\nTipp: Beginnen Sie mit {"ERROR": 0, "WARN": 0, "INFO": 0, "ungueltig": 0}.'
)

# zaehle_eintraege im Beispiel: die gültigen Einträge je Schweregrad
assert isinstance(ergebnis, dict) and [ergebnis.get(grad) for grad in GRADE] == [1, 2, 3], meldung_zaehlung(
    BEISPIEL, ergebnis, "\nTipp: zeile.split() zerlegt die Zeile; der Schweregrad ist der dritte Teil, teile[2]."
)

# zaehle_eintraege im Beispiel: zwei ungültige Zeilen, die leere zählt nicht
assert ergebnis == vergleich_zaehlung(BEISPIEL), meldung_zaehlung(
    BEISPIEL, ergebnis, "\nTipp: Leere Zeilen überspringen, alles andere ohne gültigen Schweregrad zählt als ungültig."
)

# zaehle_eintraege mit einer anderen Logdatei, letzte Zeile ohne Zeilenumbruch (nicht fest hinschreiben!)
inhalt = (
    "2026-11-21 09:00:00 ERROR Platte voll\n"
    "2026-11-21 09:00:05 ERROR Schreiben fehlgeschlagen\n"
    "2026-11-21 09:01:00 INFO Speicher freigegeben"
)
ergebnis = aufruf(zaehle_eintraege, logdatei(inhalt))
assert ergebnis == vergleich_zaehlung(inhalt), meldung_zaehlung(inhalt, ergebnis)

# zaehle_eintraege: Zeilen nur aus Leerraum zählen nicht, Tabulatoren trennen auch
inhalt = "   \n2026-11-21\t09:00:00\tWARN\tReplikation verzögert\n\t\n\n"
ergebnis = aufruf(zaehle_eintraege, logdatei(inhalt))
assert ergebnis == vergleich_zaehlung(inhalt), meldung_zaehlung(inhalt, ergebnis, "\nTipp: split() ohne Argument trennt an jedem Leerraum.")

# zaehle_eintraege: unbekannter oder klein geschriebener Schweregrad und zu kurze Zeilen sind ungültig
inhalt = "2026-11-21 09:00:00 warn klein\n2026-11-21 09:00:00 FATAL Absturz\n2026-11-21 09:00:00\nWARN\n"
ergebnis = aufruf(zaehle_eintraege, logdatei(inhalt))
assert ergebnis == vergleich_zaehlung(inhalt), meldung_zaehlung(
    inhalt, ergebnis, "\nTipp: Prüfen Sie zuerst len(teile) >= 3, dann, ob teile[2] einer der drei Schweregrade ist."
)

# zaehle_eintraege: genau drei Teile ohne Meldung sind gültig, der Schweregrad zählt nur an dritter Stelle
inhalt = "2026-11-21 09:00:00 INFO\nERROR 2026-11-21 09:00:00 Text\n2026-11-21 09:00 Text ERROR\n"
ergebnis = aufruf(zaehle_eintraege, logdatei(inhalt))
assert ergebnis == vergleich_zaehlung(inhalt), meldung_zaehlung(inhalt, ergebnis, "\nTipp: Schauen Sie nur auf teile[2], nicht, ob ERROR irgendwo vorkommt.")

# zaehle_eintraege: leere Logdatei
ergebnis = aufruf(zaehle_eintraege, logdatei(""))
assert ergebnis == vergleich_zaehlung(""), meldung_zaehlung("", ergebnis)

# zaehle_eintraege: Umlaute in den Meldungen
inhalt = "2026-11-21 10:00:00 WARN Prüfsumme weicht ab: Tabelle Bestände\n"
ergebnis = aufruf(zaehle_eintraege, logdatei(inhalt))
assert ergebnis == vergleich_zaehlung(inhalt), meldung_zaehlung(inhalt, ergebnis, '\nTipp: Öffnen Sie die Datei mit encoding="utf-8".')

def zeilen_locker(text):
    """Gibt die nicht leeren Zeilen des Texts vergleichbar gemacht zurück (Form und Wortlaut egal)."""
    return [vergleichbar(zeile) for zeile in text.splitlines() if zeile.strip()]


# schreibe_bericht im Beispiel: die richtigen Zeilen (Reihenfolge und Leerzeichen noch egal)
zaehlung = {"ERROR": 1, "WARN": 2, "INFO": 3, "ungueltig": 2}
inhalt = bericht_zu(zaehlung)
zeilen = sorted(vergleichbar(zeile) for zeile in inhalt.splitlines() if zeile.strip())
assert zeilen == sorted(vergleichbar(zeile) for zeile in BERICHT_BEISPIEL.splitlines()), meldung_bericht(
    zaehlung, inhalt, '\nTipp: with open(berichtpfad, "w", encoding="utf-8") und datei.write(f"{grad}: {anzahl}\\n").'
)

# schreibe_bericht im Beispiel: die größte Anzahl zuerst, die ungültigen am Schluss
zeilen = [vergleichbar(zeile) for zeile in inhalt.splitlines() if zeile.strip()]
assert zeilen == [vergleichbar(zeile) for zeile in BERICHT_BEISPIEL.splitlines()], meldung_bericht(
    zaehlung, inhalt, "\nTipp: sorted(..., key=lambda grad: -zaehlung[grad]) sortiert die größte Anzahl nach vorn."
)

# schreibe_bericht im Beispiel: genau diese Form mit Doppelpunkt, Leerzeichen und Zeilenumbrüchen
assert inhalt == BERICHT_BEISPIEL, meldung_bericht(
    zaehlung, inhalt, '\nTipp: Jede Zeile sieht aus wie "INFO: 3" und endet mit "\\n", auch die letzte; keine Leerzeile dazwischen.'
)

# schreibe_bericht mit anderen Anzahlen (nicht fest hinschreiben!)
zaehlung = {"ERROR": 40, "WARN": 7, "INFO": 1200, "ungueltig": 0}
inhalt = bericht_zu(zaehlung)
assert zeilen_locker(inhalt) == zeilen_locker(vergleich_bericht(zaehlung)), meldung_bericht(zaehlung, inhalt)

# schreibe_bericht: bei gleicher Anzahl ERROR vor WARN vor INFO
zaehlung = {"ERROR": 5, "WARN": 5, "INFO": 5, "ungueltig": 1}
inhalt = bericht_zu(zaehlung)
assert zeilen_locker(inhalt) == zeilen_locker(vergleich_bericht(zaehlung)), meldung_bericht(
    zaehlung, inhalt, "\nTipp: Ein Tupel als key, etwa (-zaehlung[grad], SCHWEREGRADE.index(grad)), entscheidet Gleichstände."
)

# schreibe_bericht: Gleichstand nur zwischen zwei Schweregraden
zaehlung = {"ERROR": 2, "WARN": 9, "INFO": 2, "ungueltig": 3}
inhalt = bericht_zu(zaehlung)
assert zeilen_locker(inhalt) == zeilen_locker(vergleich_bericht(zaehlung)), meldung_bericht(zaehlung, inhalt)

# schreibe_bericht: Schweregrade mit 0 stehen auch im Bericht
zaehlung = {"ERROR": 0, "WARN": 0, "INFO": 0, "ungueltig": 0}
inhalt = bericht_zu(zaehlung)
assert zeilen_locker(inhalt) == zeilen_locker(vergleich_bericht(zaehlung)), meldung_bericht(zaehlung, inhalt)

# schreibe_bericht ersetzt einen alten Bericht
pfad = neuer_pfad("bericht.txt")
with open(pfad, "w", encoding="utf-8") as datei:
    datei.write("alter Bericht\nERROR: 99\n")
zaehlung = {"ERROR": 1, "WARN": 2, "INFO": 3, "ungueltig": 2}
aufruf(schreibe_bericht, pfad, zaehlung)
assert zeilen_locker(inhalt_von(pfad)) == zeilen_locker(BERICHT_BEISPIEL), meldung_bericht(zaehlung, inhalt_von(pfad), '\nTipp: Der Modus "w" ersetzt den alten Inhalt.')

# werte_log_aus im Beispiel: sechs gültige Einträge
logpfad = logdatei(BEISPIEL)
berichtpfad = neuer_pfad("bericht.txt")
ergebnis = aufruf(werte_log_aus, logpfad, berichtpfad)
assert ergebnis == 6, (
    f"werte_log_aus für die Beispieldatei ergibt {ergebnis!r}, erwartet war 6.\n"
    "Tipp: Gültig sind die Einträge bei ERROR, WARN und INFO, nicht die ungültigen Zeilen."
)

# werte_log_aus im Beispiel: der Bericht steht in der Datei
assert zeilen_locker(inhalt_von(berichtpfad)) == zeilen_locker(BERICHT_BEISPIEL), (
    f"Nach werte_log_aus enthält die Berichtsdatei {inhalt_von(berichtpfad)!r}, erwartet war {BERICHT_BEISPIEL!r}.\n"
    "Tipp: Rufen Sie schreibe_bericht(berichtpfad, zaehlung) mit dem Ergebnis von zaehle_eintraege auf."
)

# werte_log_aus benutzt die beiden anderen Funktionen
assert verwendet("zaehle_eintraege") and verwendet("schreibe_bericht"), (
    "werte_log_aus soll zaehle_eintraege und schreibe_bericht aufrufen, statt alles noch einmal zu schreiben."
)

# Viele zufällige Logdateien
zufall = Zufall(3049)
bausteine = ["INFO", "WARN", "ERROR", "DEBUG", "info", "Abfrage", "2026-11-22", "08:00:00", "Fehler:"]
for _ in range(80):
    zeilen = []
    for _ in range(zufall.randint(0, 12)):
        art = zufall.random()
        if art < 0.6:
            zeilen.append(f"2026-11-22 08:{zufall.randint(10, 59)}:00 {zufall.choice(GRADE)} Meldung {zufall.randint(1, 9)}")
        elif art < 0.75:
            zeilen.append(zufall.choice(["", "  ", "\t"]))
        else:
            zeilen.append(" ".join(zufall.choice(bausteine) for _ in range(zufall.randint(1, 5))))
    inhalt = "\n".join(zeilen) + zufall.choice(["", "\n"])
    logpfad = logdatei(inhalt)
    berichtpfad = neuer_pfad("bericht.txt")
    ergebnis = aufruf(werte_log_aus, logpfad, berichtpfad)
    erwartet = vergleich_zaehlung(inhalt)
    gueltig = erwartet["ERROR"] + erwartet["WARN"] + erwartet["INFO"]
    assert ergebnis == gueltig and zeilen_locker(inhalt_von(berichtpfad)) == zeilen_locker(vergleich_bericht(erwartet)), (
        f"Für die Logdatei\n{kurz(inhalt)}\nergibt werte_log_aus {ergebnis!r} und den Bericht {inhalt_von(berichtpfad)!r},\n"
        f"erwartet waren {gueltig} und {vergleich_bericht(erwartet)!r}."
    )

# Obere Grenze: 100 000 Zeilen
zeilen = []
for nummer in range(100000):
    if nummer % 997 == 0:
        zeilen.append("Zeile ohne Schweregrad")
    else:
        zeilen.append(f"2026-11-22 09:{nummer % 60:02d}:00 {GRADE[nummer % 7 % 3]} Abfrage {nummer} beendet")
inhalt = "\n".join(zeilen) + "\n"
logpfad = logdatei(inhalt)
berichtpfad = neuer_pfad("bericht.txt")
ergebnis = aufruf(werte_log_aus, logpfad, berichtpfad)
erwartet = vergleich_zaehlung(inhalt)
assert ergebnis == 100000 - erwartet["ungueltig"] and zeilen_locker(inhalt_von(berichtpfad)) == zeilen_locker(vergleich_bericht(erwartet)), (
    f"Bei 100 000 Zeilen ergibt werte_log_aus {ergebnis!r} und den Bericht {inhalt_von(berichtpfad)!r},\n"
    f"erwartet waren {100000 - erwartet['ungueltig']} und {vergleich_bericht(erwartet)!r}."
)

shutil.rmtree(ORDNER, ignore_errors=True)  # aufräumen
