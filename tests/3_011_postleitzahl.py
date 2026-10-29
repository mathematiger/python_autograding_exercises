# Automatisch erzeugt aus lehrkraft/muster/3_011_postleitzahl.py - nicht von Hand ändern.
# vorlage-hash: 7bd4bde814c5ba6c
# thema: fehler
# inhalt: Testfälle schreiben

faelle = testfaelle()

# testfaelle() gibt eine nicht leere Liste von Tupeln (eingabe, erwartet) zurück
form_ok = isinstance(faelle, list) and 1 <= len(faelle) <= 100
for fall in faelle if form_ok else []:
    if not (isinstance(fall, tuple) and len(fall) == 2 and isinstance(fall[0], str) and isinstance(fall[1], bool)):
        form_ok = False
assert form_ok, (
    f"testfaelle() ergibt {faelle!r}; erwartet war eine Liste mit 1 bis 100 Tupeln (eingabe, erwartet), "
    'zum Beispiel [("33098", True), ("3309", False)]. eingabe ist ein Text, erwartet True oder False.'
)

# Alle Testfälle stimmen mit der richtigen ist_plz überein
falsche_faelle = []
for eingabe, erwartet in faelle:
    if ist_plz(eingabe) != erwartet:
        falsche_faelle.append((eingabe, erwartet))
assert falsche_faelle == [], (
    f"Diese Testfälle passen nicht zur Beschreibung: {falsche_faelle!r}. "
    f"Die richtige ist_plz liefert dafür {[ist_plz(eingabe) for eingabe, _ in falsche_faelle]!r}."
)


# Hilfsfunktion für die folgenden Tests: Scheitert eine Funktion an einem der Testfälle?
def entdeckt(funktion):
    """True, wenn funktion bei mindestens einem Testfall ein falsches Ergebnis liefert oder eine Ausnahme auslöst."""
    for eingabe, erwartet in faelle:
        try:
            if funktion(eingabe) != erwartet:
                return True
        except Exception:
            return True
    return False


# Fehlerhafte Fassungen von ist_plz, jeweils mit einem Hinweis, welcher Testfall fehlt
def immer_wahr(eingabe):
    """Fehler: liefert immer True."""
    return True


def ab_vier_ziffern(eingabe):
    """Fehler: nimmt auch vier Ziffern an."""
    plz = eingabe.strip(" ")
    return 4 <= len(plz) <= 5 and plz.isdigit()


def auch_sechs_ziffern(eingabe):
    """Fehler: nimmt auch sechs Ziffern an."""
    plz = eingabe.strip(" ")
    return 5 <= len(plz) <= 6 and plz.isdigit()


def ohne_strip(eingabe):
    """Fehler: entfernt die Leerzeichen am Rand nicht."""
    return len(eingabe) == 5 and eingabe.isdigit()


def leerzeichen_ueberall_weg(eingabe):
    """Fehler: entfernt auch Leerzeichen in der Mitte."""
    plz = eingabe.replace(" ", "")
    return len(plz) == 5 and plz.isdigit()


def nur_laenge(eingabe):
    """Fehler: prüft nur die Länge, nicht die Zeichen."""
    return len(eingabe.strip(" ")) == 5


def als_zahl(eingabe):
    """Fehler: wandelt in eine Zahl um, dabei geht die 0 am Anfang verloren."""
    try:
        return 10000 <= int(eingabe) <= 99999
    except ValueError:
        return False


def erstes_zeichen(eingabe):
    """Fehler: liest das erste Zeichen, auch wenn es keines gibt."""
    plz = eingabe.strip(" ")
    if plz[0] == "0" and len(plz) == 5:
        return plz.isdigit()
    return len(plz) == 5 and plz.isdigit()


def leer_ist_gueltig(eingabe):
    """Fehler: hält die leere Eingabe für gültig."""
    plz = eingabe.strip(" ")
    if plz == "":
        return True
    return len(plz) == 5 and plz.isdigit()


FEHLERHAFTE = [
    (immer_wahr, "immer True liefert", "einen Testfall, bei dem False herauskommen muss"),
    (ab_vier_ziffern, "auch vier Ziffern annimmt", "einen Testfall mit vier Ziffern"),
    (auch_sechs_ziffern, "auch sechs Ziffern annimmt", "einen Testfall mit sechs Ziffern"),
    (ohne_strip, "Leerzeichen am Rand nicht zulässt", "einen Testfall mit Leerzeichen am Rand einer gültigen Postleitzahl"),
    (leerzeichen_ueberall_weg, "auch Leerzeichen in der Mitte entfernt", "einen Testfall mit einem Leerzeichen zwischen den Ziffern"),
    (nur_laenge, "nur die Länge prüft", "einen Testfall mit fünf Zeichen, die nicht alle Ziffern sind"),
    (als_zahl, "eine Zahl ab 10000 verlangt", "einen Testfall mit einer 0 am Anfang"),
    (erstes_zeichen, "bei leerer Eingabe abstürzt", "einen Testfall mit leerer Eingabe"),
    (leer_ist_gueltig, "eine leere Eingabe für gültig hält", "einen Testfall mit leerer Eingabe oder nur Leerzeichen"),
]

# Ihre Testfälle entdecken jede fehlerhafte Fassung
unentdeckt = []
for funktion, fehler, fehlender_fall in FEHLERHAFTE:
    if not entdeckt(funktion):
        unentdeckt.append(f"- Eine Fassung, die {fehler}, besteht alle Ihre Testfälle. Ergänzen Sie {fehlender_fall}.")
assert unentdeckt == [], (
    f"{len(unentdeckt)} von {len(FEHLERHAFTE)} fehlerhaften Fassungen von ist_plz bemerken Ihre Testfälle nicht:\n"
    + "\n".join(unentdeckt)
)

# Die Ausgabe des Programms zeigt jeden Testfall
assert len(AUSGABE.split("\n")) == len(faelle), (
    f"Das Programm soll für jeden der {len(faelle)} Testfälle eine Zeile ausgeben; es gibt aus:\n{AUSGABE}"
)
