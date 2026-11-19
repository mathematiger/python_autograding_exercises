"""Aufgabe 5_026 – Quellensammler                                Stufe 5 ★★★★★

Für eine Prozessanalyse sollen die Durchlaufzeiten (Minuten von der
Bestellung bis zur Auslieferung) aus mehreren Systemen zusammengeführt
werden: aus dem Warenwirtschaftssystem, aus der Produktion, aus dem
Versand. Jedes System ist eine Datenquelle, die geöffnet und
anschließend wieder geschlossen werden muss, sonst bleibt dort eine
Verbindung hängen. Wie viele Quellen es sind, steht erst zur Laufzeit
fest.

Die Klasse `Datenquelle` ist vorgegeben. Sie ist ein Kontextmanager, der
jedes Öffnen und Schließen in eine gemeinsame Protokoll-Liste schreibt;
eine nicht erreichbare Quelle löst beim Öffnen einen ConnectionError aus.
Vervollständigen Sie die Funktion `sammle(quellen, protokoll)`:

- Sie öffnet alle Quellen der Reihe nach mit einem
  contextlib.ExitStack, liest von jeder die Werte (quelle.lies()) und
  gibt alle Werte zusammen aufsteigend sortiert zurück.
- Alle geöffneten Quellen werden geschlossen, bevor sammle zurückkehrt,
  in umgekehrter Reihenfolge des Öffnens.
- Ganz zum Schluss, nach dem Schließen der Quellen, hängt sie
  "Auswertung beendet" an protokoll an.
- Ist eine Quelle nicht erreichbar, schließt sie die schon geöffneten
  Quellen, schreibt ebenfalls "Auswertung beendet" und lässt den
  ConnectionError weiterlaufen.

    protokoll = []
    quellen = [Datenquelle("WWS", [30, 12], protokoll),
               Datenquelle("MES", [25], protokoll)]
    sammle(quellen, protokoll)  →  [12, 25, 30]
    protokoll  →  ["auf WWS", "auf MES", "zu MES", "zu WWS", "Auswertung beendet"]

Grenzen: 0 ≤ len(quellen) ≤ 200, jede Quelle ist eine Datenquelle. Eine
Quelle liefert 0 bis 1000 ganze Zahlen von 0 bis 10**6, zusammen
höchstens 100 000. Jede Quelle darf nicht erreichbar sein (werte ist
dann None).

Hintergrund: Mit with öffnet man eine feste Zahl von Ressourcen, eine
pro with oder durch Kommas getrennt. Bei einer Liste unbekannter Länge
geht das nicht, und von Hand mit try/finally wird es schnell falsch:
Schlägt das Öffnen der dritten Quelle fehl, müssen genau die ersten zwei
geschlossen werden. Dafür gibt es contextlib.ExitStack, einen
Kontextmanager, der andere Kontextmanager einsammelt:

    from contextlib import ExitStack

    with ExitStack() as stapel:
        dateien = [stapel.enter_context(open(name)) for name in namen]
        ...   # alle Dateien sind offen
    # hier sind alle wieder geschlossen, die zuletzt geöffnete zuerst

stapel.enter_context(cm) ruft cm.__enter__() auf, gibt dessen Ergebnis
zurück und merkt sich cm.__exit__ auf einem Stapel. Endet der
with-Block, normal oder durch eine Ausnahme, ruft der ExitStack alle
gemerkten __exit__ in umgekehrter Reihenfolge auf, wie verschachtelte
with-Blöcke es täten. Löst enter_context selbst eine Ausnahme aus, wird
nichts für diese Ressource gemerkt; geschlossen werden die, die schon
auf dem Stapel liegen.

Auf denselben Stapel kann man auch beliebige Aufräumfunktionen legen:
stapel.callback(funktion, *argumente) merkt sich den Aufruf
funktion(*argumente) und führt ihn beim Verlassen aus, ebenfalls in
umgekehrter Reihenfolge. Was als Erstes auf den Stapel kommt, wird als
Letztes ausgeführt:

    with ExitStack() as stapel:
        stapel.callback(print, "zuletzt")
        stapel.callback(print, "zuerst")
    # gibt "zuerst" und dann "zuletzt" aus

Ein ExitStack ist auch dann nützlich, wenn eine Funktion Ressourcen
öffnet und sie nur unter Umständen gleich wieder schließen soll; dafür
gibt es stapel.pop_all(), das den Inhalt in einen neuen Stapel umlegt.
"""

from contextlib import ExitStack


class Datenquelle:
    """Simuliert eine Datenquelle, die geöffnet und geschlossen werden muss (vorgegeben)."""

    def __init__(self, name, werte, protokoll):
        self.name = name
        self.werte = werte
        self.protokoll = protokoll

    def __enter__(self):
        if self.werte is None:
            self.protokoll.append(f"Fehler {self.name}")
            raise ConnectionError(f"{self.name} ist nicht erreichbar")
        self.protokoll.append(f"auf {self.name}")
        return self

    def __exit__(self, typ, wert, traceback):
        self.protokoll.append(f"zu {self.name}")
        return False

    def lies(self):
        """Liefert eine Kopie der Werte dieser Quelle."""
        return list(self.werte)


def sammle(quellen, protokoll):
    """Öffnet alle Quellen, liest ihre Werte und gibt sie zusammen sortiert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = []
quellen = [Datenquelle("WWS", [30, 12], protokoll), Datenquelle("MES", [25], protokoll)]
print(sammle(quellen, protokoll))
print(protokoll)
