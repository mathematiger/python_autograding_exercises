# Automatisch erzeugt aus lehrkraft/muster/1_021_leasing.py - nicht von Hand ändern.
# vorlage-hash: e51785a2d6d27c9b
# text-hash: 508bcd1893d405e9
# thema: kontrollfluss
# inhalt: Übung: Bedingungen

EINGABEN = ["15", "24", "ja"]


def erwartete_ausgabe(anzahl, monate, budget):
    """Baut die Ausgabe für die drei Eingaben (budget ist "ja" oder "nein"), Regel für Regel einzeln geprüft."""
    empfehlung = "Kauf"
    if anzahl >= 50:
        empfehlung = "Kauf mit Mengenrabatt"
    if budget == "nein":
        empfehlung = "Verschieben"
    if anzahl >= 5:
        if monate < 36:
            empfehlung = "Leasing"
        if budget == "nein":
            empfehlung = "Leasing"
    return f"{anzahl} Geräte für {monate} Monate\nEmpfehlung: {empfehlung}"


def meldung(anzahl, monate, budget, ausgabe, tipp=""):
    """Baut die Fehlermeldung für einen Fall."""
    erwartet = erwartete_ausgabe(anzahl, monate, budget)
    return f"Bei den Eingaben {anzahl}, {monate} und {budget} erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{tipp}"


def pruefe_fall(anzahl, monate, budget, tipp=""):
    """Startet das Programm mit den drei Eingaben; gibt None zurück, wenn es stimmt, sonst die Fehlermeldung."""
    try:
        ausgabe = starte(str(anzahl), str(monate), budget)
    except Exception as abbruch:
        # starte meldet einen Abbruch des Programms als eigene Ausnahme mit dem Text der Fehlermeldung
        ausgabe = f"(Abbruch: {abbruch})"
        if "`empfehlung` gibt es nicht" in str(abbruch):
            tipp = "\nTipp: Mit else am Ende bekommt empfehlung in jedem Fall einen Wert."
    if ausgabe == erwartete_ausgabe(anzahl, monate, budget):
        return None
    return meldung(anzahl, monate, budget, ausgabe, tipp)


# Das Beispiel aus der Aufgabe: Leasing
assert AUSGABE == erwartete_ausgabe(15, 24, "ja"), meldung(15, 24, "ja", AUSGABE)

# Längere Nutzung mit freiem Budget: Kauf (nicht fest hinschreiben!)
fehler = pruefe_fall(15, 48, "ja", "\nTipp: Bei 48 Monaten und freiem Budget passt Regel 1 nicht.")
assert fehler is None, fehler

# Wenige Geräte ohne Budget: Verschieben, auch bei kurzer Nutzung
for monate in [24, 48]:
    fehler = pruefe_fall(3, monate, "nein", "\nTipp: Leasing gibt es erst ab 5 Geräten; ohne Budget heißt es dann Verschieben.")
    assert fehler is None, fehler

# Ohne Budget wird ab 5 Geräten geleast, auch bei langer Nutzung
for anzahl in [5, 80]:
    fehler = pruefe_fall(anzahl, 60, "nein", "\nTipp: In Regel 1 steht „oder kein Budget frei“; setzen Sie Klammern um den or-Teil.")
    assert fehler is None, fehler

# Viele Geräte: Mengenrabatt bei langer Nutzung, Leasing bei kurzer
for anzahl, monate in [(80, 48), (80, 12)]:
    fehler = pruefe_fall(anzahl, monate, "ja", "\nTipp: Die Regeln werden von oben nach unten geprüft; Regel 1 kommt vor Regel 3.")
    assert fehler is None, fehler

# Wenige Geräte mit kurzer Nutzung und freiem Budget: Kauf, weil die Leasingfirma erst ab 5 vermietet
fehler = pruefe_fall(4, 12, "ja", "\nTipp: Für Leasing müssen mindestens 5 Geräte gebraucht werden, verknüpft mit and.")
assert fehler is None, fehler

# An den Grenzen: 4 und 5 Geräte, 35 und 36 Monate, 49 und 50 Geräte
for anzahl, monate, budget in [
    (4, 20, "nein"), (5, 20, "ja"), (10, 35, "ja"), (10, 36, "ja"), (49, 40, "ja"), (50, 40, "ja"), (50, 35, "ja"),
]:
    fehler = pruefe_fall(anzahl, monate, budget, "\nTipp: „mindestens 5“ heißt >= 5, „kürzer als 36“ heißt < 36.")
    assert fehler is None, fehler

# Ränder: 1 und 1000 Geräte, 1 und 60 Monate
for anzahl, monate, budget in [(1, 1, "ja"), (1, 60, "nein"), (1000, 1, "ja"), (1000, 60, "ja"), (1000, 60, "nein")]:
    fehler = pruefe_fall(anzahl, monate, budget)
    assert fehler is None, fehler

# 60 zufällige Anfragen
zufall = Zufall(1021)
for _ in range(60):
    anzahl = zufall.choice([zufall.randint(1, 60), zufall.randint(1, 1000)])
    monate = zufall.randint(1, 60)
    budget = zufall.choice(["ja", "nein"])
    fehler = pruefe_fall(anzahl, monate, budget)
    assert fehler is None, fehler
