# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_075_dialogablauf.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_075_dialogablauf

"""Aufgabe 3_075 – Dialogablauf                                  Stufe 3 ★★★☆☆

Am Empfang einer Firma steht ein Self-Service-Terminal, an dem
Beschäftigte ihr vergessenes Passwort selbst zurücksetzen. Der Dialog
besteht aus mehreren Bildschirmen: Auf dem Startbildschirm tippt man
auf „Passwort vergessen“, dann gibt man den Benutzernamen ein, dann den
Code, den das Diensthandy per SMS bekommen hat, und zuletzt das neue
Passwort. Jeder Bildschirm hat nur bestimmte Schaltflächen, und was
nach einem Tipp erscheint, hängt vom Bildschirm und von der
Schaltfläche ab. Das UX-Team beschreibt den Ablauf deshalb als Tabelle
der Übergänge, ein Dictionary {(bildschirm, ereignis): folgebildschirm}:

    DIALOG = {
        ("start", "vergessen"): "benutzername",
        ("benutzername", "weiter"): "code",
        ("benutzername", "abbrechen"): "start",
        ("code", "code_falsch"): "code",
        ("code", "code_richtig"): "passwort",
        ("code", "abbrechen"): "start",
        ("passwort", "speichern"): "fertig",
        ("passwort", "abbrechen"): "start",
    }

Ein Ereignis, für das es auf dem aktuellen Bildschirm keinen Übergang
gibt (etwa ein Tipp neben die Schaltflächen), ändert nichts: Der
Bildschirm bleibt stehen. Schreiben Sie vier Funktionen:

- `folgebildschirm(uebergaenge, bildschirm, ereignis)` gibt den
  Bildschirm zurück, der nach dem Ereignis angezeigt wird.
- `ablauf(uebergaenge, start, ereignisse)` spielt die Ereignisse der
  Reihe nach ab, beginnend bei start, und gibt die Liste aller
  angezeigten Bildschirme zurück: zuerst start, dann nach jedem
  Ereignis einen, also len(ereignisse) + 1 Einträge. Benutzen Sie
  dafür folgebildschirm.
- `schaltflaechen(uebergaenge, bildschirm)` gibt die alphabetisch
  sortierte Liste der Ereignisse zurück, für die es auf diesem
  Bildschirm einen Übergang gibt; so weiß das Terminal, welche
  Schaltflächen es zeigen muss.
- `endbildschirme(uebergaenge)` gibt die alphabetisch sortierte Liste
  der Bildschirme zurück, die als Folgebildschirm vorkommen, von denen
  aber kein Übergang wegführt, jeden einmal. Dort endet der Dialog;
  steht hier ein Bildschirm, der nicht als Ende geplant war, sitzt man
  an ihm fest.

    folgebildschirm(DIALOG, "code", "code_richtig")   →  "passwort"
    folgebildschirm(DIALOG, "start", "weiter")        →  "start"
    ablauf(DIALOG, "start", ["vergessen", "weiter", "code_falsch", "code_richtig", "speichern"])
        →  ["start", "benutzername", "code", "code", "passwort", "fertig"]
    schaltflaechen(DIALOG, "code")     →  ["abbrechen", "code_falsch", "code_richtig"]
    schaltflaechen(DIALOG, "fertig")   →  []
    endbildschirme(DIALOG)             →  ["fertig"]

Grenzen: 0 ≤ len(uebergaenge) ≤ 10 000, 0 ≤ len(ereignisse) ≤ 100 000.
Bildschirme und Ereignisse sind nicht leere Texte aus Kleinbuchstaben,
Ziffern und Unterstrichen. bildschirm und start dürfen auch Bildschirme
sein, die im Dictionary gar nicht vorkommen. uebergaenge bleibt
unverändert. ablauf soll für jedes Ereignis nur einmal im Dictionary
nachsehen, also O(len(ereignisse)) Schritte brauchen, egal wie viele
Übergänge es gibt.

Hintergrund: Ein Ablauf, der sich in jedem Moment in genau einem von
endlich vielen Zuständen befindet und bei jedem Ereignis nach einer
festen Regel in einen Folgezustand wechselt, heißt Zustandsautomat.
Man zeichnet ihn als Zustandsdiagramm: Kreise für die Zustände, Pfeile
mit dem Namen des Ereignisses für die Übergänge. Hier sind die
Bildschirme die Zustände und die Tipps auf Schaltflächen die
Ereignisse; ebenso arbeiten der Verbindungsaufbau im Netz oder der
Status einer Bestellung im Onlineshop. Statt einer langen Kette aus
if/elif für jeden Zustand legt man die Übergänge als Daten ab: als
Dictionary, dessen Schlüssel Tupel (zustand, ereignis) sind (Aufgabe
2_029). Den nächsten Zustand findet ein einziger Blick ins Dictionary,
egal wie groß es ist:

    regeln = {("aus", "taste"): "an", ("an", "taste"): "aus"}
    regeln[("aus", "taste")]                   →  "an"
    regeln.get(("an", "zweite_taste"), "an")   →  "an"   (kein Übergang)

get mit zweitem Argument liefert diesen Wert, wenn der Schlüssel fehlt
(Aufgabe 2_029). Ein neuer Bildschirm oder eine neue Schaltfläche ist
dann nur eine neue Zeile in der Tabelle, der Code bleibt gleich. Will
man über alle Übergänge etwas wissen, durchläuft man sie mit
for (von, ereignis), nach in uebergaenge.items(); eine Menge (Aufgabe
3_019) sammelt dabei jeden Bildschirm nur einmal.
"""

DIALOG = {
    ("start", "vergessen"): "benutzername",
    ("benutzername", "weiter"): "code",
    ("benutzername", "abbrechen"): "start",
    ("code", "code_falsch"): "code",
    ("code", "code_richtig"): "passwort",
    ("code", "abbrechen"): "start",
    ("passwort", "speichern"): "fertig",
    ("passwort", "abbrechen"): "start",
}


def folgebildschirm(uebergaenge, bildschirm, ereignis):
    """Gibt den Bildschirm nach dem Ereignis zurück; ohne passenden Übergang bleibt der Bildschirm."""
    return uebergaenge.get((bildschirm, ereignis), bildschirm)


def ablauf(uebergaenge, start, ereignisse):
    """Gibt die Liste aller Bildschirme zurück, die beim Abspielen der Ereignisse erscheinen."""
    bildschirm = start
    angezeigt = [start]
    for ereignis in ereignisse:
        bildschirm = folgebildschirm(uebergaenge, bildschirm, ereignis)
        angezeigt.append(bildschirm)
    return angezeigt


def schaltflaechen(uebergaenge, bildschirm):
    """Gibt die sortierten Ereignisse zurück, für die es auf dem Bildschirm einen Übergang gibt."""
    ereignisse = []
    for von, ereignis in uebergaenge:
        if von == bildschirm:
            ereignisse.append(ereignis)
    return sorted(ereignisse)


def endbildschirme(uebergaenge):
    """Gibt die sortierten Folgebildschirme zurück, von denen kein Übergang wegführt."""
    mit_ausgang = set()
    for von, _ in uebergaenge:
        mit_ausgang.add(von)
    enden = set()
    for nach in uebergaenge.values():
        if nach not in mit_ausgang:
            enden.add(nach)
    return sorted(enden)


print(folgebildschirm(DIALOG, "code", "code_richtig"))
print(ablauf(DIALOG, "start", ["vergessen", "weiter", "code_falsch", "code_richtig", "speichern"]))
print(schaltflaechen(DIALOG, "code"))
print(endbildschirme(DIALOG))


# Idee: folgebildschirm schlägt mit dem Tupel (bildschirm, ereignis) im Dictionary nach; get mit
# bildschirm als zweitem Argument erledigt den Fall „kein Übergang“. ablauf merkt sich den aktuellen
# Bildschirm, ersetzt ihn für jedes Ereignis durch den Folgebildschirm und sammelt alle in einer
# Liste, die mit start beginnt. schaltflaechen geht die Schlüssel durch und nimmt die Ereignisse
# des Bildschirms, endbildschirme sammelt die Bildschirme mit Ausgang in einer Menge und behält von
# den Folgebildschirmen die, die nicht darin stehen.
# Anderer Weg: if (bildschirm, ereignis) in uebergaenge: return uebergaenge[(bildschirm, ereignis)]
# statt get. schaltflaechen geht auch als sorted(e for von, e in uebergaenge if von == bildschirm),
# endbildschirme als Mengendifferenz set(uebergaenge.values()) - {von for von, _ in uebergaenge}.
# Typische Fehler: bei fehlendem Übergang None oder einen KeyError statt des alten Bildschirms,
# start nicht in die Liste aufnehmen, in folgebildschirm alle Übergänge durchsuchen (dann braucht
# ablauf O(n · m) Schritte), DIALOG statt uebergaenge benutzen, das Sortieren vergessen, und in
# endbildschirme Bildschirme mit einem Pfeil auf sich selbst für Enden halten.
# Laufzeit: folgebildschirm O(1), ablauf O(n) für n Ereignisse, schaltflaechen O(m log m) und
# endbildschirme O(m log m) für m Übergänge (einmal durchgehen, dann sortieren).
