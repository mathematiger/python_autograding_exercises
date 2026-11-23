"""Aufgabe 5_034 – Alarmdrossel                                  Stufe 5 ★★★★★

Ein Monitoring-System hat für jeden überwachten Server einen eigenen
Alarmkanal, der SMS schickt oder die Rufbereitschaft anruft. Fällt ein
Server richtig aus, feuern seine Prüfungen im Sekundentakt, und ohne
Bremse bekäme die Bereitschaft Hunderte SMS. Darum soll jede
Alarm-Methode eines Kanals nur eine begrenzte Zahl von Malen wirklich
auslösen; weitere Aufrufe werden nur gezählt, bis jemand den Alarm
quittiert. Ein Ausfall von web01 darf dabei die Alarme von db01 nicht
bremsen. Schreiben Sie:

- `drosseln(maximal)`, eine Dekorator-Fabrik für Methoden. Die
  dekorierte Methode läuft für jedes Objekt höchstens maximal-mal und
  gibt dann ihr Ergebnis zurück. Jeder weitere Aufruf führt sie nicht
  aus, gibt None zurück und zählt als unterdrückt. Jedes Objekt und
  jede Methode hat eigene Zähler. Ein Aufruf, der mit einer Ausnahme
  endet, zählt als ausgeführt; die Ausnahme fliegt weiter. Name und
  Docstring der Methode bleiben erhalten (functools.wraps).
- `unterdrueckt(objekt, name)` gibt zurück, wie viele Aufrufe der
  Methode name bei diesem Objekt seit dem letzten Freigeben unterdrückt
  wurden (0, wenn sie nie aufgerufen wurde).
- `freigeben(objekt)` setzt alle Zähler dieses Objekts zurück; danach
  dürfen alle seine gedrosselten Methoden wieder maximal-mal laufen.
  Andere Objekte bleiben unberührt.

Der Zustand gehört ins Objekt selbst: Speichern Sie ihn im Attribut
_drossel des Objekts, nicht im Dekorator. Die Objekte haben ein
__dict__, können aber unhashbar sein (eine Klasse mit __eq__, aber ohne
__hash__).

    class Alarmkanal:
        def __init__(self, server):
            self.server = server
            self.gesendet = []

        @drosseln(2)
        def sms(self, text):
            self.gesendet.append(text)
            return len(self.gesendet)

    web, db = Alarmkanal("web01"), Alarmkanal("db01")
    web.sms("CPU 98 %")              →  1
    web.sms("CPU 99 %")              →  2
    web.sms("CPU 99 %")              →  None   (unterdrückt)
    db.sms("Platte voll")            →  1      (eigener Zähler)
    unterdrueckt(web, "sms")         →  1
    freigeben(web)
    web.sms("CPU 97 %")              →  3

Grenzen: 0 ≤ maximal ≤ 1000. Die Methoden bekommen beliebige
Positions- und Schlüsselwortargumente. Bis zu 10 000 Objekte und
100 000 Aufrufe. Dekoriert werden nur gewöhnliche Methoden, deren Namen
in einer Klasse nicht doppelt vorkommen.

Hintergrund: Ein Dekorator läuft genau einmal, wenn Python den
Klassenkörper ausführt, und nicht einmal je Objekt. Alles, was in
seinem Closure (Aufgabe 4_021) steht, teilen sich darum alle Objekte
der Klasse:

    def drosseln_falsch(maximal):
        def dekorator(methode):
            aufrufe = 0                      # gibt es nur einmal!
            @functools.wraps(methode)
            def huelle(self, *args, **kwargs):
                nonlocal aufrufe
                if aufrufe >= maximal:
                    return None
                aufrufe += 1
                return methode(self, *args, **kwargs)
            return huelle
        return dekorator

Hier bremst ein Ausfall von web01 auch db01. Der naheliegende Ausweg,
im Closure ein Dictionary {self: zaehler} zu führen, hat drei Haken:
Es hält jedes Objekt für immer am Leben (der Schlüssel ist eine starke
Referenz), es scheitert an unhashbaren Objekten mit TypeError, und mit
id(self) als Schlüssel bekäme ein neues Objekt die Zähler eines
gelöschten, weil Python Speicheradressen wiederverwendet.

Sauber ist, den Zustand dort abzulegen, wo er hingehört: im Objekt. Die
Hülle bekommt self ohnehin mit und kann in dessen __dict__ ein
Dictionary anlegen, unter einem Schlüssel je Methode:

    zustand = self.__dict__.setdefault("_drossel", {})
    zaehler = zustand.setdefault(methode.__name__, [0, 0])

setdefault liefert den vorhandenen Wert oder trägt den Standardwert
ein und liefert ihn; so legt der erste Aufruf alles an, ohne dass
__init__ davon wissen muss. So haben Sie es schon in Aufgabe 4_030 gemacht
(self.aufrufe) und Python selbst bei functools.cached_property (Aufgabe
5_033): Das Ergebnis liegt im __dict__ des Objekts, darum hat jedes
Objekt sein eigenes, es verschwindet mit dem Objekt, und vergessen
heißt, den Eintrag zu löschen. Der Preis: Klassen mit __slots__ (Aufgabe
5_004) haben kein __dict__, und der Name _drossel darf nicht mit einem
eigenen Attribut der Klasse zusammenstoßen; der führende Unterstrich
sagt, dass er nur intern benutzt wird.

Warum die Hülle überhaupt self bekommt, wissen Sie aus Aufgabe 5_002:
Eine Funktion ist ein Deskriptor, und obj.sms bindet sie an obj. Ein
Dekorator, der eine Funktion zurückgibt, erbt das von selbst.
"""

import functools


def drosseln(maximal):
    """Gibt einen Dekorator zurück, der eine Methode je Objekt höchstens maximal-mal ausführt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def unterdrueckt(objekt, name):
    """Gibt die Zahl der unterdrückten Aufrufe der Methode name bei diesem Objekt zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def freigeben(objekt):
    """Setzt alle Drossel-Zähler dieses Objekts zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Alarmkanal:
    """Schickt Alarme eines Servers an die Rufbereitschaft."""

    def __init__(self, server):
        """Merkt sich den Server und legt die Liste der gesendeten Texte an."""
        self.server = server
        self.gesendet = []

    @drosseln(2)
    def sms(self, text):
        """Schickt eine SMS und gibt die Zahl der bisher gesendeten Texte zurück."""
        self.gesendet.append(text)
        return len(self.gesendet)


web, db = Alarmkanal("web01"), Alarmkanal("db01")
print(web.sms("CPU 98 %"))
print(web.sms("CPU 99 %"))
print(web.sms("CPU 99 %"))
print(db.sms("Platte voll"))
print(unterdrueckt(web, "sms"))
freigeben(web)
print(web.sms("CPU 97 %"))
