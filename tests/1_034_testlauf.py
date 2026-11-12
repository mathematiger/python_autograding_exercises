# Automatisch erzeugt aus lehrkraft/muster/1_034_testlauf.py - nicht von Hand ändern.
# vorlage-hash: cdd4174d2dcfaff4
# text-hash: 058e50712496ae12
# thema: kontrollfluss
# inhalt: Eingabeschleife bis "stop"

EINGABEN = ["ok", "ok", "fehler", "ok", "stop"]


def erwartete_ausgabe(ergebnisse):
    """Zählt mit count statt mit einer Schleife."""
    ok = ergebnisse.count("ok")
    schlecht = ergebnisse.count("fehler")
    return f"{ok + schlecht} Testfälle: {ok} bestanden, {schlecht} fehlgeschlagen"


def lauf(ergebnisse):
    """Startet das Programm mit diesen Ergebnissen und "stop"; liefert die Ausgabe oder den Abbruch."""
    try:
        return starte(*ergebnisse, "stop")
    except Exception as fehler:
        return f"(Abbruch: {fehler})"


def meldung(ergebnisse, ausgabe):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    text = ", ".join(ergebnisse + ["stop"])
    tipp = ""
    if "Abbruch" in ausgabe:
        tipp = "\nTipp: Lesen Sie am Ende des Schleifenblocks mit input die nächste Eingabe."
    return f"Bei den Eingaben {text} erwartet:\n{erwartete_ausgabe(ergebnisse)}\nIhr Programm gibt aus:\n{ausgabe}{tipp}"


# Das Beispiel aus der Aufgabe
assert AUSGABE == erwartete_ausgabe(["ok", "ok", "fehler", "ok"]), meldung(["ok", "ok", "fehler", "ok"], AUSGABE)

# Andere Ergebnisse (nicht fest hinschreiben!)
ergebnisse = ["fehler", "ok", "fehler", "fehler", "ok", "fehler"]
ausgabe = lauf(ergebnisse)
assert ausgabe == erwartete_ausgabe(ergebnisse), meldung(ergebnisse, ausgabe)

# Nur bestandene Testfälle
ergebnisse = ["ok", "ok"]
ausgabe = lauf(ergebnisse)
assert ausgabe == erwartete_ausgabe(ergebnisse), meldung(ergebnisse, ausgabe)

# Nur ein fehlgeschlagener Testfall: Auch die erste Eingabe wird mitgezählt
ergebnisse = ["fehler"]
ausgabe = lauf(ergebnisse)
assert ausgabe == erwartete_ausgabe(ergebnisse), (
    meldung(ergebnisse, ausgabe)
    + "\nTipp: Werten Sie in der Schleife zuerst die gerade gelesene Eingabe aus und lesen Sie erst danach die nächste."
)

# Sofort "stop": kein Testfall
ausgabe = lauf([])
assert ausgabe == "0 Testfälle: 0 bestanden, 0 fehlgeschlagen", (
    f"Bei der Eingabe stop erwartet:\n0 Testfälle: 0 bestanden, 0 fehlgeschlagen\nIhr Programm gibt aus:\n{ausgabe}\n"
    "Tipp: Die Schleife darf gar nicht laufen, wenn schon die erste Eingabe stop ist."
)

# Eine while-Schleife wird benutzt
assert verwendet("while"), 'Benutzen Sie eine while-Schleife, die läuft, solange die Eingabe nicht "stop" ist.'

# 40 zufällige Testläufe
zufall = Zufall(1034)
for laenge in range(40):
    ergebnisse = [zufall.choice(["ok", "fehler"]) for _ in range(laenge % 12)]
    ausgabe = lauf(ergebnisse)
    assert ausgabe == erwartete_ausgabe(ergebnisse), meldung(ergebnisse, ausgabe)

# Obere Grenze: 200 Testfälle
ergebnisse = ["ok", "fehler", "ok", "ok"] * 50
ausgabe = lauf(ergebnisse)
assert ausgabe == erwartete_ausgabe(ergebnisse), (
    f"Bei 200 Ergebnissen (150-mal ok, 50-mal fehler) erwartet:\n{erwartete_ausgabe(ergebnisse)}\n"
    f"Ihr Programm gibt aus:\n{ausgabe}"
)
