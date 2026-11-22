"""Aufgabe 5_031 – Lagertransaktion                              Stufe 5 ★★★★★

Ein kleines Warenwirtschaftssystem hält seinen Lagerbestand in einem
Dictionary: Artikelnummer → Stückzahl. Lieferungen und Entnahmen kommen
als Listen von Buchungen (artikel, menge) herein, eine positive Menge
ist ein Zugang, eine negative ein Abgang. Wie in einer Datenbank soll
jede Lieferung eine Transaktion sein: Entweder gelten alle ihre
Buchungen oder keine. Geht mitten in einer Lieferung etwas schief, muss
der Bestand wieder genau so aussehen wie vorher; das nennt man
Zurückrollen (Rollback), das Übernehmen heißt Commit.

Schreiben Sie mit contextlib.contextmanager den Kontextmanager
`transaktion(tabelle, protokoll)`:

- Beim Betreten sichert er den Inhalt von tabelle, schreibt "BEGIN" in
  die Liste protokoll und gibt tabelle selbst an das as weiter.
- Endet der with-Block normal, schreibt er "COMMIT"; die Änderungen
  bleiben.
- Endet der Block mit der vorgegebenen Ausnahme Abbruch, setzt er
  tabelle auf den gesicherten Inhalt zurück, schreibt "ROLLBACK" und
  schluckt die Ausnahme: Ein Abbruch ist gewollt und kein Fehler.
- Endet der Block mit einer anderen Ausnahme (Exception), setzt er
  ebenfalls zurück, schreibt "ROLLBACK" und lässt die Ausnahme
  weiterlaufen.
- Zurückgesetzt wird dasselbe Dictionary-Objekt, nicht ein neues; wer
  vorher eine Referenz auf tabelle hatte, sieht den alten Inhalt.

Dazu die Funktion `importiere(tabelle, protokoll, lieferungen)`, die
jede Lieferung in einer eigenen Transaktion bucht und zurückgibt, wie
viele Lieferungen übernommen wurden. Würde eine Buchung einen Bestand
unter 0 bringen, löst sie Abbruch aus; diese Lieferung entfällt, und
die nächste wird gebucht. Andere Fehler (etwa eine Menge, die keine
Zahl ist) brechen den ganzen Import ab, nachdem die fehlerhafte
Lieferung zurückgerollt ist.

    lager = {"A-1": 5, "B-2": 0}
    protokoll = []
    importiere(lager, protokoll, [[("A-1", -2), ("B-2", 3)],
                                  [("A-1", -9)],
                                  [("C-3", 1)]])     →  2
    lager       →  {"A-1": 3, "B-2": 3, "C-3": 1}
    protokoll   →  ["BEGIN", "COMMIT", "BEGIN", "ROLLBACK", "BEGIN", "COMMIT"]

Grenzen: tabelle hat 0 bis 10 000 Einträge mit Texten als Schlüsseln und
ganzen Zahlen als Werten. Es gibt bis zu 1000 Lieferungen mit zusammen
bis zu 100 000 Buchungen; ein Artikel, den es noch nicht gibt, beginnt
bei 0. Transaktionen dürfen verschachtelt werden: Eine innere, die
zurückrollt, setzt nur auf den Stand bei ihrem eigenen Beginn zurück.

Hintergrund: Ein Kontextmanager ist ein Objekt mit __enter__ und
__exit__ (Aufgabe 5_025). Oft ist es einfacher, ihn als Generator zu
schreiben: contextlib.contextmanager macht aus einer Generatorfunktion
mit genau einem yield einen Kontextmanager. Was vor dem yield steht,
läuft beim Betreten, der Wert hinter yield landet hinter as, und was
nach dem yield steht, läuft beim Verlassen:

    from contextlib import contextmanager

    @contextmanager
    def gesperrt(sperren, name):
        sperren.add(name)
        try:
            yield name
        finally:
            sperren.discard(name)

Der Fehlerpfad ist der wichtige Teil: Löst der with-Block eine
Ausnahme aus, wirft contextmanager sie genau an der Stelle des yield in
den Generator hinein. Ohne try läuft der Code nach dem yield dann gar
nicht, und die Sperre bliebe stehen. Mit try/finally wird immer
aufgeräumt. Mit except kann man je nach Art der Ausnahme verschieden
reagieren, und else läuft nur, wenn keine Ausnahme kam:

    try:
        yield
    except KeyError:
        ...          # ohne raise: die Ausnahme ist geschluckt
    except Exception:
        ...
        raise        # die Ausnahme läuft weiter zum Aufrufer
    else:
        ...          # nur ohne Ausnahme

Endet der Generator nach einer Ausnahme normal, gilt sie als behandelt,
so wie ein __exit__, das True zurückgibt. Wer sie weitermelden will,
muss sie mit raise ohne Argument erneut auslösen (Aufgabe 3_031).

Zur Wiederverwendung: Jeder Aufruf transaktion(lager, protokoll) baut
einen neuen Generator, darum kann man die Funktion beliebig oft in with
benutzen, auch verschachtelt. Ein einzelnes Objekt cm =
transaktion(...) dagegen lässt sich nur einmal betreten, beim zweiten
with cm: gibt es einen Fehler, denn sein Generator ist schon
verbraucht. Außerdem ist jeder solche Kontextmanager zugleich ein
Dekorator: @transaktion(lager, protokoll) über einer Funktion führt
jeden Aufruf in einer frischen Transaktion aus.

Ein Dictionary setzt man an Ort und Stelle zurück mit tabelle.clear()
und tabelle.update(sicherung); dict(tabelle) legt vorher eine Kopie an.
"""

from contextlib import contextmanager


class Abbruch(Exception):
    """Bricht eine Transaktion gewollt ab: zurückrollen, aber nicht weitermelden (vorgegeben)."""


@contextmanager
def transaktion(tabelle, protokoll):
    """Führt den with-Block als Transaktion auf tabelle aus: COMMIT oder ROLLBACK."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def importiere(tabelle, protokoll, lieferungen):
    """Bucht jede Lieferung in einer eigenen Transaktion; gibt die Zahl der übernommenen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


lager = {"A-1": 5, "B-2": 0}
protokoll = []
print(importiere(lager, protokoll, [[("A-1", -2), ("B-2", 3)], [("A-1", -9)], [("C-3", 1)]]))
print(lager)
print(protokoll)
