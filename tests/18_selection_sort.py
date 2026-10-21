# Automatisch erzeugt aus lehrkraft/muster/18_selection_sort.py - nicht von Hand ändern.
# vorlage-hash: d706b01413642db8

# Das Beispiel aus der Aufgabe wird sortiert
zeiten = [14.2, 12.8, 15.0, 12.1]
sortiere(zeiten)
if zeiten == [14.2, 12.8, 15.0, 12.1]:
    hinweis = "Tipp: Die Liste ist unverändert. Die Funktion soll die übergebene Liste selbst verändern, nicht eine neue zurückgeben."
else:
    hinweis = "Tipp: Gehen Sie das Beispiel aus dem Hintergrund Runde für Runde durch und vergleichen Sie mit Ihrer Liste."
assert zeiten == [12.1, 12.8, 14.2, 15.0], (
    f"Nach sortiere([14.2, 12.8, 15.0, 12.1]) ist die Liste {zeiten}, erwartet war [12.1, 12.8, 14.2, 15.0].\n{hinweis}"
)

# Weitere Listen (nicht fest hinschreiben!)
for vorher, nachher in [
    ([3, 1, 2], [1, 2, 3]),
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([2, 1], [1, 2]),
    ([13.5, 11.9, 12.4, 11.9, 14.0, 12.0], [11.9, 11.9, 12.0, 12.4, 13.5, 14.0]),
]:
    liste = list(vorher)
    sortiere(liste)
    assert liste == nachher, f"Nach sortiere({vorher}) ist die Liste {liste}, erwartet war {nachher}."

# Das letzte Element wird mitsortiert
liste = [4, 3, 2, 0]
sortiere(liste)
assert liste == [0, 2, 3, 4], (
    f"Nach sortiere([4, 3, 2, 0]) ist die Liste {liste}, erwartet war [0, 2, 3, 4].\n"
    "Tipp: Die innere Schleife muss bis zum letzten Index laufen: range(i + 1, len(liste))."
)

# Leere Liste und Liste mit einem Element bleiben, wie sie sind
for vorher in [[], [12.5]]:
    liste = list(vorher)
    sortiere(liste)
    assert liste == vorher, f"Nach sortiere({vorher}) ist die Liste {liste}, erwartet war {vorher}."

# Eine längere Liste wird richtig sortiert
liste = [(7 * zahl) % 31 for zahl in range(31)]
sortiere(liste)
assert liste == list(range(31)), f"Eine gemischte Liste der Zahlen 0 bis 30 ergibt nach sortiere {liste}."

# sorted(...) wird nicht benutzt
assert not verwendet("sorted"), "Benutzen Sie nicht sorted(...), sondern sortieren Sie selbst mit Schleifen."


# Diese Liste zählt Schreibzugriffe und merkt sich, ob liste.sort() aufgerufen wurde
class Messliste(list):
    """Liste, die mitzählt, wie oft ein Element überschrieben wird."""

    def __init__(self, werte):
        """Übernimmt die Werte und setzt die Zähler zurück."""
        super().__init__(werte)
        self.schreibzugriffe = 0
        self.sort_benutzt = False

    def __setitem__(self, index, wert):
        """Schreibt den Wert und zählt mit."""
        self.schreibzugriffe += 1
        super().__setitem__(index, wert)

    def sort(self, *args, **kwargs):
        """Merkt sich den Aufruf und sortiert dann wie gewohnt."""
        self.sort_benutzt = True
        super().sort(*args, **kwargs)


# liste.sort() wird nicht benutzt
messliste = Messliste([5, 3, 8, 1])
sortiere(messliste)
assert not messliste.sort_benutzt, "Benutzen Sie nicht liste.sort(), sondern sortieren Sie selbst mit Schleifen."

# Selection Sort tauscht höchstens einmal pro Runde (Bubble Sort tauscht viel öfter)
messliste = Messliste(list(range(20, 0, -1)))
sortiere(messliste)
assert messliste.schreibzugriffe <= 2 * 20, (
    f"Für eine rückwärts sortierte Liste mit 20 Zahlen hat Ihre Funktion {messliste.schreibzugriffe}-mal "
    "ein Element überschrieben; Selection Sort braucht höchstens 40 (ein Tausch pro Runde).\n"
    "Tipp: Tauschen Sie nicht bei jedem Vergleich, sondern merken Sie sich in der inneren Schleife nur den Index "
    "des kleinsten Elements und tauschen Sie erst danach."
)
