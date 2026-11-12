# Automatisch erzeugt aus lehrkraft/muster/3_033_zahlungsplaene.py - nicht von Hand ändern.
# vorlage-hash: 2f3dd6ff8830a2cd
# text-hash: 8744dfade38d5526
# thema: algorithmen
# inhalt: Memoisierung mit Dictionary

def plaene_von_hand(monate):
    """Vergleichslösung mit einer Schleife von unten nach oben."""
    vorletzter, letzter = 1, 1
    for _ in range(monate - 1):
        vorletzter, letzter = letzter, vorletzter + letzter
    return letzter


class ZuVieleAufrufe(Exception):
    """Bricht eine Rechnung ab, die sich viel zu oft selbst aufruft."""


def zaehle_aufrufe(monate, hoechstens):
    """Ruft zahlungsplaene(monate) auf und zählt alle Aufrufe, auch die rekursiven.

    Liefert (Ergebnis, Aufrufe); Ergebnis ist None, wenn mehr als hoechstens Aufrufe nötig waren.
    """
    original = globals()["zahlungsplaene"]
    aufrufe = 0

    def gezaehlt(*argumente, **benannte):
        """Zählt einen Aufruf und reicht ihn an die echte Funktion weiter."""
        nonlocal aufrufe
        aufrufe = aufrufe + 1
        if aufrufe > hoechstens:
            raise ZuVieleAufrufe()
        return original(*argumente, **benannte)

    globals()["zahlungsplaene"] = gezaehlt
    try:
        ergebnis = gezaehlt(monate)
    except ZuVieleAufrufe:
        ergebnis = None
    finally:
        globals()["zahlungsplaene"] = original
    return ergebnis, aufrufe


# Mit Merker: für 40 Monate genügen wenige Aufrufe (zuerst, bevor andere Tests etwas zwischenspeichern)
ergebnis, aufrufe = zaehle_aufrufe(40, 1000)
assert ergebnis == plaene_von_hand(40) and aufrufe <= 4 * 40, (
    f"zahlungsplaene(40) soll {plaene_von_hand(40)} ergeben und sich dabei höchstens etwa 2 · 40-mal aufrufen. "
    + (
        f"Nach 1000 Aufrufen war Ihre Funktion noch nicht fertig.\n"
        "Tipp: Schauen Sie vor dem Rechnen in merker nach, speichern Sie jedes Ergebnis in merker[monate] "
        "und reichen Sie merker bei jedem rekursiven Aufruf weiter."
        if ergebnis is None
        else f"Sie ergab {ergebnis!r} nach {aufrufe} Aufrufen."
    )
)

# Die Funktion ruft sich selbst auf (Rekursion statt Schleife)
assert aufrufe >= 2, (
    "zahlungsplaene(40) hat sich nicht selbst aufgerufen. Lösen Sie die Aufgabe rekursiv: "
    "Die Pläne für monate sind die für monate - 1 plus die für monate - 2."
)

# Die Beispiele aus der Aufgabe
for monate, erwartet in [(3, 3), (4, 5), (60, 2504730781961)]:
    ergebnis = zahlungsplaene(monate)
    assert ergebnis == erwartet, f"zahlungsplaene({monate}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Die kleinsten Laufzeiten: 0 und 1 Monat haben je einen Plan, 2 Monate zwei
for monate, erwartet in [(0, 1), (1, 1), (2, 2)]:
    ergebnis = zahlungsplaene(monate)
    assert ergebnis == erwartet, (
        f"zahlungsplaene({monate}) ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Für 0 und für 1 Monat gibt es genau einen Plan; das sind die Fälle, in denen die Rekursion endet."
    )

# Ein leerer Merker von außen wird benutzt und gefüllt
merker = {}
ergebnis = zahlungsplaene(10, merker)
assert ergebnis == 89 and merker.get(10) == 89, (
    f"Nach merker = {{}} und zahlungsplaene(10, merker) ist das Ergebnis {ergebnis!r} und merker {merker!r}; "
    "erwartet waren 89 und ein Eintrag merker[10] == 89.\n"
    "Tipp: Speichern Sie jedes Ergebnis mit merker[monate] = ergebnis im übergebenen Dictionary."
)

# Ein schon gefüllter Merker wird gelesen statt neu gerechnet
merker = {30: 7}
ergebnis = zahlungsplaene(30, merker)
assert ergebnis == 7, (
    f"zahlungsplaene(30, {{30: 7}}) ergibt {ergebnis!r}, erwartet war 7, der Wert aus dem Merker.\n"
    "Tipp: Schauen Sie zuerst nach, ob monate schon in merker steht, und geben Sie dann diesen Wert zurück."
)

# Zwei Aufrufe nacheinander stören sich nicht
erstes = zahlungsplaene(25)
zweites = zahlungsplaene(25)
assert erstes == zweites == plaene_von_hand(25), (
    f"Zweimal zahlungsplaene(25) ergibt {erstes!r} und {zweites!r}, erwartet war beide Male {plaene_von_hand(25)}."
)

# Alle Laufzeiten von 0 bis 90
for monate in range(91):
    ergebnis = zahlungsplaene(monate)
    assert ergebnis == plaene_von_hand(monate), (
        f"zahlungsplaene({monate}) ergibt {ergebnis!r}, erwartet war {plaene_von_hand(monate)}."
    )

# Obere Grenze: 90 Monate mit wenigen Aufrufen
ergebnis, aufrufe = zaehle_aufrufe(90, 1000)
assert ergebnis == plaene_von_hand(90) and aufrufe <= 4 * 90, (
    f"zahlungsplaene(90) soll {plaene_von_hand(90)} ergeben und sich höchstens etwa 2 · 90-mal aufrufen; "
    + ("nach 1000 Aufrufen war sie noch nicht fertig." if ergebnis is None else f"sie ergab {ergebnis!r} nach {aufrufe} Aufrufen.")
)

# 100 zufällige Laufzeiten mit frischem Merker
zufall = Zufall(3033)
for _ in range(100):
    monate = zufall.randint(0, 90)
    ergebnis = zahlungsplaene(monate, {})
    assert ergebnis == plaene_von_hand(monate), (
        f"zahlungsplaene({monate}, {{}}) ergibt {ergebnis!r}, erwartet war {plaene_von_hand(monate)}."
    )

# Die Ausgabe des Programms stimmt
assert AUSGABE == "3\n89", f"Erwartete Ausgabe:\n3\n89\nIhr Programm gibt aus:\n{AUSGABE}"
