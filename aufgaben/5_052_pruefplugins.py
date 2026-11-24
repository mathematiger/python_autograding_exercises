"""Aufgabe 5_052 – Prüf-Plugins                                  Stufe 5 ★★★★★

Bei jedem Kontrollgang durch das Rechenzentrum prüft ein Werkzeug die
Anlagen: ob der Akku der USV (der unterbrechungsfreien Stromversorgung)
noch genug Ladung hat, ob ein RAID-Verbund eine ausgefallene Platte
meldet, ob die Kühlung die Zuluft unter 27 °C hält. Für jede Anlage
schreibt das zuständige Team ein eigenes kleines Modul, ein Plugin, und
legt es in einen Ordner. Das Werkzeug kennt die Plugins nicht im
Voraus: Welcher Ordner und welche Modulnamen es sind, steht erst zur
Laufzeit fest, etwa in einer Konfigurationsdatei. Jedes Plugin hält
sich an eine Vereinbarung:

    GERAET = "USV Raum 1"            # Text: welche Anlage geprüft wird

    def pruefe(messwerte):           # bekommt ein Dictionary aller Messwerte
        return messwerte["usv_ladung"] >= 50   # True: in Ordnung

Schreiben Sie drei Funktionen:

- `lade_plugin(modulname)` importiert das Modul mit dem Namen modulname
  (ein Text wie "usv" oder, für ein Modul in einem Paket, "kuehlung.raum_a")
  und gibt das Modulobjekt zurück. Fehlt dem Modul die Funktion pruefe
  (oder ist pruefe nicht aufrufbar) oder ist GERAET kein Text, löst sie
  einen TypeError aus, dessen Meldung den Modulnamen nennt. Lässt sich
  das Modul nicht importieren, darf die Ausnahme des Imports
  (ModuleNotFoundError, SyntaxError, …) einfach durchgehen.
- `lade_alle(ordner, modulnamen)` lädt die Plugins mit lade_plugin aus
  dem Ordner ordner (ein Pfad als Text) und gibt ein Tupel
  (geladen, fehlerhaft) zurück: geladen ist ein Dictionary
  Modulname → Modulobjekt, fehlerhaft ein Dictionary Modulname → Meldung
  für jedes Plugin, das sich nicht laden ließ, egal mit welcher Ausnahme.
  Die Meldung beginnt mit dem Namen der Ausnahme, z. B.
  "ModuleNotFoundError: No module named 'lueftung'". Ein kaputtes
  Plugin darf die anderen nicht aufhalten. Damit Python die Module im
  Ordner findet, kommt ordner vorn in sys.path; danach muss sys.path
  wieder genau so aussehen wie vorher, auch wenn etwas schiefging.
- `auffaellige(plugins, messwerte)` ruft für jedes Modul im Dictionary
  plugins (wie geladen von lade_alle) dessen pruefe(messwerte) auf und
  gibt die Liste der GERAET-Texte zurück, deren Prüfung False ergab,
  alphabetisch sortiert.

    geladen, fehlerhaft = lade_alle("/srv/pruefungen", ["usv", "raid", "lueftung"])
    geladen        →  {'usv': <module 'usv' from '/srv/pruefungen/usv.py'>,
                       'raid': <module 'raid' from '/srv/pruefungen/raid.py'>}
    fehlerhaft     →  {'lueftung': "ModuleNotFoundError: No module named 'lueftung'"}
    auffaellige(geladen, {"usv_ladung": 35, "raid_defekt": 0})
                   →  ['USV Raum 1']

Grenzen: 0 ≤ len(modulnamen) ≤ 50, die Namen sind verschieden und
bestehen aus Python-Bezeichnern, für Module in Paketen mit Punkten
dazwischen; ordner ist ein vorhandener Ordner. Ein Plugin kann fehlen,
beim Import eine beliebige Ausnahme auslösen (auch einen Syntaxfehler
enthalten), pruefe oder GERAET nicht haben. In auffaellige liefert jedes
pruefe True oder False, und die GERAET-Texte sind verschieden.

Hintergrund: Ein Modul ist in Python ein ganz gewöhnliches Objekt. Die
Anweisung `import math` (Aufgabe 3_045) tut zwei Dinge: Sie holt das
Modulobjekt und bindet es an den Namen math. Seine Funktionen und
Konstanten sind Attribute, darum gehen getattr, hasattr und
setattr wie bei jedem anderen Objekt, und man kann Module in Listen und
Dictionaries ablegen oder einer Funktion übergeben:

    import math
    type(math)                  →  <class 'module'>
    math.__name__               →  'math'
    getattr(math, "sqrt")(16)   →  4.0
    hasattr(math, "wurzel")     →  False

Steht der Modulname erst zur Laufzeit fest, hilft import nicht, denn
dahinter muss ein fester Name stehen. Dafür gibt es
importlib.import_module, das den Namen als Text bekommt und das
Modulobjekt zurückgibt; Punkte im Namen führen in Pakete hinein (ein
Paket ist ein Ordner mit einer Datei __init__.py):

    import importlib
    modul = importlib.import_module("json")
    modul.dumps([1, 2])         →  '[1, 2]'
    importlib.import_module("os.path").join("a", "b")   →  'a/b'

Wo sucht Python? Zuerst in sys.modules, einem Dictionary aller schon
geladenen Module. Steht der Name dort, kommt sofort dasselbe Objekt
zurück, ohne die Datei noch einmal zu lesen; ein zweiter Import kostet
also nichts und liefert mit `is` dasselbe Modul. Nur beim ersten Mal
geht Python die Ordner der Liste sys.path der Reihe nach durch, findet
dort name.py oder einen Paketordner name/, führt den Code der Datei
einmal von oben nach unten aus und trägt das fertige Modul in
sys.modules ein. Darum ist ein Plugin-Ordner nur sichtbar, wenn er in
sys.path steht. Weil sys.path für das ganze Programm gilt, räumt man
nach dem Laden wieder auf, auch im Fehlerfall, mit try/finally (Aufgabe
3_008):

    sys.path.insert(0, ordner)
    try:
        ...                     # Plugins laden
    finally:
        sys.path.remove(ordner)

Die schon geladenen Module bleiben dabei in sys.modules und funktionieren
weiter. Schlägt der Code eines Moduls beim Import fehl, gibt Python die
Ausnahme an den Aufrufer weiter und lässt das halbe Modul nicht in
sys.modules stehen. Fehlt das Modul ganz, kommt ModuleNotFoundError,
eine Unterklasse von ImportError. Weil ein Plugin fremder Code ist, kann
beim Import aber alles schiefgehen, bis zum ZeroDivisionError in der
ersten Zeile; ein Ladeprogramm fängt hier ausnahmsweise Exception ab.

Zwei Feinheiten noch: Python merkt sich, welche Dateien in einem Ordner
liegen. Kommen während des Programmlaufs neue Plugin-Dateien hinzu,
sorgt importlib.invalidate_caches() dafür, dass Python neu nachsieht.
Und ein schon geladenes Modul liest erst importlib.reload(modul) neu aus
der Datei; ein zweites import_module genügt nicht, es liefert das alte
Objekt aus sys.modules. Dass der Code eines Moduls beim Import
tatsächlich läuft, ist übrigens der Grund für die Zeile
`if __name__ == "__main__":` (Aufgabe 1_049): __name__ ist beim Import
der Modulname, nur beim direkten Start "__main__".

Tipp: f"{type(fehler).__name__}: {fehler}" ergibt Meldungen wie im
Beispiel.
"""

import importlib
import sys
import tempfile


def lade_plugin(modulname):
    """Importiert das Plugin modulname, prüft GERAET und pruefe und gibt das Modulobjekt zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def lade_alle(ordner, modulnamen):
    """Lädt alle Plugins aus ordner; gibt (geladen, fehlerhaft) zurück und lässt sys.path unverändert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def auffaellige(plugins, messwerte):
    """Gibt die GERAET-Texte der Plugins, deren pruefe(messwerte) False ergibt, sortiert zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


# Ein Plugin, das es nicht gibt, landet in fehlerhaft:
print(lade_alle(tempfile.gettempdir(), ["gibt_es_nicht_5052"]))
