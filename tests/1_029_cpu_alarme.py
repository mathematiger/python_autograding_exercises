# Automatisch erzeugt aus lehrkraft/muster/1_029_cpu_alarme.py - nicht von Hand ändern.
# vorlage-hash: 28c57836e560042d
# text-hash: 6a5a710de09a3d6f
# thema: datenstrukturen
# inhalt: Liste mit append aufbauen

EINGABEN = ["45,91,78,85,80,97,60", "80"]


def erwartete_ausgabe(werte, schwelle):
    """Baut die erwartete Ausgabe, ohne append zu benutzen."""
    zu_hoch = [wert for wert in werte if wert > schwelle]
    return f"Alarme über {schwelle} %: {zu_hoch}\nDas sind {len(zu_hoch)} von {len(werte)} Messwerten."


def hinweis_zu(ausgabe, werte, schwelle):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    gleich_dabei = [wert for wert in werte if wert >= schwelle]
    zu_hoch = [wert for wert in werte if wert > schwelle]
    if gleich_dabei != zu_hoch and ausgabe.startswith(f"Alarme über {schwelle} %: {gleich_dabei}\n"):
        return "\nTipp: Ein Wert genau gleich dem Schwellwert löst keinen Alarm aus. Benutzen Sie > statt >=."
    if len(zu_hoch) > 1 and ausgabe.startswith(f"Alarme über {schwelle} %: [{zu_hoch[-1]}]\n"):
        return (
            "\nTipp: Nur der letzte Wert steht in der Liste. Legen Sie alarme = [] vor der Schleife an, "
            "nicht in ihr, sonst fängt die Liste bei jedem Durchlauf wieder leer an."
        )
    if f"'{werte[0]}'" in ausgabe or (zu_hoch and f"'{zu_hoch[0]}'" in ausgabe):
        return "\nTipp: Hängen Sie die Zahl zahl an, nicht den Text wert; sonst stehen Anführungszeichen in der Liste."
    if ausgabe.startswith(f"Alarme über {schwelle} %: {werte}\n") and werte != zu_hoch:
        return "\nTipp: Es landet jeder Wert in der Liste. Hängen Sie nur an, wenn zahl > schwelle ist."
    return ""


def meldung(werte, schwelle, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    text = ",".join(str(wert) for wert in werte)
    return (
        f"Bei den Eingaben {text} und {schwelle} erwartet:\n{erwartete_ausgabe(werte, schwelle)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, werte, schwelle)}"
    )


def pruefe_lauf(werte, schwelle):
    """Startet das Programm mit diesen Messwerten und liefert die Ausgabe."""
    return starte(",".join(str(wert) for wert in werte), str(schwelle))


# Das Beispiel aus der Aufgabe: drei Werte über 80
BEISPIEL = [45, 91, 78, 85, 80, 97, 60]
assert AUSGABE == erwartete_ausgabe(BEISPIEL, 80), meldung(BEISPIEL, 80, AUSGABE)

# Andere Messwerte und anderer Schwellwert (nicht fest hinschreiben!)
werte = [12, 55, 70, 33, 71]
ausgabe = pruefe_lauf(werte, 50)
assert ausgabe == erwartete_ausgabe(werte, 50), meldung(werte, 50, ausgabe)

# Kein Wert liegt über dem Schwellwert: Die Liste bleibt leer
werte = [20, 35, 41, 18]
ausgabe = pruefe_lauf(werte, 90)
assert ausgabe == erwartete_ausgabe(werte, 90), meldung(werte, 90, ausgabe)

# Alle Werte liegen über dem Schwellwert
werte = [88, 93, 99]
ausgabe = pruefe_lauf(werte, 75)
assert ausgabe == erwartete_ausgabe(werte, 75), meldung(werte, 75, ausgabe)

# Werte genau auf dem Schwellwert lösen keinen Alarm aus
werte = [70, 71, 70, 69, 100]
ausgabe = pruefe_lauf(werte, 70)
assert ausgabe == erwartete_ausgabe(werte, 70), meldung(werte, 70, ausgabe)

# Rand: Schwellwert 0, ein Messwert 0 löst keinen Alarm aus
werte = [0, 1, 0, 5]
ausgabe = pruefe_lauf(werte, 0)
assert ausgabe == erwartete_ausgabe(werte, 0), meldung(werte, 0, ausgabe)

# Rand: Schwellwert 100, kein Wert kann darüber liegen
werte = [100, 99, 100]
ausgabe = pruefe_lauf(werte, 100)
assert ausgabe == erwartete_ausgabe(werte, 100), meldung(werte, 100, ausgabe)

# Nur ein einziger Messwert
werte = [64]
ausgabe = pruefe_lauf(werte, 60)
assert ausgabe == erwartete_ausgabe(werte, 60), meldung(werte, 60, ausgabe)

# append wird benutzt
assert verwendet("append"), "Bauen Sie die Liste alarme mit alarme.append(zahl) auf."

# 40 zufällige Messreihen
zufall = Zufall(1029)
for _ in range(40):
    werte = [zufall.randint(0, 100) for _ in range(zufall.randint(1, 12))]
    schwelle = zufall.choice(werte + [zufall.randint(0, 100)])
    ausgabe = pruefe_lauf(werte, schwelle)
    assert ausgabe == erwartete_ausgabe(werte, schwelle), meldung(werte, schwelle, ausgabe)

# Obere Grenze: 30 Messwerte
werte = [(zahl * 37) % 101 for zahl in range(30)]
ausgabe = pruefe_lauf(werte, 50)
assert ausgabe == erwartete_ausgabe(werte, 50), meldung(werte, 50, ausgabe)
