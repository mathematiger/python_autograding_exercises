"""Aufgabe 4_063 – Abfragestau                                   Stufe 4 ★★★★☆

Ein Datenbankserver bearbeitet nur eine begrenzte Zahl von Abfragen
gleichzeitig; die übrigen warten in einer Warteschlange. Jede Minute
schreibt er ins Protokoll, wie viele Abfragen gerade warten. Die
Datenbankadministratorin will sehen, wie schnell sich ein Stau
verschärft: Zu jeder Minute soll dastehen, wie viele Minuten es dauert,
bis zum ersten Mal noch mehr Abfragen warten als in dieser Minute.
Kommt das im Protokoll nicht mehr vor, steht dort 0.

Schreiben Sie die Funktion `bis_mehr(wartend)`, die zu der Liste der
Minutenwerte eine gleich lange Liste dieser Abstände zurückgibt:

    bis_mehr([3, 5, 4, 4, 8, 2, 6])   →  [1, 3, 2, 1, 0, 1, 0]

Nach Minute 0 (3 wartende) warten schon in Minute 1 mehr (5), Abstand 1.
Nach Minute 1 (5) kommen 4 und 4, erst Minute 4 hat mehr (8), Abstand 3.
Gleich viele zählen nicht als mehr. Nach den 8 in Minute 4 kommt nichts
Höheres mehr, also 0. Die Liste wartend bleibt unverändert.

Grenzen: wartend hat 0 bis 100 000 Einträge, jeder eine ganze Zahl von 0
bis 1 000 000. Ihre Lösung soll O(n) Schritte brauchen; der naive Weg,
von jeder Minute aus nach rechts zu suchen, braucht bei einem lange
abnehmenden Protokoll O(n²) und ist zu langsam.

Hintergrund: Ein Stapel (englisch stack) ist eine Folge, bei der man nur
oben etwas drauflegt und nur oben etwas wegnimmt: Was zuletzt kam, geht
zuerst. In Python nimmt man dafür eine Liste; append legt oben drauf,
pop() nimmt das oberste weg, stapel[-1] schaut es an, ohne es
wegzunehmen. Beides kostet einen Schritt, egal wie voll der Stapel ist.

Der Trick für diese Aufgabe heißt monotoner Stapel. Man geht die
Minuten einmal von links nach rechts durch und legt auf den Stapel die
Stellen der Minuten, für die man noch keine höhere gefunden hat. Von
unten nach oben gelesen gehören zu ihnen nie steigende Werte, denn
sobald eine höhere Minute kommt, ist sie für alle niedrigeren oben auf
dem Stapel die Antwort, und diese verlassen ihn:

    for stelle, wert in enumerate(werte):
        while stapel and werte[stapel[-1]] < wert:
            frueher = stapel.pop()
            # für frueher ist stelle die erste höhere Stelle
        stapel.append(stelle)

Bei [3, 5, 4, 4, 8] liegt nach den ersten vier Werten [1, 2, 3] auf dem
Stapel (die Stellen der Werte 5, 4, 4), die 3 hat die 5 schon
verdrängt. Die 8 nimmt dann die 3, die 2 und die 1 herunter, jede
bekommt ihre Antwort. Was am Ende noch auf dem Stapel liegt, hat keine
höhere Minute mehr. Die while-Schleife sieht teuer aus, aber jede Stelle
kommt genau einmal auf den Stapel und höchstens einmal herunter;
zusammen sind das höchstens 2n Schritte, also O(n). Dieselbe Idee
findet zu jedem Wert den nächsten kleineren (Vergleich umdrehen) oder
den vorigen höheren (von rechts nach links laufen).
"""


def bis_mehr(wartend):
    """Gibt zu jeder Minute den Abstand bis zur ersten Minute mit mehr Wartenden zurück, sonst 0."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(bis_mehr([3, 5, 4, 4, 8, 2, 6]))
