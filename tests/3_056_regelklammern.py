# Automatisch erzeugt aus lehrkraft/muster/3_056_regelklammern.py - nicht von Hand ändern.
# vorlage-hash: 33f8f10cb9548040
# text-hash: a63d174234d3084b
# thema: datenstrukturen
# inhalt: Stack, Klammern prüfen

REGEL = '(betrag > 500 und [neue_adresse oder {land != "DE" und express}])'


def wert_von(funktion, regel):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(regel)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def reste(regel):
    """Langsame Vergleichslösung: streicht so lange benachbarte passende Klammerpaare, bis keins mehr da ist."""
    klammern = [(zeichen, stelle) for stelle, zeichen in enumerate(regel) if zeichen in "()[]{}"]
    gestrichen = True
    while gestrichen:
        gestrichen = False
        for stelle in range(len(klammern) - 1):
            if klammern[stelle][0] + klammern[stelle + 1][0] in ["()", "[]", "{}"]:
                del klammern[stelle : stelle + 2]
                gestrichen = True
                break
    return klammern


def vergleich_fehler(regel):
    """Vergleichslösung für fehlerstelle: erste übrig gebliebene schließende, sonst letzte öffnende Klammer."""
    uebrig = reste(regel)
    for zeichen, stelle in uebrig:
        if zeichen in ")]}":
            return stelle
    if uebrig:
        return uebrig[-1][1]
    return -1


def meldung(funktion, regel, erwartet, hinweis=""):
    """Prüft funktion(regel) gegen erwartet; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(funktion, regel)
    gezeigt = regel if len(regel) <= 80 else regel[:40] + " … " + regel[-20:] + f" ({len(regel)} Zeichen)"
    text = f"{funktion.__name__}({gezeigt!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"
    return ergebnis == erwartet, text


def zufallsregel(zufall, laenge):
    """Erzeugt eine Regel aus Klammern und Buchstaben, die oft richtig und oft knapp falsch ist."""
    zeichen = []
    offen = []
    for _ in range(laenge):
        wurf = zufall.random()
        if wurf < 0.35:
            klammer = zufall.choice("([{")
            zeichen.append(klammer)
            offen.append(klammer)
        elif wurf < 0.7 and offen:
            zeichen.append({"(": ")", "[": "]", "{": "}"}[offen.pop()])
        else:
            zeichen.append(zufall.choice("ab )]}"))
    if zufall.random() < 0.5:
        while offen:
            zeichen.append({"(": ")", "[": "]", "{": "}"}[offen.pop()])
    return "".join(zeichen)


# ausgewogen: das Beispiel ist richtig
stimmt, text = meldung(ausgewogen, REGEL, True)
assert stimmt, text

# ausgewogen: ein Text ohne Klammern ist richtig
stimmt, text = meldung(ausgewogen, "betrag > 500", True, "\nTipp: Andere Zeichen als Klammern überspringen Sie.")
assert stimmt, text

# ausgewogen: die falsche Art schließt (nicht immer True zurückgeben!)
stimmt, text = meldung(ausgewogen, "(a]", False, "\nTipp: Bei ']' muss oben auf dem Stapel '[' liegen.")
assert stimmt, text

# ausgewogen: eine schließende Klammer zu viel
stimmt, text = meldung(
    ausgewogen, "(a))", False, "\nTipp: Ist der Stapel leer, passt eine schließende Klammer zu nichts."
)
assert stimmt, text

# ausgewogen: eine schließende Klammer ganz vorn
stimmt, text = meldung(ausgewogen, ")(", False, "\nTipp: Prüfen Sie vor stapel[-1] oder pop(), ob der Stapel leer ist.")
assert stimmt, text

# ausgewogen: am Ende noch eine Klammer offen
stimmt, text = meldung(ausgewogen, "((a)", False, "\nTipp: Am Ende muss der Stapel leer sein.")
assert stimmt, text

# ausgewogen: überkreuzte Klammern sind falsch, obwohl die Anzahl stimmt
stimmt, text = meldung(
    ausgewogen, "([)]", False, "\nTipp: Zählen reicht nicht; die schließende Klammer muss zur zuletzt geöffneten passen."
)
assert stimmt, text

# ausgewogen: der leere Text ist richtig
stimmt, text = meldung(ausgewogen, "", True)
assert stimmt, text

# fehlerstelle: richtige Regeln ergeben -1
for regel in [REGEL, "{x}", ""]:
    stimmt, text = meldung(fehlerstelle, regel, -1)
    assert stimmt, text

# fehlerstelle: falsche Art
stimmt, text = meldung(fehlerstelle, "(a [b) c]", 5, "\nTipp: Geben Sie die Position der schließenden Klammer zurück.")
assert stimmt, text

# fehlerstelle: keine Klammer offen
stimmt, text = meldung(fehlerstelle, "a) (b", 1)
assert stimmt, text

# fehlerstelle: am Ende offen, die zuletzt geöffnete zählt
stimmt, text = meldung(
    fehlerstelle, "(a [b] {c", 7,
    "\nTipp: Legen Sie Positionen auf den Stapel; am Ende liegt die zuletzt geöffnete oben.",
)
assert stimmt, text

# fehlerstelle: mehrere offene, die oberste zählt
stimmt, text = meldung(fehlerstelle, "{[(", 2)
assert stimmt, text

# fehlerstelle: ein Fehler mitten im Text geht offenen Klammern am Ende vor
stimmt, text = meldung(
    fehlerstelle, "((a]", 3, "\nTipp: Brechen Sie beim ersten Fehler sofort ab und geben seine Position zurück."
)
assert stimmt, text

# Die Ausgabe des Programms
assert vergleichbar(AUSGABE) == vergleichbar("True\n5"), f"Erwartete Ausgabe:\nTrue\n5\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Regeln
zufall = Zufall(3056)
regeln = [zufallsregel(zufall, zufall.randint(0, 14)) for _ in range(1500)]

# Viele zufällige Regeln: ausgewogen
for regel in regeln:
    stimmt, text = meldung(ausgewogen, regel, vergleich_fehler(regel) == -1)
    assert stimmt, text

# Viele zufällige Regeln: fehlerstelle
for regel in regeln:
    stimmt, text = meldung(fehlerstelle, regel, vergleich_fehler(regel))
    assert stimmt, text

# Obere Grenze: 50 000 Klammern tief verschachtelt
regel = "([{" * 16666 + "x" + "}])" * 16666
stimmt, text = meldung(ausgewogen, regel, True)
assert stimmt, text

# Obere Grenze: fehlerstelle bei 50 000 tief verschachtelten Klammern
stimmt, text = meldung(fehlerstelle, regel[:-1] + "]", len(regel) - 1)
assert stimmt, text

# Obere Grenze: 100 000 Zeichen, die letzte Klammer bleibt offen
regel = "(a)" * 33333 + "["
stimmt, text = meldung(fehlerstelle, regel, len(regel) - 1)
assert stimmt, text
