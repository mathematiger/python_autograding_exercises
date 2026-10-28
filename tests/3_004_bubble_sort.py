# Automatisch erzeugt aus lehrkraft/muster/3_004_bubble_sort.py - nicht von Hand ändern.
# vorlage-hash: 02fd0f4909154af6
# thema: algorithmen
# inhalt: Bubble Sort mit Abbruch

# Das Beispiel aus der Aufgabe wird sortiert
fristen = [30, 7, 365, 90]
sortiere(fristen)
if fristen == [30, 7, 365, 90]:
    hinweis = "Tipp: Die Liste ist unverändert. Die Funktion soll die übergebene Liste selbst verändern, nicht eine neue zurückgeben."
else:
    hinweis = "Tipp: Gehen Sie das Beispiel aus dem Hintergrund Durchgang für Durchgang durch und vergleichen Sie mit Ihrer Liste."
assert fristen == [7, 30, 90, 365], (
    f"Nach sortiere([30, 7, 365, 90]) ist die Liste {fristen}, erwartet war [7, 30, 90, 365].\n{hinweis}"
)

# Weitere Listen (nicht fest hinschreiben!)
for vorher, nachher in [
    ([3, 1, 2], [1, 2, 3]),
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([2, 1], [1, 2]),
    ([180, 14, 90, 3650, 14, 30], [14, 14, 30, 90, 180, 3650]),
]:
    liste = list(vorher)
    sortiere(liste)
    assert liste == nachher, f"Nach sortiere({vorher}) ist die Liste {liste}, erwartet war {nachher}."

# Das kleinste Element ganz hinten wandert bis nach vorn
liste = [4, 3, 2, 0]
sortiere(liste)
assert liste == [0, 2, 3, 4], (
    f"Nach sortiere([4, 3, 2, 0]) ist die Liste {liste}, erwartet war [0, 2, 3, 4].\n"
    "Tipp: Ein Durchgang allein reicht nicht; wiederholen Sie die Durchgänge, bis nichts mehr getauscht wird."
)

# Leere Liste und Liste mit einem Element bleiben, wie sie sind
for vorher in [[], [365]]:
    liste = list(vorher)
    sortiere(liste)
    assert liste == vorher, f"Nach sortiere({vorher}) ist die Liste {liste}, erwartet war {vorher}."

# Gleiche Fristen führen nicht zu einer Endlosschleife
liste = [30, 30, 7, 30]
sortiere(liste)
assert liste == [7, 30, 30, 30], f"Nach sortiere([30, 30, 7, 30]) ist die Liste {liste}, erwartet war [7, 30, 30, 30]."

# Eine längere Liste wird richtig sortiert
liste = [(7 * zahl) % 31 for zahl in range(31)]
sortiere(liste)
assert liste == list(range(31)), f"Eine gemischte Liste der Zahlen 0 bis 30 ergibt nach sortiere {liste}."

# Viele zufällige Listen, auch mit gleichen Fristen (nicht fest hinschreiben!)
zufall = Zufall(3004)
for runde in range(400):
    vorher = [zufall.choice([0, 7, 14, 30, 90, 365, 3650]) for _ in range(runde // 20)]
    liste = list(vorher)
    sortiere(liste)
    assert liste == sorted(vorher), f"Nach sortiere({vorher}) ist die Liste {liste}, erwartet war {sorted(vorher)}."

# 1000 zufällige Fristen werden sortiert
vorher = [zufall.randint(0, 3650) for _ in range(1000)]
liste = list(vorher)
sortiere(liste)
assert liste == sorted(vorher), "Eine Liste mit 1000 zufälligen Fristen von 0 bis 3650 ist nach sortiere nicht sortiert."

# sorted(...) wird nicht benutzt
assert not verwendet("sorted"), "Benutzen Sie nicht sorted(...), sondern sortieren Sie selbst mit Schleifen."


# Diese Liste zählt Lesezugriffe und merkt sich, ob liste.sort() aufgerufen wurde
class Messliste(list):
    """Liste, die mitzählt, wie oft ein Element gelesen wird."""

    def __init__(self, werte):
        """Übernimmt die Werte und setzt die Zähler zurück."""
        super().__init__(werte)
        self.lesezugriffe = 0
        self.sort_benutzt = False

    def __getitem__(self, index):
        """Liest das Element und zählt mit."""
        self.lesezugriffe += 1
        return super().__getitem__(index)

    def sort(self, *args, **kwargs):
        """Merkt sich den Aufruf und sortiert dann wie gewohnt."""
        self.sort_benutzt = True
        super().sort(*args, **kwargs)


# liste.sort() wird nicht benutzt
messliste = Messliste([5, 3, 8, 1])
sortiere(messliste)
assert not messliste.sort_benutzt, "Benutzen Sie nicht liste.sort(), sondern sortieren Sie selbst mit Schleifen."

# Eine schon sortierte Liste ist nach einem Durchgang fertig
messliste = Messliste(range(1000))
sortiere(messliste)
assert messliste.lesezugriffe <= 3 * 1000, (
    f"Für eine schon sortierte Liste mit 1000 Fristen hat Ihre Funktion {messliste.lesezugriffe}-mal ein Element "
    "gelesen; ein einziger Durchgang braucht etwa 2000 Lesezugriffe.\n"
    "Tipp: Merken Sie sich in einer Variablen wie getauscht, ob im Durchgang etwas getauscht wurde, "
    "und hören Sie auf, sobald ein Durchgang ohne Tausch bleibt."
)

# Eine fast sortierte Liste ist nach zwei Durchgängen fertig
messliste = Messliste([0, 2, 1] + list(range(3, 1000)))
sortiere(messliste)
assert list(messliste) == list(range(1000)) and messliste.lesezugriffe <= 5 * 1000, (
    f"Für eine Liste mit 1000 Fristen, in der nur zwei Nachbarn vertauscht sind, hat Ihre Funktion "
    f"{messliste.lesezugriffe}-mal ein Element gelesen; zwei Durchgänge brauchen etwa 4000 Lesezugriffe.\n"
    "Tipp: Nach dem ersten Durchgang ist die Liste sortiert, der zweite tauscht nichts mehr, dann ist Schluss."
)
