"""Aufgabe 3_037 – MAC-Tabelle                                   Stufe 3 ★★★☆☆

Ein Switch verbindet mehrere Geräte in einem Netzwerk über seine Ports
(Anschlüsse, nummeriert ab 1). Jedes Gerät hat eine feste Hardware-Adresse,
die MAC-Adresse, etwa "3c:52:82:1a:0f:7e". Der Switch lernt mit: Kommt auf
Port 3 ein Datenpaket von einem Gerät an, merkt er sich in seiner
MAC-Tabelle „dieses Gerät hängt an Port 3“. Pakete an dieses Gerät schickt
er danach nur noch auf Port 3 hinaus statt an alle. Steckt jemand das
Gerät an einen anderen Port um, gilt beim nächsten Paket der neue Port.

Vervollständigen Sie die Klasse `MacTabelle`:

- `__init__(self, anzahl_ports)` speichert die Anzahl der Ports im
  Attribut `anzahl_ports` und legt im Attribut `eintraege` ein leeres
  Dictionary an (MAC-Adresse → Port).
- `lerne(self, mac, port)` trägt ein, dass mac an port hängt; ein alter
  Eintrag für mac wird überschrieben. Ist port keine Nummer von 1 bis
  anzahl_ports, löst die Methode einen ValueError aus und ändert nichts.
- `port_fuer(self, mac)` gibt den gelernten Port zurück, oder None, wenn
  mac unbekannt ist (dann muss der Switch das Paket an alle schicken).
- `geraete_an(self, port)` gibt die MAC-Adressen aller Geräte an diesem
  Port als alphabetisch sortierte Liste zurück.

    switch = MacTabelle(8)
    switch.lerne("3c:52:82:1a:0f:7e", 3)
    switch.lerne("00:1b:44:11:3a:b7", 3)
    switch.port_fuer("3c:52:82:1a:0f:7e")  →  3
    switch.port_fuer("aa:aa:aa:aa:aa:aa")  →  None
    switch.geraete_an(3)  →  ["00:1b:44:11:3a:b7", "3c:52:82:1a:0f:7e"]
    switch.lerne("00:1b:44:11:3a:b7", 5)   (Gerät umgesteckt)
    switch.geraete_an(3)  →  ["3c:52:82:1a:0f:7e"]
    switch.lerne("00:1b:44:11:3a:b7", 9)   →  ValueError

Grenzen: 1 ≤ anzahl_ports ≤ 48. Eine MAC-Adresse ist ein Text aus sechs
Paaren von Kleinbuchstaben a bis f oder Ziffern, getrennt durch
Doppelpunkte. port ist bei allen Methoden eine ganze Zahl von -100 bis 100
(also auch 0, negativ oder zu groß). Eine Tabelle bekommt bis zu 10 000
Aufrufe von lerne und port_fuer; port_fuer soll dabei nicht die ganze
Tabelle durchsuchen, sondern im Dictionary nachschlagen.

Hintergrund: Bisher lagen Daten und die Funktionen, die mit ihnen
arbeiten, getrennt. Eine Klasse bündelt beides (MIT 6.0001, Lecture 8):
Sie ist ein Bauplan, nach dem man beliebig viele Objekte erzeugen kann,
hier eine Tabelle pro Switch. Jedes Objekt hat eigene Daten, die
Attribute, und kann Methoden ausführen, das sind Funktionen, die in der
Klasse stehen.

    class Zaehler:
        def __init__(self, start):
            self.stand = start            # Attribut stand anlegen

        def erhoehe(self, schritt):
            self.stand = self.stand + schritt

    z = Zaehler(10)      # erzeugt ein Objekt und ruft __init__ auf
    z.erhoehe(5)         # ruft erhoehe mit self = z und schritt = 5 auf
    z.stand              →  15

Ein Objekt erzeugt man, indem man die Klasse wie eine Funktion aufruft.
Python ruft dann automatisch `__init__` auf, das die Attribute anlegt.
Jede Methode bekommt als ersten Parameter `self`, das Objekt, mit dem sie
aufgerufen wurde; beim Aufruf `z.erhoehe(5)` setzt Python es selbst ein.
Über `self.name` liest und schreibt eine Methode die Attribute genau
dieses Objekts. Zwei Objekte derselben Klasse haben getrennte Attribute:
Was `lerne` in die Tabelle des einen Switches schreibt, steht nicht in
der Tabelle eines anderen. Fehler auslösen mit raise kennen Sie aus
Aufgabe 3_009.

Tipp: sorted(...) liefert eine neue, sortierte Liste. In einem Dictionary
durchläuft for mac, port in self.eintraege.items() alle Einträge.
"""


class MacTabelle:
    """Die MAC-Tabelle eines Switches: welches Gerät an welchem Port hängt."""

    def __init__(self, anzahl_ports):
        """Legt eine leere Tabelle für einen Switch mit anzahl_ports Ports an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def lerne(self, mac, port):
        """Merkt sich, dass das Gerät mac an port hängt; ValueError bei ungültigem Port."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def port_fuer(self, mac):
        """Gibt den Port des Geräts mac zurück, oder None, wenn es unbekannt ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def geraete_an(self, port):
        """Gibt die MAC-Adressen aller Geräte an port alphabetisch sortiert zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


switch = MacTabelle(8)
switch.lerne("3c:52:82:1a:0f:7e", 3)
switch.lerne("00:1b:44:11:3a:b7", 3)
print(switch.port_fuer("3c:52:82:1a:0f:7e"), switch.geraete_an(3))
