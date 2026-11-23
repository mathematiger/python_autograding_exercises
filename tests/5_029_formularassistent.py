# Automatisch erzeugt aus lehrkraft/muster/5_029_formularassistent.py - nicht von Hand ändern.
# vorlage-hash: b799869cbe8fb82f
# text-hash: db82cd18c3f3048e
# thema: kontrollfluss
# inhalt: yield from, Rückgabewert

import types

BEISPIEL = [" Ada ", "zwölf", "36", "ada@example.org"]
BEISPIEL_TEXTE = ["Name:", "Alter:", "Ungültige Eingabe. Alter:", "E-Mail:"]
BEISPIEL_ERGEBNIS = {"name": "Ada", "alter": 36, "email": "ada@example.org"}


def schicke(generator, antwort):
    """Sendet antwort; gibt ("weiter", text) oder ("ende", rueckgabewert) oder ("fehler", text) zurück."""
    try:
        return ("weiter", generator.send(antwort))
    except StopIteration as ende:
        return ("ende", ende.value)
    except Exception as fehler:
        return ("fehler", f"{type(fehler).__name__}: {fehler}")


def ergebnis_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def von_hand(antworten):
    """Spielt anmeldeformular() mit den Antworten von Hand durch; gibt die Liste der Schritte zurück."""
    formular = anmeldeformular()
    schritte = [("weiter", next(formular))]
    for antwort in antworten:
        schritte.append(schicke(formular, antwort))
        if schritte[-1][0] != "weiter":
            break
    return schritte


def vergleich(antworten):
    """Vergleichslösung ohne Generatoren: dieselben Regeln als einfache Schleife."""
    fragen = [("Name:", ist_name), ("Alter:", ist_alter), ("E-Mail:", ist_email)]
    texte = []
    werte = []
    stelle = 0
    for text, pruefung in fragen:
        texte.append(text)
        while True:
            if stelle == len(antworten):
                return texte, None
            antwort = antworten[stelle]
            stelle += 1
            if pruefung(antwort):
                werte.append(antwort)
                break
            texte.append("Ungültige Eingabe. " + text)
    return texte, {"name": werte[0].strip(), "alter": int(werte[1]), "email": werte[2]}


def fragen_beim_ausfuellen(antworten):
    """Spielt anmeldeformular() von Hand durch und merkt sich, mit welchen Texten es frage aufruft."""
    original = globals()["frage"]
    aufrufe = []

    def mitschreiben(text, ist_gueltig):
        """Merkt sich den Text und reicht an die echte frage weiter."""
        aufrufe.append(text)
        return original(text, ist_gueltig)

    globals()["frage"] = mitschreiben
    try:
        schritte = von_hand(antworten)
    finally:
        globals()["frage"] = original
    return aufrufe, schritte


def zaehle_fragen():
    """Ein anderes Formular für ausfuellen: fragt dreimal und gibt die Antworten in umgekehrter Reihenfolge zurück."""
    a = yield "eins"
    b = yield "zwei"
    c = yield "drei"
    return [c, b, a]


# frage liefert zuerst den Text
f = frage("Name:", ist_name)
erster = ergebnis_von(next, f)
assert erster == "Name:", (
    f'next(frage("Name:", ist_name)) ergibt {erster!r}, erwartet war "Name:".'
    + ("\nTipp: frage soll eine Generatorfunktion sein: antwort = yield text." if not isinstance(f, types.GeneratorType) else "")
)

# frage mit einem anderen Text (nicht fest hinschreiben!)
f = frage("Postleitzahl:", str.isdigit)
erster = ergebnis_von(next, f)
assert erster == "Postleitzahl:", f'next(frage("Postleitzahl:", str.isdigit)) ergibt {erster!r}, erwartet war "Postleitzahl:".'

# frage gibt eine gültige Antwort mit return zurück
f = frage("Name:", ist_name)
next(f)
schritt = schicke(f, "Ada")
assert schritt == ("ende", "Ada"), (
    f'Nach next() und send("Ada") ergibt frage("Name:", ist_name) {schritt!r}, erwartet war das Ende mit dem '
    'Rückgabewert "Ada" (StopIteration mit value "Ada").\nTipp: Geben Sie die gültige Antwort mit return zurück.'
)

# frage wiederholt die Frage mit Hinweis bei einer ungültigen Antwort
f = frage("Name:", ist_name)
next(f)
schritt = schicke(f, "  ")
assert schritt == ("weiter", "Ungültige Eingabe. Name:"), (
    f'Nach send("  ") ergibt frage("Name:", ist_name) {schritt!r}, erwartet war der Text "Ungültige Eingabe. Name:".'
)

# frage wiederholt so oft wie nötig und gibt dann die gültige Antwort zurück
f = frage("Alter:", ist_alter)
schritte = [ergebnis_von(next, f)] + [schicke(f, antwort) for antwort in ["abc", "7", "121", "42"]]
erwartet = ["Alter:"] + [("weiter", "Ungültige Eingabe. Alter:")] * 3 + [("ende", "42")]
assert schritte == erwartet, f'frage("Alter:", ist_alter) mit "abc", "7", "121", "42" ergibt {schritte!r}, erwartet war {erwartet!r}.'

# anmeldeformular von Hand: alle Antworten gültig
schritte = von_hand(["Grace", "85", "grace@example.org"])
erwartet = [("weiter", "Name:"), ("weiter", "Alter:"), ("weiter", "E-Mail:"), ("ende", {"name": "Grace", "alter": 85, "email": "grace@example.org"})]
assert schritte == erwartet, (
    f"anmeldeformular() mit drei gültigen Antworten ergibt die Schritte {schritte!r}, erwartet war {erwartet!r}.\n"
    "Tipp: name = yield from frage(\"Name:\", ist_name) gibt den Rückgabewert von frage."
)

# anmeldeformular: Name ohne Rand-Leerzeichen
schritte = von_hand(["  Linus  ", "16", "l@x"])
ende = schritte[-1] if schritte and isinstance(schritte[-1], tuple) and len(schritte[-1]) == 2 else (None, None)
assert isinstance(ende[1], dict) and ende[1].get("name") == "Linus", (
    f"anmeldeformular() mit \"  Linus  \" als Name endet mit {schritte[-1] if schritte else schritte!r}, erwartet war der Name 'Linus'.\n"
    "Tipp: Geben Sie den Namen mit strip() zurück."
)

# anmeldeformular: Name, Alter als int und E-Mail-Adresse unverändert
assert schritte[-1] == ("ende", {"name": "Linus", "alter": 16, "email": "l@x"}), (
    f"anmeldeformular() mit \"  Linus  \", \"16\", \"l@x\" endet mit {schritte[-1]!r}, erwartet war "
    "('ende', {'name': 'Linus', 'alter': 16, 'email': 'l@x'})."
)

# anmeldeformular wiederholt ungültige Fragen mit Hinweis
schritte = von_hand(["", "Ada", "36", "keine-adresse", "ada@example.org"])
texte = [text for art, text in schritte if art == "weiter"]
assert texte == ["Name:", "Ungültige Eingabe. Name:", "Alter:", "E-Mail:", "Ungültige Eingabe. E-Mail:"], (
    f"anmeldeformular() mit einem leeren Namen und einer Adresse ohne @ zeigt {texte!r}, erwartet war "
    "['Name:', 'Ungültige Eingabe. Name:', 'Alter:', 'E-Mail:', 'Ungültige Eingabe. E-Mail:']."
)

# anmeldeformular gibt die Arbeit an frage ab
aufrufe, schritte = fragen_beim_ausfuellen(["Ada", "36", "ada@example.org"])
assert aufrufe == ["Name:", "Alter:", "E-Mail:"] and schritte[-1][0] == "ende", (
    f"anmeldeformular() ruft frage mit {aufrufe!r} auf und endet mit {schritte[-1]!r}; erwartet waren die Aufrufe "
    "['Name:', 'Alter:', 'E-Mail:'] und ein Ende mit dem Dictionary.\n"
    "Tipp: Schreiben Sie die Fragen nicht noch einmal, sondern benutzen Sie yield from frage(…)."
)

# ausfuellen im Beispiel
ergebnis = ergebnis_von(ausfuellen, anmeldeformular(), BEISPIEL)
assert ergebnis == (BEISPIEL_TEXTE, BEISPIEL_ERGEBNIS), (
    f"ausfuellen(anmeldeformular(), {BEISPIEL!r}) ergibt {ergebnis!r}, erwartet war {(BEISPIEL_TEXTE, BEISPIEL_ERGEBNIS)!r}.\n"
    "Tipp: Den Rückgabewert des Formulars finden Sie in except StopIteration as ende: ende.value."
)

# ausfuellen, wenn die Antworten nicht reichen
ergebnis = ergebnis_von(ausfuellen, anmeldeformular(), ["Ada"])
assert ergebnis == (["Name:", "Alter:"], None), f'ausfuellen(anmeldeformular(), ["Ada"]) ergibt {ergebnis!r}, erwartet war ([\'Name:\', \'Alter:\'], None).'

# ausfuellen ohne Antworten
ergebnis = ergebnis_von(ausfuellen, anmeldeformular(), [])
assert ergebnis == (["Name:"], None), f"ausfuellen(anmeldeformular(), []) ergibt {ergebnis!r}, erwartet war (['Name:'], None)."

# ausfuellen benutzt übrige Antworten nicht
ergebnis = ergebnis_von(ausfuellen, anmeldeformular(), ["Ada", "36", "ada@example.org", "noch was", "und mehr"])
assert ergebnis == (["Name:", "Alter:", "E-Mail:"], {"name": "Ada", "alter": 36, "email": "ada@example.org"}), (
    f"ausfuellen mit zwei überzähligen Antworten ergibt {ergebnis!r}, erwartet war das fertige Formular nach drei Antworten."
)

# ausfuellen funktioniert mit jedem Formular-Generator
ergebnis = ergebnis_von(ausfuellen, zaehle_fragen(), ["a", "b", "c"])
assert ergebnis == (["eins", "zwei", "drei"], ["c", "b", "a"]), (
    f'ausfuellen(zaehle_fragen(), ["a", "b", "c"]) ergibt {ergebnis!r}, erwartet war ([\'eins\', \'zwei\', \'drei\'], [\'c\', \'b\', \'a\']).\n'
    "Tipp: ausfuellen darf nichts über die Fragen des Anmeldeformulars wissen."
)

# Die Ausgabe des Programms
erwartet = f"{(BEISPIEL_TEXTE, BEISPIEL_ERGEBNIS)}\n{(['Name:', 'Alter:'], None)}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Antwortfolgen
zufall = Zufall(5029)
moeglich = ["", "  ", "Ada", " Bo ", "15", "16", "120", "121", "036", "x@y", "@y", "a@b@c", "ada@example.org", "٣٦"]
for _ in range(300):
    antworten = [zufall.choice(moeglich) for _ in range(zufall.randint(0, 9))]
    erwartet = vergleich(antworten)
    ergebnis = ergebnis_von(ausfuellen, anmeldeformular(), antworten)
    assert ergebnis == erwartet, f"ausfuellen(anmeldeformular(), {antworten!r})\n  ergibt   {ergebnis!r}\n  erwartet {erwartet!r}"

# Obere Grenze: 100 000 Antworten, fast alle ungültig
antworten = ["Ada"] + ["?"] * 99998 + ["99"]
ergebnis = ergebnis_von(ausfuellen, anmeldeformular(), antworten)
erwartet = vergleich(antworten)
assert ergebnis == erwartet, (
    f"Bei 99 998 ungültigen Altersangaben ergibt ausfuellen {len(ergebnis[0]) if isinstance(ergebnis, tuple) else ergebnis} "
    f"Texte, erwartet waren {len(erwartet[0])}."
)
