# Automatisch erzeugt aus lehrkraft/muster/3_018_sensortopics.py - nicht von Hand ändern.
# vorlage-hash: 80a27f2e22e5fb5c
# text-hash: 7180246164d7afe9
# thema: kontrollfluss
# inhalt: Dict Comprehension

def gleich_bis_auf_rundung(ergebnis, erwartet):
    """Prüft, ob zwei Dictionaries dieselben Schlüssel und bis auf Rundung gleiche Zahlen haben."""
    if not isinstance(ergebnis, dict) or set(ergebnis) != set(erwartet):
        return False
    for schluessel, wert in erwartet.items():
        if not isinstance(ergebnis[schluessel], (int, float)) or abs(ergebnis[schluessel] - wert) > 1e-9:
            return False
    return True


# in_celsius aus dem Beispiel; ausgefallene Sensoren fehlen
rohwerte = {"S1": 615, "S2": 0, "S3": 380}
ergebnis = in_celsius(rohwerte)
assert gleich_bis_auf_rundung(ergebnis, {"S1": 21.5, "S3": -2.0}), (
    f"in_celsius({rohwerte}) ergibt {ergebnis!r}, erwartet war {{'S1': 21.5, 'S3': -2.0}}.\n"
    "Tipp: Rechnen Sie (roh - 400) / 10 und lassen Sie mit if roh != 0 die ausgefallenen Sensoren weg."
)

# Andere Rohwerte (nicht fest hinschreiben!), auch an den Rändern 1 und 1023
for werte, erwartet in [
    ({"A": 400}, {"A": 0.0}),
    ({"A": 1, "B": 1023}, {"A": -39.9, "B": 62.3}),
    ({"T": 0, "U": 0}, {}),
    ({"x/1": 401, "x/2": 0, "x/3": 399}, {"x/1": 0.1, "x/3": -0.1}),
]:
    ergebnis = in_celsius(werte)
    assert gleich_bis_auf_rundung(ergebnis, erwartet), (
        f"in_celsius({werte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Ohne Sensoren
ergebnis = in_celsius({})
assert ergebnis == {}, f"in_celsius({{}}) ergibt {ergebnis!r}, erwartet war {{}}."

# umdrehen aus dem Beispiel
topics = {"S1": "halle1/ofen/temperatur", "S3": "halle2/tor/temperatur"}
ergebnis = umdrehen(topics)
erwartet = {"halle1/ofen/temperatur": "S1", "halle2/tor/temperatur": "S3"}
assert ergebnis == erwartet, (
    f"umdrehen({topics}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Vertauschen Sie vorne Schlüssel und Wert: {topic: kennung for kennung, topic in topics.items()}."
)

# Weitere Zuordnungen und das leere Dictionary
for zuordnung, erwartet in [({}, {}), ({"a": "b"}, {"b": "a"}), ({"a": "b", "b": "a"}, {"b": "a", "a": "b"})]:
    ergebnis = umdrehen(zuordnung)
    assert ergebnis == erwartet, f"umdrehen({zuordnung}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die Eingaben bleiben unverändert, die Ergebnisse sind neue Dictionaries
werte = {"S1": 615, "S2": 0}
zuordnung = {"S1": "t/1"}
celsius = in_celsius(werte)
umgedreht = umdrehen(zuordnung)
assert werte == {"S1": 615, "S2": 0} and zuordnung == {"S1": "t/1"} and celsius is not werte and umgedreht is not zuordnung, (
    f"Nach in_celsius und umdrehen sind die Eingaben {werte!r} und {zuordnung!r}; sie sollen unverändert bleiben, "
    "und die Ergebnisse sollen neue Dictionaries sein."
)

# Dict Comprehensions statt for-Schleife
assert not verwendet("for"), (
    "Schreiben Sie beide Funktionen ohne for-Schleife, jede mit einer Dict Comprehension der Form "
    "{schluessel: wert for kennung, wert in dictionary.items() if bedingung}."
)

# 300 zufällige Hallen
zufall = Zufall(3018)
for _ in range(300):
    kennungen = [f"S{nummer}" for nummer in zufall.sample(range(1, 200), zufall.randint(0, 8))]
    werte = {kennung: zufall.choice([0, 1, 400, 1023, zufall.randint(1, 1023)]) for kennung in kennungen}
    erwartet = {}
    for kennung in werte:
        if werte[kennung] > 0:
            erwartet[kennung] = werte[kennung] / 10 - 40
    ergebnis = in_celsius(werte)
    assert gleich_bis_auf_rundung(ergebnis, erwartet), f"in_celsius({werte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    zuordnung = {kennung: f"halle{zufall.randint(1, 3)}/{kennung}/wert" for kennung in kennungen}
    erwartet = {}
    for kennung in zuordnung:
        erwartet[zuordnung[kennung]] = kennung
    ergebnis = umdrehen(zuordnung)
    assert ergebnis == erwartet, f"umdrehen({zuordnung}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 000 Sensoren
gross_werte = {f"S{nummer:06d}": nummer % 1024 for nummer in range(100000)}
gross_topics = {f"S{nummer:06d}": f"halle{nummer % 7}/sensor{nummer}" for nummer in range(100000)}
ergebnis_celsius = in_celsius(gross_werte)
ergebnis_topics = umdrehen(gross_topics)
anzahl_erwartet = 100000 - len(range(0, 100000, 1024))
assert (
    len(ergebnis_celsius) == anzahl_erwartet
    and abs(ergebnis_celsius["S001023"] - 62.3) < 1e-9
    and "S001024" not in ergebnis_celsius
    and len(ergebnis_topics) == 100000
    and ergebnis_topics["halle4/sensor99999"] == "S099999"
), (
    f"Bei 100 000 Sensoren ergibt in_celsius {len(ergebnis_celsius)} Einträge und umdrehen {len(ergebnis_topics)}; "
    f"erwartet waren {anzahl_erwartet} (ohne die Rohwerte 0) und 100000."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{'S1': 21.5, 'S3': -2.0}\n{'halle1/ofen/temperatur': 'S1', 'halle2/tor/temperatur': 'S3'}"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
