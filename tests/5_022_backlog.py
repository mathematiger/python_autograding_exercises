# Automatisch erzeugt aus lehrkraft/muster/5_022_backlog.py - nicht von Hand ändern.
# vorlage-hash: ef075abd9f1cbb32
# text-hash: 21e460892cf3fe96
# thema: datenstrukturen
# inhalt: Eigenes Mapping mit MutableMapping

def versuche(funktion):
    """Ruft funktion() auf; liefert (Ergebnis, None) oder (None, Ausnahme)."""
    try:
        return funktion(), None
    except Exception as fehler:
        return None, fehler


def inhalt(objekt):
    """Liest den Inhalt über die Schlüssel und [] aus, ohne auf dict(...) angewiesen zu sein."""
    try:
        return {schluessel: objekt[schluessel] for schluessel in objekt}
    except Exception as fehler:
        return f"({type(fehler).__name__}: {fehler})"


def neu(*argumente, **schluesselwoerter):
    """Erzeugt Schaetzungen; liefert das Objekt oder eine Beschreibung der Ausnahme."""
    try:
        return Schaetzungen(*argumente, **schluesselwoerter)
    except Exception as fehler:
        return f"({type(fehler).__name__}: {fehler})"


# Eintragen und Lesen mit demselben Schlüssel
p = neu()
ergebnis, fehler = versuche(lambda: (p.__setitem__("WEB-1", 5), p["WEB-1"], len(p))[1:])
assert ergebnis == (5, 1), (
    f'Nach p = Schaetzungen() und p["WEB-1"] = 5 ergeben p["WEB-1"] und len(p) {ergebnis!r} {fehler or ""}, '
    "erwartet war (5, 1).\nTipp: Legen Sie in __init__ self._daten = {} an, bevor Sie update aufrufen."
)

# Lesen mit anders geschriebenem Schlüssel
p = neu()
ergebnis, fehler = versuche(lambda: (p.__setitem__("WEB-12", 5), p[" web-12 "], p["Web-12"])[1:])
assert ergebnis == (5, 5), (
    f'Nach p["WEB-12"] = 5 ergeben p[" web-12 "] und p["Web-12"] {ergebnis!r} {fehler or ""}, erwartet war (5, 5).\n'
    "Tipp: Normalisieren Sie den Schlüssel in __getitem__ mit normalisiere(schluessel)."
)

# Eintragen mit anders geschriebenem Schlüssel überschreibt, statt einen zweiten Eintrag anzulegen
p = neu()
ergebnis, fehler = versuche(lambda: (p.__setitem__("web-12", 5), p.__setitem__(" WEB-12", 8), len(p), list(p))[2:])
assert ergebnis == (1, ["WEB-12"]), (
    f'Nach p["web-12"] = 5 und p[" WEB-12"] = 8 ergeben len(p) und list(p) {ergebnis!r} {fehler or ""}, '
    "erwartet war (1, ['WEB-12']).\nTipp: Normalisieren Sie auch in __setitem__, und __iter__ liefert die normalisierten Schlüssel."
)

# Das Beispiel aus der Aufgabe: Konstruktor mit Dictionary und Schlüsselwort
punkte = neu({"web-12": 5}, app_3=8)
ergebnis = inhalt(punkte)
assert ergebnis == {"WEB-12": 5, "APP_3": 8}, (
    f'Schaetzungen({{"web-12": 5}}, app_3=8) enthält {ergebnis!r}, erwartet war {{"WEB-12": 5, "APP_3": 8}}.\n'
    "Tipp: In __init__ übernimmt self.update(daten, **weitere) beides über Ihr __setitem__."
)

# Der Konstruktor nimmt auch eine Liste von Paaren
p = neu([("a-1", 1), ("B-2", 2), ("A-1", 3)])
ergebnis = inhalt(p)
assert ergebnis == {"A-1": 3, "B-2": 2}, f'Schaetzungen([("a-1", 1), ("B-2", 2), ("A-1", 3)]) enthält {ergebnis!r}, erwartet war {{"A-1": 3, "B-2": 2}}.'

# del mit anders geschriebenem Schlüssel
p = neu({"WEB-1": 1, "WEB-2": 2})
ergebnis, fehler = versuche(lambda: (p.__delitem__(" web-1"), list(p), len(p))[1:])
assert ergebnis == (["WEB-2"], 1), f'Nach del p[" web-1"] ergeben list(p) und len(p) {ergebnis!r} {fehler or ""}, erwartet war ([\'WEB-2\'], 1).'

# Ein fehlender Schlüssel löst bei [] und del einen KeyError aus
p = neu({"WEB-1": 1})
lesen = versuche(lambda: p["WEB-9"])[1]
loeschen = versuche(lambda: p.__delitem__("WEB-9"))[1]
assert isinstance(lesen, KeyError) and isinstance(loeschen, KeyError), (
    f'p["WEB-9"] und del p["WEB-9"] sollen einen KeyError auslösen, bekommen {lesen!r} und {loeschen!r}.'
)

# get, in und pop über die Mixin-Methoden normalisieren ebenfalls
p = neu({"WEB-12": 13})
ergebnis, fehler = versuche(lambda: ("web-12" in p, "api-1" in p, p.get(" Web-12 "), p.get("api-1", 0), p.pop("web-12"), len(p)))
assert ergebnis == (True, False, 13, 0, 13, 0), (
    f'in, get und pop ergeben {ergebnis!r} {fehler or ""}, erwartet war (True, False, 13, 0, 13, 0).\n'
    "Tipp: Diese Methoden erbt die Klasse von MutableMapping; sie brauchen bei fehlendem Schlüssel einen KeyError."
)

# Werte außerhalb der Skala: ValueError, alter Wert bleibt
p = neu({"WEB-1": 5})
for wert in [4, -1, 100, "5", None]:
    ergebnis, fehler = versuche(lambda: p.__setitem__("web-1", wert))
    assert isinstance(fehler, ValueError) and inhalt(p) == {"WEB-1": 5}, (
        f'p["web-1"] = {wert!r} soll einen ValueError auslösen und den Wert 5 lassen; bekommen {fehler!r}, '
        f"Inhalt danach {inhalt(p)!r}.\nTipp: Prüfen Sie zuerst, ob wert eine ganze Zahl aus SKALA ist."
    )

# True, False und 3.0 sind keine gültigen Schätzungen, obwohl sie wie 1, 0 und 3 vergleichen
p = neu()
for wert in [True, False, 3.0]:
    ergebnis, fehler = versuche(lambda: p.__setitem__("web-1", wert))
    assert isinstance(fehler, ValueError) and len(inhalt(p)) == 0, (
        f'p["web-1"] = {wert!r} soll einen ValueError auslösen, bekommen {fehler!r}, Inhalt danach {inhalt(p)!r}.\n'
        "Tipp: True == 1 und 3.0 == 3; prüfen Sie den Typ mit isinstance(wert, bool) und isinstance(wert, int)."
    )

# Alle Werte der Skala sind gültig, auch 0
p = neu()
ergebnis, fehler = versuche(lambda: [p.__setitem__(f"T-{wert}", wert) for wert in SKALA] and inhalt(p))
assert ergebnis == {f"T-{wert}": wert for wert in SKALA}, f"Alle Werte aus SKALA eintragen ergibt {ergebnis!r} {fehler or ''}."

# update prüft die Werte ebenfalls
p = neu({"WEB-1": 1})
update_fehler = versuche(lambda: p.update({"web-2": 7}))[1]
assert isinstance(update_fehler, ValueError) and inhalt(p) == {"WEB-1": 1}, (
    f'update({{"web-2": 7}}) soll einen ValueError auslösen (bekommen {update_fehler!r}) und nichts eintragen; '
    f'Inhalt danach {inhalt(p)!r}, erwartet {{"WEB-1": 1}}.\n'
    "Tipp: Das geerbte update von MutableMapping ruft Ihr __setitem__ auf; von dict geerbt täte es das nicht."
)

# setdefault normalisiert ebenfalls
p = neu({"WEB-1": 1})
ergebnis, fehler = versuche(lambda: (p.setdefault(" web-1", 21), p.setdefault("web-3", 2)))
assert ergebnis == (1, 2) and inhalt(p) == {"WEB-1": 1, "WEB-3": 2}, (
    f'setdefault(" web-1", 21) und setdefault("web-3", 2) sollen (1, 2) ergeben (bekommen {ergebnis!r} '
    f'{fehler or ""}); Inhalt danach {inhalt(p)!r}, erwartet {{"WEB-1": 1, "WEB-3": 2}}.\n'
    "Tipp: Das geerbte setdefault fragt erst p[schluessel] ab und trägt nur bei einem KeyError ein; "
    "löst Ihr __getitem__ bei einem fehlenden Schlüssel einen KeyError aus?"
)

# Ein ungültiger Wert im Konstruktor löst einen ValueError aus
ergebnis = neu({"WEB-1": 4})
assert isinstance(ergebnis, str) and "ValueError" in ergebnis, (
    f'Schaetzungen({{"WEB-1": 4}}) soll einen ValueError auslösen, ergibt aber {ergebnis!r}.'
)

# Reihenfolge des ersten Eintragens bleibt, auch beim Überschreiben
p = neu()
ergebnis, fehler = versuche(lambda: [p.__setitem__(k, w) for k, w in [("c", 1), ("a", 2), ("C", 3), ("b", 5)]] and list(p.items()))
assert ergebnis == [("C", 3), ("A", 2), ("B", 5)], f"Nach c=1, a=2, C=3, b=5 ergibt list(p.items()) {ergebnis!r} {fehler or ''}, erwartet war [('C', 3), ('A', 2), ('B', 5)]."

# Ist ein MutableMapping, vergleicht sich mit Dictionaries und ist kein dict
p = neu({"x": 1})
assert isinstance(p, MutableMapping) and not isinstance(p, dict) and p == {"X": 1}, (
    "Schaetzungen soll von collections.abc.MutableMapping erben (nicht von dict) und dann über das geerbte "
    f'__eq__ gleich {{"X": 1}} sein; bekommen {p!r}.'
)

# Zwei Objekte teilen ihre Daten nicht
a = neu()
b = neu()
versuche(lambda: a.__setitem__("WEB-1", 3))
assert len(inhalt(b)) == 0, f"Nach a[\"WEB-1\"] = 3 enthält ein anderes Objekt b {inhalt(b)!r}, erwartet war nichts.\nTipp: Legen Sie self._daten in __init__ an, nicht als Klassenattribut."

# Viele zufällige Operationen, verglichen mit einem Dictionary
zufall = Zufall(5022)
p = neu()
vergleich = {}
schritte = []
fehlerfall = None
for _ in range(2000):
    name = zufall.choice(["web-1", "WEB-2", "app_3", "Api-4", "db-5"])
    schluessel = zufall.choice(["", " ", "  "]) + zufall.choice([name, name.upper(), name.lower()]) + zufall.choice(["", " "])
    norm = schluessel.strip().upper()
    art = zufall.choice(["setzen", "setzen", "lesen", "loeschen", "get"])
    if art == "setzen":
        wert = zufall.choice(list(SKALA) + [4, 7, True, "3"])
        schritte = (schritte + [f"p[{schluessel!r}] = {wert!r}"])[-4:]
        _, fehler = versuche(lambda: p.__setitem__(schluessel, wert))
        gueltig = type(wert) is int and wert in SKALA
        if gueltig:
            vergleich[norm] = wert
        richtig = (fehler is None) == gueltig and (gueltig or isinstance(fehler, ValueError))
        erwartet_schritt = "keine Ausnahme" if gueltig else "ValueError"
    elif art == "lesen":
        schritte = (schritte + [f"p[{schluessel!r}]"])[-4:]
        ergebnis, fehler = versuche(lambda: p[schluessel])
        richtig = ergebnis == vergleich[norm] if norm in vergleich else isinstance(fehler, KeyError)
        erwartet_schritt = repr(vergleich[norm]) if norm in vergleich else "KeyError"
    elif art == "loeschen":
        schritte = (schritte + [f"del p[{schluessel!r}]"])[-4:]
        _, fehler = versuche(lambda: p.__delitem__(schluessel))
        richtig = (fehler is None) == (norm in vergleich) and (norm in vergleich or isinstance(fehler, KeyError))
        erwartet_schritt = "keine Ausnahme" if norm in vergleich else "KeyError"
        vergleich.pop(norm, None)
    else:
        schritte = (schritte + [f"p.get({schluessel!r})"])[-4:]
        ergebnis, fehler = versuche(lambda: p.get(schluessel))
        richtig = ergebnis == vergleich.get(norm) and fehler is None
        erwartet_schritt = repr(vergleich.get(norm))
    if not richtig or inhalt(p) != vergleich:
        fehlerfall = (schritte, fehler, vergleich, inhalt(p), erwartet_schritt)
        break
assert fehlerfall is None, (
    f"Nach den letzten Schritten {'; '.join(fehlerfall[0])}: beim letzten Schritt erwartet {fehlerfall[4]}, "
    f"Ausnahme dabei {fehlerfall[1]!r},\n"
    f"  Inhalt erwartet {fehlerfall[2]}\n  bekommen        {fehlerfall[3]}"
)

# Obere Grenze: 100 000 Einträge, Zugriffe in O(1)
gross = neu()
for nummer in range(100_000):
    gross[f"t-{nummer}"] = SKALA[nummer % len(SKALA)]
ergebnis, schritte = zaehle_schritte(lambda: (gross[" T-99999 "], "t-50000" in gross, gross.get("t-1"), len(gross)))
assert ergebnis == (SKALA[99_999 % 8], True, 1, 100_000) and schritte <= 40, (
    f"Bei 100 000 Einträgen ergeben [], in, get und len {ergebnis!r} mit {schritte} Schritten; "
    f"erwartet waren {(SKALA[99_999 % 8], True, 1, 100_000)} mit höchstens 40 Schritten, also O(1) je Zugriff.\n"
    "Tipp: Schlagen Sie im internen Dictionary nach, statt die Schlüssel zu durchsuchen."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar("13"), f'Erwartete Ausgabe: "13" – Ihr Programm: "{AUSGABE}"'
