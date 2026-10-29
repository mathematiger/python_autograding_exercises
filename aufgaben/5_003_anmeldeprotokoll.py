"""Aufgabe 5_003 – Anmeldeprotokoll                               Stufe 5 ★★★★★

Ein Sicherheitswerkzeug zählt für jedes Benutzerkonto, wie oft an jedem
Tag eine Anmeldung mit falschem Passwort fehlgeschlagen ist. Viele
Fehlversuche an einem Tag können bedeuten, dass jemand das Passwort
errät. Die Zahlen stehen in einem zweidimensionalen numpy-Array
`protokoll`: Zeile i gehört zu Konto i, Spalte d zu Tag d, und das Jahr
beginnt an einem Montag, sodass die Tage 0 bis 6 die erste Woche sind.

Das Protokoll ist groß, und mehrere Teile des Werkzeugs arbeiten damit.
Wer es ändert und wer nur liest, muss deshalb genau wissen, ob er das
Original oder eine Kopie in der Hand hat. Schreiben Sie drei Funktionen:

- `wochenausschnitt(protokoll, woche)` gibt die sieben Spalten der Woche
  (Woche 0 sind die Tage 0 bis 6, Woche 1 die Tage 7 bis 13 …) für alle
  Konten zurück, und zwar als View: Die Administratorin korrigiert darin
  Fehlalarme, etwa ausschnitt[2, 3] = 0, und das soll sofort im
  Protokoll ankommen.
- `zuruecksetzen(protokoll, konten)` setzt nach einem Passwortwechsel die
  ganzen Zeilen der Konten aus der Liste konten im Protokoll selbst auf 0
  und gibt nichts zurück.
- `bereinigte_kopie(protokoll, konten)` gibt für einen Bericht ein neues
  Array zurück, in dem die Zeilen der Konten aus konten (Testkonten) 0
  sind. Das Protokoll selbst bleibt unverändert und teilt sich keinen
  Speicher mit dem Ergebnis.

Alle drei sollen ohne Python-Schleife auskommen und numpy die Arbeit
machen lassen.

    protokoll = np.array([[0, 3, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 0, 2],
                          [5, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 8, 0, 0]])
    w = wochenausschnitt(protokoll, 1)
    w[0, 0] = 0            →  protokoll[0, 7] ist jetzt auch 0
    bericht = bereinigte_kopie(protokoll, [2])
    bericht[2].sum()       →  0, aber protokoll[2].sum() ist weiter 12
    zuruecksetzen(protokoll, [0, 1])
    protokoll.sum()        →  12

Grenzen: protokoll ist ein Array mit ganzen Zahlen (dtype int64) von 0 bis
10**6 und der Form (n, t) mit 0 ≤ n ≤ 1000 Konten und 7 ≤ t ≤ 364 Tagen,
t ist durch 7 teilbar. 0 ≤ woche < t // 7. konten ist eine Liste
verschiedener Zeilennummern von 0 bis n - 1 in beliebiger Reihenfolge,
auch leer. Die Zahl der ausgeführten Python-Zeilen soll nicht mit n oder
der Länge von konten wachsen.

Hintergrund: Ein numpy-Array besteht aus zwei Teilen: einem Block
Speicher mit den Zahlen und einer Beschreibung, wie dieser Block zu lesen
ist (Form, Datentyp, Abstand zwischen Zeilen und Spalten). Darum kann
numpy für viele Operationen ein neues Array-Objekt liefern, das nur eine
neue Beschreibung hat, aber denselben Speicher benutzt: einen View.

Das Wichtigste, was man darüber wissen muss:

    a = np.arange(12).reshape(3, 4)   # 3 Zeilen, 4 Spalten
    v = a[:, 1:3]        # Slicing mit Doppelpunkt: View
    v[0, 0] = 99         # ändert auch a[0, 1]
    k = a[[0, 2]]        # Liste von Indizes (Fancy Indexing): Kopie
    k[0, 0] = -1         # a bleibt unverändert
    a[[0, 2]] = 0        # als Ziel einer Zuweisung: schreibt in a
    c = a.copy()         # ausdrücklich kopieren
    np.shares_memory(a, v)   →  True
    np.shares_memory(a, c)   →  False

Slicing mit Start:Ende:Schritt kann numpy immer als neue Beschreibung
desselben Speichers ausdrücken, darum ist es ein View und kostet keine
Zeit, egal wie groß das Array ist. Eine Liste von Indizes oder eine
Maske aus True und False dagegen wählt beliebige Zeilen aus, die nicht
mehr regelmäßig im Speicher liegen; das Ergebnis ist darum immer eine
Kopie. Steht derselbe Ausdruck aber links vom Gleichheitszeichen, ruft
Python a.__setitem__ auf, und numpy schreibt direkt in die ausgewählten
Stellen von a. Eine Zahl rechts vom = wird dabei an alle Stellen
verteilt: a[[0, 2]] = 0 setzt zwei ganze Zeilen auf 0.

Aufpassen muss man mit b = a: Das ist überhaupt keine neue Sicht, sondern
ein zweiter Name für dasselbe Objekt. Auch b = a[:] ist nur ein View. Wer
ein unabhängiges Array braucht, schreibt a.copy().
"""

import numpy as np


def wochenausschnitt(protokoll, woche):
    """Gibt die sieben Spalten der Woche für alle Konten als View auf protokoll zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def zuruecksetzen(protokoll, konten):
    """Setzt die Zeilen der Konten in protokoll selbst auf 0."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bereinigte_kopie(protokoll, konten):
    """Gibt eine Kopie von protokoll zurück, in der die Zeilen der Konten 0 sind."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


protokoll = np.array(
    [
        [0, 3, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 0, 2],
        [5, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 8, 0, 0],
    ]
)
w = wochenausschnitt(protokoll, 1)
w[0, 0] = 0
print("Nach der Korrektur:", protokoll[0, 7])
bericht = bereinigte_kopie(protokoll, [2])
print("Bericht:", bericht[2].sum(), "Protokoll:", protokoll[2].sum())
zuruecksetzen(protokoll, [0, 1])
print("Summe nach dem Zurücksetzen:", protokoll.sum())
