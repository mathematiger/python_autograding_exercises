# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_041_maskenzeiten.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_041_maskenzeiten

"""Aufgabe 2_041 – Maskenzeiten                                  Stufe 2 ★★☆☆☆

Eine neue Bestell-App wird in einem Usability-Test ausprobiert:
Testpersonen erledigen eine Bestellung, und die App protokolliert, wie
viele Sekunden sie auf jeder Bildschirmmaske verbracht haben. Weil man
zwischen den Masken hin- und zurückspringen kann, kommt dieselbe Maske
oft mehrmals im Protokoll vor:

    protokoll = [
        {"maske": "Anmeldung", "sekunden": 14},
        {"maske": "Warenkorb", "sekunden": 31},
        {"maske": "Zahlung", "sekunden": 52},
        {"maske": "Warenkorb", "sekunden": 9},
        {"maske": "Zahlung", "sekunden": 40},
    ]

Das Entwicklungsteam will wissen, auf welcher Maske insgesamt die
meiste Zeit vergeht, denn dort hakt die Bedienung vermutlich.
Vervollständigen Sie die Funktion `zeit_je_maske(protokoll)`, die ein
neues Dictionary zurückgibt: Schlüssel ist der Name jeder Maske, die im
Protokoll vorkommt, Wert die Summe ihrer Sekunden. Das Protokoll selbst
bleibt unverändert.

    zeit_je_maske(protokoll)
        →  {"Anmeldung": 14, "Warenkorb": 40, "Zahlung": 92}
    zeit_je_maske([])  →  {}

Grenzen: 0 ≤ len(protokoll) ≤ 100 000. Jede Zeile hat genau die
Schlüssel "maske" und "sekunden". maske ist ein nicht leerer Text,
Groß- und Kleinschreibung zählt ("Zahlung" und "zahlung" sind
verschiedene Masken). sekunden ist eine ganze Zahl von 0 bis 3600; eine
Maske mit 0 Sekunden kommt trotzdem ins Ergebnis.

Hintergrund: Gruppieren heißt, Zeilen nach dem Wert einer Spalte (hier
maske) zusammenzufassen und für jede Gruppe etwas auszurechnen (hier
die Summe der Sekunden). Ohne Bibliothek nimmt man dafür ein Dictionary
als Sammelbehälter, so wie beim Zählen von Wörtern (Aufgabe 2_025):
Der Gruppenname ist der Schlüssel, der Wert ist die laufende Summe. Man
geht die Tabelle (Aufgabe 2_032) einmal durch; kommt ein Name zum
ersten Mal, legt man ihn mit 0 an, danach addiert man immer den Wert
der Zeile:

    summen = {}
    for zeile in tabelle:
        name = zeile["gruppe"]
        if name not in summen:
            summen[name] = 0
        summen[name] = summen[name] + zeile["wert"]

Kürzer geht es mit get und einem Standardwert (Aufgabe 2_026):
summen[name] = summen.get(name, 0) + zeile["wert"]. So braucht man nur
einen Durchlauf, egal wie viele Gruppen es gibt. Genau das macht später
groupby in pandas (Stufe 4).
"""


def zeit_je_maske(protokoll):
    """Gibt ein Dictionary Maske → Summe der Sekunden zurück."""
    summen = {}
    for zeile in protokoll:
        maske = zeile["maske"]
        summen[maske] = summen.get(maske, 0) + zeile["sekunden"]
    return summen


protokoll = [
    {"maske": "Anmeldung", "sekunden": 14},
    {"maske": "Warenkorb", "sekunden": 31},
    {"maske": "Zahlung", "sekunden": 52},
    {"maske": "Warenkorb", "sekunden": 9},
    {"maske": "Zahlung", "sekunden": 40},
]
print(zeit_je_maske(protokoll))


# Idee: Ein leeres Dictionary summen anlegen und das Protokoll einmal durchgehen. Für jede Zeile den
# Namen der Maske holen und ihre Sekunden zur bisherigen Summe addieren; summen.get(maske, 0) liefert 0,
# wenn die Maske zum ersten Mal kommt. Am Ende summen zurückgeben.
#
# Anderer Weg: mit if maske not in summen: summen[maske] = 0 und danach summen[maske] += zeile["sekunden"].
# Oder erst alle Namen sammeln und für jeden Namen das ganze Protokoll erneut durchgehen; das ist richtig,
# braucht aber bei vielen Masken viel länger (Anzahl Masken mal Anzahl Zeilen Schritte statt einmal durch).
#
# Typische Fehler: summen[maske] = zeile["sekunden"] statt zu addieren (dann zählt nur die letzte Zeile),
# summen[maske] += … ohne vorher anzulegen (KeyError beim ersten Mal), das Dictionary außerhalb der
# Funktion anlegen (dann wachsen die Summen bei jedem Aufruf weiter) oder Masken mit 0 Sekunden weglassen.
