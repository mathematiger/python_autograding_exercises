# Automatisch erzeugt aus lehrkraft/muster/4_027_befehlsvorschlag.py - nicht von Hand ändern.
# vorlage-hash: 96c568c7a769b1ae
# text-hash: 1268877b32e09148
# thema: algorithmen
# inhalt: Editierdistanz mit Tabelle

# editierdistanz aus dem Beispiel
ergebnisse = [editierdistanz(a, b) for a, b in [("tset", "test"), ("biuld", "build"), ("deploy", "deplo"), ("", "test")]]
assert ergebnisse == [2, 2, 1, 4], (
    f"editierdistanz für (tset, test), (biuld, build), (deploy, deplo) und ('', test) ergibt {ergebnisse}, "
    "erwartet war [2, 2, 1, 4].\nTipp: Füllen Sie zuerst die erste Zeile und Spalte mit 0, 1, 2, … und dann jedes "
    "Feld aus seinen drei Nachbarn links, oben und links oben."
)

# Gleiche Texte haben Distanz 0, zwei leere auch
ergebnis = (editierdistanz("deploy", "deploy"), editierdistanz("", ""))
assert ergebnis == (0, 0), f'editierdistanz("deploy", "deploy") und editierdistanz("", "") ergeben {ergebnis!r}, erwartet war (0, 0).'

# Löschen, Einfügen und Ersetzen sind gleich teuer, in beide Richtungen
ergebnis = (editierdistanz("test", ""), editierdistanz("lint", "flint"), editierdistanz("lint", "list"),
            editierdistanz("flint", "lint"))
assert ergebnis == (4, 1, 1, 1), (
    f'editierdistanz für (test, ""), (lint, flint), (lint, list) und (flint, lint) ergibt {ergebnis!r}, '
    "erwartet war (4, 1, 1, 1)."
)

# Groß- und Kleinschreibung zählt
ergebnis = editierdistanz("Build", "build")
assert ergebnis == 1, f'editierdistanz("Build", "build") ergibt {ergebnis!r}, erwartet war 1.'

# Ein Fall, in dem gieriges Vergleichen Stelle für Stelle zu viel zählt
ergebnis = (editierdistanz("kitten", "sitting"), editierdistanz("abcdef", "bcdefa"), editierdistanz("ab", "b"))
assert ergebnis == (3, 2, 1), (
    f'editierdistanz für (kitten, sitting), (abcdef, bcdefa) und (ab, b) ergibt {ergebnis!r}, erwartet war (3, 2, 1).\n'
    "Tipp: Wer nur Stelle für Stelle vergleicht, übersieht, dass ein Löschen vorn alle folgenden Zeichen passend "
    "verschiebt; nehmen Sie das Minimum der drei Nachbarfelder."
)

# vorschlaege aus dem Beispiel
ergebnis = vorschlaege("tset", ["build", "test", "reset", "deploy"])
assert ergebnis == ["reset", "test"], (
    f'vorschlaege("tset", ["build", "test", "reset", "deploy"]) ergibt {ergebnis!r}, erwartet war ["reset", "test"].\n'
    "Tipp: Bei gleicher Distanz alphabetisch, zum Beispiel mit sorted über Tupel (distanz, befehl)."
)

# vorschlaege mit hoechstens=1
ergebnis = vorschlaege("bild", ["build", "bind", "lint"], hoechstens=1)
assert ergebnis == ["bind", "build"], f'vorschlaege("bild", ["build", "bind", "lint"], hoechstens=1) ergibt {ergebnis!r}, erwartet war ["bind", "build"].'

# Die Distanz ordnet vor dem Alphabet, die Eingabe selbst kommt zuerst
ergebnis = vorschlaege("test", ["zest", "tests", "test", "atest", "best", "toast"])
erwartet = ["test", "atest", "best", "tests", "zest", "toast"]
assert ergebnis == erwartet, (
    f'vorschlaege("test", ["zest", "tests", "test", "atest", "best", "toast"]) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Zuerst nach Distanz, erst bei gleicher Distanz alphabetisch."
)

# Ränder: hoechstens 0, keine Befehle, keine Treffer, leere Eingabe
ergebnis = (vorschlaege("tset", ["test"], hoechstens=0), vorschlaege("test", ["test", "tests"], hoechstens=0),
            vorschlaege("x", []), vorschlaege("", ["ab", "a", "abc"]))
erwartet = ([], ["test"], [], ["a", "ab"])
assert ergebnis == erwartet, (
    f"vorschlaege mit hoechstens 0, ohne Befehle und mit leerer Eingabe ergibt {ergebnis!r}, erwartet war {erwartet!r}."
)

# befehle bleibt unverändert
befehle = ["test", "build", "deploy"]
vorschlaege("tes", befehle)
assert befehle == ["test", "build", "deploy"], f"Nach vorschlaege ist befehle {befehle!r}, erwartet war unverändert."


# Vergleichslösung: rekursiv mit Cache über die Reste der Wörter (anders als die Tabelle)
def distanz_von_hand(a, b):
    """Rechnet die Editierdistanz von vorn über die Reste a[i:] und b[j:], mit eigenem Cache."""
    gemerkt = {}

    def rest(i, j):
        """Distanz zwischen a[i:] und b[j:]."""
        if (i, j) in gemerkt:
            return gemerkt[(i, j)]
        if i == len(a) or j == len(b):
            ergebnis = (len(a) - i) + (len(b) - j)
        elif a[i] == b[j]:
            ergebnis = rest(i + 1, j + 1)
        else:
            ergebnis = 1 + min(rest(i + 1, j), rest(i, j + 1), rest(i + 1, j + 1))
        gemerkt[(i, j)] = ergebnis
        return ergebnis

    return rest(0, 0)


def distanz_zwei_zeilen(a, b):
    """Rechnet die Editierdistanz ohne Rekursion und hebt dabei nur die vorige Zeile auf."""
    vorige = list(range(len(b) + 1))
    for zeichen in a:
        aktuelle = [vorige[0] + 1]
        for spalte in range(1, len(b) + 1):
            kosten = 0 if b[spalte - 1] == zeichen else 1
            aktuelle.append(min(vorige[spalte] + 1, aktuelle[-1] + 1, vorige[spalte - 1] + kosten))
        vorige = aktuelle
    return vorige[-1]


# 300 zufällige Wortpaare aus wenigen Buchstaben, damit viele Teile übereinstimmen
zufall = Zufall(4027)
for _ in range(300):
    a = "".join(zufall.choice("abcA") for _ in range(zufall.randint(0, 8)))
    b = "".join(zufall.choice("abcA") for _ in range(zufall.randint(0, 8)))
    ergebnis = editierdistanz(a, b)
    erwartet = distanz_von_hand(a, b)
    assert ergebnis == erwartet, f"editierdistanz({a!r}, {b!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# 100 zufällige Vorschlagslisten
for _ in range(100):
    befehle = sorted(set("".join(zufall.choice("abt") for _ in range(zufall.randint(0, 5))) for _ in range(zufall.randint(0, 8))))
    zufall.shuffle(befehle)
    eingabe = "".join(zufall.choice("abt") for _ in range(zufall.randint(0, 5)))
    hoechstens = zufall.randint(0, 4)
    ergebnis = vorschlaege(eingabe, list(befehle), hoechstens=hoechstens)
    paare = [(distanz_von_hand(eingabe, befehl), befehl) for befehl in befehle]
    erwartet = [befehl for abstand, befehl in sorted(paare) if abstand <= hoechstens]
    assert ergebnis == erwartet, (
        f"vorschlaege({eingabe!r}, {befehle}, hoechstens={hoechstens}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    )

# Laufzeit: zwei Wörter mit 12 Zeichen ohne gemeinsame Buchstaben
ergebnis, schritte = zaehle_schritte(editierdistanz, "abcdefghijkl", "mnopqrstuvwx")
assert ergebnis == 12 and schritte < 2000, (
    f"editierdistanz mit zweimal 12 Zeichen braucht {schritte} Schritte (Ergebnis {ergebnis!r}, erwartet 12); "
    "erwartet war O(len(a) · len(b)), hier also weit unter 2000.\n"
    "Tipp: Ohne Tabelle rechnet die Rekursion dieselben Teilprobleme immer wieder; füllen Sie eine Tabelle "
    "Zeile für Zeile."
)

# Laufzeit wächst mit dem Produkt der Längen: doppelte Länge, etwa vierfache Schritte
_, schritte_klein = zaehle_schritte(editierdistanz, "ab" * 10, "ba" * 10)
_, schritte_gross = zaehle_schritte(editierdistanz, "ab" * 20, "ba" * 20)
assert schritte_gross < 6 * schritte_klein, (
    f"editierdistanz braucht bei 20 Zeichen {schritte_klein} und bei 40 Zeichen {schritte_gross} Schritte; bei "
    "O(len(a) · len(b)) wären es etwa viermal so viele, nicht mehr als sechsmal."
)

# Obere Grenze: zwei Texte mit 500 Zeichen
a = "".join("acgt"[(nummer * 7) % 4] for nummer in range(500))
b = "".join("acgt"[(nummer * nummer) % 4] for nummer in range(500))
ergebnis = editierdistanz(a, b)
erwartet = distanz_zwei_zeilen(a, b)
assert ergebnis == erwartet, f"editierdistanz zweier Texte mit 500 Zeichen ergibt {ergebnis!r}, erwartet war {erwartet}."

# Obere Grenze: 200 Befehle mit 30 Zeichen
befehle = [f"{nummer:03d}" + "x" * 27 for nummer in range(200)]
ergebnis = vorschlaege("000" + "x" * 27, befehle, hoechstens=1)
erwartet = [befehl for befehl in befehle if sum(1 for z, y in zip(befehl, "000") if z != y) <= 1]
assert ergebnis == erwartet, f"vorschlaege mit 200 Befehlen ergibt {ergebnis[:5]!r}…, erwartet war {erwartet[:5]!r}…"

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "2\n['reset', 'test']\n['bind', 'build']"
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
