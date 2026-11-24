"""Aufgabe 4_079 – Symbolleisten                                 Stufe 4 ★★★★☆

Ein Programm zur Rechnungserfassung hat oben mehrere Symbolleisten, das
sind Reihen von Knöpfen wie „Neu“ oder „Speichern“. Jede Person darf ihre
Symbolleisten selbst anpassen: Knöpfe hinzufügen, entfernen, umsortieren
und ganze Leisten ausblenden. Die Einstellungen sind ein verschachteltes
Dictionary, die Ansicht:

    SYMBOLE = {"Neu": "neu.png", "Speichern": "disk.png", ...}
    standard = {
        "name": "Standard",
        "symbolleisten": [
            {"titel": "Datei", "knoepfe": ["Neu", "Speichern"], "sichtbar": True},
            {"titel": "Bearbeiten", "knoepfe": ["Kopieren", "Einfügen"], "sichtbar": True},
        ],
        "symbole": SYMBOLE,
    }

"symbole" ist der Symbolsatz, ein großes Dictionary, das zu jedem Knopf
die Bilddatei nennt. Er gehört nicht der einzelnen Person: Alle Ansichten
benutzen denselben Symbolsatz, und wenn die IT ein Bild austauscht
(SYMBOLE["Neu"] = "neu_2.png"), sollen es sofort alle sehen. Schreiben
Sie zwei Funktionen:

- `eigene_ansicht(standard)` gibt eine neue Ansicht für eine Person
  zurück, die sie anpassen kann. Was sie an ihren Symbolleisten ändert,
  egal wie tief (eine Leiste anhängen, einen Titel ändern, einen Knopf in
  eine Liste knoepfe einfügen), darf die Standardansicht und andere
  Ansichten nicht verändern. Der Symbolsatz dagegen ist in der neuen
  Ansicht dasselbe Objekt wie in standard.
- `mit_symbolsatz(ansicht, symbole)` gibt für die Vorschau eines anderen
  Symbolsatzes (etwa mit kontrastreichen Bildern für Menschen mit
  Sehschwäche) eine neue Ansicht zurück, in der "symbole" das Dictionary
  symbole ist. Die Vorschau wird nur angezeigt, nie bearbeitet. Damit das
  Durchblättern vieler Symbolsätze nichts kostet, teilt sie alles andere
  mit ansicht, auch die Liste "symbolleisten" (dasselbe Objekt). ansicht
  selbst bleibt unverändert.

Beide Funktionen übernehmen alle Schlüssel der Ansicht, auch weitere wie
"sprache", und verändern ihr Argument nicht.

    meine = eigene_ansicht(standard)
    meine["symbolleisten"][0]["knoepfe"].append("Drucken")
    standard["symbolleisten"][0]["knoepfe"]   →  ["Neu", "Speichern"]
    meine["symbole"] is standard["symbole"]   →  True
    vorschau = mit_symbolsatz(meine, {"Neu": "neu_kontrast.png"})
    vorschau["symbolleisten"] is meine["symbolleisten"]  →  True
    meine["symbole"] is SYMBOLE                          →  True

Grenzen: Eine Ansicht hat die Schlüssel "name", "symbolleisten" und
"symbole" und darf weitere Schlüssel haben, deren Werte Texte oder Zahlen
sind. 0 ≤ len(symbolleisten) ≤ 200; jede Leiste ist ein Dictionary mit
genau den Schlüsseln "titel" (Text), "knoepfe" (Liste mit 0 bis 100
Texten) und "sichtbar" (True oder False). Ein Symbolsatz ist ein
Dictionary von Texten auf Texte mit höchstens 10 000 Einträgen.

Hintergrund: Eine Zuweisung kopiert nichts, sie gibt demselben Objekt
nur einen zweiten Namen (Aufgabe 2_018). Bei verschachtelten Daten reicht
aber auch liste[:] nicht, denn eine Kopie kann flach oder tief sein. Das
Modul copy kann beides:

    import copy

    leisten = [{"titel": "Datei", "knoepfe": ["Neu"]}]
    flach = copy.copy(leisten)       # neue äußere Liste, dieselben Dictionaries
    tief = copy.deepcopy(leisten)    # alles neu, bis in die innerste Liste

    flach is leisten                 →  False
    flach[0] is leisten[0]           →  True
    flach.append({"titel": "Hilfe", "knoepfe": []})   # leisten bleibt bei 1 Leiste
    flach[0]["knoepfe"].append("Öffnen")              # ändert auch leisten!
    tief[0]["knoepfe"] is leisten[0]["knoepfe"]       →  False

Eine flache Kopie (copy.copy(x), liste[:], dict(d), d.copy()) legt nur
den äußersten Behälter neu an; darin stehen dieselben Objekte wie im
Original. Ersetzen in der Kopie ist sicher (kopie["symbole"] = neu
verändert das Original nicht), Ändern eines inneren Objekts (kopie[0]
["knoepfe"].append(...)) nicht. Eine tiefe Kopie geht rekursiv durch und
kopiert jeden veränderlichen Behälter. Unveränderliche Objekte wie Texte,
Zahlen und True muss niemand kopieren (Aufgabe 2_019): Niemand kann sie
verändern, also schadet Teilen nicht, und deepcopy gibt sie unverändert
zurück. Auch ein Tupel, das nur solche Werte enthält, behält es bei.

Wann welches? Tief kopieren Sie, wenn die Kopie unabhängig bearbeitet
werden soll, bis in alle Ebenen. Flach kopieren (oder gar nicht) Sie,
wenn die inneren Objekte nicht verändert werden oder geteilt werden
sollen: Dann spart das Zeit und Speicher, und eine zentrale Änderung
kommt bei allen an. Oft braucht ein Objekt beides, ein Teil wird tief
kopiert, ein anderer geteilt. Dann beginnen Sie mit einer flachen Kopie
des äußeren Dictionarys und ersetzen darin nur den Teil, der unabhängig
sein muss, durch seine tiefe Kopie. Ob zwei Namen dasselbe Objekt meinen,
prüft `is`; `==` vergleicht nur den Inhalt.
"""

import copy


def eigene_ansicht(standard):
    """Gibt eine anpassbare Kopie der Ansicht zurück: Symbolleisten unabhängig, Symbolsatz geteilt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_symbolsatz(ansicht, symbole):
    """Gibt eine Vorschau der Ansicht mit einem anderen Symbolsatz zurück, alles andere geteilt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


SYMBOLE = {"Neu": "neu.png", "Speichern": "disk.png", "Kopieren": "kopie.png", "Einfügen": "einfuegen.png"}
standard = {
    "name": "Standard",
    "symbolleisten": [
        {"titel": "Datei", "knoepfe": ["Neu", "Speichern"], "sichtbar": True},
        {"titel": "Bearbeiten", "knoepfe": ["Kopieren", "Einfügen"], "sichtbar": True},
    ],
    "symbole": SYMBOLE,
}
meine = eigene_ansicht(standard)
meine["symbolleisten"][0]["knoepfe"].append("Drucken")
print(standard["symbolleisten"][0]["knoepfe"])
print(meine["symbole"] is standard["symbole"])
