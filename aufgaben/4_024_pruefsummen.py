"""Aufgabe 4_024 – Prüfsummen-Cache                             Stufe 4 ★★★★☆

Ein Firmenserver verteilt Installationspakete an die Arbeitsplätze. Damit
niemand ein manipuliertes Paket unterschiebt, wird vor jeder Auslieferung
die SHA-256-Prüfsumme des Pakets berechnet und mit der veröffentlichten
verglichen. Eine Prüfsumme (ein Hashwert) ist ein kurzer Fingerabdruck
der Daten: Ändert sich auch nur ein Byte, ändert sich die Prüfsumme
völlig. Weil dieselben Pakete hundertfach geladen werden, soll jede
Prüfsumme nur einmal berechnet und danach aus einem Zwischenspeicher
(Cache) beantwortet werden. Die Sicherheitsabteilung will außerdem
sehen, wie oft wirklich gerechnet wurde. Vervollständigen Sie zwei
Dekoratoren:

- `zaehle(funktion)` gibt eine Hüllfunktion zurück, die funktion mit
  allen Argumenten aufruft und ihr Ergebnis zurückgibt. Ihr Attribut
  `aufrufe` ist zu Beginn 0 und wächst bei jedem Aufruf um 1, auch wenn
  funktion eine Ausnahme auslöst; die Ausnahme wird weitergegeben.
- `zwischenspeicher(funktion)` gibt eine Hüllfunktion zurück, die sich
  zu jeder Folge von Argumenten das Ergebnis merkt. Kommen dieselben
  Argumente noch einmal, gibt sie das gemerkte Ergebnis zurück, ohne
  funktion aufzurufen, und erhöht ihr Attribut `treffer` (zu Beginn 0)
  um 1. Löst funktion eine Ausnahme aus, wird nichts gemerkt und die
  Ausnahme weitergegeben.
- Die Hüllfunktion von zwischenspeicher hat außerdem ein Attribut
  `leeren`, eine Funktion ohne Argumente, die alle gemerkten Ergebnisse
  vergisst (treffer bleibt dabei stehen). Das braucht man, wenn sich
  die Daten hinter der Funktion ändern, etwa nach einer Änderung der
  Zugriffsrechte, damit keine veralteten Antworten mehr kommen.
- Beide Hüllfunktionen tragen dank functools.wraps Namen, Docstring und
  `__wrapped__` der ursprünglichen Funktion.

    @zaehle
    def berechne_pruefsumme(inhalt):
        return hashlib.sha256(inhalt).hexdigest()

    pruefsumme = zwischenspeicher(berechne_pruefsumme)
    pruefsumme(b"office-2.4")[:12]   →  "6d0dae2a40d2"   (berechnet)
    pruefsumme(b"browser-118")[:12]  →  "68d3fe5a4898"   (berechnet)
    pruefsumme(b"office-2.4")[:12]   →  "6d0dae2a40d2"   (aus dem Speicher)
    berechne_pruefsumme.aufrufe      →  2
    pruefsumme.treffer               →  1

Grenzen: Die Funktionen unter zaehle bekommen beliebige Argumente nach
Position und nach Namen. Die Funktionen unter zwischenspeicher bekommen
0 bis 5 Argumente nur nach Position; das sind Texte, bytes, ganze
Zahlen oder Tupel daraus, also hashbar, und nie zwei verschiedene
Argumente, die gleich sind (wie 1 und 1.0). Das Ergebnis kann alles
sein, auch None, False oder 0. Beide dürfen jede Ausnahme auslösen, die
von Exception abstammt. Ein Zwischenspeicher merkt sich bis zu 100 000
Ergebnisse; jeder Aufruf der Hüllfunktion soll dabei außer dem Aufruf
von funktion nur O(1) Schritte brauchen.

Hintergrund: Dekoratoren (Aufgabe 4_022) sind der übliche Weg, einer
Funktion Verhalten hinzuzufügen, das mit ihrer eigentlichen Arbeit
nichts zu tun hat: Aufrufe zählen, protokollieren, Ergebnisse
zwischenspeichern. Der Code der Funktion bleibt dabei unverändert.

Funktionen sind in Python Objekte und können wie andere Objekte
Attribute bekommen. So kann eine Hülle ihren Zustand so ablegen, dass
man ihn von außen lesen kann:

    import functools

    def merke_letztes(funktion):
        @functools.wraps(funktion)
        def huelle(*args, **kwargs):
            huelle.letztes = funktion(*args, **kwargs)
            return huelle.letztes
        huelle.letztes = None
        return huelle

Die Hülle findet sich selbst über ihren Namen huelle, der in der
umgebenden Funktion steht (Closure, Aufgabe 4_021). Ein Attribut kann
auch eine Funktion sein, die mit den Variablen der Closure arbeitet.

Für einen Zwischenspeicher eignet sich ein Dictionary, dessen Schlüssel
das Tupel der Argumente ist: In der Hülle ist args schon genau dieses
Tupel. Nachschlagen mit in und mit [] braucht im Dictionary O(1)
Schritte, in einer Liste dagegen O(n). Vorsicht bei der Frage „steht das
schon im Speicher?“: speicher.get(args) ist auch dann None oder falsch,
wenn das gemerkte Ergebnis None, False oder 0 ist. Fragen Sie deshalb
mit args in speicher.

    speicher = {}
    if args in speicher:
        return speicher[args]

Lässt man das Dictionary als lokale Variable des Dekorators anlegen,
bekommt jede dekorierte Funktion ihren eigenen Speicher. Dekoratoren
lassen sich auch stapeln: Bei

    @zwischenspeicher
    @zaehle
    def f(x): ...

wird zuerst der untere angewendet, also f = zwischenspeicher(zaehle(f)).
Ausblick: Die Standardbibliothek hat einen fertigen Zwischenspeicher,
functools.lru_cache; er kommt in einer späteren Aufgabe. Ihn einmal
selbst zu bauen zeigt, was er im Inneren tut.
"""

import functools
import hashlib


def zaehle(funktion):
    """Dekorator: zählt im Attribut aufrufe der Hülle, wie oft funktion aufgerufen wurde."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zwischenspeicher(funktion):
    """Dekorator: merkt sich die Ergebnisse von funktion je Argumente; treffer zählt Antworten aus dem Speicher."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


@zaehle
def berechne_pruefsumme(inhalt):
    """Berechnet die SHA-256-Prüfsumme eines Pakets als Text aus 64 Hexziffern."""
    return hashlib.sha256(inhalt).hexdigest()


pruefsumme = zwischenspeicher(berechne_pruefsumme)

for paket in [b"office-2.4", b"browser-118", b"office-2.4", b"office-2.4"]:
    print(pruefsumme(paket)[:12])
print(berechne_pruefsumme.aufrufe, pruefsumme.treffer)
