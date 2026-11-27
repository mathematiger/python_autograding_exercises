"""Aufgabe 4_060 – WLAN-Anmeldungen                              Stufe 4 ★★★★☆

Im Firmengebäude stehen mehrere WLAN-Access-Points (APs), die Sender,
mit denen sich Laptops und Handys verbinden. Jeder AP strahlt mehrere
Netze aus, erkennbar an ihrem Namen, der SSID: "Firma" für die
Beschäftigten und "Gast" für Besucher. Der WLAN-Controller, der alle APs
verwaltet, protokolliert jede Anmeldung eines Geräts als Tripel (AP,
SSID, Gerät):

    anmeldungen = [("ap-eg", "Firma", "laptop-ada"), ("ap-og", "Gast", "handy-bo"),
                   ("ap-eg", "Gast", "tablet-cem"), ("ap-eg", "Firma", "handy-dana"),
                   ("ap-og", "Firma", "laptop-ada")]

Für die Netzplanung soll ausgewertet werden, wie die APs genutzt
werden. Schreiben Sie mit collections.defaultdict drei Funktionen:

- `geraete_je_ap(anmeldungen)`: AP → Liste der Geräte in der Reihenfolge
  ihrer Anmeldungen (meldet sich ein Gerät mehrmals an, steht es
  mehrmals darin).
- `ssids_je_ap(anmeldungen)`: AP → alphabetisch sortierte Liste der
  SSIDs, über die sich dort mindestens ein Gerät angemeldet hat, jede
  nur einmal.
- `anzahl_je_ssid_und_ap(anmeldungen)`: SSID → Dictionary AP → Anzahl
  der Anmeldungen.

    geraete_je_ap(anmeldungen)  →  {"ap-eg": ["laptop-ada", "tablet-cem", "handy-dana"],
                                    "ap-og": ["handy-bo", "laptop-ada"]}
    ssids_je_ap(anmeldungen)    →  {"ap-eg": ["Firma", "Gast"], "ap-og": ["Firma", "Gast"]}
    anzahl_je_ssid_und_ap(anmeldungen)
                                →  {"Firma": {"ap-eg": 2, "ap-og": 1}, "Gast": {"ap-og": 1, "ap-eg": 1}}

Die Ergebnisse sind gewöhnliche Dictionaries (type(ergebnis) is dict),
auch die inneren bei anzahl_je_ssid_und_ap, damit ein Tippfehler beim
Nachschlagen später einen KeyError auslöst. In den Dictionaries
kommen nur APs und SSIDs vor, die in anmeldungen stehen.

Grenzen: 0 bis 100 000 Anmeldungen, alle drei Teile sind nicht leere
Texte.

Hintergrund: Beim Gruppieren mit einem gewöhnlichen Dictionary (Aufgabe
2_041) muss man vor jedem Anhängen prüfen, ob es den Schlüssel schon gibt,
oder setdefault benutzen: gruppen.setdefault(abteilung, []) gibt die Liste
unter abteilung zurück und legt vorher eine leere an, falls es sie noch
nicht gibt; gruppen.setdefault(abteilung, []).append(name) gruppiert
also in einer Zeile.

    gruppen = {}
    for name, abteilung in personen:
        if abteilung not in gruppen:
            gruppen[abteilung] = []
        gruppen[abteilung].append(name)

collections.defaultdict nimmt einem das ab. Man gibt ihm eine Funktion
ohne Argumente mit, die Fabrik; fragt man nach einem Schlüssel, den es
nicht gibt, ruft es die Fabrik auf, trägt ihr Ergebnis unter dem
Schlüssel ein und gibt es zurück:

    from collections import defaultdict

    gruppen = defaultdict(list)          # list() ist []
    for name, abteilung in personen:
        gruppen[abteilung].append(name)

    zaehler = defaultdict(int)           # int() ist 0
    zaehler["rot"] += 1                  # 0 + 1

    farben = defaultdict(set)            # set() ist eine leere Menge
    farben["Ada"].add("blau")

Die Fabrik darf alles sein, was man ohne Argument aufrufen kann, auch
eine lambda-Funktion (Aufgabe 3_025). Für zwei Ebenen nimmt man eine
Fabrik, die selbst ein defaultdict baut:

    tabelle = defaultdict(lambda: defaultdict(int))
    tabelle["Montag"]["Ada"] += 1

Vorsicht: Schon das Lesen eines fehlenden Schlüssels legt ihn an. Nach
print(gruppen["Vertrieb"]) gibt es die Gruppe "Vertrieb" mit einer
leeren Liste, und ein Tippfehler fällt nie auf. Nur
schluessel in gruppen und gruppen.get(schluessel) fragen, ohne anzulegen. Darum gibt man nach außen meist ein gewöhnliches Dictionary
zurück: dict(gruppen) kopiert die Einträge in ein dict, bei zwei Ebenen
muss man auch jedes innere umwandeln.
"""

from collections import defaultdict


def geraete_je_ap(anmeldungen):
    """Gibt ein Dictionary AP → Liste der angemeldeten Geräte zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ssids_je_ap(anmeldungen):
    """Gibt ein Dictionary AP → sortierte Liste der genutzten SSIDs zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def anzahl_je_ssid_und_ap(anmeldungen):
    """Gibt ein Dictionary SSID → (AP → Anzahl der Anmeldungen) zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


anmeldungen = [
    ("ap-eg", "Firma", "laptop-ada"),
    ("ap-og", "Gast", "handy-bo"),
    ("ap-eg", "Gast", "tablet-cem"),
    ("ap-eg", "Firma", "handy-dana"),
    ("ap-og", "Firma", "laptop-ada"),
]
print(geraete_je_ap(anmeldungen))
print(ssids_je_ap(anmeldungen))
print(anzahl_je_ssid_und_ap(anmeldungen))
