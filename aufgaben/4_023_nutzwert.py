"""Aufgabe 4_023 – Nutzwertanalyse                              Stufe 4 ★★★★☆

Eine Schule will neue Notebooks für ihre Fachräume anschaffen und hat
mehrere Angebote bekommen. Das billigste ist nicht automatisch das beste:
Auch die Jahre Herstellersupport und der Stromverbrauch zählen. Darum
macht die IT-Abteilung eine Nutzwertanalyse. Für jedes Kriterium gibt es
eine Bewertungsfunktion, die einem Angebot 0 bis 10 Punkte gibt, und ein
Gewicht, wie wichtig das Kriterium ist. Der Nutzwert eines Angebots ist
die Summe aus Punkte mal Gewicht über alle Kriterien; das Angebot mit
dem höchsten Nutzwert gewinnt.

Damit man Name und Gewicht direkt über die Bewertungsfunktion schreiben
kann, soll es einen Dekorator mit Argumenten geben. Vervollständigen Sie
`kriterium`:

- `kriterium(name, gewicht)` prüft sofort, dass gewicht zwischen 1 und
  100 liegt (beide eingeschlossen) und dass es in KRITERIEN noch kein
  Kriterium dieses Namens gibt; sonst löst es einen ValueError aus.
  Andernfalls gibt es einen Dekorator zurück.
- Der Dekorator bekommt eine Bewertungsfunktion bewertung(angebot),
  trägt eine Hüllfunktion unter name in das Dictionary KRITERIEN ein und
  gibt diese Hüllfunktion zurück. Sie trägt dank functools.wraps Namen,
  Docstring und `__wrapped__` der Bewertungsfunktion.
- Die Hüllfunktion ruft bewertung(angebot) auf und gibt Punkte mal
  gewicht zurück. Liegen die Punkte nicht zwischen 0 und 10, löst sie
  stattdessen einen ValueError aus, dessen Meldung name und die Punkte
  enthält.

Die Funktion `nutzwert` ist vorgegeben; sie addiert die Ergebnisse aller
Hüllfunktionen in KRITERIEN.

    @kriterium("Preis", gewicht=50)
    def preis(angebot):
        return max(0, 10 - angebot["preis"] // 200)

    angebot_a = {"preis": 850, "support_jahre": 3, "watt": 45}
    preis(angebot_a)                →  300        (6 Punkte mal 50)
    nutzwert(angebot_a)             →  600        (mit den Kriterien unten)
    kriterium("Preis", gewicht=10)  →  ValueError (gibt es schon)
    kriterium("Lärm", gewicht=0)    →  ValueError (Gewicht zu klein)
    preis.__name__                  →  "preis"

Grenzen: name ist ein nicht leerer Text, gewicht eine ganze Zahl von
-1000 bis 1000; erlaubt sind nur 1 bis 100. Eine Bewertungsfunktion
bekommt genau ein Argument und gibt eine ganze Zahl von -100 bis 100
zurück; erlaubt sind nur 0 bis 10. Es gibt bis zu 1000 Kriterien
gleichzeitig.

Hintergrund: Ein Dekorator (Aufgabe 4_022) bekommt genau ein Argument,
die Funktion. Will man ihm weitere Angaben mitgeben, braucht man eine
Ebene mehr: eine Funktion, die die Angaben bekommt und den eigentlichen
Dekorator baut und zurückgibt. Man nennt sie auch Dekorator-Fabrik.

    import functools

    def hoechstens(grenze):
        def dekorator(funktion):
            @functools.wraps(funktion)
            def huelle(*args, **kwargs):
                return min(funktion(*args, **kwargs), grenze)
            return huelle
        return dekorator

    @hoechstens(100)
    def rabatt(betrag):
        return betrag // 10

    rabatt(5000)   # 100 statt 500

Die Zeile @hoechstens(100) wird von links nach rechts gelesen: Zuerst
wird hoechstens(100) aufgerufen, das ergibt dekorator, und erst dieser
wird mit der Funktion aufgerufen. Sie bedeutet also genau

    rabatt = hoechstens(100)(rabatt)

Es gibt damit drei Zeitpunkte: Die Fabrik läuft einmal beim Aufruf
mit den Angaben, der Dekorator einmal beim Dekorieren, beide also schon
beim Definieren der Funktion; die Hülle läuft bei jedem Aufruf. Fehler
in den Angaben (eine unsinnige Grenze) prüft man deshalb am besten in
der Fabrik: Dann scheitert das Programm sofort an der Zeile mit dem @,
nicht erst viel später beim ersten Aufruf. Jeder Aufruf der Fabrik
legt eigene lokale Variablen an; die Hülle sieht sie als Closure
(Aufgabe 4_021). Darum behält jede dekorierte Funktion ihre eigene
Grenze, auch wenn hoechstens viele Male verwendet wird.

Ein Dekorator muss die Funktion übrigens nicht nur umhüllen. Er kann
sie auch irgendwo eintragen, etwa in ein Dictionary, und so eine
Sammlung von Funktionen aufbauen, über die ein anderer Programmteil
später läuft. Webframeworks ordnen auf diese Weise mit
@route("/start") Adressen ihren Funktionen zu.
"""

import functools

KRITERIEN = {}


def kriterium(name, gewicht):
    """Dekorator-Fabrik: gewichtet eine Bewertungsfunktion und trägt sie unter name in KRITERIEN ein."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def nutzwert(angebot):
    """Gibt die Summe der gewichteten Punkte aller Kriterien für angebot zurück."""
    summe = 0
    for gewichtet in KRITERIEN.values():
        summe = summe + gewichtet(angebot)
    return summe


@kriterium("Preis", gewicht=50)
def preis(angebot):
    """10 Punkte für ein sehr günstiges Angebot, je 200 Euro mehr einen weniger."""
    return max(0, 10 - angebot["preis"] // 200)


@kriterium("Support", gewicht=30)
def support(angebot):
    """2 Punkte je Jahr Herstellersupport, höchstens 10."""
    return min(10, 2 * angebot["support_jahre"])


@kriterium("Energie", gewicht=20)
def energie(angebot):
    """10 Punkte für ein sparsames Gerät, je 10 Watt einen weniger."""
    return max(0, 10 - angebot["watt"] // 10)


angebot_a = {"preis": 850, "support_jahre": 3, "watt": 45}
angebot_b = {"preis": 1200, "support_jahre": 5, "watt": 30}
print(preis(angebot_a), nutzwert(angebot_a), nutzwert(angebot_b))
print(sorted(KRITERIEN))
