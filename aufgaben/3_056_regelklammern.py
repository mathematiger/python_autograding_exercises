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
nimmt man das oberste wieder herunter, und stapel[-1] zeigt es an, ohne
es wegzunehmen. Was zuletzt hineinkam, kommt zuerst wieder heraus
(„last in, first out“). Genau das brauchen Klammern: Die schließende
Klammer gehört immer zur zuletzt geöffneten, die noch offen ist.

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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fehlerstelle(regel):
    """Gibt die Position des ersten Klammerfehlers zurück oder -1, wenn alles passt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


regel = '(betrag > 500 und [neue_adresse oder {land != "DE" und express}])'
print(ausgewogen(regel))
print(fehlerstelle("(a [b) c]"))
