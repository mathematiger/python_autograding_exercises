# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_006_adresskonflikt.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_006_adresskonflikt

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

Grenzen: 0 ≤ len(adressen) ≤ 1000. Jede Adresse ist ein Text wie
"192.168.0.17" (vier Zahlen von 0 bis 255, durch Punkte getrennt);
dieselbe Adresse darf mehrmals vorkommen. vergleiche_nachbarn bekommt die
Adressen mit sorted(...) sortiert, gleiche stehen also nebeneinander.

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
    vergleiche = 0
    for i in range(len(adressen)):
        for j in range(i + 1, len(adressen)):
            vergleiche = vergleiche + 1
            if adressen[i] == adressen[j]:
                return vergleiche
    return vergleiche


def vergleiche_nachbarn(sortiert):
    """Gibt zurück, wie viele Nachbarvergleiche die Suche nach einem Konflikt braucht."""
    vergleiche = 0
    for i in range(len(sortiert) - 1):
        vergleiche = vergleiche + 1
        if sortiert[i] == sortiert[i + 1]:
            return vergleiche
    return vergleiche


# Wachstum der Vergleiche in O-Notation, z. B. "O(log n)"
LAUFZEIT_PAARWEISE = "O(n²)"
LAUFZEIT_NACHBARN = "O(n)"


for anzahl in [100, 200, 400]:
    adressen = []
    for nummer in range(anzahl):
        adressen.append("10.0." + str(nummer // 256) + "." + str(nummer % 256))
    paarweise = vergleiche_paarweise(adressen)
    nachbarn = vergleiche_nachbarn(sorted(adressen))
    print(anzahl, "Adressen:", paarweise, "paarweise,", nachbarn, "Nachbarn")


# Idee: Übernehmen Sie die beiden Schleifen aus konflikt_paarweise unverändert und zählen Sie
# direkt vor jedem Vergleich einen Zähler hoch; beim ersten Konflikt und nach den Schleifen geben
# Sie den Zähler zurück. Bei vergleiche_nachbarn läuft eine einzige Schleife über die n - 1
# Nachbarpaare.
#
# Anderer Weg: Ohne Konflikt kann man die Zahl auch ausrechnen, paarweise n · (n - 1) // 2 und mit
# Nachbarn max(n - 1, 0); für den Fall mit Konflikt braucht man trotzdem die Schleifen. Ganz
# ohne Sortieren findet eine Menge (set) einen Konflikt in O(n): Man merkt sich jede gesehene
# Adresse und prüft mit in, ob sie schon vorkam.
#
# Typische Fehler: den Zähler erst nach dem Vergleich erhöhen (dann fehlt beim Konflikt einer),
# ihn in der äußeren Schleife zurücksetzen, oder bei 0 oder 1 Adressen -1 statt 0 zurückgeben.
#
# Laufzeit: paarweise O(n²), weil es n · (n - 1) / 2 Paare gibt; mit Nachbarn O(n), dazu einmal
# Sortieren mit O(n log n).
