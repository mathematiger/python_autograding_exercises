# Automatisch erzeugt aus lehrkraft/muster/3_032_passwortregeln.py - nicht von Hand ändern.
# vorlage-hash: 7bc97c642e611697
# text-hash: 502ddb7deb6a3873
# thema: funktionen
# inhalt: Funktion baut Funktion

def erlaubt_vergleich(mindestlaenge, pflichtzeichen, passwort):
    """Vergleichslösung: Länge prüfen, dann mit einer Menge nach gemeinsamen Zeichen suchen."""
    if len(passwort) < mindestlaenge:
        return False
    return pflichtzeichen == "" or len(set(passwort) & set(pflichtzeichen)) > 0


def ergebnis_von(mindestlaenge, pflichtzeichen, passwort):
    """Baut einen Prüfer und wendet ihn an; beschreibt einen Fehler, statt abzubrechen."""
    pruefer = baue_pruefer(mindestlaenge, pflichtzeichen)
    if not callable(pruefer):
        return f"(baue_pruefer liefert {pruefer!r}, keine Funktion)"
    return pruefer(passwort)


def meldung(mindestlaenge, pflichtzeichen, passwort, ergebnis):
    """Baut die Fehlermeldung für einen Aufruf."""
    erwartet = erlaubt_vergleich(mindestlaenge, pflichtzeichen, passwort)
    return f"baue_pruefer({mindestlaenge}, {pflichtzeichen!r})({passwort!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."


# baue_pruefer liefert eine Funktion, kein Ergebnis
pruefer = baue_pruefer(8, "")
assert callable(pruefer), (
    f"baue_pruefer(8, '') liefert {pruefer!r}; erwartet war eine Funktion, die man mit einem Passwort aufrufen kann.\n"
    "Tipp: Definieren Sie in baue_pruefer eine innere Funktion und geben Sie sie ohne Klammern zurück: return pruefe."
)

# Das Beispiel aus der Aufgabe: Gäste-WLAN mit 8 Zeichen
ergebnis = ergebnis_von(8, "", "sonnenschein")
assert ergebnis is True, meldung(8, "", "sonnenschein", ergebnis)

# Zu kurze Passwörter werden abgelehnt
ergebnis = ergebnis_von(8, "", "kurz")
assert ergebnis is False, meldung(8, "", "kurz", ergebnis)

# Genau die Mindestlänge reicht
ergebnis = ergebnis_von(8, "", "acht1234")
assert ergebnis is True, meldung(8, "", "acht1234", ergebnis) + "\nTipp: Mindestens 8 Zeichen heißt: 8 Zeichen sind erlaubt."

# Die Mindestlänge kommt aus dem Parameter (nicht fest hinschreiben!)
ergebnisse = (ergebnis_von(12, "", "elf zeichen"), ergebnis_von(12, "", "zwoelf zeich"), ergebnis_von(3, "", "abc"))
assert ergebnisse == (False, True, True), (
    "baue_pruefer(12, '') mit 'elf zeichen' und 'zwoelf zeich' sowie baue_pruefer(3, '') mit 'abc' "
    f"ergeben {ergebnisse!r}, erwartet war (False, True, True)."
)

# Pflichtzeichen: ohne Ziffer abgelehnt, mit Ziffer angenommen
ergebnisse = (ergebnis_von(12, "0123456789", "sonnenschein"), ergebnis_von(12, "0123456789", "sonnenschein7"))
assert ergebnisse == (False, True), (
    "baue_pruefer(12, '0123456789') mit 'sonnenschein' und 'sonnenschein7' "
    f"ergeben {ergebnisse!r}, erwartet war (False, True)."
)

# Ein Pflichtzeichen an beliebiger Stelle genügt, auch ganz vorn
ergebnis = ergebnis_von(4, "!?#", "#abc")
assert ergebnis is True, meldung(4, "!?#", "#abc", ergebnis)

# Ein langes Passwort ohne Pflichtzeichen wird trotzdem abgelehnt
ergebnis = ergebnis_von(4, "!?#", "abcdefghijklmnop")
assert ergebnis is False, meldung(4, "!?#", "abcdefghijklmnop", ergebnis)

# Ein Pflichtzeichen hilft nicht, wenn das Passwort zu kurz ist
ergebnis = ergebnis_von(16, "!?#", "kurz!")
assert ergebnis is False, meldung(16, "!?#", "kurz!", ergebnis)

# Mehrere Prüfer behalten ihre eigene Richtlinie
gaeste = baue_pruefer(8, "")
admins = baue_pruefer(16, "!?#$%&")
mitarbeiter = baue_pruefer(12, "0123456789")
ergebnisse = (gaeste("passwort"), admins("passwort"), mitarbeiter("passwort12345"), admins("passwort12345!xyz"))
assert ergebnisse == (True, False, True, True), (
    "Nacheinander gebaut: gaeste = baue_pruefer(8, ''), admins = baue_pruefer(16, '!?#$%&'), "
    "mitarbeiter = baue_pruefer(12, '0123456789'). Dann ergeben gaeste('passwort'), admins('passwort'), "
    f"mitarbeiter('passwort12345'), admins('passwort12345!xyz') {ergebnisse!r}, erwartet war (True, False, True, True).\n"
    "Tipp: Jeder Prüfer soll die Werte benutzen, mit denen er gebaut wurde, nicht globale Variablen."
)

# Ränder: Mindestlänge 0 und leeres Passwort
ergebnisse = (ergebnis_von(0, "", ""), ergebnis_von(0, "1", ""), ergebnis_von(1, "", ""))
assert ergebnisse == (True, False, False), (
    "baue_pruefer(0, '')(''), baue_pruefer(0, '1')(''), baue_pruefer(1, '')('') "
    f"ergeben {ergebnisse!r}, erwartet war (True, False, False)."
)

# 2000 zufällige Richtlinien und Passwörter
zufall = Zufall(3032)
alphabet = "abcXYZ019!?# "
for _ in range(2000):
    mindestlaenge = zufall.randint(0, 12)
    pflichtzeichen = "".join(zufall.choice(alphabet) for _ in range(zufall.randint(0, 3)))
    passwort = "".join(zufall.choice(alphabet) for _ in range(zufall.randint(0, 14)))
    ergebnis = ergebnis_von(mindestlaenge, pflichtzeichen, passwort)
    assert ergebnis == erlaubt_vergleich(mindestlaenge, pflichtzeichen, passwort), meldung(mindestlaenge, pflichtzeichen, passwort, ergebnis)

# Obere Grenze: Mindestlänge 100, 40 Pflichtzeichen, Passwörter mit 1000 Zeichen
pflicht = "".join(chr(code) for code in range(33, 73))
pruefer = baue_pruefer(100, pflicht)
ergebnisse = (pruefer("a" * 1000), pruefer("a" * 999 + "H"), pruefer("!" * 99))
assert ergebnisse == (False, True, False), (
    "Mit baue_pruefer(100, <40 Sonderzeichen, Ziffern und Großbuchstaben von ! bis H>) ergeben 'a' * 1000, "
    f"'a' * 999 + 'H' und '!' * 99 {ergebnisse!r}, erwartet war (False, True, False)."
)
