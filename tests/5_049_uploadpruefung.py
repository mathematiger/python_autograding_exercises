# Automatisch erzeugt aus lehrkraft/muster/5_049_uploadpruefung.py - nicht von Hand ändern.
# vorlage-hash: 307b3e562fd9dfe5
# text-hash: 84b0dcc1429a152c
# thema: funktionen
# inhalt: inspect.signature und bind

import functools
import inspect


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text "Typ: Meldung" zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def meldung_bei(aufruf):
    """Gibt (Meldung eines ValueError oder None, Name einer anderen Ausnahme oder None) zurück."""
    try:
        aufruf()
    except ValueError as fehler:
        return str(fehler), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"
    return None, None


def mit_hinweis(funktion):
    """Ein Dekorator wie aus Aufgabe 4_022, der die Regel mit functools.wraps umhüllt."""
    @functools.wraps(funktion)
    def huelle(*args, **kwargs):
        """Ruft die Regel unverändert auf."""
        return funktion(*args, **kwargs)
    return huelle


def mit_standard_none(dateiname, quelle=None):
    """Eine Regel mit dem Standardwert None."""
    return quelle is None or dateiname.endswith(quelle)


def groesse_und_rest(groesse, **rest):
    """Eine Regel mit einem normalen Parameter und **."""
    return groesse > 0


@mit_hinweis
def gekapselt(benutzer, *, gesperrt=("gast",)):
    """Eine dekorierte Regel: Der Benutzer ist nicht gesperrt."""
    return benutzer not in gesperrt


def keine_angaben():
    """Eine Regel ganz ohne Parameter."""
    return True


SIGNATUREN = [b"EICAR", b"X5O!P%"]

# pflichtangaben: ein normaler Parameter
ergebnis = wert_von(lambda: pflichtangaben(nicht_zu_gross))
assert ergebnis == ["groesse"], (
    f"pflichtangaben(nicht_zu_gross) ergibt {ergebnis!r}, erwartet war ['groesse'] (hoechstens hat einen Standardwert).\n"
    "Tipp: Gehen Sie durch inspect.signature(regel).parameters.values()."
)

# pflichtangaben: Nur-Schlüsselwort-Parameter ohne Standardwert gehört dazu
ergebnis = wert_von(lambda: pflichtangaben(virenscan))
assert ergebnis == ["inhalt", "signaturen"], (
    f"pflichtangaben(virenscan) ergibt {ergebnis!r}, erwartet war ['inhalt', 'signaturen']: "
    "virenscan(inhalt, *, signaturen) hat zwei Parameter ohne Standardwert."
)

# pflichtangaben: Parameter mit Standardwert gehören nicht dazu
ergebnis = wert_von(lambda: pflichtangaben(erlaubte_endung))
assert ergebnis == ["dateiname"], (
    f"pflichtangaben(erlaubte_endung) ergibt {ergebnis!r}, erwartet war ['dateiname'].\n"
    "Tipp: parameter.default is inspect.Parameter.empty heißt: kein Standardwert."
)

# pflichtangaben: der Standardwert None ist ein echter Standardwert
ergebnis = wert_von(lambda: pflichtangaben(mit_standard_none))
assert ergebnis == ["dateiname"], (
    f"pflichtangaben für def regel(dateiname, quelle=None) ergibt {ergebnis!r}, erwartet war ['dateiname'].\n"
    "Tipp: Vergleichen Sie parameter.default mit inspect.Parameter.empty, nicht mit None."
)

# pflichtangaben: der Parameter mit ** gehört nicht dazu
ergebnis = wert_von(lambda: (pflichtangaben(alles_ausgefuellt), pflichtangaben(groesse_und_rest)))
assert ergebnis == ([], ["groesse"]), (
    f"pflichtangaben(alles_ausgefuellt) und pflichtangaben für def regel(groesse, **rest) ergeben {ergebnis!r}, "
    "erwartet waren [] und ['groesse'].\nTipp: Überspringen Sie den Parameter, dessen kind inspect.Parameter.VAR_KEYWORD ist."
)

# auswahl aus dem Beispiel
ergebnis = wert_von(lambda: auswahl(erlaubte_endung, ANGABEN))
assert ergebnis == {"dateiname": "bericht.pdf"}, (
    f"auswahl(erlaubte_endung, ANGABEN) ergibt {ergebnis!r}, erwartet war {{'dateiname': 'bericht.pdf'}}.\n"
    "Tipp: Nur Angaben, deren Name in inspect.signature(regel).parameters steht."
)

# auswahl: Parameter mit Standardwert ohne Angabe wird nicht übergeben
ergebnis = wert_von(lambda: auswahl(nicht_zu_gross, ANGABEN))
assert ergebnis == {"groesse": 2_400_000}, (
    f"auswahl(nicht_zu_gross, ANGABEN) ergibt {ergebnis!r}, erwartet war {{'groesse': 2400000}}: "
    "Für hoechstens gibt es keine Angabe, also gilt der Standardwert der Regel."
)

# auswahl: eine Angabe für einen Parameter mit Standardwert wird übergeben
angaben = dict(ANGABEN, hoechstens=1_000_000)
ergebnis = wert_von(lambda: auswahl(nicht_zu_gross, angaben))
assert ergebnis == {"groesse": 2_400_000, "hoechstens": 1_000_000}, (
    f"auswahl(nicht_zu_gross, {angaben!r}) ergibt {ergebnis!r}, erwartet war {{'groesse': 2400000, 'hoechstens': 1000000}}."
)

# auswahl: eine Angabe mit dem Wert None wird übergeben
ergebnis = wert_von(lambda: auswahl(mit_standard_none, {"dateiname": "a.txt", "quelle": None}))
assert ergebnis == {"dateiname": "a.txt", "quelle": None}, (
    f"auswahl für def regel(dateiname, quelle=None) mit {{'dateiname': 'a.txt', 'quelle': None}} ergibt {ergebnis!r}, "
    "erwartet war, dass beide Angaben übergeben werden.\nTipp: Prüfen Sie mit name in angaben, nicht mit angaben.get(name)."
)

# auswahl: eine Regel mit ** bekommt alle Angaben
ergebnis = wert_von(lambda: auswahl(alles_ausgefuellt, ANGABEN))
assert ergebnis == ANGABEN, (
    f"auswahl(alles_ausgefuellt, ANGABEN) ergibt {ergebnis!r}, erwartet waren alle vier Angaben.\n"
    "Tipp: Hat ein Parameter die Art inspect.Parameter.VAR_KEYWORD, bekommt die Regel alles."
)

# auswahl: auch neben einem normalen Parameter bekommt ** alle Angaben
ergebnis = wert_von(lambda: auswahl(groesse_und_rest, ANGABEN))
assert ergebnis == ANGABEN, (
    f"auswahl für def regel(groesse, **rest) mit ANGABEN ergibt {ergebnis!r}, erwartet waren alle vier Angaben."
)

# auswahl: gibt ein neues Dictionary zurück
angaben = dict(ANGABEN)
ergebnis = wert_von(lambda: auswahl(alles_ausgefuellt, angaben))
assert ergebnis is not angaben and angaben == ANGABEN, (
    "auswahl(alles_ausgefuellt, angaben) gibt das Dictionary angaben selbst zurück oder verändert es; "
    "erwartet war ein neues Dictionary.\nTipp: dict(angaben) legt eine Kopie an."
)

# auswahl: fehlende Pflichtangabe löst ValueError aus
meldung, andere = meldung_bei(lambda: auswahl(virenscan, ANGABEN))
assert meldung is not None, (
    "auswahl(virenscan, ANGABEN) muss einen ValueError auslösen, weil die Angabe signaturen fehlt; "
    f"{'stattdessen kam ' + andere if andere else 'es kam keiner'}.\n"
    "Tipp: Prüfen Sie für jede Pflichtangabe, ob sie in angaben steht, bevor Sie die Regel aufrufen."
)

# auswahl: die Meldung nennt Regel und fehlende Angabe
meldung, andere = meldung_bei(lambda: auswahl(virenscan, ANGABEN))
assert meldung is not None and vergleichbar("virenscan") in vergleichbar(meldung) and vergleichbar("signaturen") in vergleichbar(meldung), (
    f"Die Meldung des ValueError bei auswahl(virenscan, ANGABEN) ist {meldung!r}; "
    "sie soll den Namen der Regel (virenscan) und der fehlenden Angabe (signaturen) nennen.\n"
    "Tipp: regel.__name__ ist der Name der Regel."
)

# auswahl: auch ein fehlender normaler Parameter löst ValueError aus
meldung, andere = meldung_bei(lambda: auswahl(groesse_und_rest, {"dateiname": "a.txt"}))
assert meldung is not None and vergleichbar("groesse") in vergleichbar(meldung), (
    f"auswahl für def groesse_und_rest(groesse, **rest) mit {{'dateiname': 'a.txt'}} muss einen ValueError auslösen, der "
    f"'groesse' nennt; Meldung: {meldung!r}" + (f", stattdessen kam {andere}." if andere else ".")
)

# auswahl: eine dekorierte Regel zeigt die Parameter des Originals
ergebnis = wert_von(lambda: auswahl(gekapselt, ANGABEN))
assert ergebnis == {"benutzer": "lena"}, (
    f"auswahl für eine mit functools.wraps dekorierte Regel gekapselt(benutzer, *, gesperrt=...) ergibt {ergebnis!r}, "
    "erwartet war {'benutzer': 'lena'}.\nTipp: inspect.signature folgt __wrapped__ zum Original; "
    "__code__.co_varnames sieht nur die Hülle."
)

# auswahl: eine Regel ohne Parameter bekommt nichts
ergebnis = wert_von(lambda: auswahl(keine_angaben, ANGABEN))
assert ergebnis == {}, f"auswahl für def keine_angaben() ergibt {ergebnis!r}, erwartet war {{}}."

# aufrufwerte aus dem Beispiel: mit Standardwert
ergebnis = wert_von(lambda: aufrufwerte(nicht_zu_gross, ANGABEN))
assert ergebnis == {"groesse": 2_400_000, "hoechstens": 10_000_000}, (
    f"aufrufwerte(nicht_zu_gross, ANGABEN) ergibt {ergebnis!r}, erwartet war {{'groesse': 2400000, 'hoechstens': 10000000}}.\n"
    "Tipp: gebunden = signatur.bind(**auswahl(regel, angaben)), dann gebunden.apply_defaults() und dict(gebunden.arguments)."
)

# aufrufwerte: eine Angabe überschreibt den Standardwert
ergebnis = wert_von(lambda: aufrufwerte(nicht_zu_gross, {"groesse": 5, "hoechstens": 4}))
assert ergebnis == {"groesse": 5, "hoechstens": 4}, (
    f"aufrufwerte(nicht_zu_gross, {{'groesse': 5, 'hoechstens': 4}}) ergibt {ergebnis!r}, erwartet war {{'groesse': 5, 'hoechstens': 4}}."
)

# aufrufwerte: ** bekommt das Dictionary der Angaben
ergebnis = wert_von(lambda: aufrufwerte(alles_ausgefuellt, {"benutzer": "lena"}))
assert ergebnis == {"alles": {"benutzer": "lena"}}, (
    f"aufrufwerte(alles_ausgefuellt, {{'benutzer': 'lena'}}) ergibt {ergebnis!r}, erwartet war {{'alles': {{'benutzer': 'lena'}}}}."
)

# aufrufwerte: ** bekommt nur die übrigen Angaben
ergebnis = wert_von(lambda: aufrufwerte(groesse_und_rest, {"groesse": 7, "benutzer": "lena"}))
assert ergebnis == {"groesse": 7, "rest": {"benutzer": "lena"}}, (
    f"aufrufwerte für def regel(groesse, **rest) mit {{'groesse': 7, 'benutzer': 'lena'}} ergibt {ergebnis!r}, "
    "erwartet war {'groesse': 7, 'rest': {'benutzer': 'lena'}}."
)

# aufrufwerte: ohne übrige Angaben bekommt ** ein leeres Dictionary
ergebnis = wert_von(lambda: aufrufwerte(groesse_und_rest, {"groesse": 7}))
assert ergebnis == {"groesse": 7, "rest": {}}, (
    f"aufrufwerte für def regel(groesse, **rest) mit {{'groesse': 7}} ergibt {ergebnis!r}, erwartet war {{'groesse': 7, 'rest': {{}}}}.\n"
    "Tipp: apply_defaults() setzt für einen Parameter mit ** ein leeres Dictionary ein."
)

# aufrufwerte: dekorierte Regel mit Standardwert
ergebnis = wert_von(lambda: aufrufwerte(gekapselt, ANGABEN))
assert ergebnis == {"benutzer": "lena", "gesperrt": ("gast",)}, (
    f"aufrufwerte für die dekorierte Regel gekapselt(benutzer, *, gesperrt=('gast',)) ergibt {ergebnis!r}, "
    "erwartet war {'benutzer': 'lena', 'gesperrt': ('gast',)}."
)

# aufrufwerte: fehlende Pflichtangabe löst ValueError aus
meldung, andere = meldung_bei(lambda: aufrufwerte(virenscan, ANGABEN))
assert meldung is not None and vergleichbar("signaturen") in vergleichbar(meldung), (
    f"aufrufwerte(virenscan, ANGABEN) muss einen ValueError auslösen, der 'signaturen' nennt; Meldung: {meldung!r}"
    + (f", stattdessen kam {andere}.\nTipp: signatur.bind löst einen TypeError aus; rufen Sie vorher auswahl auf." if andere else ".")
)

# pruefe_upload aus dem Beispiel
ergebnis = wert_von(lambda: pruefe_upload(REGELN, VERDAECHTIG))
assert ergebnis == ["erlaubte_endung", "kein_programm", "virenscan"], (
    f"pruefe_upload(REGELN, VERDAECHTIG) ergibt {ergebnis!r}, erwartet war ['erlaubte_endung', 'kein_programm', 'virenscan'].\n"
    "Tipp: regel(**auswahl(regel, angaben)) und bei False regel.__name__ in die Liste."
)

# pruefe_upload: eine unbedenkliche Datei
angaben = dict(ANGABEN, signaturen=SIGNATUREN)
ergebnis = wert_von(lambda: pruefe_upload(REGELN, angaben))
assert ergebnis == [], f"pruefe_upload(REGELN, ...) für bericht.pdf ohne Auffälligkeiten ergibt {ergebnis!r}, erwartet war []."

# pruefe_upload: eine andere Auswahl an Regeln
angaben = {"dateiname": "foto.png", "groesse": 0, "benutzer": "gast", "inhalt": b""}
ergebnis = wert_von(lambda: pruefe_upload([gekapselt, groesse_und_rest, alles_ausgefuellt, erlaubte_endung, keine_angaben], angaben))
assert ergebnis == ["gekapselt", "groesse_und_rest", "alles_ausgefuellt"], (
    f"pruefe_upload mit den Regeln gekapselt, groesse_und_rest, alles_ausgefuellt, erlaubte_endung, keine_angaben und {angaben!r} "
    f"ergibt {ergebnis!r}, erwartet war ['gekapselt', 'groesse_und_rest', 'alles_ausgefuellt']."
)

# pruefe_upload: keine Regeln
ergebnis = wert_von(lambda: pruefe_upload([], ANGABEN))
assert ergebnis == [], f"pruefe_upload([], ANGABEN) ergibt {ergebnis!r}, erwartet war []."

# pruefe_upload: fehlende Pflichtangabe geht als ValueError weiter
meldung, andere = meldung_bei(lambda: pruefe_upload([erlaubte_endung, virenscan], ANGABEN))
assert meldung is not None, (
    "pruefe_upload([erlaubte_endung, virenscan], ANGABEN) muss einen ValueError auslösen, weil virenscan die Angabe "
    f"signaturen braucht; {'stattdessen kam ' + andere if andere else 'es kam keiner'}."
)

# Die Ausgabe des Programms
erwartet = (
    "['inhalt', 'signaturen']\n{'dateiname': 'bericht.pdf'}\n{'groesse': 2400000, 'hoechstens': 10000000}\n"
    "['erlaubte_endung', 'kein_programm', 'virenscan']"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

NAMEN = ["dateiname", "groesse", "inhalt", "benutzer", "typ", "pfad", "quelle", "zeit", "pruefsumme", "land", "geraet", "sitzung"]


def baue_regel(name, plan, antwort):
    """Baut eine Regel mit der Parameterliste aus plan, die sich jeden Aufruf merkt.

    plan ist eine Liste von (Name, Art, Standardwert oder inspect.Parameter.empty). Die Regel
    nimmt intern alles mit ** an, zeigt nach außen über __signature__ aber genau diese Liste.
    """
    aufrufe = []

    def regel(**erhalten):
        """Merkt sich die benannten Argumente und gibt die feste Antwort zurück."""
        aufrufe.append(erhalten)
        return antwort

    regel.__name__ = name
    regel.__signature__ = inspect.Signature(
        [inspect.Parameter(pname, art, default=standard) for pname, art, standard in plan]
    )
    regel.aufrufe = aufrufe
    return regel


def zufallsplan(zufall):
    """Erzeugt eine zufällige, gültige Parameterliste mit 0 bis 8 Parametern."""
    anzahl = zufall.randint(0, 8)
    mit_rest = anzahl > 0 and zufall.random() < 0.3
    namen = zufall.sample(NAMEN, anzahl - mit_rest)
    normale = zufall.randint(0, len(namen))
    ohne_standard = zufall.randint(0, normale)
    plan = []
    for nummer, pname in enumerate(namen):
        if nummer < normale:
            art = inspect.Parameter.POSITIONAL_OR_KEYWORD
            hat_standard = nummer >= ohne_standard
        else:
            art = inspect.Parameter.KEYWORD_ONLY
            hat_standard = zufall.random() < 0.5
        standard = zufall.choice([0, None, "std", ()]) if hat_standard else inspect.Parameter.empty
        plan.append((pname, art, standard))
    if mit_rest:
        plan.append(("rest", inspect.Parameter.VAR_KEYWORD, inspect.Parameter.empty))
    return plan


def zufallsangaben(zufall, anzahl):
    """Erzeugt zufällige Angaben: einige der NAMEN und weitere Namen, die Werte auch None."""
    namen = zufall.sample(NAMEN, zufall.randint(0, len(NAMEN))) + [f"extra{nummer}" for nummer in range(anzahl)]
    zufall.shuffle(namen)
    return {name: zufall.choice([None, 0, zufall.randint(1, 10**6), name.upper(), b"\x00"]) for name in namen}


def erwartet_fuer(plan, angaben):
    """Vergleichslösung aus dem Plan: (fehlende Angabe oder None, Auswahl, Aufrufwerte)."""
    benannt = [(pname, standard) for pname, art, standard in plan if art != inspect.Parameter.VAR_KEYWORD]
    mit_rest = len(benannt) < len(plan)
    for pname, standard in benannt:
        if standard is inspect.Parameter.empty and pname not in angaben:
            return pname, None, None
    namen = [pname for pname, standard in benannt]
    if mit_rest:
        gewaehlt = dict(angaben)
    else:
        gewaehlt = {name: wert for name, wert in angaben.items() if name in namen}
    werte = {pname: angaben.get(pname, standard) for pname, standard in benannt}
    if mit_rest:
        werte["rest"] = {name: wert for name, wert in angaben.items() if name not in namen}
    return None, gewaehlt, werte


def beschreibe(plan):
    """Schreibt die Parameterliste eines Plans so, wie sie in einem def stünde."""
    return str(inspect.Signature([inspect.Parameter(pname, art, default=standard) for pname, art, standard in plan]))


# Viele zufällige Regeln und Angaben
zufall = Zufall(5049)
fehlerfall = None
for versuch in range(400):
    plan = zufallsplan(zufall)
    angaben = zufallsangaben(zufall, zufall.randint(0, 3))
    regel = baue_regel(f"regel{versuch}", plan, True)
    fehlt, gewaehlt, werte = erwartet_fuer(plan, angaben)
    pflicht = [pname for pname, art, standard in plan if art != inspect.Parameter.VAR_KEYWORD and standard is inspect.Parameter.empty]
    bekommen = (wert_von(lambda: pflichtangaben(regel)), meldung_bei(lambda: auswahl(regel, angaben))[0] is not None)
    if fehlt is None:
        bekommen += (wert_von(lambda: auswahl(regel, angaben)), wert_von(lambda: aufrufwerte(regel, angaben)))
    soll = (pflicht, fehlt is not None) + (() if fehlt is not None else (gewaehlt, werte))
    if bekommen != soll:
        fehlerfall = (beschreibe(plan), angaben, soll, bekommen)
        break
assert fehlerfall is None, (
    f"Für die Regel regel{fehlerfall[0]} und angaben = {fehlerfall[1]!r}:\n"
    f"  erwartet (pflichtangaben, ValueError bei auswahl, auswahl, aufrufwerte) = {fehlerfall[2]!r}\n"
    f"  bekommen                                                              {fehlerfall[3]!r}"
)

# Obere Grenze: 200 Regeln, 50 Angaben
zufall = Zufall(50490)
angaben = zufallsangaben(zufall, 50 - len(NAMEN))
angaben.update({name: zufall.randint(1, 9) for name in NAMEN[:6]})
regeln = []
plaene = []
antworten = []
for nummer in range(200):
    plan = zufallsplan(zufall)
    while erwartet_fuer(plan, angaben)[0] is not None:
        plan = zufallsplan(zufall)
    plaene.append(plan)
    antworten.append(zufall.random() < 0.5)
    regeln.append(baue_regel(f"regel{nummer}", plan, antworten[-1]))
ergebnis = wert_von(lambda: pruefe_upload(regeln, angaben))
erwartet = [regel.__name__ for regel, antwort in zip(regeln, antworten) if not antwort]
assert ergebnis == erwartet, (
    f"pruefe_upload mit 200 Regeln und {len(angaben)} Angaben ergibt {str(ergebnis)[:200]}, erwartet war {str(erwartet)[:200]}."
)

# Obere Grenze: jede Regel wurde genau einmal mit ihrer Auswahl aufgerufen
falsch = None
for regel, plan in zip(regeln, plaene):
    gewaehlt = erwartet_fuer(plan, angaben)[1]
    if regel.aufrufe != [gewaehlt]:
        falsch = (regel.__name__, beschreibe(plan), gewaehlt, regel.aufrufe)
        break
assert falsch is None, (
    f"pruefe_upload mit 200 Regeln: {falsch[0]}{falsch[1]} sollte genau einmal mit {falsch[2]!r} aufgerufen werden, "
    f"die Aufrufe waren {falsch[3]!r}."
)
