# Automatisch erzeugt aus lehrkraft/muster/1_040_auslastung.py - nicht von Hand ändern.
# vorlage-hash: 010e20895bef9f4c
# text-hash: 77a2c96c9bfdd6f4
# thema: funktionen
# inhalt: Übung: Funktionen

EINGABEN = ["80", "45", "92", "80", "81", "stop"]


def zeile(minute, wert, grenze):
    """Vergleichslösung für eine Zeile, nur für die Tests."""
    if wert > grenze:
        return f"Minute {minute}: {wert} % ALARM"
    return f"Minute {minute}: {wert} % ok"


def erwartete_ausgabe(grenze, werte):
    """Baut die erwartete Ausgabe des ganzen Programms."""
    zeilen = [zeile(nummer + 1, wert, grenze) for nummer, wert in enumerate(werte)]
    alarme = len([wert for wert in werte if wert > grenze])
    zeilen.append(f"Alarme: {alarme} von {len(werte)}")
    return "\n".join(zeilen)


def lauf(grenze, werte):
    """Startet das Programm mit der Grenze und den Messwerten, dann stop."""
    return starte(str(grenze), *[str(wert) for wert in werte], "stop")


def meldung(grenze, werte, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei der Grenze {grenze} und den Messwerten {werte} erwartet:\n{erwartete_ausgabe(grenze, werte)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}"
    )


def tipp_bei_none(ergebnis, tipp):
    """Gibt den Tipp mit Zeilenumbruch zurück, wenn ergebnis None ist, sonst einen leeren Text."""
    if ergebnis is None:
        return f"\nTipp: {tipp}"
    return ""


TIPP_TEXT = "statuszeile liefert None. Geben Sie den Text mit return zurück statt mit print."
TIPP_ANZAHL = (
    "anzahl_alarme liefert None: return fehlt oder steht falsch. Es gehört nach der Schleife, "
    "nicht eingerückt in die Schleife."
)


def benutzt_ist_alarm(funktion, *argumente):
    """Ruft funktion(*argumente) auf und gibt zurück, ob dabei ist_alarm aufgerufen wurde."""
    namensraum = globals()
    echtes_ist_alarm = namensraum["ist_alarm"]
    aufrufe = []

    def zaehlendes_ist_alarm(*args, **kwargs):
        """Merkt sich den Aufruf und gibt das Ergebnis der echten Funktion zurück."""
        aufrufe.append(args)
        return echtes_ist_alarm(*args, **kwargs)

    namensraum["ist_alarm"] = zaehlendes_ist_alarm
    try:
        funktion(*argumente)
    finally:
        namensraum["ist_alarm"] = echtes_ist_alarm
    return len(aufrufe) > 0


# ist_alarm: 92 liegt über der Grenze 80
ergebnis = ist_alarm(92, 80)
assert ergebnis == True, (
    f"ist_alarm(92, 80) ergibt {ergebnis!r}, erwartet war True."
    + ("\nTipp: Geben Sie das Ergebnis mit return zurück." if ergebnis is None else "")
)

# ist_alarm: 45 liegt nicht über der Grenze 80
ergebnis = ist_alarm(45, 80)
assert ergebnis == False, f"ist_alarm(45, 80) ergibt {ergebnis!r}, erwartet war False."

# ist_alarm: ein Wert genau auf der Grenze ist kein Alarm
ergebnis = ist_alarm(80, 80)
assert ergebnis == False, (
    f"ist_alarm(80, 80) ergibt {ergebnis!r}, erwartet war False (genau auf der Grenze ist noch kein Alarm).\n"
    "Tipp: Benutzen Sie > statt >=."
)

# ist_alarm: die Reihenfolge der Parameter stimmt
ergebnis = ist_alarm(30, 20)
assert ergebnis == True, f"ist_alarm(30, 20) ergibt {ergebnis!r}, erwartet war True (der Wert 30 liegt über der Grenze 20)."

# statuszeile mit Alarm
text = statuszeile(2, 92, 80)
assert vergleichbar(str(text)) == vergleichbar("Minute 2: 92 % ALARM"), (
    f'statuszeile(2, 92, 80) ergibt {text!r}, erwartet war "Minute 2: 92 % ALARM".' + tipp_bei_none(text, TIPP_TEXT)
)

# statuszeile ohne Alarm
text = statuszeile(1, 45, 80)
assert vergleichbar(str(text)) == vergleichbar("Minute 1: 45 % ok"), (
    f'statuszeile(1, 45, 80) ergibt {text!r}, erwartet war "Minute 1: 45 % ok".' + tipp_bei_none(text, TIPP_TEXT)
)

# statuszeile genau auf der Grenze
text = statuszeile(3, 80, 80)
assert vergleichbar(str(text)) == vergleichbar("Minute 3: 80 % ok"), (
    f'statuszeile(3, 80, 80) ergibt {text!r}, erwartet war "Minute 3: 80 % ok".' + tipp_bei_none(text, TIPP_TEXT)
)

# statuszeile benutzt ist_alarm
assert benutzt_ist_alarm(statuszeile, 2, 92, 80), (
    "statuszeile ruft ist_alarm nicht auf.\n"
    "Tipp: Schreiben Sie den Vergleich nicht noch einmal hin, sondern fragen Sie if ist_alarm(wert, grenze): …"
)

# anzahl_alarme im Beispiel
ergebnis = anzahl_alarme([45, 92, 80, 81], 80)
assert ergebnis == 2, (
    f"anzahl_alarme([45, 92, 80, 81], 80) ergibt {ergebnis!r}, erwartet war 2." + tipp_bei_none(ergebnis, TIPP_ANZAHL)
)

# anzahl_alarme mit anderen Werten (nicht fest hinschreiben!)
ergebnis = anzahl_alarme([10, 60, 70, 55, 90], 50)
assert ergebnis == 4, (
    f"anzahl_alarme([10, 60, 70, 55, 90], 50) ergibt {ergebnis!r}, erwartet war 4." + tipp_bei_none(ergebnis, TIPP_ANZAHL)
)

# anzahl_alarme mit einer leeren Liste
ergebnis = anzahl_alarme([], 50)
assert ergebnis == 0, (
    f"anzahl_alarme([], 50) ergibt {ergebnis!r}, erwartet war 0." + tipp_bei_none(ergebnis, TIPP_ANZAHL)
)

# anzahl_alarme benutzt ist_alarm
assert benutzt_ist_alarm(anzahl_alarme, [45, 92, 80, 81], 80), (
    "anzahl_alarme soll die Liste mit for durchgehen und für jeden Wert ist_alarm aufrufen.\n"
    "Tipp: for wert in werte: if ist_alarm(wert, grenze): …"
)

# Das Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe(80, [45, 92, 80, 81])), meldung(80, [45, 92, 80, 81], AUSGABE)

# Andere Grenze und andere Messwerte
werte = [99, 12, 70, 71, 100]
ausgabe = lauf(70, werte)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(70, werte)), meldung(70, werte, ausgabe)

# Gleich stop: keine Messwerte
ausgabe = lauf(50, [])
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(50, [])), meldung(50, [], ausgabe)

# Ränder: Grenze 0 und Grenze 100
for grenze, werte in [(0, [0, 1, 100]), (100, [100, 0, 99])]:
    ausgabe = lauf(grenze, werte)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(grenze, werte)), meldung(grenze, werte, ausgabe)

# Viele zufällige Messreihen
zufall = Zufall(1040)
for _ in range(40):
    grenze = zufall.randint(0, 100)
    werte = [zufall.randint(0, 100) for _ in range(zufall.randint(0, 8))]
    ausgabe = lauf(grenze, werte)
    assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(grenze, werte)), meldung(grenze, werte, ausgabe)

# Obere Grenze: 60 Messwerte
werte = [zufall.randint(0, 100) for _ in range(60)]
ausgabe = lauf(75, werte)
assert vergleichbar(ausgabe) == vergleichbar(erwartete_ausgabe(75, werte)), meldung(75, werte, ausgabe)
