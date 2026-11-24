"""Aufgabe 4_078 – Testimages                                    Stufe 4 ★★★★☆

Ein Qualitätssicherungsteam (QA) prüft jede neue Version seiner Software
in einem Testlabor. Dafür müssen vorher die Test-Images dorthin: fertig
eingerichtete Abbilder von Testrechnern mit Datenbank, Testdaten und
Konfiguration. Die Leitung ins Labor ist tagsüber für den Betrieb
reserviert, frei ist sie nur in nächtlichen Übertragungsfenstern, jedes
genau laenge Sekunden lang. Die Images gehen in einer festen Reihenfolge
hinaus (das Werkzeug arbeitet eine Liste ab), eins nach dem anderen.
Eine Übertragung darf nicht in einem Fenster beginnen und im nächsten
enden: Passt ein Image nicht mehr ganz in den Rest des aktuellen
Fensters, wartet es auf das nächste Fenster. Das Team will bei seinem
Anbieter eine schnellere Leitung buchen und fragt: Welche Bandbreite
brauchen wir mindestens, damit alle Images in höchstens fenster Nächten
ankommen?

Ein Image mit groesse MB braucht bei bandbreite MB/s volle Sekunden: Das
Werkzeug rechnet in ganzen Sekunden und rundet auf, 900 MB bei 200 MB/s
dauern also 5 Sekunden (4,5 aufgerundet). Schreiben Sie zwei Funktionen:

- `passt(groessen, fenster, laenge, bandbreite)` gibt True zurück, wenn
  alle Images der Liste groessen (in dieser Reihenfolge) mit dieser
  Bandbreite in höchstens fenster Übertragungsfenster passen, sonst
  False. Füllen Sie dafür die Fenster der Reihe nach so voll wie möglich.
- `kleinste_bandbreite(groessen, fenster, laenge)` gibt die kleinste
  ganze Bandbreite (mindestens 1) zurück, für die passt True ergibt,
  oder None, wenn das mit keiner Bandbreite geht. Benutzen Sie passt und
  eine binäre Suche über die Bandbreite.

    groessen = [600, 900, 300, 1200, 500]
    passt(groessen, 2, 10, 200)        →  True
        (Dauern 3, 5, 2, 6, 3: erste Nacht 3 + 5 + 2 = 10 Sekunden,
         zweite Nacht 6 + 3 = 9 Sekunden)
    passt(groessen, 2, 10, 199)        →  False
        (Dauern 4, 5, 2, 7, 3: 4 + 5, dann 2 + 7, dann 3, also drei Nächte)
    kleinste_bandbreite(groessen, 2, 10)  →  200
    kleinste_bandbreite(groessen, 3, 10)  →  150
    kleinste_bandbreite([1, 1, 1], 1, 2)  →  None

Grenzen: 0 ≤ len(groessen) ≤ 10 000, jede Größe ist eine ganze Zahl mit
1 ≤ groesse ≤ 10**9. fenster und laenge sind ganze Zahlen mit
1 ≤ fenster ≤ 10 000 und 1 ≤ laenge ≤ 10**6, für passt ist bandbreite
eine ganze Zahl mit 1 ≤ bandbreite ≤ 10**9. Ohne Images genügt jede
Bandbreite. passt soll O(n) Schritte brauchen, kleinste_bandbreite
O(n · log m) mit m = max(groessen); alle Bandbreiten von 1 an
durchzuprobieren ist bei Images von 10**9 MB viel zu langsam.

Hintergrund: In Aufgabe 3_002 haben Sie in einer sortierten Liste
gesucht, in Aufgabe 2_042 eine Wurzel durch Halbieren eines Bereichs
eingekreist, und in Aufgabe 4_077 hat bisect die Stelle in einer
sortierten Liste gefunden. Hier gibt es gar keine Liste, in der man
suchen könnte, sondern nur eine Ja-Nein-Frage: „Reicht die Bandbreite
b?“ Binäre Suche funktioniert trotzdem, und zwar immer dann, wenn diese
Frage monoton ist: Reicht b, dann reicht auch jedes größere b. Denkt
man sich die Antworten für b = 1, 2, 3, … nebeneinander, sieht das so
aus:

    b:        1      2      …    199    200    201    …
    passt:  False  False    …   False   True   True   …

Gesucht ist die Stelle, an der False in True umschlägt. Das ist eine
sortierte Folge, nur dass jeder Eintrag erst berechnet wird, wenn man
ihn anschaut. Man hält einen Bereich [unten, oben] fest, in dem die
Antwort sicher liegt, fragt in der Mitte nach und wirft jedes Mal die
Hälfte weg, in der sie nicht liegen kann. Beispiel: die kleinste ganze
Zahl x mit x · x ≥ n.

    def kleinste_wurzel(n):
        unten, oben = 0, n            # oben ist sicher groß genug
        while unten < oben:
            mitte = (unten + oben) // 2
            if mitte * mitte >= n:    # Ja: Antwort ist mitte oder kleiner
                oben = mitte
            else:                     # Nein: Antwort ist größer als mitte
                unten = mitte + 1
        return unten

    kleinste_wurzel(50)  →  8

Achten Sie darauf, dass jeder Durchlauf den Bereich wirklich verkleinert:
Mit unten = mitte statt mitte + 1 kann die Schleife bei zwei
benachbarten Zahlen ewig laufen. Und überlegen Sie vor der Suche, was
sicher reicht (die obere Grenze) und was sicher nicht. Hier lohnt die
Frage, ab welcher Bandbreite eine größere nichts mehr bringt, weil jede
Übertragung schon nur noch eine Sekunde dauert. Gibt es selbst dann
keine Lösung, gibt es überhaupt keine.

Dieses Muster heißt „binäre Suche auf der Antwort“: Statt die Antwort
direkt auszurechnen (hier gibt es keine Formel dafür, weil die
Aufteilung auf die Fenster von den aufgerundeten Dauern abhängt), prüft
man Kandidaten mit einer schnellen Ja-Nein-Funktion. Die Prüfung kostet
O(n), die Suche braucht etwa log₂ m Prüfungen, bei m = 10**9 also rund
30 statt bis zu einer Milliarde.

Aufrunden ohne Kommazahlen geht mit der ganzzahligen Division:
(a + b - 1) // b oder -(-a // b) ist a / b aufgerundet; math.ceil(a / b)
geht auch.
"""


def passt(groessen, fenster, laenge, bandbreite):
    """Gibt True zurück, wenn alle Images in dieser Reihenfolge in höchstens fenster Fenster passen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def kleinste_bandbreite(groessen, fenster, laenge):
    """Gibt die kleinste ganze Bandbreite zurück, mit der alles passt, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


groessen = [600, 900, 300, 1200, 500]
print(passt(groessen, 2, 10, 200))
print(kleinste_bandbreite(groessen, 2, 10))
