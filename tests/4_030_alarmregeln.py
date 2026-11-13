# Automatisch erzeugt aus lehrkraft/muster/4_030_alarmregeln.py - nicht von Hand ändern.
# vorlage-hash: 47bd0cdcd624939b
# text-hash: 98d80ffe313c6897
# thema: funktionen
# inhalt: Klassen- und Methodendekoratoren

def versuche(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


# Die vorgegebenen Klassen stehen in REGELN
assert "Schwellwert" in REGELN and "Dauerlast" in REGELN, (
    f"REGELN ist {REGELN!r}; erwartet waren die Einträge 'Schwellwert' und 'Dauerlast'.\n"
    "Tipp: Tragen Sie in registriere REGELN[klasse.__name__] = klasse ein."
)

# registriere gibt die Klasse unverändert zurück
class Probe:
    def ausloesen(self, werte):
        return False

ergebnis, fehler = versuche(registriere, Probe)
assert ergebnis is Probe, (
    f"registriere(Probe) liefert {ergebnis!r}" + (f" (Ausnahme {fehler!r})" if fehler else "")
    + ", erwartet war die Klasse Probe selbst.\nTipp: Geben Sie am Ende return klasse zurück, sonst ist die Klasse danach None."
)

# Eine neue Klasse mit @registriere landet in REGELN und bleibt benutzbar
@registriere
class Ausreisser:
    """Alarm, wenn ein Wert mehr als 50 vom ersten abweicht."""

    @ohne_ausfaelle
    def ausloesen(self, werte):
        return any(abs(wert - werte[0]) > 50 for wert in werte)

assert REGELN.get("Ausreisser") is Ausreisser and Ausreisser().ausloesen([10, None, 70]) is True, (
    f"Nach @registriere class Ausreisser ist REGELN.get('Ausreisser') {REGELN.get('Ausreisser')!r} und "
    "Ausreisser().ausloesen([10, None, 70]) sollte True sein.\n"
    "Tipp: Beide Dekoratoren müssen etwas zurückgeben: registriere die Klasse, ohne_ausfaelle die innere Funktion."
)

# Ohne Methode ausloesen: TypeError
class OhneMethode:
    pass

class FalschesAttribut:
    ausloesen = 42

for klasse in [OhneMethode, FalschesAttribut]:
    ergebnis, fehler = versuche(registriere, klasse)
    assert isinstance(fehler, TypeError) and klasse.__name__ not in REGELN, (
        f"registriere({klasse.__name__}) muss einen TypeError auslösen (keine aufrufbare Methode ausloesen) und "
        f"die Klasse nicht eintragen; Ausnahme: {fehler!r}, eingetragen: {klasse.__name__ in REGELN}.\n"
        "Tipp: callable(getattr(klasse, 'ausloesen', None)) prüft, ob es die Methode gibt."
    )

# Ein doppelter Name löst ValueError aus, die alte Klasse bleibt
alte = REGELN["Schwellwert"]

class Schwellwert:
    def ausloesen(self, werte):
        return True

ergebnis, fehler = versuche(registriere, Schwellwert)
Schwellwert = alte
assert isinstance(fehler, ValueError) and REGELN["Schwellwert"] is alte, (
    "Eine zweite Klasse namens Schwellwert muss bei registriere einen ValueError auslösen, und in REGELN bleibt "
    f"die alte Klasse; Ausnahme: {fehler!r}, REGELN['Schwellwert'] ist die alte: {REGELN['Schwellwert'] is alte}.\n"
    "Tipp: Prüfen Sie zuerst, ob der Name schon in REGELN steht, und tragen Sie erst danach ein."
)

# Das Beispiel: Schwellwert ignoriert ausgefallene Messungen
ergebnis, fehler = versuche(Schwellwert(80).ausloesen, [75, None, 82])
assert ergebnis is True, (
    f"Schwellwert(80).ausloesen([75, None, 82]) ergibt {ergebnis!r}" + (f" (Ausnahme {fehler!r})" if fehler else "")
    + ", erwartet war True.\nTipp: Entfernen Sie in ohne_ausfaelle alle None, bevor Sie die Methode aufrufen."
)

# Das Beispiel: Dauerlast zählt nur echte Messungen
for werte, erwartet in [([71, None, 75, 90], True), ([71, 75, 60, None], False), ([90, 95, None], False)]:
    ergebnis, fehler = versuche(Dauerlast(70, 3).ausloesen, werte)
    assert ergebnis is erwartet, (
        f"Dauerlast(70, 3).ausloesen({werte!r}) ergibt {ergebnis!r}" + (f" (Ausnahme {fehler!r})" if fehler else "")
        + f", erwartet war {erwartet}. Ausgefallene Messungen (None) zählen nicht mit."
    )

# Die übergebene Liste bleibt unverändert
werte = [75, None, 82, None]
Schwellwert(80).ausloesen(werte)
assert werte == [75, None, 82, None], (
    f"Nach Schwellwert(80).ausloesen([75, None, 82, None]) ist die Liste {werte!r}; sie soll unverändert bleiben.\n"
    "Tipp: Bauen Sie eine neue Liste, statt mit remove aus der übergebenen zu löschen."
)

# Leere Liste und nur Ausfälle
for werte in [[], [None, None]]:
    ergebnis, fehler = versuche(Schwellwert(0).ausloesen, werte)
    assert ergebnis is False, (
        f"Schwellwert(0).ausloesen({werte!r}) ergibt {ergebnis!r}" + (f" (Ausnahme {fehler!r})" if fehler else "")
        + ", erwartet war False."
    )

# Der Wert 0 ist eine echte Messung, kein Ausfall
ergebnis, fehler = versuche(Dauerlast(-5, 2).ausloesen, [0, 0])
assert ergebnis is True, (
    f"Dauerlast(-5, 2).ausloesen([0, 0]) ergibt {ergebnis!r}, erwartet war True.\n"
    "Tipp: Entfernen Sie nur None (wert is not None), nicht alles, was als falsch gilt."
)

# Name und Docstring der Methode bleiben erhalten
methode = Schwellwert.ausloesen
assert methode.__name__ == "ausloesen" and methode.__doc__ == "True, wenn ein Wert über der Grenze liegt.", (
    f"Schwellwert.ausloesen heißt {methode.__name__!r} mit Docstring {methode.__doc__!r}; erwartet waren "
    "'ausloesen' und der Docstring des Originals.\nTipp: Schreiben Sie @functools.wraps(methode) über die innere Funktion."
)

# Jedes Objekt behält seine eigenen Attribute (self wird durchgereicht)
niedrig = Schwellwert(10)
hoch = Schwellwert(100)
ergebnis = (niedrig.ausloesen([50]), hoch.ausloesen([50]))
assert ergebnis == (True, False), (
    f"Schwellwert(10).ausloesen([50]) und Schwellwert(100).ausloesen([50]) ergeben {ergebnis!r}, erwartet war (True, False)."
)

# Viele zufällige Messreihen mit Ausfällen
zufall = Zufall(4030)
for _ in range(500):
    werte = [zufall.choice([None, zufall.randint(-20, 120), zufall.uniform(-10**6, 10**6)]) for _ in range(zufall.randint(0, 12))]
    grenze = zufall.randint(-10, 110)
    anzahl = zufall.randint(1, 4)
    echte = [wert for wert in werte if wert is not None]
    erwartet_schwelle = max(echte, default=grenze) > grenze
    erwartet_dauer = len(echte) >= anzahl and min(echte[len(echte) - anzahl :]) > grenze
    kopie = list(werte)
    ergebnis = (Schwellwert(grenze).ausloesen(werte), Dauerlast(grenze, anzahl).ausloesen(werte))
    assert ergebnis == (erwartet_schwelle, erwartet_dauer) and werte == kopie, (
        f"Für werte = {kopie!r}: Schwellwert({grenze}).ausloesen und Dauerlast({grenze}, {anzahl}).ausloesen ergeben "
        f"{ergebnis!r}, erwartet war {(erwartet_schwelle, erwartet_dauer)!r}"
        + ("" if werte == kopie else f"; die Liste wurde verändert zu {werte!r}") + "."
    )

# Obere Grenze: 100 000 Messungen, jede dritte ausgefallen
werte = [None if nummer % 3 == 0 else nummer % 1000 for nummer in range(100000)]
ergebnis = (Schwellwert(998).ausloesen(werte), Dauerlast(990, 2).ausloesen(werte))
assert ergebnis == (True, True), (
    f"Bei 100 000 Messungen (jede dritte None, sonst nummer % 1000) ergeben Schwellwert(998) und Dauerlast(990, 2) "
    f"{ergebnis!r}, erwartet war (True, True)."
)
