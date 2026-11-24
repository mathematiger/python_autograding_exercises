# Automatisch erzeugt aus lehrkraft/muster/5_050_typwaechter.py - nicht von Hand ändern.
# vorlage-hash: c9c35dc4f4dbfbcf
# text-hash: e301a3483e6aadf3
# thema: funktionen
# inhalt: Argumente nach Annotationen prüfen

class Messreihe(list):
    """Eine Liste von Messwerten, als Beispiel für eine Unterklasse."""

    def __repr__(self):
        """Zeigt die Klasse mit an, damit man sie von einer Liste unterscheidet."""
        return f"Messreihe({list(self)!r})"


def wert_von(aufruf):
    """Führt den Aufruf aus; liefert ("ok", Ergebnis) oder (Name der Ausnahme, Meldung)."""
    try:
        return "ok", aufruf()
    except Exception as fehler:
        return type(fehler).__name__, str(fehler)


def fehlende_teile(meldung, teile):
    """Liefert die Teile, die in der Meldung nicht vorkommen (locker verglichen)."""
    return [teil for teil in teile if vergleichbar(teil) not in vergleichbar(str(meldung))]


def dekoriere(funktion):
    """Dekoriert funktion; liefert (dekorierte Funktion oder None, Fehlertext oder None)."""
    try:
        return typgeprueft(funktion), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


AUFRUFE = []


def lerne(gewicht: float, k: int, name: str = "modell", notiz=None) -> float:
    """Testfunktion: merkt sich den Aufruf und gibt gewicht zurück."""
    AUFRUFE.append((gewicht, k, name, notiz))
    return gewicht


# passt: das Beispiel aus dem Aufgabentext
assert passt(3, int) is True and passt("3", int) is False, (
    f"passt(3, int) ergibt {passt(3, int)!r}, passt('3', int) ergibt {passt('3', int)!r}; erwartet waren True und False.\n"
    "Tipp: Grundsätzlich gilt isinstance(wert, typ)."
)

# passt: Texte, Listen und Dictionaries
ergebnis = [passt("a", str), passt([1], list), passt({}, dict), passt([1], str), passt("a", list), passt((1,), list)]
assert ergebnis == [True, True, True, False, False, False], (
    "passt('a', str), passt([1], list), passt({}, dict), passt([1], str), passt('a', list), passt((1,), list) "
    f"ergeben {ergebnis}, erwartet waren [True, True, True, False, False, False]."
)

# passt: True und False passen zu bool, aber nicht zu int
ergebnis = [passt(True, bool), passt(False, bool), passt(True, int), passt(False, int), passt(1, bool)]
assert ergebnis == [True, True, False, False, False], (
    "passt(True, bool), passt(False, bool), passt(True, int), passt(False, int), passt(1, bool) "
    f"ergeben {ergebnis}, erwartet waren [True, True, False, False, False].\n"
    "Tipp: bool ist eine Unterklasse von int, darum ist isinstance(True, int) True; das müssen Sie ausschließen."
)

# passt: eine ganze Zahl passt auch zu float, eine Kommazahl nicht zu int
ergebnis = [passt(2, float), passt(2.5, float), passt(2.5, int), passt("2.5", float)]
assert ergebnis == [True, True, False, False], (
    f"passt(2, float), passt(2.5, float), passt(2.5, int), passt('2.5', float) ergeben {ergebnis}, "
    "erwartet waren [True, True, False, False].\nTipp: isinstance(2, float) ist False; diesen Fall müssen Sie zulassen."
)

# passt: True und False passen auch nicht zu float
ergebnis = [passt(True, float), passt(False, float)]
assert ergebnis == [False, False], f"passt(True, float) und passt(False, float) ergeben {ergebnis}, erwartet war beide Male False."

# passt: zur Annotation None passt nur None
ergebnis = [wert_von(lambda: passt(None, None)), wert_von(lambda: passt(0, None)), wert_von(lambda: passt("", None))]
assert ergebnis == [("ok", True), ("ok", False), ("ok", False)], (
    f"passt(None, None), passt(0, None), passt('', None) ergeben {ergebnis}, erwartet waren True, False, False.\n"
    "Tipp: isinstance(wert, None) geht nicht; prüfen Sie typ is None vorher."
)

# passt: eigene Klassen und Unterklassen
ergebnis = [passt(Messreihe([1.5]), Messreihe), passt(Messreihe(), list), passt([1.5], Messreihe), passt(None, int)]
assert ergebnis == [True, True, False, False], (
    "Mit class Messreihe(list): passt(Messreihe([1.5]), Messreihe), passt(Messreihe(), list), passt([1.5], Messreihe), "
    f"passt(None, int) ergeben {ergebnis}, erwartet waren [True, True, False, False]."
)

# lernschritt: das Beispiel mit passenden Typen
ergebnis = wert_von(lambda: lernschritt(0.5, 2.0, lernrate=0.1))
assert ergebnis[0] == "ok" and abs(ergebnis[1] - 0.3) < 1e-9, (
    f"lernschritt(0.5, 2.0, lernrate=0.1) ergibt {ergebnis}, erwartet war 0.3.\n"
    "Tipp: Die Hülle muss die Funktion aufrufen und ihr Ergebnis zurückgeben."
)

# lernschritt: ganze Zahlen gelten als float
ergebnis = wert_von(lambda: lernschritt(1, 2))
assert ergebnis[0] == "ok" and abs(ergebnis[1] - 0.8) < 1e-9, (
    f"lernschritt(1, 2) ergibt {ergebnis}, erwartet war 0.8: Eine ganze Zahl passt auch zu float."
)

# Ein Text für lernrate wird mit TypeError abgewiesen
ergebnis = wert_von(lambda: lernschritt(0.5, 2.0, lernrate="0.1"))
assert ergebnis[0] == "TypeError", (
    f"lernschritt(0.5, 2.0, lernrate='0.1') ergibt {ergebnis}, erwartet war ein TypeError.\n"
    "Tipp: In der Hülle gebunden = signatur.bind(*args, **kwargs), dann jeden Wert mit passt gegen die Annotation prüfen."
)

# Die Meldung nennt Funktion und Parameter
fehlt = fehlende_teile(ergebnis[1], ["lernschritt", "lernrate"])
assert ergebnis[0] == "TypeError" and not fehlt, (
    f"Die Meldung zu lernschritt(0.5, 2.0, lernrate='0.1') lautet {ergebnis[1]!r}; darin fehlt {fehlt}.\n"
    "Tipp: funktion.__name__ und den Namen des Parameters in die Meldung schreiben."
)

# Die Meldung nennt den erwarteten und den erhaltenen Typ
fehlt = fehlende_teile(ergebnis[1], ["float", "str"])
assert ergebnis[0] == "TypeError" and not fehlt, (
    f"Die Meldung zu lernschritt(0.5, 2.0, lernrate='0.1') lautet {ergebnis[1]!r}; darin fehlt {fehlt}.\n"
    "Tipp: annotation.__name__ und type(wert).__name__."
)

# Bei einem falschen Typ wird die Funktion gar nicht aufgerufen
AUFRUFE.clear()
gelernt, fehler = dekoriere(lerne)
ergebnis = wert_von(lambda: gelernt("0.5", 3))
assert fehler is None and ergebnis[0] == "TypeError" and AUFRUFE == [], (
    f"lerne('0.5', 3) mit gewicht: float ergibt {ergebnis} und hat lerne {len(AUFRUFE)}-mal aufgerufen; "
    "erwartet war ein TypeError, ohne lerne aufzurufen.\nTipp: Erst alles prüfen, dann funktion(*args, **kwargs)."
)

# Mit passenden Typen kommen alle Argumente an
AUFRUFE.clear()
ergebnis = wert_von(lambda: gelernt(0.5, 3, name="knn", notiz=[1]))
assert ergebnis == ("ok", 0.5) and AUFRUFE == [(0.5, 3, "knn", [1])], (
    f"lerne(0.5, 3, name='knn', notiz=[1]) ergibt {ergebnis}, lerne bekam {AUFRUFE}; "
    "erwartet waren ('ok', 0.5) und [(0.5, 3, 'knn', [1])]."
)

# Auch Schlüsselwortargumente werden geprüft
ergebnis = wert_von(lambda: gelernt(0.5, k=3, name=7))
fehlt = fehlende_teile(ergebnis[1], ["lerne", "name", "str", "int"])
assert ergebnis[0] == "TypeError" and not fehlt, (
    f"lerne(0.5, k=3, name=7) mit name: str ergibt {ergebnis}; erwartet war ein TypeError, der lerne, name, str und int nennt"
    + (f", darin fehlt {fehlt}." if ergebnis[0] == "TypeError" else ".")
    + "\nTipp: signatur.bind ordnet auch Schlüsselwortargumente ihrem Parameter zu."
)

# True passt nicht zu int
ergebnis = wert_von(lambda: gelernt(0.5, True))
fehlt = fehlende_teile(ergebnis[1], ["k", "int", "bool"])
assert ergebnis[0] == "TypeError" and not fehlt, (
    f"lerne(0.5, True) mit k: int ergibt {ergebnis}; erwartet war ein TypeError, der k, int und bool nennt"
    + (f", darin fehlt {fehlt}." if ergebnis[0] == "TypeError" else ".")
)

# Parameter ohne Annotation werden nicht geprüft
AUFRUFE.clear()
ergebnis = wert_von(lambda: gelernt(0.5, 3, "knn", {"egal": object()}))
assert ergebnis == ("ok", 0.5) and len(AUFRUFE) == 1, (
    f"lerne(0.5, 3, 'knn', {{'egal': ...}}) ergibt {ergebnis}; notiz hat keine Annotation, erwartet war ('ok', 0.5).\n"
    "Tipp: Ist parameter.annotation inspect.Parameter.empty, überspringen Sie den Parameter."
)

# Mehrere falsche Argumente: gemeldet wird das erste in der Reihenfolge der Signatur
ergebnis = wert_von(lambda: gelernt(name=1, k="drei", gewicht=0.5))
assert ergebnis[0] == "TypeError" and not fehlende_teile(ergebnis[1], ["k", "int", "str"]) and vergleichbar("name") not in vergleichbar(ergebnis[1]), (
    f"lerne(name=1, k='drei', gewicht=0.5) ergibt {ergebnis}; erwartet war ein TypeError zu k (erwartet int, bekommen str), "
    "nicht zu name, weil k in der Signatur vor name steht.\n"
    "Tipp: Gehen Sie gebunden.arguments durch; es steht in der Reihenfolge der Signatur, nicht der des Aufrufs."
)

# Standardwerte werden mitgeprüft
def mit_falschem_standard(anzahl: int = "fünf"):
    """Testfunktion mit einem Standardwert, der nicht zur Annotation passt."""
    return anzahl


geprueft, fehler = dekoriere(mit_falschem_standard)
ergebnis = [wert_von(lambda: geprueft()), wert_von(lambda: geprueft(5))]
assert ergebnis[0][0] == "TypeError" and ergebnis[1] == ("ok", 5), (
    f"Für def f(anzahl: int = 'fünf') ergeben f() und f(5) {ergebnis}; erwartet waren ein TypeError und ('ok', 5).\n"
    "Tipp: gebunden.apply_defaults() ergänzt die Standardwerte vor der Prüfung."
)

# Passen die Argumente nicht zur Signatur, kommt der TypeError von Python
AUFRUFE.clear()
ergebnis = [wert_von(lambda: gelernt(0.5)), wert_von(lambda: gelernt(0.5, 3, "a", None, 9))]
assert fehler is None and [art for art, meldung in ergebnis] == ["TypeError", "TypeError"] and AUFRUFE == [], (
    f"lerne(0.5) (k fehlt) und lerne(0.5, 3, 'a', None, 9) (eines zu viel) ergeben {ergebnis}, lerne wurde {len(AUFRUFE)}-mal aufgerufen; "
    "erwartet war beide Male ein TypeError ohne Aufruf.\nTipp: signatur.bind löst ihn selbst aus."
)

# Der Rückgabewert wird geprüft
def liefert_tupel(werte: list) -> list:
    """Testfunktion, die entgegen ihrer Annotation ein Tupel liefert."""
    return tuple(werte)


geprueft, fehler = dekoriere(liefert_tupel)
ergebnis = wert_von(lambda: geprueft([1, 2]))
fehlt = fehlende_teile(ergebnis[1], ["liefert_tupel", "list", "tuple"])
assert ergebnis[0] == "TypeError" and not fehlt, (
    f"Für def liefert_tupel(werte: list) -> list, die ein Tupel liefert, ergibt liefert_tupel([1, 2]) {ergebnis}; "
    "erwartet war ein TypeError, der liefert_tupel, list und tuple nennt"
    + (f", darin fehlt {fehlt}." if ergebnis[0] == "TypeError" else ".")
    + "\nTipp: signatur.return_annotation nach dem Aufruf mit passt prüfen."
)

# Rückgabe -> None: nur None ist erlaubt
def liefert(wert) -> None:
    """Testfunktion mit -> None, die wert zurückgibt."""
    return wert


geprueft, fehler = dekoriere(liefert)
ergebnis = [wert_von(lambda: geprueft(None)), wert_von(lambda: geprueft(0))]
assert ergebnis[0] == ("ok", None) and ergebnis[1][0] == "TypeError" and not fehlende_teile(ergebnis[1][1], ["None", "int"]), (
    f"Für def liefert(wert) -> None ergeben liefert(None) und liefert(0) {ergebnis if fehler is None else fehler}; "
    "erwartet waren ('ok', None) und ein TypeError, der None und int nennt.\n"
    "Tipp: Die Annotation None ist erlaubt; ihr Name in der Meldung ist einfach 'None'."
)

# Ohne Rückgabe-Annotation wird das Ergebnis nicht geprüft
def ohne_annotation(wert):
    """Testfunktion ohne Annotationen."""
    return wert


geprueft, fehler = dekoriere(ohne_annotation)
ergebnis = [wert_von(lambda: geprueft("x")), wert_von(lambda: geprueft(None))]
assert ergebnis == [("ok", "x"), ("ok", None)], (
    f"Eine Funktion ganz ohne Annotationen ergibt dekoriert {ergebnis if fehler is None else fehler}; "
    "erwartet waren [('ok', 'x'), ('ok', None)].\nTipp: Fehlt die Annotation, ist return_annotation inspect.Signature.empty."
)

# *werte: float prüft jedes einzelne Argument
def mittelwert(*werte: float) -> float:
    """Testfunktion: Mittelwert beliebig vieler Werte."""
    return sum(werte) / len(werte)


geprueft, fehler = dekoriere(mittelwert)
ergebnis = [wert_von(lambda: geprueft(1, 2.5, 3)), wert_von(lambda: geprueft(1.0, "2", 3.0))]
assert ergebnis[0][0] == "ok" and abs(ergebnis[0][1] - 6.5 / 3) < 1e-9 and ergebnis[1][0] == "TypeError" and not fehlende_teile(ergebnis[1][1], ["werte", "str"]), (
    f"Für def mittelwert(*werte: float) ergeben mittelwert(1, 2.5, 3) und mittelwert(1.0, '2', 3.0) "
    f"{ergebnis if fehler is None else fehler}; erwartet waren etwa 2.1667 und ein TypeError, der werte und str nennt.\n"
    "Tipp: Bei parameter.kind == inspect.Parameter.VAR_POSITIONAL steht in arguments ein Tupel; prüfen Sie jedes Element."
)

# **optionen: int prüft jeden Wert
def einstellungen(**optionen: int) -> dict:
    """Testfunktion: gibt die Optionen zurück."""
    return optionen


geprueft, fehler = dekoriere(einstellungen)
ergebnis = [wert_von(lambda: geprueft(epochen=10, stapel=32)), wert_von(lambda: geprueft(epochen=10, stapel=32.0)), wert_von(lambda: geprueft())]
assert ergebnis[0] == ("ok", {"epochen": 10, "stapel": 32}) and ergebnis[1][0] == "TypeError" and ergebnis[2] == ("ok", {}), (
    f"Für def einstellungen(**optionen: int) ergeben einstellungen(epochen=10, stapel=32), einstellungen(epochen=10, stapel=32.0) "
    f"und einstellungen() {ergebnis if fehler is None else fehler}; erwartet waren das Dictionary, ein TypeError und {{}}.\n"
    "Tipp: Bei VAR_KEYWORD steht in arguments ein Dictionary; prüfen Sie jeden Wert, nicht die Schlüssel."
)

# Nicht unterstützte Annotationen lösen schon beim Dekorieren einen TypeError aus
def schwelle(wert: list[float]):
    """Testfunktion mit einer verschachtelten Annotation."""
    return wert


geprueft, fehler = dekoriere(schwelle)
assert fehler is not None and fehler.startswith("TypeError") and not fehlende_teile(fehler, ["schwelle", "wert"]), (
    f"Das Dekorieren von def schwelle(wert: list[float]) ergibt {fehler or 'keinen Fehler'}; "
    "erwartet war ein TypeError, der schwelle und wert nennt.\n"
    "Tipp: isinstance(annotation, type) ist für list[float] False; prüfen Sie das gleich beim Dekorieren, nicht erst in der Hülle."
)

# Auch int | None, ein Text und eine solche Rückgabe-Annotation werden abgelehnt
def vielleicht(wert: int | None):
    """Testfunktion mit int | None."""


def als_text(wert: "int"):
    """Testfunktion mit einer Annotation als Text."""


def rueckgabe_verschachtelt(wert: int) -> list[int]:
    """Testfunktion mit verschachtelter Rückgabe-Annotation."""


ergebnis = [dekoriere(funktion)[1] or "kein Fehler" for funktion in [vielleicht, als_text, rueckgabe_verschachtelt]]
assert all(fehler.startswith("TypeError") for fehler in ergebnis), (
    f"Das Dekorieren von wert: int | None, wert: 'int' und -> list[int] ergibt {ergebnis}; erwartet war jedes Mal ein TypeError.\n"
    "Tipp: Erlaubt sind nur Klassen (isinstance(annotation, type)), None und inspect.Parameter.empty; "
    "prüfen Sie auch signatur.return_annotation."
)

# Name, Docstring und Signatur bleiben erhalten
merkmale = (lernschritt.__name__, lernschritt.__doc__, str(inspect.signature(lernschritt)))
erwartet = ("lernschritt", "Ein Schritt des Gradientenverfahrens: das Gewicht ein Stück gegen den Gradienten verschieben.",
            "(gewicht: float, gradient: float, lernrate: float = 0.1) -> float")
assert merkmale == erwartet, (
    f"Die dekorierte lernschritt hat Name, Docstring und Signatur {merkmale}, erwartet war {erwartet}.\n"
    "Tipp: @functools.wraps(funktion) über die Hülle."
)

# Die Signatur wird einmal beim Dekorieren berechnet, nicht bei jedem Aufruf
def zaehle_signaturen():
    """Zählt Aufrufe von inspect.signature beim Dekorieren und bei 50 Aufrufen; liefert die beiden Zahlen."""
    original = inspect.signature
    zaehler = [0]

    def gezaehlt(*args, **kwargs):
        """Zählt mit und ruft das echte inspect.signature auf."""
        zaehler[0] += 1
        return original(*args, **kwargs)

    inspect.signature = gezaehlt
    try:
        geprueft = typgeprueft(lerne)
        beim_dekorieren = zaehler[0]
        for nummer in range(50):
            geprueft(0.5, nummer)
        return beim_dekorieren, zaehler[0] - beim_dekorieren
    finally:
        inspect.signature = original


beim_dekorieren, bei_aufrufen = zaehle_signaturen()
assert beim_dekorieren >= 1 and bei_aufrufen == 0, (
    f"inspect.signature lief beim Dekorieren {beim_dekorieren}-mal und bei 50 Aufrufen {bei_aufrufen}-mal; "
    "erwartet war mindestens einmal beim Dekorieren und kein einziges Mal bei den Aufrufen.\n"
    "Tipp: signatur = inspect.signature(funktion) außerhalb der Hülle; die Hülle benutzt die Variable als Closure."
)

# Die vorgegebenen Funktionen: normalisiere und stichprobe
ergebnis = [wert_von(lambda: normalisiere([2, 4, 6])), wert_von(lambda: stichprobe([4, 8, 15], 2)),
            wert_von(lambda: normalisiere("2,4,6"))[0], wert_von(lambda: stichprobe([4, 8, 15], True))[0]]
assert ergebnis == [("ok", [0.0, 0.5, 1.0]), ("ok", random.Random(0).sample([4, 8, 15], 2)), "TypeError", "TypeError"], (
    f"normalisiere([2, 4, 6]), stichprobe([4, 8, 15], 2), normalisiere('2,4,6'), stichprobe([4, 8, 15], True) ergeben {ergebnis}; "
    "erwartet waren zwei Ergebnisse und zwei TypeError."
)

# Die Ausgabe des Programms
zeilen = AUSGABE.strip().splitlines()
assert len(zeilen) == 3 and vergleichbar(zeilen[0]) == vergleichbar("[0.0, 0.5, 1.0]") and vergleichbar(zeilen[1]) == vergleichbar("0.3") and not fehlende_teile(zeilen[2], ["lernschritt", "lernrate", "float", "str"]), (
    f"Erwartete Ausgabe: [0.0, 0.5, 1.0], dann 0.3, dann Ihre Meldung zu lernrate='0.1' – Ihr Programm:\n{AUSGABE}"
)


# Vergleichslösung und Bausteine für die Zufallstests
TYPEN = [int, float, str, bool, list, dict, tuple, Messreihe, None, inspect.Parameter.empty, inspect.Parameter.empty]
ARTEN = [inspect.Parameter.POSITIONAL_OR_KEYWORD] * 4 + [inspect.Parameter.KEYWORD_ONLY]


def zufallswert(zufall):
    """Ein zufälliger Wert eines der Typen aus TYPEN."""
    return zufall.choice([
        zufall.randint(-5, 5), zufall.uniform(-1, 1), zufall.choice(["", "0.1", "k"]), zufall.choice([True, False]),
        [zufall.random()], {"a": 1}, (1, 2), Messreihe([0.5]), None,
    ])


def vergleich_passt(wert, typ):
    """Langsame, andere Fassung von passt für die Zufallstests."""
    if typ is None:
        return wert is None
    if type(wert) is bool:
        return typ is bool
    if typ is float:
        return type(wert) in (int, float)
    return isinstance(wert, typ)


def typname(typ):
    """Name der Klasse oder "None"."""
    return "None" if typ is None else typ.__name__


def baue_funktion(zufall, nummer, anzahl_parameter):
    """Baut eine Funktion mit zufälliger Signatur; sie gibt ihren Rückgabewert aus der Liste RUECKGABE zurück."""
    parameter = []
    standard_erlaubt = False
    for stelle in range(anzahl_parameter):
        art = zufall.choice(ARTEN)
        if parameter and parameter[-1].kind is inspect.Parameter.KEYWORD_ONLY:
            art = inspect.Parameter.KEYWORD_ONLY
        mit_standard = zufall.random() < 0.4 or (standard_erlaubt and art is inspect.Parameter.POSITIONAL_OR_KEYWORD)
        standard_erlaubt = standard_erlaubt or mit_standard
        standard = zufallswert(zufall) if mit_standard else inspect.Parameter.empty
        parameter.append(inspect.Parameter(f"merkmal_{stelle:03d}", art, default=standard, annotation=zufall.choice(TYPEN)))
    if zufall.random() < 0.3 and all(p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD for p in parameter):
        parameter.append(inspect.Parameter("weitere", inspect.Parameter.VAR_POSITIONAL, annotation=zufall.choice(TYPEN)))
    if zufall.random() < 0.3:
        parameter.append(inspect.Parameter("optionen", inspect.Parameter.VAR_KEYWORD, annotation=zufall.choice(TYPEN)))
    aufrufe = []

    def schritt(*args, **kwargs):
        """Merkt sich den Aufruf und gibt den vorbereiteten Rückgabewert zurück."""
        aufrufe.append((args, kwargs))
        return RUECKGABE[0]

    schritt.__name__ = f"schritt_{nummer:04d}"
    schritt.__signature__ = inspect.Signature(parameter, return_annotation=zufall.choice(TYPEN))
    return schritt, aufrufe


RUECKGABE = [None]


def zufallsaufruf(zufall, signatur):
    """Ein zufälliger, zur Signatur passender Aufruf: (args, kwargs, Wert je Parametername)."""
    args, kwargs, werte = [], {}, {}
    positionell = True
    for p in signatur.parameters.values():
        if p.kind is inspect.Parameter.VAR_POSITIONAL:
            extra = [zufallswert(zufall) for _ in range(zufall.randint(0, 3))] if positionell else []
            args.extend(extra)
            werte[p.name] = extra
        elif p.kind is inspect.Parameter.VAR_KEYWORD:
            extra = {f"zusatz_{stelle}": zufallswert(zufall) for stelle in range(zufall.randint(0, 3))}
            kwargs.update(extra)
            werte[p.name] = list(extra.values())
        elif p.default is not inspect.Parameter.empty and zufall.random() < 0.3:
            werte[p.name] = [p.default]
            positionell = False
        else:
            wert = zufallswert(zufall)
            werte[p.name] = [wert]
            if positionell and p.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD and zufall.random() < 0.7:
                args.append(wert)
            else:
                kwargs[p.name] = wert
                positionell = False
    return args, kwargs, werte


def erwarteter_fehler(signatur, werte, rueckgabe):
    """Vergleichslösung: (Name, erwartet, bekommen) des ersten Verstoßes oder None."""
    for p in signatur.parameters.values():
        if p.annotation is inspect.Parameter.empty:
            continue
        for wert in werte[p.name]:
            if not vergleich_passt(wert, p.annotation):
                return p.name, typname(p.annotation), type(wert).__name__
    ziel = signatur.return_annotation
    if ziel is not inspect.Signature.empty and not vergleich_passt(rueckgabe, ziel):
        return None, typname(ziel), type(rueckgabe).__name__
    return None


def pruefe_zufaellig(zufall, nummer, anzahl_parameter, anzahl_aufrufe):
    """Dekoriert eine zufällige Funktion und ruft sie oft auf; liefert die erste Abweichung als Text oder None."""
    original, aufrufe = baue_funktion(zufall, nummer, anzahl_parameter)
    signatur = inspect.signature(original)
    geprueft, fehler = dekoriere(original)
    if fehler is not None:
        return f"Das Dekorieren von {original.__name__}{signatur} ergibt {fehler}, erwartet war kein Fehler."
    for _ in range(anzahl_aufrufe):
        args, kwargs, werte = zufallsaufruf(zufall, signatur)
        RUECKGABE[0] = zufallswert(zufall)
        aufrufe.clear()
        verstoss = erwarteter_fehler(signatur, werte, RUECKGABE[0])
        ergebnis = wert_von(lambda: geprueft(*args, **kwargs))
        aufruf = f"{original.__name__}(*{args!r}, **{kwargs!r}) mit der Signatur {signatur}, Rückgabe {RUECKGABE[0]!r}"
        if verstoss is None and ergebnis != ("ok", RUECKGABE[0]):
            return f"{aufruf}\nergibt {ergebnis}, erwartet war ('ok', {RUECKGABE[0]!r})."
        if verstoss is None:
            continue
        name, erwartet, bekommen = verstoss
        teile = [original.__name__, erwartet, bekommen] + ([name] if name else [])
        if ergebnis[0] != "TypeError" or fehlende_teile(ergebnis[1], teile):
            return (
                f"{aufruf}\nergibt {ergebnis}, erwartet war ein TypeError, der {teile} nennt.\n"
                "(Nicht übergebene Parameter haben ihren Standardwert; gemeldet wird der erste unpassende in der Reihenfolge der Signatur.)"
            )
        if name is not None and aufrufe:
            return f"{aufruf}\nhat die Funktion trotz des falschen Arguments {name} aufgerufen."
    return None


# Viele zufällige Funktionen und Aufrufe gegen eine Vergleichslösung
zufall = Zufall(5050)
abweichung = None
for nummer in range(300):
    abweichung = pruefe_zufaellig(zufall, nummer, zufall.randint(0, 6), 15)
    if abweichung:
        break
assert abweichung is None, abweichung

# Obere Grenze: 100 Parameter und viele Aufrufe
zufall = Zufall(50500)
abweichung = pruefe_zufaellig(zufall, 9999, 100, 500)
assert abweichung is None, f"Bei 100 Parametern: {abweichung[:1500]}"
