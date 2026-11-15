"""Aufgabe 3_032 – Passwortregeln                                Stufe 3 ★★★☆☆

Eine Firma prüft neue Passwörter, bevor ein Konto angelegt wird. Welche Regeln
gelten, ist aber nicht überall gleich: Für normale Konten genügen 10 Zeichen
mit einer Ziffer, für Administratorkonten sind 16 Zeichen mit Ziffer und
Sonderzeichen Pflicht, und nächstes Jahr ändert sich die Richtlinie vielleicht
wieder. Statt für jede Richtlinie eine neue Prüffunktion von Hand zu schreiben,
sollen Funktionen die Prüffunktionen bauen. Eine Prüffunktion (eine Regel)
bekommt ein Passwort und liefert True, wenn es die Regel erfüllt. Schreiben Sie:

- `mindestlaenge(n)` gibt eine Regel zurück, die True liefert, wenn das
  Passwort mindestens n Zeichen hat.
- `enthaelt_eines(zeichen)` gibt eine Regel zurück, die True liefert, wenn
  mindestens ein Zeichen des Textes zeichen im Passwort vorkommt.
- `alle(regeln)` gibt eine Regel zurück, die True liefert, wenn das Passwort
  jede Regel aus der Liste regeln erfüllt (bei leerer Liste immer True).

    lang_genug = mindestlaenge(10)
    lang_genug("sommer2025")                →  True
    lang_genug("kurz1")                     →  False
    hat_ziffer = enthaelt_eines("0123456789")
    hat_ziffer("ohneziffer")                →  False
    normal = alle([lang_genug, hat_ziffer])
    normal("sommer2025")                    →  True
    normal("sommersonne")                   →  False

Grenzen: 0 ≤ n ≤ 100. zeichen ist ein Text mit 0 bis 50 Zeichen (bei leerem
Text erfüllt kein Passwort die Regel). regeln ist eine Liste mit 0 bis 20
Regeln. Ein Passwort ist ein Text mit 0 bis 100 Zeichen. Jede gebaute Regel
wird oft aufgerufen, auch mit vielen verschiedenen Passwörtern; sie darf sich
zwischen den Aufrufen nicht verändern, und eine Regel darf die anderen nicht
beeinflussen. Die Liste regeln wird nach dem Aufruf von alle nicht mehr
verändert.

Hintergrund: Eine Funktion ist ein Wert (Aufgabe 3_028). Darum kann eine
Funktion nicht nur Funktionen als Argument bekommen, sondern auch eine
Funktion zurückgeben. Man definiert sie mit def innerhalb der äußeren Funktion
und gibt sie ohne Klammern zurück:

    def multipliziere_mit(faktor):
        def rechne(zahl):
            return zahl * faktor
        return rechne

    verdoppeln = multipliziere_mit(2)
    verdreifachen = multipliziere_mit(3)
    verdoppeln(5)      →  10
    verdreifachen(5)   →  15

Die innere Funktion rechne darf die Parameter der äußeren lesen. Bemerkenswert
ist, dass sie sich faktor merkt, auch nachdem multipliziere_mit längst fertig
ist: verdoppeln und verdreifachen sind zwei verschiedene Funktionen, jede mit
ihrem eigenen faktor. Statt def geht auch return lambda zahl: zahl * faktor
(Aufgabe 3_025). Wie genau Python sich die Werte merkt, kommt in Stufe 4
(Closures); hier genügt es, die Parameter der äußeren Funktion zu lesen.
"""


def mindestlaenge(n):
    """Gibt eine Regel zurück, die Passwörter mit mindestens n Zeichen annimmt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def enthaelt_eines(zeichen):
    """Gibt eine Regel zurück, die Passwörter mit mindestens einem der Zeichen annimmt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def alle(regeln):
    """Gibt eine Regel zurück, die Passwörter annimmt, die jede der regeln erfüllen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


lang_genug = mindestlaenge(10)
hat_ziffer = enthaelt_eines("0123456789")
normal = alle([lang_genug, hat_ziffer])
print(lang_genug("sommer2025"), hat_ziffer("ohneziffer"), normal("sommersonne"))
