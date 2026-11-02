# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_017_lastspitzen.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_017_lastspitzen

"""Aufgabe 3_017 – Lastspitzen                                   Stufe 3 ★★★☆☆

Ein Monitoring-System misst auf einem Webserver jede Minute die
CPU-Auslastung in Prozent und speichert sie als Liste von Tupeln
(minute, prozent). Minute 0 ist Mitternacht. Das Betriebsteam möchte
daraus drei Auswertungen haben:

- `freie_kapazitaet(messungen)` gibt für jede Messung die freie
  Kapazität 100 - prozent zurück, als Liste in derselben Reihenfolge.
- `spitzen(messungen, schwelle)` gibt die Minuten zurück, in denen die
  Auslastung größer als schwelle war, in derselben Reihenfolge.
- `meldungen(messungen, schwelle)` gibt für dieselben Messungen je einen
  Text der Form "Minute 481: 97 %" zurück, für den Alarmkanal des Teams.

    messungen = [(480, 35), (481, 97), (482, 88), (483, 40)]
    freie_kapazitaet(messungen)   →  [65, 3, 12, 60]
    spitzen(messungen, 85)        →  [481, 482]
    meldungen(messungen, 90)      →  ["Minute 481: 97 %"]

Schreiben Sie jede der drei Funktionen mit einer List Comprehension,
ohne for-Schleife als eigene Anweisung und ohne append.

Grenzen: messungen hat 0 bis 100 000 Einträge. Die Minuten sind
verschiedene ganze Zahlen von 0 bis 10**6 in aufsteigender Reihenfolge,
prozent und schwelle sind ganze Zahlen von 0 bis 100. Die Liste
messungen bleibt unverändert.

Hintergrund: Viele Schleifen haben dieselbe Form: eine leere Liste
anlegen, über eine andere Liste laufen, vielleicht mit if auswählen und
etwas daraus berechnetes anhängen. Dafür gibt es eine Kurzform, die List
Comprehension:

    quadrate = [zahl * zahl for zahl in zahlen]
    gerade = [zahl for zahl in zahlen if zahl % 2 == 0]

Man liest sie von links nach rechts so: „die Liste aus zahl * zahl für
jede zahl in zahlen“, im zweiten Beispiel „… aber nur, wenn zahl gerade
ist“. Vorn steht, was in die neue Liste kommt (abbilden), hinten nach
if, welche Elemente überhaupt berücksichtigt werden (filtern). Beides
lässt sich kombinieren, und auch Tupel lassen sich gleich auspacken:

    namen = [name for name, alter in personen if alter >= 18]

Die ursprüngliche Liste bleibt dabei unverändert; es entsteht immer eine
neue. Eine List Comprehension ist kürzer als die Schleife mit append und
meist auch etwas schneller, weil Python die Liste in einem Zug aufbaut.
Für komplizierte Abläufe mit mehreren Schritten bleibt die normale
Schleife aber lesbarer.
"""


def freie_kapazitaet(messungen):
    """Gibt zu jeder Messung (minute, prozent) die freie Kapazität 100 - prozent zurück."""
    return [100 - prozent for minute, prozent in messungen]


def spitzen(messungen, schwelle):
    """Gibt die Minuten zurück, in denen die Auslastung größer als schwelle war."""
    return [minute for minute, prozent in messungen if prozent > schwelle]


def meldungen(messungen, schwelle):
    """Gibt für jede Messung über schwelle einen Text "Minute <minute>: <prozent> %" zurück."""
    return [f"Minute {minute}: {prozent} %" for minute, prozent in messungen if prozent > schwelle]


messungen = [(480, 35), (481, 97), (482, 88), (483, 40)]
print(freie_kapazitaet(messungen))
print(spitzen(messungen, 85))
print(meldungen(messungen, 90))


# Idee: Jede Funktion ist eine einzige List Comprehension, die die Tupel gleich auspackt: for minute,
# prozent in messungen. freie_kapazitaet bildet nur ab ([100 - prozent for …]), spitzen filtert mit
# if prozent > schwelle und nimmt vorn die minute, meldungen filtert genauso und setzt vorn mit einem
# f-String den Text zusammen.
#
# Anderer Weg: die bekannte Schleife mit ergebnis = [], for und append. Sie tut dasselbe, braucht aber
# drei bis vier Zeilen statt einer. meldungen kann auch spitzen nicht wiederverwenden, weil dort die
# Prozentwerte fehlen; man könnte aber [f"…" for minute, prozent in messungen if minute in …] bauen,
# das wäre umständlicher und mit einer Liste langsam.
#
# Typische Fehler: >= statt > (dann zählt genau die Schwelle als Spitze), vorn das ganze Tupel statt
# der minute eintragen, das if vor das for schreiben ([x if … for …] braucht ein else und filtert
# nicht) oder ein Leerzeichen vor dem % vergessen.
#
# Laufzeit: Jede Comprehension sieht jede der n Messungen genau einmal an, also O(n).
