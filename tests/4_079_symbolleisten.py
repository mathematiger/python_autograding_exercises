# Automatisch erzeugt aus lehrkraft/muster/4_079_symbolleisten.py - nicht von Hand ändern.
# vorlage-hash: 2086f5bd2c7c20eb
# text-hash: 262947faaa83c700
# thema: datenstrukturen
# inhalt: copy: flach gegen tief

def neuer_standard():
    """Baut jedes Mal eine frische Standardansicht wie im Aufgabentext, mit einem weiteren Schlüssel."""
    return {
        "name": "Standard",
        "sprache": "de",
        "symbolleisten": [
            {"titel": "Datei", "knoepfe": ["Neu", "Speichern"], "sichtbar": True},
            {"titel": "Bearbeiten", "knoepfe": ["Kopieren", "Einfügen"], "sichtbar": True},
        ],
        "symbole": {"Neu": "neu.png", "Speichern": "disk.png", "Kopieren": "kopie.png", "Einfügen": "einfuegen.png"},
    }


def rufe(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def ist_ansicht(ergebnis, fehler, aufruf):
    """Liefert eine Meldung, wenn ergebnis keine Ansicht (Dictionary mit symbolleisten und symbole) ist, sonst None."""
    if fehler is not None:
        return f"{aufruf} ist mit {fehler} abgestürzt."
    if not isinstance(ergebnis, dict):
        hinweis = " (fehlt das return?)" if ergebnis is None else ""
        return f"{aufruf} ergibt {ergebnis!r}, erwartet war eine Ansicht als Dictionary{hinweis}."
    for schluessel in ["name", "symbolleisten", "symbole"]:
        if schluessel not in ergebnis:
            return f"{aufruf} ergibt ein Dictionary ohne den Schlüssel {schluessel!r}: {ergebnis!r}"
    return None


def eigene_von(standard):
    """Ruft eigene_ansicht(standard) auf; liefert (Ansicht, Meldung oder None)."""
    ergebnis, fehler = rufe(eigene_ansicht, standard)
    return ergebnis, ist_ansicht(ergebnis, fehler, "eigene_ansicht(standard)")


TIPP_TIEF = (
    "\nTipp: Eine flache Kopie (copy.copy, dict(...), liste[:]) legt nur den äußersten Behälter neu an. "
    'Die Symbolleisten müssen bis in die Listen knoepfe neu sein: copy.deepcopy(standard["symbolleisten"]).'
)


# eigene_ansicht: das Ergebnis hat denselben Inhalt wie standard
standard = neuer_standard()
meine, meldung = eigene_von(standard)
assert meldung is None and meine == neuer_standard(), meldung or (
    f"eigene_ansicht(standard) ergibt {meine!r},\nerwartet war derselbe Inhalt wie standard: {neuer_standard()!r}"
)

# eigene_ansicht: das Ergebnis ist ein neues Dictionary, nicht standard selbst
standard = neuer_standard()
meine, meldung = eigene_von(standard)
assert meldung is None and meine is not standard, meldung or (
    "eigene_ansicht(standard) gibt standard selbst zurück. Dann ändert jede Anpassung die Standardansicht.\n"
    "Tipp: Eine Zuweisung oder return standard kopiert nichts (Aufgabe 2_018)."
)

# eigene_ansicht: ein anderer Name in der eigenen Ansicht ändert standard nicht
standard = neuer_standard()
meine, meldung = eigene_von(standard)
if meldung is None:
    meine["name"] = "Buchhaltung"
assert meldung is None and standard["name"] == "Standard", meldung or (
    f'Nach meine["name"] = "Buchhaltung" heißt die Standardansicht {standard["name"]!r}, erwartet war "Standard".'
)

# eigene_ansicht: eine angehängte Symbolleiste erscheint nicht im Standard
standard = neuer_standard()
meine, meldung = eigene_von(standard)
if meldung is None:
    meine["symbolleisten"].append({"titel": "Hilfe", "knoepfe": [], "sichtbar": True})
assert meldung is None and len(standard["symbolleisten"]) == 2, meldung or (
    f'Nach meine["symbolleisten"].append(...) hat die Standardansicht {len(standard["symbolleisten"])} '
    "Symbolleisten, erwartet waren weiterhin 2.\n"
    'Tipp: Auch die Liste "symbolleisten" muss in der eigenen Ansicht neu sein, nicht nur das äußere Dictionary.'
)

# eigene_ansicht: eine ausgeblendete Leiste bleibt im Standard sichtbar
standard = neuer_standard()
meine, meldung = eigene_von(standard)
if meldung is None:
    meine["symbolleisten"][1]["sichtbar"] = False
assert meldung is None and standard["symbolleisten"][1]["sichtbar"] is True, meldung or (
    'Nach meine["symbolleisten"][1]["sichtbar"] = False ist die Leiste auch in der Standardansicht ausgeblendet.\n'
    "Tipp: Jede Leiste (jedes Dictionary in der Liste) muss in der eigenen Ansicht neu sein. "
    "Eine flache Kopie der Liste enthält noch dieselben Dictionaries."
)

# eigene_ansicht: ein neuer Knopf in einer Leiste ändert den Standard nicht (das Beispiel)
standard = neuer_standard()
meine, meldung = eigene_von(standard)
if meldung is None:
    meine["symbolleisten"][0]["knoepfe"].append("Drucken")
assert meldung is None and standard["symbolleisten"][0]["knoepfe"] == ["Neu", "Speichern"], meldung or (
    f'Nach meine["symbolleisten"][0]["knoepfe"].append("Drucken") ist standard["symbolleisten"][0]["knoepfe"] '
    f'{standard["symbolleisten"][0]["knoepfe"]!r}, erwartet war ["Neu", "Speichern"].' + TIPP_TIEF
)

# eigene_ansicht: zwei eigene Ansichten sind voneinander unabhängig
standard = neuer_standard()
anna, meldung = eigene_von(standard)
ben, zweite_meldung = eigene_von(standard)
meldung = meldung or zweite_meldung
if meldung is None:
    anna["symbolleisten"][1]["knoepfe"].remove("Kopieren")
assert meldung is None and ben["symbolleisten"][1]["knoepfe"] == ["Kopieren", "Einfügen"], meldung or (
    "Zwei Ansichten aus eigene_ansicht(standard): Entfernt Anna den Knopf „Kopieren“, fehlt er auch bei Ben: "
    f'{ben["symbolleisten"][1]["knoepfe"]!r}.' + TIPP_TIEF
)

# eigene_ansicht: der Symbolsatz ist dasselbe Objekt wie im Standard
standard = neuer_standard()
meine, meldung = eigene_von(standard)
assert meldung is None and meine["symbole"] is standard["symbole"], meldung or (
    'meine["symbole"] is standard["symbole"] ergibt False, erwartet war True: Alle Ansichten sollen denselben '
    "Symbolsatz benutzen.\n"
    "Tipp: copy.deepcopy(standard) kopiert auch den Symbolsatz. Kopieren Sie nur die Symbolleisten tief und "
    "übernehmen Sie den Symbolsatz, wie er ist."
)

# eigene_ansicht: ein ausgetauschtes Bild im Symbolsatz sehen alle
standard = neuer_standard()
meine, meldung = eigene_von(standard)
if meldung is None:
    standard["symbole"]["Neu"] = "neu_2.png"
assert meldung is None and meine["symbole"].get("Neu") == "neu_2.png", meldung or (
    'Nach standard["symbole"]["Neu"] = "neu_2.png" zeigt die eigene Ansicht noch '
    f'{meine["symbole"].get("Neu")!r}, erwartet war "neu_2.png" (geteilter Symbolsatz).'
)

# eigene_ansicht: weitere Schlüssel wie "sprache" werden übernommen
standard = neuer_standard()
standard["schriftgroesse"] = 14
meine, meldung = eigene_von(standard)
assert meldung is None and meine.get("sprache") == "de" and meine.get("schriftgroesse") == 14, meldung or (
    f"eigene_ansicht übernimmt nicht alle Schlüssel: Ergebnis {meine!r}.\n"
    "Tipp: Beginnen Sie mit einer flachen Kopie des ganzen Dictionarys statt die Schlüssel einzeln abzuschreiben."
)

# eigene_ansicht: standard selbst bleibt unverändert
standard = neuer_standard()
symbole = standard["symbole"]
leisten = standard["symbolleisten"]
eigene_von(standard)
assert standard == neuer_standard() and standard["symbole"] is symbole and standard["symbolleisten"] is leisten, (
    f"eigene_ansicht hat standard verändert, jetzt: {standard!r}\n"
    "Tipp: Ersetzen Sie die Symbolleisten in der Kopie, nicht im Original."
)

# eigene_ansicht: eine Ansicht ohne Symbolleisten
standard = {"name": "Leer", "symbolleisten": [], "symbole": {}}
meine, meldung = eigene_von(standard)
if meldung is None:
    meine["symbolleisten"].append({"titel": "Datei", "knoepfe": ["Neu"], "sichtbar": True})
assert meldung is None and standard["symbolleisten"] == [], meldung or (
    "Bei einer Ansicht ohne Symbolleisten soll die Liste in der eigenen Ansicht trotzdem neu sein. "
    f"Standard danach: {standard!r}"
)

# mit_symbolsatz: das Ergebnis hat den neuen Symbolsatz (dasselbe Objekt)
ansicht = neuer_standard()
kontrast = {"Neu": "neu_kontrast.png", "Speichern": "disk_kontrast.png"}
ergebnis, fehler = rufe(mit_symbolsatz, ansicht, kontrast)
meldung = ist_ansicht(ergebnis, fehler, "mit_symbolsatz(ansicht, kontrast)")
assert meldung is None and ergebnis["symbole"] is kontrast, meldung or (
    f'mit_symbolsatz(ansicht, kontrast)["symbole"] ist {ergebnis["symbole"]!r}, erwartet war das Dictionary kontrast '
    "selbst (dasselbe Objekt)."
)

# mit_symbolsatz: ansicht behält ihren Symbolsatz
ansicht = neuer_standard()
alt = ansicht["symbole"]
ergebnis, fehler = rufe(mit_symbolsatz, ansicht, {"Neu": "neu_kontrast.png"})
meldung = ist_ansicht(ergebnis, fehler, "mit_symbolsatz(ansicht, {...})")
assert meldung is None and ansicht["symbole"] is alt and ergebnis is not ansicht, meldung or (
    "Nach mit_symbolsatz(ansicht, ...) hat ansicht selbst einen anderen Symbolsatz oder das Ergebnis ist ansicht "
    "selbst. Die Vorschau soll eine neue Ansicht sein, ansicht bleibt unverändert.\n"
    'Tipp: Machen Sie zuerst eine flache Kopie und ersetzen Sie darin "symbole".'
)

# mit_symbolsatz: der alte Symbolsatz bleibt unverändert
ansicht = neuer_standard()
rufe(mit_symbolsatz, ansicht, {"Neu": "neu_kontrast.png"})
assert ansicht == neuer_standard(), (
    f"mit_symbolsatz hat ansicht verändert, jetzt: {ansicht!r}\n"
    'Tipp: Ersetzen Sie in der Kopie den Wert unter "symbole", statt den alten Symbolsatz mit update zu ändern.'
)

# mit_symbolsatz: die Vorschau teilt die Symbolleisten mit der Ansicht
ansicht = neuer_standard()
ergebnis, fehler = rufe(mit_symbolsatz, ansicht, {})
meldung = ist_ansicht(ergebnis, fehler, "mit_symbolsatz(ansicht, {})")
assert meldung is None and ergebnis["symbolleisten"] is ansicht["symbolleisten"], meldung or (
    'vorschau["symbolleisten"] is ansicht["symbolleisten"] ergibt False, erwartet war True.\n'
    "Tipp: Die Vorschau wird nie bearbeitet, eine tiefe Kopie wäre hier nur Aufwand. "
    "Eine flache Kopie (copy.copy) teilt alles außer dem äußeren Dictionary."
)

# mit_symbolsatz: weitere Schlüssel werden übernommen
ansicht = neuer_standard()
ergebnis, fehler = rufe(mit_symbolsatz, ansicht, {})
meldung = ist_ansicht(ergebnis, fehler, "mit_symbolsatz(ansicht, {})")
assert meldung is None and ergebnis.get("sprache") == "de" and ergebnis.get("name") == "Standard", meldung or (
    f"mit_symbolsatz übernimmt nicht alle Schlüssel der Ansicht: Ergebnis {ergebnis!r}."
)

# Beides zusammen: Vorschau einer eigenen Ansicht (das Beispiel)
standard = neuer_standard()
meine, meldung = eigene_von(standard)
vorschau = None
if meldung is None:
    vorschau, fehler = rufe(mit_symbolsatz, meine, {"Neu": "neu_kontrast.png"})
    meldung = ist_ansicht(vorschau, fehler, "mit_symbolsatz(meine, {...})")
assert (
    meldung is None
    and vorschau["symbolleisten"] is meine["symbolleisten"]
    and meine["symbole"] is standard["symbole"]
), meldung or "Im Beispiel erwartet: vorschau teilt die Symbolleisten mit meine, meine behält den Symbolsatz des Standards."

# 200 zufällige Ansichten, die eigene Kopie wird zufällig verändert
zufall = Zufall(4079)
namen = ["Neu", "Öffnen", "Speichern", "Drucken", "Kopieren", "Einfügen", "Suchen", "Hilfe"]
for runde in range(200):
    standard = {"name": f"Ansicht {runde}", "symbolleisten": [], "symbole": {n: n.lower() + ".png" for n in namen}}
    if zufall.random() < 0.5:
        standard["zoom"] = zufall.randint(50, 200)
    for nummer in range(zufall.randint(0, 5)):
        knoepfe = [zufall.choice(namen) for _ in range(zufall.randint(0, 4))]
        standard["symbolleisten"].append({"titel": f"Leiste {nummer}", "knoepfe": knoepfe, "sichtbar": True})
    vorher = copy.deepcopy(standard)
    meine, meldung = eigene_von(standard)
    assert meldung is None, meldung
    assert meine == vorher and meine["symbole"] is standard["symbole"], (
        f"eigene_ansicht({vorher!r}) ergibt {meine!r}; erwartet waren derselbe Inhalt und derselbe Symbolsatz."
    )
    schritte = []
    for _ in range(zufall.randint(1, 6)):
        leisten = meine["symbolleisten"]
        art = zufall.randint(0, 3)
        if art == 0 or not leisten:
            leisten.append({"titel": "Neu", "knoepfe": [], "sichtbar": True})
            schritte.append("Leiste angehängt")
        elif art == 1:
            leiste = zufall.choice(leisten)
            leiste["knoepfe"].insert(0, zufall.choice(namen))
            schritte.append(f"Knopf in {leiste['titel']} eingefügt")
        elif art == 2:
            leiste = zufall.choice(leisten)
            leiste["sichtbar"] = False
            schritte.append(f"{leiste['titel']} ausgeblendet")
        else:
            leiste = zufall.choice(leisten)
            leiste["titel"] = leiste["titel"] + " (eigen)"
            schritte.append("Titel geändert")
    assert standard == vorher, (
        f"Nach diesen Änderungen an der eigenen Ansicht hat sich die Standardansicht verändert: {schritte}.\n"
        f"Vorher: {vorher!r}\nNachher: {standard!r}" + TIPP_TIEF
    )

# Obere Grenze: 200 Symbolleisten mit je 100 Knöpfen und 10 000 Symbole
symbole = {f"Knopf {nummer}": f"bild_{nummer}.png" for nummer in range(10000)}
leisten = []
for nummer in range(200):
    leisten.append({"titel": f"Leiste {nummer}", "knoepfe": [f"Knopf {k}" for k in range(100)], "sichtbar": True})
standard = {"name": "Groß", "symbolleisten": leisten, "symbole": symbole}
meine, meldung = eigene_von(standard)
if meldung is None:
    meine["symbolleisten"][199]["knoepfe"].append("Knopf 0")
assert (
    meldung is None
    and len(leisten[199]["knoepfe"]) == 100
    and len(meine["symbolleisten"]) == 200
), meldung or "Bei 200 Symbolleisten mit je 100 Knöpfen sind die Leisten der eigenen Ansicht nicht unabhängig vom Standard."
