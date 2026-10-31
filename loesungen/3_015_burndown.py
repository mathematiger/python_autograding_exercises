# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_015_burndown.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_015_burndown

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
bis 1000 mit 0 ≤ len(erledigt) ≤ 100 000.

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
    reste = []
    rest = gesamt
    for punkte in erledigt:
        rest = max(rest - punkte, 0)
        reste.append(rest)
    return reste


def fertig_nach(gesamt, erledigt):
    """Gibt den Sprint (ab 1) zurück, nach dem nichts mehr offen war; 0 bei gesamt 0, sonst -1."""
    if gesamt == 0:
        return 0
    rest = gesamt
    sprint = 0
    for punkte in erledigt:
        rest = rest - punkte
        sprint = sprint + 1
        if rest <= 0:
            return sprint
    return -1


print(restpunkte(20, [10, 15, 5]))
print(fertig_nach(20, [8, 7, 5]), fertig_nach(20, [10, 15, 5]), fertig_nach(20, [5, 5]), fertig_nach(0, [3]))


# Idee: Die Wertetabelle für fertig_nach(20, [10, 15, 5]) zeigt im zweiten Durchlauf rest = -5, also
# fertig, aber sprint steht noch auf 1, weil erst danach hochgezählt wird. Die Tabelle für (20, [5, 5])
# endet mit return sprint, also 2, obwohl nie fertig. Und bei genau 0 ist rest < 0 falsch. Darum:
# sprint vor der Prüfung hochzählen, rest <= 0 prüfen, nach der Schleife -1 zurückgeben und gesamt == 0
# vorab mit 0 beantworten. Beim Beispiel des Kollegen hoben sich der Zählfehler und das falsche return
# genau auf. restpunkte ist die Spalte rest der Tabelle, mit max(…, 0) nach unten begrenzt.
#
# Anderer Weg: fertig_nach mit restpunkte bauen: Ist gesamt 0, ist die Antwort 0; sonst ist sie die
# Position der ersten 0 in restpunkte(gesamt, erledigt) plus eins (reste.index(0) + 1), und -1, wenn
# 0 nicht vorkommt. Oder mit enumerate(erledigt, start=1) zählen.
#
# Typische Fehler: nur sprint = 1 als Start setzen und das Hochzählen hinten lassen (dann wird
# fertig_nach(0, [3]) zu 1), rest < 0 stehen lassen, nach der Schleife sprint statt -1 zurückgeben oder
# in restpunkte negative Reste in die Liste schreiben.
#
# Laufzeit: Beide Funktionen gehen die Liste einmal durch, also O(n) für n Sprints. Die Vergleichslösung
# mit sum(erledigt[:k]) für jedes k bräuchte O(n²).
