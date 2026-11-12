# Automatisch erzeugt aus lehrkraft/muster/2_027_fehlerbericht.py - nicht von Hand ändern.
# vorlage-hash: 9b12bd9d634220a0
# text-hash: 126304356553b5df
# thema: datenstrukturen
# inhalt: Dictionary als Datensatz

# neuer_bericht aus dem Beispiel
bericht = neuer_bericht("Login hängt", "login", 2)
erwartet = {"titel": "Login hängt", "modul": "login", "schwere": 2, "status": "offen"}
assert bericht == erwartet, (
    f"neuer_bericht('Login hängt', 'login', 2) ergibt {bericht!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Die Schlüssel heißen genau \"titel\", \"modul\", \"schwere\" und \"status\"; ein neuer Bericht ist \"offen\"."
)

# kurzinfo eines offenen Berichts
ergebnis = kurzinfo(bericht)
assert vergleichbar(str(ergebnis)) == vergleichbar("[S2] login: Login hängt (offen)"), (
    f"kurzinfo ergibt für den Bericht aus dem Beispiel {ergebnis!r}, erwartet war '[S2] login: Login hängt (offen)'."
)

# schliessen ändert den übergebenen Bericht
schliessen(bericht, "1.4")
erwartet = {"titel": "Login hängt", "modul": "login", "schwere": 2, "status": "behoben", "behoben_in": "1.4"}
assert bericht == erwartet, (
    f"Nach schliessen(bericht, '1.4') ist bericht {bericht!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Ändern Sie den übergebenen Bericht mit bericht[\"status\"] = …, statt ein neues Dictionary anzulegen."
)

# kurzinfo eines behobenen Berichts
ergebnis = kurzinfo(bericht)
assert vergleichbar(str(ergebnis)) == vergleichbar("[S2] login: Login hängt (behoben in 1.4)"), (
    f"kurzinfo ergibt nach schliessen(bericht, '1.4') {ergebnis!r}, "
    "erwartet war '[S2] login: Login hängt (behoben in 1.4)'.\n"
    "Tipp: Lesen Sie zuerst bericht[\"status\"]; nur behobene Berichte haben den Schlüssel \"behoben_in\"."
)

# Andere Werte (nicht fest hinschreiben!)
bericht = neuer_bericht("Tippfehler im Menü", "oberflaeche", 4)
vorher = kurzinfo(bericht)
schliessen(bericht, "2.0.1")
nachher = kurzinfo(bericht)
ergebnis = (vorher, nachher, bericht)
erwartet = (
    "[S4] oberflaeche: Tippfehler im Menü (offen)",
    "[S4] oberflaeche: Tippfehler im Menü (behoben in 2.0.1)",
    {"titel": "Tippfehler im Menü", "modul": "oberflaeche", "schwere": 4, "status": "behoben", "behoben_in": "2.0.1"},
)
assert (vergleichbar(str(vorher)), vergleichbar(str(nachher)), bericht) == (vergleichbar(erwartet[0]), vergleichbar(erwartet[1]), erwartet[2]), (
    f"Für neuer_bericht('Tippfehler im Menü', 'oberflaeche', 4), kurzinfo, schliessen(…, '2.0.1') und wieder "
    f"kurzinfo erwartet:\n{erwartet!r}\nIhr Ergebnis:\n{ergebnis!r}"
)

# Schwere 1 und einbuchstabige Texte
bericht = neuer_bericht("x", "a", 1)
schliessen(bericht, "9")
ergebnis = kurzinfo(bericht)
assert vergleichbar(str(ergebnis)) == vergleichbar("[S1] a: x (behoben in 9)"), (
    f"Für neuer_bericht('x', 'a', 1) und schliessen(…, '9') ergibt kurzinfo {ergebnis!r}, "
    "erwartet war '[S1] a: x (behoben in 9)'."
)

# kurzinfo ändert den Bericht nicht
bericht = neuer_bericht("Absturz beim Speichern", "dateien", 1)
ergebnis = kurzinfo(bericht)
erwartet = {"titel": "Absturz beim Speichern", "modul": "dateien", "schwere": 1, "status": "offen"}
assert vergleichbar(str(ergebnis)) == vergleichbar("[S1] dateien: Absturz beim Speichern (offen)") and bericht == erwartet, (
    f"kurzinfo ergibt {ergebnis!r}, erwartet war '[S1] dateien: Absturz beim Speichern (offen)'; "
    f"der Bericht ist danach {bericht!r}, erwartet war unverändert {erwartet!r}."
)

# Jeder Aufruf von neuer_bericht legt einen eigenen Bericht an
erster = neuer_bericht("Suche findet nichts", "suche", 3)
zweiter = neuer_bericht("Export zu langsam", "export", 3)
schliessen(erster, "1.5")
assert zweiter == {"titel": "Export zu langsam", "modul": "export", "schwere": 3, "status": "offen"}, (
    f"Nach schliessen des ersten Berichts ist der zweite {zweiter!r}, erwartet war er unverändert offen.\n"
    "Tipp: Schreiben Sie das Dictionary {…} in neuer_bericht, damit jeder Aufruf ein neues anlegt, statt "
    "immer dasselbe Dictionary zu ändern und zurückzugeben."
)


# Vergleichslösung: Übersichtszeile durch Verketten von Texten
def kurzinfo_von_hand(titel, modul, schwere, version):
    """Baut die Übersichtszeile aus den einzelnen Werten; version ist None bei offenen Berichten."""
    if version is None:
        zustand = "offen"
    else:
        zustand = "behoben in " + version
    return "[S" + str(schwere) + "] " + modul + ": " + titel + " (" + zustand + ")"


# 300 zufällige Berichte
zufall = Zufall(2027)
woerter = ["Absturz", "Login", "Export", "hängt", "falsch", "Datum", "Ü", "a", "1.0", "(alt)", ":"]
for _ in range(300):
    titel = " ".join(zufall.choices(woerter, k=zufall.randint(1, 4)))
    modul = zufall.choice(["login", "db", "x", "oberflaeche", "berichte_export"])
    schwere = zufall.randint(1, 4)
    bericht = neuer_bericht(titel, modul, schwere)
    erwartet = kurzinfo_von_hand(titel, modul, schwere, None)
    ergebnis = kurzinfo(bericht)
    assert vergleichbar(str(ergebnis)) == vergleichbar(erwartet), f"Für neuer_bericht({titel!r}, {modul!r}, {schwere}) ergibt kurzinfo {ergebnis!r}, erwartet war {erwartet!r}."
    if zufall.random() < 0.5:
        version = f"{zufall.randint(0, 20)}.{zufall.randint(0, 99)}"
        schliessen(bericht, version)
        erwartet = kurzinfo_von_hand(titel, modul, schwere, version)
        ergebnis = kurzinfo(bericht)
        assert vergleichbar(str(ergebnis)) == vergleichbar(erwartet) and bericht["behoben_in"] == version, (
            f"Für neuer_bericht({titel!r}, {modul!r}, {schwere}) und schliessen(…, {version!r}) ergibt kurzinfo "
            f"{ergebnis!r}, erwartet war {erwartet!r}; der Bericht ist {bericht!r}."
        )

# An der oberen Grenze: 1000 Berichte mit Texten aus 200 Zeichen
berichte = []
for nummer in range(1000):
    berichte.append(neuer_bericht("T" * 199 + str(nummer % 10), "m" * 200, nummer % 4 + 1))
for nummer in range(0, 1000, 2):
    schliessen(berichte[nummer], "v" * 199 + str(nummer % 10))
fehler = []
for nummer in range(1000):
    if nummer % 2 == 0:
        erwartet = kurzinfo_von_hand("T" * 199 + str(nummer % 10), "m" * 200, nummer % 4 + 1, "v" * 199 + str(nummer % 10))
    else:
        erwartet = kurzinfo_von_hand("T" * 199 + str(nummer % 10), "m" * 200, nummer % 4 + 1, None)
    if vergleichbar(str(kurzinfo(berichte[nummer]))) != vergleichbar(erwartet):
        fehler.append(nummer)
assert fehler == [], (
    f"Bei 1000 Berichten mit Texten aus 200 Zeichen (jeder zweite geschlossen) stimmt kurzinfo bei "
    f"{len(fehler)} Berichten nicht, zuerst bei Bericht Nummer {fehler[:1]} (gezählt ab 0)."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "[S2] login: Login hängt (offen)\n[S2] login: Login hängt (behoben in 1.4)"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
