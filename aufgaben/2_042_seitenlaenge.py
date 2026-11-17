"""Aufgabe 2_042 – Seitenlänge                                   Stufe 2 ★★☆☆☆

Ein Netzwerktechniker plant das Netz für eine neue, quadratische
Lagerhalle. Aus dem Grundriss kennt er nur die Fläche in Quadratmetern.
Die Kabeltrasse für die Access Points soll an einer Wand entlanglaufen,
also braucht er die Seitenlänge der Halle: die Zahl x mit x * x gleich
der Fläche, die Quadratwurzel. Sein Planungsprogramm hat keine
Wurzelfunktion. Vervollständigen Sie die Funktion `seitenlaenge`, die
die Seitenlänge mit dem Bisektionsverfahren (siehe Hintergrund)
annähert. Fertig ist sie, sobald abs(x * x - flaeche) kleiner als
GENAUIGKEIT ist; dann gibt sie x zurück. Benutzen Sie weder math.sqrt
noch pow noch ** 0.5.

    seitenlaenge(2500)  →  ungefähr 50.0      (z. B. 49.99999...)
    seitenlaenge(2)     →  ungefähr 1.41421
    seitenlaenge(0.25)  →  ungefähr 0.5

Grenzen: flaeche ist eine ganze Zahl oder Kommazahl mit
0 ≤ flaeche ≤ 10**6. Das Ergebnis x muss x ≥ 0 und
abs(x * x - flaeche) < GENAUIGKEIT erfüllen. Ihre Lösung soll den
Bereich jedes Mal halbieren, also auch bei 10**6 mit weniger als 100
Schleifendurchläufen auskommen.

Hintergrund: Die Bisektion (MIT 6.0001, Lecture 3: „bisection search“)
ist ein Näherungsverfahren: Man kennt die Antwort nicht genau, aber
einen Bereich, in dem sie sicher liegt, und verkleinert ihn so lange,
bis die Antwort genau genug ist. Die Wurzel einer Zahl flaeche liegt
zwischen tief = 0 und hoch = flaeche, aber Vorsicht: Bei einer Zahl
unter 1 ist die Wurzel größer als die Zahl selbst (0.5 * 0.5 = 0.25),
darum nimmt man als obere Grenze max(flaeche, 1). Dann rät man die
Mitte und prüft sie:

    tief = 0
    hoch = max(flaeche, 1)
    mitte = (tief + hoch) / 2
    while abs(mitte * mitte - flaeche) >= GENAUIGKEIT:
        if mitte * mitte < flaeche:
            tief = mitte        # Wurzel liegt rechts von mitte
        else:
            hoch = mitte        # Wurzel liegt links von mitte
        mitte = (tief + hoch) / 2

Ist mitte zu klein, kann die Wurzel nur in der rechten Hälfte liegen,
sonst nur in der linken; die andere Hälfte fällt weg. Bei jedem
Durchlauf halbiert sich der Bereich. Raten und Prüfen in kleinen
Schritten (Aufgabe 2_005) bräuchte für eine Genauigkeit von 0.001 bei
10**6 Quadratmetern Millionen von Versuchen, die Bisektion nur etwa 40.
abs(...) liefert den Betrag einer Zahl, also den Abstand ohne
Vorzeichen.
"""

GENAUIGKEIT = 0.001


def seitenlaenge(flaeche):
    """Gibt die Quadratwurzel von flaeche zurück, genähert mit Bisektion."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(round(seitenlaenge(2500), 2))
