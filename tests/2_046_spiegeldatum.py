# Automatisch erzeugt aus lehrkraft/muster/2_046_spiegeldatum.py - nicht von Hand ändern.
# vorlage-hash: 1354b3ebeb817ff9
# text-hash: cf9dd877c4f570a6
# thema: algorithmen
# inhalt: Rekursion: Palindrom

def innere_aufrufe(text):
    """Gibt zurück, mit welchen Texten ist_palindrom(text) sich selbst aufruft."""
    global ist_palindrom
    original = ist_palindrom
    innere = []

    def mitzaehlen(teil):
        """Merkt sich den inneren Aufruf und reicht ihn an die echte Funktion weiter."""
        innere.append(teil)
        return original(teil)

    ist_palindrom = mitzaehlen
    try:
        original(text)
    finally:
        ist_palindrom = original
    return innere


def ergebnis_von(text):
    """Ruft ist_palindrom(text) auf; ein RecursionError oder IndexError wird als Text zurückgegeben."""
    try:
        return ist_palindrom(text)
    except RecursionError:
        return "RecursionError"
    except IndexError:
        return "IndexError (fehlt die Abbruchbedingung für den leeren Text?)"


# Das Spiegeldatum aus der Aufgabe
ergebnis = ergebnis_von("12022021")
assert ergebnis == True, f'ist_palindrom("12022021") ergibt {ergebnis!r}, erwartet war True.'

# Ein Datum, das kein Spiegeldatum ist (nicht fest True zurückgeben!)
ergebnis = ergebnis_von("20250101")
assert ergebnis == False, f'ist_palindrom("20250101") ergibt {ergebnis!r}, erwartet war False.'

# Gerade und ungerade Länge
ergebnis = [ergebnis_von("1221"), ergebnis_von("12321")]
assert ergebnis == [True, True], (
    f'ist_palindrom("1221") und ist_palindrom("12321") ergeben {ergebnis!r}, erwartet war [True, True].\n'
    "Tipp: Bei gerader Länge bleibt am Ende der leere Text übrig, bei ungerader ein einzelnes Zeichen."
)

# Erstes und letztes Zeichen gleich, innen aber nicht
ergebnis = ergebnis_von("1231")
assert ergebnis == False, (
    f'ist_palindrom("1231") ergibt {ergebnis!r}, erwartet war False (innen steht "23").\n'
    "Tipp: Sind die äußeren Zeichen gleich, entscheidet der Aufruf für text[1:-1]."
)

# Der Unterschied steht ganz innen
ergebnis = ergebnis_von("abcxdcba")
assert ergebnis == False, f'ist_palindrom("abcxdcba") ergibt {ergebnis!r}, erwartet war False.'

# Der leere Text
ergebnis = ergebnis_von("")
assert ergebnis == True, f'ist_palindrom("") ergibt {ergebnis!r}, erwartet war True.'

# Ein einzelnes Zeichen
ergebnis = ergebnis_von("7")
assert ergebnis == True, f'ist_palindrom("7") ergibt {ergebnis!r}, erwartet war True.'

# Zwei Zeichen: gleich und verschieden
ergebnis = [ergebnis_von("33"), ergebnis_von("34")]
assert ergebnis == [True, False], f'ist_palindrom("33") und ist_palindrom("34") ergeben {ergebnis!r}, erwartet war [True, False].'

# Groß- und Kleinschreibung zählt
ergebnis = ergebnis_von("Aa")
assert ergebnis == False, f'ist_palindrom("Aa") ergibt {ergebnis!r}, erwartet war False ("A" und "a" sind verschieden).'

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("12.02.2021 True\n01.01.2025 False\n22.02.2022 True"), (
    f"Erwartete Ausgabe:\n12.02.2021 True\n01.01.2025 False\n22.02.2022 True\nIhr Programm:\n{AUSGABE}"
)

# Rekursiv: die Funktion ruft sich mit dem Text ohne erstes und letztes Zeichen auf
innere = innere_aufrufe("radar")
assert innere[:2] == ["ada", "d"], (
    f'ist_palindrom("radar") ruft sich mit {innere!r} auf, erwartet war ["ada", "d"].\n'
    "Tipp: Rufen Sie ist_palindrom(text[1:-1]) auf und geben Sie dessen Ergebnis zurück."
)

# Ohne Schleife und ohne reversed
assert not verwendet("for") and not verwendet("while") and not verwendet("reversed"), (
    "Lösen Sie die Aufgabe rekursiv, ohne for, while oder reversed."
)

# Beim ersten Unterschied hört die Rekursion auf
innere = innere_aufrufe("1" + "5" * 50 + "2")
assert innere == [], (
    f'ist_palindrom("1" + "5" * 50 + "2") ruft sich noch {len(innere)}-mal selbst auf, obwohl schon das erste und '
    "das letzte Zeichen verschieden sind.\nTipp: Geben Sie in diesem Fall sofort False zurück."
)

# Viele zufällige Texte, auch Palindrome mit einem einzigen falschen Zeichen
zufall = Zufall(2046)
for runde in range(400):
    halb = "".join(zufall.choice("01ab") for _ in range(zufall.randint(0, 12)))
    mitte = zufall.choice(["", "x", "0"])
    text = halb + mitte + halb[::-1]
    if runde % 2 == 1 and len(text) > 0:
        stelle = zufall.randrange(len(text))
        text = text[:stelle] + zufall.choice("01abx") + text[stelle + 1 :]
    erwartet = text == text[::-1]
    ergebnis = ergebnis_von(text)
    assert ergebnis == erwartet, f"ist_palindrom({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: ein Palindrom mit 800 Zeichen
halb = "".join(zufall.choice("0123456789") for _ in range(400))
ergebnis = ergebnis_von(halb + halb[::-1])
assert ergebnis == True, f"Ein Palindrom mit 800 Zeichen ergibt {ergebnis!r}, erwartet war True."

# Obere Grenze: 800 Zeichen mit einem Unterschied genau in der Mitte
anders = "8" if halb[-1] == "9" else "9"
ergebnis = ergebnis_von(halb + anders + halb[::-1][1:])
assert ergebnis == False, f"800 Zeichen mit einem Unterschied in der Mitte ergeben {ergebnis!r}, erwartet war False."
