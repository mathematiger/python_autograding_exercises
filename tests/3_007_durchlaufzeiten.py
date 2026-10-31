# Automatisch erzeugt aus lehrkraft/muster/3_007_durchlaufzeiten.py - nicht von Hand ändern.
# vorlage-hash: 032dcfc22557a164
# text-hash: 156502b9f3bdd940
# thema: fehler
# inhalt: Fehler abfangen mit try/except

# Ganze Zahlen und Kommazahlen werden umgewandelt
for text, erwartet in [("42", 42.0), ("37.5", 37.5), ("0", 0.0), ("120", 120.0)]:
    try:
        ergebnis = als_minuten(text)
        fehler = None
    except Exception as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == erwartet, (
        f"als_minuten({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}; aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Wandeln Sie mit float(text) um. Eine Prüfung mit isdigit() erkennt keine Zahlen mit Punkt."
    )

# Leerzeichen am Rand stören nicht
ergebnis = als_minuten(" 37.5 ")
assert ergebnis == 37.5, f'als_minuten(" 37.5 ") ergibt {ergebnis!r}, erwartet war 37.5.'

# Unbrauchbare Texte ergeben None statt eines Absturzes
for text in ["n/a", "", "4S", "zwölf", "--", "1.2.3", "3..5"]:
    try:
        ergebnis = als_minuten(text)
        fehler = None
    except Exception as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis is None, (
        f"als_minuten({text!r}) muss None zurückgeben; Ergebnis: {ergebnis!r}, aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Fangen Sie den ValueError von float(...) mit try und except ValueError ab."
    )

# Das Beispiel aus der Aufgabe
try:
    ergebnis = auswerten(["40", "n/a", "50", "", "45"])
    fehler = None
except Exception as ausnahme:
    ergebnis = None
    fehler = ausnahme
assert fehler is None and ergebnis == (45.0, 2), (
    f'auswerten(["40", "n/a", "50", "", "45"]) ergibt {ergebnis!r}, erwartet war (45.0, 2); '
    f"aufgetretene Ausnahme: {fehler!r}.\n"
    "Tipp: Der Mittelwert ist die Summe der brauchbaren Werte geteilt durch deren Anzahl, nicht durch alle Werte."
)

# Weitere Messreihen (nicht fest hinschreiben!)
for werte, erwartet in [
    (["10", "20"], (15.0, 0)),
    (["12.5", "x", "7.5", "y", "z"], (10.0, 3)),
    (["90"], (90.0, 0)),
    (["0", "0", "30"], (10.0, 0)),
]:
    ergebnis = auswerten(werte)
    assert ergebnis == erwartet, f"auswerten({werte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ohne brauchbaren Wert ist der Mittelwert None
for werte, erwartet in [(["n/a"], (None, 1)), (["", "-"], (None, 2)), ([], (None, 0))]:
    try:
        ergebnis = auswerten(werte)
        fehler = None
    except ZeroDivisionError as ausnahme:
        ergebnis = None
        fehler = ausnahme
    assert fehler is None and ergebnis == erwartet, (
        f"auswerten({werte}) ergibt {ergebnis!r}, erwartet war {erwartet}; aufgetretene Ausnahme: {fehler!r}.\n"
        "Tipp: Ohne brauchbaren Wert dürfen Sie nicht teilen. Geben Sie dann None als Mittelwert zurück."
    )

# Viele zufällige Messreihen aus brauchbaren und kaputten Werten (nicht fest hinschreiben!)
zufall = Zufall(3007)
for runde in range(300):
    werte = []
    summe = 0
    brauchbar = 0
    for _ in range(runde // 20):
        if zufall.random() < 0.3:
            werte.append(zufall.choice(["", "n/a", "4S", "--", "zwölf", "1,5", "x"]))
        else:
            zahl = zufall.randint(0, 20000) / 2
            werte.append(" " * zufall.randint(0, 1) + str(zahl).removesuffix(".0"))
            summe = summe + zahl
            brauchbar = brauchbar + 1
    erwartet_fehler = len(werte) - brauchbar
    erwartet_mittel = summe / brauchbar if brauchbar > 0 else None
    ergebnis = auswerten(werte)
    if erwartet_mittel is None:
        richtig = ergebnis == (None, erwartet_fehler)
    else:
        richtig = ergebnis[1] == erwartet_fehler and ergebnis[0] is not None and abs(ergebnis[0] - erwartet_mittel) < 1e-6
    assert richtig, f"auswerten({werte}) ergibt {ergebnis!r}, erwartet war ({erwartet_mittel!r}, {erwartet_fehler})."

# 10 000 Werte, jeder zweite kaputt
werte = []
for nummer in range(10000):
    if nummer % 2 == 0:
        werte.append(str(nummer))
    else:
        werte.append("n/a")
ergebnis = auswerten(werte)
assert ergebnis == (4999.0, 5000), (
    f'Für die 10 000 Werte "0", "n/a", "2", "n/a", …, "9998", "n/a" ergibt auswerten {ergebnis!r}, '
    "erwartet war (4999.0, 5000)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "Mittlere Durchlaufzeit: 45.0 Minuten\nUnbrauchbare Werte: 2"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
