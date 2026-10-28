"""Aufgabe 3_007 – Durchlaufzeiten                              Stufe 3 ★★★☆☆

Ein Versandhändler will wissen, wie lange eine Bestellung im Lager braucht,
vom Eingang bis zum fertig gepackten Paket. Diese Durchlaufzeit wird für
jede Bestellung in Minuten erfasst. Die Messwerte kommen als Texte aus einem
Export der Lagersoftware, und nicht alle sind brauchbar: Mal fehlt der Wert
(leerer Text), mal steht "n/a" oder ein Tippfehler wie "4S" darin. Ein
einziger kaputter Wert darf die Auswertung nicht abstürzen lassen.

- `als_minuten(text)` wandelt den Text mit float(...) in eine Zahl um und
  gibt sie zurück. Lässt sich der Text nicht umwandeln, gibt die Funktion
  None zurück, statt abzustürzen. Leerzeichen am Anfang und am Ende stören
  float nicht.
- `auswerten(werte)` bekommt eine Liste solcher Texte und gibt ein Tupel
  zurück: den Mittelwert aller brauchbaren Werte und die Zahl der
  unbrauchbaren. Ist kein Wert brauchbar, ist der Mittelwert None. Benutzen
  Sie dafür als_minuten.

    als_minuten("42")      →  42.0
    als_minuten(" 37.5 ")  →  37.5
    als_minuten("n/a")     →  None
    als_minuten("")        →  None
    auswerten(["40", "n/a", "50", "", "45"])  →  (45.0, 2)
    auswerten(["n/a"])                         →  (None, 1)

Grenzen: 0 ≤ len(werte) ≤ 10 000, jeder Text hat höchstens 20 Zeichen.
Brauchbare Texte sind Zahlen von 0 bis 10 000 wie "42" oder " 37.5 ";
unbrauchbar ist jeder Text, den float(...) nicht umwandeln kann. Texte
wie "nan", "inf" oder "1e3" kommen nicht vor.

Hintergrund: float("n/a") lässt sich nicht ausrechnen; Python löst dann
einen ValueError aus, eine Ausnahme. Ohne weitere Vorkehrung bricht das
Programm damit ab. Mit try und except kann man eine Ausnahme abfangen:
Python führt den Block unter try aus. Geht dort etwas schief, springt es
sofort in den Block unter except, statt abzubrechen, und macht danach ganz
normal weiter.

    try:
        zahl = int(eingabe)
        print("Danke!")
    except ValueError:
        print("Das war keine ganze Zahl.")

Hinter except steht die Art der Ausnahme, die man erwartet. Andere Fehler,
etwa ein Tippfehler im Variablennamen (NameError), werden dann nicht
verschluckt, sondern weiterhin gemeldet. Man fängt also nur ab, womit man
rechnet. Statt vorher mühsam zu prüfen, ob ein Text eine Zahl ist (hat er
einen Punkt? ein Minus? Leerzeichen?), probiert man es einfach aus und
behandelt den Fehlschlag (MIT 6.0001, Lecture 7).

Tipp: Ein return im try-Block gibt die Zahl zurück, ein return im
except-Block den Wert None. In auswerten prüfen Sie mit is None, ob ein
Wert unbrauchbar war.
"""


def als_minuten(text):
    """Wandelt text in eine Zahl um; gibt None zurück, wenn das nicht geht."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auswerten(werte):
    """Gibt den Mittelwert der brauchbaren Werte und die Zahl der unbrauchbaren zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


mittelwert, fehlerhaft = auswerten(["40", "n/a", "50", "", "45"])
print("Mittlere Durchlaufzeit:", mittelwert, "Minuten")
print("Unbrauchbare Werte:", fehlerhaft)
