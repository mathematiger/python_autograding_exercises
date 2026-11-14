# Automatisch erzeugt aus lehrkraft/muster/4_030_alarmregeln.py - nicht von Hand ändern.
# vorlage-hash: 469f759bc6f2dda9
# text-hash: fe74cc5a17fef0e6
# thema: funktionen
# inhalt: Klassen- und Methodendekoratoren

# alarmregel trägt die Klasse unter ihrem Namen ein
assert REGELN.get("Schwellwert") is Schwellwert, (
    f"Nach @alarmregel über class Schwellwert erwartet REGELN['Schwellwert'] ist die Klasse; REGELN ist {REGELN!r}."
)

# alarmregel gibt die Klasse unverändert zurück
class Bereich:
    """Alarm außerhalb von unten bis oben."""

    def pruefe(self, wert):
        """True außerhalb des Bereichs 10 bis 20."""
        return not 10 <= wert <= 20


ergebnis = alarmregel(Bereich)
assert ergebnis is Bereich and REGELN.get("Bereich") is Bereich, (
    f"alarmregel(Bereich) liefert {ergebnis!r} und REGELN['Bereich'] ist {REGELN.get('Bereich')!r}; "
    "erwartet war beides die Klasse Bereich selbst.\n"
    "Tipp: Vergessen Sie am Ende des Klassendekorators nicht return klasse."
)

# Die bisherigen Einträge bleiben erhalten
assert REGELN.get("Schwellwert") is Schwellwert and REGELN.get("Bereich") is Bereich, (
    f"Nach zwei dekorierten Klassen erwartet REGELN mit Schwellwert und Bereich, gefunden {REGELN!r}."
)

# Die dekorierte Methode liefert weiter ihr Ergebnis
regel = Schwellwert(90)
ergebnisse = (regel.pruefe(95), regel.pruefe(40))
assert ergebnisse == (True, False), (
    f"Schwellwert(90).pruefe(95) und .pruefe(40) ergeben {ergebnisse!r}, erwartet war (True, False).\n"
    "Tipp: Die Hülle muss das Ergebnis der ursprünglichen Methode mit return zurückgeben."
)

# Das Beispiel aus der Aufgabe: zwei Einträge im Protokoll
regel = Schwellwert(90)
regel.pruefe(95)
regel.pruefe(40)
gefunden = getattr(regel, "protokoll", "(kein Attribut protokoll)")
assert gefunden == [("pruefe", (95,), True), ("pruefe", (40,), False)], (
    f"Nach Schwellwert(90).pruefe(95) und .pruefe(40) ist protokoll {gefunden!r}, "
    "erwartet war [('pruefe', (95,), True), ('pruefe', (40,), False)]."
)

# Jedes Objekt hat sein eigenes Protokoll
a = Schwellwert(10)
b = Schwellwert(20)
a.pruefe(15)
b.pruefe(15)
b.pruefe(25)
gefunden = (getattr(a, "protokoll", None), getattr(b, "protokoll", None))
assert gefunden == ([("pruefe", (15,), True)], [("pruefe", (15,), False), ("pruefe", (25,), True)]), (
    "a = Schwellwert(10), b = Schwellwert(20); a.pruefe(15), b.pruefe(15), b.pruefe(25): "
    f"erwartet a.protokoll mit einem und b.protokoll mit zwei Einträgen, gefunden {gefunden!r}.\n"
    "Tipp: Speichern Sie das Protokoll auf self, nicht in einer Variablen des Dekorators."
)

# Name und Docstring bleiben erhalten
assert Schwellwert.pruefe.__name__ == "pruefe" and Schwellwert.pruefe.__doc__ == "True, wenn wert größer als die Grenze ist.", (
    f"Schwellwert.pruefe heißt {Schwellwert.pruefe.__name__!r} mit Docstring {Schwellwert.pruefe.__doc__!r}; "
    "erwartet waren Name und Docstring der ursprünglichen Methode.\n"
    "Tipp: Schreiben Sie @functools.wraps(methode) über die Hülle."
)

# Mehrere Argumente und Schlüsselwortargumente werden weitergereicht
class Fenster:
    """Alarm, wenn mehrere Werte im Mittel über der Grenze liegen."""

    @protokolliert
    def mittel_ueber(self, *werte, grenze=50):
        """True, wenn der Mittelwert der Werte über grenze liegt."""
        return sum(werte) / len(werte) > grenze

    @protokolliert
    def anzahl_ueber(self, werte, grenze):
        """Wie viele Werte über grenze liegen."""
        return len([wert for wert in werte if wert > grenze])


fenster = Fenster()
ergebnisse = (fenster.mittel_ueber(40, 70, grenze=50), fenster.mittel_ueber(10, 20, 30), fenster.anzahl_ueber([1, 5, 9], grenze=4))
gefunden = getattr(fenster, "protokoll", None)
assert ergebnisse == (True, False, 2) and gefunden == [
    ("mittel_ueber", (40, 70), True),
    ("mittel_ueber", (10, 20, 30), False),
    ("anzahl_ueber", ([1, 5, 9],), 2),
], (
    "fenster.mittel_ueber(40, 70, grenze=50), fenster.mittel_ueber(10, 20, 30), fenster.anzahl_ueber([1, 5, 9], grenze=4): "
    f"Ergebnisse {ergebnisse!r}, erwartet (True, False, 2); Protokoll {gefunden!r}, erwartet "
    "[('mittel_ueber', (40, 70), True), ('mittel_ueber', (10, 20, 30), False), ('anzahl_ueber', ([1, 5, 9],), 2)].\n"
    "Tipp: Nehmen Sie in der Hülle self, *args und **kwargs entgegen; ins Protokoll gehört args (ohne self)."
)

# Eine Ausnahme geht weiter, und nichts wird eingetragen
fenster = Fenster()
fenster.mittel_ueber(60)
try:
    fenster.mittel_ueber()
    ausnahme = None
except ZeroDivisionError as fehler:
    ausnahme = fehler
gefunden = getattr(fenster, "protokoll", None)
assert ausnahme is not None and gefunden == [("mittel_ueber", (60,), True)], (
    "fenster.mittel_ueber(60), dann fenster.mittel_ueber() (teilt durch 0): erwartet ein ZeroDivisionError und "
    f"nur der erste Eintrag im Protokoll; Ausnahme: {ausnahme!r}, Protokoll: {gefunden!r}.\n"
    "Tipp: Rufen Sie die Methode zuerst auf und tragen Sie erst danach ein; fangen Sie die Ausnahme nicht ab."
)

# Ein schon vorhandenes Protokoll wird weitergeführt, nicht ersetzt
regel = Schwellwert(5)
regel.protokoll = [("start", (), None)]
regel.pruefe(1)
assert regel.protokoll == [("start", (), None), ("pruefe", (1,), False)], (
    f"Hat das Objekt schon protokoll = [('start', (), None)], soll pruefe(1) anhängen; gefunden {regel.protokoll!r}."
)

# Viele zufällige Prüfungen an mehreren Regeln
zufall = Zufall(4030)
regeln = [Schwellwert(zufall.randint(0, 100)) for _ in range(5)]
erwartet = [[] for _ in regeln]
fehlerfall = None
for schritt in range(2000):
    nummer = zufall.randrange(len(regeln))
    wert = zufall.randint(-50, 150)
    ergebnis = regeln[nummer].pruefe(wert)
    erwartet[nummer].append(("pruefe", (wert,), wert > regeln[nummer].grenze))
    if ergebnis != (wert > regeln[nummer].grenze) or getattr(regeln[nummer], "protokoll", None) != erwartet[nummer]:
        fehlerfall = (schritt, nummer, regeln[nummer].grenze, wert, ergebnis, getattr(regeln[nummer], "protokoll", None))
        break
assert fehlerfall is None, (
    f"Bei Schritt {fehlerfall[0]}: Regel {fehlerfall[1]} (Grenze {fehlerfall[2]}).pruefe({fehlerfall[3]}) ergibt "
    f"{fehlerfall[4]!r}; die letzten Protokolleinträge: {(fehlerfall[5] or [])[-3:]!r}."
)

# Obere Grenze: 10 000 protokollierte Aufrufe an einem Objekt
regel = Schwellwert(5000)
for wert in range(10000):
    regel.pruefe(wert)
protokoll = getattr(regel, "protokoll", [])
assert len(protokoll) == 10000 and protokoll[5000] == ("pruefe", (5000,), False) and protokoll[-1] == ("pruefe", (9999,), True), (
    f"Nach 10 000 Aufrufen pruefe(0) bis pruefe(9999) hat das Protokoll {len(protokoll)} Einträge, "
    f"erwartet 10 000; Eintrag 5000: {protokoll[5000] if len(protokoll) > 5000 else None!r}."
)
