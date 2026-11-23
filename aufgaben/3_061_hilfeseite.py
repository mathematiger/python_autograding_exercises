"""Aufgabe 3_061 – Hilfeseite                                    Stufe 3 ★★★☆☆

Das Hilfe-Center eines Kundenportals ist eine lange Liste häufiger
Fragen (FAQ) in fester, thematischer Reihenfolge. Auf dem Handy passen
nur k Einträge gleichzeitig auf den Bildschirm; der Rest ist erst nach
dem Scrollen zu sehen. Das Team will die Seite deshalb beim Öffnen so
weit vorscrollen, dass möglichst viel von dem sichtbar ist, was die
Leute wirklich suchen. Für jeden Eintrag ist bekannt, wie oft er im
letzten Monat aufgeklappt wurde:

    klicks = [12, 40, 7, 3, 55, 21, 9, 30]

Ein Bildschirm ab Position s zeigt die Einträge s bis s + k - 1.
Schreiben Sie zwei Funktionen:

- `fenstersummen(klicks, k)` gibt die Liste der Klicksummen aller
  Bildschirme zurück, in der Reihenfolge der Startpositionen 0, 1, 2, …
  Ein Bildschirm muss ganz gefüllt sein; ist die Liste kürzer als k,
  ist das Ergebnis die leere Liste.
- `beste_position(klicks, k)` gibt das Paar (s, summe) für den
  Bildschirm mit den meisten Klicks zurück, bei Gleichstand den mit der
  kleinsten Startposition, oder None, wenn kein Bildschirm ganz gefüllt
  ist. Benutzen Sie dafür fenstersummen.

    fenstersummen(klicks, 3)    →  [59, 50, 65, 79, 85, 60]
    beste_position(klicks, 3)   →  (4, 85)
    beste_position(klicks, 9)   →  None

Grenzen: klicks hat 0 bis 100 000 Einträge, ganze Zahlen von 0 bis
1 000 000. k ist eine ganze Zahl von 1 bis 100 000. Beide Funktionen
sollen O(n) Schritte brauchen, unabhängig davon, wie groß k ist.

Hintergrund: Naiv rechnet man jede Summe neu aus, etwa mit
sum(klicks[s:s + k]). Das liest für jeden der n - k + 1 Bildschirme k
Einträge, also O(n · k) Schritte; bei 100 000 Einträgen und k = 50 000
sind das zweieinhalb Milliarden. Dabei unterscheiden sich zwei
benachbarte Bildschirme nur am Rand: Rückt das Fenster um eins weiter,
fällt vorn ein Eintrag heraus und hinten kommt einer hinzu. Diese
Technik heißt gleitendes Fenster (englisch sliding window). Man rechnet
die erste Summe einmal ganz aus und schiebt dann weiter:

    summe = sum(werte[:k])                # das erste Fenster, k Schritte
    for neu in range(k, len(werte)):
        summe = summe + werte[neu] - werte[neu - k]
        ...                               # summe gehört zum Fenster ab neu - k + 1

Jeder Schritt kostet nun nur zwei Zugriffe, egal wie breit das Fenster
ist: zusammen O(n). Die Invariante der Schleife (Aufgabe 2_058): Nach
jedem Durchlauf ist summe die Summe der k Einträge, die mit werte[neu]
enden. Für beste_position merkt man sich wie beim Maximum von Hand
(Aufgabe 2_053) die beste Summe und ihre Stelle; bei Gleichstand bleibt
die frühere, wenn man nur bei echt größeren Summen übernimmt.
"""


def fenstersummen(klicks, k):
    """Gibt die Summen aller vollständigen Fenster der Breite k zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def beste_position(klicks, k):
    """Gibt (Startposition, Summe) des Fensters mit der größten Summe zurück, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


klicks = [12, 40, 7, 3, 55, 21, 9, 30]
print(fenstersummen(klicks, 3))
print(beste_position(klicks, 3))
