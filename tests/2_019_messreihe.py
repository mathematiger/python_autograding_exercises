# Automatisch erzeugt aus lehrkraft/muster/2_019_messreihe.py - nicht von Hand ändern.
# vorlage-hash: 6525ad7e375670a9
# text-hash: acc25427bd0a5215
# thema: datenstrukturen
# inhalt: Liste in einer Funktion ändern

# entferne_ausfaelle aus dem Beispiel
cpu = [12, -1, 47, 130, -1, 99]
ergebnis = entferne_ausfaelle(cpu)
assert cpu == [12, 47, 130, 99], (
    f"Nach entferne_ausfaelle(cpu) mit cpu = [12, -1, 47, 130, -1, 99] ist cpu {cpu!r}, erwartet war [12, 47, 130, 99].\n"
    "Tipp: messwerte = [...] in der Funktion ändert die Liste des Aufrufers nicht; ändern Sie die Liste selbst, "
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
    if werte == vorher:
        hinweis = "\nTipp: Die Liste ist unverändert. Ändern Sie die Liste selbst, nicht nur den lokalen Namen messwerte."
    elif -1 in werte:
        hinweis = "\nTipp: Wer beim Durchlaufen mit for aus derselben Liste entfernt, überspringt das Element danach."
    else:
        hinweis = ""
    assert werte == erwartet, f"entferne_ausfaelle mit {vorher} ergibt {werte!r}, erwartet war {erwartet}.{hinweis}"

# kappe aus dem Beispiel: die Liste wird gekappt
cpu = [12, 47, 130, 99]
ergebnis = kappe(cpu, 100)
assert cpu == [12, 47, 100, 99], (
    f"Nach kappe(cpu, 100) mit cpu = [12, 47, 130, 99] ist cpu {cpu!r}, erwartet war [12, 47, 100, 99].\n"
    "Tipp: Ändern Sie messwerte[index], nicht die Schleifenvariable oder einen lokalen Namen."
)

# kappe aus dem Beispiel: die Zahl der Ersetzungen
cpu = [12, 47, 130, 99]
ergebnis = kappe(cpu, 100)
assert ergebnis == 1, (
    f"kappe(cpu, 100) mit cpu = [12, 47, 130, 99] gibt {ergebnis!r} zurück, erwartet war 1.\n"
    "Tipp: Zählen Sie die Ersetzungen in einer Variablen mit und geben Sie sie am Ende mit return zurück."
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
    if dieselbe == vorher and anzahl > 0:
        hinweis = (
            "Tipp: Die Liste ist unverändert. Ändern Sie messwerte[index], nicht die Schleifenvariable "
            "oder einen lokalen Namen."
        )
    else:
        hinweis = "Tipp: Genau obergrenze ist nicht zu groß und wird nicht gezählt."
    assert (ergebnis, dieselbe) == (anzahl, erwartet), (
        f"kappe({vorher}, {obergrenze}) gibt {ergebnis!r} zurück, die Liste ist danach {dieselbe!r}; "
        f"erwartet waren {anzahl} und {erwartet}.\n{hinweis}"
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

# 500 zufällige Messreihen ohne Ausfälle für kappe
zufall = Zufall(2019)
for _ in range(500):
    vorher = [zufall.choice([-1, -1, zufall.randint(0, 120), zufall.randint(0, 1000)]) for _ in range(zufall.randint(0, 15))]
    obergrenze = zufall.randint(0, 120)
    ohne, gekappt, anzahl = bereinigt_von_hand(vorher, obergrenze)
    werte = list(ohne)
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

# An der oberen Grenze: entferne_ausfaelle bei 10 000 Messwerten, davon 1000 Ausfälle
werte = list(gross)
entferne_ausfaelle(werte)
assert werte == erwartet_ohne, (
    f"Bei 10 000 Messwerten mit 1000 Ausfällen hat die Liste nach entferne_ausfaelle {len(werte)} Werte, "
    f"davon {werte.count(-1)} mal -1; erwartet waren 9000 Werte ohne -1."
)

# An der oberen Grenze: kappe bei 9000 Messwerten
werte = list(erwartet_ohne)
ergebnis = kappe(werte, 500)
assert (ergebnis, werte == erwartet_gekappt) == (erwartet_anzahl, True), (
    f"Bei 9000 Messwerten ersetzt kappe(…, 500) {ergebnis!r} Werte, danach sind {len([w for w in werte if w > 500])} "
    f"über 500; erwartet waren {erwartet_anzahl} Ersetzungen und keiner über 500."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[12, 47, 130, 99]\n1\n[12, 47, 100, 99]"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
