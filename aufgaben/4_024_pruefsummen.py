"""Aufgabe 4_024 – Prüfsummen                                   Stufe 4 ★★★★☆

Ein Werkzeug zur Integritätsprüfung erkennt, ob Angreifer Dateien auf
den Servern einer Firma verändert haben: Es berechnet für jede Datei
eine Prüfsumme mit SHA-256 und vergleicht sie mit der Prüfsumme aus
einer Liste bekannter, sauberer Dateien. Schon ein einziges geändertes
Byte ergibt eine völlig andere Prüfsumme. Auf hundert Servern liegen
aber oft dieselben Programmbibliotheken mit genau demselben Inhalt,
und die Prüfsumme wird immer wieder neu berechnet. Zwei Dekoratoren
sollen helfen: einer zählt, wie oft wirklich gerechnet wird, einer
merkt sich Ergebnisse. Vervollständigen Sie:

- `zaehle(funktion)` gibt eine Hüllfunktion zurück, die funktion mit
  allen Argumenten aufruft und ihr Ergebnis zurückgibt. Sie hat das
  Attribut aufrufe, das bei 0 beginnt und bei jedem Aufruf um 1
  wächst, auch wenn funktion eine Ausnahme auslöst.
- `zwischenspeicher(funktion)` gibt eine Hüllfunktion zurück, die
  sich in ihrem Attribut cache, einem Dictionary, jedes Ergebnis
  merkt. Schlüssel ist das Tupel (args, tuple(sorted(kwargs.items()))).
  Steht der Schlüssel schon im cache, gibt sie das gemerkte Ergebnis
  zurück, ohne funktion aufzurufen; sonst ruft sie funktion auf,
  merkt sich das Ergebnis und gibt es zurück. Löst funktion eine
  Ausnahme aus, wird nichts gemerkt und die Ausnahme weitergegeben.
  Das Attribut cache_leeren ist eine Funktion ohne Argumente, die den
  cache leert.

Jede dekorierte Funktion hat ihren eigenen Zähler und ihren eigenen
cache; beide Hüllfunktionen übernehmen mit functools.wraps Namen und
Docstring.

    def pruefsumme(daten):
        return hashlib.sha256(daten).hexdigest()

    gezaehlt = zaehle(pruefsumme)
    schnell = zwischenspeicher(gezaehlt)
    schnell(b"libssl 3.0")       →  "5be0…"   (gerechnet)
    schnell(b"libssl 3.0")       →  "5be0…"   (aus dem cache)
    schnell(b"libc 2.39")        →  "52cd…"   (gerechnet)
    gezaehlt.aufrufe             →  2
    len(schnell.cache)           →  2

Grenzen: Die dekorierten Funktionen bekommen 0 bis 10 Argumente nach
Position und nach Namen, alle hashbar (Zahlen, Texte, bytes, Tupel
daraus), und können jede Ausnahme auslösen, die von Exception abstammt.
Ihr Ergebnis kann jeder Wert sein, auch None, 0 oder ein leerer Text.
Bis zu 100 000 Aufrufe mit bis zu 10 000 verschiedenen Argumenten.

Hintergrund: Ein Dekorator kann sich zwischen den Aufrufen etwas
merken. Weil Funktionen in Python Objekte sind, kann man ihnen wie
jedem Objekt Attribute geben, auch der Hüllfunktion, die man gerade
definiert hat:

    import functools

    def merke_letztes(funktion):
        @functools.wraps(funktion)
        def huelle(*args, **kwargs):
            huelle.letztes = funktion(*args, **kwargs)
            return huelle.letztes
        huelle.letztes = None
        return huelle

Beim Aufruf sucht Python den Namen huelle in der umgebenden Funktion
(Closure, Aufgabe 4_021) und findet dort genau diese Hüllfunktion. So
hat jede dekorierte Funktion ihren eigenen Zustand, und man kann ihn
von außen ansehen: f.letztes. Wird merke_letztes für zwei Funktionen
aufgerufen, entstehen zwei verschiedene Hüllfunktionen mit je einem
eigenen Attribut. Eine Variable auf Modulebene dagegen würden sich
alle dekorierten Funktionen teilen. Auch eine Funktion kann man als
Attribut anhängen: huelle.zuruecksetzen = zuruecksetzen, wobei
zuruecksetzen eine innere Funktion ohne Argumente ist.

Ein Zwischenspeicher (Cache) lohnt sich, wenn dieselbe Funktion oft mit
denselben Argumenten aufgerufen wird und ihr Ergebnis nur von den
Argumenten abhängt. Als Schlüssel eines Dictionaries muss ein Wert
hashbar sein; args ist schon ein Tupel, kwargs ein Dictionary, darum
macht man daraus ein sortiertes Tupel von Paaren. Ob ein Ergebnis
schon gemerkt ist, prüft man mit schluessel in cache, nicht mit
cache.get(schluessel): Das Ergebnis selbst könnte None oder 0 sein.
Eine Ausnahme merkt man sich nicht, denn beim nächsten Versuch kann es
klappen. Python bringt mit functools.lru_cache einen fertigen Cache
mit; hier bauen Sie ihn selbst, um zu sehen, wie er arbeitet.
"""

import functools
import hashlib


def zaehle(funktion):
    """Dekorator: zählt im Attribut aufrufe, wie oft funktion aufgerufen wurde."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zwischenspeicher(funktion):
    """Dekorator: merkt sich die Ergebnisse von funktion im Attribut cache."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefsumme(daten):
    """Berechnet die SHA-256-Prüfsumme von daten als Text aus Hexadezimalziffern."""
    return hashlib.sha256(daten).hexdigest()


gezaehlt = zaehle(pruefsumme)
schnell = zwischenspeicher(gezaehlt)
for datei in [b"libssl 3.0", b"libssl 3.0", b"libc 2.39", b"libssl 3.0"]:
    print(schnell(datei)[:8])
print(gezaehlt.aufrufe, len(schnell.cache), schnell.__name__)
