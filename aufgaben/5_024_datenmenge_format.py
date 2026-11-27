"""Aufgabe 5_024 – Formatierte Datenmengen                       Stufe 5 ★★★★★

Ein Monitoring-Werkzeug zeigt, wie viele Daten jeder Server in der letzten
Stunde gesendet hat. Intern speichert es die Menge in Byte als ganze Zahl,
in Berichten soll sie aber lesbar erscheinen, und zwar je nach Bericht in
einer festen Einheit oder automatisch gewählt, mit wählbarer Zahl von
Nachkommastellen und in Spalten ausgerichtet. Das alles soll direkt in
f-Strings gehen: f"{menge:MB}", f"{menge:.3GB}", f"{menge:10auto}".
Vervollständigen Sie die Methode `Datenmenge.__format__(self, spec)`.

Aufbau der Formatangabe spec: `[breite][.stellen]einheit` oder leer.

- einheit ist eine von B, kB, MB, GB, TB (Faktor 1000 je Stufe, also
  1 kB = 1000 B, 1 MB = 10**6 B, …) oder auto. Bei auto wird die größte
  Einheit gewählt, deren Faktor höchstens so groß ist wie die Byte-Zahl
  (unter 1000 Byte also B).
- stellen (ganze Zahl) ist die Zahl der Nachkommastellen. Fehlt sie, gilt 0
  für B und 1 für alle anderen Einheiten.
- Die Zahl ist format(self.byte / faktor, f".{stellen}f"), dahinter ein
  Leerzeichen und die Einheit, z. B. "1.5 MB".
- breite (ganze Zahl) richtet den ganzen Text samt Einheit rechtsbündig auf
  diese Breite aus; ist er länger, bleibt er unverändert.
- Leere spec liefert dasselbe wie str(menge) (__str__ ist vorgegeben).
- Jede andere spec löst einen ValueError aus, dessen Meldung die spec nennt.

    menge = Datenmenge(1536000)
    f"{menge}"          →  "1536000 B"
    f"{menge:kB}"       →  "1536.0 kB"
    f"{menge:MB}"       →  "1.5 MB"
    f"{menge:.3MB}"     →  "1.536 MB"
    f"{menge:auto}"     →  "1.5 MB"
    f"{menge:10.2GB}"   →  "   0.00 GB"
    f"{menge:MiB}"      →  ValueError: Unbekannte Formatangabe 'MiB'

Grenzen: self.byte ist eine ganze Zahl mit 0 ≤ byte ≤ 10**15. breite ist
eine ganze Zahl von 0 bis 40 (ohne Vorzeichen, ohne führendes +), stellen
von 0 bis 10. Groß- und Kleinschreibung der Einheit zählt (kb oder mb sind
ungültig). Ungültig ist auch alles andere, etwa ">10MB", "MB10", "1.2.3MB",
".MB", "M B" oder "x". Bei auto hängt die Einheit von der ungerundeten
Byte-Zahl ab: 999 999 Byte werden zu "1000.0 kB".

Hintergrund: f"{wert:spec}" und format(wert, spec) rufen beide
`type(wert).__format__(wert, spec)` auf, und spec ist einfach der Text hinter
dem Doppelpunkt. f"{wert}" ohne Doppelpunkt ruft `__format__` mit dem leeren
Text auf. Was der Text bedeutet, legt jede Klasse selbst fest: Für Zahlen
heißt ".2f" zwei Nachkommastellen, für datetime heißt "%d.%m.%Y" ein Datum.

    format(3.14159, ".2f")       →  '3.14'
    format("Ok", ">6")           →  '    Ok'

Die geerbte Methode `object.__format__` kann nur die leere spec und liefert
dann str(wert); bei jeder anderen löst sie einen TypeError aus. Eine eigene
Klasse überschreibt `__format__` und gibt immer einen Text zurück (kein
print!):

    class Temperatur:
        def __init__(self, celsius):
            self.celsius = celsius
        def __str__(self):
            return f"{self.celsius} °C"
        def __format__(self, spec):
            if spec == "":
                return str(self)
            if spec == "F":
                return f"{self.celsius * 9 / 5 + 32:.1f} °F"
            raise ValueError(f"Unbekannte Formatangabe {spec!r}")

    t = Temperatur(20)
    f"{t}", f"{t:F}"             →  ('20 °C', '68.0 °F')

Eine gute eigene Formatsprache greift auf die vorhandenen zurück: Die Zahl
formatiert man mit format(zahl, f".{stellen}f"), das Ausrichten übernimmt
format(text, f">{breite}") oder text.rjust(breite). Die spec zerlegt man
zum Beispiel, indem man zuerst eine passende Einheit am Ende abschneidet
(spec.endswith(...)) und den Rest vorn prüft: Ziffern (rest.isdigit()),
dann vielleicht ein Punkt und wieder Ziffern. Ein regulärer Ausdruck wie
re.fullmatch (Aufgabe 4_067)(r"([0-9]*)(?:[.]([0-9]+))?(B|kB|MB|GB|TB|auto)",
spec) erledigt das in einem Schritt; er liefert None, wenn die spec nicht
passt.

Unbekannte Angaben sollte `__format__` nicht stillschweigend übergehen,
sondern einen ValueError auslösen, so wie format(3.5, "MB"). Mit !s oder !r
im f-String (f"{menge!s:>12}") wird übrigens zuerst str() oder repr()
gebildet und dann der Text formatiert; `__format__` der Klasse wird dann gar
nicht gefragt.
"""


class Datenmenge:
    """Eine Datenmenge in Byte mit eigener Formatangabe für f-Strings."""

    EINHEITEN = {"B": 1, "kB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}

    def __init__(self, byte):
        self.byte = byte

    def __str__(self):
        return f"{self.byte} B"

    def __format__(self, spec):
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


menge = Datenmenge(1536000)
print(f"{menge} | {menge:MB} | {menge:.3MB} | {menge:auto}")
