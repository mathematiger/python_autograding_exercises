# Automatisch erzeugt aus lehrkraft/muster/1_047_rolllaeden.py - nicht von Hand ändern.
# vorlage-hash: e7cfcc4687b3bd52
# text-hash: 6fc8fb5c6a83545f
# thema: datenstrukturen
# inhalt: Tupel im Dictionary

EINGABEN = ["R2", "Küche", "30"]

VORHER = {"R1": ("Wohnzimmer", 100), "R2": ("Küche", 0), "R3": ("Bad", 50)}


def ausgabe_bei(kennung, raum, oeffnung):
    """Startet das Programm mit einer Meldung; ein Abbruch wird als Text zurückgegeben."""
    try:
        return starte(kennung, raum, str(oeffnung))
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"


def erwartete_zeilen(kennung, raum, oeffnung):
    """Die erwartete Ausgabe als Liste von Zeilen."""
    if kennung in VORHER:
        alter_raum, alte_oeffnung = VORHER[kennung]
        zeilen = [f"{kennung} bekannt: vorher {alter_raum} {alte_oeffnung} %"]
    else:
        zeilen = [f"{kennung} neu"]
    tabelle = dict(VORHER)
    tabelle[kennung] = (raum, oeffnung)
    zeilen.append("Alle Rollläden:")
    for name, (ort, prozent) in tabelle.items():
        zeilen.append(f"{name} {ort} {prozent} %")
    return zeilen


def zeilen_von(ausgabe):
    """Die Zeilen der Ausgabe ohne leere Zeilen, jede vergleichbar gemacht."""
    return [vergleichbar(zeile) for zeile in ausgabe.splitlines() if zeile.strip()]


def meldung(kennung, raum, oeffnung, ausgabe):
    """Fehlermeldung mit Eingabe, erwarteter und tatsächlicher Ausgabe."""
    erwartet = "\n".join(erwartete_zeilen(kennung, raum, oeffnung))
    return f"Bei Eingabe {kennung}, {raum} und {oeffnung} erwartet:\n{erwartet}\nIhr Programm:\n{ausgabe}"


def passt(kennung, raum, oeffnung, ausgabe):
    """True, wenn die Ausgabe Zeile für Zeile (vergleichbar gemacht) der erwarteten entspricht."""
    return zeilen_von(ausgabe) == [vergleichbar(zeile) for zeile in erwartete_zeilen(kennung, raum, oeffnung)]


# Für den bekannten Rollladen R2 stehen der alte Raum und die alte Öffnung in der ersten Zeile
erste_zeile = zeilen_von(AUSGABE)[0] if zeilen_von(AUSGABE) else ""
assert erste_zeile == vergleichbar("R2 bekannt: vorher Küche 0 %"), (
    meldung("R2", "Küche", 30, AUSGABE) + "\nTipp: Mit alter_raum, alte_oeffnung = rolllaeden[kennung] packen Sie das Tupel aus, "
    "bevor Sie den neuen Wert eintragen."
)

# Die übrigen Rollläden stehen unverändert in der Ausgabe
fehlend = []
for name, (ort, prozent) in VORHER.items():
    if name != "R2" and vergleichbar(f"{name} {ort} {prozent} %") not in zeilen_von(AUSGABE):
        fehlend.append(f"{name} {ort} {prozent} %")
assert fehlend == [], (
    f"In der Ausgabe fehlen die Zeilen {fehlend}.\n{meldung('R2', 'Küche', 30, AUSGABE)}\n"
    "Tipp: Packen Sie in der Schleife eintrag in zwei Variablen aus und geben Sie Kennung, Raum und Öffnung aus."
)

# R2 steht mit der neuen Öffnung in der Liste, alles in der richtigen Reihenfolge
assert passt("R2", "Küche", 30, AUSGABE), (
    meldung("R2", "Küche", 30, AUSGABE) + "\nTipp: rolllaeden[kennung] = (raum, oeffnung) trägt die neue Meldung als Tupel ein."
)

# Ein bekannter Rollladen mit anderem Raum und anderer Öffnung (nicht fest hinschreiben!)
ausgabe = ausgabe_bei("R1", "Besprechung", 40)
assert passt("R1", "Besprechung", 40, ausgabe), meldung("R1", "Besprechung", 40, ausgabe)

# Ein neuer Rollladen wird gemeldet und hinten angehängt
ausgabe = ausgabe_bei("R4", "Flur", 80)
assert passt("R4", "Flur", 80, ausgabe), (
    meldung("R4", "Flur", 80, ausgabe) + "\nTipp: Prüfen Sie mit if kennung in rolllaeden:, ob die Kennung bekannt ist; "
    "sonst gibt es nichts nachzuschlagen."
)

# Auch der letzte bekannte Rollladen lässt sich ändern
ausgabe = ausgabe_bei("R3", "Bad", 100)
assert passt("R3", "Bad", 100, ausgabe), meldung("R3", "Bad", 100, ausgabe)

# Randfall: Öffnung 0 bei einem neuen Rollladen
ausgabe = ausgabe_bei("R10", "Lager", 0)
assert passt("R10", "Lager", 0, ausgabe), meldung("R10", "Lager", 0, ausgabe)

# Viele zufällige Meldungen
zufall = Zufall(1047)
kennungen = ["R1", "R2", "R3", "R4", "R5", "R7", "R12"]
raeume = ["Küche", "Bad", "Flur", "Wohnzimmer", "Lager", "Empfang", "Serverraum"]
for _ in range(30):
    kennung = zufall.choice(kennungen)
    raum = zufall.choice(raeume)
    oeffnung = zufall.randint(0, 100)
    ausgabe = ausgabe_bei(kennung, raum, oeffnung)
    assert passt(kennung, raum, oeffnung, ausgabe), meldung(kennung, raum, oeffnung, ausgabe)

# Genau so wie verlangt: Kennung, Raum und Öffnung mit Leerzeichen und % (ohne Klammern und Anführungszeichen)
zeilen_genau = [zeile.strip() for zeile in AUSGABE.splitlines()]
assert "R2 bekannt: vorher Küche 0 %" in zeilen_genau and "R1 Wohnzimmer 100 %" in zeilen_genau, (
    f"Erwartet waren genau die Zeilen \"R2 bekannt: vorher Küche 0 %\" und \"R1 Wohnzimmer 100 %\", Ihr Programm gibt aus:\n{AUSGABE}\n"
    "Tipp: Packen Sie das Tupel aus und setzen Sie die Teile in einen f-String ein, statt das ganze Tupel auszugeben."
)
