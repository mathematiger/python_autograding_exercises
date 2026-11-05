"""Aufgabe 3_024 – Hostauslastung                               Stufe 3 ★★★☆☆

Ein Rechenzentrum betreibt für seine Kunden virtuelle Maschinen (VMs):
Rechner, die nur als Software existieren und sich zu mehreren einen
echten Server, den Host, teilen. Die Verwaltung liefert jede VM als
Tupel (name, host, ram_mb, laeuft): ihr Name, der Host, auf dem sie
liegt, der Arbeitsspeicher in MB, den sie belegt, solange sie läuft,
und ob sie gerade läuft (True oder False). Ausgeschaltete VMs belegen
keinen Arbeitsspeicher. Zu jedem Host ist im Dictionary kapazitaet
eingetragen, wie viel MB er hat. Für die Nachtschicht soll ein kleines
Werkzeug zeigen, wie voll die Hosts sind. Schreiben Sie vier Funktionen:

- `laufende(vms)` gibt die Liste der Namen aller laufenden VMs zurück,
  in der Reihenfolge von vms.
- `belegte_hosts(vms)` gibt die Menge der Hosts zurück, auf denen
  mindestens eine VM läuft.
- `auslastung(vms, kapazitaet)` gibt ein Dictionary zurück, das jedem
  Host aus kapazitaet seine Auslastung in Prozent zuordnet:
  round(100 * belegt / kapazitaet[host], 1), wobei belegt die Summe
  der ram_mb seiner laufenden VMs ist (0 ohne laufende VM).
- `alle_unter(vms, kapazitaet, grenze)` gibt True zurück, wenn kein
  Host eine Auslastung über grenze Prozent hat, sonst False.

Benutzen Sie für die ersten drei Funktionen je eine Comprehension, für
die Summe in auslastung und für alle_unter einen Generator-Ausdruck.

    vms = [("web1", "host-a", 4096, True), ("web2", "host-a", 4096, False),
           ("db1", "host-b", 16384, True), ("mail", "host-a", 2048, True)]
    kapazitaet = {"host-a": 8192, "host-b": 32768, "host-c": 16384}
    laufende(vms)                      →  ["web1", "db1", "mail"]
    belegte_hosts(vms)                 →  {"host-a", "host-b"}
    auslastung(vms, kapazitaet)        →  {"host-a": 75.0, "host-b": 50.0, "host-c": 0.0}
    alle_unter(vms, kapazitaet, 80)    →  True
    alle_unter(vms, kapazitaet, 70)    →  False

Grenzen: vms hat 0 bis 10 000 Tupel mit verschiedenen Namen; ram_mb
ist eine ganze Zahl von 1 bis 10**6. kapazitaet hat 1 bis 50 Hosts mit
ganzen Zahlen von 1 bis 10**7, und jeder Host aus vms steht darin. Die
Summe auf einem Host darf größer sein als seine Kapazität (überbucht,
mehr als 100 %). grenze ist eine ganze Zahl von 0 bis 1000. Eine
Auslastung, die genau gleich grenze ist, liegt nicht über der Grenze.

Hintergrund: Diese Übung verbindet die letzten Aufgaben. Eine List
Comprehension [name for name, host, ram, an in vms if an] filtert und
bildet ab in einer Zeile (Aufgabe 3_017), eine Set Comprehension in
geschweiften Klammern sammelt jeden Wert nur einmal (Aufgabe 3_019),
und eine Dict Comprehension {host: wert for host in …} baut ein
Dictionary aus Schlüssel und Wert (Aufgabe 3_018). Ein
Generator-Ausdruck in runden Klammern liefert seine Werte einzeln an
sum oder all, ohne eine Liste anzulegen (Aufgabe 3_023). Comprehensions
lassen sich verschachteln: In der Dict Comprehension für auslastung
darf als Wert ein sum(... for ...) stehen, das für jeden Host die
passenden VMs aufsummiert. Eine Comprehension darf auch eine andere
Funktion aufrufen; alle_unter kann also auslastung benutzen.
"""


def laufende(vms):
    """Gibt die Namen aller laufenden VMs in ihrer Reihenfolge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def belegte_hosts(vms):
    """Gibt die Menge der Hosts mit mindestens einer laufenden VM zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auslastung(vms, kapazitaet):
    """Gibt jedem Host aus kapazitaet seine Auslastung in Prozent zu, auf eine Stelle gerundet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def alle_unter(vms, kapazitaet, grenze):
    """Gibt zurück, ob kein Host über grenze Prozent ausgelastet ist."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


vms = [("web1", "host-a", 4096, True), ("web2", "host-a", 4096, False), ("db1", "host-b", 16384, True), ("mail", "host-a", 2048, True)]
kapazitaet = {"host-a": 8192, "host-b": 32768, "host-c": 16384}
print(laufende(vms))
print(sorted(belegte_hosts(vms)))
print(auslastung(vms, kapazitaet))
print(alle_unter(vms, kapazitaet, 80), alle_unter(vms, kapazitaet, 70))
