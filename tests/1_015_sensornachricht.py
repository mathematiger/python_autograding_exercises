# Automatisch erzeugt aus lehrkraft/muster/1_015_sensornachricht.py - nicht von Hand ändern.
# vorlage-hash: 4c21d2b32e974c32
# thema: texte_zahlen
# inhalt: Übung: Text zerlegen, rechnen, ausgeben

EINGABEN = ["K12:0231", "21"]

# Das Beispiel aus der Aufgabe
erwartet = "Sensor K12 misst 23.1 °C, Abweichung vom Sollwert: 2.1 Grad."
assert AUSGABE == erwartet, f'Bei den Eingaben "K12:0231" und "21" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}'

# Ein anderer Sensor, kälter als der Sollwert (nicht fest K12 hinschreiben!)
ausgabe = starte("B07:0185", "20")
erwartet = "Sensor B07 misst 18.5 °C, Abweichung vom Sollwert: -1.5 Grad."
if "185" in ausgabe:
    hinweis = "\nTipp: Die vier Ziffern sind Zehntelgrad. Teilen Sie die Zahl durch 10."
elif "1.5 Grad" in ausgabe and "-1.5" not in ausgabe:
    hinweis = "\nTipp: Rechnen Sie Temperatur minus Sollwert, dann ist die Abweichung bei Kälte negativ."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f'Bei den Eingaben "B07:0185" und "20" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Der Sollwert darf eine Nachkommastelle haben, und ganze Grade stehen mit .0 da
ausgabe = starte("R2a:0200", "19.5")
erwartet = "Sensor R2a misst 20.0 °C, Abweichung vom Sollwert: 0.5 Grad."
if "20 °C" in ausgabe:
    hinweis = "\nTipp: {temperatur:.1f} im f-String schreibt immer genau eine Nachkommastelle."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f'Bei den Eingaben "R2a:0200" und "19.5" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Der Name besteht aus genau den ersten drei Zeichen, ohne Doppelpunkt
ausgabe = starte("Lab:0219", "22")
erwartet = "Sensor Lab misst 21.9 °C, Abweichung vom Sollwert: -0.1 Grad."
if "Lab:" in ausgabe:
    hinweis = "\nTipp: nachricht[:3] sind die ersten drei Zeichen; nachricht[:4] enthält schon den Doppelpunkt."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f'Bei den Eingaben "Lab:0219" und "22" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}'
)

# Ränder: 0.0 °C bei Sollwert 0, 150.0 °C bei Sollwert 100, genau auf dem Sollwert
for nachricht_test, soll_test, erwartet in [
    ("S01:0000", "0", "Sensor S01 misst 0.0 °C, Abweichung vom Sollwert: 0.0 Grad."),
    ("S99:1500", "100", "Sensor S99 misst 150.0 °C, Abweichung vom Sollwert: 50.0 Grad."),
    ("K03:0215", "21.5", "Sensor K03 misst 21.5 °C, Abweichung vom Sollwert: 0.0 Grad."),
    ("K04:0005", "100", "Sensor K04 misst 0.5 °C, Abweichung vom Sollwert: -99.5 Grad."),
]:
    ausgabe = starte(nachricht_test, soll_test)
    assert ausgabe == erwartet, (
        f'Bei den Eingaben "{nachricht_test}" und "{soll_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )

# 40 zufällige Nachrichten und Sollwerte
zufall = Zufall(1015)
zeichen = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
for _ in range(40):
    name_test = zufall.choice(zeichen) + zufall.choice(zeichen) + zufall.choice(zeichen)
    zehntel = zufall.randint(0, 1500)
    soll_zehntel = zufall.randint(0, 1000)
    nachricht_test = f"{name_test}:{zehntel:04d}"
    soll_test = str(soll_zehntel // 10) if soll_zehntel % 10 == 0 else str(soll_zehntel / 10)
    # In Zehntelgrad gerechnet, damit kein Rundungsfehler entsteht
    differenz = zehntel - soll_zehntel
    vorzeichen = "-" if differenz < 0 else ""
    abweichung = f"{vorzeichen}{abs(differenz) // 10}.{abs(differenz) % 10}"
    erwartet = f"Sensor {name_test} misst {zehntel // 10}.{zehntel % 10} °C, Abweichung vom Sollwert: {abweichung} Grad."
    ausgabe = starte(nachricht_test, soll_test)
    assert ausgabe == erwartet, (
        f'Bei den Eingaben "{nachricht_test}" und "{soll_test}" erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}'
    )
