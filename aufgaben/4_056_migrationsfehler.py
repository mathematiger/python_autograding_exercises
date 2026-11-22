"""Aufgabe 4_056 – Migrationsfehler                              Stufe 4 ★★★★☆

In einem Rechenzentrum laufen virtuelle Maschinen (VMs) auf mehreren
Hosts. Vor einem Hardwaretausch sollen viele VMs auf andere Hosts
umziehen (migriert werden). Ein Planungsskript prüft vorher jeden
Umzug: Der Zielhost darf nicht selbst in Wartung sein und muss genug
freien Arbeitsspeicher (RAM, in GB) und genug freie Prozessorkerne
haben. Damit das Skript und später andere Werkzeuge die Fehler gezielt
behandeln können, bekommt jede Fehlerart eine eigene Klasse:

    Exception
    └── MigrationsFehler          Attribut vm
        ├── HostInWartung         Attribut host
        └── KapazitaetsFehler     Attribut fehlend
            ├── ZuWenigRam
            └── ZuWenigKerne

- `MigrationsFehler(vm, meldung)`: speichert den Namen der VM als
  Attribut vm; str(fehler) ist die meldung.
- `HostInWartung(vm, host)`: zusätzlich das Attribut host, Meldung
  "esx-3 ist in Wartung, web-2 kann nicht umziehen" (mit host esx-3 und
  vm web-2).
- `KapazitaetsFehler(vm, fehlend, meldung)`: zusätzlich das Attribut
  fehlend, wie viel fehlt.
- `ZuWenigRam(vm, fehlend)`: Meldung "db-1: es fehlen 8 GB RAM".
- `ZuWenigKerne(vm, fehlend)`: Meldung "db-1: es fehlen 2 Kerne".

Schreiben Sie diese Klassen und zwei Funktionen. Eine VM ist ein
Dictionary mit "name", "ram" und "kerne"; hosts ist ein Dictionary
Hostname → {"ram_frei": …, "kerne_frei": …, "wartung": True/False}.

- `pruefe_umzug(vm, ziel, hosts)` löst den passenden Fehler aus, wenn
  die VM nicht auf den Host ziel umziehen kann, und prüft in dieser
  Reihenfolge: Wartung, RAM, Kerne. Sonst gibt sie None zurück. Ist
  ziel kein bekannter Host, fliegt der KeyError von hosts[ziel] weiter.
- `plane_umzuege(auftraege, hosts)` bekommt eine Liste von Paaren (vm,
  ziel) und prüft sie der Reihe nach. Passt ein Umzug, zieht sie RAM
  und Kerne der VM von den freien Werten des Zielhosts in hosts ab,
  damit der nächste Auftrag den neuen Stand sieht. Sie gibt ein
  Dictionary mit drei Listen zurück: "geplant" (Namen der VMs, die
  umziehen können), "zu_klein" (die Meldungen aller Kapazitätsfehler)
  und "wartung" (die Namen der Hosts in Wartung, die ein Auftrag
  treffen wollte, jeder nur einmal, in der Reihenfolge des ersten
  Treffers). Andere Ausnahmen fliegen weiter.

    hosts = {
        "esx-1": {"ram_frei": 64, "kerne_frei": 8, "wartung": False},
        "esx-3": {"ram_frei": 256, "kerne_frei": 32, "wartung": True},
    }
    db = {"name": "db-1", "ram": 72, "kerne": 4}
    web = {"name": "web-2", "ram": 16, "kerne": 4}
    pruefe_umzug(db, "esx-1", hosts)    →  ZuWenigRam: db-1: es fehlen 8 GB RAM
    plane_umzuege([(web, "esx-1"), (web, "esx-3"), (db, "esx-1")], hosts)
        →  {"geplant": ["web-2"], "zu_klein": ["db-1: es fehlen 24 GB RAM"], "wartung": ["esx-3"]}
    hosts["esx-1"]                      →  {"ram_frei": 48, "kerne_frei": 4, "wartung": False}

Grenzen: 0 bis 1000 Aufträge, 1 bis 100 Hosts. RAM und Kerne sind
ganze Zahlen von 1 bis 1024, die freien Werte von 0 bis 4096.

Hintergrund: Ausnahmen sind Klassen, und Python wählt den except-Zweig
über die Vererbung: except LookupError fängt auch KeyError und
IndexError (Aufgabe 3_030). Genauso baut man eigene Fehlerarten als
Unterklassen von Exception (Vererbung und super(), Aufgabe 4_006):

    class LagerFehler(Exception):
        def __init__(self, artikel, meldung):
            super().__init__(meldung)      # Exception speichert die Meldung
            self.artikel = artikel

    class Ausverkauft(LagerFehler):
        def __init__(self, artikel):
            super().__init__(artikel, f"{artikel} ist ausverkauft")

    try:
        raise Ausverkauft("Maus")
    except LagerFehler as fehler:
        fehler.artikel             →  "Maus"
        str(fehler)                →  "Maus ist ausverkauft"

super().__init__(meldung) gibt die Meldung an Exception weiter; daraus
macht str(fehler) den Text. Zusätzliche Attribute tragen die Daten, mit
denen der Aufrufer weiterarbeiten kann, ohne die Meldung zerlegen zu
müssen. Eine Hierarchie lässt jeden Aufrufer selbst wählen, wie fein er
unterscheidet: except KapazitaetsFehler behandelt RAM und Kerne
gemeinsam, except MigrationsFehler alles, was beim Umzug schiefgeht,
aber keine Programmierfehler wie KeyError. Die except-Zweige stehen vom
Speziellen zum Allgemeinen. Eine Klasse ohne eigene Methoden braucht
als Rumpf nur ihren Docstring.
"""

pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def pruefe_umzug(vm, ziel, hosts):
    """Löst den passenden MigrationsFehler aus, wenn die VM nicht auf ziel umziehen kann."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def plane_umzuege(auftraege, hosts):
    """Prüft alle Aufträge, bucht passende Umzüge und sammelt die Fehler nach Art."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


hosts = {
    "esx-1": {"ram_frei": 64, "kerne_frei": 8, "wartung": False},
    "esx-3": {"ram_frei": 256, "kerne_frei": 32, "wartung": True},
}
db = {"name": "db-1", "ram": 72, "kerne": 4}
web = {"name": "web-2", "ram": 16, "kerne": 4}
try:
    pruefe_umzug(db, "esx-1", hosts)
except MigrationsFehler as fehler:
    print(type(fehler).__name__, fehler)
print(plane_umzuege([(web, "esx-1"), (web, "esx-3"), (db, "esx-1")], hosts))
print(hosts["esx-1"])
