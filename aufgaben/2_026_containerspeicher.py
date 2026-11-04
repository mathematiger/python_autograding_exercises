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
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def speicher_pro_host(limits, laufend):
    """Gibt ein Dictionary zurück, das jedem Host die Summe der Limits seiner Container zuordnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


limits = {"shop": 2048, "datenbank": 8192}
print(speicherlimit(limits, "shop"), speicherlimit(limits, "mailer"))
print(speicher_pro_host(limits, [("shop", "host-a"), ("mailer", "host-b"), ("datenbank", "host-a")]))
