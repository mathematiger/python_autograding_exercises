# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_056_regelklammern.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_056_regelklammern

"""Aufgabe 3_056 – Regelklammern                                 Stufe 3 ★★★☆☆

Ein Onlineshop markiert verdächtige Bestellungen mit einem
Entscheidungsbaum: einem Modell, das Frage für Frage weitergeht
(„Ist der Betrag über 500 Euro? Wenn ja: Ist die Lieferadresse neu?“).
Das Analysewerkzeug exportiert den Baum als eine lange Regel, in der
Klammern zeigen, was zusammengehört. Es verwendet drei Arten von
Klammern, (), [] und {}:

    (betrag > 500 und [neue_adresse oder {land != "DE" und express}])

Seit einem Update schneidet der Export manche Regeln falsch ab. Bevor
eine Regel in das Prüfsystem geladen wird, sollen die Klammern geprüft
werden. Richtig sind sie, wenn jede schließende Klammer zur zuletzt
geöffneten, noch offenen Klammer derselben Art passt und am Ende keine
Klammer mehr offen ist. Alle anderen Zeichen spielen keine Rolle.
Schreiben Sie zwei Funktionen:

- `ausgewogen(regel)` gibt True zurück, wenn die Klammern richtig sind,
  sonst False.
- `fehlerstelle(regel)` gibt -1 zurück, wenn die Klammern richtig sind.
  Sonst die Position (den Index) der ersten schließenden Klammer, die
  nicht passt, weil keine Klammer offen ist oder die zuletzt geöffnete
  eine andere Art hat. Gibt es keine solche, aber am Ende ist noch eine
  Klammer offen, die Position der zuletzt geöffneten offenen Klammer.

    ausgewogen("(a [b] {c})")     →  True
    ausgewogen("([)]")            →  False
    fehlerstelle("(a [b) c]")     →  5      (")" passt nicht zu "[")
    fehlerstelle("a) (b")         →  1      (keine Klammer offen)
    fehlerstelle("(a [b] {c")     →  7      ("{" ist noch offen)
    fehlerstelle("{x}")           →  -1

Das Wörterbuch PASSEND ist vorgegeben: Es ordnet jeder schließenden
Klammer die öffnende derselben Art zu.

Grenzen: regel ist ein Text mit 0 bis 100 000 Zeichen; er kann beliebige
Zeichen enthalten, Klammern können beliebig tief verschachtelt sein.

Hintergrund: Ein Stapel (englisch Stack) ist eine Liste, an der man nur
an einem Ende arbeitet: Mit append legt man oben etwas drauf, mit pop()
nimmt man das oberste wieder herunter (Aufgabe 3_035), und stapel[-1] zeigt
es an (negative Indizes: Aufgabe 1_012), ohne es wegzunehmen. Was zuletzt
hineinkam, kommt zuerst wieder heraus („last in, first out“). Genau das
brauchen Klammern: Die schließende Klammer gehört immer zur zuletzt
geöffneten, die noch offen ist.

    stapel = []
    stapel.append("(")          # stapel ist ["("]
    stapel.append("[")          # stapel ist ["(", "["]
    stapel[-1]                  →  "["
    stapel.pop()                →  "["     stapel ist wieder ["("]

Man geht die Regel Zeichen für Zeichen durch: Eine öffnende Klammer
kommt auf den Stapel, bei einer schließenden muss oben die passende
liegen, dann nimmt man sie herunter. Ist der Stapel leer oder liegt oben
die falsche, ist die Regel kaputt. Ein bloßes Zählen der Klammern reicht
nicht: "([)]" hat gleich viele öffnende wie schließende, ist aber
falsch. Für fehlerstelle legt man statt der Klammer ihre Position auf den
Stapel, dann weiß man am Ende, wo die offene Klammer steht. Ein pop() auf
einen leeren Stapel löst einen IndexError aus; prüfen Sie vorher, ob
etwas daraufliegt.

Tipp: zeichen in PASSEND prüft, ob zeichen eine schließende Klammer ist,
zeichen in "([{" ob es eine öffnende ist.
"""

PASSEND = {")": "(", "]": "[", "}": "{"}


def ausgewogen(regel):
    """Gibt True zurück, wenn alle Klammern in regel richtig geschlossen sind."""
    stapel = []
    for zeichen in regel:
        if zeichen in "([{":
            stapel.append(zeichen)
        elif zeichen in PASSEND:
            if not stapel or stapel[-1] != PASSEND[zeichen]:
                return False
            stapel.pop()
    return not stapel


def fehlerstelle(regel):
    """Gibt die Position des ersten Klammerfehlers zurück oder -1, wenn alles passt."""
    offen = []
    for position, zeichen in enumerate(regel):
        if zeichen in "([{":
            offen.append(position)
        elif zeichen in PASSEND:
            if not offen or regel[offen[-1]] != PASSEND[zeichen]:
                return position
            offen.pop()
    if offen:
        return offen[-1]
    return -1


regel = '(betrag > 500 und [neue_adresse oder {land != "DE" und express}])'
print(ausgewogen(regel))
print(fehlerstelle("(a [b) c]"))


# Idee: Ein Stapel merkt sich die offenen Klammern. Eine öffnende kommt mit append obenauf; bei einer
# schließenden muss oben die passende öffnende liegen (PASSEND[zeichen]), dann wird sie mit pop()
# entfernt, sonst ist die Regel falsch. Am Ende muss der Stapel leer sein. fehlerstelle legt statt der
# Klammer ihre Position ab (regel[position] liefert die Klammer zurück), gibt beim ersten Fehler die
# Position der schließenden Klammer zurück und am Ende die oberste noch offene Position.
# Anderer Weg: ausgewogen(regel) als fehlerstelle(regel) == -1 schreiben. Der naive Weg entfernt erst alle
# Zeichen außer Klammern und streicht dann immer wieder "()", "[]" und "{}" mit replace, bis sich nichts
# mehr ändert; das geht bei tiefer Verschachtelung
# bis zu n/2-mal durch den ganzen Text, also O(n²).
# Typische Fehler: nur zählen (dann ist "([)]" richtig), pop() auf einen leeren Stapel (IndexError bei
# ")("), am Ende den Stapel nicht prüfen, bei fehlerstelle die erste statt der zuletzt geöffneten offenen
# Klammer zurückgeben.
# Laufzeit: O(n), jedes Zeichen wird einmal angesehen, append, pop und stapel[-1] kosten O(1).
