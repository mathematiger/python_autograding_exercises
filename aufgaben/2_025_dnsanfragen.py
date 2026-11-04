"""Aufgabe 2_025 – DNS-Anfragen                                 Stufe 2 ★★☆☆☆

Rechner finden einander im Netz über IP-Adressen; Menschen merken sich
lieber Namen wie "intranet.firma.de". Ein DNS-Server (Domain Name
System) übersetzt solche Namen in Adressen. Der Netzwerkadministrator
eines Unternehmens hat einen Mitschnitt der Anfragen an den eigenen
DNS-Server: einen Text, in dem die angefragten Namen durch Leerzeichen
oder Zeilenumbrüche getrennt stehen. Er möchte wissen, welche Namen wie
oft angefragt wurden, denn ein unbekannter Name mit sehr vielen
Anfragen kann auf Schadsoftware hindeuten. Groß- und Kleinschreibung
spielt bei DNS-Namen keine Rolle: "Intranet.Firma.de" und
"intranet.firma.de" sind derselbe Name. Schreiben Sie zwei Funktionen:

- `zaehle_anfragen(mitschnitt)` gibt ein Dictionary zurück, das jedem
  angefragten Namen, in Kleinbuchstaben, die Anzahl seiner Anfragen
  zuordnet.
- `haeufige_namen(mitschnitt, mindestens)` gibt die Liste der Namen (in
  Kleinbuchstaben) zurück, die mindestens mindestens-mal angefragt
  wurden, alphabetisch sortiert. Benutzen Sie dafür zaehle_anfragen.

    mitschnitt = "intranet.firma.de mail.firma.de Intranet.Firma.de x7q.example.org intranet.firma.de"
    zaehle_anfragen(mitschnitt)
        →  {"intranet.firma.de": 3, "mail.firma.de": 1, "x7q.example.org": 1}
    haeufige_namen(mitschnitt, 2)      →  ["intranet.firma.de"]
    zaehle_anfragen("")                →  {}

Grenzen: mitschnitt ist ein Text mit 0 bis 100 000 Namen, getrennt
durch Leerzeichen und Zeilenumbrüche, auch mehrere hintereinander und
am Anfang oder Ende. Ein Name besteht aus 1 bis 60 Buchstaben, Ziffern,
Punkten und Bindestrichen. mindestens ist eine ganze Zahl von 1 bis
100 000.

Hintergrund: Ein Dictionary (Typ dict) ordnet Schlüsseln Werte zu, wie
ein Telefonbuch Namen ihre Nummern. Man schreibt es in geschweiften
Klammern, {} ist das leere Dictionary. Mit eckigen Klammern liest und
schreibt man den Wert zu einem Schlüssel:

    anzahl = {}
    anzahl["mail"] = 1          # neuer Eintrag
    anzahl["mail"] = anzahl["mail"] + 1
    print(anzahl["mail"])       # 2
    print("web" in anzahl)      # False: diesen Schlüssel gibt es nicht

Jeder Schlüssel kommt höchstens einmal vor; eine Zuweisung an einen
vorhandenen Schlüssel ersetzt seinen Wert. Liest man einen Schlüssel,
den es nicht gibt, bricht das Programm mit einem KeyError ab. Beim
Zählen prüft man deshalb mit in, ob der Schlüssel schon da ist: Wenn
ja, erhöht man seinen Wert um 1, sonst legt man ihn mit dem Wert 1 an.
for name in anzahl durchläuft die Schlüssel, anzahl[name] liefert dann
den Wert dazu. Zwei Dictionaries sind gleich (==), wenn sie dieselben
Schlüssel mit denselben Werten haben, egal in welcher Reihenfolge.
split() ohne Argument trennt an beliebig vielen Leerzeichen und
Zeilenumbrüchen (Aufgabe 2_015).
"""


def zaehle_anfragen(mitschnitt):
    """Gibt ein Dictionary zurück, das jedem Namen in Kleinbuchstaben die Anzahl seiner Anfragen zuordnet."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def haeufige_namen(mitschnitt, mindestens):
    """Gibt die alphabetisch sortierte Liste der Namen mit mindestens mindestens Anfragen zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


mitschnitt = "intranet.firma.de mail.firma.de Intranet.Firma.de x7q.example.org intranet.firma.de"
print(zaehle_anfragen(mitschnitt))
print(haeufige_namen(mitschnitt, 2))
