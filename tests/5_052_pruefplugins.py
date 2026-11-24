# Automatisch erzeugt aus lehrkraft/muster/5_052_pruefplugins.py - nicht von Hand ändern.
# vorlage-hash: 2a06ad09b0951c9b
# text-hash: 81337514d0a44325
# thema: programmaufbau
# inhalt: Plugins mit importlib laden

import pathlib

USV = 'GERAET = "USV Raum 1"\n\ndef pruefe(messwerte):\n    return messwerte["usv_ladung"] >= 50\n'
RAID = 'GERAET = "RAID Speicher 2"\n\ndef pruefe(messwerte):\n    return messwerte["raid_defekt"] == 0\n'
KUEHLUNG = 'GERAET = "Kühlung Raum A"\n\ndef pruefe(messwerte):\n    return messwerte["zuluft"] < 27\n'
zaehler = [0]


def neuer_name(wort):
    """Liefert einen Modulnamen, den noch kein Test benutzt hat, damit sys.modules nichts vorwegnimmt."""
    zaehler[0] += 1
    return f"t5052_{zaehler[0]}_{wort}"


def mit_plugins(dateien, aktion):
    """Legt dateien (relativer Pfad → Code) in einem frischen Ordner an und gibt aktion(ordner) zurück.

    Danach werden sys.path und die Module aus dem Ordner in sys.modules zurückgesetzt.
    """
    vorher = list(sys.path)
    with tempfile.TemporaryDirectory() as ordner:
        for pfad, code in dateien.items():
            datei = pathlib.Path(ordner, pfad)
            datei.parent.mkdir(parents=True, exist_ok=True)
            datei.write_text(code, encoding="utf-8")
        try:
            return aktion(ordner)
        finally:
            sys.path[:] = vorher
            for name in list(sys.modules):
                if name.startswith("t5052_"):
                    del sys.modules[name]


def versuche(funktion, *argumente):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(*argumente), None
    except Exception as fehler:
        return None, fehler


def lade_einzeln(ordner, name):
    """Ruft lade_plugin(name) mit ordner in sys.path auf; liefert (Ergebnis, Ausnahme)."""
    sys.path.insert(0, ordner)
    importlib.invalidate_caches()
    return versuche(lade_plugin, name)


def ist_modul(wert, name):
    """Prüft, ob wert das Modulobjekt mit dem Namen name ist."""
    return type(wert) is type(sys) and wert.__name__ == name


def beschreibe(wert):
    """Beschreibt ein Ergebnis kurz für Meldungen."""
    if type(wert) is type(sys):
        return f"<Modul {wert.__name__}>"
    text = repr(wert)
    return text if len(text) <= 300 else text[:300] + " …"


# lade_plugin: ein gültiges Plugin wird als Modulobjekt zurückgegeben
name = neuer_name("usv")
ergebnis, fehler = mit_plugins({f"{name}.py": USV}, lambda ordner: lade_einzeln(ordner, name))
assert fehler is None and ist_modul(ergebnis, name), (
    f"lade_plugin({name!r}) soll das Modulobjekt {name} zurückgeben, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: importlib.import_module(modulname) gibt das Modul zurück."
)

# lade_plugin: das Modul ist wirklich geladen, GERAET und pruefe sind benutzbar
name = neuer_name("raid")


def geraet_und_pruefung(ordner):
    """Lädt das RAID-Plugin und liefert GERAET und zwei Prüfergebnisse."""
    modul, fehler = lade_einzeln(ordner, name)
    if fehler is not None:
        return fehler
    return modul.GERAET, modul.pruefe({"raid_defekt": 0}), modul.pruefe({"raid_defekt": 1})


ergebnis = mit_plugins({f"{name}.py": RAID}, geraet_und_pruefung)
assert ergebnis == ("RAID Speicher 2", True, False), (
    f"Vom geladenen Plugin {name} erwartet: GERAET 'RAID Speicher 2' und pruefe mit True/False, "
    f"gefunden: {beschreibe(ergebnis)}."
)

# lade_plugin: ein zweiter Import liefert dasselbe Objekt aus sys.modules
name = neuer_name("zweimal")


def zweimal_laden(ordner):
    """Lädt dasselbe Plugin zweimal und liefert, ob beide Male dasselbe Objekt kam."""
    erstes, _ = lade_einzeln(ordner, name)
    zweites, _ = versuche(lade_plugin, name)
    return erstes is not None and erstes is zweites and sys.modules.get(name) is erstes


assert mit_plugins({f"{name}.py": USV}, zweimal_laden), (
    f"Zweimal lade_plugin({name!r}) soll beide Male dasselbe Modulobjekt liefern, und zwar das aus sys.modules.\n"
    "Tipp: Lesen Sie die Datei nicht selbst ein und führen Sie sie nicht mit exec aus; importlib.import_module benutzt den Cache sys.modules."
)

# lade_plugin: ein Modul in einem Paket (Name mit Punkt)
paket = neuer_name("kuehlung")
ergebnis, fehler = mit_plugins(
    {f"{paket}/__init__.py": "", f"{paket}/raum_a.py": KUEHLUNG},
    lambda ordner: lade_einzeln(ordner, f"{paket}.raum_a"),
)
assert fehler is None and ist_modul(ergebnis, f"{paket}.raum_a") and ergebnis.GERAET == "Kühlung Raum A", (
    f"lade_plugin({paket + '.raum_a'!r}) soll das Modul raum_a aus dem Paket {paket} liefern, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: import_module folgt den Punkten in Pakete hinein; zerlegen Sie den Namen nicht selbst."
)

# lade_plugin: ohne Funktion pruefe gibt es einen TypeError mit dem Modulnamen
name = neuer_name("ohne_pruefe")
ergebnis, fehler = mit_plugins({f"{name}.py": 'GERAET = "Klima"\n'}, lambda ordner: lade_einzeln(ordner, name))
assert isinstance(fehler, TypeError) and name in str(fehler), (
    f"lade_plugin({name!r}) für ein Plugin ohne pruefe soll einen TypeError mit dem Modulnamen auslösen, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: hasattr(modul, 'pruefe') oder getattr(modul, 'pruefe', None)."
)

# lade_plugin: ein pruefe, das keine Funktion ist, zählt nicht
name = neuer_name("pruefe_text")
code = 'GERAET = "Klima"\npruefe = "immer gut"\n'
ergebnis, fehler = mit_plugins({f"{name}.py": code}, lambda ordner: lade_einzeln(ordner, name))
assert isinstance(fehler, TypeError) and name in str(fehler), (
    f"lade_plugin({name!r}) für ein Plugin mit pruefe = 'immer gut' (ein Text) soll einen TypeError auslösen, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: callable(...) sagt, ob man etwas aufrufen kann."
)

# lade_plugin: ohne GERAET gibt es einen TypeError mit dem Modulnamen
name = neuer_name("ohne_geraet")
code = "def pruefe(messwerte):\n    return True\n"
ergebnis, fehler = mit_plugins({f"{name}.py": code}, lambda ordner: lade_einzeln(ordner, name))
assert isinstance(fehler, TypeError) and name in str(fehler), (
    f"lade_plugin({name!r}) für ein Plugin ohne GERAET soll einen TypeError mit dem Modulnamen auslösen, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
)

# lade_plugin: GERAET muss ein Text sein
name = neuer_name("geraet_zahl")
code = "GERAET = 7\n\ndef pruefe(messwerte):\n    return True\n"
ergebnis, fehler = mit_plugins({f"{name}.py": code}, lambda ordner: lade_einzeln(ordner, name))
assert isinstance(fehler, TypeError) and name in str(fehler), (
    f"lade_plugin({name!r}) für ein Plugin mit GERAET = 7 soll einen TypeError auslösen, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: isinstance(getattr(modul, 'GERAET', None), str)."
)

# lade_alle: das Beispiel mit zwei Plugins und einem fehlenden
usv, raid, lueftung = neuer_name("usv"), neuer_name("raid"), neuer_name("lueftung")
ergebnis, fehler = mit_plugins(
    {f"{usv}.py": USV, f"{raid}.py": RAID}, lambda ordner: versuche(lade_alle, ordner, [usv, raid, lueftung])
)
geladen, fehlerhaft = ergebnis if isinstance(ergebnis, tuple) and len(ergebnis) == 2 else ({}, {})
assert (
    fehler is None
    and isinstance(geladen, dict)
    and list(geladen) == [usv, raid]
    and ist_modul(geladen[usv], usv)
    and ist_modul(geladen[raid], raid)
), (
    f"lade_alle(ordner, {[usv, raid, lueftung]}) soll als erstes Element ein Dictionary mit den Modulen {usv} und "
    "{raid} liefern, ergab " + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: Setzen Sie ordner vorn in sys.path (sys.path.insert(0, ordner)), bevor Sie importieren."
)

# lade_alle: das fehlende Plugin steht in fehlerhaft, die Meldung beginnt mit dem Namen der Ausnahme
assert isinstance(fehlerhaft, dict) and list(fehlerhaft) == [lueftung] and str(
    fehlerhaft[lueftung]
).startswith("ModuleNotFoundError"), (
    f"Als zweites Element erwartet: {{{lueftung!r}: \"ModuleNotFoundError: No module named …\"}}, "
    f"gefunden: {beschreibe(fehlerhaft)}.\nTipp: f\"{{type(fehler).__name__}}: {{fehler}}\""
)

# lade_alle: ein Plugin mit Fehler beim Import hält die anderen nicht auf
kaputt, usv = neuer_name("kaputt"), neuer_name("usv")
ergebnis, fehler = mit_plugins(
    {f"{kaputt}.py": 'GERAET = "Defekt"\ngrenze = 50 / 0\n', f"{usv}.py": USV},
    lambda ordner: versuche(lade_alle, ordner, [kaputt, usv]),
)
geladen, fehlerhaft = ergebnis if isinstance(ergebnis, tuple) and len(ergebnis) == 2 else ({}, {})
assert (
    fehler is None
    and list(geladen) == [usv]
    and list(fehlerhaft) == [kaputt]
    and str(fehlerhaft[kaputt]).startswith("ZeroDivisionError")
), (
    f"Ein Plugin, das beim Import durch 0 teilt, soll mit 'ZeroDivisionError: …' in fehlerhaft landen und {usv} "
    "trotzdem geladen werden; lade_alle ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: Fremder Code kann beim Import jede Ausnahme auslösen; fangen Sie hier Exception ab."
)

# lade_alle: ein Syntaxfehler im Plugin landet ebenfalls in fehlerhaft
kaputt, raid = neuer_name("syntax"), neuer_name("raid")
ergebnis, fehler = mit_plugins(
    {f"{kaputt}.py": "def pruefe(messwerte)\n    return True\n", f"{raid}.py": RAID},
    lambda ordner: versuche(lade_alle, ordner, [raid, kaputt]),
)
geladen, fehlerhaft = ergebnis if isinstance(ergebnis, tuple) and len(ergebnis) == 2 else ({}, {})
assert fehler is None and list(geladen) == [raid] and str(fehlerhaft.get(kaputt, "")).startswith("SyntaxError"), (
    f"Ein Plugin mit Syntaxfehler soll mit 'SyntaxError: …' in fehlerhaft landen; lade_alle ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
)

# lade_alle: Plugins ohne pruefe stehen mit dem TypeError von lade_plugin in fehlerhaft
ohne, usv = neuer_name("ohne"), neuer_name("usv")
ergebnis, fehler = mit_plugins(
    {f"{ohne}.py": 'GERAET = "Klima"\n', f"{usv}.py": USV}, lambda ordner: versuche(lade_alle, ordner, [ohne, usv])
)
geladen, fehlerhaft = ergebnis if isinstance(ergebnis, tuple) and len(ergebnis) == 2 else ({}, {})
assert fehler is None and list(geladen) == [usv] and str(fehlerhaft.get(ohne, "")).startswith("TypeError"), (
    f"Ein Plugin ohne pruefe soll mit 'TypeError: …' in fehlerhaft landen; lade_alle ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: Benutzen Sie in lade_alle die Funktion lade_plugin, dann wird auch hier geprüft."
)

# lade_alle: ordner kommt vorn in sys.path und gewinnt gegen ein gleichnamiges Modul anderswo
usv = neuer_name("usv")


def mit_doppelgaenger(ordner):
    """Legt ein gleichnamiges Modul in einen zweiten Ordner vorn in sys.path und ruft dann lade_alle auf."""
    with tempfile.TemporaryDirectory() as anderswo:
        pathlib.Path(anderswo, f"{usv}.py").write_text(USV.replace("USV Raum 1", "Alte Kopie"), encoding="utf-8")
        sys.path.insert(0, anderswo)
        ergebnis, fehler = versuche(lade_alle, ordner, [usv])
        if fehler is not None:
            return fehler
        return ergebnis[0][usv].GERAET if usv in ergebnis[0] else ergebnis


ergebnis = mit_plugins({f"{usv}.py": USV}, mit_doppelgaenger)
assert ergebnis == "USV Raum 1", (
    f"Liegt ein gleichnamiges Modul in einem anderen Ordner von sys.path, soll lade_alle trotzdem das Plugin aus "
    f"ordner laden (GERAET 'USV Raum 1'), gefunden: {beschreibe(ergebnis)}.\n"
    "Tipp: Python nimmt den ersten Treffer in sys.path; setzen Sie ordner mit sys.path.insert(0, ordner) ganz nach vorn."
)

# lade_alle: Module in Paketen
paket = neuer_name("kuehlung")
ergebnis, fehler = mit_plugins(
    {f"{paket}/__init__.py": "", f"{paket}/raum_a.py": KUEHLUNG},
    lambda ordner: versuche(lade_alle, ordner, [f"{paket}.raum_a"]),
)
geladen, fehlerhaft = ergebnis if isinstance(ergebnis, tuple) and len(ergebnis) == 2 else ({}, {})
assert fehler is None and list(geladen) == [f"{paket}.raum_a"] and fehlerhaft == {}, (
    f"lade_alle(ordner, [{paket + '.raum_a'!r}]) soll das Modul aus dem Paket laden; ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
)

# lade_alle: keine Plugins
ergebnis, fehler = mit_plugins({}, lambda ordner: versuche(lade_alle, ordner, []))
assert fehler is None and ergebnis == ({}, {}), (
    "lade_alle(ordner, []) soll ({}, {}) liefern, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
)


def pfad_nach_laden(namen, dateien):
    """Ruft lade_alle auf und liefert sys.path danach sowie sys.path vorher."""

    def aktion(ordner):
        """Lädt die Plugins und vergleicht sys.path vorher und nachher."""
        vorher = list(sys.path)
        versuche(lade_alle, ordner, namen)
        return list(sys.path), vorher

    return mit_plugins(dateien, aktion)


# lade_alle: sys.path sieht danach aus wie vorher
usv = neuer_name("usv")
nachher, vorher = pfad_nach_laden([usv], {f"{usv}.py": USV})
assert nachher == vorher, (
    f"Nach lade_alle soll sys.path wieder aussehen wie vorher. Zusätzlich oder anders: "
    f"{[pfad for pfad in nachher if pfad not in vorher] or nachher[:3]}.\n"
    "Tipp: Nehmen Sie den Ordner am Ende mit sys.path.remove(ordner) wieder heraus."
)

# lade_alle: sys.path wird auch aufgeräumt, wenn Plugins fehlen oder kaputt sind
kaputt = neuer_name("kaputt")
nachher, vorher = pfad_nach_laden([neuer_name("fehlt"), kaputt], {f"{kaputt}.py": "1 / 0\n"})
assert nachher == vorher, (
    "Auch wenn Plugins fehlen oder beim Import abstürzen, soll sys.path danach aussehen wie vorher.\n"
    "Tipp: try/finally räumt in jedem Fall auf."
)

# lade_alle: geladene Plugins funktionieren nach dem Aufräumen weiter
usv = neuer_name("usv")


def laden_und_pruefen(ordner):
    """Lädt das USV-Plugin und ruft danach pruefe auf."""
    ergebnis, fehler = versuche(lade_alle, ordner, [usv])
    if fehler is not None:
        return fehler
    modul = ergebnis[0][usv]
    return modul.pruefe({"usv_ladung": 80}), modul.pruefe({"usv_ladung": 20})


ergebnis = mit_plugins({f"{usv}.py": USV}, laden_und_pruefen)
assert ergebnis == (True, False), (
    f"Nach lade_alle sollte pruefe des geladenen Plugins weiter funktionieren, ergab {beschreibe(ergebnis)}."
)


def auffaellige_mit(dateien, messwerte):
    """Lädt alle Plugins aus dateien mit der Vergleichslösung und ruft auffaellige auf."""

    def aktion(ordner):
        """Lädt die Plugins von Hand und ruft auffaellige auf."""
        sys.path.insert(0, ordner)
        importlib.invalidate_caches()
        plugins = {}
        for pfad in dateien:
            name = pfad[:-3]
            plugins[name] = importlib.import_module(name)
        return versuche(auffaellige, plugins, messwerte)

    return mit_plugins(dateien, aktion)


# auffaellige: das Beispiel
usv, raid = neuer_name("usv"), neuer_name("raid")
ergebnis, fehler = auffaellige_mit({f"{usv}.py": USV, f"{raid}.py": RAID}, {"usv_ladung": 35, "raid_defekt": 0})
assert fehler is None and ergebnis == ["USV Raum 1"], (
    "auffaellige(geladen, {'usv_ladung': 35, 'raid_defekt': 0}) soll ['USV Raum 1'] liefern, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
    + "\nTipp: Rufen Sie für jedes Modul modul.pruefe(messwerte) auf und sammeln Sie modul.GERAET."
)

# auffaellige: andere Messwerte (nicht fest hinschreiben!)
usv, raid, kuehl = neuer_name("usv"), neuer_name("raid"), neuer_name("kuehl")
dateien = {f"{usv}.py": USV, f"{raid}.py": RAID, f"{kuehl}.py": KUEHLUNG}
ergebnis, fehler = auffaellige_mit(dateien, {"usv_ladung": 90, "raid_defekt": 1, "zuluft": 30})
assert fehler is None and ergebnis == ["Kühlung Raum A", "RAID Speicher 2"], (
    "Bei raid_defekt 1 und zuluft 30 erwartet: ['Kühlung Raum A', 'RAID Speicher 2'] (alphabetisch), ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
)

# auffaellige: alles in Ordnung
ergebnis, fehler = auffaellige_mit(
    {f"{neuer_name('usv')}.py": USV, f"{neuer_name('raid')}.py": RAID}, {"usv_ladung": 50, "raid_defekt": 0}
)
assert fehler is None and ergebnis == [], (
    "Wenn alle Prüfungen True ergeben, soll auffaellige [] liefern, ergab "
    + (f"{type(fehler).__name__}: {fehler}." if fehler else f"{beschreibe(ergebnis)}.")
)

# auffaellige: keine Plugins
ergebnis, fehler = versuche(auffaellige, {}, {"usv_ladung": 10})
assert fehler is None and ergebnis == [], f"auffaellige({{}}, …) soll [] liefern, ergab {beschreibe(ergebnis)}."

# Das Programm benutzt importlib.import_module
assert verwendet("import_module"), (
    "Laden Sie die Plugins mit importlib.import_module(modulname), nicht mit exec oder open."
)

# Viele zufällige Plugin-Sammlungen bis zur oberen Grenze von 50 Plugins
zufall = Zufall(5052)
ARTEN = ["gut", "fehlt", "absturz", "syntax", "ohne_pruefe", "geraet_zahl"]


def plugin_code(art, geraet, grenze):
    """Liefert den Code eines Plugins der Art art; bei "fehlt" None."""
    if art == "gut":
        return f"GERAET = {geraet!r}\n\ndef pruefe(messwerte):\n    return messwerte['wert'] >= {grenze}\n"
    if art == "absturz":
        return "raise RuntimeError('Sensor nicht erreichbar')\n"
    if art == "syntax":
        return "def pruefe(:\n"
    if art == "ohne_pruefe":
        return f"GERAET = {geraet!r}\n"
    if art == "geraet_zahl":
        return "GERAET = 42\n\ndef pruefe(messwerte):\n    return True\n"
    return None


ERWARTETE_AUSNAHME = {
    "fehlt": "ModuleNotFoundError",
    "absturz": "RuntimeError",
    "syntax": "SyntaxError",
    "ohne_pruefe": "TypeError",
    "geraet_zahl": "TypeError",
}


def zufallsrunde(anzahl):
    """Erzeugt anzahl zufällige Plugins, lädt sie und prüft alles; liefert eine Beschreibung des Fehlers oder None."""
    namen, dateien, arten, grenzen = [], {}, {}, {}
    for nummer in range(anzahl):
        art = zufall.choice(ARTEN)
        name = neuer_name(art)
        grenzen[name] = zufall.randint(0, 100)
        code = plugin_code(art, f"Anlage {nummer:02d}", grenzen[name])
        if code is not None:
            dateien[f"{name}.py"] = code
        namen.append(name)
        arten[name] = art
    wert = zufall.randint(0, 100)

    def aktion(ordner):
        """Lädt die Plugins und ruft auffaellige auf; prüft dabei auch sys.path."""
        vorher = list(sys.path)
        ergebnis, fehler = versuche(lade_alle, ordner, namen)
        if fehler is not None:
            return f"lade_alle ist mit {type(fehler).__name__}: {fehler} abgestürzt."
        if sys.path != vorher:
            return "Nach lade_alle sieht sys.path anders aus als vorher."
        geladen, fehlerhaft = ergebnis
        gute = [name for name in namen if arten[name] == "gut"]
        if list(geladen) != gute:
            return f"Bei {anzahl} Plugins erwartet geladen: {gute}, gefunden: {list(geladen)}."
        for name in namen:
            if arten[name] == "gut":
                continue
            meldung = str(fehlerhaft.get(name, ""))
            if not meldung.startswith(ERWARTETE_AUSNAHME[arten[name]]):
                return (
                    f"Plugin {name} (Art {arten[name]}) erwartet in fehlerhaft mit "
                    f"{ERWARTETE_AUSNAHME[arten[name]]}: …, gefunden: {meldung!r}."
                )
        erwartet = sorted(geladen[name].GERAET for name in gute if wert < grenzen[name])
        ergebnis, fehler = versuche(auffaellige, geladen, {"wert": wert})
        if fehler is not None or ergebnis != erwartet:
            return f"auffaellige mit wert {wert} erwartet {erwartet}, ergab {beschreibe(ergebnis or fehler)}."
        return None

    return mit_plugins(dateien, aktion)


for anzahl in [1, 3, 6, 10, 50]:
    fehler = zufallsrunde(anzahl)
    assert fehler is None, fehler
