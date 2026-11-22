"""Aufgabe 4_042 – Rollenrechte                                  Stufe 4 ★★★★☆

Im Berechtigungskonzept eines Unternehmens bekommt niemand Rechte
direkt, sondern nur über Rollen: Die Rolle "vertrieb" darf etwa
"crm_lesen" und "angebote_schreiben", die Rolle "support" darf
"crm_lesen" und "tickets_bearbeiten". Wer mehrere Rollen hat, hat alle
ihre Rechte zusammen. Einmal im Quartal prüft die IT-Sicherheit, ob die
Rechte noch stimmen. Schreiben Sie mit dem Modul itertools drei
Funktionen:

- `alle_konten(admins, dienstkonten, gaeste)` gibt einen Iterator
  zurück, der erst alle Namen aus admins, dann aus dienstkonten, dann
  aus gaeste liefert, ohne vorher eine gemeinsame Liste zu bauen
  (itertools.chain). Die drei Argumente können Listen oder Iteratoren
  sein, auch solche, die die Namen erst beim Abholen erzeugen.
- `rechte_von(rollen, rollenrechte)` gibt die Liste aller Rechte zurück,
  die die Rollen in der Liste rollen zusammen haben. rollenrechte
  ordnet jeder Rolle die Liste ihrer Rechte zu. Jedes Recht steht nur
  einmal in der Liste, an der Stelle seines ersten Vorkommens, wenn man
  die Rollen der Reihe nach durchgeht (itertools.chain.from_iterable).
- `aenderungen(vorher, nachher)` vergleicht zwei Exporte einer
  Rechteliste Zeile für Zeile und gibt eine Liste von Tupeln (zeile,
  alt, neu) für jede Zeile zurück, in der sich etwas geändert hat. zeile
  zählt ab 1. Ist eine Liste kürzer, steht für ihre fehlenden Zeilen
  None (itertools.zip_longest).

    list(alle_konten(["root"], ["backup"], ["gast1", "gast2"]))
        →  ["root", "backup", "gast1", "gast2"]
    rollenrechte = {"vertrieb": ["crm_lesen", "angebote_schreiben"],
                    "support": ["crm_lesen", "tickets_bearbeiten"]}
    rechte_von(["vertrieb", "support"], rollenrechte)
        →  ["crm_lesen", "angebote_schreiben", "tickets_bearbeiten"]
    aenderungen(["a", "b", "c"], ["a", "x"])
        →  [(2, "b", "x"), (3, "c", None)]

Grenzen: Zusammen höchstens 100 000 Namen in den drei Gruppen. rollen
hat 0 bis 1000 Einträge, jeder ist ein Schlüssel von rollenrechte; jede
Rolle hat 0 bis 100 Rechte; insgesamt höchstens 100 000 Rechte.
Namen und Rechte sind nicht leere Texte. vorher und nachher haben je 0
bis 100 000 Zeilen, Texte ohne None. Ihre Lösung soll O(n) Schritte
brauchen.

Hintergrund: In Aufgabe 4_040 haben Sie unendliche Iteratoren aus
itertools kennengelernt. Das Modul hat auch Werkzeuge, die mehrere
endliche Iterables verbinden, ohne sie zu kopieren.

chain hängt Iterables hintereinander. Anders als liste1 + liste2 baut es
keine neue Liste, sondern liefert die Werte erst beim Abholen, eins
nach dem anderen, und funktioniert auch mit Generatoren:

    from itertools import chain

    list(chain([1, 2], (3,), "ab"))      →  [1, 2, 3, "a", "b"]

Liegen die Iterables selbst in einer Liste oder kommen sie aus einem
Generator, nimmt man chain.from_iterable. Das „klopft“ eine
verschachtelte Struktur eine Ebene flach:

    gruppen = [["a", "b"], [], ["c"]]
    list(chain.from_iterable(gruppen))    →  ["a", "b", "c"]
    list(chain.from_iterable(d[k] for k in schluessel))

Doppelte entfernt man, ohne die Reihenfolge zu verlieren, mit einer
Menge für das schnelle „schon gesehen?“ (Aufgabe 2_028) und einer Liste
für das Ergebnis. dict.fromkeys(werte) geht auch: Ein Dictionary behält
die Reihenfolge, in der die Schlüssel zuerst eingefügt wurden.

zip (Aufgabe 2_022) hört auf, sobald das kürzeste Iterable leer ist.
zip_longest macht weiter, bis auch das längste fertig ist, und füllt
die Lücken mit fillvalue auf (ohne Angabe None):

    from itertools import zip_longest

    list(zip_longest("ab", "xyz"))                 →  [("a", "x"), ("b", "y"), (None, "z")]
    list(zip_longest([1], [2, 3], fillvalue=0))    →  [(1, 2), (0, 3)]

Mit enumerate(..., start=1) bekommt jedes Paar zusätzlich seine
Zeilennummer.
"""

from itertools import chain, zip_longest


def alle_konten(admins, dienstkonten, gaeste):
    """Gibt einen Iterator über alle Namen der drei Gruppen nacheinander zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def rechte_von(rollen, rollenrechte):
    """Gibt alle Rechte der Rollen ohne Doppelte in der Reihenfolge des ersten Vorkommens zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def aenderungen(vorher, nachher):
    """Gibt (zeile, alt, neu) für jede geänderte Zeile zurück; fehlende Zeilen sind None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(list(alle_konten(["root"], ["backup"], ["gast1", "gast2"])))
rollenrechte = {
    "vertrieb": ["crm_lesen", "angebote_schreiben"],
    "support": ["crm_lesen", "tickets_bearbeiten"],
}
print(rechte_von(["vertrieb", "support"], rollenrechte))
print(aenderungen(["a", "b", "c"], ["a", "x"]))
