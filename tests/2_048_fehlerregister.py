# Automatisch erzeugt aus lehrkraft/muster/2_048_fehlerregister.py - nicht von Hand ändern.
# vorlage-hash: fa35188dd469cbb7
# text-hash: 22f4f40e15daa3cd
# thema: algorithmen
# inhalt: Übung: Rekursion

def ergebnis_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except RecursionError:
        return "RecursionError (fehlt eine Abbruchbedingung?)"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_bits(register):
    """Vergleichslösung: zählt die Einsen im Text der Binärdarstellung."""
    return format(register, "b").count("1")


def vergleich_position(werte, grenze):
    """Vergleichslösung mit einer Schleife."""
    for position, wert in enumerate(werte):
        if wert > grenze:
            return position
    return -1


def ruft_sich_selbst(name, *argumente):
    """True, wenn die Funktion mit dem Namen name bei diesen Argumenten sich selbst aufruft."""
    original = globals()[name]
    aufrufe = []

    def mitzaehlen(*innere_argumente, **benannt):
        """Zählt den inneren Aufruf und reicht ihn weiter."""
        aufrufe.append(innere_argumente)
        return original(*innere_argumente, **benannt)

    globals()[name] = mitzaehlen
    try:
        original(*argumente)
    finally:
        globals()[name] = original
    return len(aufrufe) > 0


# aktive_fehler im Beispiel: 13 ist binär 1101
ergebnis = ergebnis_von(aktive_fehler, 13)
assert ergebnis == 3, (
    f"aktive_fehler(13) ergibt {ergebnis!r}, erwartet war 3 (13 ist binär 1101)."
    + ("\nTipp: Geben Sie das Ergebnis mit return zurück." if ergebnis is None else "")
)

# aktive_fehler mit anderen Registern (nicht fest hinschreiben!)
ergebnis = [ergebnis_von(aktive_fehler, 8), ergebnis_von(aktive_fehler, 7)]
assert ergebnis == [1, 3], (
    f"aktive_fehler(8) und aktive_fehler(7) ergeben {ergebnis!r}, erwartet war [1, 3] (binär 1000 und 111).\n"
    "Tipp: Die letzte Stelle ist register % 2, der Rest ist register // 2."
)

# aktive_fehler ohne Fehler
ergebnis = ergebnis_von(aktive_fehler, 0)
assert ergebnis == 0, f"aktive_fehler(0) ergibt {ergebnis!r}, erwartet war 0."

# aktive_fehler mit genau einem Fehler an der letzten Stelle
ergebnis = ergebnis_von(aktive_fehler, 1)
assert ergebnis == 1, f"aktive_fehler(1) ergibt {ergebnis!r}, erwartet war 1."

# aktive_fehler mit Nullen zwischen den Einsen
ergebnis = ergebnis_von(aktive_fehler, 0b1000100010001)
assert ergebnis == 4, f"aktive_fehler({0b1000100010001}) ergibt {ergebnis!r}, erwartet war 4 (binär 1000100010001)."

# erste_ueberschreitung im Beispiel
ergebnis = ergebnis_von(erste_ueberschreitung, [61, 64, 72, 70], 65)
assert ergebnis == 2, f"erste_ueberschreitung([61, 64, 72, 70], 65) ergibt {ergebnis!r}, erwartet war 2."

# erste_ueberschreitung: der erste Wert liegt schon darüber
ergebnis = ergebnis_von(erste_ueberschreitung, [90, 10, 95], 50)
assert ergebnis == 0, f"erste_ueberschreitung([90, 10, 95], 50) ergibt {ergebnis!r}, erwartet war 0."

# erste_ueberschreitung: der Wert liegt weiter hinten (nicht fest hinschreiben!)
ergebnis = ergebnis_von(erste_ueberschreitung, [3, 1, 4, 1, 5, 9, 2], 8)
assert ergebnis == 5, (
    f"erste_ueberschreitung([3, 1, 4, 1, 5, 9, 2], 8) ergibt {ergebnis!r}, erwartet war 5 (9 liegt über 8).\n"
    "Tipp: Die Position im Rest werte[1:] ist um eins kleiner als in der ganzen Liste."
)

# erste_ueberschreitung: kein Wert liegt darüber
ergebnis = ergebnis_von(erste_ueberschreitung, [61, 64], 65)
assert ergebnis == -1, (
    f"erste_ueberschreitung([61, 64], 65) ergibt {ergebnis!r}, erwartet war -1.\n"
    "Tipp: Liefert der Aufruf für den Rest -1, ist auch das Ergebnis -1, nicht -1 + 1."
)

# erste_ueberschreitung mit leerer Liste
ergebnis = ergebnis_von(erste_ueberschreitung, [], 65)
assert ergebnis == -1, f"erste_ueberschreitung([], 65) ergibt {ergebnis!r}, erwartet war -1."

# erste_ueberschreitung: ein Wert genau auf der Grenze liegt nicht darüber
ergebnis = ergebnis_von(erste_ueberschreitung, [65, 65, 66], 65)
assert ergebnis == 2, f"erste_ueberschreitung([65, 65, 66], 65) ergibt {ergebnis!r}, erwartet war 2 (65 liegt nicht über 65)."

# erste_ueberschreitung mit negativen Werten
ergebnis = ergebnis_von(erste_ueberschreitung, [-30, -12, -5], -10)
assert ergebnis == 2, f"erste_ueberschreitung([-30, -12, -5], -10) ergibt {ergebnis!r}, erwartet war 2."

# Die Ausgabe des Programms
erwartet = "Aktive Fehler: 3\nErste Überschreitung bei Index 2"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Beide Funktionen rufen sich selbst auf
selbst = [ruft_sich_selbst("aktive_fehler", 13), ruft_sich_selbst("erste_ueberschreitung", [61, 64, 72, 70], 65)]
assert selbst == [True, True], (
    f"Ruft sich selbst auf: aktive_fehler {selbst[0]}, erste_ueberschreitung {selbst[1]}; erwartet war beide Male True.\n"
    "Tipp: Die Funktion selbst soll sich aufrufen, nicht nur eine innere Hilfsfunktion."
)

# Ohne Schleife und ohne fertige Hilfen
verboten = [wort for wort in ["for", "while", "bin", "count", "index", "bit_count"] if verwendet(wort)]
assert verboten == [], f"Ihr Code verwendet {verboten}. Lösen Sie die Aufgabe rekursiv, ohne Schleifen und ohne diese Hilfen."

# Viele zufällige Register
zufall = Zufall(2048)
for _ in range(300):
    register = zufall.randrange(2 ** zufall.randint(0, 60))
    ergebnis = ergebnis_von(aktive_fehler, register)
    erwartet = vergleich_bits(register)
    assert ergebnis == erwartet, f"aktive_fehler({register}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige Messreihen
for _ in range(300):
    werte = [zufall.randint(-20, 20) for _ in range(zufall.randint(0, 10))]
    grenze = zufall.randint(-20, 20)
    ergebnis = ergebnis_von(erste_ueberschreitung, werte, grenze)
    erwartet = vergleich_position(werte, grenze)
    assert ergebnis == erwartet, f"erste_ueberschreitung({werte}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: das größte Register mit 60 Einsen
ergebnis = ergebnis_von(aktive_fehler, 2**60 - 1)
assert ergebnis == 60, f"aktive_fehler(2**60 - 1) ergibt {ergebnis!r}, erwartet war 60."

# Obere Grenze: 400 Werte, der einzige darüber ganz am Ende
werte = [zufall.randint(-1000, 999) for _ in range(399)] + [1000]
ergebnis = ergebnis_von(erste_ueberschreitung, werte, 999)
assert ergebnis == 399, f"Bei 400 Werten, nur der letzte über der Grenze, ergibt erste_ueberschreitung {ergebnis!r}, erwartet war 399."

# Obere Grenze: 400 Werte, keiner darüber
ergebnis = ergebnis_von(erste_ueberschreitung, [1000] * 400, 1000)
assert ergebnis == -1, f"Bei 400 Werten genau auf der Grenze 1000 ergibt erste_ueberschreitung {ergebnis!r}, erwartet war -1."
