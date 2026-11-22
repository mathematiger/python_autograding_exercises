# Automatisch erzeugt aus lehrkraft/muster/3_043_messstellen.py - nicht von Hand ändern.
# vorlage-hash: d5397c5d4e62d75f
# text-hash: e84e37de1b1643cf
# thema: klassen
# inhalt: Klassen- und Instanzattribute

def neu_anfangen():
    """Setzt die Klassenattribute zurück, wie es die Grenzen versprechen."""
    Messstelle.angelegt = 0
    Messstelle.grenzwert = 80


def wert_von(aufruf):
    """Führt den Aufruf (eine Funktion ohne Argumente) aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def beispiel():
    """Baut die beiden Messstellen aus dem Beispiel mit ihren Werten."""
    neu_anfangen()
    a = Messstelle("web-01")
    b = Messstelle("render-01")
    a.messen(85)
    a.messen(70)
    b.messen(95)
    return a, b


# Jede Messstelle hat ihren Namen und eine eigene Liste
a, b = wert_von(beispiel)
werte = wert_von(lambda: (a.name, a.werte, b.name, b.werte))
assert werte == ("web-01", [85, 70], "render-01", [95]), (
    f"Im Beispiel haben a und b die Namen und Werte {werte!r}, erwartet war ('web-01', [85, 70], 'render-01', [95]).\n"
    "Tipp: Legen Sie die Liste in __init__ mit self.werte = [] an, dann bekommt jede Messstelle ihre eigene."
)

# Eine neue Messstelle beginnt mit einer leeren Liste
neu_anfangen()
alt = Messstelle("db-01")
alt.messen(50)
neu = Messstelle("db-02")
assert wert_von(lambda: neu.werte) == [] and neu.werte is not alt.werte, (
    f"Nach a.messen(50) hat die danach angelegte Messstelle die Werte {wert_von(lambda: neu.werte)!r}, erwartet war []."
)

# Die laufende Nummer: 1, 2, 3
neu_anfangen()
nummern = wert_von(lambda: [Messstelle(name).nummer for name in ["x", "y", "z"]])
assert nummern == [1, 2, 3], (
    f"Drei neue Messstellen haben die Nummern {nummern!r}, erwartet war [1, 2, 3].\n"
    "Tipp: Erhöhen Sie Messstelle.angelegt (über den Klassennamen) und setzen Sie dann self.nummer."
)

# Die Klasse zählt mit: Messstelle.angelegt
neu_anfangen()
for name in ["x", "y", "z", "w"]:
    Messstelle(name)
assert Messstelle.angelegt == 4, (
    f"Nach vier neuen Messstellen ist Messstelle.angelegt {Messstelle.angelegt!r}, erwartet war 4.\n"
    "Tipp: self.angelegt += 1 legt nur ein Attribut beim Objekt an; schreiben Sie Messstelle.angelegt += 1."
)

# alarme mit dem gemeinsamen Grenzwert 80
a, b = beispiel()
alarme = wert_von(lambda: (a.alarme(), b.alarme()))
assert alarme == (1, 1), f"Mit dem Grenzwert 80 ergeben a.alarme() und b.alarme() {alarme!r}, erwartet war (1, 1)."

# alarme: ein Wert genau auf dem Grenzwert ist kein Alarm
neu_anfangen()
m = Messstelle("edge")
for wert in [80, 81, 79, 80, 100]:
    m.messen(wert)
alarme = wert_von(m.alarme)
assert alarme == 2, f"Mit den Werten [80, 81, 79, 80, 100] ergibt alarme() {alarme!r}, erwartet war 2 (nur 81 und 100)."

# alarme ohne Werte
neu_anfangen()
alarme = wert_von(Messstelle("leer").alarme)
assert alarme == 0, f"Eine Messstelle ohne Werte hat {alarme!r} Alarme, erwartet war 0."

# eigener_grenzwert gilt nur für diese Messstelle
a, b = beispiel()
b.eigener_grenzwert(98)
alarme = wert_von(lambda: (a.alarme(), b.alarme(), Messstelle.grenzwert))
assert alarme == (1, 0, 80), (
    f"Nach b.eigener_grenzwert(98) ergeben a.alarme(), b.alarme() und Messstelle.grenzwert {alarme!r}, "
    "erwartet war (1, 0, 80).\nTipp: self.grenzwert = grenze gibt nur diesem Objekt einen eigenen Wert."
)

# gemeinsamer_grenzwert gilt für alle ohne eigenen Grenzwert
a, b = beispiel()
c = Messstelle("db-01")
c.messen(85)
gemeinsamer_grenzwert(84)
alarme = wert_von(lambda: (a.alarme(), b.alarme(), c.alarme(), Messstelle.grenzwert))
assert alarme == (1, 1, 1, 84), (
    f"Nach gemeinsamer_grenzwert(84) ergeben a, b, c.alarme() und Messstelle.grenzwert {alarme!r}, erwartet war (1, 1, 1, 84)."
)

# gemeinsamer_grenzwert gilt sofort, auch für schon angelegte Messstellen
a, b = beispiel()
gemeinsamer_grenzwert(90)
alarme = wert_von(lambda: (a.alarme(), b.alarme()))
assert alarme == (0, 1), (
    f"Nach gemeinsamer_grenzwert(90) ergeben a.alarme() und b.alarme() {alarme!r}, erwartet war (0, 1).\n"
    "Tipp: Ändern Sie Messstelle.grenzwert, und lesen Sie in alarme self.grenzwert, nicht eine Kopie aus __init__."
)

# Ein eigener Grenzwert bleibt, wenn sich der gemeinsame ändert
a, b = beispiel()
b.eigener_grenzwert(98)
gemeinsamer_grenzwert(60)
alarme = wert_von(lambda: (a.alarme(), b.alarme()))
assert alarme == (2, 0), f"Mit eigenem Grenzwert 98 für b und gemeinsamem 60 ergeben die Alarme {alarme!r}, erwartet war (2, 0)."

# Grenzwerte am Rand: 0 und 100
a, b = beispiel()
a.eigener_grenzwert(0)
b.eigener_grenzwert(100)
a.messen(0)
b.messen(100)
alarme = wert_von(lambda: (a.alarme(), b.alarme()))
assert alarme == (2, 0), f"Mit eigenem Grenzwert 0 für a und 100 für b ergeben die Alarme {alarme!r}, erwartet war (2, 0)."

# Die Ausgabe des Programms
erwartet = "1 [85, 70] 2 [95]\nAlarme: 1 0\nAlarme: 0 0"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Abläufe, verglichen mit einem Modell aus Dictionaries
zufall = Zufall(3043)
for runde in range(150):
    neu_anfangen()
    stellen = []
    modell_werte = []
    modell_eigen = []
    gemeinsam = 80
    ablauf = []
    for _ in range(zufall.randint(1, 25)):
        schritt = zufall.random()
        if schritt < 0.2 or not stellen:
            stellen.append(Messstelle(f"m{len(stellen)}"))
            modell_werte.append([])
            modell_eigen.append(None)
            ablauf.append("neu")
        elif schritt < 0.75:
            nummer = zufall.randrange(len(stellen))
            wert = zufall.randint(0, 100)
            stellen[nummer].messen(wert)
            modell_werte[nummer].append(wert)
            ablauf.append(f"m{nummer}.messen({wert})")
        elif schritt < 0.87:
            nummer = zufall.randrange(len(stellen))
            grenze = zufall.randint(0, 100)
            stellen[nummer].eigener_grenzwert(grenze)
            modell_eigen[nummer] = grenze
            ablauf.append(f"m{nummer}.eigener_grenzwert({grenze})")
        else:
            gemeinsam = zufall.randint(0, 100)
            gemeinsamer_grenzwert(gemeinsam)
            ablauf.append(f"gemeinsamer_grenzwert({gemeinsam})")
    for nummer, stelle in enumerate(stellen):
        grenze = gemeinsam if modell_eigen[nummer] is None else modell_eigen[nummer]
        erwartet = (nummer + 1, modell_werte[nummer], len([w for w in modell_werte[nummer] if w > grenze]))
        ergebnis = wert_von(lambda: (stelle.nummer, stelle.werte, stelle.alarme()))
        assert ergebnis == erwartet, (
            f"Nach dem Ablauf {ablauf} hat m{nummer} (nummer, werte, alarme) = {ergebnis!r}, erwartet war {erwartet!r}."
        )

# Obere Grenze: 10 000 Messstellen mit zusammen 100 000 Werten
neu_anfangen()
stellen = [Messstelle(f"m{nummer}") for nummer in range(10000)]
for nummer in range(100000):
    stellen[nummer % 10000].messen(nummer % 101)
gemeinsamer_grenzwert(50)
gesamt = wert_von(lambda: sum(stelle.alarme() for stelle in stellen))
erwartet = len([nummer for nummer in range(100000) if nummer % 101 > 50])
assert gesamt == erwartet and stellen[-1].nummer == 10000 and Messstelle.angelegt == 10000, (
    f"Bei 10 000 Messstellen und 100 000 Werten gibt es {gesamt!r} Alarme, erwartet waren {erwartet}; "
    f"die letzte hat die Nummer {stellen[-1].nummer}, erwartet war 10000."
)
