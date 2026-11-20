"""Aufgabe 1_039 – Einsatzkosten                                 Stufe 1 ★☆☆☆☆

Ein IT-Dienstleister rechnet jeden Support-Einsatz gleich ab: Jede
Arbeitsstunde kostet den Stundensatz der Person, die den Einsatz macht,
dazu kommt einmal die Anfahrtspauschale. Bei einer Fernwartung (der
Techniker loggt sich aus der Ferne auf dem Rechner ein) fällt keine
Anfahrt an, die Pauschale ist dann 0.

Schreiben Sie oben im Programm eine eigene Funktion einsatzkosten mit den
drei Parametern stunden, stundensatz und anfahrt, in dieser Reihenfolge.
Sie soll die Kosten in Euro mit return zurückgeben:

    Kosten = stunden * stundensatz + anfahrt

Das Programm darunter ist vorgegeben: Es fragt nach den Arbeitsstunden
und gibt die Kosten für drei Arten von Einsätzen aus. Bei Eingabe 3:

    Vor Ort, Junior: 165 Euro
    Vor Ort, Senior: 240 Euro
    Fernwartung, Senior: 210 Euro

Grenzen: Die Eingabe ist eine ganze Zahl von 0 bis 40.

Hintergrund: Eine Funktion darf mehrere Parameter haben; sie stehen durch
Kommas getrennt in den Klammern hinter def. Beim Aufruf schreibt man
genauso viele Werte durch Kommas getrennt in die Klammern. Python ordnet
sie der Reihe nach zu: der erste Wert dem ersten Parameter, der zweite
dem zweiten und so weiter.

    def rechteck(breite, hoehe):
        return breite * hoehe

    rechteck(4, 3)      # breite ist 4, hoehe ist 3, das Ergebnis ist 12

Vertauscht man beim Festlegen die Reihenfolge der Parameter, bekommen sie
beim Aufruf die falschen Werte. Wie return funktioniert, steht in Aufgabe
1_038.
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


stunden = int(input("Arbeitsstunden: "))

print(f"Vor Ort, Junior: {einsatzkosten(stunden, 45, 30)} Euro")
print(f"Vor Ort, Senior: {einsatzkosten(stunden, 70, 30)} Euro")
print(f"Fernwartung, Senior: {einsatzkosten(stunden, 70, 0)} Euro")
