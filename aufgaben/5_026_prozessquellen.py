"""Aufgabe 5_026 – Prozessquellen                                Stufe 5 ★★★★★

Ein Versandhändler will wissen, wie lange eine Bestellung insgesamt
braucht, vom Eingang bis zum Versand. Jeder Prozessschritt (Prüfen,
Kommissionieren, Verpacken, …) läuft in einem eigenen System und liefert
über eine eigene Verbindung, eine Messquelle, die Dauer jedes Falls in
Minuten. Fall i hat in jeder Quelle denselben Platz i. Die Durchlaufzeit
von Fall i ist die Summe seiner Dauern über alle Schritte. Dafür müssen
alle Quellen gleichzeitig offen sein, und wie viele es sind, steht erst
zur Laufzeit fest.

Eine `Messquelle` ist ein fertiger Kontextmanager: Beim Betreten öffnet
sie die Verbindung (das kann mit ConnectionError scheitern), beim
Verlassen schließt sie sie wieder, und beides vermerkt sie im gemeinsamen
Protokoll. Schreiben Sie `durchlaufzeiten(quellen, protokoll)`:

- Öffnen Sie alle Quellen in der Reihenfolge der Liste mit einem
  contextlib.ExitStack, lesen Sie jede mit lies() und geben Sie die Liste
  der Durchlaufzeiten aller Fälle zurück.
- Am Ende werden alle geöffneten Quellen geschlossen, in umgekehrter
  Reihenfolge, auch wenn etwas schiefgeht: Scheitert das Öffnen einer
  Quelle oder lies(), werden alle schon geöffneten wieder geschlossen,
  und die Ausnahme erreicht den Aufrufer unverändert.
- Als allerletzter Eintrag, nach dem Schließen, steht in jedem Fall
  "Auswertung beendet" im Protokoll, auch nach einem Fehler.
  Registrieren Sie das mit callback am ExitStack.

    protokoll = []
    quellen = [Messquelle("Prüfen", [5, 3], protokoll),
               Messquelle("Packen", [12, 20], protokoll)]
    durchlaufzeiten(quellen, protokoll)   →  [17, 23]
    protokoll  →  ["auf Prüfen", "auf Packen", "zu Packen", "zu Prüfen",
                   "Auswertung beendet"]

Grenzen: 0 ≤ len(quellen) ≤ 100. Alle Quellen liefern gleich viele Fälle,
0 bis 1000, jede Dauer ist eine ganze Zahl von 0 bis 10**6. Ohne Quellen
ist das Ergebnis die leere Liste. Jede Quelle darf beim Öffnen oder in
lies() einen Fehler auslösen. Jede Quelle wird höchstens einmal geöffnet.

Hintergrund: Mit with öffnet man eine feste Zahl von Ressourcen sicher:

    with Messquelle("A", …) as a, Messquelle("B", …) as b:
        …

Bei einer Liste unbekannter Länge geht das nicht, und von Hand wird es
schnell falsch: Scheitert die dritte Quelle, müssen die ersten beiden
trotzdem geschlossen werden, in umgekehrter Reihenfolge. Genau dafür gibt
es contextlib.ExitStack. Er ist selbst ein Kontextmanager und führt einen
Stapel von Aufräumarbeiten:

- `stapel.enter_context(cm)` ruft cm.__enter__() auf, gibt dessen
  Ergebnis zurück und legt cm.__exit__ oben auf den Stapel. Scheitert
  schon __enter__, kommt nichts auf den Stapel.
- `stapel.callback(funktion, *argumente)` legt einen beliebigen Aufruf
  auf den Stapel, etwa protokoll.append mit einem Text.
- Beim Verlassen des with-Blocks arbeitet der ExitStack den Stapel von
  oben nach unten ab (LIFO: zuletzt hinzugefügt, zuerst ausgeführt), auch
  wenn im Block eine Ausnahme fliegt; danach läuft die Ausnahme weiter.

    from contextlib import ExitStack

    with ExitStack() as stapel:
        stapel.callback(print, "zuletzt")
        dateien = [stapel.enter_context(open(name)) for name in namen]
        …                       # alle Dateien sind offen
    # hier sind alle geschlossen, dann wurde "zuletzt" ausgegeben

Was zuerst auf den Stapel kommt, läuft zuletzt. Ein callback, das nach
dem Schließen aller Quellen laufen soll, muss deshalb als Erstes
registriert werden. Wie ein Kontextmanager mit __exit__ auf Ausnahmen
reagiert, kennen Sie aus Aufgabe 5_025; ExitStack ruft die __exit__ aller
Einträge so auf, als stünden die with-Blöcke ineinander.

Tipp: zip(*listen) setzt aus mehreren gleich langen Listen die Einträge
mit gleichem Platz zusammen: list(zip(*[[5, 3], [12, 20]])) ist
[(5, 12), (3, 20)].
"""

from contextlib import ExitStack


class Messquelle:
    """Verbindung zu einem Prozessschritt, die Dauern liefert; als Kontextmanager zu öffnen."""

    def __init__(self, name, dauern, protokoll, defekt=False):
        """Merkt sich Name, Dauern und Protokoll; eine defekte Quelle lässt sich nicht öffnen."""
        self.name = name
        self.dauern = dauern
        self.protokoll = protokoll
        self.defekt = defekt
        self.offen = False

    def __enter__(self):
        """Öffnet die Verbindung; ConnectionError, wenn die Quelle defekt ist."""
        if self.defekt:
            raise ConnectionError(f"{self.name} nicht erreichbar")
        if self.offen:
            raise RuntimeError(f"{self.name} ist schon offen")
        self.offen = True
        self.protokoll.append(f"auf {self.name}")
        return self

    def __exit__(self, typ, wert, verlauf):
        """Schließt die Verbindung und lässt eine Ausnahme weiterlaufen."""
        self.offen = False
        self.protokoll.append(f"zu {self.name}")
        return False

    def lies(self):
        """Gibt die Dauern aller Fälle zurück; nur bei offener Verbindung."""
        if not self.offen:
            raise RuntimeError(f"{self.name} ist nicht geöffnet")
        return list(self.dauern)


def durchlaufzeiten(quellen, protokoll):
    """Öffnet alle Quellen, summiert die Dauern je Fall und schließt alles sicher wieder."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = []
quellen = [Messquelle("Prüfen", [5, 3], protokoll), Messquelle("Packen", [12, 20], protokoll)]
print(durchlaufzeiten(quellen, protokoll))
print(protokoll)
