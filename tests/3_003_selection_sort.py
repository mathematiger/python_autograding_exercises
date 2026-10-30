# Automatisch erzeugt aus lehrkraft/muster/3_003_selection_sort.py - nicht von Hand ändern.
# vorlage-hash: 9752641e04d5f6ae
# text-hash: 7e23650dcabbd249
# thema: algorithmen
# inhalt: Selection Sort

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

# Viele zufällige Listen, auch mit gleichen Zeiten (nicht fest hinschreiben!)
zufall = Zufall(3003)
for runde in range(400):
    vorher = [zufall.randint(0, 30) / 2 for _ in range(runde // 20)]
    liste = list(vorher)
    sortiere(liste)
    assert liste == sorted(vorher), f"Nach sortiere({vorher}) ist die Liste {liste}, erwartet war {sorted(vorher)}."

# sorted(...) wird nicht benutzt
assert not verwendet("sorted"), "Benutzen Sie nicht sorted(...), sondern sortieren Sie selbst mit Schleifen."

# liste.sort() wird nicht benutzt, auch nicht auf einer Kopie
assert not verwendet("sort"), "Benutzen Sie nicht .sort(), sondern sortieren Sie selbst mit Schleifen."


# Diese Liste zählt Schreibzugriffe
class Messliste(list):
    """Liste, die mitzählt, wie oft ein Element überschrieben wird."""

    def __init__(self, werte):
        """Übernimmt die Werte und setzt den Zähler zurück."""
        super().__init__(werte)
        self.schreibzugriffe = 0

    def __setitem__(self, index, wert):
        """Schreibt den Wert und zählt mit."""
        self.schreibzugriffe += 1
        super().__setitem__(index, wert)


# Selection Sort tauscht höchstens einmal pro Runde
messliste = Messliste(list(range(20, 0, -1)))
sortiere(messliste)
assert messliste.schreibzugriffe <= 2 * 20, (
    f"Für eine rückwärts sortierte Liste mit 20 Zahlen hat Ihre Funktion {messliste.schreibzugriffe}-mal "
    "ein Element überschrieben; Selection Sort braucht höchstens 40 (ein Tausch pro Runde).\n"
    "Tipp: Tauschen Sie nicht bei jedem Vergleich, sondern merken Sie sich in der inneren Schleife nur den Index "
    "des kleinsten Elements und tauschen Sie erst danach."
)
# 1000 zufällige Zeiten werden sortiert, mit höchstens einem Tausch pro Runde
vorher = [zufall.randint(0, 100000) / 100 for _ in range(1000)]
messliste = Messliste(vorher)
sortiere(messliste)
richtig_sortiert = list(messliste) == sorted(vorher)
assert richtig_sortiert and messliste.schreibzugriffe <= 2 * 1000, (
    f"Für 1000 zufällige Zeiten ist die Liste danach richtig sortiert: {richtig_sortiert}; Ihre Funktion hat "
    f"{messliste.schreibzugriffe}-mal ein Element überschrieben. Erwartet war eine richtig sortierte Liste "
    "mit höchstens 2000 Schreibzugriffen (ein Tausch pro Runde)."
)
