# Automatisch erzeugt aus lehrkraft/muster/3_032_speichertarife.py - nicht von Hand ändern.
# vorlage-hash: 14e0188aea055020
# text-hash: de377b7dfb64b6b1
# thema: funktionen
# inhalt: Funktionen als Rückgabe

def preis_von_hand(grundgebuehr, freikontingent, preis_pro_gb, gigabyte):
    """Vergleichsrechnung mit if statt max."""
    if gigabyte <= freikontingent:
        return grundgebuehr
    return grundgebuehr + (gigabyte - freikontingent) * preis_pro_gb


def baue_sicher(*werte):
    """Ruft baue_tarif(*werte) auf; liefert das Ergebnis oder eine Beschreibung des Abbruchs."""
    try:
        return baue_tarif(*werte)
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"


# baue_tarif gibt eine Funktion zurück
basis_test = baue_sicher(500, 100, 4)
assert callable(basis_test), (
    f"baue_tarif(500, 100, 4) ergibt {basis_test!r}, erwartet war eine Funktion.\n"
    "Tipp: Geben Sie die innere Funktion mit return zurück, ohne Klammern dahinter (return monatspreis)."
)

# Die Beispiele aus der Aufgabe
for gigabyte, erwartet in [(130, 620), (80, 500)]:
    ergebnis = basis_test(gigabyte)
    assert ergebnis == erwartet, f"baue_tarif(500, 100, 4)({gigabyte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Genau das Freikontingent und keine belegten Gigabyte kosten nur die Grundgebühr
for gigabyte in [100, 0]:
    ergebnis = basis_test(gigabyte)
    assert ergebnis == 500, (
        f"baue_tarif(500, 100, 4)({gigabyte}) ergibt {ergebnis!r}, erwartet war 500 (nur die Grundgebühr).\n"
        "Tipp: Bezahlt wird nur, was über dem Freikontingent liegt; darunter gibt es nichts zurück."
    )

# Ein Gigabyte über dem Freikontingent
assert basis_test(101) == 504, f"baue_tarif(500, 100, 4)(101) ergibt {basis_test(101)!r}, erwartet war 504."

# Jeder Tarif behält seine eigenen Werte, auch nachdem weitere gebaut wurden
erster = baue_sicher(100, 10, 5)
zweiter = baue_sicher(2000, 0, 1)
ergebnisse = (erster(20), zweiter(20))
assert ergebnisse == (150, 2020), (
    "Nach erster = baue_tarif(100, 10, 5) und zweiter = baue_tarif(2000, 0, 1) ergeben erster(20) und "
    f"zweiter(20) {ergebnisse!r}, erwartet war (150, 2020).\n"
    "Tipp: Speichern Sie die Werte nicht in globalen Variablen; die innere Funktion liest die Parameter der äußeren."
)

# Tarif ohne Grundgebühr und ohne Freikontingent, Tarif ganz ohne Preis pro GB
for werte, gigabyte in [((0, 0, 3), 7), ((900, 50, 0), 10**6), ((0, 0, 0), 0)]:
    ergebnis = baue_sicher(*werte)(gigabyte)
    erwartet = preis_von_hand(*werte, gigabyte)
    assert ergebnis == erwartet, f"baue_tarif{werte}({gigabyte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die Beispiele zu billigster_tarif
tarife = {"Basis": baue_tarif(500, 100, 4), "Profi": baue_tarif(1500, 500, 2)}
for gigabyte, erwartet in [(130, "Basis"), (900, "Profi")]:
    ergebnis = billigster_tarif(tarife, gigabyte)
    assert ergebnis == erwartet, (
        f'billigster_tarif({{"Basis": baue_tarif(500, 100, 4), "Profi": baue_tarif(1500, 500, 2)}}, {gigabyte}) '
        f"ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Nur ein Tarif
ergebnis = billigster_tarif({"Einzig": baue_tarif(1, 1, 1)}, 5)
assert ergebnis == "Einzig", f'billigster_tarif({{"Einzig": baue_tarif(1, 1, 1)}}, 5) ergibt {ergebnis!r}, erwartet war "Einzig".'

# Bei gleichem Preis gewinnt der zuerst genannte Tarif, auch wenn er am Ende steht
tarife = {"C": baue_tarif(300, 0, 0), "A": baue_tarif(200, 0, 0), "B": baue_tarif(200, 0, 0)}
ergebnis = billigster_tarif(tarife, 10)
assert ergebnis == "A", (
    f"Bei den Tarifen C (300 Cent), A (200 Cent) und B (200 Cent) ergibt billigster_tarif {ergebnis!r}, "
    "erwartet war 'A'.\nTipp: Ersetzen Sie den bisher besten Tarif nur, wenn ein anderer wirklich billiger ist (<, nicht <=)."
)

# Der billigste Tarif steht am Ende
tarife = {"Teuer": baue_tarif(900, 0, 9), "Mittel": baue_tarif(500, 0, 5), "Billig": baue_tarif(100, 0, 1)}
ergebnis = billigster_tarif(tarife, 10)
assert ergebnis == "Billig", f"Bei drei Tarifen, deren letzter am billigsten ist, ergibt billigster_tarif {ergebnis!r}, erwartet war 'Billig'."

# Preisfunktionen, die nicht von baue_tarif stammen, gehen auch
tarife = {"Pauschal": lambda gigabyte: 1000, "Pro GB": lambda gigabyte: 3 * gigabyte}
for gigabyte, erwartet in [(100, "Pro GB"), (400, "Pauschal")]:
    ergebnis = billigster_tarif(tarife, gigabyte)
    assert ergebnis == erwartet, (
        f'billigster_tarif({{"Pauschal": lambda gigabyte: 1000, "Pro GB": lambda gigabyte: 3 * gigabyte}}, '
        f"{gigabyte}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Rufen Sie für jeden Tarif seine Preisfunktion mit gigabyte auf und vergleichen Sie die Preise."
    )

# 300 zufällige Tarife und Mengen gegen eine Vergleichsrechnung
zufall = Zufall(3032)
for _ in range(300):
    werte = (zufall.randint(0, 10**6), zufall.randint(0, 10**5), zufall.randint(0, 10**4))
    gigabyte = zufall.choice([zufall.randint(0, 10**6), werte[1], werte[1] + 1, zufall.randint(0, 200)])
    ergebnis = baue_tarif(*werte)(gigabyte)
    erwartet = preis_von_hand(*werte, gigabyte)
    assert ergebnis == erwartet, f"baue_tarif{werte}({gigabyte}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# 200 zufällige Tarifvergleiche, oft mit gleichen Preisen
for _ in range(200):
    roh = {}
    for nummer in range(zufall.randint(1, 6)):
        roh[f"T{nummer}"] = (zufall.randint(0, 5) * 100, zufall.randint(0, 3) * 50, zufall.randint(0, 3))
    gigabyte = zufall.randint(0, 300)
    tarife = {name: baue_tarif(*werte) for name, werte in roh.items()}
    preise = [preis_von_hand(*werte, gigabyte) for werte in roh.values()]
    erwartet = list(roh)[preise.index(min(preise))]
    ergebnis = billigster_tarif(tarife, gigabyte)
    assert ergebnis == erwartet, (
        f"Tarife (Grundgebühr, Freikontingent, Preis pro GB) {roh}, {gigabyte} GB: billigster_tarif ergibt "
        f"{ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenze: 1000 Tarife, der billigste steht irgendwo in der Mitte
tarife = {f"Tarif {nummer}": baue_tarif(10**6 - nummer * (nummer % 7), 10**5, 10**4) for nummer in range(1000)}
gigabyte = 10**6
preise = {name: funktion(gigabyte) for name, funktion in tarife.items()}
erwartet = min(preise, key=preise.get)
ergebnis = billigster_tarif(tarife, gigabyte)
assert ergebnis == erwartet, f"Bei 1000 Tarifen und 10**6 GB ergibt billigster_tarif {ergebnis!r}, erwartet war {erwartet!r}."

# Die Ausgabe des Programms stimmt
assert AUSGABE == "620\nProfi", f"Erwartete Ausgabe:\n620\nProfi\nIhr Programm gibt aus:\n{AUSGABE}"
