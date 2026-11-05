"""Aufgabe 2_027 – Testkonten                                   Stufe 2 ★★☆☆☆

Ein Team entwickelt die Schnittstelle einer Vereinsverwaltung. Laut
ihrer Dokumentation liefert sie jedes Benutzerkonto als Dictionary mit
genau drei Schlüsseln: "name" (nicht leerer Text), "alter" (ganze Zahl
von 0 bis 120) und "rolle" (einer der Texte "gast", "mitglied" oder
"vorstand"). Für die Tests der Schnittstelle braucht das Team
Testdatensätze und eine Prüfung, ob ein Datensatz zur Dokumentation
passt. Schreiben Sie drei Funktionen:

- `konto(name, alter, rolle="gast")` gibt ein neues Dictionary mit den
  drei Schlüsseln und den übergebenen Werten zurück.
- `ist_gueltig(datensatz)` gibt True zurück, wenn datensatz genau die
  Schlüssel "name", "alter" und "rolle" hat und alle drei Werte die
  Regeln oben erfüllen, sonst False. Fehlt ein Schlüssel oder ist ein
  weiterer dabei, ist der Datensatz ungültig.
- `beschreibe(datensatz)` gibt für einen gültigen Datensatz einen Text
  wie "Kim (34 Jahre, vorstand)" zurück und für einen ungültigen den
  Text "ungültiger Datensatz". Benutzen Sie dafür ist_gueltig.

Keine der Funktionen verändert einen übergebenen Datensatz.

    konto("Kim", 34, "vorstand")      →  {"name": "Kim", "alter": 34, "rolle": "vorstand"}
    konto("Ali", 17)                  →  {"name": "Ali", "alter": 17, "rolle": "gast"}
    ist_gueltig({"name": "Kim", "alter": 121, "rolle": "gast"})  →  False
    ist_gueltig({"name": "Kim", "alter": 34})                    →  False
    beschreibe(konto("Kim", 34, "vorstand"))                    →  "Kim (34 Jahre, vorstand)"

Grenzen: konto bekommt einen nicht leeren Text, eine ganze Zahl von 0
bis 120 und eine der drei Rollen. Der datensatz für ist_gueltig und
beschreibe ist ein Dictionary mit 0 bis 10 Schlüsseln, die Texte sind;
unter "name" und "rolle" steht, wenn es sie gibt, immer ein Text (auch
ein leerer oder ein falscher), unter "alter" immer eine ganze Zahl von
-1000 bis 1000. Namen sind höchstens 100 Zeichen lang.

Hintergrund: Ein Dictionary (Aufgabe 2_025) kann auch einen einzelnen
Datensatz darstellen: Die Schlüssel sind die Namen der Felder, die
Werte deren Inhalt, so wie eine Zeile in einer Tabelle.

    person = {"name": "Kim", "alter": 34}
    person["alter"]        # 34
    "name" in person       # True: Gibt es das Feld?
    len(person)            # 2 Felder

Anders als bei einer Liste muss man sich nicht merken, an welcher
Stelle das Alter steht; man fragt das Feld über seinen Namen ab. Ob
ein Datensatz genau die erwarteten Felder hat, prüfen Sie zum Beispiel
mit len und in für jedes Feld, oder Sie vergleichen
sorted(datensatz) mit der sortierten Liste der Feldnamen, denn eine
for-Schleife oder sorted über ein Dictionary liefert seine Schlüssel.
"""

ROLLEN = ["gast", "mitglied", "vorstand"]


def konto(name, alter, rolle="gast"):
    """Gibt einen neuen Datensatz mit name, alter und rolle zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def ist_gueltig(datensatz):
    """Gibt zurück, ob datensatz genau die drei Felder mit erlaubten Werten hat."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def beschreibe(datensatz):
    """Gibt den Datensatz als Text wie "Kim (34 Jahre, vorstand)" zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


print(konto("Kim", 34, "vorstand"))
print(konto("Ali", 17))
print(ist_gueltig({"name": "Kim", "alter": 121, "rolle": "gast"}), ist_gueltig({"name": "Kim", "alter": 34}))
print(beschreibe(konto("Kim", 34, "vorstand")))
