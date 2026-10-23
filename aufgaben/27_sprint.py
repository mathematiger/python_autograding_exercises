"""Aufgabe 27 – Sprintplanung                                    Stufe 4 ★★★★☆

Ein Entwicklungsteam arbeitet in Sprints, festen Zeitabschnitten von zwei
Wochen. Vor jedem Sprint schätzt das Team, wie viel Arbeit es schafft: die
Kapazität in Story Points, einer Einheit für den Aufwand. Dann plant es
Aufgaben aus dem Backlog, der Liste aller offenen Aufgaben, in den Sprint
ein, jede mit ihren Story Points. Die Klasse `Sprint` soll dabei helfen.
Vorgegeben sind __init__ und einplanen; vervollständigen Sie drei Properties:

- `kapazitaet` liefert die Kapazität. Der Setter prüft den neuen Wert: Ist er
  0 oder kleiner, löst er einen ValueError aus. Ebenso, wenn er kleiner ist
  als die schon eingeplanten Story Points. Nur ein gültiger Wert wird in
  self._kapazitaet gespeichert.
- `geplant` liefert die Summe der Story Points aller eingeplanten Aufgaben.
  Diesen Wert kann man nur lesen, nicht zuweisen (kein Setter).
- `auslastung` liefert, wie viel Prozent der Kapazität verplant sind, also
  geplant / kapazitaet * 100. Auch ohne Setter.

    sprint = Sprint(40)
    sprint.einplanen("Anmeldung per E-Mail", 13)
    sprint.einplanen("Passwort zurücksetzen", 8)
    sprint.geplant       →  21
    sprint.auslastung    →  52.5
    sprint.kapazitaet = 30      (Team ist krank, Kapazität sinkt)
    sprint.auslastung    →  70.0
    sprint.kapazitaet = 20  →  ValueError   (21 Punkte sind schon geplant)
    sprint.kapazitaet = 0   →  ValueError
    sprint.geplant = 5      →  AttributeError
    Sprint(-3)              →  ValueError

Hintergrund: Von außen sieht ein Attribut wie sprint.kapazitaet einfach aus:
lesen mit sprint.kapazitaet, ändern mit sprint.kapazitaet = 30. Will man beim
Ändern aber prüfen oder beim Lesen etwas ausrechnen, braucht man Methoden.
Damit der Aufruf trotzdem wie ein Attribut aussieht, gibt es den Dekorator
@property. Er macht aus einer Methode ein Attribut, dessen Wert beim Lesen
berechnet wird; mit @<name>.setter kommt eine zweite Methode für das
Zuweisen dazu:

    class Kreis:
        def __init__(self, radius):
            self.radius = radius          # ruft schon den Setter auf

        @property
        def radius(self):
            return self._radius           # der echte Wert liegt in _radius

        @radius.setter
        def radius(self, wert):
            if wert < 0:
                raise ValueError("Der Radius darf nicht negativ sein.")
            self._radius = wert

        @property
        def flaeche(self):
            return 3.14159 * self._radius ** 2

    k = Kreis(2)
    k.flaeche      →  12.56636   (ohne Klammern!)
    k.radius = -1  →  ValueError, k.radius bleibt 2
    k.flaeche = 5  →  AttributeError, es gibt keinen Setter

Der eigentliche Wert muss unter einem anderen Namen gespeichert werden, meist
mit Unterstrich davor (_radius). Würde der Setter self.radius = wert
schreiben, riefe er sich selbst auf, immer wieder. Der Unterstrich sagt
außerdem: „Bitte nur über die Property benutzen.“ Weil auch __init__ über den
Setter geht, kann es kein Objekt mit ungültigem Wert geben. Berechnete
Properties wie flaeche sind immer aktuell, denn sie werden bei jedem Lesen
neu ausgerechnet, statt einmal gespeichert und dann vergessen zu werden.

Tipp: In geplant können Sie mit sum(...) über die Punkte in self.aufgaben
summieren; einplanen speichert dort Paare (titel, punkte).
"""


class Sprint:
    """Ein Sprint mit Kapazität in Story Points und eingeplanten Aufgaben."""

    def __init__(self, kapazitaet):
        """Legt einen leeren Sprint an; die Kapazität prüft der Setter."""
        self.aufgaben = []
        self.kapazitaet = kapazitaet

    def einplanen(self, titel, punkte):
        """Plant eine Aufgabe mit ihren Story Points ein, wenn sie noch passt."""
        if self.geplant + punkte > self.kapazitaet:
            raise ValueError(f"{titel!r} passt nicht mehr in den Sprint.")
        self.aufgaben.append((titel, punkte))

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


sprint = Sprint(40)
sprint.einplanen("Anmeldung per E-Mail", 13)
sprint.einplanen("Passwort zurücksetzen", 8)
print(sprint.geplant, sprint.auslastung)
sprint.kapazitaet = 30
print(sprint.kapazitaet, sprint.auslastung)
