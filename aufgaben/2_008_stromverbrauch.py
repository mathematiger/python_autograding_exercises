"""Aufgabe 2_008 – Stromverbrauch                                Stufe 2 ★★☆☆☆

Für die Energiebilanz eines Büros soll die IT-Abteilung angeben, wie viel
Strom die Arbeitsplatzrechner im Durchschnitt pro Monat verbrauchen. Ein
Zwischenzähler hat jeden Monat den Verbrauch in Kilowattstunden (kWh)
notiert. In manchen Monaten war der Zähler aber defekt; dort steht in der
Liste der Wert -1. Diese Monate sollen beim Durchschnitt nicht mitzählen,
weder in der Summe noch bei der Anzahl. Ein Verbrauch von 0 kWh ist dagegen
ein echter Messwert (das Büro war zu) und zählt mit. Vervollständigen Sie die
Funktion `mittlerer_verbrauch`, die den Durchschnitt der gemessenen Monate
zurückgibt. Gibt es keinen gemessenen Monat, ist das Ergebnis 0.

    mittlerer_verbrauch([400, -1, 500, 600])  →  500.0
    mittlerer_verbrauch([300, 0, -1])         →  150.0
    mittlerer_verbrauch([-1, -1])             →  0
    mittlerer_verbrauch([])                   →  0

Grenzen: verbraeuche ist eine Liste mit 0 ≤ len(verbraeuche) ≤ 1000 ganzen
Zahlen. Jeder Wert ist entweder -1 (Zähler defekt) oder ein Verbrauch mit
0 ≤ verbrauch ≤ 100 000.

Hintergrund: In einer for-Schleife beendet die Anweisung continue nur den
aktuellen Durchlauf: Der Rest des Schleifenblocks wird übersprungen, und die
Schleife macht sofort mit dem nächsten Element weiter. So sortiert man
ungültige Werte gleich am Anfang des Blocks aus, und der eigentliche Code
darunter muss sich nicht mehr darum kümmern:

    for zahl in [3, -2, 5]:
        if zahl < 0:
            continue
        print(zahl)

Das gibt 3 und 5 aus. Anders als break (Aufgabe 2_007) hört die Schleife nicht
auf, sondern lässt nur das eine Element aus.

Tipp: Zählen Sie in einer Variablen die Summe und in einer zweiten die Anzahl
der gemessenen Monate. Teilen Sie erst nach der Schleife, und nur, wenn die
Anzahl größer als 0 ist.
"""


def mittlerer_verbrauch(verbraeuche):
    """Gibt den Durchschnitt aller Werte außer -1 zurück (0, wenn es keine gibt)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(mittlerer_verbrauch([400, -1, 500, 600]))
