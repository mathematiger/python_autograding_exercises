"""Aufgabe 5_008 – Speicherinventar                                Stufe 5 ★★★★★

Ein Rechenzentrum führt ein Inventar seiner Server und des
Arbeitsspeichers (RAM), der in jedem steckt. Die Angaben kommen aus
verschiedenen Quellen: Mal steht dort eine Zahl in MiB, mal ein Text wie
"16G" oder "512 m". Intern soll jeder Wert einfach eine ganze Zahl in MiB
sein, damit man ihn ohne Umrechnung vergleichen und addieren kann; nur
bei der Ausgabe soll er lesbar aussehen. Außerdem darf es im ganzen
Programm nur ein einziges Inventar geben: Jeder Programmteil, der
Inventar() schreibt, soll dasselbe Objekt mit denselben Daten bekommen.

Vervollständigen Sie:

- `Speicher(wert)` als Unterklasse von int. wert ist entweder eine ganze
  Zahl ab 0 (auch ein Speicher, aber nicht True oder False), die schon in
  MiB angegeben ist, oder ein Text aus einer Zahl und einer Einheit M, G
  oder T, ohne Rücksicht auf Groß- und Kleinschreibung und auf
  Leerzeichen am Rand und vor der Einheit. Dabei ist 1 G = 1024 M und
  1 T = 1024 G. Alles andere löst einen ValueError aus.
  `str(speicher)` zeigt den Wert in der größten Einheit, in der er eine
  ganze Zahl ist: "1 TiB", "16 GiB", "1536 MiB", "0 MiB".
- `Inventar()` gibt bei jedem Aufruf dasselbe Objekt zurück, und ein
  zweiter Aufruf darf die schon gespeicherten Server nicht löschen. Die
  Methoden: `hinzufuegen(name, ram)` speichert Speicher(ram) unter name,
  ValueError, wenn es name schon gibt; `ram(name)` gibt den Speicher
  dieses Servers zurück (KeyError, wenn es ihn nicht gibt); `gesamt()`
  gibt die Summe aller als Speicher zurück; `leeren()` entfernt alle
  Server.

    Speicher("16G")              →  16384
    isinstance(Speicher("16G"), int)  →  True
    str(Speicher(" 1 t "))       →  "1 TiB"
    str(Speicher(1536))          →  "1536 MiB"
    Speicher("1.5G")             →  ValueError
    Inventar() is Inventar()     →  True
    Inventar().hinzufuegen("db01", "64G")
    Inventar().hinzufuegen("web01", 8192)
    str(Inventar().gesamt())     →  "72 GiB"

Grenzen: Die Zahl in einem Text hat 1 bis 9 Ziffern, ganze Zahlen liegen
zwischen -10**12 und 10**12; wert kann außerdem ein beliebiges anderes
Objekt sein. Das Inventar hat bis zu 100 000 Server mit verschiedenen
Namen.

Hintergrund: Ein Objekt entsteht in zwei Schritten. Klasse(argumente)
ruft zuerst Klasse.__new__(Klasse, argumente) auf; diese statische
Methode erzeugt das Objekt und gibt es zurück. Ist das Ergebnis eine
Instanz der Klasse, ruft Python danach __init__(objekt, argumente) auf,
um es einzurichten. Fast immer genügt __init__; __new__ braucht man in
zwei Fällen.

Erstens bei unveränderlichen Typen wie int, str und tuple. Ihr Wert steht
schon fest, wenn __init__ läuft, und lässt sich dort nicht mehr ändern.
Eine Unterklasse, die ihren Wert umrechnen will, muss das in __new__ tun
und den fertigen Wert an die __new__ der Elternklasse geben:

    class Prozent(int):
        def __new__(cls, text):
            zahl = int(text.rstrip("%"))
            return super().__new__(cls, zahl)

        def __str__(self):
            return f"{int(self)} %"

    p = Prozent("42%")
    p + 1        →  43           (int-Rechnungen liefern gewöhnliche ints)
    str(p)       →  "42 %"

In __str__ steht int(self) statt self, weil f"{self}" wieder __str__
aufrufen würde. Mit Prozent rechnet man wie mit jeder Zahl; das Ergebnis
einer Rechnung ist aber wieder ein int, kein Prozent. Soll es ein Prozent
sein, muss man es ausdrücklich umwandeln.

Zweitens, wenn Klasse() nicht jedes Mal ein neues Objekt liefern soll,
etwa bei einem Singleton, von dem es nur ein Exemplar gibt. __new__ merkt
sich das erste Objekt in einem Klassenattribut und gibt danach immer
dieses zurück:

    class Einstellungen:
        _einziges = None

        def __new__(cls):
            if cls._einziges is None:
                cls._einziges = super().__new__(cls)
                cls._einziges.werte = {}
            return cls._einziges

Die Falle: Weil __new__ jedes Mal ein Objekt der Klasse zurückgibt, ruft
Python auch jedes Mal __init__ auf. Stünde self.werte = {} in __init__,
wären die Werte nach dem zweiten Einstellungen() wieder leer. Darum
richtet man das Objekt hier nur in __new__ ein, beim ersten Mal.
"""


class Speicher(int):
    """Eine Speichergröße in MiB, die sich aus "16G" oder 16384 erzeugen lässt und lesbar ausgibt."""

    EINHEITEN = {"M": 1, "G": 1024, "T": 1024 * 1024}

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Inventar:
    """Das einzige Inventar aller Server mit ihrem Arbeitsspeicher."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def hinzufuegen(self, name, ram):
        """Speichert Speicher(ram) unter name; ValueError, wenn es name schon gibt."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def ram(self, name):
        """Gibt den Speicher des Servers name zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def gesamt(self):
        """Gibt den Speicher aller Server zusammen als Speicher zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def leeren(self):
        """Entfernt alle Server."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(Speicher("16G"), int(Speicher("16G")), Speicher(1536))
Inventar().hinzufuegen("db01", "64G")
Inventar().hinzufuegen("web01", 8192)
print(Inventar() is Inventar(), Inventar().gesamt())
Inventar().leeren()
