# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_037_switchport.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_037_switchport

"""Aufgabe 3_037 – Switchport                                    Stufe 3 ★★★☆☆

Ein Switch verbindet die Rechner eines Netzwerks. Jeder seiner
Anschlüsse (Ports) hat eine Nummer, gehört zu einem VLAN (einem
virtuellen Teilnetz mit einer Nummer von 1 bis 4094, ab Werk 1) und ist
aktiv oder abgeschaltet. An einem aktiven Port merkt sich der Switch die
MAC-Adressen (Hardware-Adressen) der Geräte, die dort Daten senden.
Für ein Planungswerkzeug soll ein Port als Klasse modelliert werden.
Vervollständigen Sie die Klasse `Switchport`:

- `__init__(self, nummer)` legt die Attribute `nummer`, `vlan` (1),
  `aktiv` (False) und `geraete` (eine leere Liste) an.
- `aktivieren(self)` schaltet den Port ein.
- `deaktivieren(self)` schaltet ihn ab; dabei vergisst er alle gelernten
  MAC-Adressen.
- `vlan_setzen(self, vlan)` ordnet den Port einem anderen VLAN zu. Liegt
  vlan nicht zwischen 1 und 4094, löst die Methode einen ValueError aus
  und lässt das VLAN, wie es war.
- `lerne(self, mac)` hängt die MAC-Adresse an geraete an, aber nur, wenn
  der Port aktiv ist und die Adresse noch nicht in der Liste steht.
- `beschreibung(self)` gibt einen Text wie "Port 3: VLAN 10, aktiv,
  2 Geräte" oder "Port 7: VLAN 1, inaktiv, 0 Geräte" zurück.

    port = Switchport(3)
    port.aktivieren()
    port.vlan_setzen(10)
    port.lerne("00:1a:2b:3c:4d:5e")
    port.lerne("00:1a:2b:3c:4d:5e")      # schon bekannt, bleibt einmal
    port.lerne("00:aa:bb:cc:dd:ee")
    port.beschreibung()   →  "Port 3: VLAN 10, aktiv, 2 Geräte"
    port.vlan_setzen(5000)  →  ValueError

Grenzen: nummer ist eine ganze Zahl von 1 bis 48. vlan ist eine ganze
Zahl von -10 000 bis 10 000. Eine MAC-Adresse ist ein Text wie
"00:1a:2b:3c:4d:5e". Ein Port erlebt bis zu 2000 Methodenaufrufe in
beliebiger Reihenfolge, und es gibt beliebig viele Ports nebeneinander.

Hintergrund: Bisher haben Sie Daten in Listen und Dictionaries abgelegt
und mit Funktionen bearbeitet. Eine Klasse bündelt beides: Sie ist der
Bauplan für Objekte, die Daten (Attribute) und die passenden Funktionen
(Methoden) zusammen mitbringen (MIT 6.0001, Lecture 8). Ein Beispiel:

    class Lampe:
        def __init__(self, raum):
            self.raum = raum          # Attribut raum auf dem neuen Objekt
            self.an = False

        def einschalten(self):
            self.an = True

    flur = Lampe("Flur")              # neues Objekt, Python ruft __init__ auf
    flur.einschalten()                # Methode aufrufen
    flur.an                           →  True

Die Methode __init__ läuft automatisch, wenn ein Objekt entsteht, und
legt dessen Attribute an. Jede Methode bekommt als ersten Parameter self,
das Objekt, für das sie aufgerufen wurde; bei flur.einschalten() setzt
Python self = flur ein, man schreibt es beim Aufruf nicht hin. Über
self.attribut liest und ändert die Methode die Daten genau dieses
Objekts. Jedes Objekt hat eigene Attribute: Eine zweite Lampe("Küche")
bleibt aus, wenn flur eingeschaltet wird. Wie man mit raise einen
ValueError auslöst, steht in Aufgabe 3_009.
"""


class Switchport:
    """Ein Anschluss eines Switches mit VLAN, Zustand und gelernten MAC-Adressen."""

    def __init__(self, nummer):
        self.nummer = nummer
        self.vlan = 1
        self.aktiv = False
        self.geraete = []

    def aktivieren(self):
        """Schaltet den Port ein."""
        self.aktiv = True

    def deaktivieren(self):
        """Schaltet den Port ab und vergisst alle gelernten MAC-Adressen."""
        self.aktiv = False
        self.geraete = []

    def vlan_setzen(self, vlan):
        """Ordnet den Port dem VLAN vlan zu; erlaubt sind 1 bis 4094."""
        if vlan < 1 or vlan > 4094:
            raise ValueError(f"VLAN {vlan} gibt es nicht, erlaubt sind 1 bis 4094")
        self.vlan = vlan

    def lerne(self, mac):
        """Merkt sich die MAC-Adresse, wenn der Port aktiv ist und sie noch nicht kennt."""
        if self.aktiv and mac not in self.geraete:
            self.geraete.append(mac)

    def beschreibung(self):
        """Gibt den Zustand des Ports als Text zurück."""
        if self.aktiv:
            zustand = "aktiv"
        else:
            zustand = "inaktiv"
        return f"Port {self.nummer}: VLAN {self.vlan}, {zustand}, {len(self.geraete)} Geräte"


port = Switchport(3)
port.aktivieren()
port.vlan_setzen(10)
port.lerne("00:1a:2b:3c:4d:5e")
port.lerne("00:1a:2b:3c:4d:5e")
port.lerne("00:aa:bb:cc:dd:ee")
print(port.beschreibung())


# Idee: __init__ legt die vier Attribute auf self an, die Liste geraete jedes Mal neu. Jede Methode
# liest oder ändert nur die Attribute ihres eigenen Objekts über self. vlan_setzen prüft zuerst den
# Bereich und löst bei einem Verstoß einen ValueError aus, bevor es etwas ändert; lerne hängt nur an,
# wenn self.aktiv gilt und die Adresse neu ist. beschreibung baut den Text mit einem f-String.
# Anderer Weg: in lerne mit if not self.aktiv: return früh aussteigen und erst danach prüfen, ob
# die Adresse neu ist. Die Prüfung des VLANs kann man auch als if not 1 <= vlan <= 4094 schreiben.
# Eine Menge (set) statt der Liste machte die Prüfung „schon bekannt“ schneller, die Aufgabe
# verlangt aber eine Liste in der Reihenfolge des Lernens.
# Typische Fehler: in einer Methode vlan = ... statt self.vlan = ... schreiben (dann entsteht nur
# eine lokale Variable), self in der Parameterliste vergessen (TypeError beim Aufruf), erst setzen
# und dann prüfen, beim Abschalten die Liste nicht leeren oder in beschreibung print statt return.
# Laufzeit: Jede Methode braucht O(1) Schritte, außer lerne: mac not in self.geraete sieht die Liste
# durch, also O(g) bei g gelernten Adressen (mit einer Menge wäre es O(1)).
