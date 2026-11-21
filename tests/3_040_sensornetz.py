# Automatisch erzeugt aus lehrkraft/muster/3_040_sensornetz.py - nicht von Hand ändern.
# vorlage-hash: 7a6124197ba81343
# text-hash: 8f70a310df288d85
# thema: klassen
# inhalt: Objekte in Listen

def beispielnetz():
    """Baut das Netz aus dem Beispiel und gibt es mit seinen drei Sensoren zurück."""
    netz = Sensornetz()
    sensoren = [Sensor("T-01", "Büro 1", 21.5), Sensor("T-02", "Serverraum", 24.0), Sensor("T-03", "Büro 1", 22.5)]
    for sensor in sensoren:
        netz.hinzufuegen(sensor)
    return netz, sensoren


def als_tupel(sensor):
    """Kennung, Raum und Wert eines Sensors für Vergleiche; kein Sensor wird als Text zurückgegeben."""
    if not isinstance(sensor, Sensor):
        return f"kein Sensor, sondern {sensor!r}"
    return (sensor.kennung, sensor.raum, sensor.wert)


def texte(sensoren):
    """Die Texte einer Liste von Sensoren, für Meldungen."""
    if not isinstance(sensoren, list):
        return f"keine Liste, sondern {sensoren!r}"
    return [str(sensor) for sensor in sensoren]


def zufallsnetz(zufall, anzahl):
    """Baut ein Netz mit anzahl zufälligen Sensoren; gibt das Netz und die Liste der Sensoren zurück."""
    netz = Sensornetz()
    sensoren = []
    for nummer in range(anzahl):
        wert = zufall.choice([zufall.randint(-400, 1250) / 10, zufall.randint(18, 26)])
        sensor = Sensor(f"T-{nummer:05d}", zufall.choice(["Büro 1", "Büro 2", "Lager", "Serverraum"]), wert)
        netz.hinzufuegen(sensor)
        sensoren.append(sensor)
    return netz, sensoren


def nah(a, b):
    """True, wenn zwei Werte bis auf Rundungsfehler gleich sind."""
    return abs(a - b) < 1e-9


# Sensor.kalibriert gibt einen Sensor mit dem neuen Wert zurück
original = Sensor("T-01", "Büro 1", 21.5)
neu = original.kalibriert(-0.5)
assert als_tupel(neu) == ("T-01", "Büro 1", 21.0), (
    f'Sensor("T-01", "Büro 1", 21.5).kalibriert(-0.5) ergibt {als_tupel(neu)!r}, erwartet war ein Sensor '
    "('T-01', 'Büro 1', 21.0).\nTipp: Legen Sie mit Sensor(self.kennung, self.raum, …) einen neuen Sensor an."
)

# Sensor.kalibriert mit einem anderen Versatz (nicht fest hinschreiben!)
neu = Sensor("T-09", "Lager", 10.0).kalibriert(2.5)
assert als_tupel(neu) == ("T-09", "Lager", 12.5), (
    f'Sensor("T-09", "Lager", 10.0).kalibriert(2.5) ergibt {als_tupel(neu)!r}, erwartet war (\'T-09\', \'Lager\', 12.5).'
)

# Sensor.kalibriert verändert den ursprünglichen Sensor nicht
original = Sensor("T-01", "Büro 1", 21.5)
neu = original.kalibriert(-0.5)
assert original.wert == 21.5 and neu is not original, (
    f"Nach kalibriert(-0.5) hat der ursprüngliche Sensor den Wert {original.wert}"
    + (" und ist dasselbe Objekt wie das Ergebnis" if neu is original else "")
    + "; erwartet war 21.5 und ein neues Objekt.\nTipp: Ändern Sie nicht self.wert, sondern geben Sie einen neuen Sensor zurück."
)

# hinzufuegen hängt die Sensoren in der Reihenfolge an
netz, sensoren = beispielnetz()
assert isinstance(netz.sensoren, list) and len(netz.sensoren) == 3 and all(a is b for a, b in zip(netz.sensoren, sensoren)), (
    f"Nach drei Aufrufen von hinzufuegen enthält netz.sensoren {texte(netz.sensoren)}, erwartet waren die drei Sensoren "
    "aus dem Beispiel in dieser Reihenfolge."
)

# im_raum im Beispiel
netz, sensoren = beispielnetz()
ergebnis = netz.im_raum("Büro 1")
assert texte(ergebnis) == ["T-01 (Büro 1): 21.5 °C", "T-03 (Büro 1): 22.5 °C"], (
    f'netz.im_raum("Büro 1") ergibt {texte(ergebnis)}, erwartet waren die Sensoren T-01 und T-03.'
)

# im_raum gibt die Sensor-Objekte selbst zurück
netz, sensoren = beispielnetz()
ergebnis = netz.im_raum("Serverraum")
assert isinstance(ergebnis, list) and len(ergebnis) == 1 and ergebnis[0] is sensoren[1], (
    f'netz.im_raum("Serverraum") ergibt {ergebnis!r}; erwartet war eine Liste mit genau dem Sensor-Objekt T-02 '
    "(keine Kopie, kein Text).\nTipp: Hängen Sie sensor selbst an die Ergebnisliste an, nicht str(sensor)."
)

# im_raum für einen Raum ohne Sensor
netz, sensoren = beispielnetz()
ergebnis = netz.im_raum("Küche")
assert ergebnis == [], f'netz.im_raum("Küche") ergibt {ergebnis!r}, erwartet war [].'

# waermster im Beispiel
netz, sensoren = beispielnetz()
ergebnis = netz.waermster()
assert ergebnis is sensoren[1], (
    f"netz.waermster() ergibt {ergebnis}, erwartet war der Sensor T-02 (Serverraum): 24.0 °C selbst."
)

# waermster, wenn der wärmste zuletzt kommt (nicht fest hinschreiben!)
netz, sensoren = beispielnetz()
letzter = Sensor("T-04", "Lager", 30.0)
netz.hinzufuegen(letzter)
ergebnis = netz.waermster()
assert ergebnis is letzter, f"Mit einem Sensor T-04 mit 30.0 °C am Ende ergibt waermster() {ergebnis}, erwartet war T-04."

# waermster bei Gleichstand: der zuerst hinzugefügte
netz = Sensornetz()
erster = Sensor("A", "Büro 1", 25.0)
for sensor in [Sensor("X", "Büro 2", 19.0), erster, Sensor("B", "Lager", 25.0)]:
    netz.hinzufuegen(sensor)
ergebnis = netz.waermster()
assert ergebnis is erster, (
    f"Bei zwei Sensoren mit 25.0 °C ergibt waermster() {ergebnis}, erwartet war der zuerst hinzugefügte A.\n"
    "Tipp: Ersetzen Sie den bisher besten nur, wenn der neue Wert echt größer ist."
)

# waermster bei negativen Werten
netz = Sensornetz()
kaeltester_raum = [Sensor("K1", "Kühlhaus", -30.0), Sensor("K2", "Kühlhaus", -12.5), Sensor("K3", "Kühlhaus", -40.0)]
for sensor in kaeltester_raum:
    netz.hinzufuegen(sensor)
ergebnis = netz.waermster()
assert ergebnis is kaeltester_raum[1], (
    f"Bei den Werten -30.0, -12.5 und -40.0 ergibt waermster() {ergebnis}, erwartet war K2 mit -12.5 °C.\n"
    "Tipp: Beginnen Sie nicht mit dem Wert 0 als bisher bestem, sondern mit dem ersten Sensor oder None."
)

# waermster ohne Sensoren
ergebnis = Sensornetz().waermster()
assert ergebnis is None, f"Sensornetz().waermster() ergibt {ergebnis!r}, erwartet war None."

# kalibriert gibt ein neues Sensornetz mit korrigierten Werten zurück
netz, sensoren = beispielnetz()
neu = netz.kalibriert(-0.5)
werte = [als_tupel(sensor) for sensor in neu.sensoren] if isinstance(neu, Sensornetz) else neu
assert werte == [("T-01", "Büro 1", 21.0), ("T-02", "Serverraum", 23.5), ("T-03", "Büro 1", 22.0)], (
    f"netz.kalibriert(-0.5) enthält {werte!r}, erwartet war ein Sensornetz mit den Werten 21.0, 23.5 und 22.0."
)

# kalibriert lässt das ursprüngliche Netz und seine Sensoren unverändert
netz, sensoren = beispielnetz()
neu = netz.kalibriert(1.0)
assert [als_tupel(sensor) for sensor in netz.sensoren] == [als_tupel(s) for s in beispielnetz()[1]] and neu is not netz, (
    f"Nach netz.kalibriert(1.0) enthält das ursprüngliche Netz {texte(netz.sensoren)}; erwartet waren die alten Werte "
    "21.5, 24.0 und 22.5.\nTipp: Legen Sie ein neues Sensornetz an und füllen Sie es mit sensor.kalibriert(versatz)."
)

# Das neue Netz teilt keine Sensoren mit dem alten
netz, sensoren = beispielnetz()
neu = netz.kalibriert(0)
gemeinsam = [str(a) for a in neu.sensoren if any(a is b for b in netz.sensoren)]
assert gemeinsam == [] and neu.sensoren is not netz.sensoren, (
    f"Das kalibrierte Netz enthält dieselben Objekte wie das alte: {gemeinsam}; erwartet waren lauter neue Sensoren."
)

# kalibriert eines leeren Netzes
neu = Sensornetz().kalibriert(3)
assert isinstance(neu, Sensornetz) and neu.sensoren == [], f"Sensornetz().kalibriert(3) ergibt {neu!r}, erwartet war ein leeres Sensornetz."

# Die Ausgabe des Programms
erwartet = "T-01 (Büro 1): 21.5 °C\nT-03 (Büro 1): 22.5 °C\nWärmster: T-02 (Serverraum): 24.0 °C\nKorrigiert: T-02 (Serverraum): 23.5 °C"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Netze
zufall = Zufall(3040)
for runde in range(150):
    netz, sensoren = zufallsnetz(zufall, zufall.randint(0, 12))
    raum = zufall.choice(["Büro 1", "Büro 2", "Lager", "Serverraum", "Küche"])
    ergebnis = netz.im_raum(raum)
    erwartet = [sensor for sensor in sensoren if sensor.raum == raum]
    assert isinstance(ergebnis, list) and len(ergebnis) == len(erwartet) and all(a is b for a, b in zip(ergebnis, erwartet)), (
        f"Bei den Sensoren {texte(sensoren)} ergibt im_raum({raum!r}) {texte(ergebnis)}, erwartet war {texte(erwartet)}."
    )
    erwartet = None
    for sensor in sensoren:
        if erwartet is None or sensor.wert > erwartet.wert:
            erwartet = sensor
    ergebnis = netz.waermster()
    assert ergebnis is erwartet, f"Bei den Sensoren {texte(sensoren)} ergibt waermster() {ergebnis}, erwartet war {erwartet}."
    versatz = zufall.randint(-100, 100) / 10
    neu = netz.kalibriert(versatz)
    neue_werte = [sensor.wert for sensor in neu.sensoren]
    assert len(neue_werte) == len(sensoren) and all(nah(a, s.wert + versatz) for a, s in zip(neue_werte, sensoren)), (
        f"Bei den Sensoren {texte(sensoren)} ergibt kalibriert({versatz}) die Werte {neue_werte}."
    )

# Obere Grenze: 10 000 Sensoren
netz, sensoren = zufallsnetz(zufall, 10000)
erwartet = sensoren[0]
for sensor in sensoren:
    if sensor.wert > erwartet.wert:
        erwartet = sensor
neu = netz.kalibriert(-10)
assert netz.waermster() is erwartet and len(netz.im_raum("Lager")) == len([s for s in sensoren if s.raum == "Lager"]), (
    "Bei 10 000 Sensoren stimmen waermster() oder im_raum(\"Lager\") nicht."
)

# Obere Grenze: 10 000 Sensoren kalibrieren
assert len(neu.sensoren) == 10000 and nah(neu.waermster().wert, erwartet.wert - 10), (
    f"Bei 10 000 Sensoren hat das kalibrierte Netz {len(neu.sensoren)} Sensoren, erwartet waren 10 000 mit "
    f"{erwartet.wert - 10} °C als höchstem Wert."
)
