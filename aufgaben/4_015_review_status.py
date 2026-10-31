"""Aufgabe 4_015 – Review-Status                                   Stufe 4 ★★★★☆

In einem Softwareteam geht jede Änderung am Code durch ein Review, bevor
sie in den Hauptzweig darf. Ein kleines Werkzeug verwaltet dafür den
Status jeder Änderung. Bisher stand der Status als Text in der
Datenbank, und es gab Ärger: Mal stand dort "freigegeben", mal
"Freigegeben", einmal sogar "frei gegeben", und eine Abfrage nach
freigegebenen Änderungen fand nur einen Teil. Das Team stellt deshalb
auf eine Aufzählung mit festen Namen um.

Ein Status darf nur auf bestimmte Weise wechseln:

    ENTWURF           →  IN_PRUEFUNG
    IN_PRUEFUNG       →  FREIGEGEBEN oder ABGELEHNT
    ABGELEHNT         →  ENTWURF          (überarbeiten)
    FREIGEGEBEN       →  ZUSAMMENGEFUEHRT
    ZUSAMMENGEFUEHRT  →  (nichts mehr)

Vervollständigen Sie:

- `Status` als Unterklasse von enum.Enum mit den fünf Mitgliedern in
  dieser Reihenfolge und den Texten für die Anzeige als Werten:
  ENTWURF = "Entwurf", IN_PRUEFUNG = "In Prüfung", FREIGEGEBEN =
  "Freigegeben", ABGELEHNT = "Abgelehnt", ZUSAMMENGEFUEHRT =
  "Zusammengeführt". Das Dictionary UEBERGAENGE mit den erlaubten
  Wechseln steht schon im Code.
- `wechsle(aktuell, neu)` gibt neu zurück, wenn der Wechsel von aktuell
  nach neu erlaubt ist. Sonst löst sie einen ValueError aus, der beide
  Anzeigetexte nennt. Ist neu kein Status (etwa der Text "Freigegeben"),
  löst sie einen TypeError aus.
- `status_aus_text(text)` gibt den Status zu einem Anzeigetext zurück,
  ohne Rücksicht auf Groß- und Kleinschreibung und auf Leerzeichen am
  Anfang und Ende. Passt kein Status, kommt ein ValueError.
- `statistik(zustaende)` bekommt eine Liste von Status und gibt ein
  Dictionary zurück, das jedem der fünf Status die Zahl seiner Vorkommen
  zuordnet, in der Reihenfolge der Aufzählung, auch mit 0.

    wechsle(Status.ENTWURF, Status.IN_PRUEFUNG)   →  Status.IN_PRUEFUNG
    wechsle(Status.ENTWURF, Status.FREIGEGEBEN)   →  ValueError
    status_aus_text("  in prüfung ")              →  Status.IN_PRUEFUNG
    Status.FREIGEGEBEN.name                       →  "FREIGEGEBEN"
    Status.FREIGEGEBEN.value                      →  "Freigegeben"
    statistik([Status.ENTWURF, Status.ABGELEHNT, Status.ENTWURF])
        →  {Status.ENTWURF: 2, Status.IN_PRUEFUNG: 0, Status.FREIGEGEBEN: 0,
            Status.ABGELEHNT: 1, Status.ZUSAMMENGEFUEHRT: 0}

Grenzen: aktuell ist ein Status, neu ein beliebiges Objekt. text ist
ein beliebiger Text mit höchstens 50 Zeichen. zustaende ist eine Liste
mit 0 bis 100 000 Status.

Hintergrund: Eine Aufzählung (Enum) ist eine Klasse mit einer festen
Menge benannter Werte. Man schreibt sie als Unterklasse von Enum, jedes
Klassenattribut wird ein Mitglied:

    from enum import Enum

    class Ampel(Enum):
        ROT = "rot"
        GELB = "gelb"
        GRUEN = "grün"

Ampel.ROT ist ein Objekt vom Typ Ampel mit dem Namen ROT (Ampel.ROT.name)
und dem Wert "rot" (Ampel.ROT.value). Jedes Mitglied gibt es genau
einmal, darum vergleicht man mit is oder ==. Ein Tippfehler wie
Ampel.RTO ist sofort ein AttributeError, während der Text "rto" still
durchrutschen würde. Ein Mitglied ist auch nicht gleich seinem Wert:
Ampel.ROT == "rot" ist False.

Über eine Aufzählung kann man iterieren; die Reihenfolge ist die der
Definition: list(Ampel) ergibt [Ampel.ROT, Ampel.GELB, Ampel.GRUEN].
Zum Nachschlagen gibt es zwei Wege: Ampel("gelb") sucht nach dem Wert,
Ampel["GELB"] nach dem Namen; passt nichts, kommt ValueError bzw.
KeyError. Mitglieder sind hashbar und taugen darum als Schlüssel in
Dictionaries und Mengen, so wie in UEBERGAENGE. Mit enum.auto() lässt
man Python die Werte vergeben, wenn sie egal sind.

Tipp: isinstance(neu, Status) prüft, ob neu ein Mitglied der Aufzählung
ist.
"""

from enum import Enum


class Status(Enum):
    """Der Status einer Änderung im Review; der Wert ist der Text für die Anzeige."""

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


UEBERGAENGE = {
    Status.ENTWURF: {Status.IN_PRUEFUNG},
    Status.IN_PRUEFUNG: {Status.FREIGEGEBEN, Status.ABGELEHNT},
    Status.ABGELEHNT: {Status.ENTWURF},
    Status.FREIGEGEBEN: {Status.ZUSAMMENGEFUEHRT},
    Status.ZUSAMMENGEFUEHRT: set(),
}


def wechsle(aktuell, neu):
    """Gibt neu zurück, wenn der Wechsel erlaubt ist; sonst ValueError, TypeError bei einem Nicht-Status."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def status_aus_text(text):
    """Gibt den Status zum Anzeigetext zurück, ohne Rücksicht auf Groß-/Kleinschreibung und Rand-Leerzeichen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def statistik(zustaende):
    """Gibt für jeden Status in der Reihenfolge der Aufzählung zurück, wie oft er in zustaende vorkommt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


status = Status.ENTWURF
for schritt in ["In Prüfung", "abgelehnt", "Entwurf", "in prüfung", "FREIGEGEBEN"]:
    status = wechsle(status, status_aus_text(schritt))
print(status.name, status.value)
print(statistik([Status.ENTWURF, Status.ABGELEHNT, Status.ENTWURF]))
