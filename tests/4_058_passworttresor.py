# Automatisch erzeugt aus lehrkraft/muster/4_058_passworttresor.py - nicht von Hand ändern.
# vorlage-hash: 4b31cf1c961925d3
# text-hash: 38a47bf166da72bf
# thema: fehler
# inhalt: raise … from, Fehler umwandeln

BEISPIEL = {"vpn": "kim;67656865696d;400", "wiki": "ole;zz;500", "mail": "ada;616461;100"}


def ausnahme_von(aufruf):
    """Führt den Aufruf aus und gibt die ausgelöste Ausnahme zurück, sonst ("keine Ausnahme", Ergebnis)."""
    try:
        ergebnis = aufruf()
    except Exception as fehler:
        return fehler
    return ("keine Ausnahme", ergebnis)


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def beschreibe(fehler):
    """Klasse, Meldung und Ursachen einer Ausnahme, zum Anzeigen."""
    if not isinstance(fehler, BaseException):
        return repr(fehler)
    ursache = type(fehler.__cause__).__name__ if fehler.__cause__ is not None else None
    kontext = type(fehler.__context__).__name__ if fehler.__context__ is not None else None
    return f"{type(fehler).__name__}({str(fehler)!r}) mit __cause__={ursache}, __context__={kontext}, __suppress_context__={fehler.__suppress_context__}"


def hexadezimal(text):
    """Das Passwort, wie es im Tresor steht."""
    return text.encode("utf-8").hex()


# lies_eintrag im Beispiel
ergebnis = wert_von(lambda: lies_eintrag(BEISPIEL, "vpn"))
assert ergebnis == ("kim", "geheim", 400), (
    f"lies_eintrag(tresor, 'vpn') ergibt {ergebnis!r}, erwartet war ('kim', 'geheim', 400).\n"
    "Tipp: bytes.fromhex(text).decode(\"utf-8\") entschlüsselt das Passwort, int(...) den Ablauftag."
)

# lies_eintrag mit einem anderen Eintrag, auch mit Umlauten (nicht fest hinschreiben!)
tresor_test = {"wlan": f"gast;{hexadezimal('Grün-2026!')};12345"}
ergebnis = wert_von(lambda: lies_eintrag(tresor_test, "wlan"))
assert ergebnis == ("gast", "Grün-2026!", 12345), f"lies_eintrag für 'gast;{hexadezimal('Grün-2026!')};12345' ergibt {ergebnis!r}, erwartet war ('gast', 'Grün-2026!', 12345)."

# lies_eintrag: ein fehlender Dienst löst EintragFehlt aus
fehler = ausnahme_von(lambda: lies_eintrag(BEISPIEL, "drucker"))
assert isinstance(fehler, EintragFehlt), (
    f"lies_eintrag(tresor, 'drucker') löst {beschreibe(fehler)} aus, erwartet war EintragFehlt.\n"
    "Tipp: Fangen Sie den KeyError ab und lösen Sie im except-Zweig EintragFehlt aus."
)

# lies_eintrag: EintragFehlt hat den KeyError als __cause__ (raise … from)
assert isinstance(fehler.__cause__, KeyError), (
    f"lies_eintrag(tresor, 'drucker') löst {beschreibe(fehler)} aus; erwartet war der KeyError als __cause__.\n"
    "Tipp: except KeyError as fehler: raise EintragFehlt(...) from fehler"
)

# lies_eintrag: die Meldung nennt den Dienst
assert "drucker" in str(fehler), f"Die Meldung von EintragFehlt ist {str(fehler)!r}; sie soll den Dienst drucker nennen."

# lies_eintrag: zu wenige oder zu viele Felder
fehler_zwei = ausnahme_von(lambda: lies_eintrag({"x": "kim;6162"}, "x"))
fehler_vier = ausnahme_von(lambda: lies_eintrag({"x": "kim;6162;10;extra"}, "x"))
assert isinstance(fehler_zwei, EintragDefekt) and isinstance(fehler_vier, EintragDefekt), (
    f"Bei zwei Feldern löst lies_eintrag {beschreibe(fehler_zwei)} aus, bei vier {beschreibe(fehler_vier)}; erwartet war jeweils EintragDefekt."
)

# lies_eintrag: ein Ablauftag, der keine Zahl ist, mit dem ValueError als Ursache
fehler = ausnahme_von(lambda: lies_eintrag({"x": "kim;6162;morgen"}, "x"))
assert isinstance(fehler, EintragDefekt) and isinstance(fehler.__cause__, ValueError), (
    f"Bei Ablauftag 'morgen' löst lies_eintrag {beschreibe(fehler)} aus, erwartet war EintragDefekt mit dem ValueError von int() als __cause__."
)

# lies_eintrag: ein Passwort, das kein Hexadezimaltext ist
fehler = ausnahme_von(lambda: lies_eintrag(BEISPIEL, "wiki"))
assert isinstance(fehler, EintragDefekt), f"lies_eintrag(tresor, 'wiki') mit Passwortfeld 'zz' löst {beschreibe(fehler)} aus, erwartet war EintragDefekt."

# lies_eintrag: beim unlesbaren Passwort verschwindet die ursprüngliche Ausnahme (raise … from None)
assert fehler.__cause__ is None and fehler.__suppress_context__ is True, (
    f"lies_eintrag(tresor, 'wiki') löst {beschreibe(fehler)} aus; erwartet war kein __cause__ und __suppress_context__=True.\n"
    "Tipp: raise EintragDefekt(...) from None"
)

# lies_eintrag: auch ungültiges UTF-8 ist ein unlesbares Passwort, ohne sichtbare Ursache
geheim = "fe" + hexadezimal("Sommer2026")
fehler = ausnahme_von(lambda: lies_eintrag({"db": f"admin;{geheim};900"}, "db"))
assert isinstance(fehler, EintragDefekt) and fehler.__cause__ is None and fehler.__suppress_context__ is True, (
    f"Bei einem Passwort, das kein gültiges UTF-8 ist, löst lies_eintrag {beschreibe(fehler)} aus, "
    "erwartet war EintragDefekt mit from None.\nTipp: UnicodeDecodeError ist eine Unterart von ValueError."
)

# lies_eintrag: die Meldung verrät nichts aus dem Passwortfeld
assert "db" in str(fehler) and geheim not in str(fehler) and "Sommer" not in str(fehler), (
    f"Die Meldung ist {str(fehler)!r}; sie soll den Dienst db nennen, aber nichts aus dem Passwortfeld."
)

# verbinde_dienst im Beispiel
ergebnis = wert_von(lambda: verbinde_dienst(BEISPIEL, "vpn", 300))
assert ergebnis == ("kim", "geheim"), f"verbinde_dienst(tresor, 'vpn', 300) ergibt {ergebnis!r}, erwartet war ('kim', 'geheim')."

# verbinde_dienst: am letzten gültigen Tag geht es noch
ergebnis = wert_von(lambda: verbinde_dienst(BEISPIEL, "vpn", 400))
assert ergebnis == ("kim", "geheim"), f"verbinde_dienst(tresor, 'vpn', 400) ergibt {ergebnis!r}, erwartet war ('kim', 'geheim'): Tag 400 ist der letzte gültige."

# verbinde_dienst: ein abgelaufenes Passwort
fehler = ausnahme_von(lambda: verbinde_dienst(BEISPIEL, "vpn", 401))
assert isinstance(fehler, DienstNichtVerfuegbar) and isinstance(fehler.__cause__, EintragAbgelaufen), (
    f"verbinde_dienst(tresor, 'vpn', 401) löst {beschreibe(fehler)} aus, erwartet war DienstNichtVerfuegbar mit EintragAbgelaufen als __cause__."
)

# verbinde_dienst: ein fehlender Dienst wird zu DienstNichtVerfuegbar
fehler = ausnahme_von(lambda: verbinde_dienst(BEISPIEL, "drucker", 300))
assert isinstance(fehler, DienstNichtVerfuegbar) and getattr(fehler, "dienst", None) == "drucker", (
    f"verbinde_dienst(tresor, 'drucker', 300) löst {beschreibe(fehler)} aus, erwartet war DienstNichtVerfuegbar('drucker').\n"
    "Tipp: except TresorFehler as fehler: raise DienstNichtVerfuegbar(dienst) from fehler"
)

# verbinde_dienst: die Ursache ist der TresorFehler, dessen Ursache der KeyError
assert isinstance(fehler.__cause__, EintragFehlt) and isinstance(fehler.__cause__.__cause__, KeyError), (
    f"Die Ursache ist {beschreibe(fehler.__cause__)}; erwartet war EintragFehlt mit KeyError als __cause__."
)

# verbinde_dienst: ein defekter Eintrag wird zu DienstNichtVerfuegbar
fehler = ausnahme_von(lambda: verbinde_dienst(BEISPIEL, "wiki", 300))
assert isinstance(fehler, DienstNichtVerfuegbar) and isinstance(fehler.__cause__, EintragDefekt), (
    f"verbinde_dienst(tresor, 'wiki', 300) löst {beschreibe(fehler)} aus, erwartet war DienstNichtVerfuegbar mit EintragDefekt als __cause__."
)

# verbinde_dienst: andere Ausnahmen (hier AttributeError, weil der Eintrag kein Text ist) fliegen unverändert weiter
fehler = ausnahme_von(lambda: verbinde_dienst({"kaputt": 42}, "kaputt", 0))
assert isinstance(fehler, AttributeError), (
    f"verbinde_dienst für einen Eintrag 42 löst {beschreibe(fehler)} aus, erwartet war der AttributeError von split.\n"
    "Tipp: Fangen Sie in verbinde_dienst nur TresorFehler ab, nicht Exception."
)

# fehlerkette mit raise … from
try:
    try:
        {}["x"]
    except KeyError as innen:
        raise EintragFehlt("x") from innen
except EintragFehlt as aussen:
    test_fehler = aussen
ergebnis = wert_von(lambda: fehlerkette(test_fehler))
assert ergebnis == ["EintragFehlt", "KeyError"], f"fehlerkette für EintragFehlt from KeyError ergibt {ergebnis!r}, erwartet war ['EintragFehlt', 'KeyError']."

# fehlerkette: eine einzelne Ausnahme
ergebnis = wert_von(lambda: fehlerkette(ValueError("allein")))
assert ergebnis == ["ValueError"], f"fehlerkette(ValueError('allein')) ergibt {ergebnis!r}, erwartet war ['ValueError']."

# fehlerkette folgt auch __context__, wenn kein from angegeben ist
try:
    try:
        1 / 0
    except ZeroDivisionError:
        raise RuntimeError("beim Aufräumen")
except RuntimeError as aussen:
    test_fehler = aussen
ergebnis = wert_von(lambda: fehlerkette(test_fehler))
assert ergebnis == ["RuntimeError", "ZeroDivisionError"], (
    f"fehlerkette für einen RuntimeError, der in einem except ZeroDivisionError entstand, ergibt {ergebnis!r}, "
    "erwartet war ['RuntimeError', 'ZeroDivisionError'].\nTipp: Ist __cause__ None, folgen Sie __context__."
)

# fehlerkette: nach from None endet die Kette
try:
    try:
        int("x")
    except ValueError:
        raise EintragDefekt("versteckt") from None
except EintragDefekt as aussen:
    test_fehler = aussen
ergebnis = wert_von(lambda: fehlerkette(test_fehler))
assert ergebnis == ["EintragDefekt"], (
    f"fehlerkette für EintragDefekt from None ergibt {ergebnis!r}, erwartet war ['EintragDefekt'].\n"
    "Tipp: Ist __suppress_context__ True, zeigt Python __context__ nicht an."
)

# fehlerkette im Beispiel: alle drei Fälle über verbinde_dienst
ergebnis = [wert_von(lambda: fehlerkette(ausnahme_von(lambda: verbinde_dienst(BEISPIEL, dienst, 300)))) for dienst in ["drucker", "wiki", "mail"]]
erwartet = [["DienstNichtVerfuegbar", "EintragFehlt", "KeyError"], ["DienstNichtVerfuegbar", "EintragDefekt"], ["DienstNichtVerfuegbar", "EintragAbgelaufen"]]
assert ergebnis == erwartet, f"Die Fehlerketten für drucker, wiki und mail sind {ergebnis!r}, erwartet war {erwartet}."

# fehlerkette: eine lange Kette mit __cause__ und __context__ gemischt
try:
    try:
        try:
            [][1]
        except IndexError:
            raise KeyError("b")
    except KeyError as mitte:
        raise TypeError("c") from mitte
except TypeError as aussen:
    test_fehler = aussen
ergebnis = wert_von(lambda: fehlerkette(test_fehler))
assert ergebnis == ["TypeError", "KeyError", "IndexError"], f"fehlerkette ergibt {ergebnis!r}, erwartet war ['TypeError', 'KeyError', 'IndexError']."

# Die Ausgabe des Programms
erwartet = (
    "('kim', 'geheim')\n"
    "Dienst drucker ist nicht verfügbar ['DienstNichtVerfuegbar', 'EintragFehlt', 'KeyError']\n"
    "Dienst wiki ist nicht verfügbar ['DienstNichtVerfuegbar', 'EintragDefekt']\n"
    "Dienst mail ist nicht verfügbar ['DienstNichtVerfuegbar', 'EintragAbgelaufen']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"


def erlaubte_ergebnisse(eintrag, heute):
    """Vergleichslösung: die möglichen Fehlerketten von verbinde_dienst oder das Ergebnis, ohne Ausnahmen gerechnet.

    Bei falscher Felderzahl legt die Aufgabe nicht fest, ob ein ValueError als Ursache dabeisteht.
    """
    if eintrag is None:
        return [["DienstNichtVerfuegbar", "EintragFehlt", "KeyError"]]
    felder = eintrag.split(";")
    if len(felder) != 3:
        return [["DienstNichtVerfuegbar", "EintragDefekt"], ["DienstNichtVerfuegbar", "EintragDefekt", "ValueError"]]
    benutzer, verschluesselt, ablauf = felder
    if not ablauf.lstrip("-").isdigit():
        return [["DienstNichtVerfuegbar", "EintragDefekt", "ValueError"]]
    try:
        passwort = bytes.fromhex(verschluesselt).decode("utf-8")
    except ValueError:
        return [["DienstNichtVerfuegbar", "EintragDefekt"]]
    if int(ablauf) < heute:
        return [["DienstNichtVerfuegbar", "EintragAbgelaufen"]]
    return [(benutzer, passwort)]


# Viele zufällige Tresore
zufall = Zufall(4058)
woerter = ["kim", "ole", "Grün", "Pa$$w0rt", "", "ä", "x y"]
for _ in range(300):
    art = zufall.randint(0, 5)
    passwort = zufall.choice(woerter) + str(zufall.randint(0, 99))
    feld = hexadezimal(passwort) if art != 1 else zufall.choice(["zz", "abc", "ff", "c3", hexadezimal(passwort) + "g"])
    ablauf = str(zufall.randint(0, 100000)) if art != 2 else zufall.choice(["morgen", "1.5", ""])
    felder = [zufall.choice(["kim", "ole", "svc"]), feld, ablauf]
    if art == 3:
        felder = felder[: zufall.randint(1, 2)]
    eintrag = None if art == 4 else ";".join(felder)
    tresor_zufall = {} if eintrag is None else {"dienst": eintrag}
    heute = zufall.randint(0, 100000)
    erlaubt = erlaubte_ergebnisse(eintrag, heute)
    fehler = ausnahme_von(lambda: verbinde_dienst(tresor_zufall, "dienst", heute))
    ergebnis = fehler[1] if isinstance(fehler, tuple) else wert_von(lambda: fehlerkette(fehler))
    assert ergebnis in erlaubt, f"verbinde_dienst({tresor_zufall}, 'dienst', {heute}) ergibt {ergebnis!r}, erwartet war {erlaubt[0]}."

# Obere Grenze: 1000 Einträge
tresor_gross = {f"dienst{n}": f"svc{n};{hexadezimal(f'pw{n}')};{n * 100}" for n in range(1000)}
ergebnis = [wert_von(lambda: verbinde_dienst(tresor_gross, f"dienst{n}", 50000)) for n in range(500, 1000)]
assert ergebnis == [(f"svc{n}", f"pw{n}") for n in range(500, 1000)], "Bei 1000 Einträgen stimmt verbinde_dienst nicht."
