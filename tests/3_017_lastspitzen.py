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
assert ergebnis == ["Minute 481: 97 %"], (
    f'meldungen(messungen, 90) ergibt {ergebnis!r}, erwartet war ["Minute 481: 97 %"].\n'
    'Tipp: Ein f-String wie f"Minute {minute}: {prozent} %" baut den Text.'
)

# Andere Schwellen (nicht fest hinschreiben!)
for schwelle, erwartet in [(30, [480, 481, 482, 483]), (90, [481]), (97, []), (39, [481, 482, 483])]:
    ergebnis = spitzen(messungen, schwelle)
    assert ergebnis == erwartet, f"spitzen(messungen, {schwelle}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Genau die Schwelle zählt nicht als Spitze
grenzfall = [(0, 50), (1, 51), (2, 49)]
ergebnis = spitzen(grenzfall, 50)
ergebnis_text = meldungen(grenzfall, 50)
assert ergebnis == [1] and ergebnis_text == ["Minute 1: 51 %"], (
    f"Bei {grenzfall} und schwelle 50 ergeben spitzen {ergebnis!r} und meldungen {ergebnis_text!r}; "
    'erwartet waren [1] und ["Minute 1: 51 %"].\nTipp: „größer als schwelle“ heißt prozent > schwelle, genau 50 zählt nicht.'
)

# Ränder: 0 und 100 Prozent, Schwelle 0 und 100, Minute 0 und 10**6
rand = [(0, 0), (7, 100), (10**6, 1)]
for funktion, argumente, erwartet in [
    (freie_kapazitaet, (rand,), [100, 0, 99]),
    (spitzen, (rand, 0), [7, 10**6]),
    (spitzen, (rand, 100), []),
    (meldungen, (rand, 0), ["Minute 7: 100 %", "Minute 1000000: 1 %"]),
    (meldungen, (rand, 100), []),
]:
    ergebnis = funktion(*argumente)
    aufruf = f"{funktion.__name__}({rand}" + "".join(f", {wert}" for wert in argumente[1:]) + ")"
    assert ergebnis == erwartet, f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet!r}."

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

# Jede Funktion benutzt eine List Comprehension, keine Schleife mit append
for funktion in [freie_kapazitaet, spitzen, meldungen]:
    mit_comprehension, mit_schleife = bauweise(funktion)
    assert mit_comprehension and not mit_schleife, (
        f"{funktion.__name__} soll mit einer List Comprehension [… for … in … if …] arbeiten, "
        f"ohne for-/while-Anweisung und ohne append; gefunden: List Comprehension {'ja' if mit_comprehension else 'nein'}, "
        f"Schleife oder append {'ja' if mit_schleife else 'nein'}."
    )


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


# 300 zufällige Messreihen
zufall = Zufall(3017)
for _ in range(300):
    minuten = sorted(zufall.sample(range(0, 10**6 + 1), zufall.randint(0, 8)))
    reihe = [(minute, zufall.randint(0, 100)) for minute in minuten]
    schwelle = zufall.randint(0, 100)
    erwartet = von_hand(reihe, schwelle)
    ergebnis = (freie_kapazitaet(reihe), spitzen(reihe, schwelle), meldungen(reihe, schwelle))
    for name, wert, soll in zip(["freie_kapazitaet(reihe)", f"spitzen(reihe, {schwelle})", f"meldungen(reihe, {schwelle})"], ergebnis, erwartet):
        assert wert == soll, f"Mit reihe = {reihe} ergibt {name} {wert!r}, erwartet war {soll!r}."

# An der oberen Grenze: 100 000 Messungen
gross = [(minute * 10, (minute * 37) % 101) for minute in range(100000)]
erwartet = von_hand(gross, 95)
ergebnis = (freie_kapazitaet(gross), spitzen(gross, 95), meldungen(gross, 95))
assert ergebnis == erwartet, (
    f"Bei 100 000 Messungen liefern die Funktionen {len(ergebnis[0])}, {len(ergebnis[1])} und {len(ergebnis[2])} Einträge; "
    f"erwartet waren {len(erwartet[0])}, {len(erwartet[1])} und {len(erwartet[2])}, "
    f"die ersten Spitzen {erwartet[1][:3]}, Ihre {ergebnis[1][:3]}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[65, 3, 12, 60]\n[481, 482]\n['Minute 481: 97 %']"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
