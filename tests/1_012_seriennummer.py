# Automatisch erzeugt aus lehrkraft/muster/1_012_seriennummer.py - nicht von Hand ändern.
# vorlage-hash: 2b1195eaa75f471b

EINGABEN = ["TH-2024-4711-EU"]

# Bei Eingabe TH-2024-4711-EU stimmen alle vier Teile
erwartet = "Gerätetyp: TH\nBaujahr: 2024\nLaufende Nummer: 4711\nRegion: EU"
assert AUSGABE == erwartet, f"Bei Eingabe TH-2024-4711-EU erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}"

# Eine andere Seriennummer gleicher Länge (nicht fest 2024, 4711 und EU hinschreiben!)
ausgabe = starte("BW-2019-0815-US")
erwartet = "Gerätetyp: BW\nBaujahr: 2019\nLaufende Nummer: 0815\nRegion: US"
assert ausgabe == erwartet, f"Bei Eingabe BW-2019-0815-US erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}"

# Eine längere laufende Nummer: Nummer und Region verschieben sich nach hinten
ausgabe = starte("TH-2025-104711-CH")
erwartet = "Gerätetyp: TH\nBaujahr: 2025\nLaufende Nummer: 104711\nRegion: CH"
if "Region: 71" in ausgabe or "Region: 47" in ausgabe or "Laufende Nummer: 1047\n" in ausgabe:
    hinweis = "\nTipp: Zählen Sie das Ende der laufenden Nummer und die Region mit negativen Indizes von hinten."
else:
    hinweis = ""
assert ausgabe == erwartet, (
    f"Bei Eingabe TH-2025-104711-CH erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
)

# Eine kürzere laufende Nummer
ausgabe = starte("LX-2023-7-JP")
erwartet = "Gerätetyp: LX\nBaujahr: 2023\nLaufende Nummer: 7\nRegion: JP"
if "Laufende Nummer: 7-" in ausgabe or "Laufende Nummer: -" in ausgabe:
    hinweis = "\nTipp: Der Bindestrich gehört nicht zur laufenden Nummer. Das Stück endet vor dem Index -3."
else:
    hinweis = ""
assert ausgabe == erwartet, f"Bei Eingabe LX-2023-7-JP erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"

# Die Bindestriche gehören nicht zu den Teilen
ausgabe = starte("MO-2020-31-AT")
erwartet = "Gerätetyp: MO\nBaujahr: 2020\nLaufende Nummer: 31\nRegion: AT"
if "-" in ausgabe:
    hinweis = "\nTipp: In Ihrer Ausgabe steht ein Bindestrich. Denken Sie daran: text[a:b] endet vor dem Index b."
else:
    hinweis = ""
assert ausgabe == erwartet, f"Bei Eingabe MO-2020-31-AT erwartet:\n{erwartet}\nIhr Programm gibt aus:\n{ausgabe}{hinweis}"
