# Automatisch erzeugt aus lehrkraft/muster/3_075_dialogablauf.py - nicht von Hand ändern.
# vorlage-hash: 9943ce08806e3e7e
# text-hash: 83f082c45f348f83
# thema: datenstrukturen
# inhalt: Zustandsautomat mit Dictionary

def wert_von(funktion, *argumente):
    """Ruft funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_folge(uebergaenge, bildschirm, ereignis):
    """Vergleichslösung: sucht den Übergang durch Ansehen aller Einträge."""
    for (von, art), nach in uebergaenge.items():
        if von == bildschirm and art == ereignis:
            return nach
    return bildschirm


def vergleich_ablauf(uebergaenge, start, ereignisse):
    """Vergleichslösung für ablauf."""
    liste = [start]
    for ereignis in ereignisse:
        liste.append(vergleich_folge(uebergaenge, liste[-1], ereignis))
    return liste


def vergleich_enden(uebergaenge):
    """Vergleichslösung für endbildschirme."""
    enden = []
    for nach in uebergaenge.values():
        hat_ausgang = any(von == nach for von, _ in uebergaenge)
        if not hat_ausgang and nach not in enden:
            enden.append(nach)
    return sorted(enden)


BEISPIEL = ["vergessen", "weiter", "code_falsch", "code_richtig", "speichern"]
KOPIE = dict(DIALOG)

# folgebildschirm: ein Übergang aus der Tabelle
ergebnis = wert_von(folgebildschirm, DIALOG, "start", "vergessen")
assert ergebnis == "benutzername", (
    f'folgebildschirm(DIALOG, "start", "vergessen") ergibt {ergebnis!r}, erwartet war "benutzername".\n'
    "Tipp: Der Schlüssel ist das Tupel (bildschirm, ereignis), also uebergaenge[(bildschirm, ereignis)]."
)

# folgebildschirm: das Beispiel aus der Aufgabe (nicht fest hinschreiben!)
ergebnis = wert_von(folgebildschirm, DIALOG, "code", "code_richtig")
assert ergebnis == "passwort", (
    f'folgebildschirm(DIALOG, "code", "code_richtig") ergibt {ergebnis!r}, erwartet war "passwort".'
)

# folgebildschirm: ein Übergang, der auf denselben Bildschirm zurückführt
ergebnis = wert_von(folgebildschirm, DIALOG, "code", "code_falsch")
assert ergebnis == "code", f'folgebildschirm(DIALOG, "code", "code_falsch") ergibt {ergebnis!r}, erwartet war "code".'

# folgebildschirm: ohne passenden Übergang bleibt der Bildschirm
ergebnis = wert_von(folgebildschirm, DIALOG, "start", "weiter")
assert ergebnis == "start", (
    f'folgebildschirm(DIALOG, "start", "weiter") ergibt {ergebnis!r}, erwartet war "start": Auf dem '
    "Startbildschirm gibt es keine Schaltfläche weiter, also bleibt er stehen.\n"
    "Tipp: uebergaenge.get(schluessel, bildschirm) liefert bildschirm, wenn der Schlüssel fehlt."
)

# folgebildschirm: ein Ereignis, das es nur auf anderen Bildschirmen gibt
ergebnis = wert_von(folgebildschirm, DIALOG, "passwort", "code_richtig")
assert ergebnis == "passwort", (
    f'folgebildschirm(DIALOG, "passwort", "code_richtig") ergibt {ergebnis!r}, erwartet war "passwort".\n'
    "Tipp: Es zählt nur der Übergang, dessen Schlüssel genau (bildschirm, ereignis) ist."
)

# folgebildschirm: ein Bildschirm, der in der Tabelle nicht vorkommt
ergebnis = wert_von(folgebildschirm, DIALOG, "hilfe", "weiter")
assert ergebnis == "hilfe", f'folgebildschirm(DIALOG, "hilfe", "weiter") ergibt {ergebnis!r}, erwartet war "hilfe".'

# folgebildschirm: eine andere Tabelle
anmeldung = {("karte", "eingesteckt"): "pin", ("pin", "pin_ok"): "menue", ("menue", "abmelden"): "karte"}
ergebnis = [wert_von(folgebildschirm, anmeldung, b, e) for b, e in [("karte", "eingesteckt"), ("menue", "abmelden"), ("pin", "abmelden")]]
assert ergebnis == ["pin", "karte", "pin"], (
    f"Mit der Tabelle {anmeldung} ergeben die Übergänge (karte, eingesteckt), (menue, abmelden) und "
    f"(pin, abmelden) {ergebnis!r}, erwartet war ['pin', 'karte', 'pin'].\n"
    "Tipp: Lesen Sie aus uebergaenge, nicht aus DIALOG."
)

# ablauf: das Beispiel aus der Aufgabe
ergebnis = wert_von(ablauf, DIALOG, "start", BEISPIEL)
erwartet = ["start", "benutzername", "code", "code", "passwort", "fertig"]
assert ergebnis == erwartet, (
    f"ablauf(DIALOG, 'start', {BEISPIEL}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}.\n"
    "Tipp: Merken Sie sich den aktuellen Bildschirm in einer Variablen, ersetzen Sie ihn bei jedem Ereignis "
    "durch folgebildschirm(...) und hängen Sie ihn an die Liste an."
)

# ablauf: ohne Ereignisse wird nur der Startbildschirm angezeigt
ergebnis = wert_von(ablauf, DIALOG, "start", [])
assert ergebnis == ["start"], (
    f"ablauf(DIALOG, 'start', []) ergibt {ergebnis!r}, erwartet war ['start'].\n"
    "Tipp: Der Startbildschirm steht immer als erster Eintrag in der Liste."
)

# ablauf: Abbrechen führt zurück zum Start, danach geht es von vorn los
ereignisse = ["vergessen", "weiter", "abbrechen", "vergessen", "abbrechen"]
ergebnis = wert_von(ablauf, DIALOG, "start", ereignisse)
erwartet = ["start", "benutzername", "code", "start", "benutzername", "start"]
assert ergebnis == erwartet, f"ablauf(DIALOG, 'start', {ereignisse}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}."

# ablauf: Ereignisse ohne Übergang lassen den Bildschirm stehen, auch am Ende
ereignisse = ["weiter", "vergessen", "speichern", "weiter", "code_richtig", "speichern", "abbrechen"]
ergebnis = wert_von(ablauf, DIALOG, "start", ereignisse)
erwartet = ["start", "start", "benutzername", "benutzername", "code", "passwort", "fertig", "fertig"]
assert ergebnis == erwartet, (
    f"ablauf(DIALOG, 'start', {ereignisse}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}.\n"
    "Tipp: Auch ohne Übergang kommt für jedes Ereignis ein Eintrag in die Liste, nämlich der alte Bildschirm."
)

# ablauf: ein anderer Startbildschirm
ergebnis = wert_von(ablauf, DIALOG, "code", ["code_falsch", "code_falsch", "abbrechen"])
assert ergebnis == ["code", "code", "code", "start"], (
    f"ablauf(DIALOG, 'code', ['code_falsch', 'code_falsch', 'abbrechen']) ergibt {ergebnis!r}, "
    "erwartet war ['code', 'code', 'code', 'start']."
)

# ablauf: eine andere Tabelle
ereignisse = ["eingesteckt", "pin_ok", "abmelden", "pin_ok"]
ergebnis = wert_von(ablauf, anmeldung, "karte", ereignisse)
assert ergebnis == ["karte", "pin", "menue", "karte", "karte"], (
    f"Mit der Tabelle {anmeldung} ergibt ablauf(…, 'karte', {ereignisse}) {ergebnis!r}, "
    "erwartet war ['karte', 'pin', 'menue', 'karte', 'karte']."
)

# schaltflaechen: die Schaltflächen des Codebildschirms (Reihenfolge noch egal)
ergebnis = wert_von(schaltflaechen, DIALOG, "code")
assert isinstance(ergebnis, list) and sorted(ergebnis) == ["abbrechen", "code_falsch", "code_richtig"], (
    f"schaltflaechen(DIALOG, 'code') ergibt {ergebnis!r}, erwartet waren die Ereignisse abbrechen, code_falsch "
    "und code_richtig in einer Liste.\nTipp: Gehen Sie mit for (von, ereignis) in uebergaenge alle Schlüssel durch "
    "und sammeln Sie die Ereignisse, deren von gleich bildschirm ist."
)

# schaltflaechen: alphabetisch sortiert
assert ergebnis == ["abbrechen", "code_falsch", "code_richtig"], (
    f"schaltflaechen(DIALOG, 'code') ergibt {ergebnis!r}, erwartet war ['abbrechen', 'code_falsch', 'code_richtig'].\n"
    "Tipp: Geben Sie die Liste mit sorted(...) zurück."
)

# schaltflaechen: ein anderer Bildschirm (nicht fest hinschreiben!)
ergebnis = wert_von(schaltflaechen, DIALOG, "benutzername")
assert ergebnis == ["abbrechen", "weiter"], (
    f"schaltflaechen(DIALOG, 'benutzername') ergibt {ergebnis!r}, erwartet war ['abbrechen', 'weiter']."
)

# schaltflaechen: ein Bildschirm mit nur einer Schaltfläche
ergebnis = wert_von(schaltflaechen, DIALOG, "start")
assert ergebnis == ["vergessen"], f"schaltflaechen(DIALOG, 'start') ergibt {ergebnis!r}, erwartet war ['vergessen']."

# schaltflaechen: der Endbildschirm hat keine Schaltflächen
ergebnis = wert_von(schaltflaechen, DIALOG, "fertig")
assert ergebnis == [], (
    f"schaltflaechen(DIALOG, 'fertig') ergibt {ergebnis!r}, erwartet war [].\n"
    "Tipp: Zählen Sie nur Übergänge, die vom Bildschirm wegführen, nicht die, die zu ihm hinführen."
)

# schaltflaechen: ein Bildschirm, der in der Tabelle nicht vorkommt
ergebnis = wert_von(schaltflaechen, DIALOG, "hilfe")
assert ergebnis == [], f"schaltflaechen(DIALOG, 'hilfe') ergibt {ergebnis!r}, erwartet war []."

# endbildschirme: das Beispiel aus der Aufgabe
ergebnis = wert_von(endbildschirme, DIALOG)
assert ergebnis == ["fertig"], (
    f"endbildschirme(DIALOG) ergibt {ergebnis!r}, erwartet war ['fertig'].\n"
    "Tipp: Sammeln Sie erst alle Bildschirme, von denen ein Übergang wegführt (die von-Teile der Schlüssel), "
    "und dann die Folgebildschirme, die nicht darunter sind."
)

# endbildschirme: mehrere Enden, jedes nur einmal (Reihenfolge noch egal)
selbstbedienung = {
    ("start", "drucken"): "druckauftrag",
    ("druckauftrag", "ok"): "erledigt",
    ("druckauftrag", "papier_leer"): "stoerung",
    ("start", "scannen"): "scan",
    ("scan", "ok"): "erledigt",
    ("scan", "fehler"): "stoerung",
}
ergebnis = wert_von(endbildschirme, selbstbedienung)
assert isinstance(ergebnis, list) and sorted(ergebnis) == ["erledigt", "stoerung"], (
    f"endbildschirme({selbstbedienung}) ergibt {ergebnis!r}, erwartet waren erledigt und stoerung, jedes einmal.\n"
    "Tipp: Eine Menge (set) nimmt jeden Bildschirm nur einmal auf."
)

# endbildschirme: alphabetisch sortiert
selbstbedienung[("scan", "abbruch")] = "abgebrochen"
ergebnis = wert_von(endbildschirme, selbstbedienung)
assert ergebnis == ["abgebrochen", "erledigt", "stoerung"], (
    f"Mit dem zusätzlichen Übergang ('scan', 'abbruch') → 'abgebrochen' ergibt endbildschirme(…) {ergebnis!r}, "
    "erwartet war ['abgebrochen', 'erledigt', 'stoerung'].\nTipp: Geben Sie die Liste mit sorted(...) zurück."
)

# endbildschirme: ein Bildschirm, der nur auf sich selbst führt, hat einen Ausgang
schleife = {("start", "los"): "warten", ("warten", "tippen"): "warten"}
ergebnis = wert_von(endbildschirme, schleife)
assert ergebnis == [], (
    f"endbildschirme({schleife}) ergibt {ergebnis!r}, erwartet war []: Von warten führt ein Übergang weg "
    "(auch wenn er zurück zu warten geht)."
)

# endbildschirme: ein Startbildschirm ohne Pfeil dorthin ist kein Ende
kurz = {("start", "los"): "fertig"}
ergebnis = wert_von(endbildschirme, kurz)
assert ergebnis == ["fertig"], (
    f"endbildschirme({kurz}) ergibt {ergebnis!r}, erwartet war ['fertig']: Von start führt ein Übergang weg, "
    "von fertig keiner."
)

# endbildschirme: eine leere Tabelle hat keine Enden
ergebnis = wert_von(endbildschirme, {})
assert ergebnis == [], f"endbildschirme({{}}) ergibt {ergebnis!r}, erwartet war []."

# Die Tabelle bleibt unverändert
wert_von(folgebildschirm, DIALOG, "start", "weiter")
wert_von(ablauf, DIALOG, "start", BEISPIEL)
wert_von(schaltflaechen, DIALOG, "code")
wert_von(endbildschirme, DIALOG)
assert DIALOG == KOPIE, f"Nach den Aufrufen der vier Funktionen ist DIALOG\n{DIALOG}\nstatt\n{KOPIE}."

zufall = Zufall(3075)


def zufallstabelle():
    """Gibt zufällige Bildschirme, Ereignisarten und eine Tabelle daraus zurück."""
    bildschirme = [f"b{nummer}" for nummer in range(zufall.randint(1, 6))]
    arten = ["ok", "zurueck", "hilfe", "x"][: zufall.randint(1, 4)]
    tabelle = {}
    for _ in range(zufall.randint(0, 12)):
        tabelle[(zufall.choice(bildschirme), zufall.choice(arten))] = zufall.choice(bildschirme + ["ende"])
    return bildschirme, arten, tabelle


# Viele zufällige Tabellen und Ereignisfolgen: ablauf
for _ in range(300):
    bildschirme, arten, tabelle = zufallstabelle()
    start = zufall.choice(bildschirme + ["fremd"])
    ereignisse = [zufall.choice(arten + ["neu"]) for _ in range(zufall.randint(0, 8))]
    ergebnis = wert_von(ablauf, tabelle, start, ereignisse)
    erwartet = vergleich_ablauf(tabelle, start, ereignisse)
    assert ergebnis == erwartet, (
        f"ablauf({tabelle}, {start!r}, {ereignisse}) ergibt\n{ergebnis!r},\nerwartet war\n{erwartet!r}."
    )

# Viele zufällige Tabellen: schaltflaechen
for _ in range(300):
    bildschirme, arten, tabelle = zufallstabelle()
    bildschirm = zufall.choice(bildschirme + ["ende"])
    ergebnis = wert_von(schaltflaechen, tabelle, bildschirm)
    erwartet = sorted(art for von, art in tabelle if von == bildschirm)
    assert ergebnis == erwartet, f"schaltflaechen({tabelle}, {bildschirm!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Viele zufällige Tabellen: endbildschirme
for _ in range(300):
    bildschirme, arten, tabelle = zufallstabelle()
    ergebnis = wert_von(endbildschirme, tabelle)
    erwartet = vergleich_enden(tabelle)
    assert ergebnis == erwartet, f"endbildschirme({tabelle}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Laufzeit: ablauf sieht pro Ereignis nur einmal im Dictionary nach
kreis = {}
for nummer in range(500):
    kreis[(f"s{nummer}", "weiter")] = f"s{(nummer + 1) % 500}"
    kreis[(f"s{nummer}", "zurueck")] = f"s{(nummer + 499) % 500}"
_, schritte = zaehle_schritte(ablauf, kreis, "s400", ["weiter"] * 100)
assert schritte <= 2000, (
    f"ablauf mit 1000 Übergängen und 100 Ereignissen brauchte {schritte} Schritte, erlaubt sind 2000 "
    "(die Musterlösung braucht etwa 400).\nTipp: Gehen Sie nicht für jedes Ereignis alle Übergänge durch, "
    "sondern schlagen Sie mit dem Schlüssel (bildschirm, ereignis) direkt im Dictionary nach."
)

# Obere Grenze: 10 000 Übergänge und 100 000 Ereignisse
gross = {}
for nummer in range(5000):
    gross[(f"s{nummer}", "weiter")] = f"s{(nummer + 1) % 5000}"
    gross[(f"s{nummer}", "zurueck")] = f"s{(nummer + 4999) % 5000}"
ereignisse = [zufall.choice(["weiter", "weiter", "zurueck", "hilfe"]) for _ in range(100_000)]
ergebnis = wert_von(ablauf, gross, "s0", ereignisse)
erwartet = [0]
for ereignis in ereignisse:
    if ereignis == "weiter":
        erwartet.append((erwartet[-1] + 1) % 5000)
    elif ereignis == "zurueck":
        erwartet.append((erwartet[-1] + 4999) % 5000)
    else:
        erwartet.append(erwartet[-1])
erwartet = [f"s{nummer}" for nummer in erwartet]
assert ergebnis == erwartet, (
    "Bei 10 000 Übergängen im Kreis s0 … s4999 (weiter/zurueck) und 100 000 Ereignissen stimmt ablauf nicht; "
    f"erhalten {str(ergebnis)[:120]}, erwartet war {str(erwartet)[:120]}."
)
