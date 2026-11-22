"""Aufgabe 4_055 – Switchabfrage                                 Stufe 4 ★★★★☆

Ein Netzwerkteam verwaltet viele Switches über ein eigenes
Verwaltungsnetz. Ein Skript meldet sich bei jedem Switch an, schickt
einen Befehl wie "show version" und sammelt die Antworten. Jede
Anmeldung ist eine Sitzung, die der Switch nur in begrenzter Zahl
zulässt; vergisst das Skript, eine Sitzung zu schließen, kann sich nach
ein paar Durchläufen niemand mehr anmelden. Manche Switches sind
gerade nicht erreichbar, etwa wegen einer Wartung; dann soll das Skript
sie überspringen.

Die Verbindungen liefert ein fertiges Objekt netz (siehe unten):
netz.verbinde(host) öffnet eine Sitzung und gibt ein Objekt mit den
Methoden sende(befehl) (gibt die Antwort als Text zurück) und close()
zurück. Ist der Switch nicht erreichbar, löst verbinde einen
TimeoutError oder einen ConnectionError aus. Einen Kontextmanager
bietet die Sitzung selbst nicht an. Schreiben Sie:

- `mit_sitzung(netz, host, aktion)` öffnet eine Sitzung zu host, ruft
  aktion(sitzung) auf und gibt deren Ergebnis zurück. Die Sitzung wird
  danach in jedem Fall geschlossen, auch wenn aktion eine Ausnahme
  auslöst; die Ausnahme fliegt dann weiter. Benutzen Sie dafür
  contextlib.closing.
- `befrage_alle(netz, hosts, befehl)` schickt befehl an jeden Switch
  aus hosts, jeweils über mit_sitzung, und gibt ein Dictionary host →
  Antwort zurück, in der Reihenfolge von hosts. Switches, bei denen
  verbinde einen TimeoutError oder ConnectionError auslöst, fehlen
  darin. Benutzen Sie dafür contextlib.suppress. Andere Ausnahmen (etwa
  ein KeyError für einen unbekannten Befehl) fliegen weiter.
- `erster_erreichbarer(netz, hosts, befehl)` gibt ein Tupel (host,
  Antwort) für den ersten erreichbaren Switch aus hosts zurück und
  öffnet danach keine weitere Sitzung; ist keiner erreichbar, None.

    netz = Verwaltungsnetz(
        {"sw-1": {"show version": "IOS 15.2"}, "sw-3": {"show version": "IOS 16.9"}},
        nicht_erreichbar=["sw-2"],
    )
    mit_sitzung(netz, "sw-1", lambda s: s.sende("show version"))   →  "IOS 15.2"
    befrage_alle(netz, ["sw-1", "sw-2", "sw-3"], "show version")
        →  {"sw-1": "IOS 15.2", "sw-3": "IOS 16.9"}
    erster_erreichbarer(netz, ["sw-2", "sw-3", "sw-1"], "show version")
        →  ("sw-3", "IOS 16.9")
    netz.offene                                                    →  set()

Grenzen: hosts enthält 0 bis 500 verschiedene Namen. aktion ist eine
Funktion mit einem Parameter, die beliebige Ausnahmen auslösen darf.

Hintergrund: In Aufgabe 4_051 und 4_052 haben Sie eigene Kontextmanager
geschrieben. Für zwei häufige Fälle hat contextlib schon fertige:

    from contextlib import closing, suppress

    with closing(netz.verbinde("sw-1")) as sitzung:
        antwort = sitzung.sende("show clock")
    # hier ist sitzung.close() schon aufgerufen, auch nach einem Fehler

    with suppress(KeyError):
        del lager["Maus"]           # fehlt der Schlüssel, passiert nichts
    print("weiter")                 # läuft in jedem Fall

closing(objekt) macht aus jedem Objekt mit einer Methode close() einen
Kontextmanager: as liefert das Objekt selbst, beim Verlassen ruft es
close() auf. suppress(Art1, Art2, …) schluckt Ausnahmen dieser Arten
(und ihrer Unterarten, Aufgabe 3_030) und macht hinter dem with-Block
weiter; der Rest des Blocks nach der Ausnahme wird übersprungen. Es
ist eine kurze Form für try/except mit pass. Andere Ausnahmen fliegen
weiter. Setzen Sie suppress darum so eng wie möglich: um den Teil
einer einzelnen Runde, nicht um eine ganze Schleife, sonst bricht der
erste Fehler alles ab.

Oft soll nicht jeder Aufrufer selbst an das Öffnen und Schließen denken.
Dann schreibt man eine Funktion, die die Ressource öffnet, sie einer
übergebenen Funktion (einem Callback) reicht und danach aufräumt:

    def mit_datei(pfad, aktion):
        with open(pfad, encoding="utf-8") as datei:
            return aktion(datei)

    mit_datei("hosts.txt", lambda d: d.readline())

Ein return im with-Block ist erlaubt: Erst wird aufgeräumt, dann
kommt der Wert beim Aufrufer an. Was die Aktion braucht, gibt man ihr
mit einem lambda oder functools.partial mit (Aufgabe 4_028).
"""

from contextlib import closing, suppress


class Sitzung:
    """Eine Sitzung auf einem Switch; muss mit close() geschlossen werden."""

    def __init__(self, host, antworten, offene):
        """Öffnet die Sitzung und trägt sie in offene ein."""
        self.host = host
        self.antworten = antworten
        self.offene = offene
        self.offene.add(host)

    def sende(self, befehl):
        """Schickt einen Befehl und gibt die Antwort zurück; KeyError bei einem unbekannten Befehl."""
        if self.host not in self.offene:
            raise RuntimeError(f"Die Sitzung zu {self.host} ist schon geschlossen.")
        return self.antworten[befehl]

    def close(self):
        """Schließt die Sitzung."""
        self.offene.discard(self.host)


class Verwaltungsnetz:
    """Das Verwaltungsnetz: kennt die Switches und ihre Antworten."""

    def __init__(self, switches, nicht_erreichbar=()):
        """switches: host → {befehl: antwort}; nicht_erreichbar: Hosts, die nicht antworten."""
        self.switches = switches
        self.nicht_erreichbar = set(nicht_erreichbar)
        self.offene = set()

    def verbinde(self, host):
        """Öffnet eine Sitzung; TimeoutError oder ConnectionRefusedError, wenn das nicht geht."""
        if host in self.nicht_erreichbar:
            raise TimeoutError(f"{host} antwortet nicht")
        if host not in self.switches:
            raise ConnectionRefusedError(f"{host} lehnt die Anmeldung ab")
        return Sitzung(host, self.switches[host], self.offene)


def mit_sitzung(netz, host, aktion):
    """Öffnet eine Sitzung zu host, gibt aktion(sitzung) zurück und schließt die Sitzung in jedem Fall."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def befrage_alle(netz, hosts, befehl):
    """Schickt befehl an alle erreichbaren Switches; gibt host → Antwort zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def erster_erreichbarer(netz, hosts, befehl):
    """Gibt (host, Antwort) des ersten erreichbaren Switches zurück, sonst None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


netz = Verwaltungsnetz(
    {"sw-1": {"show version": "IOS 15.2"}, "sw-3": {"show version": "IOS 16.9"}},
    nicht_erreichbar=["sw-2"],
)
print(mit_sitzung(netz, "sw-1", lambda s: s.sende("show version")))
print(befrage_alle(netz, ["sw-1", "sw-2", "sw-3"], "show version"))
print(erster_erreichbarer(netz, ["sw-2", "sw-3", "sw-1"], "show version"))
print(netz.offene)
