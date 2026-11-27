# Automatisch erzeugt aus lehrkraft/muster/5_025_zugriffspruefung.py - nicht von Hand ändern.
# vorlage-hash: 6c2bd923aee2c3cb
# text-hash: 82b8d59f998856c0
# thema: fehler
# inhalt: __exit__ unterdrückt Ausnahmen

class EigenerFehler(PermissionError):
    """Eine Unterklasse von PermissionError für die Tests."""


def block(abwehr, ausnahme):
    """Führt einen with-Block aus, der ausnahme auslöst (oder nichts bei None).

    Gibt die Ausnahme zurück, die aus dem Block herauskam, oder None.
    """
    try:
        with abwehr:
            if ausnahme is not None:
                raise ausnahme
    except Exception as fehler:
        return fehler
    return None


# Eine erwartete Ausnahme wird unterdrückt
abwehr = Abwehr([], PermissionError)
heraus = block(abwehr, PermissionError("kein Zugriff"))
assert heraus is None, (
    f"Ein PermissionError im Block von Abwehr(bericht, PermissionError) kam heraus: {heraus!r}.\n"
    "Tipp: Geben Sie in __exit__ True zurück, damit Python die Ausnahme verwirft."
)

# Die unterdrückte Ausnahme steht im Bericht
bericht = []
block(Abwehr(bericht, PermissionError), PermissionError("kein Zugriff auf /etc/shadow"))
assert bericht == [("PermissionError", "kein Zugriff auf /etc/shadow")], (
    f"Nach einem PermissionError('kein Zugriff auf /etc/shadow') ist bericht {bericht!r}, "
    "erwartet war [('PermissionError', 'kein Zugriff auf /etc/shadow')].\n"
    "Tipp: type(wert).__name__ liefert den Klassennamen, str(wert) die Meldung."
)

# Das Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar("läuft weiter\n[('PermissionError', 'kein Zugriff auf /etc/shadow')]"), (
    f"Erwartete Ausgabe:\nläuft weiter\n[('PermissionError', 'kein Zugriff auf /etc/shadow')]\nIhr Programm:\n{AUSGABE}"
)

# Eine andere Ausnahme schlägt durch, unverändert
bericht = []
abwehr = Abwehr(bericht, PermissionError, TimeoutError)
vorher = block(abwehr, PermissionError("erlaubt"))
ausnahme = KeyError("Tippfehler")
heraus = block(abwehr, ausnahme)
assert vorher is None and heraus is ausnahme, (
    "Abwehr(bericht, PermissionError, TimeoutError): erst ein PermissionError (erwartet unterdrückt, "
    f"herausgekommen {vorher!r}), dann ein KeyError (erwartet unverändert heraus, herausgekommen {heraus!r}).\n"
    "Tipp: Geben Sie True nur für die erwarteten Arten zurück, für alle anderen False."
)

# Eine durchschlagende Ausnahme kommt nicht in den Bericht
bericht = []
abwehr = Abwehr(bericht, PermissionError)
block(abwehr, PermissionError("erlaubt"))
block(abwehr, KeyError("Tippfehler"))
assert bericht == [("PermissionError", "erlaubt")], (
    f"Nach PermissionError('erlaubt') und KeyError('Tippfehler') bei Abwehr(bericht, PermissionError) ist bericht "
    f"{bericht!r}, erwartet war nur [('PermissionError', 'erlaubt')]."
)

# Ohne Ausnahme: kein Eintrag, nichts kommt heraus
bericht = []
abwehr = Abwehr(bericht, PermissionError)
block(abwehr, PermissionError("erlaubt"))
heraus = block(abwehr, None)
assert heraus is None and bericht == [("PermissionError", "erlaubt")], (
    "Erst ein PermissionError('erlaubt'), dann ein Block ohne Ausnahme: erwartet keine Ausnahme und bericht "
    f"[('PermissionError', 'erlaubt')] (kein zweiter Eintrag), bekommen {heraus!r} und {bericht!r}."
)

# __enter__ gibt das Objekt selbst zurück
abwehr = Abwehr([], PermissionError)
with abwehr as wert:
    pass
assert wert is abwehr, f"with abwehr as a: a ist {wert!r}, erwartet war das Abwehr-Objekt selbst."

# abgefangen enthält die unterdrückte Ausnahme
abwehr = Abwehr([], PermissionError)
ausnahme = PermissionError("Dienst gesperrt")
block(abwehr, ausnahme)
assert getattr(abwehr, "abgefangen", "(fehlt)") is ausnahme, (
    f"Nach einem unterdrückten PermissionError ist abgefangen {getattr(abwehr, 'abgefangen', '(fehlt)')!r}, "
    "erwartet war genau dieses Ausnahme-Objekt."
)

# Beim nächsten Block beginnt abgefangen wieder mit None
abwehr = Abwehr([], PermissionError)
block(abwehr, PermissionError("Dienst gesperrt"))
with abwehr as wert:
    zwischendurch = wert.abgefangen
assert zwischendurch is None and abwehr.abgefangen is None, (
    "Nach einem unterdrückten PermissionError und einem weiteren Block ohne Ausnahme soll abgefangen "
    f"None sein (schon innerhalb des Blocks); bekommen: im Block {zwischendurch!r}, danach {abwehr.abgefangen!r}.\n"
    "Tipp: Setzen Sie abgefangen in __enter__ auf None."
)

# Mehrere Arten: jede wird abgefangen
bericht = []
abwehr = Abwehr(bericht, PermissionError, TimeoutError)
heraus = [block(abwehr, PermissionError("a")), block(abwehr, TimeoutError("b"))]
assert heraus == [None, None] and bericht == [("PermissionError", "a"), ("TimeoutError", "b")], (
    "Abwehr(bericht, PermissionError, TimeoutError), dann ein PermissionError('a') und ein TimeoutError('b'): "
    f"erwartet keine Ausnahme und bericht [('PermissionError', 'a'), ('TimeoutError', 'b')]; "
    f"herausgekommen {heraus!r}, bericht {bericht!r}."
)

# Unterklassen zählen mit, im Bericht steht der Name der Unterklasse
bericht = []
heraus = [
    block(Abwehr(bericht, OSError), FileNotFoundError("fehlt.txt")),
    block(Abwehr(bericht, PermissionError), EigenerFehler("eigen")),
]
assert heraus == [None, None] and bericht == [("FileNotFoundError", "fehlt.txt"), ("EigenerFehler", "eigen")], (
    "Abwehr(bericht, OSError) mit FileNotFoundError('fehlt.txt') und Abwehr(bericht, PermissionError) mit einer "
    "Unterklasse EigenerFehler('eigen'): erwartet beide unterdrückt und bericht "
    f"[('FileNotFoundError', 'fehlt.txt'), ('EigenerFehler', 'eigen')]; herausgekommen {heraus!r}, bericht {bericht!r}.\n"
    "Tipp: isinstance(wert, self.arten) zählt Unterklassen mit; vergleichen Sie nicht typ == art."
)

# Eine Oberklasse wird nicht abgefangen, wenn nur die Unterklasse erlaubt ist
bericht = []
abwehr = Abwehr(bericht, PermissionError)
block(abwehr, PermissionError("erlaubt"))
ausnahme = OSError("Platte voll")
heraus = block(abwehr, ausnahme)
assert heraus is ausnahme and bericht == [("PermissionError", "erlaubt")], (
    "Abwehr(bericht, PermissionError), erst PermissionError('erlaubt'), dann OSError('Platte voll'): Der OSError muss "
    "herauskommen (PermissionError ist die Unterklasse, nicht umgekehrt), im Bericht steht nur der PermissionError; "
    f"herausgekommen {heraus!r}, bericht {bericht!r}."
)

# Viele zufällige Blöcke mit demselben Objekt, verglichen mit einer Nachrechnung
zufall = Zufall(5025)
vorrat = [PermissionError, TimeoutError, FileNotFoundError, KeyError, ValueError, OSError, EigenerFehler, ZeroDivisionError]
for runde in range(40):
    arten = tuple(zufall.sample(vorrat, zufall.randint(1, 4)))
    bericht = []
    abwehr = Abwehr(bericht, *arten)
    erwartet = []
    verlauf = []
    for schritt in range(25):
        art = zufall.choice(vorrat + [None])
        ausnahme = None if art is None else art(f"Meldung {schritt}")
        verlauf.append("nichts" if art is None else art.__name__)
        heraus = block(abwehr, ausnahme)
        abfangen = ausnahme is not None and isinstance(ausnahme, arten)
        if abfangen:
            erwartet.append((art.__name__, str(ausnahme)))
        erwartet_heraus = None if abfangen else ausnahme
        assert heraus is erwartet_heraus and bericht == erwartet and abwehr.abgefangen is (ausnahme if abfangen else None), (
            f"Abwehr(bericht, {', '.join(a.__name__ for a in arten)}), dann Blöcke mit {', '.join(verlauf)}:\n"
            f"  beim letzten Block erwartet herauskommend {erwartet_heraus!r}, bekommen {heraus!r}\n"
            f"  bericht erwartet {erwartet}\n  bericht bekommen {bericht}\n"
            f"  abgefangen erwartet {ausnahme if abfangen else None!r}, bekommen {abwehr.abgefangen!r}"
        )

# Obere Grenze: 10 Arten und 10 000 Blöcke mit demselben Objekt
bericht = []
arten = (PermissionError, TimeoutError, FileNotFoundError, KeyError, ValueError, IndexError, TypeError, NameError, LookupError, ArithmeticError)
abwehr = Abwehr(bericht, *arten)
durchgeschlagen = 0
for nummer in range(10000):
    if block(abwehr, RuntimeError("x") if nummer % 4 == 0 else PermissionError("y")) is not None:
        durchgeschlagen += 1
assert durchgeschlagen == 2500 and len(bericht) == 7500, (
    "10 000 Blöcke, jeder vierte mit RuntimeError (nicht abgefangen), die übrigen mit PermissionError: "
    f"erwartet 2500 durchgeschlagen und 7500 Einträge im Bericht, bekommen {durchgeschlagen} und {len(bericht)}."
)
