# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_011_aufwand.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_011_aufwand

"""Aufgabe 2_011 – Aufwand                                       Stufe 2 ★★☆☆☆

Ein Entwicklungsteam plant seine Arbeit in Sprints von zwei Wochen. Jeder
Eintrag im Backlog, der Liste aller geplanten Aufgaben, wird in Story
Points geschätzt: Das ist eine grobe Größe für den Aufwand, keine Zeit.
Eine Kollegin hat schon die Funktion `aufwand` geschrieben, die aus den
Story Points eine Dauer in Arbeitstagen macht. Sie hat vier Parameter,
drei davon mit Standardwert: wie viele Stunden ein Story Point im Schnitt
kostet (6), wie viel Puffer für Unvorhergesehenes dazukommt (0.2, also
20 Prozent) und wie viele Personen gleichzeitig daran arbeiten (1).

Schreiben Sie zwei kurze Funktionen, die `aufwand` aufrufen und dabei nur
den einen Wert angeben, der sich ändert. Für alle anderen gelten die
Standardwerte von `aufwand`.

- `aufwand_im_team(story_points, personen)` gibt den Aufwand zurück, wenn
  personen Leute gleichzeitig an dem Eintrag arbeiten.
- `aufwand_ohne_puffer(story_points)` gibt den Aufwand ohne Puffer zurück,
  also mit puffer gleich 0, für Aufgaben, die das Team schon oft erledigt
  hat.

    aufwand(10)                 →  9.0
    aufwand_im_team(10, 3)      →  3.0
    aufwand_ohne_puffer(10)     →  7.5

Die Standardwerte von `aufwand` sollen nur an einer Stelle stehen. Ändert
die Kollegin später zum Beispiel die Stunden pro Story Point, müssen Ihre
Funktionen automatisch den neuen Wert benutzen.

Grenzen: story_points und personen sind ganze Zahlen mit
0 ≤ story_points ≤ 100 und 1 ≤ personen ≤ 20.

Hintergrund: Beim Aufruf einer Funktion kann man ein Argument mit seinem
Parameternamen angeben: aufwand(10, puffer=0). Das ist ein
Schlüsselwort-Argument. Python ordnet es nach dem Namen zu, nicht nach der
Position. So kann man Parameter mit Standardwert überspringen: puffer ist
der dritte Parameter, trotzdem muss man stunden_pro_punkt nicht angeben.
Ohne Namen müsste man aufwand(10, 6, 0) schreiben und dabei die 6 von
der Kollegin abschreiben; ändert sie ihren Standardwert, rechnet Ihr Code
weiter mit dem alten. Außerdem liest sich der Aufruf mit Namen leichter:
Bei aufwand(10, 6, 0, 3) muss man nachsehen, was die 3 bedeutet, bei
aufwand(10, personen=3) nicht. Schlüsselwort-Argumente stehen immer hinter
den Argumenten ohne Namen.

Tipp: Der Rumpf von aufwand_im_team ist eine einzige Zeile mit return.
"""


def aufwand(story_points, stunden_pro_punkt=6, puffer=0.2, personen=1):
    """Schätzt, wie viele Arbeitstage zu je 8 Stunden ein Backlog-Eintrag dauert."""
    stunden = story_points * stunden_pro_punkt * (1 + puffer)
    return round(stunden / (8 * personen), 1)


def aufwand_im_team(story_points, personen):
    """Gibt den Aufwand in Arbeitstagen zurück, wenn personen Leute daran arbeiten."""
    return aufwand(story_points, personen=personen)


def aufwand_ohne_puffer(story_points):
    """Gibt den Aufwand in Arbeitstagen ohne Puffer zurück."""
    return aufwand(story_points, puffer=0)


print("Allein mit Puffer:", aufwand(10), "Tage")
print("Zu dritt:", aufwand_im_team(10, 3), "Tage")
print("Ohne Puffer:", aufwand_ohne_puffer(10), "Tage")


# Idee: Beide Funktionen rufen aufwand auf und geben nur den Wert mit Namen an,
# der sich ändert: aufwand(story_points, personen=personen) und
# aufwand(story_points, puffer=0). Alle anderen Parameter behalten die
# Standardwerte, die in aufwand stehen.
#
# Anderer Weg: alle Argumente nach Position ausschreiben, etwa
# aufwand(story_points, 6, 0.2, personen). Das rechnet heute dasselbe, bricht
# aber, sobald die Kollegin einen Standardwert ändert; deshalb ist hier nur der
# Weg mit Schlüsselwort-Argumenten richtig.
#
# Typische Fehler: aufwand(story_points, personen) ohne Namen übergibt personen
# als stunden_pro_punkt; das Ergebnis mit return zurückgeben nicht vergessen.
