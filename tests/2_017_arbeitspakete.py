# Automatisch erzeugt aus lehrkraft/muster/2_017_arbeitspakete.py - nicht von Hand ändern.
# vorlage-hash: 858f9e7f933af908
# text-hash: 3f71739247687b3a
# thema: texte_zahlen
# inhalt: Übung: Zeilen zerlegen, Tabelle ausgeben

def zeigen(text):
    """Rückt einen mehrzeiligen Text für die Fehlermeldung ein und macht Leerzeichen am Zeilenende sichtbar."""
    if not isinstance(text, str):
        return f"    {text!r}"
    return "\n".join("    " + zeile.replace(" ", "·") for zeile in text.split("\n"))


def melde(zeilen_test, ergebnis, erwartet):
    """Baut die Fehlermeldung für tabelle(zeilen_test); Leerzeichen erscheinen darin als ·."""
    return (
        f"tabelle({zeilen_test!r}) ergibt (Leerzeichen als ·):\n{zeigen(ergebnis)}\n"
        f"erwartet war:\n{zeigen(erwartet)}"
    )


# Das Beispiel aus der Aufgabe
beispiel = ["AP1;Anforderungen aufnehmen;3", " AP2 ; Datenbank einrichten ; 5", "AP3;Schnittstelle zur Buchhaltung;12"]
erwartet = (
    "AP    Bezeichnung          Tage\n"
    "AP1   Anforderungen auf...    3\n"
    "AP2   Datenbank einrichten    5\n"
    "AP3   Schnittstelle zur...   12\n"
    "Summe                        20"
)
ergebnis = tabelle(beispiel)
assert ergebnis == erwartet, melde(beispiel, ergebnis, erwartet)

# Andere Pakete (nicht fest hinschreiben!)
zeilen_test = ["T1;Tests;7", "T22;Abnahme;1"]
erwartet = (
    "AP    Bezeichnung          Tage\n"
    "T1    Tests                   7\n"
    "T22   Abnahme                 1\n"
    "Summe                         8"
)
ergebnis = tabelle(zeilen_test)
assert ergebnis == erwartet, melde(zeilen_test, ergebnis, erwartet)

# Leerzeichen um die Felder fallen weg, auch um die Zahl
zeilen_test = ["   AP7   ;   Server bestellen   ;   10   "]
erwartet = (
    "AP    Bezeichnung          Tage\n"
    "AP7   Server bestellen       10\n"
    "Summe                        10"
)
ergebnis = tabelle(zeilen_test)
assert ergebnis == erwartet, (
    melde(zeilen_test, ergebnis, erwartet) + "\nTipp: Entfernen Sie die Leerzeichen um jedes Feld mit strip()."
)

# Genau 20 Zeichen bleiben, ab 21 Zeichen wird gekürzt
zeilen_test = ["A;12345678901234567890;1", "B;123456789012345678901;2"]
erwartet = (
    "AP    Bezeichnung          Tage\n"
    "A     12345678901234567890    1\n"
    "B     12345678901234567...    2\n"
    "Summe                         3"
)
ergebnis = tabelle(zeilen_test)
assert ergebnis == erwartet, (
    melde(zeilen_test, ergebnis, erwartet)
    + "\nTipp: Nur Bezeichnungen mit mehr als 20 Zeichen werden gekürzt, auf bezeichnung[:17] + \"...\"."
)

# Gekürzt wird erst nach dem Entfernen der Leerzeichen
zeilen_test = ["C;   Netzwerk planen      ;4"]
erwartet = (
    "AP    Bezeichnung          Tage\n"
    "C     Netzwerk planen         4\n"
    "Summe                         4"
)
ergebnis = tabelle(zeilen_test)
assert ergebnis == erwartet, melde(zeilen_test, ergebnis, erwartet)

# Ohne Pakete: nur Kopf und Summe 0
ergebnis = tabelle([])
erwartet = "AP    Bezeichnung          Tage\nSumme                         0"
assert ergebnis == erwartet, melde([], ergebnis, erwartet)

# Ränder: 5 Zeichen Kürzel, 40 Zeichen Bezeichnung, 0 und 99 Tage
zeilen_test = ["ABCDE;" + "x" * 40 + ";99", "Z;y;0"]
erwartet = (
    "AP    Bezeichnung          Tage\n"
    "ABCDE xxxxxxxxxxxxxxxxx...   99\n"
    "Z     y                       0\n"
    "Summe                        99"
)
ergebnis = tabelle(zeilen_test)
assert ergebnis == erwartet, melde(zeilen_test, ergebnis, erwartet)

# Die Tabelle wird zurückgegeben, nicht ausgegeben
assert isinstance(tabelle(["A;b;1"]), str), (
    f'tabelle(["A;b;1"]) ergibt {tabelle(["A;b;1"])!r}, erwartet war ein Text.\n'
    "Tipp: Geben Sie die Tabelle mit return zurück, statt sie mit print auszugeben."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "AP    Bezeichnung          Tage\n"
    "AP1   Anforderungen auf...    3\n"
    "AP2   Datenbank einrichten    5\n"
    "AP3   Schnittstelle zur...   12\n"
    "Summe                        20"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"


# Vergleichslösung: Felder von Hand mit Leerzeichen auffüllen statt mit Breiten im f-String
def tabelle_von_hand(zeilen):
    """Baut die Tabelle, indem sie jede Spalte mit Leerzeichen auf ihre Breite auffüllt."""
    ergebnis = KOPF
    summe = 0
    for zeile in zeilen:
        teile = [teil.strip() for teil in zeile.split(";")]
        name = teile[1]
        if len(name) > 20:
            name = name[:17] + "..."
        summe += int(teile[2])
        ergebnis += "\n" + teile[0] + " " * (6 - len(teile[0])) + name + " " * (20 - len(name))
        ergebnis += " " * (5 - len(teile[2])) + teile[2]
    return ergebnis + "\nSumme" + " " * (26 - 5 + 5 - len(str(summe))) + str(summe)


# 300 zufällige Paketlisten mit zufälligen Leerzeichen
zufall = Zufall(2017)
zeichen = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
buchstaben = "abcdefghijklmnopqrstuvwxyzäöü "
for _ in range(300):
    zeilen_test = []
    for _ in range(zufall.randint(0, 6)):
        kuerzel = "".join(zufall.choice(zeichen) for _ in range(zufall.randint(1, 5)))
        bezeichnung = zufall.choice("ABCDEFGHIJ") + "".join(
            zufall.choice(buchstaben) for _ in range(zufall.choice([zufall.randint(0, 39), zufall.randint(18, 21)]))
        )
        bezeichnung = bezeichnung.rstrip() + zufall.choice("xyz")
        tage = zufall.randint(0, 99)
        felder = [kuerzel, bezeichnung[:40], str(tage)]
        zeilen_test.append(";".join(" " * zufall.randint(0, 2) + feld + " " * zufall.randint(0, 2) for feld in felder))
    erwartet = tabelle_von_hand(zeilen_test)
    ergebnis = tabelle(zeilen_test)
    assert ergebnis == erwartet, melde(zeilen_test, ergebnis, erwartet)

# An der oberen Grenze: 1000 Pakete mit je 99 Tagen
zeilen_test = [f"P{nummer};Paket {nummer};99" for nummer in range(1000)]
ergebnis = tabelle(zeilen_test)
erwartet = tabelle_von_hand(zeilen_test)
assert ergebnis == erwartet, (
    f"Bei 1000 Paketen mit je 99 Tagen ist die Tabelle falsch. Erwartet waren 1002 Zeilen, die letzte\n"
    f"{zeigen(erwartet.split(chr(10))[-1])}\nIhre Tabelle hat "
    f"{len(ergebnis.split(chr(10))) if isinstance(ergebnis, str) else '?'} Zeilen, die letzte\n"
    f"{zeigen(ergebnis.split(chr(10))[-1]) if isinstance(ergebnis, str) else zeigen(ergebnis)}"
)
