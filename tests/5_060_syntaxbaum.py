# Automatisch erzeugt aus lehrkraft/muster/5_060_syntaxbaum.py - nicht von Hand ändern.
# vorlage-hash: 1f55033912a52eab
# text-hash: baac6032aad6e4d9
# thema: algorithmen
# inhalt: Aufrufstapel, Rekursion als Schleife

KINDER = {"modul": ["def f", "def g"], "def f": ["return"], "return": ["a + b"], "def g": ["pass"]}
ZEICHEN = {"modul": 0, "def f": 8, "return": 7, "a + b": 5, "def g": 8, "pass": 4}
REIHENFOLGE = ["modul", "def f", "return", "a + b", "def g", "pass"]
GROESSEN = {"modul": 32, "def f": 20, "return": 12, "a + b": 5, "def g": 12, "pass": 4}
LIMIT = sys.getrecursionlimit()


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    if fehler and fehler.startswith("RecursionError"):
        return (
            "\nDer Aufruf löst RecursionError aus: Ihre Funktion ruft sich selbst (oder eine rekursive Hilfsfunktion) "
            "auf. Verwalten Sie stattdessen einen eigenen Stapel in einer while-Schleife."
        )
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def kette(laenge):
    """Ein Baum, der nur aus einer Kette K0 → K1 → … besteht, mit laenge Ebenen."""
    return {f"K{nummer}": [f"K{nummer + 1}"] for nummer in range(laenge - 1)}


def zufallsbaum(zufall, anzahl):
    """Ein zufälliger Baum mit anzahl Knoten; liefert (kinder, zeichen)."""
    kinder = {}
    for nummer in range(1, anzahl):
        eltern = f"N{zufall.randrange(max(0, nummer - 4), nummer)}"
        kinder.setdefault(eltern, []).append(f"N{nummer}")
    zeichen = {f"N{nummer}": zufall.randint(0, 1000) for nummer in range(anzahl)}
    return kinder, zeichen


# tiefe: ein Knoten ohne Kinder
ergebnis, fehler = rufe(lambda: tiefe("pass", {}))
assert ergebnis == 1, f"tiefe('pass', {{}}) ergibt {ergebnis!r}, erwartet war 1: ein Knoten ohne Kinder ist eine Ebene." + absturz(fehler)

# tiefe: das Beispiel
ergebnis, fehler = rufe(lambda: tiefe("modul", KINDER))
assert ergebnis == 4, (
    f"tiefe('modul', kinder) ergibt {ergebnis!r}, erwartet war 4 (modul, def f, return, a + b).\n"
    "Tipp: Legen Sie Paare (knoten, ebene) auf den Stapel und merken Sie sich die größte Ebene." + absturz(fehler)
)

# tiefe: der tiefste Zweig ist nicht der erste
kinder = {"w": ["a", "b", "c"], "c": ["c1"], "c1": ["c2"], "a": ["a1"]}
ergebnis, fehler = rufe(lambda: tiefe("w", kinder))
assert ergebnis == 4, f"tiefe('w', {kinder}) ergibt {ergebnis!r}, erwartet war 4." + absturz(fehler)

# tiefe: eine Kette tiefer als das Rekursionslimit
ergebnis, fehler = rufe(lambda: tiefe("K0", kette(5000)))
assert ergebnis == 5000, (
    f"tiefe für eine Kette mit 5000 Ebenen ergibt {ergebnis!r}, erwartet war 5000 (das Rekursionslimit ist {LIMIT})."
    + absturz(fehler)
)

# reihenfolge: ein Knoten ohne Kinder
ergebnis, fehler = rufe(lambda: reihenfolge("pass", {}))
assert ergebnis == ["pass"], f"reihenfolge('pass', {{}}) ergibt {ergebnis!r}, erwartet war ['pass']." + absturz(fehler)

# reihenfolge: alle Knoten, jeder vor seinen Kindern
ergebnis, fehler = rufe(lambda: reihenfolge("modul", KINDER))
assert ergebnis is not None and sorted(ergebnis) == sorted(REIHENFOLGE) and ergebnis[0] == "modul", (
    f"reihenfolge('modul', kinder) ergibt {ergebnis!r}; erwartet waren alle sechs Knoten, 'modul' zuerst."
    + absturz(fehler)
)

# reihenfolge: das Beispiel, in der Reihenfolge der Rekursion
ergebnis, fehler = rufe(lambda: reihenfolge("modul", KINDER))
assert ergebnis == REIHENFOLGE, (
    f"reihenfolge('modul', kinder) ergibt {ergebnis!r}, erwartet war {REIHENFOLGE!r}."
    + ("\nTipp: pop nimmt das zuletzt hingelegte Kind zuerst; legen Sie die Kinder mit reversed(...) auf den Stapel."
       if ergebnis and ergebnis[1:2] == ["def g"] else "")
    + absturz(fehler)
)

# reihenfolge: eine Kette tiefer als das Rekursionslimit
ergebnis, fehler = rufe(lambda: reihenfolge("K0", kette(5000)))
assert ergebnis == [f"K{nummer}" for nummer in range(5000)], (
    f"reihenfolge für eine Kette mit 5000 Ebenen ergibt {str(ergebnis)[:60]}, erwartet war ['K0', 'K1', …, 'K4999']."
    + absturz(fehler)
)

# teilbaumgroessen: ein Knoten ohne Kinder
ergebnis, fehler = rufe(lambda: teilbaumgroessen("pass", {}, {"pass": 4}))
assert ergebnis == {"pass": 4}, f"teilbaumgroessen('pass', {{}}, {{'pass': 4}}) ergibt {ergebnis!r}, erwartet war {{'pass': 4}}." + absturz(fehler)

# teilbaumgroessen: das Beispiel
ergebnis, fehler = rufe(lambda: teilbaumgroessen("modul", KINDER, ZEICHEN))
assert ergebnis == GROESSEN, (
    f"teilbaumgroessen('modul', kinder, zeichen) ergibt {ergebnis!r}, erwartet war {GROESSEN!r}.\n"
    "Tipp: Gehen Sie die Knoten aus reihenfolge rückwärts durch; dann sind die Kinder jedes Knotens schon fertig."
    + absturz(fehler)
)

# teilbaumgroessen: Knoten mit 0 Zeichen und eine Kette tiefer als das Rekursionslimit
kinder = kette(5000)
zeichen = {f"K{nummer}": nummer % 2 for nummer in range(5000)}
ergebnis, fehler = rufe(lambda: teilbaumgroessen("K0", kinder, zeichen))
assert ergebnis is not None and ergebnis.get("K0") == 2500 and ergebnis.get("K4999") == 1 and ergebnis.get("K4998") == 1, (
    f"teilbaumgroessen für eine Kette mit 5000 Ebenen ergibt für K0, K4998 und K4999 "
    f"{[ergebnis.get(k) for k in ('K0', 'K4998', 'K4999')] if ergebnis else None}, erwartet war [2500, 1, 1]."
    + absturz(fehler)
)

# rekursion_reicht: das Beispiel
ergebnis, fehler = rufe(lambda: rekursion_reicht("modul", KINDER))
assert ergebnis is True, f"rekursion_reicht('modul', kinder) ergibt {ergebnis!r}, erwartet war True." + absturz(fehler)

# rekursion_reicht: zu tief für das Rekursionslimit
ergebnis, fehler = rufe(lambda: rekursion_reicht("K0", kette(LIMIT)))
assert ergebnis is False, (
    f"rekursion_reicht für eine Kette mit {LIMIT} Ebenen (so viele wie das Rekursionslimit) ergibt {ergebnis!r}, "
    "erwartet war False.\nTipp: Vergleichen Sie tiefe(wurzel, kinder) + 50 mit sys.getrecursionlimit()." + absturz(fehler)
)

# rekursion_reicht: genau an der Grenze
ergebnis, fehler = rufe(lambda: (rekursion_reicht("K0", kette(LIMIT - 50)), rekursion_reicht("K0", kette(LIMIT - 49))))
assert ergebnis == (True, False), (
    f"rekursion_reicht für Ketten mit {LIMIT - 50} und {LIMIT - 49} Ebenen ergibt {ergebnis!r}, erwartet war "
    f"(True, False): {LIMIT - 50} + 50 ist höchstens {LIMIT}." + absturz(fehler)
)

# rekursion_reicht: stimmt mit den rekursiven Fassungen überein
kinder = kette(LIMIT - 50)
reicht, fehler = rufe(lambda: rekursion_reicht("K0", kinder))
klappt, _ = rufe(lambda: tiefe_rekursiv("K0", kinder))
assert reicht is True and klappt == LIMIT - 50, (
    f"Für eine Kette mit {LIMIT - 50} Ebenen ergibt rekursion_reicht {reicht!r} und tiefe_rekursiv {klappt!r}; erwartet "
    f"war True und {LIMIT - 50}." + absturz(fehler)
)

# Das Rekursionslimit bleibt unverändert
assert not verwendet("setrecursionlimit") and sys.getrecursionlimit() == LIMIT, (
    "Ihr Programm ruft sys.setrecursionlimit auf. Ein höheres Limit verschiebt das Problem nur und ist keine "
    "verlässliche Lösung (siehe Hintergrund). Verwalten Sie einen eigenen Stapel."
)

zufall = Zufall(5060)

# Viele zufällige Bäume im Vergleich mit den rekursiven Fassungen
for _ in range(100):
    kinder, zeichen = zufallsbaum(zufall, zufall.randint(1, 40))
    ergebnis, fehler = rufe(lambda: (tiefe("N0", kinder), reihenfolge("N0", kinder), teilbaumgroessen("N0", kinder, zeichen)))
    erwartet = (tiefe_rekursiv("N0", kinder), reihenfolge_rekursiv("N0", kinder), teilbaumgroessen_rekursiv("N0", kinder, zeichen))
    assert ergebnis == erwartet, (
        f"Für den Baum {kinder} mit zeichen {zeichen} ergeben tiefe, reihenfolge und teilbaumgroessen\n{ergebnis!r},"
        f"\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )


def viele_knoten(anzahl):
    """Baut einen breiten, flachen Baum mit anzahl Knoten und ruft alle vier Funktionen auf."""
    kinder = {f"N{nummer}": [f"N{2 * nummer + 1}", f"N{2 * nummer + 2}"] for nummer in range((anzahl - 1) // 2)}
    zeichen = {f"N{nummer}": 1 for nummer in range(anzahl)}
    return tiefe("N0", kinder), len(reihenfolge("N0", kinder)), teilbaumgroessen("N0", kinder, zeichen)["N0"], rekursion_reicht("N0", kinder)


# Laufzeit: O(n) Schritte
_, schritte_klein = zaehle_schritte(viele_knoten, 1001)
ergebnis, schritte_gross = zaehle_schritte(viele_knoten, 4001)
assert ergebnis == (12, 4001, 4001, True) and schritte_gross <= 5 * schritte_klein + 100, (
    f"Für 1001 Knoten brauchen die vier Funktionen {schritte_klein} Schritte, für 4001 {schritte_gross} und ergeben "
    f"{ergebnis!r}; erwartet war (12, 4001, 4001, True) und etwa das Vierfache an Schritten (O(n)).\nTipp: Bauen Sie "
    "keine Listen mit + zusammen und suchen Sie nicht mit in in Listen."
)

# Obere Grenze: eine Kette mit 200000 Ebenen
kinder = kette(200_000)
zeichen = {f"K{nummer}": 3 for nummer in range(200_000)}
ergebnis, fehler = rufe(
    lambda: (tiefe("K0", kinder), len(reihenfolge("K0", kinder)), teilbaumgroessen("K0", kinder, zeichen)["K0"], rekursion_reicht("K0", kinder))
)
assert ergebnis == (200_000, 200_000, 600_000, False), (
    f"Für eine Kette mit 200000 Ebenen ergeben tiefe, len(reihenfolge), teilbaumgroessen['K0'] und rekursion_reicht "
    f"{ergebnis!r}, erwartet war (200000, 200000, 600000, False)." + absturz(fehler)
)
