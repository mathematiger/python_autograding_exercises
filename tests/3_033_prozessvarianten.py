# Automatisch erzeugt aus lehrkraft/muster/3_033_prozessvarianten.py - nicht von Hand ändern.
# vorlage-hash: 01c7d4a968292fd5
# text-hash: ce5502594adedb67
# thema: algorithmen
# inhalt: Memoisierung mit Dictionary

def vergleich(n):
    """Vergleichslösung als Tabelle von unten, ohne Rekursion."""
    tabelle = [1, 1, 2]
    while len(tabelle) <= n:
        tabelle.append(tabelle[-1] + tabelle[-2] + tabelle[-3])
    return tabelle[n]


# Das Beispiel: drei Schritte
ergebnis = varianten(3)
assert ergebnis == 4, (
    f"varianten(3) ergibt {ergebnis!r}, erwartet war 4 (1+1+1, 1+2, 2+1, 3).\n"
    "Tipp: varianten(3) = varianten(2) + varianten(1) + varianten(0), und varianten(0) ist 1."
)

# Kleine Werte (nicht fest hinschreiben!)
for n, erwartet in [(1, 1), (2, 2), (4, 7), (5, 13), (10, 274)]:
    ergebnis = varianten(n)
    assert ergebnis == erwartet, f"varianten({n}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Null Schritte: genau eine Variante
ergebnis = varianten(0)
assert ergebnis == 1, (
    f"varianten(0) ergibt {ergebnis!r}, erwartet war 1 (nichts tun ist eine Variante).\n"
    "Tipp: Ohne die 1 bei n == 0 würde sich die ganze Rekursion zu 0 aufsummieren."
)

# Das Ergebnis landet im übergebenen merker
merker = {}
ergebnis = varianten(5, merker)
assert ergebnis == 13 and merker.get(5) == 13, (
    f"Nach merker = {{}} und varianten(5, merker) ist das Ergebnis {ergebnis!r} und merker = {merker!r}; "
    "erwartet waren 13 und merker[5] == 13.\n"
    "Tipp: Speichern Sie das Ergebnis mit merker[n] = ergebnis, bevor Sie es zurückgeben, und reichen Sie "
    "merker an die rekursiven Aufrufe weiter."
)

# Auch die Teilergebnisse landen im merker, alle richtig
merker = {}
varianten(12, merker)
falsche = [k for k in merker if not isinstance(k, int) or not 0 <= k <= 12 or merker[k] != vergleich(k)]
assert len(merker) >= 10 and not falsche, (
    f"Nach varianten(12, merker) enthält merker {merker!r}; erwartet waren richtige Werte für (fast) alle "
    "k von 1 bis 12.\nTipp: Reichen Sie merker an jeden rekursiven Aufruf weiter, damit alle dasselbe "
    "Dictionary benutzen."
)

# Ein schon gefüllter merker wird benutzt statt neu zu rechnen
merker = {20: 999}
ergebnis = varianten(20, merker)
assert ergebnis == 999, (
    f"Mit merker = {{20: 999}} ergibt varianten(20, merker) {ergebnis!r}; erwartet war 999 aus dem merker.\n"
    "Tipp: Schauen Sie zuerst mit if n in merker nach, bevor Sie rechnen."
)

# Ohne merker funktionieren mehrere Aufrufe nacheinander
bekommen = [varianten(6), varianten(7), varianten(6)]
assert bekommen == [24, 44, 24], f"varianten(6), varianten(7), varianten(6) ergeben {bekommen}, erwartet war [24, 44, 24]."

# Viele zufällige n, verglichen mit einer Tabelle
zufall = Zufall(3033)
for n in sorted(zufall.sample(range(0, 301), 60)):
    ergebnis = varianten(n)
    assert ergebnis == vergleich(n), f"varianten({n}) ergibt {ergebnis!r}, erwartet war {vergleich(n)}."

# Obere Grenze: n = 300
ergebnis = varianten(300)
assert ergebnis == vergleich(300), (
    f"varianten(300) ergibt eine falsche Zahl, erwartet war eine Zahl mit {len(str(vergleich(300)))} Stellen."
)

# Laufzeit: Jedes Teilergebnis wird nur einmal berechnet
_, schritte_30 = zaehle_schritte(varianten, 30)
_, schritte_120 = zaehle_schritte(varianten, 120)
assert schritte_30 <= 1000 and schritte_120 <= 4000, (
    f"varianten(30) braucht {schritte_30} Schritte, varianten(120) {schritte_120}; erwartet waren höchstens "
    "1000 und 4000, also O(n).\nTipp: Ohne Nachschlagen im merker wird dasselbe Teilergebnis immer wieder "
    "berechnet; prüfen Sie if n in merker, bevor Sie rekursiv rechnen."
)
