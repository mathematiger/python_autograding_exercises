"""Aufgabe 4_036 – Firewallprotokoll                             Stufe 4 ★★★★☆

Die Firewall eines Firmennetzes schreibt für jedes Paket, über das sie
entscheidet, eine Zeile in ihr Protokoll: ob sie es durchgelassen
(ACCEPT) oder verworfen (DROP) hat, die IP-Adresse des Absenders, das
Ziel mit Port (die Nummer des Dienstes, etwa 22 für SSH oder 443 für
HTTPS) und die Größe in Byte:

    # Protokoll fw-01
    ACCEPT 10.0.0.12 10.0.1.5:443 1500

    DROP 203.0.113.7 10.0.1.5:22 60

Leerzeilen und Kommentarzeilen, die mit # beginnen, gehören nicht dazu.
Das Protokoll ist sehr lang und wächst ständig weiter; es wird darum
nicht als Ganzes eingelesen, sondern Zeile für Zeile durch eine Kette von
Generatoren geschickt. Schreiben Sie die Stufen dieser Kette als
Generatorfunktionen. Jede bekommt ein Iterable und liefert erst dann den
nächsten Wert, wenn er abgeholt wird:

- `lies(zeilen)` liefert jede Zeile ohne Leerzeichen und Zeilenumbruch am
  Anfang und Ende, Leerzeilen und Kommentarzeilen nicht.
- `zerlege(zeilen)` macht aus jeder Zeile ein Tupel
  (aktion, absender, ziel, port, groesse) mit port und groesse als int.
- `verworfen(pakete)` liefert nur die Tupel mit der Aktion "DROP".

Dazu kommt die Funktion `erste_angreifer(zeilen, anzahl)`, die die
Kette zusammensteckt und eine Liste der Absender der ersten anzahl
verworfenen Pakete zurückgibt. Sie darf nur so viele Zeilen lesen, wie
sie dafür braucht, denn zeilen kann ein Protokoll sein, das nie endet.

    zeilen = ["# Protokoll fw-01", "ACCEPT 10.0.0.12 10.0.1.5:443 1500", "",
              "DROP 203.0.113.7 10.0.1.5:22 60\\n", "DROP 198.51.100.3 10.0.1.9:3389 52"]
    list(lies(zeilen))  →  ["ACCEPT 10.0.0.12 10.0.1.5:443 1500",
                            "DROP 203.0.113.7 10.0.1.5:22 60",
                            "DROP 198.51.100.3 10.0.1.9:3389 52"]
    next(zerlege(lies(zeilen)))  →  ("ACCEPT", "10.0.0.12", "10.0.1.5", 443, 1500)
    erste_angreifer(zeilen, 1)   →  ["203.0.113.7"]
    erste_angreifer(zeilen, 5)   →  ["203.0.113.7", "198.51.100.3"]

Grenzen: zeilen ist ein beliebiges Iterable von Texten, endlich mit bis
zu 100 000 Zeilen oder unendlich. Jede Zeile, die nach dem Entfernen der
Leerzeichen nicht leer ist und nicht mit # beginnt, hat genau die Form
oben: Aktion ACCEPT oder DROP, Absender, Ziel:Port und Größe, durch je
ein Leerzeichen getrennt; Port und Größe sind ganze Zahlen von 0 bis
65 535. 0 ≤ anzahl ≤ 10 000. Ist zeilen endlich und enthält weniger
verworfene Pakete als anzahl, kommen alle zurück.

Hintergrund: Ein Generator rechnet erst, wenn jemand next() aufruft
(Aufgabe 4_034). Bekommt ein Generator als Eingabe wieder einen
Generator, entsteht eine Pipeline, wie sie die Shell mit | kennt:

    def quadrate(zahlen):
        for zahl in zahlen:
            yield zahl * zahl

    def nur_gerade(zahlen):
        for zahl in zahlen:
            if zahl % 2 == 0:
                yield zahl

    kette = nur_gerade(quadrate(range(10**12)))
    next(kette)   →  0
    next(kette)   →  4

Beim Aufbau der Kette passiert noch gar nichts. Erst next(kette) fragt
nur_gerade nach einem Wert, nur_gerade fragt quadrate, quadrate fragt
range, und so wandert immer ein einzelner Wert durch alle Stufen. Darum
ist die riesige range kein Problem: Es werden nur so viele Zahlen
erzeugt, wie man am Ende abholt, und im Speicher liegt immer nur ein
Wert je Stufe. Jede Stufe ist klein, für sich testbar und lässt sich
mit anderen neu kombinieren.

Würde eine Stufe dagegen mit list(...) oder einer Liste und append
alles auf einmal sammeln, müsste sie die ganze Eingabe lesen, bevor die
nächste Stufe den ersten Wert bekommt, und bei einer unendlichen Eingabe
käme sie nie an. Um von einer Pipeline nur die ersten k Werte zu nehmen,
hilft zip(range(k), kette) aus Aufgabe 4_034: zip hört auf, sobald
range(k) leer ist, und fragt die Kette nur k-mal.

Text zerlegt man mit split (Aufgabe 2_015); zeile.split(" ", 3) teilt
höchstens dreimal, zeile.rpartition(":") an dem letzten Doppelpunkt.
"""


def lies(zeilen):
    """Liefert die Zeilen ohne Rand-Leerzeichen, ohne Leer- und Kommentarzeilen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zerlege(zeilen):
    """Liefert für jede Zeile ein Tupel (aktion, absender, ziel, port, groesse)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def verworfen(pakete):
    """Liefert nur die Pakete mit der Aktion DROP."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def erste_angreifer(zeilen, anzahl):
    """Gibt die Absender der ersten anzahl verworfenen Pakete als Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = [
    "# Protokoll fw-01",
    "ACCEPT 10.0.0.12 10.0.1.5:443 1500",
    "",
    "DROP 203.0.113.7 10.0.1.5:22 60\n",
    "DROP 198.51.100.3 10.0.1.9:3389 52",
]
print(list(lies(protokoll)))
print(next(zerlege(lies(protokoll))))
print(erste_angreifer(protokoll, 5))
