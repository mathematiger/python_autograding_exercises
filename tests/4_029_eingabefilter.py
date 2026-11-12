# Automatisch erzeugt aus lehrkraft/muster/4_029_eingabefilter.py - nicht von Hand ändern.
# vorlage-hash: 9fdeb50c52dd731a
# text-hash: 652ef9cf2674d4ba
# thema: funktionen
# inhalt: functools.reduce

def xor_von_hand(daten):
    """Vergleichslösung mit einer Schleife."""
    ergebnis = 0
    for byte in daten:
        ergebnis = ergebnis ^ byte
    return ergebnis


def rechte_von_hand(rollen):
    """Vergleichslösung: jedes Recht einzeln einsammeln."""
    ergebnis = set()
    for rolle in rollen:
        for recht in rolle:
            ergebnis.add(recht)
    return ergebnis


def rufe_auf(funktion, *argumente):
    """Ruft funktion(*argumente) auf; liefert das Ergebnis oder eine Beschreibung des Abbruchs."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"


# Das Beispiel zu pruefsumme
ergebnis = rufe_auf(pruefsumme, b"\x0f\xf0\x01")
assert ergebnis == 254, f'pruefsumme(b"\\x0f\\xf0\\x01") ergibt {ergebnis!r}, erwartet war 254 (0x0f ^ 0xf0 ^ 0x01).'

# Leere Daten haben die Prüfsumme 0
ergebnis = rufe_auf(pruefsumme, b"")
assert ergebnis == 0, (
    f'pruefsumme(b"") ergibt {ergebnis!r}, erwartet war 0.\n'
    "Tipp: Geben Sie reduce einen Startwert mit: reduce(operator.xor, daten, 0)."
)

# Ein einzelnes Byte ist seine eigene Prüfsumme; zwei gleiche heben sich auf
for daten, erwartet in [(b"A", 65), (b"AA", 0), (b"\xff", 255), (bytes([1, 2, 4, 8]), 15)]:
    ergebnis = rufe_auf(pruefsumme, daten)
    assert ergebnis == erwartet, f"pruefsumme({daten!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ein verändertes Bit ändert die Prüfsumme
original = b"Kontostand: 1000"
verfaelscht = b"Kontostand: 9000"
assert pruefsumme(original) != pruefsumme(verfaelscht), (
    f"pruefsumme({original!r}) und pruefsumme({verfaelscht!r}) ergeben beide {pruefsumme(original)!r}; "
    "die Prüfsumme soll alle Bytes mit XOR verknüpfen."
)

# Das Beispiel zu alle_rechte
ergebnis = rufe_auf(alle_rechte, [{"lesen"}, {"lesen", "schreiben"}])
assert ergebnis == {"lesen", "schreiben"}, (
    f'alle_rechte([{{"lesen"}}, {{"lesen", "schreiben"}}]) ergibt {ergebnis!r}, erwartet war {{"lesen", "schreiben"}}.'
)

# Ohne Rollen gibt es keine Rechte
ergebnis = rufe_auf(alle_rechte, [])
assert ergebnis == set(), (
    f"alle_rechte([]) ergibt {ergebnis!r}, erwartet war set().\n"
    "Tipp: Ohne Startwert bricht reduce bei einer leeren Liste ab; geben Sie set() als Startwert mit."
)

# Eine Rolle, leere Rollen, viele Rollen
for rollen in [[{"admin"}], [set(), set()], [{"a"}, set(), {"b", "c"}, {"a", "d"}]]:
    ergebnis = rufe_auf(alle_rechte, rollen)
    erwartet = rechte_von_hand(rollen)
    assert ergebnis == erwartet, f"alle_rechte({rollen!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Die übergebenen Rollen bleiben unverändert, auch die erste
rollen = [{"lesen"}, {"schreiben"}, {"loeschen"}]
ergebnis = rufe_auf(alle_rechte, rollen)
assert rollen == [{"lesen"}, {"schreiben"}, {"loeschen"}], (
    f"Nach alle_rechte([{{'lesen'}}, {{'schreiben'}}, {{'loeschen'}}]) sind die Rollen {rollen!r}; "
    "sie sollen unverändert bleiben.\n"
    "Tipp: Fangen Sie mit einer neuen leeren Menge set() an und verknüpfen Sie mit | statt mit |=."
)

# Das Ergebnis ist eine neue Menge: sie zu ändern, ändert keine Rolle
rollen = [{"lesen"}]
ergebnis = rufe_auf(alle_rechte, rollen)
ergebnis.add("alles")
assert rollen == [{"lesen"}], (
    "Nach rechte = alle_rechte([{'lesen'}]) und rechte.add('alles') ist die Rolle "
    f"{rollen[0]!r}; sie soll {{'lesen'}} bleiben.\nTipp: Geben Sie eine neue Menge zurück, nicht die erste Rolle selbst."
)

# Das Beispiel zu bereinige
schritte = [str.strip, entferne_spitze_klammern, str.lower]
ergebnis = rufe_auf(bereinige, "  <b>Admin</b> ", schritte)
assert ergebnis == "badmin/b", (
    f'bereinige("  <b>Admin</b> ", [str.strip, entferne_spitze_klammern, str.lower]) ergibt {ergebnis!r}, '
    'erwartet war "badmin/b".'
)

# Ohne Schritte bleibt der Text unverändert
ergebnis = rufe_auf(bereinige, " Hallo ", [])
assert ergebnis == " Hallo ", (
    f'bereinige(" Hallo ", []) ergibt {ergebnis!r}, erwartet war " Hallo ".\n'
    "Tipp: Der Text selbst ist der Startwert von reduce."
)

# Die Reihenfolge der Schritte zählt: der erste zuerst
schritte = [lambda t: t + "!", lambda t: t * 2]
ergebnis = rufe_auf(bereinige, "ab", schritte)
assert ergebnis == "ab!ab!", (
    f'bereinige("ab", [lambda t: t + "!", lambda t: t * 2]) ergibt {ergebnis!r}, erwartet war "ab!ab!".\n'
    "Tipp: Wenden Sie den ersten Schritt zuerst an und jeden weiteren auf das Ergebnis des vorigen."
)

# Ein einzelner Schritt
ergebnis = rufe_auf(bereinige, "Admin'--", [lambda t: t.replace("'", "")])
assert ergebnis == "Admin--", f"bereinige(\"Admin'--\", [Hochkomma entfernen]) ergibt {ergebnis!r}, erwartet war 'Admin--'."

# reduce wird benutzt
assert verwendet("reduce"), "Benutzen Sie functools.reduce statt eigener Schleifen."

# Keine eigenen Schleifen
assert not verwendet("for") and not verwendet("while"), (
    "Ihr Code enthält eine for- oder while-Schleife. Lassen Sie reduce die Schleife übernehmen."
)

# 300 zufällige Nachrichten
zufall = Zufall(4029)
for _ in range(300):
    daten = bytes(zufall.randint(0, 255) for _ in range(zufall.randint(0, 40)))
    ergebnis = pruefsumme(daten)
    assert ergebnis == xor_von_hand(daten), f"pruefsumme({daten!r}) ergibt {ergebnis!r}, erwartet war {xor_von_hand(daten)}."

# 300 zufällige Konten
rechte = ["lesen", "schreiben", "loeschen", "admin", "export", "import"]
for _ in range(300):
    rollen = [set(zufall.sample(rechte, zufall.randint(0, 4))) for _ in range(zufall.randint(0, 5))]
    kopie = [set(rolle) for rolle in rollen]
    ergebnis = alle_rechte(rollen)
    assert ergebnis == rechte_von_hand(kopie) and rollen == kopie, (
        f"alle_rechte({kopie!r}) ergibt {ergebnis!r}, erwartet war {rechte_von_hand(kopie)!r}; "
        f"die Rollen sind danach {rollen!r}."
    )

# 300 zufällige Folgen von Schritten
bausteine = [str.strip, str.lower, str.upper, entferne_spitze_klammern, lambda t: t + "x", lambda t: t[1:]]
namen = ["strip", "lower", "upper", "klammern", "+x", "[1:]"]
for _ in range(300):
    auswahl = [zufall.randrange(len(bausteine)) for _ in range(zufall.randint(0, 6))]
    text = "".join(zufall.choice(" aB<>") for _ in range(zufall.randint(0, 8)))
    erwartet = text
    for nummer in auswahl:
        erwartet = bausteine[nummer](erwartet)
    ergebnis = bereinige(text, [bausteine[nummer] for nummer in auswahl])
    assert ergebnis == erwartet, (
        f"bereinige({text!r}, [{', '.join(namen[nummer] for nummer in auswahl)}]) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Obere Grenzen: 10**5 Bytes, 1000 Rollen mit je 50 Rechten, 20 Schritte
daten = bytes((zahl * 37) % 256 for zahl in range(10**5))
assert pruefsumme(daten) == xor_von_hand(daten), "Bei 10**5 Bytes stimmt die Prüfsumme nicht."
rollen = [{f"recht{(nummer * 7 + stelle) % 3000}" for stelle in range(50)} for nummer in range(1000)]
assert alle_rechte(rollen) == rechte_von_hand(rollen), "Bei 1000 Rollen mit je 50 Rechten stimmt die Vereinigung nicht."
ergebnis = bereinige("a" * 1000, [lambda t: t[1:]] * 20)
assert ergebnis == "a" * 980, f"Nach 20 Schritten, die je ein Zeichen abschneiden, hat der Text {len(ergebnis)} Zeichen, erwartet waren 980."

# Die Ausgabe des Programms stimmt
assert AUSGABE == "254\n['lesen', 'schreiben']\nbadmin/b", (
    f"Erwartete Ausgabe:\n254\n['lesen', 'schreiben']\nbadmin/b\nIhr Programm gibt aus:\n{AUSGABE}"
)
