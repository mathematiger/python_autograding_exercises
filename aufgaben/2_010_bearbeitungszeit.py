"""Aufgabe 2_010 – Usability-Test                               Stufe 2 ★★☆☆☆

Ein Team hat eine neue Eingabemaske für Urlaubsanträge gebaut. In einem
Usability-Test probieren mehrere Personen die Maske aus, während das Team
zuschaut; gemessen wird, wie viele Sekunden jede Person braucht, bis der
Antrag abgeschickt ist. Für den Bericht interessiert vor allem die kürzeste
und die längste Zeit: Liegen sie weit auseinander, finden manche Personen
den richtigen Weg durch die Maske nicht.

Vervollständigen Sie die Funktion `kuerzeste_und_laengste(zeiten)`. Sie
bekommt eine Liste mit mindestens einer Zeit und gibt beide Werte zusammen
als Tupel zurück, die kürzeste zuerst:

    kuerzeste_und_laengste([42, 95, 61, 38])   →  (38, 95)
    kuerzeste_und_laengste([50])               →  (50, 50)

Das Programm darunter ist schon fertig. Es packt das Tupel in zwei Variablen
aus und gibt aus:

    Kürzeste Zeit: 38 s
    Längste Zeit: 95 s

Grenzen: zeiten ist eine Liste mit 1 ≤ len(zeiten) ≤ 1000. Jede Zeit ist eine
ganze Zahl oder eine Kommazahl mit 0 < zeit ≤ 3600. Dieselbe Zeit kann mehrfach
vorkommen.

Hintergrund: Mit return gibt eine Funktion genau einen Wert zurück. Dieser
eine Wert darf aber ein Tupel sein, also mehrere Werte, die mit Kommas in
runden Klammern zusammengefasst sind: return (a, b), die Klammern darf man
auch weglassen. Beim Aufruf kann man das Tupel gleich wieder auspacken,
indem links vom = so viele Variablen stehen, wie das Tupel Werte hat:

    def teile(zahl, teiler):
        return zahl // teiler, zahl % teiler

    ganze, rest = teile(17, 5)    # ganze ist 3, rest ist 2

Tipp: min(liste) und max(liste) liefern den kleinsten und den größten Wert
einer Liste.
"""


def kuerzeste_und_laengste(zeiten):
    """Gibt die kürzeste und die längste Zeit als Tupel zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


kurz, lang = kuerzeste_und_laengste([42, 95, 61, 38])
print("Kürzeste Zeit:", kurz, "s")
print("Längste Zeit:", lang, "s")
