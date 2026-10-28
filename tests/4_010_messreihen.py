# Automatisch erzeugt aus lehrkraft/muster/4_010_messreihen.py - nicht von Hand ändern.
# vorlage-hash: cbd3f781292a19d1

# CpuLast speichert Name, Einheit und Schwelle und beginnt mit einer leeren Werteliste
c = CpuLast("srv02", 80)
angaben = tuple(getattr(c, name, None) for name in ["name", "einheit", "schwellwert", "werte"])
assert angaben == ("srv02", "%", 80, []), (
    f'CpuLast("srv02", 80) hat name, einheit, schwellwert, werte = {angaben!r}, erwartet waren ("srv02", "%", 80, []).\n'
    'Tipp: super().__init__(name, "%") legt Name, Einheit und Werteliste an.'
)

# Die MRO von CpuLast ist wie vorgegeben
mro = [klasse.__name__ for klasse in CpuLast.__mro__]
assert mro == ["CpuLast", "SchwellwertMixin", "StatistikMixin", "Messreihe", "object"], (
    f"Die MRO von CpuLast ist {mro}, erwartet war CpuLast, SchwellwertMixin, StatistikMixin, Messreihe, object.\n"
    "Tipp: Ändern Sie die Reihenfolge der Basisklassen in class CpuLast(...) nicht."
)

# ueberschreitungen findet die Werte über der Schwelle (nicht fest hinschreiben!)
for schwelle, werte, erwartet in [
    (90, [35, 92, 90, 97], [92, 97]),
    (50, [60, 40, 55, 50, 51], [60, 55, 51]),
    (99, [10, 20], []),
    (0, [3, 0, 1], [3, 1]),
]:
    c = CpuLast("srv", schwelle)
    for wert in werte:
        c.hinzufuegen(wert)
    ergebnis = c.ueberschreitungen()
    if ergebnis == [wert for wert in werte if wert >= schwelle] and ergebnis != erwartet:
        hinweis = "\nTipp: Genau die Schwelle ist noch kein Alarm; verlangt ist echt größer, also >."
    else:
        hinweis = ""
    assert ergebnis == erwartet, (
        f"Bei Schwelle {schwelle} und den Werten {werte} ergibt ueberschreitungen() {ergebnis!r}, "
        f"erwartet war {erwartet!r}.{hinweis}"
    )

# spitze liefert den größten Wert
for werte, erwartet in [([35, 92, 90, 97], 97), ([88, 12, 40], 88), ([5], 5)]:
    c = CpuLast("srv", 90)
    for wert in werte:
        c.hinzufuegen(wert)
    ergebnis = c.spitze()
    assert ergebnis == erwartet, f"Bei den Werten {werte} ergibt spitze() {ergebnis!r}, erwartet war {erwartet!r}."

# Eine leere Messreihe hat keine Spitze
try:
    ergebnis = CpuLast("srv", 90).spitze()
except ValueError as ausnahme:
    ergebnis = ausnahme
assert ergebnis is None, (
    f"Bei einer leeren Messreihe ergibt spitze() {ergebnis!r}, erwartet war None.\n"
    "Tipp: max([]) löst einen ValueError aus. Prüfen Sie den Fall der leeren Liste vorher."
)

# Die Beschreibung aus dem Beispiel
c = CpuLast("srv01", 90)
for wert in [35, 92, 90, 97]:
    c.hinzufuegen(wert)
ergebnis = c.beschreibung()
assert ergebnis == "srv01 (%), 4 Werte, Schwelle 90", (
    f'beschreibung() ergibt {ergebnis!r}, erwartet war "srv01 (%), 4 Werte, Schwelle 90".\n'
    "Tipp: Jedes Mixin hängt seinen Teil an super().beschreibung() an."
)

# Andere Namen, Schwellen und Anzahlen
c = CpuLast("db7", 75)
c.hinzufuegen(10)
ergebnis = c.beschreibung()
assert ergebnis == "db7 (%), 1 Werte, Schwelle 75", (
    f'Bei CpuLast("db7", 75) mit einem Wert ergibt beschreibung() {ergebnis!r}, erwartet war "db7 (%), 1 Werte, Schwelle 75".'
)


class Temperatur(StatistikMixin, Messreihe):
    """Eine Messreihe, die in der Aufgabe nicht vorkommt: nur mit Statistik."""

    def __init__(self, name):
        """Speichert den Namen; die Einheit ist immer °C."""
        super().__init__(name, "°C")


class Speicher(StatistikMixin, SchwellwertMixin, Messreihe):
    """Eine Messreihe, die in der Aufgabe nicht vorkommt: Mixins in umgekehrter Reihenfolge."""

    def __init__(self, name, schwellwert):
        """Speichert Name und Schwelle; die Einheit ist immer GB."""
        super().__init__(name, "GB")
        self.schwellwert = schwellwert


# Das StatistikMixin funktioniert auch ohne SchwellwertMixin
t = Temperatur("gehaeuse")
t.hinzufuegen(41)
t.hinzufuegen(44)
ergebnis = t.beschreibung()
assert ergebnis == "gehaeuse (°C), 2 Werte", (
    f'Bei einer Klasse Temperatur(StatistikMixin, Messreihe) mit zwei Werten ergibt beschreibung() {ergebnis!r}, '
    'erwartet war "gehaeuse (°C), 2 Werte".'
)

# Mit umgekehrter Reihenfolge der Mixins dreht sich auch die Beschreibung um
s = Speicher("ram", 12)
s.hinzufuegen(14)
ergebnis = s.beschreibung()
assert ergebnis == "ram (GB), Schwelle 12, 1 Werte", (
    f'Bei einer Klasse Speicher(StatistikMixin, SchwellwertMixin, Messreihe) ergibt beschreibung() {ergebnis!r}, '
    'erwartet war "ram (GB), Schwelle 12, 1 Werte".\n'
    "Tipp: Rufen Sie super().beschreibung() auf, nicht Messreihe.beschreibung(self). Nur dann kommt jede "
    "Klasse der MRO an die Reihe."
)

# Beide Mixins arbeiten in der anderen Reihenfolge auch einzeln
ergebnis = (s.ueberschreitungen(), s.spitze())
assert ergebnis == ([14], 14), (
    f"Bei Speicher mit Schwelle 12 und dem Wert 14 ergeben ueberschreitungen() und spitze() {ergebnis!r}, "
    "erwartet war ([14], 14)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "srv01 (%), 4 Werte, Schwelle 90\nÜber der Schwelle: [92, 97]\nSpitze: 97"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
