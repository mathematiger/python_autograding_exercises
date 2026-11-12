# Automatisch erzeugt aus lehrkraft/muster/3_018_sensorkarte.py - nicht von Hand ändern.
# vorlage-hash: a2c881074a4602e9
# text-hash: f46d9e7d34250486
# thema: kontrollfluss
# inhalt: Dict Comprehension

import ast
import inspect
import textwrap


def bauweise(funktion):
    """Gibt zurück, ob die Funktion eine Dict Comprehension und ob sie eine for-/while-Anweisung enthält."""
    try:
        baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    except (OSError, TypeError, SyntaxError):
        return False, False
    mit_comprehension = False
    mit_schleife = False
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.DictComp):
            mit_comprehension = True
        if isinstance(knoten, (ast.For, ast.While)):
            mit_schleife = True
    return mit_comprehension, mit_schleife


def gleich(ergebnis, erwartet):
    """Vergleicht zwei Dictionaries mit Temperaturen; Kommazahlen dürfen in der letzten Stelle abweichen."""
    if not isinstance(ergebnis, dict) or ergebnis.keys() != erwartet.keys():
        return False
    for sensor, wert in erwartet.items():
        if not isinstance(ergebnis[sensor], (int, float)) or abs(ergebnis[sensor] - wert) > 0.000001:
            return False
    return True


# in_celsius aus dem Beispiel
ergebnis = in_celsius({"s1": 215, "s2": -32768, "s3": -45})
assert gleich(ergebnis, {"s1": 21.5, "s3": -4.5}), (
    f'in_celsius({{"s1": 215, "s2": -32768, "s3": -45}}) ergibt {ergebnis!r}, erwartet war {{"s1": 21.5, "s3": -4.5}}.\n'
    "Tipp: Teilen Sie den Rohwert durch 10, und lassen Sie Sensoren mit dem Fehlerwert -32768 mit if weg."
)

# Andere Werte (nicht fest hinschreiben!)
for rohwerte, erwartet in [
    ({"a": 200}, {"a": 20.0}),
    ({"t7": 1, "t8": -1, "t9": 0}, {"t7": 0.1, "t8": -0.1, "t9": 0.0}),
    ({"x": -400, "y": 1250}, {"x": -40.0, "y": 125.0}),
]:
    ergebnis = in_celsius(rohwerte)
    assert gleich(ergebnis, erwartet), f"in_celsius({rohwerte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Nur Fehlerwerte oder gar keine Sensoren ergeben ein leeres Dictionary
for rohwerte in [{"s1": -32768, "s2": -32768}, {}]:
    ergebnis = in_celsius(rohwerte)
    assert ergebnis == {}, (
        f"in_celsius({rohwerte}) ergibt {ergebnis!r}, erwartet war {{}}.\n"
        "Tipp: Sensoren mit -32768 sollen ganz fehlen, nicht mit -3276.8 im Ergebnis stehen."
    )

# topic_von aus dem Beispiel
ergebnis = topic_von({"haus1/beet3/temp": "s1", "haus2/tisch1/temp": "s3"})
erwartet = {"s1": "haus1/beet3/temp", "s3": "haus2/tisch1/temp"}
assert ergebnis == erwartet, (
    f"topic_von(...) aus dem Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Packen Sie die Paare aus .items() aus und vertauschen Sie vorn Schlüssel und Wert."
)

# Ein einzelner Eintrag und gar keiner
for sensoren, erwartet in [({"a/b": "k"}, {"k": "a/b"}), ({}, {})]:
    ergebnis = topic_von(sensoren)
    assert ergebnis == erwartet, f"topic_von({sensoren}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# in_celsius lässt das übergebene Dictionary unverändert
rohwerte = {"s1": 215, "s2": -32768}
in_celsius(rohwerte)
assert rohwerte == {"s1": 215, "s2": -32768}, (
    f"Nach dem Aufruf ist rohwerte {rohwerte!r}, soll aber unverändert {{'s1': 215, 's2': -32768}} bleiben.\n"
    "Tipp: Eine Dict Comprehension baut ein neues Dictionary, statt das alte zu ändern."
)

# topic_von lässt das übergebene Dictionary unverändert
sensoren = {"a/temp": "s1"}
topic_von(sensoren)
assert sensoren == {"a/temp": "s1"}, (
    f"Nach dem Aufruf ist sensoren {sensoren!r}, soll aber unverändert {{'a/temp': 's1'}} bleiben.\n"
    "Tipp: Eine Dict Comprehension baut ein neues Dictionary, statt das alte zu ändern."
)

# in_celsius benutzt eine Dict Comprehension, keine Schleife
mit_comprehension, mit_schleife = bauweise(in_celsius)
assert mit_comprehension and not mit_schleife, (
    "in_celsius soll mit einer Dict Comprehension {schlüssel: wert for … in ….items()} arbeiten, "
    f"ohne for- oder while-Anweisung; gefunden: Dict Comprehension {'ja' if mit_comprehension else 'nein'}, "
    f"Schleife {'ja' if mit_schleife else 'nein'}."
)

# topic_von benutzt eine Dict Comprehension, keine Schleife
mit_comprehension, mit_schleife = bauweise(topic_von)
assert mit_comprehension and not mit_schleife, (
    "topic_von soll mit einer Dict Comprehension {schlüssel: wert for … in ….items()} arbeiten, "
    f"ohne for- oder while-Anweisung; gefunden: Dict Comprehension {'ja' if mit_comprehension else 'nein'}, "
    f"Schleife {'ja' if mit_schleife else 'nein'}."
)


# Vergleichslösungen mit gewöhnlichen Schleifen über die Schlüssel
def celsius_von_hand(rohwerte):
    """Rechnet die Temperaturen mit einer Schleife über die Schlüssel um."""
    ergebnis = {}
    for sensor in rohwerte:
        if rohwerte[sensor] == -32768:
            continue
        ergebnis[sensor] = rohwerte[sensor] / 10
    return ergebnis


def umgedreht_von_hand(sensoren):
    """Dreht die Zuordnung mit einer Schleife über die Schlüssel um."""
    ergebnis = {}
    for topic in sensoren:
        ergebnis[sensoren[topic]] = topic
    return ergebnis


def zufaellige_gewaechshaeuser():
    """Liefert 300 zufällige Paare (rohwerte, sensoren), bei jedem Aufruf dieselben."""
    zufall = Zufall(3018)
    paare = []
    for _ in range(300):
        anzahl = zufall.randint(0, 8)
        kennungen = [f"s{nummer}" for nummer in zufall.sample(range(100), anzahl)]
        rohwerte = {sensor: zufall.choice([zufall.randint(-400, 1250), -32768]) for sensor in kennungen}
        sensoren = {f"haus{zufall.randint(1, 3)}/beet{nummer}/temp": sensor for nummer, sensor in enumerate(kennungen)}
        paare.append((rohwerte, sensoren))
    return paare


# in_celsius in 300 zufälligen Gewächshäusern
for rohwerte, sensoren in zufaellige_gewaechshaeuser():
    erwartet = celsius_von_hand(rohwerte)
    ergebnis = in_celsius(rohwerte)
    assert gleich(ergebnis, erwartet), f"in_celsius({rohwerte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# topic_von in 300 zufälligen Gewächshäusern
for rohwerte, sensoren in zufaellige_gewaechshaeuser():
    erwartet = umgedreht_von_hand(sensoren)
    ergebnis = topic_von(sensoren)
    assert ergebnis == erwartet, f"topic_von({sensoren}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 000 Sensoren, jeder siebte meldet einen Fehler
rohwerte = {f"s{nummer}": (-32768 if nummer % 7 == 0 else nummer % 1651 - 400) for nummer in range(100000)}
sensoren = {f"halle{nummer // 1000}/platz{nummer % 1000}/temp": f"s{nummer}" for nummer in range(100000)}
ergebnis = in_celsius(rohwerte)
erwartet = celsius_von_hand(rohwerte)
umgedreht = topic_von(sensoren)
assert gleich(ergebnis, erwartet) and umgedreht == umgedreht_von_hand(sensoren), (
    f"Bei 100 000 Sensoren liefert in_celsius {len(ergebnis)} Einträge (erwartet {len(erwartet)}) "
    f"und topic_von {len(umgedreht)} Einträge (erwartet 100000); "
    f"topic_von(...)['s12345'] ist {umgedreht.get('s12345')!r}, erwartet 'halle12/platz345/temp'."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{'s1': 21.5, 's3': -4.5}\n{'s1': 'haus1/beet3/temp', 's3': 'haus2/tisch1/temp'}"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
