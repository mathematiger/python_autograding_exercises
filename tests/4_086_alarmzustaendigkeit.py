# Automatisch erzeugt aus lehrkraft/muster/4_086_alarmzustaendigkeit.py - nicht von Hand ändern.
# vorlage-hash: 4c4ff128a8b0b323
# text-hash: b1a55fedaca0d7bd
# thema: datenstrukturen
# inhalt: Trie, Präfixsuche, längstes Präfix

REGELN = {"web": "Team Web", "db": "Team Datenbank", "db-muc-prod": "Bereitschaft München"}


def von_hand(paare):
    """Baut einen Trie ohne die Methoden der SuS."""
    trie = Trie()
    for schluessel, wert in paare.items():
        knoten = trie.wurzel
        for zeichen in schluessel:
            knoten = knoten.kinder.setdefault(zeichen, Knoten())
        knoten.wert = wert
    trie.anzahl = len(paare)
    return trie


def ablesen(trie):
    """Liest alle Schlüssel mit Werten aus dem Baum, ohne die Methoden der SuS."""
    paare = {}
    offen = [(trie.wurzel, "")]
    while offen:
        knoten, weg = offen.pop()
        if knoten.wert is not None:
            paare[weg] = knoten.wert
        for zeichen, kind in knoten.kinder.items():
            offen.append((kind, weg + zeichen))
    return paare


def rufe(aufruf):
    """Führt aufruf() aus; liefert (Ergebnis, Fehlertext oder None)."""
    try:
        return aufruf(), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


def absturz(fehler):
    """Ergänzt eine Meldung um den Fehlertext, falls es einen gab."""
    return f"\nDer Aufruf löst {fehler} aus." if fehler else ""


def vergleich_laengstes(paare, text):
    """Vergleichslösung: probiert alle Schlüssel durch."""
    passend = [schluessel for schluessel in paare if text.startswith(schluessel)]
    if not passend:
        return None
    bester = max(passend, key=len)
    return (bester, paare[bester])


ZEICHEN = "abcdeh-.019"


def zufallsname(zufall, laenge):
    """Ein zufälliger Name aus wenigen Zeichen, damit sich viele Anfänge teilen."""
    return "".join(zufall.choice(ZEICHEN) for _ in range(laenge))


# einfuegen: ein Schlüssel landet im Baum, Zeichen für Zeichen
trie = Trie()
_, fehler = rufe(lambda: trie.einfuegen("web", "Team Web"))
assert ablesen(trie) == {"web": "Team Web"} and list(trie.wurzel.kinder) == ["w"], (
    f"Nach einfuegen('web', 'Team Web') stehen im Baum {ablesen(trie)!r}, die Wurzel hat die Kinder "
    f"{list(trie.wurzel.kinder)!r}; erwartet war {{'web': 'Team Web'}} und ein Kind 'w'." + absturz(fehler)
    + "\nTipp: Gehen Sie von self.wurzel Zeichen für Zeichen nach unten, legen Sie fehlende Kinder an und setzen Sie "
    "am letzten Knoten den Wert."
)

# einfuegen: das Beispiel, gemeinsame Anfänge teilen sich den Weg
trie = Trie()
_, fehler = rufe(lambda: [trie.einfuegen(schluessel, wert) for schluessel, wert in REGELN.items()])
assert ablesen(trie) == REGELN and sorted(trie.wurzel.kinder) == ["d", "w"], (
    f"Nach dem Einfügen der drei Regeln stehen im Baum {ablesen(trie)!r} und die Wurzel hat die Kinder "
    f"{sorted(trie.wurzel.kinder)!r}; erwartet war {REGELN!r} und die Kinder ['d', 'w']." + absturz(fehler)
)

# einfuegen: Zwischenknoten tragen keinen Wert
trie = Trie()
rufe(lambda: [trie.einfuegen(schluessel, wert) for schluessel, wert in REGELN.items()])
zwischen = trie.wurzel.kinder.get("d")
assert zwischen is not None and zwischen.wert is None, (
    f"Der Knoten nach 'd' hat den Wert {getattr(zwischen, 'wert', None)!r}, erwartet war None: 'd' ist kein Schlüssel."
)

# einfuegen: ein vorhandener Schlüssel bekommt einen neuen Wert
trie = von_hand(REGELN)
_, fehler = rufe(lambda: trie.einfuegen("db", "Team Daten"))
erwartet = dict(REGELN, db="Team Daten")
assert ablesen(trie) == erwartet and trie.anzahl == 3, (
    f"Nach einfuegen('db', 'Team Daten') stehen im Baum {ablesen(trie)!r} mit anzahl {trie.anzahl!r}; erwartet war "
    f"{erwartet!r} mit anzahl 3.\nTipp: Erhöhen Sie anzahl nur, wenn der Knoten vorher keinen Wert hatte." + absturz(fehler)
)

# __len__: die Anzahl der Schlüssel
trie = Trie()
rufe(lambda: [trie.einfuegen(schluessel, wert) for schluessel, wert in REGELN.items()])
ergebnis, fehler = rufe(lambda: (len(trie), len(Trie())))
assert ergebnis == (3, 0), f"len() ergibt nach drei Regeln und für einen leeren Trie {ergebnis!r}, erwartet war (3, 0)." + absturz(fehler)

# __len__: ein Schlüssel, der Anfang eines anderen ist, zählt extra
trie = Trie()
rufe(lambda: (trie.einfuegen("db-muc", "A"), trie.einfuegen("db", "B"), trie.einfuegen("db-muc", "C")))
ergebnis, fehler = rufe(lambda: len(trie))
assert ergebnis == 2, (
    f"Nach einfuegen('db-muc', …), einfuegen('db', …) und noch einmal einfuegen('db-muc', …) ergibt len() "
    f"{ergebnis!r}, erwartet war 2." + absturz(fehler)
)

# nachschlagen: das Beispiel
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: (trie.nachschlagen("db"), trie.nachschlagen("db-muc-prod"), trie.nachschlagen("web")))
assert ergebnis == ("Team Datenbank", "Bereitschaft München", "Team Web"), (
    f"nachschlagen für 'db', 'db-muc-prod' und 'web' ergibt {ergebnis!r}, erwartet war "
    "('Team Datenbank', 'Bereitschaft München', 'Team Web')." + absturz(fehler)
)

# nachschlagen: ein Anfang, der kein Schlüssel ist, ergibt None
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.nachschlagen("db-muc"))
assert fehler is None and ergebnis is None, f"nachschlagen('db-muc') ergibt {ergebnis!r}, erwartet war None." + absturz(fehler)

# nachschlagen: ein unbekannter Weg ergibt None
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: (trie.nachschlagen("mail"), trie.nachschlagen("webserver")))
assert fehler is None and ergebnis == (None, None), (
    f"nachschlagen('mail') und nachschlagen('webserver') ergeben {ergebnis!r}, erwartet war (None, None)."
    + absturz(fehler) + "\nTipp: Fehlt unterwegs ein Kind, gibt es den Schlüssel nicht; kinder.get(zeichen) liefert dann None."
)

# laengstes_praefix: das Beispiel, die längste Regel gewinnt
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.laengstes_praefix("db-muc-prod-12"))
assert ergebnis == ("db-muc-prod", "Bereitschaft München"), (
    f"laengstes_praefix('db-muc-prod-12') ergibt {ergebnis!r}, erwartet war ('db-muc-prod', 'Bereitschaft München')."
    + absturz(fehler)
    + "\nTipp: Laufen Sie den Text entlang und merken Sie sich bei jedem Knoten mit Wert das Paar; hören Sie erst auf, "
    "wenn es kein passendes Kind mehr gibt."
)

# laengstes_praefix: der Weg geht weiter, aber nur die kürzere Regel passt
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.laengstes_praefix("db-muc-test-01"))
assert ergebnis == ("db", "Team Datenbank"), (
    f"laengstes_praefix('db-muc-test-01') ergibt {ergebnis!r}, erwartet war ('db', 'Team Datenbank').\n"
    "Tipp: Merken Sie sich den letzten Knoten mit Wert, nicht den letzten erreichten Knoten." + absturz(fehler)
)

# laengstes_praefix: ein anderer Server (nicht fest hinschreiben!)
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.laengstes_praefix("web-fra-03"))
assert ergebnis == ("web", "Team Web"), f"laengstes_praefix('web-fra-03') ergibt {ergebnis!r}, erwartet war ('web', 'Team Web')." + absturz(fehler)

# laengstes_praefix: der Text ist selbst ein Schlüssel
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.laengstes_praefix("db"))
assert ergebnis == ("db", "Team Datenbank"), f"laengstes_praefix('db') ergibt {ergebnis!r}, erwartet war ('db', 'Team Datenbank')." + absturz(fehler)

# laengstes_praefix: keine Regel passt
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: (trie.laengstes_praefix("mail-01"), trie.laengstes_praefix("d"), Trie().laengstes_praefix("db")))
assert fehler is None and ergebnis == (None, None, None), (
    f"laengstes_praefix('mail-01'), laengstes_praefix('d') und für einen leeren Trie ergeben {ergebnis!r}, erwartet "
    "war (None, None, None): 'd' ist nur der Anfang einer Regel, keine Regel." + absturz(fehler)
)

# mit_praefix: das Beispiel
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.mit_praefix("d"))
assert ergebnis == ["db", "db-muc-prod"], (
    f"mit_praefix('d') ergibt {ergebnis!r}, erwartet war ['db', 'db-muc-prod'].\n"
    "Tipp: Gehen Sie bis zum Knoten des Präfixes und sammeln Sie darunter alle Knoten mit Wert; tragen Sie dabei den "
    "Weg als Text mit." + absturz(fehler)
)

# mit_praefix: der Präfix selbst gehört dazu, wenn er ein Schlüssel ist
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.mit_praefix("db"))
assert ergebnis == ["db", "db-muc-prod"], f"mit_praefix('db') ergibt {ergebnis!r}, erwartet war ['db', 'db-muc-prod']." + absturz(fehler)

# mit_praefix: alphabetisch sortiert
namen = {"web-fra-03": "x", "web-ber-01": "x", "web-fra-01": "x", "web-ham-07": "x", "db-muc-01": "x"}
trie = von_hand(namen)
ergebnis, fehler = rufe(lambda: trie.mit_praefix("web-"))
erwartet = ["web-ber-01", "web-fra-01", "web-fra-03", "web-ham-07"]
assert ergebnis == erwartet, f"mit_praefix('web-') ergibt {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)

# mit_praefix: leerer Präfix liefert alle Schlüssel
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: trie.mit_praefix(""))
assert ergebnis == ["db", "db-muc-prod", "web"], f"mit_praefix('') ergibt {ergebnis!r}, erwartet war ['db', 'db-muc-prod', 'web']." + absturz(fehler)

# mit_praefix: nichts passt
trie = von_hand(REGELN)
ergebnis, fehler = rufe(lambda: (trie.mit_praefix("mail"), trie.mit_praefix("dbx"), Trie().mit_praefix("")))
assert ergebnis == ([], [], []), f"mit_praefix('mail'), mit_praefix('dbx') und für einen leeren Trie ergeben {ergebnis!r}, erwartet war ([], [], [])." + absturz(fehler)

zufall = Zufall(4086)

# Viele zufällige Tries im Vergleich mit einem Dictionary
for _ in range(80):
    paare = {}
    trie = Trie()
    for _ in range(zufall.randint(0, 25)):
        schluessel, wert = zufallsname(zufall, zufall.randint(1, 6)), f"Team {zufall.randint(1, 9)}"
        paare[schluessel] = wert
        _, fehler = rufe(lambda: trie.einfuegen(schluessel, wert))
    text = zufallsname(zufall, zufall.randint(1, 8))
    if paare and zufall.random() < 0.5:
        text = zufall.choice(list(paare)) + text
    praefix = zufallsname(zufall, zufall.randint(0, 2))
    ergebnis, fehler = rufe(lambda: (len(trie), trie.nachschlagen(text[:3]), trie.laengstes_praefix(text), trie.mit_praefix(praefix)))
    erwartet = (
        len(paare), paare.get(text[:3]), vergleich_laengstes(paare, text),
        sorted(schluessel for schluessel in paare if schluessel.startswith(praefix)),
    )
    assert ergebnis == erwartet, (
        f"Mit den Schlüsseln {paare!r} ergeben len(), nachschlagen({text[:3]!r}), laengstes_praefix({text!r}) und "
        f"mit_praefix({praefix!r})\n{ergebnis!r},\nerwartet war\n{erwartet!r}." + absturz(fehler)
    )

# Laufzeit: laengstes_praefix hängt nicht von der Zahl der Schlüssel ab
klein = von_hand({f"srv-{nummer:05d}": "Team" for nummer in range(1000)})
gross = von_hand({f"srv-{nummer:05d}": "Team" for nummer in range(40_000)})
_, schritte_klein = zaehle_schritte(klein.laengstes_praefix, "srv-00999-x")
ergebnis, schritte_gross = zaehle_schritte(gross.laengstes_praefix, "srv-00999-x")
assert ergebnis == ("srv-00999", "Team") and schritte_gross <= schritte_klein + 20 and schritte_gross <= 200, (
    f"laengstes_praefix('srv-00999-x') ergibt {ergebnis!r} (erwartet ('srv-00999', 'Team')) und braucht bei 1000 Schlüsseln {schritte_klein} Schritte, bei 40000 "
    f"{schritte_gross}; erwartet war bei beiden etwa gleich viel (O(L)).\nTipp: Gehen Sie nicht alle Schlüssel durch, "
    "sondern laufen Sie den Text im Baum entlang."
)

# Laufzeit: nachschlagen hängt nicht von der Zahl der Schlüssel ab
_, schritte_klein = zaehle_schritte(klein.nachschlagen, "srv-00999")
ergebnis, schritte_gross = zaehle_schritte(gross.nachschlagen, "srv-00999")
assert ergebnis == "Team" and schritte_gross <= schritte_klein + 20 and schritte_gross <= 200, (
    f"nachschlagen('srv-00999') ergibt {ergebnis!r} (erwartet 'Team') und braucht bei 1000 Schlüsseln {schritte_klein} Schritte, bei 40000 {schritte_gross}; "
    "erwartet war bei beiden etwa gleich viel (O(L))."
)

# Laufzeit: mit_praefix sieht nur den passenden Teilbaum an
ergebnis, schritte = zaehle_schritte(gross.mit_praefix, "srv-0099")
assert ergebnis == [f"srv-{nummer:05d}" for nummer in range(990, 1000)] and schritte <= 1000, (
    f"mit_praefix('srv-0099') bei 40000 Schlüsseln ergibt {str(ergebnis)[:80]} mit {schritte} Schritten; erwartet "
    "waren die zehn Schlüssel srv-00990 bis srv-00999 mit höchstens 1000 Schritten.\nTipp: Gehen Sie erst bis zum "
    "Knoten des Präfixes und sammeln Sie nur darunter."
)

# Obere Grenze: 100000 Schlüssel mit bis zu 60 Zeichen
trie = Trie()
schluessel_liste = [f"host-{nummer:06d}-" + "x" * (nummer % 49) for nummer in range(100_000)]


def gross_einfuegen():
    """Fügt 100000 Schlüssel ein und fragt danach."""
    for nummer, schluessel in enumerate(schluessel_liste):
        trie.einfuegen(schluessel, f"Team {nummer % 10}")
    return len(trie), trie.laengstes_praefix(schluessel_liste[-1] + "-a"), len(trie.mit_praefix("host-09999"))


ergebnis, fehler = rufe(gross_einfuegen)
erwartet = (100_000, (schluessel_liste[-1], "Team 9"), 10)
assert ergebnis == erwartet, f"Mit 100000 Schlüsseln ergibt das {ergebnis!r}, erwartet war {erwartet!r}." + absturz(fehler)
