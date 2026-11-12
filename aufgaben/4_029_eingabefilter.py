"""Aufgabe 4_029 – Eingabefilter                                 Stufe 4 ★★★★☆

Die IT-Sicherheit einer Firma baut ein kleines Prüfmodul für ihre
Webanwendungen. Drei Teile darin fassen jeweils viele Werte zu einem
einzigen zusammen:

- `pruefsumme(daten)` bekommt die Bytes einer Nachricht und verknüpft alle
  mit XOR (`^`) zu einer Zahl von 0 bis 255, der Längsparität. Ändert sich
  unterwegs ein einzelnes Bit, ändert sich auch die Prüfsumme. Leere Daten
  haben die Prüfsumme 0.
- `alle_rechte(rollen)` bekommt die Rollen eines Kontos als Liste von
  Mengen von Rechten und gibt die Menge aller Rechte zurück, die das Konto
  über irgendeine Rolle hat (die Vereinigung). Ohne Rollen ist das die
  leere Menge. Die übergebenen Mengen bleiben unverändert.
- `bereinige(text, schritte)` bekommt einen Text aus einem Formularfeld und
  eine Liste von Funktionen, die je einen Text bekommen und einen Text
  zurückgeben. Sie wendet die Funktionen der Reihe nach an, die erste
  zuerst, jede auf das Ergebnis der vorigen, und gibt das Ergebnis zurück.
  Ohne Schritte bleibt der Text, wie er ist.

    pruefsumme(b"\\x0f\\xf0\\x01")              →  254
    pruefsumme(b"")                           →  0
    alle_rechte([{"lesen"}, {"lesen", "schreiben"}])  →  {"lesen", "schreiben"}
    alle_rechte([])                           →  set()
    bereinige("  <b>Admin</b> ", [str.strip, entferne_spitze_klammern, str.lower])
                                              →  "badmin/b"

Benutzen Sie in allen drei Funktionen functools.reduce statt einer
eigenen Schleife.

Grenzen: daten hat 0 bis 10**5 Bytes. rollen hat 0 bis 1000 Einträge, jede
Menge 0 bis 50 Rechte (nicht leere Texte). text hat höchstens 1000
Zeichen, schritte 0 bis 20 Funktionen.

Hintergrund: Viele Rechnungen falten eine Folge zu einem einzigen Wert:
Summe, Produkt, Maximum, Vereinigung. Das Muster ist immer gleich: ein
Zwischenergebnis, das mit jedem Element zu einem neuen Zwischenergebnis
verknüpft wird. functools.reduce erledigt genau diese Schleife:

    from functools import reduce
    reduce(funktion, folge, startwert)

ruft funktion(startwert, erstes) auf, dann funktion(ergebnis, zweites) und
so weiter, und gibt das letzte Ergebnis zurück. Die Funktion bekommt also
immer zwei Argumente: das bisherige Ergebnis und das nächste Element.

    reduce(lambda a, b: a + b, [3, 4, 5], 0)   →  ((0 + 3) + 4) + 5 = 12
    reduce(max, [3, 9, 2])                     →  max(max(3, 9), 2) = 9

Ohne Startwert nimmt reduce das erste Element als Anfang; bei einer leeren
Folge bricht es dann mit TypeError ab. Darum gehört ein Startwert dazu,
wann immer die Folge leer sein darf: 0 für XOR (denn x ^ 0 ist x) und eine
neue leere Menge für die Vereinigung. Als Startwert die erste Menge aus
rollen zu nehmen und in sie hinein zu vereinigen (|=), würde die Rolle des
Aufrufers verändern.

Für die Verknüpfung braucht man oft kein eigenes lambda: Das Modul
operator hat die Rechenzeichen als Funktionen, operator.xor(a, b) ist
a ^ b, operator.or_(a, b) ist a | b. Und die Funktion darf selbst
Funktionen als Elemente bekommen: Bei bereinige ist das Zwischenergebnis
der Text und jedes Element ein Schritt, den man darauf anwendet (Funktionen
als Werte, Aufgabe 3_028).
"""

import operator
from functools import reduce


def pruefsumme(daten):
    """Verknüpft alle Bytes von daten mit XOR; 0 für leere Daten."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def alle_rechte(rollen):
    """Gibt die Vereinigung aller Rechte-Mengen in rollen zurück, ohne sie zu verändern."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bereinige(text, schritte):
    """Wendet die Funktionen in schritte der Reihe nach auf text an."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def entferne_spitze_klammern(text):
    """Entfernt < und >, damit kein HTML-Tag durchkommt."""
    return text.replace("<", "").replace(">", "")


print(pruefsumme(b"\x0f\xf0\x01"))
print(sorted(alle_rechte([{"lesen"}, {"lesen", "schreiben"}])))
print(bereinige("  <b>Admin</b> ", [str.strip, entferne_spitze_klammern, str.lower]))
