# Automatisch erzeugt aus lehrkraft/muster/5_016_benachrichtigung.py - nicht von Hand ändern.
# vorlage-hash: 54d29e6764b6db2b
# text-hash: 635466603c76c9d3
# thema: klassen
# inhalt: typing.Protocol

import inspect
import typing


class Testkanal:
    """Kanal für die Tests: schreibt jeden Aufruf in ein gemeinsames Protokoll und antwortet wie vorgegeben."""

    def __init__(self, name, max_zeichen, antwort, aufrufe):
        self.name = name
        self.max_zeichen = max_zeichen
        self.antwort = antwort
        self.aufrufe = aufrufe

    def sende(self, empfaenger, text):
        """Merkt sich den Aufruf; gibt die Antwort zurück oder löst sie aus, wenn sie eine Ausnahmeklasse ist."""
        self.aufrufe.append((self.name, empfaenger, text))
        if isinstance(self.antwort, type):
            raise self.antwort(f"{self.name} kaputt")
        return self.antwort


class OhneMaxZeichen:
    """Hat name und sende, aber kein max_zeichen."""

    name = "ohne_max"

    def sende(self, empfaenger, text):
        """Würde immer zustellen."""
        return True


class OhneSende:
    """Hat name und max_zeichen, aber kein sende."""

    def __init__(self):
        self.name = "ohne_sende"
        self.max_zeichen = 50


class OhneName:
    """Hat max_zeichen und sende, aber keinen name."""

    max_zeichen = 50

    def sende(self, empfaenger, text):
        """Würde immer zustellen."""
        return True


def gekuerzt(text, max_zeichen):
    """Vergleichslösung für das Kürzen."""
    if len(text) <= max_zeichen:
        return text
    return text[: max_zeichen - 1] + "…"


def von_hand(beschreibung, empfaenger, text):
    """Vergleichslösung: gibt (Ergebnis, erwartete Aufrufe) zurück; beschreibung sind (name, max_zeichen, antwort) oder Nicht-Kanäle als Text."""
    for position, eintrag in enumerate(beschreibung):
        if isinstance(eintrag, str):
            return f"TypeError mit Position {position}", []
    aufrufe = []
    for name, max_zeichen, antwort in beschreibung:
        aufrufe.append((name, empfaenger, gekuerzt(text, max_zeichen)))
        if antwort is OSError or antwort is False:
            continue
        if antwort is ValueError:
            return "ValueError", aufrufe
        return name, aufrufe
    return None, aufrufe


NICHT_KANAELE = {"None": None, "7": 7, "'sms'": "sms", "OhneMaxZeichen()": OhneMaxZeichen(), "OhneSende()": OhneSende(), "OhneName()": OhneName()}


def baue(beschreibung, aufrufe):
    """Baut aus der Beschreibung die Liste der Objekte für benachrichtige."""
    objekte = []
    for eintrag in beschreibung:
        if isinstance(eintrag, str):
            objekte.append(NICHT_KANAELE[eintrag])
        else:
            objekte.append(Testkanal(*eintrag, aufrufe))
    return objekte


def lauf(beschreibung, empfaenger, text):
    """Ruft benachrichtige mit den Objekten zur Beschreibung auf; gibt (Ergebnis, Aufrufe) zurück."""
    aufrufe = []
    objekte = baue(beschreibung, aufrufe)
    try:
        ergebnis = benachrichtige(objekte, empfaenger, text)
    except TypeError as fehler:
        ergebnis = f"TypeError {fehler}"
    except ValueError:
        ergebnis = "ValueError"
    return ergebnis, aufrufe


def passt(bekommen, erwartet):
    """Vergleicht (Ergebnis, Aufrufe); beim TypeError genügt, dass die Position in der Meldung steht."""
    ergebnis, aufrufe = bekommen
    soll, soll_aufrufe = erwartet
    if isinstance(soll, str) and soll.startswith("TypeError"):
        position = soll.split()[-1]
        return isinstance(ergebnis, str) and ergebnis.startswith("TypeError") and position in ergebnis[10:] and aufrufe == []
    return ergebnis == soll and aufrufe == soll_aufrufe


# Kanal ist ein Protokoll, das man mit isinstance prüfen kann
try:
    isinstance(object(), Kanal)
    pruefbar = True
except TypeError:
    pruefbar = False
except NameError:
    pruefbar = None
assert pruefbar is not None and typing.Protocol in getattr(Kanal, "__mro__", ()) and pruefbar, (
    "Kanal soll eine Klasse sein, die von typing.Protocol erbt und mit @runtime_checkable dekoriert ist, "
    f"damit isinstance funktioniert; isinstance(object(), Kanal) "
    + {True: "funktioniert.", False: "löst einen TypeError aus.\nTipp: Setzen Sie @runtime_checkable über die Klasse.",
       None: "scheitert, weil es Kanal noch nicht gibt."}[pruefbar]
)

# Kanäle der Teams und unpassende Objekte
ergebnis = {
    "EMail()": isinstance(EMail(), Kanal),
    "SMS()": isinstance(SMS(), Kanal),
    "Testkanal": isinstance(Testkanal("t", 5, True, []), Kanal),
    "Wandanzeige()": isinstance(Wandanzeige(), Kanal),
}
for name, objekt in NICHT_KANAELE.items():
    ergebnis[name] = isinstance(objekt, Kanal)
erwartet = {name: name in ("EMail()", "SMS()", "Testkanal") for name in ergebnis}
assert ergebnis == erwartet, (
    f"isinstance(…, Kanal) ergibt {ergebnis}, erwartet war {erwartet}.\n"
    "Tipp: Das Protokoll braucht genau name: str, max_zeichen: int und die Methode sende; "
    "fehlt einem Objekt einer davon, ist es kein Kanal."
)

# Die Kanäle erben nicht von Kanal
ergebnis = [klasse.__name__ for klasse in (EMail, SMS, Protokollkanal) if Kanal in klasse.__mro__]
assert ergebnis == [], (
    f"{ergebnis} erbt von Kanal; ein Protokoll wirkt strukturell, darum soll Protokollkanal ohne Basisklasse auskommen."
)

# Protokollkanal hat die verlangten Attribute und gilt als Kanal
standard = Protokollkanal()
eigener = Protokollkanal(max_zeichen=7)
ergebnis = (standard.name, standard.max_zeichen, standard.verlauf, eigener.max_zeichen, isinstance(standard, Kanal))
assert ergebnis == ("protokoll", 1000, [], 7, True), (
    "Protokollkanal() soll name 'protokoll', max_zeichen 1000 und einen leeren verlauf haben, Protokollkanal(max_zeichen=7) "
    f"max_zeichen 7, und beide sollen Kanäle sein; bekommen (name, max_zeichen, verlauf, max_zeichen, isinstance): {ergebnis!r}."
)

# Protokollkanal sammelt Nachrichten, jedes Objekt für sich
erster = Protokollkanal()
zweiter = Protokollkanal()
antworten = (erster.sende("a", "x"), erster.sende("b", ""))
ergebnis = (antworten, erster.verlauf, zweiter.verlauf)
assert ergebnis == ((True, True), [("a", "x"), ("b", "")], []), (
    f"Nach erster.sende('a', 'x') und erster.sende('b', '') ergeben (Rückgaben, erster.verlauf, zweiter.verlauf) {ergebnis!r}; "
    "erwartet war ((True, True), [('a', 'x'), ('b', '')], []).\n"
    "Tipp: Legen Sie verlauf in __init__ an, nicht als Klassenattribut, sonst teilen sich alle Objekte eine Liste."
)

# Beispiele aus der Aufgabe
text = "INC-4711: Reaktionsfrist abgelaufen, bitte übernehmen"
kurz = Protokollkanal(max_zeichen=10)
ergebnis = (
    benachrichtige([SMS(), EMail()], "+491701234567", text),
    benachrichtige([SMS(), EMail()], "netz@firma.example", text),
    benachrichtige([SMS(erreichbar=False), kurz], "+4930123", text),
    kurz.verlauf,
)
erwartet = ("sms", "email", "protokoll", [("+4930123", "INC-4711:…")])
assert ergebnis == erwartet, (
    f"Die Beispiele aus der Aufgabe ergeben {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Ein OSError beim SMS-Gateway heißt: weiter zum nächsten Kanal; gekürzt wird auf max_zeichen - 1 Zeichen plus '…'."
)

# Der erste erfolgreiche Kanal beendet die Suche, spätere werden nicht gefragt
beschreibung = [("a", 100, False), ("b", 100, True), ("c", 100, True)]
ergebnis = lauf(beschreibung, "team", "Hallo")
erwartet = ("b", [("a", "team", "Hallo"), ("b", "team", "Hallo")])
assert ergebnis == erwartet, (
    f"Bei den Kanälen a (False), b (True), c (True) ergibt benachrichtige (Ergebnis, Aufrufe) {ergebnis!r}, "
    f"erwartet war {erwartet!r}.\nTipp: Nach dem ersten True sofort den name zurückgeben."
)

# Kein Kanal stellt zu: None; leere Liste: None
ergebnisse = (lauf([("a", 5, False), ("b", 5, OSError)], "x", "abc"), lauf([], "x", "abc"))
erwartet = ((None, [("a", "x", "abc"), ("b", "x", "abc")]), (None, []))
assert ergebnisse == erwartet, f"Ohne erfolgreichen Kanal und bei leerer Liste ergeben sich {ergebnisse!r}, erwartet war {erwartet!r}."

# Kürzen genau an der Grenze
text = "abcdefghij"
ergebnis = lauf([("genau", 10, False), ("eins_weniger", 9, False), ("eins", 1, False), ("zwei", 2, False)], "x", text)[1]
erwartet = [("genau", "x", "abcdefghij"), ("eins_weniger", "x", "abcdefgh…"), ("eins", "x", "…"), ("zwei", "x", "a…")]
assert ergebnis == erwartet, (
    f"Mit dem Text {text!r} bekommen Kanäle mit max_zeichen 10, 9, 1 und 2 die Texte {[aufruf[2] for aufruf in ergebnis]!r}, "
    f"erwartet waren {[aufruf[2] for aufruf in erwartet]!r}.\n"
    "Tipp: Nur kürzen, wenn len(text) > max_zeichen; dann text[:max_zeichen - 1] + '…', zusammen genau max_zeichen Zeichen."
)

# Leerer Text und leerer Empfänger werden unverändert weitergegeben
ergebnis = lauf([("a", 1, True)], "", "")
assert ergebnis == ("a", [("a", "", "")]), f"benachrichtige mit leerem Empfänger und Text ergibt {ergebnis!r}, erwartet war ('a', [('a', '', '')])."

# Andere Ausnahmen als OSError werden weitergegeben
ergebnis = lauf([("a", 5, OSError), ("b", 5, ValueError), ("c", 5, True)], "x", "y")
assert ergebnis == ("ValueError", [("a", "x", "y"), ("b", "x", "y")]), (
    f"Bei a (OSError), b (ValueError), c (True) ergibt benachrichtige (Ergebnis, Aufrufe) {ergebnis!r}; erwartet war, "
    "dass der ValueError von b herauskommt und c nicht mehr gefragt wird.\nTipp: Fangen Sie nur OSError ab."
)

# Kein Kanal: TypeError mit Position, bevor etwas gesendet wird
for beschreibung, position in [([("a", 5, True), "7"], 1), (["None"], 0), ([("a", 5, True), ("b", 5, True), "OhneSende()", "'sms'"], 2)]:
    aufrufe = []
    objekte = baue(beschreibung, aufrufe)
    try:
        benachrichtige(objekte, "x", "y")
        meldung = None
    except TypeError as fehler:
        meldung = str(fehler)
    assert meldung is not None and str(position) in meldung and aufrufe == [], (
        f"benachrichtige mit {beschreibung} soll einen TypeError mit der Position {position} in der Meldung auslösen, "
        f"ohne vorher zu senden; Meldung: {meldung!r}, gesendet: {aufrufe!r}.\n"
        "Tipp: Prüfen Sie erst alle Elemente mit isinstance(kanal, Kanal) und senden Sie erst danach."
    )

# Wandanzeige ist kein Kanal
try:
    benachrichtige([EMail(), Wandanzeige()], "a@b.example", "Test")
    meldung = None
except TypeError as fehler:
    meldung = str(fehler)
assert meldung is not None and "1" in meldung, (
    f"benachrichtige([EMail(), Wandanzeige()], …) soll einen TypeError mit der Position 1 auslösen; Meldung: {meldung!r}."
)

# benachrichtige prüft mit dem Protokoll
try:
    quelltext = inspect.getsource(benachrichtige)
except (OSError, TypeError, NameError):
    quelltext = ""
assert "isinstance" in quelltext and "Kanal" in quelltext, (
    "benachrichtige soll mit isinstance(…, Kanal) prüfen, ob ein Objekt ein Kanal ist, statt die Attribute einzeln abzufragen."
)

# 300 zufällige Listen von Kanälen und anderen Objekten
zufall = Zufall(5016)
fehlerfall = None
for _ in range(300):
    beschreibung = []
    for nummer in range(zufall.randint(0, 6)):
        if zufall.random() < 0.1:
            beschreibung.append(zufall.choice(list(NICHT_KANAELE)))
        else:
            antwort = zufall.choice([False, False, False, True, OSError, OSError, ValueError])
            beschreibung.append((f"k{nummer}", zufall.choice([1, 2, zufall.randint(1, 30), 10000]), antwort))
    text = "".join(zufall.choice("abc ä…") for _ in range(zufall.choice([0, 1, zufall.randint(0, 40)])))
    empfaenger = zufall.choice(["", "+49", "bereitschaft@firma.example"])
    bekommen = lauf(beschreibung, empfaenger, text)
    erwartet = von_hand(beschreibung, empfaenger, text)
    if not passt(bekommen, erwartet):
        fehlerfall = (beschreibung, empfaenger, text, bekommen, erwartet)
        break
assert fehlerfall is None, (
    f"benachrichtige mit den Kanälen {fehlerfall[0]} (name, max_zeichen, Antwort von sende; Texte sind Objekte, die kein "
    f"Kanal sind), empfaenger {fehlerfall[1]!r} und text {fehlerfall[2]!r} ergibt (Ergebnis, Aufrufe)\n"
    f"{fehlerfall[3]!r}\nerwartet war\n{fehlerfall[4]!r}"
)

# An der oberen Grenze: 1000 Kanäle, 10 000 Zeichen langer Text
zufall = Zufall(51016)
text = "".join(zufall.choice("abcdefghij") for _ in range(10000))
empfaenger = "+" + "9" * 9999
beschreibung = [(f"k{nummer}", zufall.randint(1, 10000), zufall.choice([False, OSError])) for nummer in range(999)]
beschreibung.append(("letzter", 10000, True))
bekommen = lauf(beschreibung, empfaenger, text)
erwartet = von_hand(beschreibung, empfaenger, text)
abweichung = next((nummer for nummer, (a, b) in enumerate(zip(bekommen[1], erwartet[1])) if a != b), None)
assert bekommen == erwartet, (
    f"Bei 1000 Kanälen, von denen nur der letzte zustellt, und einem Text mit 10 000 Zeichen ergibt benachrichtige "
    f"{bekommen[0]!r} nach {len(bekommen[1])} Aufrufen, erwartet war {erwartet[0]!r} nach {len(erwartet[1])} Aufrufen."
    + (
        f"\nBeim Aufruf {abweichung} (max_zeichen {beschreibung[abweichung][1]}) bekam der Kanal einen Text der Länge "
        f"{len(bekommen[1][abweichung][2])}, der mit {bekommen[1][abweichung][2][-3:]!r} endet; erwartet war die Länge "
        f"{len(erwartet[1][abweichung][2])}, Ende {erwartet[1][abweichung][2][-3:]!r}."
        if abweichung is not None else ""
    )
)

# An der oberen Grenze: das 1000. Objekt ist kein Kanal
beschreibung = [(f"k{nummer}", 50, True) for nummer in range(999)] + ["OhneName()"]
bekommen = lauf(beschreibung, "x", "y")
assert passt(bekommen, ("TypeError mit Position 999", [])), (
    f"Bei 999 Kanälen und einem letzten Objekt ohne name ergibt benachrichtige {bekommen[0]!r} nach {len(bekommen[1])} "
    "Aufrufen; erwartet war ein TypeError mit der Position 999, ohne dass vorher gesendet wird."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "sms\nemail\nprotokoll [('+4930123', 'INC-4711:…')]\nTrue False\nTypeError"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
