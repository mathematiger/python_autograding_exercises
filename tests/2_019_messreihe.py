# Automatisch erzeugt aus lehrkraft/muster/2_019_messreihe.py - nicht von Hand ändern.
# vorlage-hash: 6525ad7e375670a9
# text-hash: 666404ce99148fbe
# thema: datenstrukturen
# inhalt: Liste in einer Funktion ändern

# entferne_ausfaelle aus dem Beispiel
cpu = [12, -1, 47, 130, -1, 99]
ergebnis = entferne_ausfaelle(cpu)
assert cpu == [12, 47, 130, 99], (
    f"Nach entferne_ausfaelle(cpu) mit cpu = [12, -1, 47, 130, -1, 99] ist cpu {cpu!r}, erwartet war [12, 47, 130, 99].\n"
    "Tipp: werte = [...] in der Funktion ändert die Liste des Aufrufers nicht; ändern Sie die Liste selbst, "
    "etwa mit messwerte[:] = ... oder remove."
)

# entferne_ausfaelle gibt nichts zurück
cpu = [5, -1]
ergebnis = entferne_ausfaelle(cpu)
assert ergebnis is None, f"entferne_ausfaelle soll nichts zurückgeben, gibt aber {ergebnis!r} zurück."

# Es bleibt dieselbe Liste, auch für andere Namen derselben Liste
cpu = [-1, 3, -1]
dieselbe = cpu
entferne_ausfaelle(cpu)
assert dieselbe is cpu and dieselbe == [3], (
    f"Nach entferne_ausfaelle(cpu) mit cpu = [-1, 3, -1] sieht ein zweiter Name derselben Liste {dieselbe!r}, erwartet war [3]."
)

# Weitere Fälle: mehrere -1 hintereinander, nur -1, keine -1, leere Liste, 0 bleibt
for vorher, erwartet in [
    ([-1, -1, 7, -1, -1, -1, 8], [7, 8]),
    ([-1, -1, -1], []),
    ([0, 1000, 3], [0, 1000, 3]),
    ([], []),
    ([0, -1, 0], [0, 0]),
]:
    werte = list(vorher)
    entferne_ausfaelle(werte)
    assert werte == erwartet, (
        f"entferne_ausfaelle mit {vorher} ergibt {werte!r}, erwartet war {erwartet}.\n"
        "Tipp: Wer beim Durchlaufen mit for aus derselben Liste entfernt, überspringt das Element danach."
    )

# kappe aus dem Beispiel
cpu = [12, 47, 130, 99]
ergebnis = kappe(cpu, 100)
assert (ergebnis, cpu) == (1, [12, 47, 100, 99]), (
    f"kappe(cpu, 100) mit cpu = [12, 47, 130, 99] gibt {ergebnis!r} zurück, cpu ist danach {cpu!r}; "
    "erwartet waren 1 und [12, 47, 100, 99]."
)

# kappe ändert dieselbe Liste und zählt richtig
for vorher, obergrenze, erwartet, anzahl in [
    ([150, 200, 50], 100, [100, 100, 50], 2),
    ([100, 101, 99], 100, [100, 100, 99], 1),
    ([1, 2, 3], 1000, [1, 2, 3], 0),
    ([0, 5, 0], 0, [0, 0, 0], 1),
    ([], 50, [], 0),
]:
    werte = list(vorher)
    dieselbe = werte
    ergebnis = kappe(werte, obergrenze)
    assert (ergebnis, dieselbe) == (anzahl, erwartet), (
        f"kappe({vorher}, {obergrenze}) gibt {ergebnis!r} zurück, die Liste ist danach {dieselbe!r}; "
        f"erwartet waren {anzahl} und {erwartet}.\nTipp: Genau obergrenze ist nicht zu groß und wird nicht gezählt."
    )


# Vergleichslösung: neue Listen bauen
def bereinigt_von_hand(werte, obergrenze):
    """Gibt die Liste ohne -1 und gekappt sowie die Zahl der gekappten Werte zurück."""
    ohne = [wert for wert in werte if wert != -1]
    gekappt = [min(wert, obergrenze) for wert in ohne]
    return ohne, gekappt, len([wert for wert in ohne if wert > obergrenze])


# 500 zufällige Messreihen
zufall = Zufall(2019)
for _ in range(500):
    vorher = [zufall.choice([-1, -1, zufall.randint(0, 120), zufall.randint(0, 1000)]) for _ in range(zufall.randint(0, 15))]
    obergrenze = zufall.randint(0, 120)
    ohne, gekappt, anzahl = bereinigt_von_hand(vorher, obergrenze)
    werte = list(vorher)
    entferne_ausfaelle(werte)
    assert werte == ohne, f"entferne_ausfaelle mit {vorher} ergibt {werte!r}, erwartet war {ohne}."
    ergebnis = kappe(werte, obergrenze)
    assert (ergebnis, werte) == (anzahl, gekappt), (
        f"kappe({ohne}, {obergrenze}) gibt {ergebnis!r} zurück, die Liste ist danach {werte!r}; "
        f"erwartet waren {anzahl} und {gekappt}."
    )

# An der oberen Grenze: 10 000 Messwerte, davon 1000 Ausfälle
gross = []
for nummer in range(10000):
    if nummer % 10 == 0:
        gross.append(-1)
    else:
        gross.append(nummer % 1001)
erwartet_ohne, erwartet_gekappt, erwartet_anzahl = bereinigt_von_hand(gross, 500)
entferne_ausfaelle(gross)
ergebnis = kappe(gross, 500)
assert (len(gross), ergebnis, gross == erwartet_gekappt) == (9000, erwartet_anzahl, True), (
    f"Bei 10 000 Messwerten mit 1000 Ausfällen hat die Liste danach {len(gross)} Werte, kappe(…, 500) ersetzt "
    f"{ergebnis!r}; erwartet waren 9000 Werte und {erwartet_anzahl} Ersetzungen."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[12, 47, 130, 99]\n1\n[12, 47, 100, 99]"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
