"""Aufgabe 1_021 – Angebotsprüfung                               Stufe 1 ★☆☆☆☆

Eine Firma will neue Notebooks für ihre Beschäftigten kaufen. Die
IT-Abteilung holt dazu Angebote von mehreren Händlern ein und bewertet
jedes nach denselben Regeln, damit der Vergleich fair bleibt. Neben dem
Preis zählen die Garantie, also wie viele Jahre der Händler kaputte
Geräte kostenlos repariert, und ein Siegel für geringen Stromverbrauch.

Die Regeln des Teams:

- Kostet ein Gerät mehr als 1500 Euro, ist das Angebot „zu teuer“, egal
  was es sonst bietet.
- Sonst ist es „sehr gut“, wenn die Garantie mindestens 3 Jahre beträgt
  und das Gerät das Siegel hat.
- Sonst ist es „gut“, wenn die Garantie mindestens 2 Jahre beträgt oder
  das Gerät das Siegel hat.
- In allen anderen Fällen ist es „ungenügend“.

Das Programm fragt schon nach Preis, Garantie und Siegel. Ergänzen Sie
die Entscheidung, die die passende Bewertung ausgibt. Bei den Eingaben
1200, 3 und ja:

    Angebot: 1200 Euro, 3 Jahre Garantie
    Bewertung: sehr gut

Bei den Eingaben 1200, 3 und nein steht dort „Bewertung: gut“, bei
1600, 5 und ja „Bewertung: zu teuer“ und bei 900, 1 und nein
„Bewertung: ungenügend“.

Grenzen: Der Preis ist eine ganze Zahl von 0 bis 5000, die Garantie eine
ganze Zahl von 0 bis 10, die letzte Antwort ist "ja" oder "nein".

Hintergrund: Diese Übung verbindet, was Sie über Bedingungen wissen. Ein
Vergleich wie preis > 1500 (Aufgabe 1_016) ergibt True oder False. Mit
if, elif und else (Aufgaben 1_018 und 1_019) führt Python genau einen
Block aus, den der ersten wahren Bedingung; darum steht die Regel, die
alles andere schlägt, ganz oben. and und or (Aufgabe 1_020) verknüpfen
zwei Bedingungen. Die Variable siegel ist schon True oder False und kann
darum direkt in einer Bedingung stehen:

    if garantie >= 2 and siegel:

Tipp: Gehen Sie die Regeln in ihrer Reihenfolge durch: ein if, zwei elif
und ein else, in jedem Block ein print.
"""

preis = int(input("Preis pro Gerät in Euro: "))
garantie = int(input("Garantie in Jahren: "))
siegel = input("Siegel für geringen Stromverbrauch (ja/nein)? ") == "ja"
print(f"Angebot: {preis} Euro, {garantie} Jahre Garantie")

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code
