# Automatisch erzeugt aus lehrkraft/muster/3_037_mac_tabelle.py - nicht von Hand ändern.
# vorlage-hash: 8979215b9bf76acf
# text-hash: 89f1179f10a0b691
# thema: klassen
# inhalt: Klasse mit Methoden

GERAET_A = "3c:52:82:1a:0f:7e"
GERAET_B = "00:1b:44:11:3a:b7"
UNBEKANNT = "aa:aa:aa:aa:aa:aa"


def lerne_mit_fehler(tabelle, mac, port):
    """Ruft tabelle.lerne(mac, port) auf; liefert die Ausnahme oder None."""
    try:
        tabelle.lerne(mac, port)
    except Exception as ausnahme:
        return ausnahme
    return None


def zufalls_mac(zufall):
    """Erzeugt eine zufällige MAC-Adresse aus einem kleinen Vorrat, damit sich Adressen wiederholen."""
    return ":".join(f"{zufall.randint(0, 3):02x}" for _ in range(6))


# __init__ speichert die Anzahl der Ports und legt ein leeres Dictionary an
tabelle = MacTabelle(8)
anzahl = getattr(tabelle, "anzahl_ports", "(fehlt)")
eintraege = getattr(tabelle, "eintraege", "(fehlt)")
assert anzahl == 8 and eintraege == {}, (
    f"Nach MacTabelle(8) erwartet anzahl_ports = 8 und eintraege = {{}}; gefunden: anzahl_ports = {anzahl!r}, "
    f"eintraege = {eintraege!r}.\nTipp: Legen Sie die Attribute in __init__ mit self.anzahl_ports = … an."
)

# lerne und port_fuer: ein gelerntes Gerät wird gefunden
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
ergebnis = tabelle.port_fuer(GERAET_A)
assert ergebnis == 3, f"Nach lerne({GERAET_A!r}, 3) ergibt port_fuer({GERAET_A!r}) {ergebnis!r}, erwartet war 3."

# lerne und port_fuer: zwei Geräte an verschiedenen Ports (nicht fest hinschreiben!)
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
tabelle.lerne(GERAET_B, 7)
ergebnis = (tabelle.port_fuer(GERAET_A), tabelle.port_fuer(GERAET_B))
assert ergebnis == (3, 7), (
    f"Nach lerne(A, 3) und lerne(B, 7) ergibt port_fuer für A und B {ergebnis!r}, erwartet war (3, 7).\n"
    "Tipp: Speichern Sie jedes Gerät mit self.eintraege[mac] = port als eigenen Eintrag."
)

# port_fuer: ein unbekanntes Gerät ergibt None
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
try:
    ergebnis = tabelle.port_fuer(UNBEKANNT)
except KeyError:
    ergebnis = "KeyError"
assert ergebnis is None, (
    f"port_fuer({UNBEKANNT!r}) für ein unbekanntes Gerät ergibt {ergebnis!r}, erwartet war None.\n"
    "Tipp: self.eintraege.get(mac) liefert None statt eines KeyError."
)

# lerne: ein umgestecktes Gerät bekommt den neuen Port
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
tabelle.lerne(GERAET_A, 5)
ergebnis = tabelle.port_fuer(GERAET_A)
assert ergebnis == 5, f"Nach lerne(A, 3) und lerne(A, 5) ergibt port_fuer(A) {ergebnis!r}, erwartet war 5."

# Zwei Tabellen sind voneinander getrennt
erster = MacTabelle(8)
zweiter = MacTabelle(8)
erster.lerne(GERAET_A, 3)
ergebnis = zweiter.port_fuer(GERAET_A)
assert ergebnis is None, (
    f"Nach erster.lerne(A, 3) ergibt zweiter.port_fuer(A) {ergebnis!r}, erwartet war None.\n"
    "Tipp: Legen Sie das Dictionary in __init__ auf self an, nicht als gemeinsame Variable außerhalb."
)

# geraete_an: das Beispiel, alphabetisch sortiert
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
tabelle.lerne(GERAET_B, 3)
ergebnis = tabelle.geraete_an(3)
if isinstance(ergebnis, list) and sorted(ergebnis) == [GERAET_B, GERAET_A] and ergebnis != [GERAET_B, GERAET_A]:
    hinweis = "\nTipp: Die Geräte stimmen, aber die Liste soll mit sorted(...) alphabetisch sortiert sein."
else:
    hinweis = ""
assert ergebnis == [GERAET_B, GERAET_A], (
    f"Nach lerne(A, 3) und lerne(B, 3) ergibt geraete_an(3) {ergebnis!r}, erwartet war {[GERAET_B, GERAET_A]!r}."
    f"{hinweis}"
)

# geraete_an: nur die Geräte dieses Ports
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
tabelle.lerne(GERAET_B, 3)
tabelle.lerne(UNBEKANNT, 4)
ergebnis = tabelle.geraete_an(4)
assert ergebnis == [UNBEKANNT], f"Mit zwei Geräten an Port 3 und einem an Port 4 ergibt geraete_an(4) {ergebnis!r}, erwartet war {[UNBEKANNT]!r}."

# geraete_an: nach dem Umstecken nicht mehr am alten Port
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
tabelle.lerne(GERAET_B, 3)
tabelle.lerne(GERAET_B, 5)
ergebnis = (tabelle.geraete_an(3), tabelle.geraete_an(5))
assert ergebnis == ([GERAET_A], [GERAET_B]), (
    f"Nach lerne(A, 3), lerne(B, 3), lerne(B, 5) ergeben geraete_an(3) und geraete_an(5) {ergebnis!r}, "
    f"erwartet war ({[GERAET_A]!r}, {[GERAET_B]!r})."
)

# geraete_an: ein Port ohne Geräte ergibt eine leere Liste
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
ergebnis = tabelle.geraete_an(8)
assert ergebnis == [], f"geraete_an(8) ohne Geräte an Port 8 ergibt {ergebnis!r}, erwartet war []."

# lerne: ein zu großer Port löst ValueError aus und ändert nichts
tabelle = MacTabelle(8)
tabelle.lerne(GERAET_A, 3)
fehler = lerne_mit_fehler(tabelle, GERAET_A, 9)
ergebnis = tabelle.port_fuer(GERAET_A)
assert isinstance(fehler, ValueError) and ergebnis == 3, (
    f"lerne(A, 9) bei 8 Ports muss einen ValueError auslösen und den alten Port 3 behalten; Ausnahme: {fehler!r}, "
    f"port_fuer(A) danach: {ergebnis!r}.\nTipp: Prüfen Sie den Port, bevor Sie etwas eintragen."
)

# lerne: Port 0 und negative Ports gibt es nicht
for port in [0, -1, -100]:
    tabelle = MacTabelle(8)
    fehler = lerne_mit_fehler(tabelle, GERAET_A, port)
    ergebnis = tabelle.port_fuer(GERAET_A)
    assert isinstance(fehler, ValueError) and ergebnis is None, (
        f"lerne(A, {port}) muss einen ValueError auslösen und nichts eintragen; Ausnahme: {fehler!r}, "
        f"port_fuer(A) danach: {ergebnis!r}.\nTipp: Die Ports sind von 1 an nummeriert."
    )

# lerne: der erste und der letzte Port sind erlaubt
tabelle = MacTabelle(8)
fehler_erster = lerne_mit_fehler(tabelle, GERAET_A, 1)
fehler_letzter = lerne_mit_fehler(tabelle, GERAET_B, 8)
ergebnis = (tabelle.port_fuer(GERAET_A), tabelle.port_fuer(GERAET_B))
assert fehler_erster is None and fehler_letzter is None and ergebnis == (1, 8), (
    f"lerne(A, 1) und lerne(B, 8) bei 8 Ports müssen klappen; Ausnahmen: {fehler_erster!r}, {fehler_letzter!r}, "
    f"Ports danach: {ergebnis!r}.\nTipp: Auch Port anzahl_ports gibt es noch (<=, nicht <)."
)

# Ein Switch mit einem einzigen Port
tabelle = MacTabelle(1)
fehler_eins = lerne_mit_fehler(tabelle, GERAET_A, 1)
fehler_zwei = lerne_mit_fehler(tabelle, GERAET_B, 2)
assert fehler_eins is None and isinstance(fehler_zwei, ValueError), (
    f"Bei MacTabelle(1) muss lerne(A, 1) klappen und lerne(B, 2) einen ValueError auslösen; "
    f"Ausnahmen: {fehler_eins!r}, {fehler_zwei!r}.\nTipp: Vergleichen Sie mit self.anzahl_ports, nicht mit einer festen Zahl."
)

# Viele zufällige Abläufe, verglichen mit einer Nachrechnung
zufall = Zufall(3037)
for runde in range(200):
    anzahl_ports = zufall.randint(1, 48)
    tabelle = MacTabelle(anzahl_ports)
    erwartet = {}
    schritte = []
    for _ in range(20):
        mac = zufalls_mac(zufall)
        port = zufall.choice([zufall.randint(1, anzahl_ports), zufall.randint(-3, anzahl_ports + 3)])
        schritte.append(f"lerne({mac!r}, {port})")
        fehler = lerne_mit_fehler(tabelle, mac, port)
        gueltig = 1 <= port <= anzahl_ports
        if gueltig:
            erwartet[mac] = port
        assert (fehler is None) == gueltig, (
            f"MacTabelle({anzahl_ports}), dann {', '.join(schritte)}: beim letzten Aufruf erwartet "
            f"{'kein' if gueltig else 'ein'} ValueError, bekommen: {fehler!r}."
        )
    frage = zufalls_mac(zufall)
    ergebnis = tabelle.port_fuer(frage)
    assert ergebnis == erwartet.get(frage), (
        f"MacTabelle({anzahl_ports}), dann {', '.join(schritte)}: port_fuer({frage!r}) ergibt {ergebnis!r}, "
        f"erwartet war {erwartet.get(frage)!r}."
    )
    port = zufall.randint(1, anzahl_ports)
    ergebnis = tabelle.geraete_an(port)
    erwartet_an_port = sorted(mac for mac in erwartet if erwartet[mac] == port)
    assert ergebnis == erwartet_an_port, (
        f"MacTabelle({anzahl_ports}), dann {', '.join(schritte)}: geraete_an({port}) ergibt {ergebnis!r}, "
        f"erwartet war {erwartet_an_port!r}."
    )

# Obere Grenze: 10 000 Geräte an 48 Ports, dann 10 000 Abfragen
tabelle = MacTabelle(48)
adressen = [":".join(f"{(nummer >> (8 * stelle)) & 255:02x}" for stelle in range(6)) for nummer in range(10_000)]
for nummer, mac in enumerate(adressen):
    tabelle.lerne(mac, nummer % 48 + 1)
falsch = [mac for nummer, mac in enumerate(adressen) if tabelle.port_fuer(mac) != nummer % 48 + 1]
anzahl_an_eins = len(tabelle.geraete_an(1))
assert falsch == [] and anzahl_an_eins == 209, (
    f"Nach 10 000 Aufrufen von lerne liefert port_fuer bei {len(falsch)} Geräten den falschen Port "
    f"(z. B. {falsch[:2]}), und an Port 1 hängen laut geraete_an(1) {anzahl_an_eins} Geräte, erwartet 209."
)

# Die Ausgabe des Programms stimmt
assert vergleichbar(AUSGABE) == vergleichbar(f"3 {[GERAET_B, GERAET_A]}"), (
    f'Erwartete Ausgabe: "3 {[GERAET_B, GERAET_A]}" – Ihr Programm: "{AUSGABE}"'
)
