# Automatisch erzeugt aus lehrkraft/muster/2_006_transporter.py - nicht von Hand ändern.
# vorlage-hash: 4f3970e0e8472067

# Das Beispiel aus der Aufgabe: zwei Pakete passen
ergebnis = einladen([300, 200, 400, 150], 800)
assert ergebnis == 2, (
    f"einladen([300, 200, 400, 150], 800) ergibt {ergebnis!r}, erwartet war 2.\n"
    "Tipp: Nach dem Paket mit 400 kg ist Schluss, auch wenn 150 kg noch gepasst hätten. Verlassen Sie die Schleife mit break."
)

# Weitere Ladungen (nicht fest 2 hinschreiben!)
for gewichte, hoechstlast, erwartet in [
    ([100, 250, 50], 400, 3),
    ([100, 250, 60], 400, 2),
    ([10, 20, 30, 40, 50], 75, 3),
    ([500, 1, 1, 1], 400, 0),
]:
    ergebnis = einladen(gewichte, hoechstlast)
    assert ergebnis == erwartet, f"einladen({gewichte}, {hoechstlast}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Genau die Höchstlast ist noch erlaubt
ergebnis = einladen([300, 200], 500)
assert ergebnis == 2, (
    f"einladen([300, 200], 500) ergibt {ergebnis!r}, erwartet war 2, denn 500 kg sind genau die Höchstlast.\n"
    "Tipp: Erst wenn die Last die Höchstlast überschreitet (>), passt das Paket nicht mehr."
)

# Kein späteres Paket wird nachgeschoben
ergebnis = einladen([400, 500, 100, 100], 700)
assert ergebnis == 1, (
    f"einladen([400, 500, 100, 100], 700) ergibt {ergebnis!r}, erwartet war 1.\n"
    "Das Paket mit 500 kg passt nicht mehr, also fährt der Transporter los; die beiden Pakete mit 100 kg kommen nicht mehr dran.\n"
    "Tipp: Überspringen Sie nicht nur das zu schwere Paket, sondern beenden Sie die Schleife mit break."
)

# Leeres Band und zu schweres erstes Paket ergeben 0
for gewichte in [[], [900, 10]]:
    ergebnis = einladen(gewichte, 800)
    assert ergebnis == 0, f"einladen({gewichte}, 800) ergibt {ergebnis!r}, erwartet war 0."


# Dieses Förderband zählt, wie viele Pakete angesehen werden
class Foerderband:
    """Liste von Gewichten, die mitzählt, wie viele Pakete angesehen werden."""

    def __init__(self, gewichte):
        """Speichert die Gewichte und setzt den Zähler auf 0."""
        self.gewichte = gewichte
        self.angesehen = 0

    def __iter__(self):
        """Liefert die Gewichte einzeln und zählt mit."""
        for gewicht in self.gewichte:
            self.angesehen += 1
            yield gewicht

    def __len__(self):
        """Gibt die Anzahl der Pakete zurück, ohne mitzuzählen."""
        return len(self.gewichte)

    def __getitem__(self, index):
        """Gibt das Gewicht an index zurück und zählt mit."""
        self.angesehen += 1
        return self.gewichte[index]


# Nach dem ersten Paket, das nicht passt, wird kein weiteres angesehen
band = Foerderband([300, 200, 400] + [1] * 1000)
ergebnis = einladen(band, 800)
assert ergebnis == 2 and band.angesehen <= 10, (
    f"Bei einem Band mit 1003 Paketen, bei dem das dritte nicht mehr passt, ergibt einladen {ergebnis!r} "
    f"und hat {band.angesehen} Pakete angesehen; erwartet waren 2 Pakete und nur wenige angesehene (höchstens 10).\n"
    "Tipp: Mit break hört die Schleife sofort auf, statt den Rest des Bandes durchzugehen."
)
