"""Aufgabe 3_026 – E-Mail-Verteiler                              Stufe 3 ★★★☆☆

Im Anmeldeformular eines Newsletters kann man mehrere Empfänger auf
einmal eintragen. Die Formularsoftware liefert die Einträge als Liste
von Texten, so wie sie getippt wurden: mit Leerzeichen davor und
dahinter, in gemischter Groß- und Kleinschreibung und mit leeren
Feldern dazwischen. Bevor die Adressen gespeichert werden, soll das
Formular sie bereinigen und dem Benutzer in einer verständlichen
Fehlermeldung zeigen, welche Adressen nicht gültig sind. Ob eine
Adresse gültig ist, prüft die vorgegebene Funktion ist_gueltig.
Schreiben Sie drei Funktionen, jede mit map oder filter, und geben Sie
jeweils eine Liste zurück:

- `bereinige(eintraege)`: jeder Eintrag ohne Leerzeichen am Anfang und
  Ende und in Kleinbuchstaben; Einträge, die danach leer sind, fallen
  weg. Benutzen Sie map und filter.
- `ungueltige(adressen)`: die Adressen, für die ist_gueltig False
  liefert. Benutzen Sie filter.
- `domains(adressen)`: zu jeder Adresse der Teil hinter dem @ (die
  Domain). Benutzen Sie map.

Die Reihenfolge bleibt immer die der Eingabe.

    bereinige(["  Ada@Firma.de", "", "ben@web.de ", "   ", "CEM@mail"])
        →  ["ada@firma.de", "ben@web.de", "cem@mail"]
    ungueltige(["ada@firma.de", "ben@web.de", "cem@mail"])  →  ["cem@mail"]
    domains(["ada@firma.de", "ben@web.de"])                 →  ["firma.de", "web.de"]

Grenzen: Jede Liste hat 0 bis 100 000 Einträge. Ein Eintrag in
bereinige ist ein Text mit 0 bis 100 Zeichen aus Buchstaben ohne
Umlaute, Ziffern, Leerzeichen und den Zeichen @ . - _. ungueltige
bekommt Ergebnisse von bereinige, domains nur gültige Adressen.

Hintergrund: map(funktion, liste) wendet funktion auf jedes Element an,
filter(funktion, liste) behält nur die Elemente, für die funktion einen
wahren Wert liefert. Beide geben keine Liste zurück, sondern einen
Iterator, der seine Werte erst beim Durchlaufen ausrechnet und nur
einmal durchlaufen werden kann (Aufgabe 3_021); list(...) macht daraus
eine Liste. Als funktion passt jede Funktion mit einem Parameter: eine
mit def geschriebene, ein lambda-Ausdruck (Aufgabe 3_025) oder eine
fertige wie len oder str.upper. Wichtig: Man übergibt die Funktion
selbst, ohne Klammern dahinter, denn map ruft sie später auf.

    preise = [3, 12, 7, 20]
    list(map(lambda p: p * 2, preise))           →  [6, 24, 14, 40]
    list(filter(lambda p: p > 5, preise))        →  [12, 7, 20]
    list(map(len, ["ab", "cde"]))                →  [2, 3]
    list(filter(lambda p: p > 5, map(lambda p: p * 2, preise)))
        →  [6, 24, 14, 40]                       (erst verdoppeln, dann filtern)

Das Gleiche schreibt man oft auch als List Comprehension (Aufgabe
3_017): [p * 2 for p in preise if p > 5]. map und filter sind praktisch,
wenn es die passende Funktion schon gibt, und man kann sie hintereinander
schalten, ohne Zwischenlisten zu bauen.
"""


def ist_gueltig(adresse):
    """Prüft vereinfacht: genau ein @, davor etwas, dahinter ein Punkt, der weder vorn noch hinten steht."""
    teile = adresse.split("@")
    if len(teile) != 2 or teile[0] == "":
        return False
    domain = teile[1]
    return "." in domain and not domain.startswith(".") and not domain.endswith(".")


def bereinige(eintraege):
    """Gibt die Einträge ohne Leerzeichen am Rand, in Kleinbuchstaben und ohne leere Einträge zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ungueltige(adressen):
    """Gibt die Adressen zurück, die ist_gueltig ablehnt."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def domains(adressen):
    """Gibt zu jeder Adresse den Teil hinter dem @ zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


eingabe = ["  Ada@Firma.de", "", "ben@web.de ", "   ", "CEM@mail"]
adressen = bereinige(eingabe)
print(adressen)
print(ungueltige(adressen))
print(domains(["ada@firma.de", "ben@web.de"]))
