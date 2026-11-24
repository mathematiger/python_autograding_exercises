"""Aufgabe 3_064 – Replikatverzug                                Stufe 3 ★★★☆☆

Eine Firma betreibt ihre Kundendatenbank auf einem Hauptserver und hält
in einem zweiten Rechenzentrum ein Replikat: eine Kopie, die jede
Änderung des Hauptservers nach wenigen Sekunden nachträgt. Hängt das
Replikat zu weit hinterher, ist es nicht synchron, und wer dort liest,
bekommt veraltete Daten. Drei Überwachungsprogramme melden solche
Zeiträume unabhängig voneinander. Ihre Meldungen überschneiden sich,
kommen doppelt vor und landen ungeordnet in einer Liste. Für den
Monatsbericht sollen daraus die tatsächlichen Zeiträume ohne
Synchronität und ihre Gesamtdauer werden.

Ein Zeitraum ist ein Tupel (start, ende) in Sekunden seit
Monatsbeginn. Er umfasst wie bei range die Sekunden start bis
ausschließlich ende und dauert ende - start Sekunden. Endet ein
Zeitraum genau dort, wo ein anderer beginnt (ende == start), war das
Replikat ohne Pause nicht synchron; beide gehören zu einem Zeitraum.
Schon eine Sekunde Abstand trennt sie. Schreiben Sie zwei Funktionen:

- `zusammenfuehren(zeitraeume)` gibt die zusammengeführten Zeiträume
  als neue Liste von Tupeln (start, ende) zurück, nach start
  aufsteigend geordnet und so, dass sich keine zwei mehr überschneiden
  oder berühren. Die Liste zeitraeume selbst bleibt unverändert, denn
  andere Teile der Überwachung brauchen die Meldungen noch in ihrer
  Reihenfolge.
- `gesamtdauer(zeitraeume)` gibt zurück, wie viele Sekunden das
  Replikat insgesamt nicht synchron war. Jede Sekunde zählt nur einmal,
  auch wenn sie mehrfach gemeldet wurde. Benutzen Sie dafür
  zusammenfuehren.

    meldungen = [(300, 420), (60, 180), (400, 500), (150, 200), (500, 560), (900, 960)]
    zusammenfuehren(meldungen)  →  [(60, 200), (300, 560), (900, 960)]
    gesamtdauer(meldungen)      →  460        (140 + 260 + 60)
    zusammenfuehren([(10, 20), (21, 30)])  →  [(10, 20), (21, 30)]

Grenzen: zeitraeume hat 0 bis 100 000 Einträge, jeder ein Tupel
(start, ende) aus ganzen Zahlen mit 0 ≤ start < ende ≤ 2 678 400 (so
viele Sekunden hat ein Monat mit 31 Tagen). Die Liste ist nicht
geordnet, derselbe Zeitraum darf mehrmals vorkommen, und ein Zeitraum
darf ganz in einem anderen liegen. Ihre Lösung soll O(n log n) Schritte
brauchen.

Hintergrund: Naiv vergleicht man jedes Paar von Zeiträumen, verschmilzt
zwei, die sich überschneiden, und fängt von vorn an, bis sich nichts
mehr ändert. Schon ein einziger Durchgang sind n · (n - 1) / 2
Vergleiche, also O(n²), bei 100 000 Meldungen rund fünf Milliarden.
Schneller geht es, wenn man die Zeiträume zuerst nach start sortiert.
sorted ordnet Tupel nach dem ersten Eintrag und bei Gleichstand nach
dem zweiten (Aufgabe 3_027), hier braucht es also nicht einmal einen
key. In der sortierten Liste kann der nächste Zeitraum nur noch den
zuletzt zusammengeführten berühren, denn alle früheren enden schon
vorher. Man geht deshalb einmal durch und vergleicht jeden Zeitraum
nur mit dem letzten Eintrag des Ergebnisses: Beginnt er spätestens
dort, wo dieser endet, verlängert er ihn, sonst beginnt mit ihm ein
neuer Eintrag. Im Beispiel kommt nach dem Sortieren zuerst (60, 180);
(150, 200) beginnt davor und verlängert ihn zu (60, 200); (300, 420)
beginnt erst danach und wird ein neuer Eintrag, den (400, 500) und
(500, 560) zu (300, 560) verlängern. Das Sortieren kostet O(n log n)
(wie Merge Sort in Aufgabe 3_005), der Durchgang O(n), zusammen also
O(n log n).

Tipp: Ein Tupel lässt sich nicht ändern. Um den letzten Eintrag zu
verlängern, ersetzen Sie ihn: ergebnis[-1] = (ergebnis[-1][0], neues_ende).
"""


def zusammenfuehren(zeitraeume):
    """Gibt die zusammengeführten Zeiträume nach start geordnet als neue Liste zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gesamtdauer(zeitraeume):
    """Gibt zurück, wie viele Sekunden insgesamt in mindestens einem Zeitraum liegen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


meldungen = [(300, 420), (60, 180), (400, 500), (150, 200), (500, 560), (900, 960)]
print(zusammenfuehren(meldungen))
print(gesamtdauer(meldungen))
