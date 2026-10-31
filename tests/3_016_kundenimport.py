# Automatisch erzeugt aus lehrkraft/muster/3_016_kundenimport.py - nicht von Hand ändern.
# vorlage-hash: 2e3500e1cb49d346
# text-hash: b0a7a491603de9c9
# thema: fehler
# inhalt: Traceback lesen

# fehlerstellen() gibt drei Tupel (funktion, zeile, fehlerart) zurück
stellen = fehlerstellen()
form_ok = isinstance(stellen, (list, tuple)) and len(stellen) == 3
for stelle in stellen if form_ok else []:
    if not (isinstance(stelle, tuple) and len(stelle) == 3 and isinstance(stelle[0], str) and type(stelle[1]) is int and isinstance(stelle[2], str)):
        form_ok = False
assert form_ok, (
    f"fehlerstellen() ergibt {stellen!r}; erwartet waren drei Tupel in einer Liste (funktion, zeile, fehlerart), "
    'zum Beispiel ("main", 5, "TypeError"): ein Text, eine ganze Zahl und ein Text.'
)

# Die Art jeder Ausnahme steht in der letzten Zeile des Tracebacks
arten = [stelle[2] for stelle in stellen]
assert arten == ["ValueError", "KeyError", "ZeroDivisionError"], (
    f"Die Fehlerarten in fehlerstellen() sind {arten}; das stimmt nicht.\n"
    "Tipp: Die letzte Zeile jedes Tracebacks beginnt mit der Art der Ausnahme, vor dem Doppelpunkt."
)

# Funktion und Zeile stehen im untersten File-Eintrag
falsch = []
for nummer, (stelle, richtig) in enumerate(zip(stellen, [("lies_alter", 3), ("durchschnittsalter", 10), ("durchschnittsalter", 13)]), start=1):
    if stelle[:2] != richtig:
        falsch.append(f"Traceback {nummer}: Sie geben {stelle[:2]!r} an")
assert falsch == [], (
    "Funktion und Zeile stimmen nicht:\n" + "\n".join(falsch) + "\n"
    "Tipp: Der unterste Eintrag File \"import.py\", line …, in … ist die Stelle, an der der Fehler passiert ist; "
    "line 17 in <module> ist nur der erste Aufruf."
)

# Das Beispiel aus der Aufgabe
kunden = [
    {"name": "Ada", "alter": "36"},
    {"name": "Bo", "alter": "unbekannt"},
    {"name": "Cem"},
    {"name": "Dana", "alter": "41"},
]
try:
    ergebnis = durchschnittsalter(kunden)
except (KeyError, ValueError, ZeroDivisionError) as fehler:
    ergebnis = fehler
assert ergebnis == 38.5, (
    f"durchschnittsalter(...) mit dem Beispiel aus der Aufgabe ergibt {ergebnis!r}, erwartet war 38.5.\n"
    "Tipp: Ein fehlender Schlüssel löst KeyError aus, ein Text wie 'unbekannt' ValueError; sortieren Sie beide vorher aus."
)

# Ohne gültiges Alter: None statt ZeroDivisionError
for kunden in [[{"name": "Eli", "alter": ""}], [], [{"name": "Fe"}, {"name": "Gus", "alter": "k. a."}]]:
    try:
        ergebnis = durchschnittsalter(kunden)
    except (KeyError, ValueError, ZeroDivisionError) as fehler:
        ergebnis = fehler
    assert ergebnis is None, (
        f"durchschnittsalter({kunden}) ergibt {ergebnis!r}, erwartet war None.\n"
        "Tipp: Ohne gültigen Datensatz ist anzahl 0; prüfen Sie das vor dem Teilen."
    )

# Nur Ziffern zählen: Leerzeichen, Minus, Punkt und Buchstaben nicht
kunden = [
    {"name": "A", "alter": "30"},
    {"name": "B", "alter": " 50"},
    {"name": "C", "alter": "-5"},
    {"name": "D", "alter": "4.5"},
    {"name": "E", "alter": "20a"},
    {"name": "F", "alter": "60 "},
    {"name": "G", "alter": "40"},
]
try:
    ergebnis = durchschnittsalter(kunden)
except ValueError as fehler:
    ergebnis = fehler
assert ergebnis == 35.0, (
    f"durchschnittsalter(...) mit den Altern '30', ' 50', '-5', '4.5', '20a', '60 ' und '40' ergibt {ergebnis!r}, "
    "erwartet war 35.0: Gültig sind nur '30' und '40'.\nTipp: text.isdigit() ist nur True, wenn alle Zeichen Ziffern sind."
)

# Ränder 0 und 150, Rundung auf eine Stelle
for alter, erwartet in [(["0"], 0.0), (["150", "0"], 75.0), (["20", "21", "21"], 20.7), (["007"], 7.0)]:
    kunden = [{"name": f"K{nummer}", "alter": text} for nummer, text in enumerate(alter)]
    ergebnis = durchschnittsalter(kunden)
    assert ergebnis == erwartet, f"durchschnittsalter mit den Altern {alter} ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die Datensätze bleiben unverändert
kunden = [{"name": "Ada", "alter": "36"}, {"name": "Cem"}]
durchschnittsalter(kunden)
assert kunden == [{"name": "Ada", "alter": "36"}, {"name": "Cem"}], (
    f"Nach durchschnittsalter(kunden) ist kunden {kunden!r}; die Datensätze sollen unverändert bleiben."
)


# Vergleichslösung: gültige Alter erst sammeln, Ziffern einzeln prüfen
def durchschnitt_von_hand(kunden):
    """Sammelt die gültigen Alter in einer Liste und rechnet daraus den Durchschnitt."""
    gueltig = []
    for datensatz in kunden:
        if "alter" not in datensatz or datensatz["alter"] == "":
            continue
        if all(zeichen in "0123456789" for zeichen in datensatz["alter"]):
            gueltig.append(int(datensatz["alter"]))
    if not gueltig:
        return None
    return round(sum(gueltig) / len(gueltig), 1)


# 300 zufällige Exportdateien
zufall = Zufall(3016)
for _ in range(300):
    kunden = []
    for nummer in range(zufall.randint(0, 8)):
        datensatz = {"name": f"K{nummer}"}
        art = zufall.randint(0, 5)
        if art <= 2:
            datensatz["alter"] = str(zufall.randint(0, 150))
        elif art == 3:
            datensatz["alter"] = zufall.choice(["", "unbekannt", "k. a.", " 42", "-3", "1.5", "x7", "12 "])
        elif art == 4:
            datensatz["alter"] = "".join(zufall.choice("ab1 -.") for _ in range(zufall.randint(0, 10)))
        kunden.append(datensatz)
    erwartet = durchschnitt_von_hand(kunden)
    try:
        ergebnis = durchschnittsalter(kunden)
    except (KeyError, ValueError, ZeroDivisionError) as fehler:
        ergebnis = fehler
    assert ergebnis == erwartet, f"durchschnittsalter({kunden}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 100 000 Datensätze
kunden = []
for nummer in range(100000):
    if nummer % 4 == 0:
        kunden.append({"name": f"K{nummer}"})
    elif nummer % 4 == 1:
        kunden.append({"name": f"K{nummer}", "alter": "unbekannt"})
    else:
        kunden.append({"name": f"K{nummer}", "alter": str(nummer % 151)})
erwartet = durchschnitt_von_hand(kunden)
ergebnis = durchschnittsalter(kunden)
assert ergebnis == erwartet, f"Bei 100 000 Datensätzen ergibt durchschnittsalter {ergebnis!r}, erwartet war {erwartet}."

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "[('lies_alter', 3, 'ValueError'), ('durchschnittsalter', 10, 'KeyError'), "
    "('durchschnittsalter', 13, 'ZeroDivisionError')]\n38.5\nNone"
)
als_tupel = "(" + erwartete_ausgabe[1:].replace(")]", "))", 1)  # der Text verlangt keine Liste
assert AUSGABE in (erwartete_ausgabe, als_tupel), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
