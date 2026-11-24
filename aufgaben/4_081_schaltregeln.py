"""Aufgabe 4_081 – Schaltregeln                                  Stufe 4 ★★★★☆

Ein IoT-Gateway in einem Firmengebäude steuert die Lüfter mehrerer Räume.
Jeder Lüfter ist ein Aktor (ein Gerät, das etwas schaltet) und hat eine
Grenztemperatur: Liegt die gemessene Temperatur über der Grenze, wird er
eingeschaltet, sonst aus. Für jeden Aktor erzeugt das Gateway eine
Schaltregel, eine Funktion, die die Temperatur bekommt und True (an)
oder False (aus) zurückgibt. Ein Kollege hat das so versucht:

    grenzen = {"luefter_serverraum": 27.0, "luefter_lager": 30.0,
               "luefter_buero": 24.5}
    regeln = {aktor: lambda temperatur: temperatur > grenzen[aktor]
              for aktor in grenzen}
    regeln["luefter_lager"](28.0)   →  True    (erwartet: False)

Alle drei Regeln vergleichen mit der Grenze des Büros. Schreiben Sie drei
Funktionen:

- `schaltregeln(grenzen)` gibt ein Dictionary aktor → Schaltregel
  zurück. Jede Regel arbeitet mit der Grenze ihres eigenen Aktors, so
  wie sie beim Aufruf von schaltregeln war. Ändert jemand danach das
  Dictionary grenzen (Werte ändern, Einträge löschen), bleiben die
  Regeln, wie sie sind; das Gateway baut sie nur nach einer geprüften
  Freigabe neu.
- `live_regeln(grenzen)` gibt ebenfalls ein Dictionary aktor →
  Schaltregel zurück, für den Testbetrieb. Hier soll eine Regel bei
  jedem Aufruf die aktuelle Grenze ihres Aktors aus grenzen lesen: Wer
  in der App eine Grenze verschiebt, sieht die Wirkung sofort, ohne die
  Regeln neu zu bauen. Welcher Aktor zu welcher Regel gehört, bleibt
  aber fest.
- `gebundene_werte(funktion)` hilft bei der Fehlersuche. Sie gibt ein
  Dictionary zurück, das jede Variable, die funktion aus einer
  umgebenden Funktion oder Comprehension benutzt, auf ihren aktuellen
  Wert abbildet, und {}, wenn funktion keine solche Variable hat.

    regeln = schaltregeln(grenzen)
    regeln["luefter_lager"](28.0)          →  False
    regeln["luefter_buero"](28.0)          →  True
    grenzen["luefter_lager"] = 25.0
    regeln["luefter_lager"](28.0)          →  False   (Stand beim Bauen)
    live = live_regeln(grenzen)
    live["luefter_lager"](28.0)            →  True
    grenzen["luefter_lager"] = 29.0
    live["luefter_lager"](28.0)            →  False   (aktuelle Grenze)
    gebundene_werte(live["luefter_lager"])
            →  {"aktor": "luefter_lager", "grenzen": {...}}

Grenzen: grenzen hat 0 bis 1000 Einträge; die Aktoren sind nicht leere
Texte, die Grenzen und Temperaturen Zahlen von -50 bis 150. Eine
Temperatur gleich der Grenze schaltet aus. Bei live_regeln werden nach
dem Bauen nur Werte geändert, keine Aktoren gelöscht. funktion in
gebundene_werte ist eine mit def oder lambda geschriebene Funktion;
jede Variable, die sie von außen benutzt, hat schon einen Wert.

Hintergrund: In Aufgabe 4_028 haben Sie gesehen, dass ein lambda in
einer Schleife den letzten Wert der Schleifenvariablen benutzt, und
partial als Ausweg kennengelernt. Hier geht es darum, warum das so ist,
und wann man es sogar will. Eine Closure (Aufgabe 4_021) hebt nicht den
Wert einer äußeren Variablen auf, sondern die Variable selbst, in einer
Zelle (cell). Erst beim Aufruf schaut sie nach, was gerade in der Zelle
steht; das heißt späte Bindung. Die Zellen sieht man in
funktion.__closure__, ihre Namen in funktion.__code__.co_freevars:

    def schwelle(grenze):
        return lambda wert: wert > grenze

    regel = schwelle(27.0)
    regel.__code__.co_freevars       →  ("grenze",)
    regel.__closure__[0].cell_contents   →  27.0
    (lambda x: x * 2).__closure__    →  None   (keine äußeren Variablen)

Jeder Aufruf von schwelle hat seine eigene lokale Variable grenze, also
eine eigene Zelle. Eine Schleife oder Comprehension dagegen hat nur eine
Variable für alle Durchläufe. Alle darin gebauten Funktionen teilen sich
deren Zelle und sehen am Ende denselben, letzten Wert:

    regeln = [lambda wert: wert > g for g in (24.5, 27.0, 30.0)]
    regeln[0].__closure__[0] is regeln[2].__closure__[0]   →  True
    regeln[0](28.0)                  →  False   (vergleicht mit 30.0)

Es gibt drei übliche Auswege, die den Wert früh festhalten:

    [schwelle(g) for g in grenzen_liste]           # 1. Fabrikfunktion
    [lambda wert, g=g: wert > g for g in ...]      # 2. Standardwert
    [partial(groesser, grenze=g) for g in ...]     # 3. partial

Die Fabrikfunktion ist meist am klarsten: Jeder Aufruf legt eine neue
Zelle an. Der Standardwert nutzt aus, dass er beim Ausführen von def
bzw. lambda einmal ausgewertet wird (Aufgabe 4_080); die Regel bekommt
dadurch aber einen zweiten Parameter, den ein Aufrufer versehentlich
überschreiben kann.

Späte Bindung ist kein Fehler, sondern oft gewollt: Eine Funktion, die
ein Dictionary mit Einstellungen erst beim Aufruf liest, sieht jede
spätere Änderung. Fragen Sie sich also bei jeder äußeren Variablen und
bei jedem veränderlichen Objekt darin: Meine ich den Wert beim Bauen der
Funktion oder den beim Aufruf? Beim Bauen bindet man durch einen eigenen
Wert in einer eigenen Zelle, etwa grenzen[aktor] als Argument einer
Fabrikfunktion; beim Aufruf, indem man grenzen[aktor] erst im Rumpf der
Regel ausrechnet.
"""


def schaltregeln(grenzen):
    """Gibt aktor → Regel zurück; jede Regel benutzt die Grenze ihres Aktors beim Bauen."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def live_regeln(grenzen):
    """Gibt aktor → Regel zurück; jede Regel liest die aktuelle Grenze ihres Aktors beim Aufruf."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def gebundene_werte(funktion):
    """Gibt die äußeren Variablen von funktion mit ihren aktuellen Werten zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


grenzen = {"luefter_serverraum": 27.0, "luefter_lager": 30.0, "luefter_buero": 24.5}
regeln = schaltregeln(grenzen)
print(regeln["luefter_lager"](28.0), regeln["luefter_buero"](28.0))
grenzen["luefter_lager"] = 25.0
print(regeln["luefter_lager"](28.0))
live = live_regeln(grenzen)
print(live["luefter_lager"](28.0))
grenzen["luefter_lager"] = 29.0
print(live["luefter_lager"](28.0))
