"""Aufgabe 3_015 – Burndown                                      Stufe 3 ★★★☆☆

Ein agiles Team plant seine Arbeit in Sprints von zwei Wochen. Der
Aufwand aller offenen Aufgaben wird in Story Points geschätzt, und nach
jedem Sprint wird eingetragen, wie viele Punkte das Team geschafft hat.
Ein Burndown-Diagramm zeigt dann, wie viele Punkte nach jedem Sprint
noch offen sind.

Ein Kollege hat eine Funktion geschrieben, die sagen soll, nach welchem
Sprint alles erledigt war:

    def fertig_nach(gesamt, erledigt):
        rest = gesamt
        sprint = 0
        for punkte in erledigt:
            rest = rest - punkte
            if rest < 0:
                return sprint
            sprint = sprint + 1
        return sprint

Er hat sie mit einer Wertetabelle für fertig_nach(20, [8, 7, 5])
geprüft und das richtige Ergebnis 3 bekommen:

    Durchlauf   punkte   rest   rest < 0   sprint danach
    1           8        12     False      1
    2           7        5      False      2
    3           5        0      False      3
    nach der Schleife: return sprint, also 3

Trotzdem liefert fertig_nach(20, [10, 15, 5]) die 1 statt 2 und
fertig_nach(20, [5, 5]) die 2, obwohl die Arbeit nie fertig wurde.
Stellen Sie für diese Aufrufe selbst Wertetabellen auf, finden Sie die
Fehler und schreiben Sie die Funktionen richtig:

- `restpunkte(gesamt, erledigt)` gibt die Spalte rest der Wertetabelle
  als Liste zurück: die offenen Punkte nach jedem Sprint. Hat das Team
  mehr geschafft als offen war, ist der Rest 0, nie negativ.
- `fertig_nach(gesamt, erledigt)` gibt die Nummer des Sprints zurück
  (gezählt ab 1), nach dem keine Punkte mehr offen waren; 0, wenn schon
  vor dem ersten Sprint nichts offen war (gesamt ist 0), und -1, wenn die
  Sprints nicht gereicht haben.

    restpunkte(20, [10, 15, 5])   →  [10, 0, 0]
    fertig_nach(20, [8, 7, 5])    →  3
    fertig_nach(20, [10, 15, 5])  →  2
    fertig_nach(20, [5, 5])       →  -1
    fertig_nach(0, [3])           →  0

Grenzen: 0 ≤ gesamt ≤ 10**6; erledigt ist eine Liste ganzer Zahlen von 0
bis 1000 mit 0 ≤ len(erledigt) ≤ 100 000. Beide Funktionen sollen in
O(n) laufen, n = len(erledigt): die Summe nicht für jeden Sprint neu bilden.

Hintergrund: Liefert eine Funktion ein falsches Ergebnis, hilft genaues
Hinsehen meist mehr als wildes Ändern. Eine Wertetabelle ist das
Werkzeug dafür: Man spielt selbst den Computer, schreibt für jede
Variable eine Spalte auf und trägt nach jeder Zeile des Codes ein, welchen
Wert sie jetzt hat, bei Schleifen eine Zeile pro Durchlauf. Wo der
Inhalt der Tabelle zum ersten Mal von dem abweicht, was man erwartet
hätte, sitzt der Fehler. Dazu braucht man vorher eine klare Erwartung:
Was soll nach dem ersten Durchlauf in sprint stehen, was soll bei
genau 0 Punkten passieren?

Ein richtiges Ergebnis beweist dabei wenig: Zwei Fehler können sich
gegenseitig aufheben, so wie hier beim Beispiel des Kollegen. Darum
stellt man Tabellen auch für Randfälle auf: genau erledigt, nie
erledigt, nichts zu tun, keine Sprints. Statt auf Papier kann man die
Tabelle auch mit print(punkte, rest, sprint) in der Schleife ausgeben
lassen und die Ausgabe später wieder entfernen.
"""


def restpunkte(gesamt, erledigt):
    """Gibt die offenen Story Points nach jedem Sprint als Liste zurück, nie negativ."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fertig_nach(gesamt, erledigt):
    """Gibt den Sprint (ab 1) zurück, nach dem nichts mehr offen war; 0 bei gesamt 0, sonst -1."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(restpunkte(20, [10, 15, 5]))
print(fertig_nach(20, [8, 7, 5]), fertig_nach(20, [10, 15, 5]), fertig_nach(20, [5, 5]), fertig_nach(0, [3]))
