# Musterlösung, automatisch erzeugt aus lehrkraft/muster/2_026_containerspeicher.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 2_026_containerspeicher

"""Aufgabe 2_026 – Containerspeicher                            Stufe 2 ★★☆☆☆

Ein Rechenzentrum betreibt die Anwendungen seiner Kunden in Containern:
abgeschotteten Paketen aus Programm und allem, was es braucht, die
gemeinsam auf einigen Servern (Hosts) laufen. Für jeden Container kann
ein Speicherlimit in MB eingetragen werden, mehr Arbeitsspeicher darf er
nicht belegen. Ist für einen Container nichts eingetragen, gilt das
Standardlimit STANDARD_MB = 512. Das Betriebsteam will wissen, wie viel
Speicher auf jedem Host höchstens belegt werden kann. Schreiben Sie zwei
Funktionen:

- `speicherlimit(limits, container)` gibt das Limit des Containers aus
  dem Dictionary limits zurück, oder STANDARD_MB, wenn er dort nicht
  steht.
- `speicher_pro_host(limits, laufend)` bekommt eine Liste von Tupeln
  (container, host), einen für jeden laufenden Container, und gibt ein
  Dictionary zurück, das jedem Host die Summe der Limits seiner
  Container zuordnet. Hosts ohne laufende Container kommen nicht vor.
  Benutzen Sie dafür speicherlimit.

Beide Funktionen benutzen get mit einem Standardwert und lassen limits
unverändert.

    limits = {"shop": 2048, "datenbank": 8192}
    speicherlimit(limits, "shop")          →  2048
    speicherlimit(limits, "mailer")        →  512
    laufend = [("shop", "host-a"), ("mailer", "host-b"), ("datenbank", "host-a")]
    speicher_pro_host(limits, laufend)     →  {"host-a": 10240, "host-b": 512}

Grenzen: limits hat 0 bis 10 000 Einträge, Containernamen sind nicht
leere Texte, Limits ganze Zahlen von 1 bis 10**6. Ein Limit darf auch
genau 512 oder kleiner sein. laufend hat 0 bis 100 000 Einträge, jeder
Container läuft höchstens einmal, Hostnamen sind nicht leere Texte.

Hintergrund: Liest man mit limits[container] einen Schlüssel, den es
nicht gibt, bricht das Programm mit einem KeyError ab (Aufgabe 2_025).
Die Methode get liefert stattdessen einen Ersatzwert:
limits.get("mailer", 512) gibt den Wert zu "mailer" zurück, wenn es
den Schlüssel gibt, sonst 512. Ohne zweites Argument ist der
Ersatzwert None. get liest nur und legt keinen neuen Eintrag an; das
Dictionary bleibt, wie es war. Beim Zählen und Summieren spart get das
if mit in: summe[host] = summe.get(host, 0) + wert legt den Host beim
ersten Mal mit 0 + wert an und addiert danach zum bisherigen Wert.
"""

STANDARD_MB = 512


def speicherlimit(limits, container):
    """Gibt das Speicherlimit des Containers zurück, ohne Eintrag STANDARD_MB."""
    return limits.get(container, STANDARD_MB)


def speicher_pro_host(limits, laufend):
    """Gibt ein Dictionary zurück, das jedem Host die Summe der Limits seiner Container zuordnet."""
    summe = {}
    for container, host in laufend:
        summe[host] = summe.get(host, 0) + speicherlimit(limits, container)
    return summe


limits = {"shop": 2048, "datenbank": 8192}
print(speicherlimit(limits, "shop"), speicherlimit(limits, "mailer"))
print(speicher_pro_host(limits, [("shop", "host-a"), ("mailer", "host-b"), ("datenbank", "host-a")]))


# Idee: speicherlimit ist ein einziger Aufruf limits.get(container, STANDARD_MB): Steht der Container im
# Dictionary, kommt sein Limit zurück, sonst das Standardlimit. speicher_pro_host läuft durch die Tupel,
# packt jedes in container und host aus und addiert das Limit zum bisherigen Wert des Hosts; get(host, 0)
# liefert beim ersten Container eines Hosts die 0, mit der die Summe anfängt.
#
# Anderer Weg: Mit if container in limits: … else: … und if host in summe: … else: … wie in Aufgabe 2_025.
# Das liefert dasselbe, braucht aber vier Zweige statt zwei Aufrufe von get.
#
# Typische Fehler: limits[container] ohne Prüfung (KeyError bei Containern ohne Eintrag), max(limit, 512)
# (ein kleineres eingetragenes Limit gilt trotzdem), das Standardlimit mit limits[container] = 512 in limits
# eintragen (dann ändert die Funktion das Dictionary des Aufrufers) oder summe[host] = limit statt
# summe.get(host, 0) + limit (dann zählt nur der letzte Container eines Hosts).
