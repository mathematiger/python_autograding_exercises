# Automatisch erzeugt aus lehrkraft/muster/1_048_druckerwartung.py - nicht von Hand ändern.
# vorlage-hash: 1fc4979858554b54
# text-hash: 273460d6636ef2ed
# thema: programmaufbau
# inhalt: Docstrings und Kommentare

import ast

EINGABEN = ["148500"]


def docstring_von(funktion):
    """Der Docstring der Funktion ohne Leerraum am Rand, oder None."""
    text = funktion.__doc__
    if text is None:
        return None
    return text.strip()


def kommentare_in(name):
    """Alle Kommentarzeilen im Rumpf der Funktion name aus dem Programm der SuS."""
    with open(__file__, encoding="utf-8") as datei:
        quelltext = datei.read()
    zeilen = quelltext.splitlines()
    for knoten in ast.walk(ast.parse(quelltext)):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == name:
            rumpf = zeilen[knoten.lineno : knoten.end_lineno]
            return [zeile.strip() for zeile in rumpf if zeile.strip().startswith("#") and len(zeile.strip("# \t")) > 0]
    return []


def zeilen_bei(zaehlerstand):
    """Startet das Programm mit dem Zählerstand; liefert die Zeilen der Ausgabe oder den Abbruch als Text."""
    try:
        return starte(str(zaehlerstand)).splitlines()
    except Exception as fehler:
        return [f"(Abbruch: {type(fehler).__name__}: {fehler})"]


def erwartete_entscheidung(zaehlerstand):
    """Vergleichslösung: die zweite Zeile der Ausgabe."""
    naechste = zaehlerstand - zaehlerstand % 50000 + 50000
    if naechste - zaehlerstand <= 2000:
        return "Wartung jetzt einplanen"
    return "Noch keine Wartung nötig"


def entscheidung_stimmt(zaehlerstand):
    """Liefert (stimmt, Meldung) für die zweite Zeile der Ausgabe."""
    zeilen = zeilen_bei(zaehlerstand)
    erwartet = erwartete_entscheidung(zaehlerstand)
    tatsaechlich = zeilen[1] if len(zeilen) > 1 else "(keine zweite Zeile)"
    text = (
        f"Bei Zählerstand {zaehlerstand} erwartet als zweite Zeile: {erwartet}\n"
        f"Ihr Programm gibt aus:\n" + "\n".join(zeilen)
    )
    return vergleichbar(tatsaechlich) == vergleichbar(erwartet), text


# naechste_wartung hat einen Docstring
assert docstring_von(naechste_wartung), (
    f"naechste_wartung.__doc__ ist {naechste_wartung.__doc__!r}, erwartet war ein Text.\n"
    'Tipp: Schreiben Sie den Docstring in drei Anführungszeichen """…""" als erste Zeile direkt unter die def-Zeile.'
)

# Der Docstring von naechste_wartung nennt Zählerstand und Wartung
text = vergleichbar(docstring_von(naechste_wartung) or "")
assert "zählerstand" in text and "wartung" in text, (
    f"Der Docstring von naechste_wartung ist {naechste_wartung.__doc__!r}.\n"
    "Erwartet war ein Satz, der sagt, was die Funktion zurückgibt, mit den Wörtern Zählerstand und Wartung."
)

# In naechste_wartung steht ein Kommentar über der return-Zeile
kommentare = kommentare_in("naechste_wartung")
assert kommentare != [], (
    "In naechste_wartung steht kein Kommentar.\n"
    "Tipp: Schreiben Sie über die return-Zeile eine Zeile, die mit # beginnt und erklärt, warum dort + 1 steht."
)

# Der Kommentar ist ein Kommentar und kein Docstring-Ersatz: der Docstring bleibt erste Zeile
assert docstring_von(naechste_wartung) is not None and len(kommentare) > 0, (
    "naechste_wartung braucht beides: einen Docstring als erste Zeile und darunter einen Kommentar mit #."
)

# wartung_bald hat einen Docstring
assert docstring_von(wartung_bald), (
    f"wartung_bald.__doc__ ist {wartung_bald.__doc__!r}, erwartet war ein Text.\n"
    'Tipp: Der Docstring """…""" muss die erste Zeile im Rumpf sein, noch vor return.'
)

# Der Docstring von wartung_bald sagt, wann True herauskommt
assert "true" in vergleichbar(docstring_von(wartung_bald) or ""), (
    f"Der Docstring von wartung_bald ist {wartung_bald.__doc__!r}.\n"
    "Erwartet war ein Satz, der sagt, wann die Funktion True zurückgibt."
)

# Im Beispiel 148500 fehlen 1500 Seiten: Wartung jetzt einplanen
stimmt, text = entscheidung_stimmt(148500)
assert stimmt, text + "\nTipp: return naechste_wartung(zaehlerstand) - zaehlerstand <= vorlauf"

# Bei 120000 fehlen noch 30000 Seiten (nicht fest hinschreiben!)
stimmt, text = entscheidung_stimmt(120000)
assert stimmt, text

# wartung_bald gibt True oder False zurück
ergebnis = wartung_bald(149000, 2000)
assert ergebnis is True or ergebnis is False, (
    f"wartung_bald(149000, 2000) ergibt {ergebnis!r}, erwartet war True.\n"
    "Tipp: Ein Vergleich wie a <= b ist schon True oder False; geben Sie ihn mit return zurück, statt ihn auszugeben."
)

# Randfall: genau 2000 Seiten vorher wird schon eingeplant
stimmt, text = entscheidung_stimmt(148000)
assert stimmt, text + "\nTipp: „höchstens 2000 Seiten“ schließt 2000 ein, also <= statt <."

# Randfall: 2001 Seiten vorher noch nicht
stimmt, text = entscheidung_stimmt(147999)
assert stimmt, text

# wartung_bald benutzt den Vorlauf aus dem Aufruf
assert wartung_bald(140000, 10000) is True and wartung_bald(140000, 5000) is False, (
    f"wartung_bald(140000, 10000) ergibt {wartung_bald(140000, 10000)!r} und wartung_bald(140000, 5000) "
    f"{wartung_bald(140000, 5000)!r}, erwartet waren True und False.\nTipp: Vergleichen Sie mit vorlauf, nicht mit 2000."
)

# Randfall: Zählerstand 0
stimmt, text = entscheidung_stimmt(0)
assert stimmt, text

# Randfall: genau auf einer Wartung, die nächste kommt erst 50 000 Seiten später
stimmt, text = entscheidung_stimmt(100000)
assert stimmt, text

# Viele zufällige Zählerstände bis zur oberen Grenze
zufall = Zufall(1048)
staende = [10000000, 9999999, 9998000] + [zufall.randint(0, 10000000) for _ in range(40)]
staende += [zufall.randint(1, 200) * 50000 - zufall.randint(0, 2500) for _ in range(40)]
for stand in staende:
    stimmt, text = entscheidung_stimmt(stand)
    assert stimmt, text
