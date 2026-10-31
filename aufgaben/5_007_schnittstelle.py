"""Aufgabe 5_007 – Netzwerkschnittstelle                           Stufe 5 ★★★★★

Ein Werkzeug zur Netzwerkverwaltung hält für jeden Router die
Einstellungen seiner Schnittstellen (englisch Interfaces) als Objekte:
die IP-Adresse, die MTU (die größte Paketgröße in Byte, die über die
Leitung geht) und ob die Schnittstelle aktiv ist. Bei einer Störung will
das Betriebsteam später nachvollziehen, wer wann was umgestellt hat; und
ist eine Konfiguration einmal abgenommen und ausgerollt, darf niemand sie
mehr versehentlich ändern.

Vervollständigen Sie die Klasse `Schnittstelle`, sodass sie jede
Änderung selbst überwacht:

- `__init__(self, name, **werte)`: name (zum Beispiel "eth0") ist danach
  unveränderlich. Jedes Feld aus FELDER bekommt seinen Wert aus werte
  oder sonst den Standardwert aus FELDER. Diese ersten Werte werden
  geprüft wie jede spätere Zuweisung, aber nicht protokolliert. Am Ende
  sind protokoll eine leere Liste und gesperrt False.
- Zuweisung `s.feld = wert`: Ist die Schnittstelle gesperrt, kommt ein
  AttributeError. Ist feld kein Feld aus FELDER (auch name, protokoll,
  gesperrt oder ein Tippfehler wie s.mut), kommt ein AttributeError. Für
  mtu sind nur ganze Zahlen von 68 bis 9216 erlaubt (True und False
  nicht), sonst ein ValueError. Ändert sich der Wert wirklich, wird das
  Tupel (feld, alt, neu) an protokoll angehängt; bei gleichem Wert nicht.
- `del s.feld` setzt ein Feld aus FELDER auf seinen Standardwert zurück,
  mit Protokolleintrag, wenn sich dabei der Wert ändert. Für alle anderen
  Namen und bei gesperrter Schnittstelle kommt ein AttributeError.
- `sperren()` setzt gesperrt auf True. Danach lässt sich nichts mehr
  zuweisen oder löschen, auch nicht mit den Mitteln oben.

    s = Schnittstelle("eth0", ip="10.0.0.1")
    s.mtu                 →  1500
    s.mtu = 9000
    s.aktiv = True
    s.aktiv = True        (kein neuer Eintrag)
    del s.mtu
    s.protokoll           →  [("mtu", 1500, 9000), ("aktiv", False, True), ("mtu", 9000, 1500)]
    s.mut = 1400          →  AttributeError
    s.mtu = 10000         →  ValueError
    s.name = "eth1"       →  AttributeError
    s.sperren()
    s.ip = "10.0.0.2"     →  AttributeError

Grenzen: Die Werte für ip und aktiv werden nicht geprüft. Werte für mtu
können beliebige Objekte sein. Eine Schnittstelle erlebt bis zu 100 000
Zuweisungen; die Namen in werte sind Felder aus FELDER.

Hintergrund: Jede Zuweisung obj.name = wert ruft
type(obj).__setattr__(obj, "name", wert) auf, jedes del obj.name ruft
__delattr__(obj, "name"). Die Standardfassungen von object schreiben in
das __dict__ des Objekts (oder rufen den __set__ eines Deskriptors auf,
Aufgabe 5_001). Wer sie überschreibt, sieht jede Zuweisung, auch die in
__init__ und in den eigenen Methoden:

    class Protokolliert:
        def __setattr__(self, name, wert):
            print(f"{name} = {wert!r}")
            super().__setattr__(name, wert)

    p = Protokolliert()
    p.x = 5         gibt "x = 5" aus und speichert dann
    p.x += 1        liest wie gewohnt (5), gibt "x = 6" aus

Im Inneren darf man nicht self.name = wert schreiben, sonst ruft sich
__setattr__ endlos selbst auf. Gespeichert wird über die Fassung der
Elternklasse: super().__setattr__(name, wert) oder gleichbedeutend
object.__setattr__(self, name, wert). Dasselbe gilt für __delattr__ mit
super().__delattr__(name). Lesen ist davon nicht betroffen: Ein
überschriebenes __setattr__ ändert nichts an obj.name, und self.protokoll
liest wie immer.

Genau dieser Umweg ist auch die Hintertür für die eigene Klasse: Der
eigene Code legt seine inneren Attribute mit object.__setattr__ an,
während alle anderen über das geprüfte __setattr__ müssen. So arbeiten
auch die unveränderlichen Datenklassen mit frozen=True (Aufgabe 4_014):
Ihr __setattr__ löst immer einen Fehler aus, und ihr erzeugtes __init__
benutzt object.__setattr__. Ganz dicht ist das in Python nie; wer
unbedingt will, kommt mit object.__setattr__ auch von außen an die
Attribute. Es schützt vor Versehen, nicht vor Absicht.
"""


class Schnittstelle:
    """Einstellungen einer Netzwerkschnittstelle, die jede Änderung prüft und protokolliert."""

    # Feld → Standardwert
    FELDER = {"ip": "0.0.0.0", "mtu": 1500, "aktiv": False}

    def __init__(self, name, **werte):
        """Legt name, die Felder aus FELDER, ein leeres Protokoll und gesperrt = False an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __setattr__(self, feld, wert):
        """Lässt nur geprüfte Änderungen der Felder aus FELDER zu und protokolliert sie."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __delattr__(self, feld):
        """Setzt ein Feld aus FELDER auf seinen Standardwert zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def sperren(self):
        """Verhindert jede weitere Änderung."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


s = Schnittstelle("eth0", ip="10.0.0.1")
s.mtu = 9000
s.aktiv = True
s.aktiv = True
del s.mtu
print(s.name, s.ip, s.mtu, s.aktiv)
print(s.protokoll)
s.sperren()
try:
    s.ip = "10.0.0.2"
except AttributeError:
    print("gesperrt")
