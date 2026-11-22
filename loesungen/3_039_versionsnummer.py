# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_039_versionsnummer.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_039_versionsnummer

"""Aufgabe 3_039 – Versionsnummer                                Stufe 3 ★★★☆☆

Viele Softwareprojekte nummerieren ihre Veröffentlichungen nach dem
Schema Major.Minor.Patch, zum Beispiel 2.4.1: Die erste Zahl steigt bei
Änderungen, die alte Programme brechen, die zweite bei neuen Funktionen,
die dritte bei Fehlerkorrekturen. Ein Werkzeug, das Abhängigkeiten
zwischen Bibliotheken prüft, soll Versionen als Objekte speichern.
Vervollständigen Sie die Klasse `Version`:

- `__init__(self, major, minor, patch=0)` speichert die drei Zahlen in
  den Attributen `major`, `minor` und `patch`.
- `__str__(self)` gibt die Version als Text wie "2.4.1" zurück, die drei
  Zahlen mit Punkten dazwischen, ohne Leerzeichen.
- `__eq__(self, andere)` gibt True zurück, wenn andere auch eine Version
  ist und alle drei Zahlen übereinstimmen. Ist andere keine Version
  (etwa der Text "2.4.1" oder None), gibt es False zurück, ohne Fehler.

    v = Version(2, 4, 1)
    str(v)                       →  "2.4.1"
    print(v)                     gibt 2.4.1 aus
    v == Version(2, 4, 1)        →  True
    v == Version(2, 4)           →  False   (patch ist dann 0)
    v != Version(2, 5, 1)        →  True
    v in [Version(1, 0), Version(2, 4, 1)]   →  True
    v == "2.4.1"                 →  False

Grenzen: major, minor und patch sind ganze Zahlen von 0 bis 10**6.
andere kann ein beliebiges Objekt sein.

Hintergrund: Eine Klasse mit __init__ und Methoden kennen Sie aus
Aufgabe 3_037. Gibt man ein Objekt einer solchen Klasse aus, steht da
etwas wie <__main__.Version object at 0x7f…>, und zwei Objekte mit
denselben Werten gelten als verschieden, weil == ohne weitere Angabe
nur prüft, ob es dasselbe Objekt ist. Beides kann man ändern, indem man
besondere Methoden mit zwei Unterstrichen vorn und hinten schreibt
(„dunder“-Methoden, von double underscore). Python ruft sie selbst auf:

- str(objekt), print(objekt) und f"{objekt}" rufen objekt.__str__() auf;
  die Methode muss einen Text zurückgeben.
- a == b ruft a.__eq__(b) auf; die Methode gibt True oder False zurück.
  Auch a != b und x in liste benutzen __eq__.

    class Punkt:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return f"({self.x}|{self.y})"

        def __eq__(self, andere):
            if not isinstance(andere, Punkt):
                return False
            return self.x == andere.x and self.y == andere.y

isinstance(andere, Punkt) prüft, ob andere ein Punkt ist. Ohne diese
Prüfung würde Punkt(1, 2) == None mit einem AttributeError abbrechen,
weil None kein Attribut x hat.
"""


class Version:
    """Eine Versionsnummer nach dem Schema Major.Minor.Patch."""

    def __init__(self, major, minor, patch=0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        """Gibt die Version als Text wie "2.4.1" zurück."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, andere):
        """Gibt True zurück, wenn andere eine Version mit denselben drei Zahlen ist."""
        if not isinstance(andere, Version):
            return False
        return self.major == andere.major and self.minor == andere.minor and self.patch == andere.patch


v = Version(2, 4, 1)
print(v)
print(v == Version(2, 4, 1), v == Version(2, 4))


# Idee: __init__ legt die drei Zahlen als Attribute an, patch mit dem Standardwert 0. __str__ setzt
# sie mit einem f-String und Punkten zusammen. __eq__ prüft zuerst mit isinstance, ob das Gegenüber
# überhaupt eine Version ist, und vergleicht dann alle drei Attribute. Weil Python != und in auf
# __eq__ zurückführt, funktionieren sie danach von selbst.
# Anderer Weg: In __eq__ die Zahlen als Tupel vergleichen: (self.major, self.minor, self.patch) ==
# (andere.major, andere.minor, andere.patch). Statt False kann man bei fremden Typen auch
# NotImplemented zurückgeben; dann fragt Python das andere Objekt und vergleicht zuletzt die Identität,
# was ebenfalls False ergibt. In __str__ geht auch ".".join([str(self.major), ...]).
# Typische Fehler: in __str__ print statt return (str() bricht dann mit TypeError ab), nur zwei der
# drei Zahlen vergleichen, die isinstance-Prüfung vergessen (AttributeError bei None oder einem Text)
# oder str(self) == str(andere) vergleichen (dann wäre auch ein Text "2.4.1" gleich).
# Laufzeit: Alle Methoden brauchen O(1) Schritte.
# Ausblick: Mit eigenem __eq__ setzt Python __hash__ auf None; Versionen passen dann nicht mehr in
# eine Menge oder als Schlüssel in ein Dictionary (TypeError: unhashable type). Wie man das löst,
# zeigt Aufgabe 4_003.
