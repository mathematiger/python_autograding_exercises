"""Aufgabe 3_040 – Sensornetz                                    Stufe 3 ★★★☆☆

In einem Bürogebäude messen Funksensoren die Temperatur in den Räumen.
Die Gebäudesteuerung soll die Sensoren als Objekte verwalten: Jeder
Sensor hat eine Kennung, einen Raum und seinen letzten Messwert in Grad
Celsius. Ein Techniker hat festgestellt, dass alle Sensoren einer
Lieferung um denselben Betrag falsch messen; für die Auswertung soll
deshalb eine korrigierte Fassung des ganzen Netzes entstehen, ohne die
Originaldaten zu verändern.

Die Klasse `Sensor` mit `__init__` und `__str__` ist vorgegeben, ebenso
`Sensornetz.__init__`, das eine leere Liste `sensoren` anlegt.
Vervollständigen Sie:

- `Sensor.kalibriert(self, versatz)` gibt einen neuen Sensor mit
  derselben Kennung und demselben Raum zurück, dessen Wert um versatz
  größer ist. Der Sensor selbst bleibt unverändert.
- `Sensornetz.hinzufuegen(self, sensor)` hängt den Sensor an die Liste
  sensoren an.
- `Sensornetz.im_raum(self, raum)` gibt eine Liste der Sensoren in
  diesem Raum zurück, in der Reihenfolge des Hinzufügens. Es sind die
  Sensor-Objekte selbst, keine Kopien und keine Texte.
- `Sensornetz.waermster(self)` gibt den Sensor mit dem höchsten Wert
  zurück; haben mehrere denselben höchsten Wert, den zuerst
  hinzugefügten. Ohne Sensoren gibt es None zurück.
- `Sensornetz.kalibriert(self, versatz)` gibt ein neues Sensornetz
  zurück, das zu jedem Sensor den kalibrierten Sensor enthält, in
  derselben Reihenfolge. Das ursprüngliche Netz und seine Sensoren
  bleiben unverändert.

    netz = Sensornetz()
    netz.hinzufuegen(Sensor("T-01", "Büro 1", 21.5))
    netz.hinzufuegen(Sensor("T-02", "Serverraum", 24.0))
    netz.hinzufuegen(Sensor("T-03", "Büro 1", 22.5))
    [str(s) for s in netz.im_raum("Büro 1")]
        →  ["T-01 (Büro 1): 21.5 °C", "T-03 (Büro 1): 22.5 °C"]
    str(netz.waermster())             →  "T-02 (Serverraum): 24.0 °C"
    neu = netz.kalibriert(-0.5)
    str(neu.waermster())              →  "T-02 (Serverraum): 23.5 °C"
    str(netz.waermster())             →  "T-02 (Serverraum): 24.0 °C"

Grenzen: Ein Netz hat 0 bis 10 000 Sensoren. Werte sind Zahlen von -40
bis 125, versatz liegt zwischen -10 und 10. Kennungen sind eindeutig,
Räume sind beliebige Texte, und ein Raum kann auch keinen Sensor haben.

Hintergrund: Klassen mit __init__, Methoden und __str__ kennen Sie aus
den Aufgaben 3_037 und 3_039. Objekte lassen sich wie Zahlen oder Texte
in Listen speichern, als Argument übergeben und mit return zurückgeben.
Eine Methode darf auch ein neues Objekt ihrer eigenen Klasse anlegen und
zurückgeben, so wie hier eine Methode, die einen verschobenen Punkt
liefert:

    class Punkt:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def verschoben(self, dx):
            return Punkt(self.x + dx, self.y)

    p = Punkt(1, 2)
    q = p.verschoben(5)     # q ist ein neuer Punkt (6, 2), p bleibt (1, 2)

Wichtig ist der Unterschied zwischen „dasselbe Objekt“ und „ein neues
Objekt“: Steht ein Objekt in zwei Listen, sind das nicht zwei Kopien,
sondern zwei Verweise auf ein und dasselbe Objekt. Ändert man es über
die eine Liste, sieht man die Änderung auch über die andere. a is b
prüft, ob a und b dasselbe Objekt sind. Wer die Originaldaten behalten
will, darf deshalb die vorhandenen Sensoren nicht verändern, sondern
legt neue an.
"""


class Sensor:
    """Ein Temperatursensor mit Kennung, Raum und letztem Messwert (vorgegeben bis auf kalibriert)."""

    def __init__(self, kennung, raum, wert):
        self.kennung = kennung
        self.raum = raum
        self.wert = wert

    def __str__(self):
        """Gibt den Sensor als Text wie "T-01 (Büro 1): 21.5 °C" zurück."""
        return f"{self.kennung} ({self.raum}): {self.wert} °C"

    def kalibriert(self, versatz):
        """Gibt einen neuen Sensor zurück, dessen Wert um versatz größer ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Sensornetz:
    """Alle Sensoren eines Gebäudes in einer Liste."""

    def __init__(self):
        self.sensoren = []

    def hinzufuegen(self, sensor):
        """Hängt den Sensor an die Liste an."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def im_raum(self, raum):
        """Gibt die Liste der Sensoren in diesem Raum zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def waermster(self):
        """Gibt den Sensor mit dem höchsten Wert zurück, ohne Sensoren None."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def kalibriert(self, versatz):
        """Gibt ein neues Sensornetz mit allen Sensoren kalibriert zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


netz = Sensornetz()
netz.hinzufuegen(Sensor("T-01", "Büro 1", 21.5))
netz.hinzufuegen(Sensor("T-02", "Serverraum", 24.0))
netz.hinzufuegen(Sensor("T-03", "Büro 1", 22.5))
for sensor in netz.im_raum("Büro 1"):
    print(sensor)
print("Wärmster:", netz.waermster())
print("Korrigiert:", netz.kalibriert(-0.5).waermster())
