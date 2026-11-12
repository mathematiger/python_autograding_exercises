# Automatisch erzeugt aus lehrkraft/muster/1_015_sensornachricht.py - nicht von Hand ändern.
# vorlage-hash: f489e8fe19523e85
# text-hash: cf803c55536f6ffb
# thema: texte_zahlen
# inhalt: Übung: Text zerlegen, rechnen, ausgeben

EINGABEN = [" k12:0231", "21"]


def passt(ausgabe, erwartet):
    """Vergleicht locker; nur Name (groß, ohne Doppelpunkt) und Zahlen (eine Nachkommastelle) müssen genau stimmen.

    Großbuchstaben, genau drei Zeichen und eine Nachkommastelle verlangt die Aufgabe ausdrücklich,
    Leerzeichen und Satzzeichen im übrigen Satz nicht.
    """
    woerter = erwartet.split()
    genau = [woerter[1], woerter[3], woerter[-2]]
    mit_doppelpunkt = woerter[1] + ":"
    return (
        vergleichbar(ausgabe) == vergleichbar(erwartet)
        and all(teil in ausgabe for teil in genau)
        and mit_doppelpunkt not in ausgabe
    )

# Das Beispiel aus der Aufgabe, zunächst locker (Groß-/Kleinschreibung und Satzzeichen zählen hier noch nicht)
erwartet = "Sensor K12 misst 23.1 °C, Abweichung vom Sollwert: 2.1 Grad."
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), (
    f'Bei den Eingaben " k12:0231" und "21" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}\n'
    "Tipp: Die vier Ziffern sind Zehntelgrad; {abweichung:.1f} im f-String zeigt genau eine Nachkommastelle."
)

# Das Beispiel aus der Aufgabe, genau: Name groß und ohne Doppelpunkt, Zahlen mit einer Nachkommastelle
if "k12" in AUSGABE:
    hinweis = "\nTipp: upper() macht aus Kleinbuchstaben Großbuchstaben."
elif "K12:" in AUSGABE:
    hinweis = "\nTipp: nachricht[:3] sind die ersten drei Zeichen; nachricht[:4] enthält schon den Doppelpunkt."
else:
    hinweis = ""
assert passt(AUSGABE, erwartet), f'Bei den Eingaben " k12:0231" und "21" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}{hinweis}'

# Ein anderer Sensor, kälter als der Sollwert (nicht fest K12 hinschreiben!)
ausgabe = starte("B07:0185", "20")
erwartet = "Sensor B07 misst 18.5 °C, Abweichung vom Sollwert: -1.5 Grad."
if "185" in ausgabe:
    hinweis = "\nTipp: Die vier Ziffern sind Zehntelgrad. Teilen Sie die Zahl durch 10."
elif "1.5 Grad" in ausgabe and "-1.5" not in ausgabe:
    hinweis = "\nTipp: Rechnen Sie Temperatur minus Sollwert, dann ist die Abweichung bei Kälte negativ."
else:
    hinweis = ""
assert passt(ausgabe, erwartet), (
    f'Bei den Eingaben "B07:0185" und "20" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Der Sollwert darf eine Nachkommastelle haben, und ganze Grade stehen mit .0 da
ausgabe = starte("R27:0200", "19.5")
erwartet = "Sensor R27 misst 20.0 °C, Abweichung vom Sollwert: 0.5 Grad."
if "20 °C" in ausgabe:
    hinweis = "\nTipp: {temperatur:.1f} im f-String schreibt immer genau eine Nachkommastelle."
else:
    hinweis = ""
assert passt(ausgabe, erwartet), (
    f'Bei den Eingaben "R27:0200" und "19.5" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Der Name besteht aus genau den ersten drei Zeichen, ohne Doppelpunkt
ausgabe = starte("LAB:0219", "22")
erwartet = "Sensor LAB misst 21.9 °C, Abweichung vom Sollwert: -0.1 Grad."
if "LAB:" in ausgabe:
    hinweis = "\nTipp: nachricht[:3] sind die ersten drei Zeichen; nachricht[:4] enthält schon den Doppelpunkt."
else:
    hinweis = ""
assert passt(ausgabe, erwartet), (
    f'Bei den Eingaben "LAB:0219" und "22" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Ein Name in Kleinbuchstaben wird groß angezeigt
ausgabe = starte("srv:0264", "18")
erwartet = "Sensor SRV misst 26.4 °C, Abweichung vom Sollwert: 8.4 Grad."
if "srv" in ausgabe:
    hinweis = "\nTipp: upper() macht aus Kleinbuchstaben Großbuchstaben."
else:
    hinweis = ""
assert passt(ausgabe, erwartet), (
    f'Bei den Eingaben "srv:0264" und "18" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Leerzeichen vor und hinter der Nachricht stören nicht
erwartet = "Sensor E05 misst 17.2 °C, Abweichung vom Sollwert: -3.8 Grad."
try:
    ausgabe = starte("   E05:0172   ", "21")
except Exception as fehler:
    # Ohne strip() bricht int(...) ab, weil vor den Ziffern noch Zeichen stehen; dann soll der Tipp erscheinen
    ausgabe = f"(Abbruch: {fehler})"
assert passt(ausgabe, erwartet), (
    f'Bei den Eingaben "   E05:0172   " und "21" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}\n'
    "Tipp: strip() entfernt die Leerzeichen am Rand; danach stehen Name und Ziffern an den gewohnten Stellen. "
    "Speichern Sie das Ergebnis wieder in nachricht, strip() allein ändert den Text nicht."
)

# Ränder: 0.0 °C und 50.0 °C, Sollwert 15 und 30, genau auf dem Sollwert
for nachricht_test, soll_test, erwartet in [
    ("S01:0000", "15", "Sensor S01 misst 0.0 °C, Abweichung vom Sollwert: -15.0 Grad."),
    ("S99:0500", "30", "Sensor S99 misst 50.0 °C, Abweichung vom Sollwert: 20.0 Grad."),
    ("K03:0215", "21.5", "Sensor K03 misst 21.5 °C, Abweichung vom Sollwert: 0.0 Grad."),
    ("K04:0005", "30", "Sensor K04 misst 0.5 °C, Abweichung vom Sollwert: -29.5 Grad."),
]:
    ausgabe = starte(nachricht_test, soll_test)
    assert passt(ausgabe, erwartet), (
        f'Bei den Eingaben "{nachricht_test}" und "{soll_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )

# 40 zufällige Nachrichten und Sollwerte
zufall = Zufall(1015)
zeichen = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
for _ in range(40):
    name_test = zufall.choice(zeichen) + zufall.choice(zeichen) + zufall.choice(zeichen)
    zehntel = zufall.randint(0, 500)
    soll_zehntel = zufall.randint(150, 300)
    links = " " * zufall.randint(0, 3)
    rechts = " " * zufall.randint(0, 3)
    nachricht_test = f"{links}{name_test}:{zehntel:04d}{rechts}"
    soll_test = str(soll_zehntel // 10) if soll_zehntel % 10 == 0 else str(soll_zehntel / 10)
    # In Zehntelgrad gerechnet, damit kein Rundungsfehler entsteht
    differenz = zehntel - soll_zehntel
    vorzeichen = "-" if differenz < 0 else ""
    abweichung = f"{vorzeichen}{abs(differenz) // 10}.{abs(differenz) % 10}"
    erwartet = (
        f"Sensor {name_test.upper()} misst {zehntel // 10}.{zehntel % 10} °C, Abweichung vom Sollwert: {abweichung} Grad."
    )
    ausgabe = starte(nachricht_test, soll_test)
    assert passt(ausgabe, erwartet), (
        f'Bei den Eingaben "{nachricht_test}" und "{soll_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )
