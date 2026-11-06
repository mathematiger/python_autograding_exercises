"""Aufgabe 5_016 – Benachrichtigungskanäle                       Stufe 5 ★★★★★

Im Ticketsystem eines IT-Dienstleisters wird ein Ticket eskaliert, wenn
seine Reaktionsfrist (SLA) abläuft: Die zuständige Bereitschaft muss
sofort erfahren, dass sie übernehmen soll. Dafür gibt es mehrere
Benachrichtigungskanäle, E-Mail, SMS, Chat und weitere, gebaut von
verschiedenen Teams und ohne gemeinsame Basisklasse. Das Ticketsystem
soll trotzdem mit jedem Kanal arbeiten können, der drei Dinge hat:

- ein Attribut `name` (Text), etwa "sms",
- ein Attribut `max_zeichen` (ganze Zahl): so lang darf eine Nachricht
  höchstens sein,
- eine Methode `sende(empfaenger, text)`, die True zurückgibt, wenn die
  Nachricht zugestellt wurde, sonst False.

Schreiben Sie:

- `Kanal`: ein Protokoll (typing.Protocol) mit genau diesen drei
  Bestandteilen, das man mit isinstance prüfen kann. Ein Objekt soll als
  Kanal gelten, sobald es alle drei hat, ohne von Kanal zu erben.
- `Protokollkanal`: einen Kanal, der nichts verschickt, sondern jede
  Nachricht als Tupel (empfaenger, text) an seine Liste `verlauf` hängt
  und immer True zurückgibt. Er heißt "protokoll", max_zeichen kommt aus
  dem Konstruktor (Standard 1000), und jedes Objekt hat seinen eigenen
  verlauf. Die Klasse erbt nicht von Kanal.
- `benachrichtige(kanaele, empfaenger, text)`: Ist ein Element von
  kanaele kein Kanal, löst die Funktion einen TypeError aus, dessen
  Meldung die Position des ersten solchen Elements enthält (ab 0
  gezählt), und zwar bevor irgendein Kanal etwas sendet. Sonst probiert
  sie die Kanäle der Reihe nach: Jeder bekommt den text, gekürzt auf
  seine max_zeichen (ist der text länger, die ersten max_zeichen - 1
  Zeichen und dahinter "…"). Der erste Kanal, dessen sende True
  zurückgibt, beendet die Suche; die Funktion gibt seinen name zurück.
  Gibt sende False zurück oder löst einen OSError aus (etwa wenn ein
  Server nicht erreichbar ist), ist der nächste Kanal dran. Andere
  Ausnahmen gibt die Funktion unverändert weiter. Klappt es bei keinem
  Kanal, gibt sie None zurück.

    text = "INC-4711: Reaktionsfrist abgelaufen, bitte übernehmen"
    benachrichtige([SMS(), EMail()], "+491701234567", text)        →  "sms"
    benachrichtige([SMS(), EMail()], "netz@firma.example", text)   →  "email"
    kurz = Protokollkanal(max_zeichen=10)
    benachrichtige([SMS(erreichbar=False), kurz], "+4930123", text)
        →  "protokoll"; kurz.verlauf == [("+4930123", "INC-4711:…")]
    isinstance(EMail(), Kanal), isinstance(Wandanzeige(), Kanal)   →  (True, False)
    benachrichtige([EMail(), Wandanzeige()], "a@b.example", text)
        →  TypeError, Meldung mit der Position 1

Grenzen: kanaele ist eine Liste mit 0 bis 1000 beliebigen Objekten
(aber keine Klassen). Hat ein Objekt name, max_zeichen und sende, dann
ist name ein Text, max_zeichen eine ganze Zahl von 1 bis 10 000 und
sende eine Methode, die True oder False zurückgibt oder eine Ausnahme
auslöst. empfaenger und text sind Texte mit 0 bis 10 000 Zeichen.
max_zeichen im Konstruktor von Protokollkanal ist eine ganze Zahl von 1
bis 10 000.

Hintergrund: Die meisten Sprachen mit Klassen fragen bei Typen nach der
Abstammung: Ein Objekt ist ein Kanal, wenn seine Klasse von Kanal erbt.
Das heißt nominale Typisierung, und so arbeitet auch abc.ABC aus Aufgabe
4_011. Python selbst fragt zur Laufzeit dagegen nur, ob ein Objekt kann,
was man von ihm will: for braucht __iter__, len() braucht __len__, und
woher die Methode stammt, ist egal („duck typing“: Was quakt wie eine
Ente, ist eine Ente). typing.Protocol schreibt genau diese Erwartung als
Typ auf. Das nennt man strukturelle Typisierung: Ein Objekt passt zu
einem Protokoll, wenn es dessen Bestandteile hat.

    from typing import Protocol

    class Druckbar(Protocol):
        seiten: int                       # ein Attribut: nur die Annotation

        def drucke(self) -> str:          # eine Methode: Rumpf ist ...
            ...

    class Bericht:                        # erbt nicht von Druckbar!
        def __init__(self):
            self.seiten = 3

        def drucke(self) -> str:
            return "Bericht"

    def ausgeben(etwas: Druckbar) -> None:
        print(etwas.drucke())

    ausgeben(Bericht())                   # für mypy in Ordnung

Die Methoden eines Protokolls haben keinen Rumpf, nur ... (Ellipsis),
denn das Protokoll beschreibt, implementiert aber nichts. Attribute
stehen nur als Annotation da. Ein Typprüfer wie mypy vergleicht bei
ausgeben(Bericht()) die Bestandteile: Fehlt drucke oder hat es die
falsche Signatur, meldet er einen Fehler, ohne dass Bericht von
Druckbar erben müsste. So kann man Schnittstellen für Klassen
beschreiben, die man nicht ändern kann oder will, etwa aus fremden
Bibliotheken. Erbt eine Klasse trotzdem ausdrücklich vom Protokoll, ist
sie eine gewöhnliche Unterklasse; nötig ist das nie.

Zur Laufzeit sind Annotationen nur Hinweise; Python prüft sie nicht.
Darum löst isinstance(Bericht(), Druckbar) einen TypeError aus, solange
man nicht ausdrücklich erlaubt, das Protokoll zur Laufzeit zu prüfen.
Das tut der Dekorator runtime_checkable:

    from typing import Protocol, runtime_checkable

    @runtime_checkable
    class Druckbar(Protocol):
        seiten: int
        def drucke(self) -> str: ...

    isinstance(Bericht(), Druckbar)       →  True
    isinstance("Text", Druckbar)          →  False   (kein drucke, kein seiten)

Ein solches isinstance prüft nur, ob alle Bestandteile als Attribute
vorhanden sind, nicht ihre Typen oder Signaturen: Ein Objekt mit
seiten = "viele" und einer Methode drucke(self, x, y) gilt ebenfalls
als Druckbar. Hat ein Protokoll Attribute und nicht nur Methoden,
funktioniert issubclass(Bericht, Druckbar) nicht (TypeError), denn
Attribute, die erst in __init__ entstehen, sieht man der Klasse nicht
an; isinstance auf einem Objekt geht dagegen. Und isinstance mit einem
Protokoll ist deutlich langsamer als mit einer gewöhnlichen Klasse, weil
Python jedes Mal alle Bestandteile nachschlägt.

Wann was? abc.ABC, wenn die Klassen ohnehin zu Ihnen gehören und eine
gemeinsame Basis mit fertigen Methoden sinnvoll ist; die Abstammung
wird dann ausdrücklich erklärt. Protocol, wenn nur zählt, was ein Objekt
kann, und die Klassen unabhängig voneinander entstehen.
"""

from typing import Protocol, runtime_checkable

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class EMail:
    """Kanal des Mail-Teams: stellt an Adressen mit @ zu."""

    def __init__(self):
        self.name = "email"
        self.max_zeichen = 2000
        self.postausgang = []

    def sende(self, empfaenger, text):
        """Legt die Nachricht in den Postausgang, wenn empfaenger eine Mailadresse ist."""
        if "@" not in empfaenger:
            return False
        self.postausgang.append((empfaenger, text))
        return True


class SMS:
    """Kanal des Telefonie-Teams: stellt an Nummern mit + zu, solange das Gateway erreichbar ist."""

    name = "sms"
    max_zeichen = 160

    def __init__(self, erreichbar=True):
        self.erreichbar = erreichbar
        self.gesendet = []

    def sende(self, empfaenger, text):
        """Schickt eine SMS an eine Nummer im Format +49…; ohne Gateway ein OSError."""
        if not self.erreichbar:
            raise OSError("SMS-Gateway nicht erreichbar")
        if not empfaenger.startswith("+"):
            return False
        self.gesendet.append((empfaenger, text))
        return True


class Wandanzeige:
    """Bildschirm im Leitstand; hat kein max_zeichen und ist deshalb kein Kanal."""

    name = "wand"

    def sende(self, empfaenger, text):
        """Zeigt den Text an."""
        return True


class Protokollkanal:
    """Kanal, der Nachrichten nur in seinem verlauf sammelt."""

    def __init__(self, max_zeichen=1000):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def sende(self, empfaenger, text):
        """Hängt (empfaenger, text) an verlauf und gibt True zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def benachrichtige(kanaele, empfaenger, text):
    """Probiert die Kanäle der Reihe nach; gibt den Namen des ersten erfolgreichen zurück oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


text = "INC-4711: Reaktionsfrist abgelaufen, bitte übernehmen"
print(benachrichtige([SMS(), EMail()], "+491701234567", text))
print(benachrichtige([SMS(), EMail()], "netz@firma.example", text))
kurz = Protokollkanal(max_zeichen=10)
print(benachrichtige([SMS(erreichbar=False), kurz], "+4930123", text), kurz.verlauf)
print(isinstance(EMail(), Kanal), isinstance(Wandanzeige(), Kanal))
try:
    benachrichtige([EMail(), Wandanzeige()], "a@b.example", text)
except TypeError:
    print("TypeError")
