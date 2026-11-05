# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_024_hostauslastung.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_024_hostauslastung

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
    return [name for name, _, _, laeuft in vms if laeuft]


def belegte_hosts(vms):
    """Gibt die Menge der Hosts mit mindestens einer laufenden VM zurück."""
    return {host for _, host, _, laeuft in vms if laeuft}


def auslastung(vms, kapazitaet):
    """Gibt jedem Host aus kapazitaet seine Auslastung in Prozent zu, auf eine Stelle gerundet."""
    return {
        host: round(100 * sum(ram for _, vm_host, ram, laeuft in vms if laeuft and vm_host == host) / gesamt, 1)
        for host, gesamt in kapazitaet.items()
    }


def alle_unter(vms, kapazitaet, grenze):
    """Gibt zurück, ob kein Host über grenze Prozent ausgelastet ist."""
    return all(wert <= grenze for wert in auslastung(vms, kapazitaet).values())


vms = [("web1", "host-a", 4096, True), ("web2", "host-a", 4096, False), ("db1", "host-b", 16384, True), ("mail", "host-a", 2048, True)]
kapazitaet = {"host-a": 8192, "host-b": 32768, "host-c": 16384}
print(laufende(vms))
print(sorted(belegte_hosts(vms)))
print(auslastung(vms, kapazitaet))
print(alle_unter(vms, kapazitaet, 80), alle_unter(vms, kapazitaet, 70))


# Idee: laufende filtert mit if laeuft und behält nur den Namen, belegte_hosts tut dasselbe mit dem Host in
# geschweiften Klammern, sodass jeder Host nur einmal vorkommt. auslastung läuft mit einer Dict
# Comprehension über kapazitaet.items(); für jeden Host summiert ein Generator-Ausdruck die ram_mb der
# laufenden VMs auf diesem Host, und das Ergebnis wird in Prozent umgerechnet und gerundet. alle_unter
# benutzt auslastung und prüft mit all(wert <= grenze for …), dass kein Wert darüber liegt.
#
# Anderer Weg: In auslastung erst mit einer for-Schleife und get (Aufgabe 2_026) die Summe je Host in
# einem Dictionary sammeln und dann mit einer Dict Comprehension umrechnen; das geht die VMs nur einmal
# durch statt einmal pro Host. alle_unter ginge auch als not any(wert > grenze for …) oder als
# max(auslastung(...).values()) <= grenze, denn kapazitaet ist nie leer.
#
# Typische Fehler: ausgeschaltete VMs mitzählen, Hosts ohne laufende VM weglassen (sie sollen 0.0
# haben), < statt <= in alle_unter, anders runden als verlangt (erst teilen, dann mit 100 malnehmen kann
# in der letzten Stelle abweichen), oder {} für eine leere Menge halten.
#
# Laufzeit: laufende und belegte_hosts brauchen O(n) für n VMs. auslastung geht für jeden der h Hosts alle
# VMs durch, also O(h · n); bei höchstens 50 Hosts ist das schnell genug. Mit dem Dictionary aus dem anderen
# Weg wären es O(n + h).
