# Automatisch erzeugt aus lehrkraft/muster/5_025_anmeldeschutz.py - nicht von Hand ändern.
# vorlage-hash: 98846062a006e82b
# text-hash: 20984d4542444f75
# thema: fehler
# inhalt: __exit__ unterdrückt Ausnahmen

class Netzwerkfehler(Exception):
    """Ein Fehler, für den der Anmeldeschutz nicht zuständig ist."""


def block(schutz, ausnahme):
    """Führt einen with-Block aus, der ausnahme auslöst (oder keine bei None).

    Liefert (was mit der Ausnahme passiert ist, ob der Rest des Blocks lief): "unterdrückt",
    "durchgelassen" oder "durchgelassen, aber verändert: …".
    """
    rest_gelaufen = False
    try:
        with schutz:
            if ausnahme is not None:
                raise ausnahme
            rest_gelaufen = True
    except BaseException as angekommen:
        if angekommen is ausnahme:
            return "durchgelassen", rest_gelaufen
        return f"durchgelassen, aber verändert: {type(angekommen).__name__}: {angekommen}", rest_gelaufen
    if ausnahme is None:
        return "ohne Ausnahme", rest_gelaufen
    return "unterdrückt", rest_gelaufen


def falsch(name="admin"):
    """Ein neuer Fehlversuch für name."""
    return Zugriffsverweigert(f"{name}: falsches Passwort")


# __init__ und __enter__: das Protokoll ist leer, with … as liefert den Schutz selbst
schutz = Anmeldeschutz(3)
try:
    with schutz as zurueck:
        pass
except Exception as ausnahme:
    zurueck = ausnahme
protokoll = getattr(schutz, "fehlversuche", "(fehlt)")
assert zurueck is schutz and protokoll == [], (
    f"Nach Anmeldeschutz(3) erwartet: with schutz as s liefert s = schutz und fehlversuche == []; bekommen "
    f"s = {zurueck!r}, fehlversuche = {protokoll!r}.\nTipp: __enter__ gibt return self zurück."
)

# Ohne Ausnahme läuft der Block durch und nichts wird protokolliert
schutz = Anmeldeschutz(3)
ergebnis, rest = block(schutz, None)
assert ergebnis == "ohne Ausnahme" and rest and schutz.fehlversuche == [], (
    f"Ein with-Block ohne Ausnahme soll ganz laufen und nichts protokollieren; Ergebnis: {ergebnis}, "
    f"fehlversuche: {schutz.fehlversuche!r}.\nTipp: Ohne Ausnahme ist typ None; dann gibt __exit__ einfach False zurück."
)

# Ohne Ausnahme gibt __exit__ False zurück
schutz = Anmeldeschutz(3)
schutz.__enter__()
rueckgabe = schutz.__exit__(None, None, None)
assert rueckgabe is False, f"schutz.__exit__(None, None, None) gibt {rueckgabe!r} zurück, erwartet war False."

# Ein Fehlversuch wird unterdrückt
schutz = Anmeldeschutz(3)
ergebnis, rest = block(schutz, falsch())
assert ergebnis == "unterdrückt", (
    f"Bei Anmeldeschutz(3) soll der erste Zugriffsverweigert unterdrückt werden; die Ausnahme wurde {ergebnis}.\n"
    "Tipp: Gibt __exit__ True zurück, gilt die Ausnahme als erledigt."
)

# Der Rest des Blocks läuft nach der Ausnahme nicht weiter
schutz = Anmeldeschutz(3)
ergebnis, rest = block(schutz, falsch())
assert not rest, "Nach der Ausnahme wurde der Rest des with-Blocks trotzdem ausgeführt; das darf nicht passieren."

# Der Fehlversuch steht mit seiner Meldung im Protokoll
schutz = Anmeldeschutz(3)
block(schutz, falsch("gast"))
assert schutz.fehlversuche == ["gast: falsches Passwort"], (
    f"Nach einem Fehlversuch mit der Meldung 'gast: falsches Passwort' ist fehlversuche {schutz.fehlversuche!r}, "
    "erwartet war ['gast: falsches Passwort'].\nTipp: Hängen Sie str(wert) an, nicht typ oder wert selbst."
)

# Beim Unterdrücken gibt __exit__ genau True zurück
schutz = Anmeldeschutz(3)
fehler = falsch()
rueckgabe = schutz.__exit__(Zugriffsverweigert, fehler, None)
assert rueckgabe is True, f"__exit__ gibt beim Unterdrücken {rueckgabe!r} zurück, erwartet war True."

# Fehlversuche bis zur Grenze werden unterdrückt, der nächste kommt durch
schutz = Anmeldeschutz(2)
ergebnisse = [block(schutz, falsch())[0] for _ in range(3)]
assert ergebnisse == ["unterdrückt", "unterdrückt", "durchgelassen"], (
    f"Bei Anmeldeschutz(2) erwartet: zwei Fehlversuche unterdrückt, der dritte durchgelassen; bekommen: {ergebnisse}.\n"
    "Tipp: Unterdrückt wird, solange danach höchstens erlaubte_fehler Einträge im Protokoll stehen (<=)."
)

# Auch der durchgelassene Fehlversuch wird protokolliert, und weitere kommen ebenfalls durch
schutz = Anmeldeschutz(2)
ergebnisse = [block(schutz, falsch(f"nutzer{nummer}"))[0] for nummer in range(5)]
erwartet = [f"nutzer{nummer}: falsches Passwort" for nummer in range(5)]
assert ergebnisse[2:] == ["durchgelassen"] * 3 and schutz.fehlversuche == erwartet, (
    f"Bei Anmeldeschutz(2) und fünf Fehlversuchen erwartet: die letzten drei durchgelassen und alle fünf im "
    f"Protokoll; bekommen: {ergebnisse}, fehlversuche = {schutz.fehlversuche!r}."
)

# Beim Durchlassen gibt __exit__ False zurück und löst nicht selbst neu aus
schutz = Anmeldeschutz(0)
fehler = falsch()
try:
    rueckgabe = schutz.__exit__(Zugriffsverweigert, fehler, None)
except BaseException as ausnahme:
    rueckgabe = f"selbst ausgelöst: {type(ausnahme).__name__}"
assert rueckgabe is False, (
    f"__exit__ gibt beim Durchlassen {rueckgabe!r} zurück, erwartet war False.\n"
    "Tipp: Lösen Sie die Ausnahme nicht mit raise neu aus; return False lässt sie mit ihrem Traceback weiterlaufen."
)

# Grenze 0: schon der erste Fehlversuch kommt durch
schutz = Anmeldeschutz(0)
ergebnis, _ = block(schutz, falsch())
assert ergebnis == "durchgelassen" and schutz.fehlversuche == ["admin: falsches Passwort"], (
    f"Bei Anmeldeschutz(0) soll schon der erste Fehlversuch durchkommen und protokolliert werden; die Ausnahme "
    f"wurde {ergebnis}, fehlversuche = {schutz.fehlversuche!r}."
)

# Unterklassen von Zugriffsverweigert zählen auch
schutz = Anmeldeschutz(1)
ergebnis, _ = block(schutz, PasswortAbgelaufen("gast: Passwort abgelaufen"))
assert ergebnis == "unterdrückt" and schutz.fehlversuche == ["gast: Passwort abgelaufen"], (
    f"PasswortAbgelaufen ist eine Unterklasse von Zugriffsverweigert und soll ebenso unterdrückt und protokolliert "
    f"werden; die Ausnahme wurde {ergebnis}, fehlversuche = {schutz.fehlversuche!r}.\n"
    "Tipp: issubclass(typ, Zugriffsverweigert) erkennt auch Unterklassen, typ == Zugriffsverweigert nicht."
)

# Andere Ausnahmen kommen unverändert durch und werden nicht protokolliert
schutz = Anmeldeschutz(5)
ergebnisse = [
    block(schutz, ValueError("kaputt"))[0],
    block(schutz, Netzwerkfehler("Server weg"))[0],
    block(schutz, KeyError("admin"))[0],
]
assert ergebnisse == ["durchgelassen"] * 3 and schutz.fehlversuche == [], (
    f"ValueError, ein eigener Netzwerkfehler und KeyError sollen unverändert durchkommen und nicht im Protokoll "
    f"landen; bekommen: {ergebnisse}, fehlversuche = {schutz.fehlversuche!r}.\n"
    "Tipp: Nur Zugriffsverweigert und seine Unterklassen gehen den Schutz etwas an."
)

# Auch KeyboardInterrupt und SystemExit kommen durch
schutz = Anmeldeschutz(5)
ergebnisse = [block(schutz, KeyboardInterrupt())[0], block(schutz, SystemExit(1))[0]]
assert ergebnisse == ["durchgelassen", "durchgelassen"] and schutz.fehlversuche == [], (
    f"KeyboardInterrupt und SystemExit sollen durchkommen und nicht protokolliert werden; bekommen: {ergebnisse}, "
    f"fehlversuche = {schutz.fehlversuche!r}."
)

# Andere Ausnahmen zählen nicht zur Grenze
schutz = Anmeldeschutz(1)
ergebnisse = [block(schutz, ValueError("x"))[0], block(schutz, falsch())[0], block(schutz, falsch())[0]]
assert ergebnisse == ["durchgelassen", "unterdrückt", "durchgelassen"], (
    f"Bei Anmeldeschutz(1): ValueError, dann zwei Fehlversuche; erwartet durchgelassen, unterdrückt, "
    f"durchgelassen; bekommen {ergebnisse}."
)

# Erfolgreiche Anmeldungen dazwischen ändern nichts
schutz = Anmeldeschutz(1)
ergebnisse = []
for passwort in ["falsch", "Sommer2026!", "auch falsch"]:
    try:
        with schutz:
            anmelden("admin", passwort)
        ergebnisse.append("weiter")
    except Zugriffsverweigert:
        ergebnisse.append("gesperrt")
assert ergebnisse == ["weiter", "weiter", "gesperrt"] and len(schutz.fehlversuche) == 2, (
    f"Bei Anmeldeschutz(1) und den Passwörtern falsch, richtig, falsch erwartet: weiter, weiter, gesperrt und zwei "
    f"Einträge im Protokoll; bekommen {ergebnisse}, fehlversuche = {schutz.fehlversuche!r}."
)

# Zwei Schutz-Objekte zählen getrennt
erster = Anmeldeschutz(1)
zweiter = Anmeldeschutz(1)
block(erster, falsch())
ergebnis, _ = block(zweiter, falsch())
assert ergebnis == "unterdrückt" and len(erster.fehlversuche) == 1 and len(zweiter.fehlversuche) == 1, (
    f"Zwei Anmeldeschutz(1) mit je einem Fehlversuch: beim zweiten Objekt wurde die Ausnahme {ergebnis}, "
    f"Protokolle {erster.fehlversuche!r} und {zweiter.fehlversuche!r}.\n"
    "Tipp: Legen Sie fehlversuche in __init__ auf self an, nicht als Klassenattribut."
)

# Viele zufällige Abläufe, verglichen mit einer Nachrechnung
zufall = Zufall(5025)
for runde in range(200):
    grenze = zufall.randint(0, 6)
    schutz = Anmeldeschutz(grenze)
    protokoll = []
    ablauf = []
    for schritt in range(12):
        art = zufall.choice(["ok", "falsch", "falsch", "abgelaufen", "ValueError", "Netzwerkfehler"])
        ausnahme = {
            "ok": None,
            "falsch": Zugriffsverweigert(f"versuch{schritt}: falsches Passwort"),
            "abgelaufen": PasswortAbgelaufen(f"versuch{schritt}: abgelaufen"),
            "ValueError": ValueError(f"versuch{schritt}"),
            "Netzwerkfehler": Netzwerkfehler(f"versuch{schritt}"),
        }[art]
        ablauf.append(art)
        if isinstance(ausnahme, Zugriffsverweigert):
            protokoll.append(str(ausnahme))
            erwartet = "unterdrückt" if len(protokoll) <= grenze else "durchgelassen"
        elif ausnahme is None:
            erwartet = "ohne Ausnahme"
        else:
            erwartet = "durchgelassen"
        ergebnis, _ = block(schutz, ausnahme)
        assert ergebnis == erwartet and schutz.fehlversuche == protokoll, (
            f"Anmeldeschutz({grenze}) mit den Blöcken {ablauf}: beim letzten erwartet {erwartet} und fehlversuche "
            f"{protokoll!r}; bekommen {ergebnis} und {schutz.fehlversuche!r}."
        )

# Obere Grenze: 10 000 Fehlversuche bei Grenze 1000
schutz = Anmeldeschutz(1000)
unterdrueckt = 0
for nummer in range(10_000):
    if block(schutz, falsch(f"n{nummer}"))[0] == "unterdrückt":
        unterdrueckt += 1
assert unterdrueckt == 1000 and len(schutz.fehlversuche) == 10_000, (
    f"Bei Anmeldeschutz(1000) und 10 000 Fehlversuchen erwartet 1000 unterdrückte und 10 000 Einträge im "
    f"Protokoll; bekommen {unterdrueckt} unterdrückte und {len(schutz.fehlversuche)} Einträge."
)

# Die Ausgabe des Programms stimmt
erwartet = "Konto gesperrt\n" + str(["admin: falsches Passwort"] * 3)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"
