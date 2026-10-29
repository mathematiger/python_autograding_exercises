# Automatisch erzeugt aus lehrkraft/muster/3_012_portbereich.py - nicht von Hand ändern.
# vorlage-hash: e9336e85edaafa07
# thema: fehler
# inhalt: Äquivalenzklassen und Grenzwerte

faelle = testfaelle()
BEREICHE = ["System", "Registriert", "Dynamisch", "ValueError"]

# testfaelle() gibt eine Liste von 1 bis 12 Tupeln (port, erwartet) zurück
form_ok = isinstance(faelle, list) and 1 <= len(faelle) <= 12
for fall in faelle if isinstance(faelle, list) else []:
    if not (isinstance(fall, tuple) and len(fall) == 2 and type(fall[0]) is int and fall[1] in BEREICHE):
        form_ok = False
assert form_ok, (
    f"testfaelle() ergibt {faelle!r}; erwartet war eine Liste mit 1 bis 12 Tupeln (port, erwartet), zum Beispiel "
    '[(22, "System"), (70000, "ValueError")]. port ist eine ganze Zahl, erwartet einer der Texte '
    f"{', '.join(BEREICHE)}."
)

# Alle Testfälle stimmen mit der richtigen portbereich überein
falsche_faelle = []
for port, erwartet in faelle:
    if ergebnis_von(portbereich, port) != erwartet:
        falsche_faelle.append((port, erwartet, ergebnis_von(portbereich, port)))
assert falsche_faelle == [], (
    "Diese Testfälle passen nicht zur Beschreibung (port, Ihr erwartet, richtig):\n"
    + "\n".join(f"  {fall!r}" for fall in falsche_faelle)
)

# Die vier Grenzen der richtigen portbereich: kleinster und größter Port jedes Bereichs
RICHTIG = [0, 1023, 49151, 65535]


def mit_grenzen(unten, system_bis, registriert_bis, oben):
    """Baut eine Fassung von portbereich mit anderen Grenzen; bei RICHTIG ist sie die richtige."""

    def bereich(port):
        """portbereich mit den Grenzen unten, system_bis, registriert_bis und oben."""
        if port < unten or port > oben:
            raise ValueError(f"Keine Portnummer: {port}")
        if port <= system_bis:
            return "System"
        if port <= registriert_bis:
            return "Registriert"
        return "Dynamisch"

    return bereich


def entdeckt(funktion):
    """True, wenn funktion bei mindestens einem Testfall etwas anderes liefert als erwartet."""
    for port, erwartet in faelle:
        if ergebnis_von(funktion, port) != erwartet:
            return True
    return False


GRENZNAMEN = [
    "die untere Grenze 0 (kleinster Port)",
    "die Grenze zwischen System und Registriert (1023/1024)",
    "die Grenze zwischen Registriert und Dynamisch (49151/49152)",
    "die obere Grenze 65535 (größter Port)",
]

# Jede um eins verschobene Grenze wird entdeckt
unentdeckt = []
for nummer in range(4):
    for verschiebung, richtung in [(-1, "nach unten"), (1, "nach oben")]:
        grenzen = list(RICHTIG)
        grenzen[nummer] += verschiebung
        if not entdeckt(mit_grenzen(*grenzen)):
            unentdeckt.append(f"- {GRENZNAMEN[nummer]} um eins {richtung} verschoben")
assert unentdeckt == [], (
    "Diese fehlerhaften Fassungen von portbereich bestehen alle Ihre Testfälle:\n" + "\n".join(unentdeckt) + "\n"
    "Tipp: Testen Sie an jeder Grenze beide Seiten, den letzten Port des einen Bereichs und den ersten des nächsten."
)

# Viele zufällig verschobene Grenzen, auch um mehr als eins und an mehreren Stellen zugleich
zufall = Zufall(3012)
nicht_entdeckt = None
for _ in range(300):
    grenzen = list(RICHTIG)
    for nummer in zufall.sample(range(4), zufall.randint(1, 4)):
        grenzen[nummer] += zufall.choice([-1, 1]) * zufall.choice([1, 2, 5, 100, 1000])
    if grenzen != RICHTIG and not entdeckt(mit_grenzen(*grenzen)):
        nicht_entdeckt = grenzen
        break
assert nicht_entdeckt is None, (
    f"Eine Fassung von portbereich mit den Grenzen {nicht_entdeckt} statt {RICHTIG} (kleinster Port, letzter "
    "System-Port, letzter registrierter Port, größter Port) besteht alle Ihre Testfälle."
)

# Ein Bereich, der ganz fehlt, wird entdeckt
for grenzen, beschreibung in [
    ([0, 49151, 49151, 65535], 'kennt "Registriert" nicht'),
    ([0, 1023, 65535, 65535], 'kennt "Dynamisch" nicht'),
    ([-10**7, 1023, 49151, 10**7], "löst nie einen ValueError aus"),
]:
    assert entdeckt(mit_grenzen(*grenzen)), (
        f"Eine Fassung von portbereich, die {beschreibung}, besteht alle Ihre Testfälle.\n"
        "Tipp: Nehmen Sie aus jeder der fünf Äquivalenzklassen mindestens einen Port."
    )

# Die Ausgabe des Programms zeigt jeden Testfall
assert len(AUSGABE.split("\n")) == len(faelle), (
    f"Das Programm soll für jeden der {len(faelle)} Testfälle eine Zeile ausgeben; es gibt aus:\n{AUSGABE}"
)
