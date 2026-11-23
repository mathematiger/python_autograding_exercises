"""Aufgabe 1_048 – Druckerwartung                                Stufe 1 ★☆☆☆☆

Der IT-Service betreut die Multifunktionsdrucker einer Firma. Jeder
Drucker zählt die gedruckten Seiten, und alle 50 000 Seiten kommt ein
Techniker zur Wartung: bei 50 000, 100 000, 150 000 Seiten und so
weiter. Damit der Termin rechtzeitig steht, soll er bestellt werden,
sobald bis zur nächsten Wartung höchstens 2000 Seiten fehlen.

Ein Kollege hat das Programm unten geschrieben, aber nichts erklärt.
Bevor es an alle Standorte geht, soll es dokumentiert werden. Ergänzen
Sie:

- In naechste_wartung einen Docstring, der sagt, was die Funktion
  zurückgibt; darin kommen die Wörter Zählerstand und Wartung vor.
- Darunter, direkt über der return-Zeile, einen Kommentar, der erklärt,
  warum dort + 1 steht. (Überlegen Sie, was bei genau 100 000 Seiten
  herauskommen soll.)
- Die Funktion wartung_bald: ein Docstring, der sagt, wann sie True
  zurückgibt, und eine return-Zeile, die True zurückgibt, wenn bis zur
  nächsten Wartung höchstens vorlauf Seiten fehlen, sonst False.
  Benutzen Sie dafür naechste_wartung.

Das Programm gibt zum Schluss Ihre beiden Docstrings als Hilfe aus. Bei
Eingabe 148500 beginnt die Ausgabe so:

    Nächste Wartung bei 150000 Seiten
    Wartung jetzt einplanen
    Hilfe:

Grenzen: Der Zählerstand ist eine ganze Zahl von 0 bis 10 000 000.

Hintergrund: Ein Kommentar beginnt mit # und gilt bis zum Zeilenende;
Python überspringt ihn. Er ist für Menschen und erklärt am besten,
warum etwas so gemacht ist, denn was der Code tut, steht schon im Code.
Ein Docstring ist ein Text in drei Anführungszeichen direkt unter der
def-Zeile, als erste Zeile im Rumpf. Python merkt ihn sich in
funktion.__doc__, und help(funktion) zeigt ihn an:

    def brutto(netto):
        '''Gibt den Preis mit 19 % Mehrwertsteuer zurück.'''
        # round, weil Kommazahlen sonst wie 11.899999999999999 aussehen
        return round(netto * 1.19, 2)

    print(brutto.__doc__)     # Gibt den Preis mit 19 % Mehrwertsteuer zurück.

Steht vor dem Docstring noch eine andere Anweisung (Kommentare zählen
nicht), ist er kein Docstring mehr, und __doc__ ist None. Die Rechnung
mit // (ganzzahlig teilen) kennen Sie aus Aufgabe 1_005.
"""

INTERVALL = 50000  # Seiten zwischen zwei Wartungen
VORLAUF = 2000  # so viele Seiten vorher wird der Techniker bestellt


def naechste_wartung(zaehlerstand):
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
    return (zaehlerstand // INTERVALL + 1) * INTERVALL


def wartung_bald(zaehlerstand, vorlauf):
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


zaehlerstand = int(input("Zählerstand des Druckers: "))
print(f"Nächste Wartung bei {naechste_wartung(zaehlerstand)} Seiten")
if wartung_bald(zaehlerstand, VORLAUF):
    print("Wartung jetzt einplanen")
else:
    print("Noch keine Wartung nötig")
print("Hilfe:")
print(naechste_wartung.__doc__)
print(wartung_bald.__doc__)
