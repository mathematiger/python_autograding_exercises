"""Aufgabe 4_007 – Ticketpriorität                              Stufe 4 ★★★★☆

Im IT-Support bekommt jede Störung ein Ticket. Welche Störung zuerst
bearbeitet wird, legt die Priorität fest, und die ergibt sich aus zwei
Einschätzungen: der Auswirkung (wie viele Personen oder Systeme betroffen
sind) und der Dringlichkeit (wie schnell es ohne Lösung teuer wird). Beide
werden in drei Stufen angegeben, 1 heißt hoch, 3 heißt niedrig. Daraus
entsteht nach der Prioritätenmatrix eine Priorität von 1 (kritisch) bis 5
(kann warten):

                     Dringlichkeit 1   Dringlichkeit 2   Dringlichkeit 3
    Auswirkung 1            1                 2                 3
    Auswirkung 2            2                 3                 4
    Auswirkung 3            3                 4                 5

Die Klasse `Ticket` braucht dafür zwei Hilfsfunktionen, die weder ein
Ticket-Objekt noch die Klasse brauchen; sie sollen deshalb statische
Methoden der Klasse werden:

- `berechne_prioritaet(auswirkung, dringlichkeit)` (Gerüst vorgegeben)
  gibt die Priorität nach der Matrix zurück. Ist einer der beiden Werte
  nicht 1, 2 oder 3, löst sie einen ValueError aus.
- `ist_ticketnummer(text)` schreiben Sie ganz selbst, mit Dekorator. Sie
  gibt True zurück, wenn text eine gültige Ticketnummer ist: die Buchstaben
  INC und dahinter genau sechs Ziffern, z. B. "INC004711". Sonst False.
- `__init__(self, nummer, auswirkung, dringlichkeit)` löst einen
  ValueError aus, wenn nummer keine gültige Ticketnummer ist, und speichert
  sonst die Attribute `nummer` und `prioritaet`. Benutzen Sie dafür die
  beiden statischen Methoden.

    Ticket.berechne_prioritaet(1, 2)   →  2
    Ticket.berechne_prioritaet(3, 3)   →  5
    Ticket.berechne_prioritaet(0, 2)   →  ValueError
    Ticket.ist_ticketnummer("INC004711")  →  True
    Ticket.ist_ticketnummer("INC4711")    →  False
    ticket = Ticket("INC004711", 2, 1)
    ticket.prioritaet                  →  2
    ticket.reaktionszeit()             →  4   (Stunden, vorgegeben)
    Ticket("REQ004711", 2, 1)          →  ValueError

Grenzen: `auswirkung` und `dringlichkeit` sind ganze Zahlen mit
-100 ≤ wert ≤ 100; alles außer 1, 2 und 3 muss einen ValueError auslösen.
`text` und `nummer` sind Texte aus höchstens 20 ASCII-Zeichen (Buchstaben,
Ziffern 0 bis 9, Satzzeichen, Leerzeichen), auch der leere Text.

Hintergrund: Eine normale Methode bekommt beim Aufruf das Objekt als self,
eine Klassenmethode (@classmethod, Aufgabe 4_006) die Klasse als cls. Manche
Funktionen brauchen keins von beiden: Sie rechnen nur mit ihren Argumenten.
Man könnte sie als gewöhnliche Funktion neben die Klasse schreiben. Gehören
sie aber inhaltlich zur Klasse, macht man sie mit dem Dekorator
@staticmethod zu einer statischen Methode. Sie hat weder self noch cls als
ersten Parameter:

    class Temperatur:
        def __init__(self, celsius):
            if not Temperatur.ist_moeglich(celsius):
                raise ValueError("Unter dem absoluten Nullpunkt")
            self.celsius = celsius

        @staticmethod
        def ist_moeglich(celsius):
            return celsius >= -273.15

    Temperatur.ist_moeglich(-300)      # False, ganz ohne Objekt
    t = Temperatur(20)
    t.ist_moeglich(25)                 # True, auch über ein Objekt

Man ruft sie über die Klasse oder über ein Objekt auf; Python übergibt in
keinem Fall automatisch etwas. Innerhalb der Klasse schreibt man
self.ist_moeglich(...) oder Temperatur.ist_moeglich(...). Der Vorteil:
Die Hilfsfunktion steht dort, wo man sie sucht, man kann sie einzeln testen,
und andere Programmteile können sie benutzen, ohne erst ein Objekt zu
erzeugen, etwa um eine Eingabe im Formular schon vor dem Anlegen eines
Tickets zu prüfen. Vergisst man den Dekorator, behandelt Python die erste
Variable als self, und der Aufruf über ein Objekt geht schief.

Tipp: text[:3] liefert die ersten drei Zeichen, text[3:] den Rest,
text.isdigit() prüft, ob ein Text nur aus Ziffern besteht. Die Priorität
in der Matrix ist auswirkung + dringlichkeit - 1.
"""


class Ticket:
    """Ein Störungsticket mit Nummer und Priorität."""

    REAKTIONSZEIT = {1: 1, 2: 4, 3: 8, 4: 24, 5: 72}

    def __init__(self, nummer, auswirkung, dringlichkeit):
        """Prüft die Nummer und berechnet die Priorität."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @staticmethod
    def berechne_prioritaet(auswirkung, dringlichkeit):
        """Gibt die Priorität 1 bis 5 nach der Prioritätenmatrix zurück."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def reaktionszeit(self):
        """Gibt zurück, nach wie vielen Stunden spätestens jemand reagieren muss."""
        return self.REAKTIONSZEIT[self.prioritaet]

    def __repr__(self):
        """Liefert z. B. Ticket('INC004711', Priorität 2)."""
        return f"Ticket({self.nummer!r}, Priorität {self.prioritaet})"


print(Ticket.berechne_prioritaet(1, 2))
print(Ticket.ist_ticketnummer("INC004711"), Ticket.ist_ticketnummer("INC4711"))
ticket = Ticket("INC004711", 2, 1)
print(ticket, ticket.reaktionszeit())
