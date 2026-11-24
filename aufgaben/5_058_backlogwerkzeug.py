"""Aufgabe 5_058 – Backlogwerkzeug                               Stufe 5 ★★★★★

Ein Team plant seine Arbeit mit einem selbst geschriebenen Werkzeug für
das Product Backlog, die geordnete Liste aller offenen Aufgaben. Solange
das Backlog ein paar Dutzend Einträge hatte, war alles schnell. Seit
das Werkzeug die Backlogs aller Teams der Firma verwaltet, mit
Hunderttausenden Einträgen, dauert jede Auswertung Minuten. Der Code sah
harmlos aus: Jede Zeile benutzt nur eingebaute Operationen. Aber nicht
jede eingebaute Operation ist billig (siehe Hintergrund).

Die drei langsamen Funktionen sind unten vorgegeben. Schreiben Sie zu
jeder eine schnelle Fassung, die dasselbe Ergebnis liefert, aber nur
O(n) Schritte braucht:

- `offene_aufgaben(backlog, erledigt)` gibt die Kennungen aus backlog,
  die nicht in erledigt stehen, in der Reihenfolge von backlog zurück.
- `einplanen(eingaenge)` bekommt die neuen Aufgaben in der Reihenfolge
  ihres Eingangs als Paare (kennung, dringend). Eine dringende Aufgabe
  kommt vor alle bisher eingeplanten, eine normale hinter sie. Die
  Funktion gibt die Kennungen in der geplanten Reihenfolge als Liste
  zurück. Verwenden Sie dafür collections.deque statt insert.
- `bericht(aufgaben)` bekommt Tripel (kennung, titel, punkte) und gibt
  den Bericht als einen Text zurück: je Aufgabe eine Zeile
  "kennung: titel (punkte SP)", jede mit "\\n" abgeschlossen. Bauen Sie
  den Text mit join statt mit +=.

    offene_aufgaben(["A-1", "A-2", "A-3", "A-4"], ["A-3", "A-1"])
        →  ["A-2", "A-4"]
    einplanen([("A-1", False), ("A-2", True), ("A-3", False), ("A-4", True)])
        →  ["A-4", "A-2", "A-1", "A-3"]
    bericht([("A-1", "Login", 3), ("A-2", "Export", 5)])
        →  "A-1: Login (3 SP)\\nA-2: Export (5 SP)\\n"

Grenzen: backlog und erledigt haben je 0 bis 200 000 Kennungen
(nicht leere Texte), backlog ohne Doppelte, erledigt darf Kennungen
enthalten, die nicht in backlog stehen. eingaenge hat 0 bis 200 000
Paare mit verschiedenen Kennungen, aufgaben 0 bis 200 000 Tripel mit
Titeln ohne Zeilenumbruch und punkte ganzen Zahlen von 0 bis 100. Alle
drei Funktionen sollen O(n) Schritte brauchen (bei offene_aufgaben
O(len(backlog) + len(erledigt))).

Hintergrund: Eine Zeile Python kann eine Schleife verstecken. Was eine
Operation kostet, hängt davon ab, wie die Daten im Speicher liegen:

    Operation                    list         set / dict     deque
    x in daten                   O(n)         O(1)           O(n)
    daten.append(x)              O(1)         –              O(1)
    daten.insert(0, x)           O(n)         –              –
    daten.appendleft(x)          –            –              O(1)
    daten.pop()                  O(1)         –              O(1)
    daten.pop(0) / popleft()     O(n)         –              O(1)
    daten[i]                     O(1)         –              O(n) in der Mitte

Eine Liste liegt als ein Block im Speicher: Das letzte Element anfügen
oder wegnehmen ist billig, aber insert(0, x) schiebt alle n Elemente
einen Platz weiter, und x in liste vergleicht im schlimmsten Fall mit
jedem Element (wie die lineare Suche in Aufgabe 3_001). Eine Menge
findet ein Element dagegen über seinen Hashwert direkt (Aufgabe 3_063).
Eine deque (Aufgaben 3_057 und 4_062) ist eine doppelt verkettete
Liste von kleinen Blöcken (vergleiche die verkettete Liste in Aufgabe
4_084); sie kann an beiden Enden billig wachsen, dafür ist der Zugriff
mitten hinein langsam.

Texte sind unveränderlich. text += zeile baut darum jedes Mal einen neuen
Text und kopiert den alten hinein; bei n Zeilen sind das zusammen
O(n²) kopierte Zeichen. CPython erkennt den Fall manchmal und hängt
heimlich an, aber darauf kann man sich nicht verlassen (in anderen
Python-Umgebungen und schon bei text = text + zeile + "\\n" oft nicht).
"".join(teile) rechnet erst die Gesamtlänge aus und kopiert jeden Teil
genau einmal:

    zeilen = []
    for name in namen:
        zeilen.append(f"{name}\\n")
    text = "".join(zeilen)          # oder "".join(f"{n}\\n" for n in namen)

Eine Operation, die O(n) kostet, in einer Schleife über n Elemente
ergibt O(n²) (Aufgabe 3_006): Bei 200 000 Einträgen sind das 4 · 10**10
Schritte, also Minuten statt Millisekunden. Die Abhilfe ist fast immer,
einmal vorab eine passende Datenstruktur zu bauen (eine Menge der
erledigten Kennungen, eine deque für beide Enden, eine Liste der Teile)
und in der Schleife nur noch billige Operationen zu benutzen.
"""

from collections import deque


def offene_aufgaben_langsam(backlog, erledigt):
    """Langsame Fassung: x in erledigt geht jedes Mal die ganze Liste durch."""
    offen = []
    for kennung in backlog:
        if kennung not in erledigt:
            offen.append(kennung)
    return offen


def einplanen_langsam(eingaenge):
    """Langsame Fassung: insert(0, …) verschiebt jedes Mal alle Einträge."""
    plan = []
    for kennung, dringend in eingaenge:
        if dringend:
            plan.insert(0, kennung)
        else:
            plan.append(kennung)
    return plan


def bericht_langsam(aufgaben):
    """Langsame Fassung: text += … kopiert jedes Mal den ganzen bisherigen Text."""
    text = ""
    for kennung, titel, punkte in aufgaben:
        text = text + f"{kennung}: {titel} ({punkte} SP)" + "\n"
    return text


def offene_aufgaben(backlog, erledigt):
    """Gibt die Kennungen aus backlog zurück, die nicht in erledigt stehen, in O(n)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def einplanen(eingaenge):
    """Plant dringende Aufgaben vorn und normale hinten ein, in O(n)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def bericht(aufgaben):
    """Gibt den Bericht mit einer Zeile je Aufgabe als einen Text zurück, in O(n)."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(offene_aufgaben(["A-1", "A-2", "A-3", "A-4"], ["A-3", "A-1"]))
print(einplanen([("A-1", False), ("A-2", True), ("A-3", False), ("A-4", True)]))
print(bericht([("A-1", "Login", 3), ("A-2", "Export", 5)]), end="")
