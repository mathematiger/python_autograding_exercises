"""Aufgabe 3_010 – Reaktionszeit                                  Stufe 3 ★★★☆☆

Ein IT-Dienstleister hat mit seinen Kunden vereinbart, wie schnell er auf
eine Störungsmeldung reagiert. Diese Vereinbarung heißt Service Level
Agreement (SLA). Die Reaktionszeit hängt von der Priorität des Tickets ab:

    Priorität   Reaktionszeit
    1           60 Minuten
    2           240 Minuten
    3           480 Minuten

Das Ticketsystem zeigt neben jedem offenen Ticket eine Ampel an. Dafür
schreiben Sie zwei Funktionen:

- `restzeit(prioritaet, vergangen)` gibt zurück, wie viele Minuten von der
  Reaktionszeit noch übrig sind, wenn seit dem Eingang des Tickets
  vergangen Minuten verstrichen sind. Ist die Frist überschritten, ist die
  Restzeit negativ.
- `ampel(prioritaet, vergangen)` gibt "grün" zurück, wenn noch mehr als
  die Hälfte der Reaktionszeit übrig ist, "gelb", wenn noch etwas, aber
  höchstens die Hälfte übrig ist, und "rot", wenn keine Zeit mehr übrig
  ist. Benutzen Sie dafür restzeit.

Beide Funktionen werden nur innerhalb des Ticketsystems aufgerufen; die
Eingaben der Nutzer hat das System vorher schon geprüft. Eine unbekannte
Priorität oder eine negative Zeit kann also nur von einem Programmierfehler
kommen. restzeit soll solche Fehler sofort mit assert melden:

- Ist die Priorität nicht 1, 2 oder 3, lautet die Meldung zum Beispiel
  "Unbekannte Priorität: 4".
- Ist vergangen negativ, lautet sie "Die vergangene Zeit darf nicht
  negativ sein".

    restzeit(1, 20)    →  40
    restzeit(2, 300)   →  -60
    ampel(1, 20)       →  "grün"
    ampel(1, 30)       →  "gelb"
    ampel(1, 60)       →  "rot"
    restzeit(4, 20)    →  AssertionError: Unbekannte Priorität: 4

Hintergrund: Mit assert bedingung, "Meldung" behauptet man im Code, dass
etwas an dieser Stelle immer gilt. Ist die Bedingung wahr, passiert
nichts; ist sie falsch, löst Python einen AssertionError mit der Meldung
aus:

    def mittelwert(werte):
        assert len(werte) > 0, "Die Liste darf nicht leer sein"
        return sum(werte) / len(werte)

So schreibt man einen Vertrag zwischen einer Funktion und ihren
Aufrufern in den Code: Die Aufrufer versprechen, nur gültige Werte zu
übergeben (Vorbedingung), und die Funktion verspricht dafür ein richtiges
Ergebnis. Verletzt ein Aufrufer den Vertrag, fällt das sofort und an der
richtigen Stelle auf, statt dass das Programm mit falschen Werten
weiterrechnet. Anders als raise ValueError(...) aus Aufgabe 3_009 ist
assert für Programmierfehler gedacht, nicht für falsche Eingaben von
Nutzern: Startet man Python mit der Option -O, werden alle assert-Zeilen
übersprungen. Eine Eingabe von außen muss man deshalb immer mit if und
raise prüfen; assert prüft nur, was bei richtig geschriebenem Code nie
passieren dürfte.

Tipp: Die Tabelle steht schon als Dictionary REAKTIONSZEIT im Code.
"""

REAKTIONSZEIT = {1: 60, 2: 240, 3: 480}


def restzeit(prioritaet, vergangen):
    """Gibt die restlichen Minuten bis zum Ende der Reaktionszeit zurück, negativ bei Überschreitung."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ampel(prioritaet, vergangen):
    """Gibt "grün", "gelb" oder "rot" zurück, je nachdem, wie viel Reaktionszeit noch übrig ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for prioritaet, vergangen in [(1, 20), (2, 150), (3, 500)]:
    print(f"Priorität {prioritaet} nach {vergangen} Minuten: {restzeit(prioritaet, vergangen)} Minuten übrig,", ampel(prioritaet, vergangen))
