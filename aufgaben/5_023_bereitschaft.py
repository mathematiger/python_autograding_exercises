"""Aufgabe 5_023 – Bereitschaft                                  Stufe 5 ★★★★★

Ein IT-Servicedesk arbeitet mit Eskalationsstufen: Was die erste Stufe
(der Servicedesk selbst) nicht lösen kann, geht an die zweite
(Fachleute für ein System), dann an die dritte (Hersteller). Nachts
gibt es für jede Stufe einen Bereitschaftsplan mit eingetragenen
Personen, von denen aber nicht alle erreichbar sind. Das
Ticketsystem soll eigene Objekte so verwenden können, wie Python es
mit Listen tut: len(schlange) für die Anzahl und if schlange: für die
Frage „ist da etwas?“. Vervollständigen Sie:

- `Warteschlange` mit den offenen Ticketnummern: `hinzufuegen(nummer)`
  nimmt ein Ticket auf (ValueError, wenn es schon offen ist),
  `erledigen(nummer)` entfernt es (ValueError, wenn es nicht offen
  ist), und `len(schlange)` ist die Anzahl der offenen Tickets. Eine
  leere Warteschlange gilt als falsch, eine mit Tickets als wahr.
  Schreiben Sie dafür nur `__len__`, kein `__bool__`.
- `Bereitschaft` mit den eingetragenen Personen einer Stufe:
  `eintragen(name)` trägt eine Person ein, erreichbar (ValueError,
  wenn sie schon eingetragen ist), `abmelden(name)` und
  `zurueckmelden(name)` setzen sie auf nicht erreichbar bzw. wieder
  erreichbar (ValueError, wenn sie nicht eingetragen ist). len(plan)
  ist die Zahl aller eingetragenen Personen, aber der Plan gilt nur
  dann als wahr, wenn mindestens eine davon erreichbar ist.
- `zustaendige_stufe(stufen)` bekommt eine Liste von
  Bereitschaft-Objekten, Stufe 1 zuerst, und gibt die Nummer der
  ersten Stufe zurück, die als wahr gilt, ab 1 gezählt; gilt keine als
  wahr, None.
- `lagebericht(schlange)` gibt "keine Warteschlange" zurück, wenn
  schlange None ist, "keine offenen Tickets" bei einer leeren
  Warteschlange und sonst zum Beispiel "3 offene Tickets".

    schlange = Warteschlange()
    bool(schlange)              →  False
    schlange.hinzufuegen(4711)
    schlange.hinzufuegen(4712)
    len(schlange), bool(schlange)   →  (2, True)
    stufe1 = Bereitschaft()
    stufe1.eintragen("Ada")
    stufe1.abmelden("Ada")
    len(stufe1), bool(stufe1)   →  (1, False)
    stufe2 = Bereitschaft()
    stufe2.eintragen("Cem")
    zustaendige_stufe([stufe1, stufe2])   →  2
    lagebericht(Warteschlange())          →  "keine offenen Tickets"

Grenzen: Ticketnummern sind ganze Zahlen von 1 bis 10**9, Namen nicht
leere Texte. Es gibt bis zu 100 000 Tickets bzw. Personen und
0 bis 100 Stufen. len und bool sollen O(1) Schritte brauchen, also
nicht bei jedem Aufruf alle Tickets oder Personen durchzählen;
hinzufuegen, erledigen, eintragen, abmelden und zurueckmelden ebenso.

Hintergrund: Wann gilt ein Objekt als wahr? Python fragt das bei if,
while, and, or, not und bool(objekt) und geht dabei in einer festen
Reihenfolge vor:

1. Hat die Klasse `__bool__`, entscheidet dessen Ergebnis. Es muss
   True oder False sein, sonst gibt es einen TypeError.
2. Sonst, wenn die Klasse `__len__` hat: Das Objekt ist falsch, wenn
   die Länge 0 ist, und sonst wahr. `__len__` muss eine ganze Zahl
   von 0 an liefern; len(objekt) ruft es auf.
3. Hat die Klasse keine der beiden Methoden, ist jedes Objekt wahr.

Deshalb sind eine leere Liste, ein leeres Dictionary und "" falsch:
Sie haben nur `__len__`. Eine eigene Sammlung braucht also meist kein
`__bool__`. Man schreibt es nur, wenn „wahr“ etwas anderes bedeuten
soll als „nicht leer“, wie beim Bereitschaftsplan, der Personen
enthält, aber nichts nützt, wenn keine erreichbar ist:

    class Lager:
        def __init__(self):
            self.teile = {}            # Teil → Menge, auch 0
        def __len__(self):
            return len(self.teile)     # wie viele Teile geführt werden
        def __bool__(self):
            return any(self.teile.values())   # ist irgendetwas vorrätig?

Hier rechnet `__bool__` bei jedem Aufruf alles neu; schneller ist es,
die Zahl der vorrätigen Teile in einem Attribut mitzuführen und bei
jeder Änderung anzupassen.

Eine Falle: `if schlange:` ist auch dann falsch, wenn die Warteschlange
leer ist. Will man nur wissen, ob überhaupt eine da ist, also ob die
Variable nicht None ist, schreibt man `if schlange is not None:`. Wer
beides verwechselt, behandelt eine leere Sammlung, als gäbe es sie
nicht.
"""


class Warteschlange:
    """Die offenen Tickets; als wahr gilt sie, wenn sie nicht leer ist."""

    def __init__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def hinzufuegen(self, nummer):
        """Nimmt das Ticket nummer auf."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def erledigen(self, nummer):
        """Entfernt das Ticket nummer."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class Bereitschaft:
    """Ein Bereitschaftsplan; als wahr gilt er, wenn jemand erreichbar ist."""

    def __init__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def eintragen(self, name):
        """Trägt name als erreichbar ein."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def abmelden(self, name):
        """Setzt name auf nicht erreichbar."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def zurueckmelden(self, name):
        """Setzt name wieder auf erreichbar."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __len__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    def __bool__(self):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zustaendige_stufe(stufen):
    """Gibt die Nummer der ersten Stufe zurück, die als wahr gilt, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lagebericht(schlange):
    """Beschreibt die Warteschlange in einem kurzen Satz."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


schlange = Warteschlange()
schlange.hinzufuegen(4711)
schlange.hinzufuegen(4712)
print(lagebericht(schlange))
stufe1 = Bereitschaft()
stufe1.eintragen("Ada")
stufe1.abmelden("Ada")
stufe2 = Bereitschaft()
stufe2.eintragen("Cem")
print(len(stufe1), bool(stufe1), zustaendige_stufe([stufe1, stufe2]))
