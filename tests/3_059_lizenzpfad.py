# Automatisch erzeugt aus lehrkraft/muster/3_059_lizenzpfad.py - nicht von Hand ändern.
# vorlage-hash: 11dd084d7967263a
# text-hash: 12ea07c971e6a567
# thema: algorithmen
# inhalt: Tiefensuche rekursiv, Pfad

import copy

ABH = {
    "kassensystem": ["oberflaeche", "datenbanktreiber"],
    "oberflaeche": ["grafik", "schriften"],
    "datenbanktreiber": ["verschluesselung"],
    "grafik": ["bildformate"],
    "verschluesselung": ["zufallszahlen"],
    "bildformate": ["kompression"],
}
KREIS = {"a": ["b"], "b": ["c"], "c": ["a", "d"]}


def wert_von(funktion, *argumente):
    """Ruft funktion mit Kopien der Argumente auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*copy.deepcopy(argumente))
    except RecursionError:
        return "RecursionError (die Rekursion hört nicht auf)"
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def erreichbar(abhaengigkeiten, start):
    """Vergleichslösung: alle von start aus erreichbaren Pakete, mit einer Liste als Stapel."""
    gesehen = {start}
    offen = [start]
    while offen:
        paket = offen.pop()
        for naechstes in abhaengigkeiten.get(paket, []):
            if naechstes not in gesehen:
                gesehen.add(naechstes)
                offen.append(naechstes)
    return gesehen


def fehler_im_weg(abhaengigkeiten, start, ziel, weg):
    """Gibt zurück, was an weg nicht stimmt, oder None, wenn er ein richtiger Weg ist."""
    if ziel not in erreichbar(abhaengigkeiten, start):
        return None if weg is None else "es gibt keinen Weg, erwartet war None"
    if not isinstance(weg, list) or not weg:
        return "erwartet war eine Liste von Paketen"
    if weg[0] != start or weg[-1] != ziel:
        return f"der Weg muss mit {start!r} beginnen und mit {ziel!r} enden"
    for vorher, nachher in zip(weg, weg[1:]):
        if nachher not in abhaengigkeiten.get(vorher, []):
            return f"{vorher!r} benutzt {nachher!r} nicht direkt"
    if len(set(weg)) != len(weg):
        return "ein Paket kommt zweimal vor"
    return None


def pruefe_pfad(abhaengigkeiten, start, ziel, hinweis=""):
    """Prüft pfad(abhaengigkeiten, start, ziel); liefert (stimmt, Meldung)."""
    weg = wert_von(pfad, abhaengigkeiten, start, ziel)
    fehler = fehler_im_weg(abhaengigkeiten, start, ziel, weg)
    gezeigt = abhaengigkeiten if len(abhaengigkeiten) <= 8 else f"<{len(abhaengigkeiten)} Pakete>"
    kurz = repr(weg) if len(repr(weg)) <= 300 else repr(weg)[:200] + " …"
    text = f"pfad({gezeigt}, {start!r}, {ziel!r}) ergibt {kurz}; {fehler}.{hinweis}"
    return fehler is None, text


def pruefe_begruendung(abhaengigkeiten, produkt, verdaechtig, hinweis=""):
    """Prüft begruendung gegen die erreichbaren Pakete und jeden Weg einzeln; liefert (stimmt, Meldung)."""
    ergebnis = wert_von(begruendung, abhaengigkeiten, produkt, verdaechtig)
    drin = erreichbar(abhaengigkeiten, produkt)
    erwartet = sorted(paket for paket in verdaechtig if paket in drin)
    gezeigt = abhaengigkeiten if len(abhaengigkeiten) <= 8 else f"<{len(abhaengigkeiten)} Pakete>"
    text = f"begruendung({gezeigt}, {produkt!r}, {verdaechtig})\nergibt {ergebnis!r}\n"
    if not isinstance(ergebnis, dict) or sorted(ergebnis) != erwartet:
        return False, text + f"erwartet waren genau die Schlüssel {erwartet}.{hinweis}"
    for paket, weg in ergebnis.items():
        fehler = fehler_im_weg(abhaengigkeiten, produkt, paket, weg)
        if fehler is not None:
            return False, text + f"Der Weg zu {paket!r} stimmt nicht: {fehler}.{hinweis}"
    return True, text


def zufallsgraph(zufall, pakete, kanten):
    """Erzeugt Abhängigkeiten zwischen den Paketen p0, p1, …, auch mit Kreisen."""
    abhaengigkeiten = {}
    for _ in range(kanten):
        von, nach = zufall.randrange(pakete), zufall.randrange(pakete)
        liste = abhaengigkeiten.setdefault(f"p{von}", [])
        if von != nach and f"p{nach}" not in liste:
            liste.append(f"p{nach}")
    return abhaengigkeiten


def rauten(stufen):
    """Erzeugt eine Kette von Rauten: zu jedem Paket der Kette führen zwei Wege."""
    abhaengigkeiten = {}
    for stufe in range(stufen):
        abhaengigkeiten[f"k{stufe}"] = [f"l{stufe}", f"r{stufe}"]
        abhaengigkeiten[f"l{stufe}"] = [f"k{stufe + 1}"]
        abhaengigkeiten[f"r{stufe}"] = [f"k{stufe + 1}"]
    return abhaengigkeiten


# pfad: das Beispiel
stimmt, text = pruefe_pfad(ABH, "kassensystem", "kompression")
assert stimmt, text

# pfad: ein anderes Ziel (nicht fest hinschreiben!)
stimmt, text = pruefe_pfad(ABH, "kassensystem", "zufallszahlen", "\nTipp: Probieren Sie alle direkten Pakete der Reihe nach.")
assert stimmt, text

# pfad: ein direktes Paket
stimmt, text = pruefe_pfad(ABH, "oberflaeche", "schriften")
assert stimmt, text

# pfad: kein Weg ergibt None
stimmt, text = pruefe_pfad(
    ABH, "datenbanktreiber", "schriften",
    "\nTipp: Hat kein direktes Paket Erfolg, geben Sie nach der Schleife None zurück.",
)
assert stimmt, text

# pfad: gegen die Richtung gibt es keinen Weg
stimmt, text = pruefe_pfad(ABH, "kompression", "kassensystem", "\nTipp: Die Abhängigkeiten gelten nur in eine Richtung.")
assert stimmt, text

# pfad: Start und Ziel gleich
stimmt, text = pruefe_pfad(ABH, "grafik", "grafik", "\nTipp: Ist paket schon das Ziel, ist der Weg [paket].")
assert stimmt, text

# pfad: ein Paket ohne eigene Abhängigkeiten
stimmt, text = pruefe_pfad(
    ABH, "schriften", "grafik", "\nTipp: Pakete ohne Abhängigkeiten fehlen als Schlüssel: abhaengigkeiten.get(paket, [])."
)
assert stimmt, text

# pfad: ein Kreis führt nicht in eine endlose Suche
stimmt, text = pruefe_pfad(KREIS, "a", "d", "\nTipp: Tragen Sie jedes Paket in besucht ein und gehen Sie nur in neue.")
assert stimmt, text

# pfad: im Kreis ohne Weg zum Ziel
stimmt, text = pruefe_pfad(KREIS, "a", "x")
assert stimmt, text

# pfad: keine Abhängigkeiten
stimmt, text = pruefe_pfad({}, "a", "b")
assert stimmt, text

# suche trägt besuchte Pakete in die übergebene Menge ein
besucht = set()
try:
    suche(copy.deepcopy(ABH), "datenbanktreiber", "schriften", besucht)
except Exception:
    pass
assert besucht >= {"datenbanktreiber", "verschluesselung"}, (
    f"Nach suche(abhaengigkeiten, 'datenbanktreiber', 'schriften', besucht) ist besucht {besucht}; "
    "erwartet war, dass mindestens 'datenbanktreiber' und 'verschluesselung' darin stehen."
)

# suche geht nicht in schon besuchte Pakete
ergebnis = wert_von(suche, ABH, "kassensystem", "kompression", {"grafik"})
assert ergebnis is None, (
    f"suche(abhaengigkeiten, 'kassensystem', 'kompression', {{'grafik'}}) ergibt {ergebnis!r}, erwartet war None, "
    "weil der einzige Weg über das schon besuchte Paket 'grafik' führt."
)

# suche ruft sich selbst auf
aufrufe = []
eigene_suche = suche


def suche(abhaengigkeiten, paket, ziel, besucht):
    """Zählt die Aufrufe und reicht sie an die eigene Funktion weiter."""
    aufrufe.append(paket)
    return eigene_suche(abhaengigkeiten, paket, ziel, besucht)


try:
    eigene_suche(copy.deepcopy(ABH), "kassensystem", "kompression", set())
except Exception:
    pass
suche = eigene_suche
assert len(aufrufe) >= 2, (
    f"suche hat sich auf dem Weg von 'kassensystem' zu 'kompression' {len(aufrufe)}-mal selbst aufgerufen; "
    "erwartet war eine rekursive Lösung, die für jedes nächste Paket suche(…) aufruft."
)

# pfad benutzt suche
aufrufe = []


def suche(abhaengigkeiten, paket, ziel, besucht):
    """Zählt die Aufrufe und reicht sie an die eigene Funktion weiter."""
    aufrufe.append(paket)
    return eigene_suche(abhaengigkeiten, paket, ziel, besucht)


try:
    pfad(copy.deepcopy(ABH), "kassensystem", "kompression")
except Exception:
    pass
suche = eigene_suche
assert aufrufe, "pfad ruft suche nicht auf. Benutzen Sie return suche(abhaengigkeiten, start, ziel, set())."

# begruendung: das Beispiel
stimmt, text = pruefe_begruendung(ABH, "kassensystem", ["zufallszahlen", "druckertreiber"])
assert stimmt, text

# begruendung: mehrere verdächtige Pakete
stimmt, text = pruefe_begruendung(ABH, "kassensystem", ["kompression", "schriften", "zufallszahlen"])
assert stimmt, text

# begruendung: nichts Verdächtiges steckt drin
stimmt, text = pruefe_begruendung(
    ABH, "oberflaeche", ["zufallszahlen"], "\nTipp: Nehmen Sie nur Pakete auf, für die pfad nicht None liefert."
)
assert stimmt, text

# begruendung: leere Liste
stimmt, text = pruefe_begruendung(ABH, "kassensystem", [])
assert stimmt, text

# begruendung: das Produkt selbst ist verdächtig
stimmt, text = pruefe_begruendung(
    ABH, "grafik", ["grafik", "kompression"], "\nTipp: Steht produkt selbst in verdaechtig, ist sein Weg [produkt]."
)
assert stimmt, text

# begruendung: jede Suche beginnt mit einer leeren Menge
stimmt, text = pruefe_begruendung(
    {"app": ["a", "b"], "a": ["x"], "b": ["x"], "x": ["y"]}, "app", ["y", "x"],
    "\nTipp: Eine Menge besucht aus einer früheren Suche versperrt der nächsten den Weg; pfad legt jedes Mal set() neu an.",
)
assert stimmt, text

# pfad verändert die Abhängigkeiten nicht
abhaengigkeiten = copy.deepcopy(ABH)
try:
    pfad(abhaengigkeiten, "kassensystem", "kompression")
except Exception:
    pass
assert abhaengigkeiten == ABH, f"Nach pfad ist abhaengigkeiten {abhaengigkeiten}; es sollte unverändert bleiben."

# Die Ausgabe des Programms
erwartet = (
    "['kassensystem', 'oberflaeche', 'grafik', 'bildformate', 'kompression']\n"
    "{'zufallszahlen': ['kassensystem', 'datenbanktreiber', 'verschluesselung', 'zufallszahlen']}"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Abhängigkeiten
zufall = Zufall(3059)
for _ in range(400):
    abhaengigkeiten = zufallsgraph(zufall, zufall.randint(1, 8), zufall.randint(0, 14))
    start = f"p{zufall.randint(0, 8)}"
    stimmt, text = pruefe_pfad(abhaengigkeiten, start, f"p{zufall.randint(0, 8)}")
    assert stimmt, text
    stimmt, text = pruefe_begruendung(abhaengigkeiten, start, [f"p{nummer}" for nummer in range(0, 9, 2)])
    assert stimmt, text

# Laufzeit: viele Wege zum selben Paket werden nicht mehrfach durchsucht
abhaengigkeiten = rauten(14)
try:
    weg, schritte = zaehle_schritte(pfad, abhaengigkeiten, "k0", "fehlt")
except RecursionError:
    weg, schritte = None, "(RecursionError)"
except Exception as fehler:
    weg, schritte = None, f"(Abbruch: {type(fehler).__name__}: {fehler})"
assert isinstance(schritte, int) and schritte <= 30 * 43, (
    f"Für 14 Rauten (43 Pakete, ohne Weg zum Ziel) braucht pfad {schritte} Schritte, erlaubt sind 30 · 43 = 1290.\n"
    "Tipp: Gehen Sie in kein Paket, das schon in besucht steht; ein erfolglos durchsuchtes Paket hilft auch "
    "beim zweiten Mal nicht."
)

# Obere Grenze: eine Kette aus 500 Paketen
abhaengigkeiten = {f"p{nummer}": [f"p{nummer + 1}"] for nummer in range(499)}
stimmt, text = pruefe_pfad(abhaengigkeiten, "p0", "p499")
assert stimmt, text

# Obere Grenze: 500 Pakete mit 5000 Abhängigkeiten
abhaengigkeiten = zufallsgraph(zufall, 500, 5000)
stimmt, text = pruefe_pfad(abhaengigkeiten, "p0", "p499")
assert stimmt, text

# Obere Grenze: begruendung bei 500 Paketen
stimmt, text = pruefe_begruendung(abhaengigkeiten, "p1", [f"p{nummer}" for nummer in range(0, 500, 10)])
assert stimmt, text
