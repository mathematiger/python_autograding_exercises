# Automatisch erzeugt aus lehrkraft/muster/3_017_lastspitzen.py - nicht von Hand ändern.
# vorlage-hash: f80de5b3f519475a
# text-hash: 416537ad48c32538
# thema: kontrollfluss
# inhalt: List Comprehension

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt zurück, ob die Funktion eine List Comprehension und ob sie eine for-/while-Anweisung oder append enthält."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False, False
    mit_comprehension = False
    mit_schleife = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ListComp):
            mit_comprehension = True
        if isinstance(knoten, (ast.For, ast.While)):
            mit_schleife = True
        if isinstance(knoten, ast.Attribute) and knoten.attr == "append":
            mit_schleife = True
    return mit_comprehension, mit_schleife


def vergleichbare_texte(werte):
    """Macht die Texte einer Liste mit vergleichbar unempfindlich gegen Leerzeichen und Schreibweise; Zahlen bleiben."""
    if not isinstance(werte, list):
        return werte
    return [vergleichbar(wert) if isinstance(wert, str) else wert for wert in werte]


messungen = [(480, 35), (481, 97), (482, 88), (483, 40)]

# freie_kapazitaet aus dem Beispiel
ergebnis = freie_kapazitaet(messungen)
assert ergebnis == [65, 3, 12, 60], (
    f"freie_kapazitaet(messungen) ergibt {ergebnis!r}, erwartet war [65, 3, 12, 60].\n"
    "Tipp: Vorn in der Comprehension steht, was in die neue Liste kommt: 100 - prozent."
)

# spitzen aus dem Beispiel
ergebnis = spitzen(messungen, 85)
assert ergebnis == [481, 482], (
    f"spitzen(messungen, 85) ergibt {ergebnis!r}, erwartet war [481, 482].\n"
    "Tipp: In die Liste kommen die Minuten, nicht die Prozentwerte oder die ganzen Tupel."
)

# meldungen aus dem Beispiel
ergebnis = meldungen(messungen, 90)
assert vergleichbare_texte(ergebnis) == vergleichbare_texte(["Minute 481: 97 %"]), (
    f'meldungen(messungen, 90) ergibt {ergebnis!r}, erwartet war ["Minute 481: 97 %"].\n'
    'Tipp: Ein f-String wie f"Minute {minute}: {prozent} %" baut den Text.'
)

# Andere Schwellen (nicht fest hinschreiben!)
for schwelle, erwartet in [(30, [480, 481, 482, 483]), (90, [481]), (97, []), (39, [481, 482, 483])]:
    ergebnis = spitzen(messungen, schwelle)
    assert ergebnis == erwartet, f"spitzen(messungen, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet}."

TIPP_SCHWELLE = "Tipp: „größer als schwelle“ heißt prozent > schwelle, genau 50 zählt nicht."

# Genau die Schwelle zählt nicht als Spitze: spitzen
grenzfall = [(0, 50), (1, 51), (2, 49)]
ergebnis = spitzen(grenzfall, 50)
assert ergebnis == [1], f"Bei {grenzfall} und schwelle 50 ergibt spitzen {ergebnis!r}, erwartet war [1].\n{TIPP_SCHWELLE}"

# Genau die Schwelle zählt nicht als Spitze: meldungen
ergebnis_text = meldungen(grenzfall, 50)
assert vergleichbare_texte(ergebnis_text) == vergleichbare_texte(["Minute 1: 51 %"]), (
    f'Bei {grenzfall} und schwelle 50 ergibt meldungen {ergebnis_text!r}, erwartet war ["Minute 1: 51 %"].\n{TIPP_SCHWELLE}'
)

# Ränder (0 und 100 Prozent, Minute 0 und 10**6): freie_kapazitaet
rand = [(0, 0), (7, 100), (10**6, 1)]
ergebnis = freie_kapazitaet(rand)
assert ergebnis == [100, 0, 99], f"freie_kapazitaet({rand}) ergibt {ergebnis!r}, erwartet war [100, 0, 99]."

# Ränder (Schwelle 0 und 100): spitzen
for schwelle, erwartet in [(0, [7, 10**6]), (100, [])]:
    ergebnis = spitzen(rand, schwelle)
    assert ergebnis == erwartet, f"spitzen({rand}, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Ränder (Schwelle 0 und 100): meldungen
for schwelle, erwartet in [(0, ["Minute 7: 100 %", "Minute 1000000: 1 %"]), (100, [])]:
    ergebnis = meldungen(rand, schwelle)
    assert vergleichbare_texte(ergebnis) == vergleichbare_texte(erwartet), (
        f"meldungen({rand}, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Leere Messreihe ergibt leere Listen
for funktion, argumente in [(freie_kapazitaet, ([],)), (spitzen, ([], 50)), (meldungen, ([], 50))]:
    ergebnis = funktion(*argumente)
    assert ergebnis == [], f"{funktion.__name__} mit leerer Messreihe ergibt {ergebnis!r}, erwartet war []."

# Die Messreihe bleibt unverändert
kopie = [(1, 10), (2, 95)]
freie_kapazitaet(kopie)
spitzen(kopie, 50)
meldungen(kopie, 50)
assert kopie == [(1, 10), (2, 95)], f"Nach den drei Aufrufen ist die Messreihe {kopie!r}, sie soll unverändert sein."

def bauweise_meldung(funktion):
    """Baut die Meldung, ob funktion eine List Comprehension und ob sie eine Schleife oder append enthält."""
    mit_comprehension, mit_schleife = bauweise(funktion)
    return (
        f"{funktion.__name__} soll mit einer List Comprehension [… for … in … if …] arbeiten, "
        f"ohne for-/while-Anweisung und ohne append; gefunden: List Comprehension {'ja' if mit_comprehension else 'nein'}, "
        f"Schleife oder append {'ja' if mit_schleife else 'nein'}."
    )


# freie_kapazitaet benutzt eine List Comprehension, keine Schleife mit append
assert bauweise(freie_kapazitaet) == (True, False), bauweise_meldung(freie_kapazitaet)

# spitzen benutzt eine List Comprehension, keine Schleife mit append
assert bauweise(spitzen) == (True, False), bauweise_meldung(spitzen)

# meldungen benutzt eine List Comprehension, keine Schleife mit append
assert bauweise(meldungen) == (True, False), bauweise_meldung(meldungen)

# Vergleichslösung mit einer gewöhnlichen Schleife über die Indizes
def von_hand(messungen, schwelle):
    """Berechnet alle drei Ergebnisse mit einer Schleife über die Indizes."""
    frei, minuten, texte = [], [], []
    for index in range(len(messungen)):
        minute = messungen[index][0]
        prozent = messungen[index][1]
        frei.append(100 - prozent)
        if prozent > schwelle:
            minuten.append(minute)
            texte.append("Minute " + str(minute) + ": " + str(prozent) + " %")
    return frei, minuten, texte


# 300 zufällige Messreihen: freie_kapazitaet
zufall = Zufall(3017)
zufaellige = []
for _ in range(300):
    minuten = sorted(zufall.sample(range(0, 10**6 + 1), zufall.randint(0, 8)))
    reihe = [(minute, zufall.randint(0, 100)) for minute in minuten]
    schwelle = zufall.randint(0, 100)
    zufaellige.append((reihe, schwelle))
for reihe, schwelle in zufaellige:
    erwartet = von_hand(reihe, schwelle)[0]
    ergebnis = freie_kapazitaet(reihe)
    assert ergebnis == erwartet, f"Mit reihe = {reihe} ergibt freie_kapazitaet(reihe) {ergebnis!r}, erwartet war {erwartet!r}."

# Dieselben 300 zufälligen Messreihen: spitzen
for reihe, schwelle in zufaellige:
    erwartet = von_hand(reihe, schwelle)[1]
    ergebnis = spitzen(reihe, schwelle)
    assert ergebnis == erwartet, (
        f"Mit reihe = {reihe} ergibt spitzen(reihe, {schwelle}) {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Dieselben 300 zufälligen Messreihen: meldungen
for reihe, schwelle in zufaellige:
    erwartet = von_hand(reihe, schwelle)[2]
    ergebnis = meldungen(reihe, schwelle)
    assert vergleichbare_texte(ergebnis) == vergleichbare_texte(erwartet), (
        f"Mit reihe = {reihe} ergibt meldungen(reihe, {schwelle}) {ergebnis!r}, erwartet war {erwartet!r}."
    )

# An der oberen Grenze: 100 000 Messungen bei freie_kapazitaet
gross = [(minute * 10, (minute * 37) % 101) for minute in range(100000)]
erwartet = von_hand(gross, 95)
ergebnis = freie_kapazitaet(gross)
assert ergebnis == erwartet[0], (
    f"Bei 100 000 Messungen liefert freie_kapazitaet {len(ergebnis)} Einträge, erwartet waren {len(erwartet[0])}; "
    f"die ersten sind {ergebnis[:3]}, erwartet {erwartet[0][:3]}."
)

# An der oberen Grenze: 100 000 Messungen bei spitzen
ergebnis = spitzen(gross, 95)
assert ergebnis == erwartet[1], (
    f"Bei 100 000 Messungen liefert spitzen {len(ergebnis)} Einträge, erwartet waren {len(erwartet[1])}; "
    f"die ersten Spitzen {erwartet[1][:3]}, Ihre {ergebnis[:3]}."
)

# An der oberen Grenze: 100 000 Messungen bei meldungen
ergebnis = meldungen(gross, 95)
assert vergleichbare_texte(ergebnis) == vergleichbare_texte(erwartet[2]), (
    f"Bei 100 000 Messungen liefert meldungen {len(ergebnis)} Einträge, erwartet waren {len(erwartet[2])}; "
    f"die ersten {erwartet[2][:3]}, Ihre {ergebnis[:3]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[65, 3, 12, 60]\n[481, 482]\n['Minute 481: 97 %']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
