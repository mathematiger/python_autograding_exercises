# Automatisch erzeugt aus lehrkraft/muster/5_002_eigenschaft.py - nicht von Hand ändern.
# vorlage-hash: 0fa30d9d61bb1ff5

# fget und fset werden gespeichert
def lesen(objekt):
    """Funktion zum Lesen für die Tests."""
    return 1


def schreiben(objekt, wert):
    """Funktion zum Schreiben für die Tests; tut nichts."""


e = Eigenschaft(lesen, schreiben)
assert getattr(e, "fget", None) is lesen and getattr(e, "fset", None) is schreiben, (
    "Eigenschaft(lesen, schreiben) muss die Funktionen in den Attributen fget und fset speichern; "
    f"gefunden: fget={getattr(e, 'fget', None)!r}, fset={getattr(e, 'fset', None)!r}."
)

# Ohne zweites Argument ist fset None
e = Eigenschaft(lesen)
assert getattr(e, "fset", "fehlt") is None, (
    f"Eigenschaft(lesen) muss fset auf None setzen; gefunden: {getattr(e, 'fset', 'fehlt')!r}."
)

# Lesen ruft fget auf, Schreiben ruft fset auf
regel = Alarmregel("CPU", 90)
assert regel.schwellwert == 90 and getattr(regel, "_schwellwert", None) == 90, (
    f"Nach Alarmregel('CPU', 90) ist schwellwert {regel.schwellwert!r}, erwartet war 90.\n"
    "Tipp: __set__ muss self.fset(objekt, wert) aufrufen, __get__ muss self.fget(objekt) zurückgeben."
)

# Ein neuer Wert geht durch den Setter
regel = Alarmregel("RAM", 80)
regel.schwellwert = 65
assert (regel.schwellwert, regel.beschreibung) == (65, "Alarm, wenn RAM über 65 %"), (
    f"Nach regel.schwellwert = 65 ergeben schwellwert und beschreibung {regel.schwellwert!r} und "
    f"{regel.beschreibung!r}, erwartet waren 65 und 'Alarm, wenn RAM über 65 %'."
)

# Die Prüfung im Setter greift, der alte Wert bleibt
regel = Alarmregel("CPU", 90)
for wert in [120, -5, 100.5]:
    try:
        regel.schwellwert = wert
        fehler = None
    except ValueError as ausnahme:
        fehler = ausnahme
    assert fehler is not None and regel.schwellwert == 90, (
        f"regel.schwellwert = {wert!r} muss einen ValueError auslösen und den Wert bei 90 lassen; "
        f"Ausnahme: {fehler!r}, schwellwert danach: {regel.schwellwert!r}."
    )

# Auch der Konstruktor geht durch den Setter
try:
    Alarmregel("CPU", 150)
    fehler = None
except ValueError as ausnahme:
    fehler = ausnahme
assert fehler is not None, "Alarmregel('CPU', 150) muss einen ValueError auslösen, weil __init__ über den Setter geht."

# Ein Attribut ohne Setter lässt sich nicht zuweisen
regel = Alarmregel("CPU", 90)
try:
    regel.beschreibung = "x"
    fehler = None
except AttributeError as ausnahme:
    fehler = ausnahme
assert fehler is not None and regel.beschreibung == "Alarm, wenn CPU über 90 %", (
    "regel.beschreibung = 'x' muss einen AttributeError auslösen, und beschreibung bleibt berechnet; "
    f"Ausnahme: {fehler!r}, beschreibung danach: {regel.beschreibung!r}."
)

# Ein Eintrag im __dict__ der Instanz verdeckt die Eigenschaft nicht
regel = Alarmregel("Temperatur", 70)
regel.__dict__["beschreibung"] = "verdeckt"
assert regel.beschreibung == "Alarm, wenn Temperatur über 70 %", (
    f"Mit einem Eintrag 'beschreibung' im __dict__ liefert regel.beschreibung {regel.beschreibung!r}, "
    "erwartet war der berechnete Text.\n"
    "Tipp: Ein Daten-Deskriptor braucht __set__, auch wenn es keinen Setter gibt."
)

# Zugriff über die Klasse liefert die Eigenschaft selbst
assert isinstance(Alarmregel.schwellwert, Eigenschaft) and isinstance(Alarmregel.beschreibung, Eigenschaft), (
    f"Alarmregel.schwellwert soll das Eigenschaft-Objekt liefern; gefunden: {Alarmregel.schwellwert!r}.\n"
    "Tipp: Ist objekt None, gibt __get__ self zurück."
)

# setter liefert eine neue Eigenschaft, die alte bleibt unverändert
alt = Eigenschaft(lesen)
neu = alt.setter(schreiben)
assert isinstance(neu, Eigenschaft) and neu is not alt, (
    f"alt.setter(schreiben) muss eine neue Eigenschaft zurückgeben; gefunden: {neu!r}.\n"
    "Tipp: Geben Sie nicht self zurück, sondern erzeugen Sie mit type(self)(…) ein neues Objekt."
)

# Die neue Eigenschaft hat beide Funktionen, die alte weiterhin keinen Setter
assert neu.fget is lesen and neu.fset is schreiben and alt.fset is None, (
    "Nach neu = alt.setter(schreiben) muss neu.fget das alte fget und neu.fset schreiben sein, "
    f"alt.fset muss None bleiben; gefunden: neu.fget={neu.fget!r}, neu.fset={neu.fset!r}, alt.fset={alt.fset!r}."
)


# Eine Unterklasse bekommt einen eigenen Setter, ohne die Oberklasse zu ändern
class StrengeRegel(Alarmregel):
    """Alarmregel, deren Schwellwert mindestens 50 % sein muss."""

    @Alarmregel.schwellwert.setter
    def schwellwert(self, wert):
        """Setzt den Schwellwert; nur 50 bis 100 Prozent sind erlaubt."""
        if not 50 <= wert <= 100:
            raise ValueError("Strenge Regeln brauchen mindestens 50 %.")
        self._schwellwert = wert


try:
    Alarmregel("CPU", 30)
    locker = None
except ValueError as ausnahme:
    locker = ausnahme
try:
    StrengeRegel("CPU", 30)
    streng = None
except ValueError as ausnahme:
    streng = ausnahme
assert locker is None and streng is not None and StrengeRegel("CPU", 60).schwellwert == 60, (
    "Mit @Alarmregel.schwellwert.setter in einer Unterklasse darf sich der Setter von Alarmregel nicht ändern: "
    f"Alarmregel('CPU', 30) löst {locker!r} aus, StrengeRegel('CPU', 30) löst {streng!r} aus.\n"
    "Tipp: setter darf self.fset nicht überschreiben, sondern muss eine neue Eigenschaft zurückgeben."
)

# Mit dem Messwert wird richtig verglichen
regel = Alarmregel("CPU", 90)
assert (regel.pruefe(95), regel.pruefe(90), regel.pruefe(40)) == (True, False, False), (
    f"regel.pruefe(95), pruefe(90), pruefe(40) ergeben {(regel.pruefe(95), regel.pruefe(90), regel.pruefe(40))!r}, "
    "erwartet war (True, False, False)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Alarm, wenn CPU über 90 %\nAlarm, wenn CPU über 75 % True"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
