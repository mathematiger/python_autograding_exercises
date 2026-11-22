# Automatisch erzeugt aus lehrkraft/muster/3_037_switchport.py - nicht von Hand ändern.
# vorlage-hash: 8b5e7984c98af68e
# text-hash: e6224974988e76ab
# thema: klassen
# inhalt: Klasse mit Methoden

MAC_A = "00:1a:2b:3c:4d:5e"
MAC_B = "00:aa:bb:cc:dd:ee"


def zustand(port):
    """Liest die Attribute eines Ports für Fehlermeldungen, auch wenn welche fehlen."""
    namen = ["nummer", "vlan", "aktiv", "geraete"]
    return {name: getattr(port, name, "(fehlt)") for name in namen}


def vlan_fehler(port, vlan):
    """Ruft vlan_setzen auf; True, wenn ein ValueError kam."""
    try:
        port.vlan_setzen(vlan)
    except ValueError:
        return True
    return False


# Ein neuer Port hat die Startwerte
port = Switchport(7)
assert zustand(port) == {"nummer": 7, "vlan": 1, "aktiv": False, "geraete": []}, (
    "Nach Switchport(7) erwartet nummer=7, vlan=1, aktiv=False, geraete=[]; "
    f"gefunden: {zustand(port)}.\nTipp: Legen Sie alle vier Attribute in __init__ auf self an."
)

# aktivieren schaltet den Port ein
port = Switchport(7)
port.aktivieren()
assert port.aktiv == True, f"Nach aktivieren() ist aktiv {port.aktiv!r}, erwartet war True."

# deaktivieren schaltet ihn wieder ab
port = Switchport(7)
port.aktivieren()
port.deaktivieren()
assert port.aktiv == False, f"Nach aktivieren() und deaktivieren() ist aktiv {port.aktiv!r}, erwartet war False."

# vlan_setzen ändert das VLAN
port = Switchport(7)
port.vlan_setzen(10)
assert port.vlan == 10, f"Nach vlan_setzen(10) ist vlan {port.vlan!r}, erwartet war 10."

# lerne merkt sich eine Adresse an einem aktiven Port
port = Switchport(3)
port.aktivieren()
port.lerne(MAC_A)
assert port.geraete == [MAC_A], f"Aktiver Port, lerne({MAC_A!r}): geraete ist {port.geraete!r}, erwartet war [{MAC_A!r}]."

# Eine bekannte Adresse steht nur einmal in der Liste
port = Switchport(3)
port.aktivieren()
port.lerne(MAC_A)
port.lerne(MAC_A)
port.lerne(MAC_B)
assert port.geraete == [MAC_A, MAC_B], (
    f"Aktiver Port, lerne A, lerne A, lerne B: geraete ist {port.geraete!r}, erwartet war [{MAC_A!r}, {MAC_B!r}].\n"
    "Tipp: Prüfen Sie mit mac not in self.geraete, ob die Adresse neu ist."
)

# Ein inaktiver Port lernt nichts
port = Switchport(3)
port.lerne(MAC_A)
assert port.geraete == [], (
    f"Inaktiver Port, lerne({MAC_A!r}): geraete ist {port.geraete!r}, erwartet war [].\n"
    "Tipp: Lernen darf der Port nur, wenn self.aktiv True ist."
)

# deaktivieren vergisst die gelernten Adressen
port = Switchport(3)
port.aktivieren()
port.lerne(MAC_A)
port.deaktivieren()
port.aktivieren()
assert port.geraete == [], (
    f"Nach lerne, deaktivieren und erneutem aktivieren ist geraete {port.geraete!r}, erwartet war []."
)

# beschreibung im Beispiel aus der Aufgabe
assert vergleichbar(AUSGABE) == vergleichbar("Port 3: VLAN 10, aktiv, 2 Geräte"), (
    f'Erwartete Ausgabe: "Port 3: VLAN 10, aktiv, 2 Geräte" – Ihr Programm: "{AUSGABE}"'
)

# beschreibung eines neuen Ports (nicht fest hinschreiben!)
text = Switchport(7).beschreibung()
assert vergleichbar(text) == vergleichbar("Port 7: VLAN 1, inaktiv, 0 Geräte"), (
    f'Switchport(7).beschreibung() ergibt {text!r}, erwartet war "Port 7: VLAN 1, inaktiv, 0 Geräte".\n'
    "Tipp: Setzen Sie self.nummer, self.vlan, den Zustand und len(self.geraete) in den Text ein."
)

# Zwei Ports haben eigene Attribute
eins = Switchport(1)
zwei = Switchport(2)
eins.aktivieren()
eins.vlan_setzen(20)
eins.lerne(MAC_A)
assert zustand(zwei) == {"nummer": 2, "vlan": 1, "aktiv": False, "geraete": []}, (
    f"Port 1 wurde verändert, Port 2 nicht; trotzdem ist Port 2 jetzt {zustand(zwei)}.\n"
    "Tipp: Speichern Sie alles auf self, und legen Sie die Liste in __init__ jedes Mal neu an."
)

# Ein VLAN über 4094 löst ValueError aus
port = Switchport(3)
ausgeloest = vlan_fehler(port, 5000)
assert ausgeloest, "vlan_setzen(5000) hat keinen ValueError ausgelöst, erwartet war einer (erlaubt sind 1 bis 4094)."

# Nach dem ValueError bleibt das alte VLAN
port = Switchport(3)
port.vlan_setzen(10)
vlan_fehler(port, 5000)
assert port.vlan == 10, (
    f"Nach vlan_setzen(10) und dem ungültigen vlan_setzen(5000) ist vlan {port.vlan!r}, erwartet war weiter 10.\n"
    "Tipp: Prüfen Sie zuerst und ändern Sie self.vlan erst danach."
)

# VLAN 0 löst ValueError aus
port = Switchport(3)
ausgeloest = vlan_fehler(port, 0)
assert ausgeloest, "vlan_setzen(0) hat keinen ValueError ausgelöst, erwartet war einer (erlaubt sind 1 bis 4094)."

# Ein negatives VLAN löst ValueError aus
port = Switchport(3)
ausgeloest = vlan_fehler(port, -1)
assert ausgeloest, "vlan_setzen(-1) hat keinen ValueError ausgelöst, erwartet war einer (erlaubt sind 1 bis 4094)."

# Die Ränder 1 und 4094 sind erlaubt
port = Switchport(3)
ausgeloest = [vlan_fehler(port, 4094), port.vlan, vlan_fehler(port, 1), port.vlan]
assert ausgeloest == [False, 4094, False, 1], (
    "vlan_setzen(4094) und dann vlan_setzen(1) müssen beide klappen; erwartet [kein Fehler, 4094, kein Fehler, 1], "
    f"bekommen {['ValueError' if x is True else x for x in ausgeloest]}.\nTipp: Erlaubt sind 1 bis einschließlich 4094."
)

# 4095 ist nicht erlaubt
port = Switchport(3)
ausgeloest = vlan_fehler(port, 4095)
assert ausgeloest, "vlan_setzen(4095) hat keinen ValueError ausgelöst, erwartet war einer (erlaubt sind 1 bis 4094)."

# Viele zufällige Aufrufe an mehreren Ports, verglichen mit einer Nachrechnung
zufall = Zufall(3037)
macs = [f"00:00:00:00:00:{zahl:02x}" for zahl in range(12)]
for versuch in range(100):
    ports = [Switchport(nummer) for nummer in (1, 2, 3)]
    modell = [{"vlan": 1, "aktiv": False, "geraete": []} for _ in ports]
    aufrufe = []
    for schritt in range(20):
        i = zufall.randrange(3)
        aktion = zufall.choice(["aktivieren", "deaktivieren", "vlan", "lerne", "lerne", "lerne"])
        m = modell[i]
        if aktion == "aktivieren":
            aufrufe.append(f"p{i + 1}.aktivieren()")
            ports[i].aktivieren()
            m["aktiv"] = True
        elif aktion == "deaktivieren":
            aufrufe.append(f"p{i + 1}.deaktivieren()")
            ports[i].deaktivieren()
            m["aktiv"] = False
            m["geraete"] = []
        elif aktion == "vlan":
            vlan = zufall.choice([zufall.randint(-10000, 10000), zufall.randint(-2, 3), zufall.randint(4093, 4096)])
            aufrufe.append(f"p{i + 1}.vlan_setzen({vlan})")
            ausgeloest = vlan_fehler(ports[i], vlan)
            erlaubt = 1 <= vlan <= 4094
            if erlaubt:
                m["vlan"] = vlan
            assert ausgeloest != erlaubt, (
                f"Nach {', '.join(aufrufe)}: beim letzten Aufruf erwartet {'kein' if erlaubt else 'ein'} ValueError, "
                f"bekommen {'ein' if ausgeloest else 'kein'} ValueError."
            )
        else:
            mac = zufall.choice(macs)
            aufrufe.append(f"p{i + 1}.lerne({mac!r})")
            ports[i].lerne(mac)
            if m["aktiv"] and mac not in m["geraete"]:
                m["geraete"].append(mac)
        for nummer, (p, erwartet) in enumerate(zip(ports, modell), start=1):
            bekommen = {"vlan": p.vlan, "aktiv": p.aktiv, "geraete": list(p.geraete)}
            assert bekommen == erwartet, (
                f"Drei Ports p1, p2, p3, dann {', '.join(aufrufe)}:\n"
                f"  p{nummer} erwartet {erwartet}\n  p{nummer} bekommen {bekommen}"
            )

# Obere Grenze: 2000 Aufrufe an einem Port, Beschreibung am Ende
port = Switchport(48)
port.aktivieren()
for zahl in range(1000):
    port.lerne(f"02:00:00:00:{zahl // 256:02x}:{zahl % 256:02x}")
    port.lerne(f"02:00:00:00:00:{zahl % 7:02x}")
text = port.beschreibung()
assert vergleichbar(text) == vergleichbar("Port 48: VLAN 1, aktiv, 1000 Geräte"), (
    f'Nach 2000 Aufrufen von lerne mit 1000 verschiedenen Adressen ergibt beschreibung() {text!r}, '
    'erwartet war "Port 48: VLAN 1, aktiv, 1000 Geräte".'
)
