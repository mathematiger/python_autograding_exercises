"""Aufgabe 1_009 – Umgedrehte Uhr                                Stufe 1 ★☆☆☆☆

Im Eingangsbereich der Firma hängt ein Bildschirm, der eine analoge Uhr
anzeigt; ihr Zifferblatt hat nur Striche und keine Zahlen. Beim Montieren wurde er auf den Kopf gedreht, also um
180°. Wer vorbeigeht und die Uhr ganz normal abliest, liest eine falsche Zeit
ab. Das Programm fragt schon nach der richtigen Uhrzeit, zum Beispiel 14:20.
Berechnen Sie, welche Uhrzeit man auf der gedrehten Uhr abliest, und speichern
Sie Stunde und Minute in den Variablen stunde_180 und minute_180; die Zeile
mit print steht schon im Programm. Bei Eingabe 14:20 soll das Programm
ausgeben:

    Um 180° gedreht: 8 Uhr und 50 Minuten

So liest man ab: Man denkt sich die 12 wie gewohnt oben. Der Minutenzeiger
zeigt die Minuten. Der Stundenzeiger steht meist zwischen zwei Stundenstrichen;
es zählt die Stunde, an der er zuletzt vorbeigekommen ist. Es gibt nur die
Stunden 1 bis 12, also keine 0 Uhr und keine 14 Uhr.

Zusatz (wird ebenfalls geprüft): Geben Sie in zwei weiteren Zeilen aus, was man abliest, wenn der
Bildschirm um 90° und um 270° im Uhrzeigersinn gedreht ist. Bei Eingabe 14:20:

    Um 90° gedreht: 5 Uhr und 35 Minuten
    Um 270° gedreht: 11 Uhr und 5 Minuten

Grenzen: Die Uhrzeit hat die Form Stunde:Minute mit einer Stunde von 0 bis 23
und einer Minute von 0 bis 59, zum Beispiel 14:20, 9:05 oder 0:00.

Hintergrund: Der Rest-Operator % (siehe Aufgabe 1_005) eignet sich zum Zählen im
Kreis. Nach 59 Minuten kommt wieder 0: (50 + 30) % 60 ergibt 20. Genauso
laufen die Stunden mit % 12 im Kreis, nur liefert % 12 die Werte 0 bis 11.
Damit aus der 0 eine 12 wird, ziehen Sie vorher 1 ab und zählen hinterher 1
dazu: (stunde - 1) % 12 + 1 macht aus 13 eine 1, aus 12 wieder eine 12 und aus
0 eine 12. % rechnet auch rückwärts im Kreis: (2 - 3) % 12 ergibt 11.

Die Zeile mit uhrzeit.split(":") steht schon im Programm: Sie zerlegt den
Text am Doppelpunkt in zwei Teile und speichert den ersten in stunde_text,
den zweiten in minute_text. Mit beiden Teilen rechnen Sie wie gewohnt weiter.

Tipp: Überlegen Sie am Zifferblatt, wie viele Stunden zwischen der 12 und der
6 liegen und wie viele Minuten. Um so viel rückt jeder Zeiger bei einer halben
Drehung weiter.
"""

uhrzeit = input("Uhrzeit (z. B. 14:20): ")
# Zerlegt "14:20" am Doppelpunkt in "14" und "20"
stunde_text, minute_text = uhrzeit.split(":")
stunde = int(stunde_text)
minute = int(minute_text)

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
print("Um 180° gedreht:", stunde_180, "Uhr und", minute_180, "Minuten")

# Zusatz: um 90° und um 270° im Uhrzeigersinn gedreht
pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
