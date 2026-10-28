# Automatisch erzeugt aus lehrkraft/muster/4_005_sprint.py - nicht von Hand ändern.
# vorlage-hash: 038f34a212009667
# thema: klassen
# inhalt: `property` mit Setter

# Die drei Properties sind mit @property angelegt
fehlend = [name for name in ["kapazitaet", "geplant", "auslastung"] if not isinstance(Sprint.__dict__.get(name), property)]
assert not fehlend, (
    f"In der Klasse Sprint sind {', '.join(fehlend)} keine Properties.\n"
    "Tipp: Schreiben Sie @property in die Zeile über jede der drei Methoden."
)

# Ein neuer Sprint hat die angegebene Kapazität und nichts geplant
try:
    sprint = Sprint(40)
    werte = (sprint.kapazitaet, sprint.geplant, sprint.auslastung)
    fehler = None
except Exception as ausnahme:
    werte = None
    fehler = ausnahme
assert fehler is None and werte == (40, 0, 0), (
    f"Für Sprint(40) ergeben kapazitaet, geplant, auslastung {werte!r} bzw. lösen {fehler!r} aus, "
    "erwartet war (40, 0, 0.0).\n"
    "Tipp: Der Setter von kapazitaet speichert den Wert in self._kapazitaet; der Getter liest ihn dort."
)

# geplant summiert die Story Points der eingeplanten Aufgaben
sprint = Sprint(40)
sprint.einplanen("Anmeldung per E-Mail", 13)
sprint.einplanen("Passwort zurücksetzen", 8)
assert sprint.geplant == 21, (
    f"Nach dem Einplanen von 13 und 8 Story Points ergibt geplant {sprint.geplant!r}, erwartet war 21."
)

# auslastung ist der verplante Anteil in Prozent
assert sprint.auslastung == 52.5, (
    f"Bei 21 von 40 Story Points ergibt auslastung {sprint.auslastung!r}, erwartet war 52.5.\n"
    "Tipp: Rechnen Sie self.geplant / self.kapazitaet * 100."
)

# geplant und auslastung sind nach jedem Einplanen aktuell (nicht nur in __init__ ausrechnen!)
sprint = Sprint(20)
werte = []
for titel, punkte in [("Logo austauschen", 2), ("Export als CSV", 5), ("Suche beschleunigen", 8)]:
    sprint.einplanen(titel, punkte)
    werte.append((sprint.geplant, sprint.auslastung))
assert werte == [(2, 10.0), (7, 35.0), (15, 75.0)], (
    f"Bei Kapazität 20 und Aufgaben mit 2, 5 und 8 Punkten ergeben (geplant, auslastung) nacheinander {werte}, "
    "erwartet war [(2, 10.0), (7, 35.0), (15, 75.0)].\n"
    "Tipp: Rechnen Sie bei jedem Lesen neu aus den Aufgaben in self.aufgaben, statt einen Wert zu speichern."
)

# Die Kapazität lässt sich ändern, die Auslastung passt sich an
sprint = Sprint(40)
sprint.einplanen("Anmeldung per E-Mail", 13)
sprint.einplanen("Passwort zurücksetzen", 8)
sprint.kapazitaet = 30
assert sprint.kapazitaet == 30 and sprint.auslastung == 70.0, (
    f"Nach sprint.kapazitaet = 30 (21 Punkte geplant) ist kapazitaet {sprint.kapazitaet!r} und auslastung "
    f"{sprint.auslastung!r}, erwartet war 30 und 70.0."
)

# Genau so viel Kapazität wie geplant ist erlaubt
sprint.kapazitaet = 21
assert sprint.kapazitaet == 21 and sprint.auslastung == 100.0, (
    f"Nach sprint.kapazitaet = 21 (21 Punkte geplant) ist kapazitaet {sprint.kapazitaet!r} und auslastung "
    f"{sprint.auslastung!r}, erwartet war 21 und 100.0.\n"
    "Tipp: Nur eine Kapazität, die echt kleiner als geplant ist, löst einen ValueError aus."
)

# Eine Kapazität von 0 oder weniger löst ValueError aus und ändert nichts
ergebnisse = []
for wert in [0, -5]:
    sprint = Sprint(40)
    try:
        sprint.kapazitaet = wert
        ergebnisse.append(("kein Fehler", sprint.kapazitaet))
    except ValueError:
        ergebnisse.append(("ValueError", sprint.kapazitaet))
assert ergebnisse == [("ValueError", 40), ("ValueError", 40)], (
    f"sprint.kapazitaet = 0 und = -5 bei Kapazität 40 ergeben (Fehler, Kapazität danach) {ergebnisse}, "
    "erwartet war [('ValueError', 40), ('ValueError', 40)].\n"
    "Tipp: Prüfen Sie im Setter zuerst und speichern Sie den Wert erst, wenn er gültig ist."
)

# Die kleinste erlaubte Kapazität ist 1
try:
    kapazitaet = Sprint(1).kapazitaet
    fehler = None
except ValueError as ausnahme:
    kapazitaet = None
    fehler = ausnahme
assert fehler is None and kapazitaet == 1, (
    f"Sprint(1) ergibt die Kapazität {kapazitaet!r} bzw. löst {fehler!r} aus, erwartet war Kapazität 1.\n"
    "Tipp: Nur 0 oder weniger löst einen ValueError aus, also wert <= 0."
)

# Eine Kapazität unter den geplanten Punkten löst ValueError aus und ändert nichts
sprint = Sprint(40)
sprint.einplanen("Anmeldung per E-Mail", 13)
sprint.einplanen("Passwort zurücksetzen", 8)
try:
    sprint.kapazitaet = 20
    fehler = "kein Fehler"
except ValueError:
    fehler = "ValueError"
assert fehler == "ValueError" and sprint.kapazitaet == 40, (
    f"sprint.kapazitaet = 20 bei 21 geplanten Punkten ergibt {fehler}, danach ist kapazitaet {sprint.kapazitaet!r}; "
    "erwartet war ValueError und weiterhin 40.\n"
    "Tipp: Vergleichen Sie im Setter den neuen Wert mit self.geplant."
)

# Schon beim Anlegen wird die Kapazität geprüft
ergebnisse = []
for wert in [0, -3]:
    try:
        Sprint(wert)
        ergebnisse.append("kein Fehler")
    except ValueError:
        ergebnisse.append("ValueError")
assert ergebnisse == ["ValueError", "ValueError"], (
    f"Sprint(0) und Sprint(-3) ergeben {ergebnisse}, erwartet war beide Male ValueError.\n"
    "Tipp: __init__ schreibt self.kapazitaet = kapazitaet und geht damit über Ihren Setter."
)

# geplant und auslastung lassen sich nicht zuweisen
sprint = Sprint(40)
ergebnisse = []
for name in ["geplant", "auslastung"]:
    try:
        setattr(sprint, name, 5)
        ergebnisse.append("kein Fehler")
    except AttributeError:
        ergebnisse.append("AttributeError")
assert ergebnisse == ["AttributeError", "AttributeError"], (
    f"sprint.geplant = 5 und sprint.auslastung = 5 ergeben {ergebnisse}, erwartet war beide Male AttributeError.\n"
    "Tipp: Schreiben Sie für geplant und auslastung nur @property, keinen Setter."
)

# einplanen nutzt die Properties: zu große Aufgaben passen nicht
sprint = Sprint(10)
sprint.einplanen("Logo austauschen", 8)
try:
    sprint.einplanen("Export als CSV", 5)
    fehler = "kein Fehler"
except ValueError:
    fehler = "ValueError"
assert fehler == "ValueError" and sprint.geplant == 8, (
    f"Bei Kapazität 10 und 8 geplanten Punkten ergibt einplanen mit 5 Punkten {fehler}, geplant ist danach "
    f"{sprint.geplant!r}; erwartet war ValueError und weiterhin 8."
)

# Die Ausgabe des Programms stimmt
assert AUSGABE == "21 52.5\n30 70.0", f"Erwartete Ausgabe:\n21 52.5\n30 70.0\nIhr Programm:\n{AUSGABE}"
