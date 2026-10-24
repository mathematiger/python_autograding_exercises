"""Aufgabe 3_006 – Adresskonflikt                               Stufe 3 ★★★☆☆

Bekommen zwei Geräte im selben Netz dieselbe IP-Adresse, kann keines der
beiden mehr zuverlässig kommunizieren; man spricht von einem Adresskonflikt.
Ein Skript der Netzwerkabteilung prüft deshalb die Liste aller vergebenen
Adressen mit der Funktion `konflikt_paarweise` (unten vorgegeben): Sie
vergleicht jede Adresse mit jeder späteren. Für ein kleines Büro geht das
schnell, für den ganzen Campus mit 50 000 Geräten dauert es viel zu lange.
Finden Sie heraus, warum, indem Sie die Vergleiche zählen:

- `vergleiche_paarweise(adressen)` gibt zurück, wie oft konflikt_paarweise
  für diese Liste zwei Adressen mit == vergleicht. Wie dort ist beim ersten
  Konflikt Schluss.
- `vergleiche_nachbarn(sortiert)` bekommt die Adressen sortiert. Dann stehen
  gleiche Adressen direkt nebeneinander, und es reicht, jede Adresse mit
  ihrer rechten Nachbarin zu vergleichen. Die Funktion gibt zurück, wie viele
  solche Vergleiche nötig sind, bis ein Konflikt gefunden ist oder alle
  Nachbarn verglichen sind.
- Tragen Sie in die Variablen `LAUFZEIT_PAARWEISE` und `LAUFZEIT_NACHBARN`
  ein, wie die Zahl der Vergleiche im schlechtesten Fall mit der Zahl n der
  Adressen wächst, in O-Notation als Text, z. B. "O(log n)".

    vergleiche_paarweise(["10.0.0.1", "10.0.0.2", "10.0.0.3"])               →  3
    vergleiche_paarweise(["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.1"])   →  3
    vergleiche_nachbarn(["10.0.0.1", "10.0.0.2", "10.0.0.3"])                →  2
    vergleiche_nachbarn(["10.0.0.1", "10.0.0.1", "10.0.0.2"])                →  1

Im zweiten Beispiel vergleicht konflikt_paarweise die erste Adresse mit der
zweiten, der dritten und der vierten und findet dort den Konflikt.

Hintergrund: Wie lange ein Programm läuft, hängt vom Rechner ab. Vergleichbar
wird es, wenn man die wichtigsten Schritte zählt, hier die Vergleiche, und
fragt, wie ihre Zahl mit der Größe der Eingabe wächst. Bei n Adressen ohne
Konflikt vergleicht konflikt_paarweise die erste mit n - 1 anderen, die
zweite mit n - 2 und so weiter, zusammen

    (n - 1) + (n - 2) + … + 1  =  n · (n - 1) / 2

Vergleiche, also ungefähr n² / 2. Für die O-Notation lässt man feste Faktoren
wie ½ und kleinere Summanden weg, denn bei großem n zählt nur, wie stark der
größte Teil wächst: Die Laufzeit ist O(n²), quadratisch. Doppelt so viele
Adressen bedeuten viermal so viele Vergleiche, 50 000 Adressen schon über eine
Milliarde. Was man zählt, ist der schlechteste Fall: Ein früher Konflikt
macht die Suche zwar kürzer, darauf verlassen kann man sich aber nicht. Zum
Vergleich: Die lineare Suche (Aufgabe 3_001) braucht höchstens n Vergleiche,
O(n). Das Sortieren vorher kostet auch Zeit, mit Merge Sort (Aufgabe 3_005)
O(n log n); zusammen ist das immer noch viel schneller als O(n²).

Tipp: Kopieren Sie die Schleifen aus konflikt_paarweise, legen Sie vorher
einen Zähler mit dem Wert 0 an und erhöhen Sie ihn direkt vor jedem
Vergleich um 1. Statt True oder False geben Sie den Zähler zurück.
"""


def konflikt_paarweise(adressen):
    """Gibt True zurück, wenn eine Adresse mehrfach vorkommt, sonst False."""
    for i in range(len(adressen)):
        for j in range(i + 1, len(adressen)):
            if adressen[i] == adressen[j]:
                return True
    return False


def vergleiche_paarweise(adressen):
    """Gibt zurück, wie viele Vergleiche konflikt_paarweise(adressen) macht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def vergleiche_nachbarn(sortiert):
    """Gibt zurück, wie viele Nachbarvergleiche die Suche nach einem Konflikt braucht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


# Wachstum der Vergleiche in O-Notation, z. B. "O(log n)"
pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


for anzahl in [100, 200, 400]:
    adressen = []
    for nummer in range(anzahl):
        adressen.append("10.0." + str(nummer // 256) + "." + str(nummer % 256))
    paarweise = vergleiche_paarweise(adressen)
    nachbarn = vergleiche_nachbarn(sorted(adressen))
    print(anzahl, "Adressen:", paarweise, "paarweise,", nachbarn, "Nachbarn")
