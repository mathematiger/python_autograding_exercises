# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_010_reaktionszeit.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_010_reaktionszeit

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
  Reaktionszeit noch übrig sind. vergangen ist die Zahl der Minuten seit
  dem Eingang des Tickets. Ist die Frist überschritten, ist die
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

Grenzen: prioritaet und vergangen sind ganze Zahlen. Bei richtigen
Aufrufen ist prioritaet 1, 2 oder 3 und 0 ≤ vergangen ≤ 100 000. Eine
unbekannte Priorität oder eine negative Zeit kommt nur von
Programmierfehlern und löst den AssertionError aus.

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
    assert prioritaet in REAKTIONSZEIT, f"Unbekannte Priorität: {prioritaet}"
    assert vergangen >= 0, "Die vergangene Zeit darf nicht negativ sein"
    return REAKTIONSZEIT[prioritaet] - vergangen


def ampel(prioritaet, vergangen):
    """Gibt "grün", "gelb" oder "rot" zurück, je nachdem, wie viel Reaktionszeit noch übrig ist."""
    rest = restzeit(prioritaet, vergangen)
    if rest <= 0:
        return "rot"
    if rest <= REAKTIONSZEIT[prioritaet] / 2:
        return "gelb"
    return "grün"


for prioritaet, vergangen in [(1, 20), (2, 150), (3, 500)]:
    print(f"Priorität {prioritaet} nach {vergangen} Minuten: {restzeit(prioritaet, vergangen)} Minuten übrig,", ampel(prioritaet, vergangen))


# Idee: restzeit prüft mit zwei assert-Zeilen zuerst ihre Vorbedingungen (bekannte Priorität,
# keine negative Zeit) und rechnet dann Reaktionszeit minus vergangene Minuten. ampel ruft restzeit
# auf, sodass dieselben Prüfungen auch hier greifen, und vergleicht den Rest von oben nach unten:
# höchstens 0 ist rot, höchstens die Hälfte gelb, sonst grün.
#
# Anderer Weg: In ampel ohne Division vergleichen, z. B. gelb, wenn 2 * rest <= frist. Eine ampel,
# die restzeit gar nicht aufruft und nur mit vergangen rechnet, ist hier nicht erlaubt: Der Text
# verlangt restzeit, und ohne sie meldet ampel keine Programmierfehler (der Test merkt das).
#
# Typische Fehler: raise ValueError statt assert (falsche Ausnahme), < statt <= an den Grenzen
# (genau die Hälfte ist schon gelb, genau 0 schon rot) und in ampel die Prüfungen in der falschen
# Reihenfolge, sodass ein überschrittenes Ticket gelb statt rot wird. Und assert (bedingung,
# "Meldung") mit Klammern: Das Tupel ist immer wahr, die
# Prüfung greift nie (Python warnt nur mit einer SyntaxWarning).
#
# Laufzeit: O(1), es wird nur nachgeschlagen und verglichen.
