"""Aufgabe 5_038 – Routingentwurf                                Stufe 5 ★★★★★

Ein Router entscheidet für jedes Paket anhand seiner Routingtabelle,
wohin er es weiterschickt: Zu jedem Zielnetz wie "10.20.0.0/16" steht
dort eine Liste von Next Hops, den Adressen der nächsten Router auf dem
Weg; stehen mehrere da, verteilt er die Pakete auf alle. Ein
Planungswerkzeug hält für jeden Router ein Objekt Routingtabelle. Bevor
eine Änderung auf das echte Gerät geht, probiert das Netzwerkteam sie an
einer Kopie aus, einem Entwurf. Dafür muss klar sein, was eine Kopie
teilt und was nicht:

- router ist das Objekt für das echte Gerät mit seiner Sperre gegen
  gleichzeitige Änderungen. Es gibt das Gerät nur einmal; jede Kopie
  verweist auf dasselbe Router-Objekt.
- aenderungen ist das Protokoll dieser einen Tabelle. Eine Kopie
  beginnt mit einem leeren Protokoll.
- routen ist das Dictionary Zielnetz → Liste der Next Hops.

Ergänzen Sie in der Klasse `Routingtabelle`:

- `__copy__(self)` für copy.copy: ein neues Dictionary routen mit
  denselben Listen darin (ein schneller Entwurf, der nur Zielnetze
  hinzufügt oder entfernt).
- `__deepcopy__(self, memo)` für copy.deepcopy: routen mit allen Listen
  tief kopiert. Geben Sie memo an copy.deepcopy weiter, damit eine Liste,
  die in der Tabelle und anderswo im kopierten Ganzen vorkommt, auch in
  der Kopie nur einmal existiert.

Beide geben eine neue Routingtabelle mit demselben router und leerem
Protokoll zurück; das Original bleibt unverändert.

    kern = Router("kern-01")
    tabelle = Routingtabelle(kern)
    tabelle.setze("10.20.0.0/16", ["192.168.0.2", "192.168.0.3"])
    tabelle.setze("0.0.0.0/0", ["192.168.0.1"])

    flach = copy.copy(tabelle)
    flach.routen is tabelle.routen                                   →  False
    flach.routen["0.0.0.0/0"] is tabelle.routen["0.0.0.0/0"]         →  True
    flach.router is kern, flach.aenderungen                          →  (True, [])

    tief = copy.deepcopy(tabelle)        # ohne __deepcopy__: TypeError wegen der Sperre
    tief.ergaenze("0.0.0.0/0", "192.168.0.9")
    tabelle.routen["0.0.0.0/0"]                                      →  ['192.168.0.1']
    tief.router is kern, tief.aenderungen                            →  (True, ['ergaenze 0.0.0.0/0'])

Grenzen: routen hat 0 bis 10 000 Zielnetze mit je 0 bis 8 Next Hops,
alle als Texte. aenderungen hat 0 bis 10 000 Einträge.

Hintergrund: Eine Zuweisung b = a kopiert nichts; beide Namen zeigen auf
dasselbe Objekt (Aufgabe 2_018). Das Modul copy kopiert wirklich, und
zwar auf zwei Arten. copy.copy(x) ist flach: ein neuer Behälter, aber
dieselben Objekte darin. copy.deepcopy(x) ist tief: Es kopiert den
Behälter und, Schritt für Schritt, alles, was darin steckt:

    import copy

    plan = {"montag": ["Ada"], "dienstag": ["Bo"]}
    flach = copy.copy(plan)            # wie dict(plan)
    tief = copy.deepcopy(plan)
    plan["montag"].append("Cem")
    flach["montag"]                    # ['Ada', 'Cem'] – dieselbe Liste
    tief["montag"]                     # ['Ada']        – eine eigene Liste

Bei Objekten eigener Klassen kopiert copy ohne weitere Angabe das
__dict__, flach oder tief, über __getstate__ und __setstate__ wie
pickle (Aufgabe 5_037). Das passt selten: Tief kopiert es auch Dinge,
die es nur einmal geben darf, und scheitert an allem, was sich nicht
kopieren lässt, etwa an einem threading.Lock (TypeError); flach teilt es
auch Dinge, die jede Kopie für sich braucht. Darum darf eine Klasse
selbst bestimmen, wie sie kopiert wird. copy.copy ruft __copy__() auf,
copy.deepcopy ruft __deepcopy__(memo) auf:

    class Messreihe:
        def __init__(self, sensor, werte):
            self.sensor = sensor               # geteilt: das Gerät gibt es einmal
            self.werte = werte

        def __copy__(self):
            return Messreihe(self.sensor, list(self.werte))

        def __deepcopy__(self, memo):
            neu = Messreihe.__new__(Messreihe)  # ohne __init__
            memo[id(self)] = neu                # vor dem Kopieren der Inhalte eintragen
            neu.sensor = self.sensor
            neu.werte = copy.deepcopy(self.werte, memo)
            return neu

memo ist ein Dictionary id(Original) → Kopie, das copy.deepcopy durch
den ganzen Kopiervorgang reicht. Bevor es ein Objekt kopiert, schaut es
dort nach; ist das Objekt schon kopiert, nimmt es dieselbe Kopie. So
bleibt erhalten, dass zwei Stellen auf dasselbe Objekt zeigen, und
Ringe (ein Objekt, das über andere auf sich selbst verweist) führen nicht
zu einer endlosen Rekursion. Darum gibt man memo bei jedem inneren
deepcopy weiter, statt ein neues anzufangen, und trägt das neue Objekt
gleich nach dem Anlegen ein. Ob man in __copy__ und __deepcopy__ über
__init__ oder über cls.__new__ geht, ist Geschmackssache; über __new__
läuft keine Prüfung oder Nebenwirkung aus __init__ ein zweites Mal.
"""

import copy
import threading


class Router:
    """Ein echtes Gerät; es gibt jedes nur einmal, darum hat es eine Sperre gegen gleichzeitige Änderungen."""

    def __init__(self, name):
        """Merkt sich den Namen und legt die Sperre an."""
        self.name = name
        self.sperre = threading.Lock()


class Routingtabelle:
    """Die Routingtabelle eines Routers mit Zielnetzen, Next Hops und Änderungsprotokoll."""

    def __init__(self, router):
        """Legt eine leere Tabelle für den Router an."""
        self.router = router
        self.routen = {}
        self.aenderungen = []

    def setze(self, ziel, next_hops):
        """Setzt die Next Hops für ein Zielnetz und protokolliert die Änderung."""
        self.routen[ziel] = list(next_hops)
        self.aenderungen.append(f"setze {ziel}")

    def ergaenze(self, ziel, next_hop):
        """Hängt einen Next Hop an die Liste eines vorhandenen Zielnetzes an und protokolliert das."""
        self.routen[ziel].append(next_hop)
        self.aenderungen.append(f"ergaenze {ziel}")

    def __copy__(self):
        """Gibt eine flache Kopie zurück: neues Dictionary, dieselben Listen, derselbe Router, leeres Protokoll."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __deepcopy__(self, memo):
        """Gibt eine tiefe Kopie zurück: alle Listen kopiert, derselbe Router, leeres Protokoll."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kern = Router("kern-01")
tabelle = Routingtabelle(kern)
tabelle.setze("10.20.0.0/16", ["192.168.0.2", "192.168.0.3"])
tabelle.setze("0.0.0.0/0", ["192.168.0.1"])
flach = copy.copy(tabelle)
print(flach.routen is tabelle.routen, flach.routen["0.0.0.0/0"] is tabelle.routen["0.0.0.0/0"], flach.aenderungen)
tief = copy.deepcopy(tabelle)
tief.ergaenze("0.0.0.0/0", "192.168.0.9")
print(tabelle.routen["0.0.0.0/0"], tief.router is kern, tief.aenderungen)
