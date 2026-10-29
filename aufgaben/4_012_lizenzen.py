"""Aufgabe 4_012 – Lizenzen zählen                                Stufe 4 ★★★★☆

Eine Firma kauft Software meist als Lizenzpaket mit einer festen Zahl von
Plätzen: Für 10 Plätze dürfen 10 Personen das Programm nutzen, und jeder
Platz kostet im Jahr einen festen Preis, egal ob ihn jemand nutzt. Die
IT-Abteilung will wissen, wie viel Geld für Plätze ausgegeben wird, die
niemandem zugewiesen sind, damit sie beim nächsten Vertrag weniger Plätze
bestellen kann.

Vervollständigen Sie die Datenklasse `Lizenz` mit diesen Feldern, in
dieser Reihenfolge:

- `produkt` (Text, ohne Standardwert),
- `plaetze` (ganze Zahl, Standardwert 1),
- `preis_pro_platz` (Euro pro Jahr, Standardwert 0.0),
- `nutzer` (Liste der Namen, denen ein Platz zugewiesen ist, Standardwert
  eine neue leere Liste für jede Lizenz).

Dazu die Methoden `frei()`, die die Zahl der freien Plätze zurückgibt, und
`zuweisen(name)`, die name an nutzer anhängt. Hat name schon einen Platz
oder ist keiner mehr frei, löst zuweisen einen ValueError aus und ändert
nichts. Schließlich die Funktion `ungenutzte_kosten(lizenzen)`: was alle
freien Plätze der Liste zusammen im Jahr kosten.

    office = Lizenz("Office", 3, 120.0)
    office.zuweisen("Kaya")
    office                →  Lizenz(produkt='Office', plaetze=3, preis_pro_platz=120.0, nutzer=['Kaya'])
    office.frei()         →  2
    Lizenz("Editor")      →  Lizenz(produkt='Editor', plaetze=1, preis_pro_platz=0.0, nutzer=[])
    ungenutzte_kosten([office, Lizenz("CAD", 2, 900.0, ["Nowak"])])   →  1140.0

Grenzen: produkt und die Namen sind nicht leere Texte. 0 ≤ plaetze ≤ 10**6,
0 ≤ preis_pro_platz ≤ 10**4 (ganze Zahl oder Kommazahl). Eine übergebene
Liste nutzer hat höchstens plaetze Namen, keinen doppelt. Eine Liste
lizenzen hat 0 bis 100 000 Einträge.

Hintergrund: Viele Klassen tun vor allem eines: ein paar Werte unter
Namen zusammenhalten. Dafür muss man __init__, __repr__ und __eq__ immer
wieder nach demselben Muster schreiben. Der Dekorator @dataclass aus dem
Modul dataclasses nimmt einem das ab. Man schreibt nur die Felder mit
ihrem Typ in den Klassenkörper, und @dataclass erzeugt daraus die drei
Methoden:

    from dataclasses import dataclass, field

    @dataclass
    class Server:
        name: str
        kerne: int = 4
        dienste: list = field(default_factory=list)

    s = Server("web01")
    s                         →  Server(name='web01', kerne=4, dienste=[])
    Server("db", 8) == Server("db", 8)   →  True

__init__ nimmt die Felder in der Reihenfolge der Klasse als Parameter, als
Position oder als Schlüsselwort (Server("db", kerne=8)). Ein Feld mit
Standardwert ist beim Aufruf optional; darum müssen alle Felder ohne
Standardwert vor denen mit Standardwert stehen. __repr__ zeigt alle Felder,
__eq__ vergleicht alle Felder der Reihe nach. Die Typangaben prüft Python
nicht, @dataclass braucht sie nur, um die Felder zu erkennen.

Vorsicht bei Listen: Ein Standardwert wird nur einmal angelegt, wenn die
Klasse entsteht. Mit dienste: list = [] würden sich alle Server dieselbe
Liste teilen, und ein Dienst, den man bei einem Server einträgt, stünde
bei allen. @dataclass verbietet das deshalb mit einem ValueError. Stattdessen
gibt field(default_factory=list) eine Funktion an, die für jedes neue
Objekt aufgerufen wird; list() liefert jedes Mal eine neue leere Liste.
Eigene Methoden schreibt man wie in jeder Klasse dazu.
"""

from dataclasses import dataclass, field


@dataclass
class Lizenz:
    """Ein Lizenzpaket mit einer festen Zahl von Plätzen und den Namen der Personen, die einen Platz haben."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def frei(self):
        """Gibt die Zahl der Plätze zurück, die niemandem zugewiesen sind."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def zuweisen(self, name):
        """Gibt name einen Platz; ValueError, wenn name schon einen hat oder keiner frei ist."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ungenutzte_kosten(lizenzen):
    """Gibt zurück, was die freien Plätze aller Lizenzen der Liste zusammen im Jahr kosten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


office = Lizenz("Office", 3, 120.0)
office.zuweisen("Kaya")
print(office)
print(ungenutzte_kosten([office, Lizenz("CAD", 2, 900.0, ["Nowak"])]))
