# Musterlösung, automatisch erzeugt aus lehrkraft/muster/3_032_speichertarife.py - nicht von Hand ändern.
# Erst ansehen, wenn Ihre eigene Lösung besteht: python pruefe.py 3_032_speichertarife

"""Aufgabe 3_032 – Speichertarife                                Stufe 3 ★★★☆☆

Ein Rechenzentrum vermietet Speicherplatz für Sicherungen. Jeder Tarif hat
eine monatliche Grundgebühr, ein Freikontingent an Gigabyte, das in der
Grundgebühr enthalten ist, und einen Preis für jedes weitere Gigabyte. Alle
Beträge sind in Cent angegeben, damit keine Rundungsfehler entstehen. Der
Tarif „Basis“ kostet zum Beispiel 500 Cent im Monat, enthält 100 GB und
berechnet jedes weitere GB mit 4 Cent; bei 130 GB kostet er also
500 + 30 · 4 = 620 Cent.

Die Vertriebsabteilung will für jede Kundin schnell ausrechnen, welcher
Tarif am billigsten ist. Statt für jeden Tarif eine eigene Funktion von
Hand zu schreiben, soll eine Funktion die Preisfunktion eines Tarifs bauen.

Vervollständigen Sie zwei Funktionen:

- `baue_tarif(grundgebuehr, freikontingent, preis_pro_gb)` gibt eine
  Funktion zurück. Diese bekommt die belegten Gigabyte und gibt den
  Monatspreis des Tarifs in Cent zurück.
- `billigster_tarif(tarife, gigabyte)` bekommt ein Dictionary, das jedem
  Tarifnamen seine Preisfunktion zuordnet, und gibt den Namen des Tarifs
  zurück, der bei dieser Menge am wenigsten kostet. Kosten mehrere gleich
  wenig, gewinnt der, der im Dictionary zuerst steht.

    basis = baue_tarif(500, 100, 4)
    basis(130)                                  →  620
    basis(80)                                   →  500
    profi = baue_tarif(1500, 500, 2)
    billigster_tarif({"Basis": basis, "Profi": profi}, 130)  →  "Basis"
    billigster_tarif({"Basis": basis, "Profi": profi}, 900)  →  "Profi"

Grenzen: 0 ≤ grundgebuehr ≤ 10**6, 0 ≤ freikontingent ≤ 10**5 und
0 ≤ preis_pro_gb ≤ 10**4, alles ganze Zahlen. Die belegten Gigabyte sind
eine ganze Zahl mit 0 ≤ gigabyte ≤ 10**6. tarife ist nicht leer und hat
höchstens 1000 Einträge. Eine von baue_tarif gebaute Funktion rechnet auch
noch richtig, nachdem weitere Tarife gebaut wurden.

Hintergrund: Funktionen sind in Python Werte wie Zahlen oder Listen. Man
kann sie einer Variablen zuweisen, in ein Dictionary stecken und anderen
Funktionen übergeben (Aufgabe 3_028). Man kann sie auch zurückgeben: Eine
Funktion, die innerhalb einer anderen mit def angelegt wird, entsteht bei
jedem Aufruf der äußeren Funktion neu, und return gibt sie heraus, ohne sie
aufzurufen (ohne Klammern dahinter):

    def baue_gruss(anrede):
        def gruesse(name):
            return f"{anrede} {name}"
        return gruesse

    hallo = baue_gruss("Hallo")
    hallo("Ada")   →  "Hallo Ada"

Die innere Funktion darf die Parameter der äußeren lesen, und sie behält
deren Werte, auch wenn die äußere Funktion längst fertig ist: Jedes Ergebnis
von baue_gruss kennt seine eigene Anrede. Statt der inneren def geht auch
ein lambda (Aufgabe 3_025), wenn die Rechnung in einen Ausdruck passt.
"""


def baue_tarif(grundgebuehr, freikontingent, preis_pro_gb):
    """Gibt eine Funktion zurück, die zu den belegten Gigabyte den Monatspreis in Cent liefert."""
    def monatspreis(gigabyte):
        """Monatspreis dieses Tarifs in Cent bei gigabyte belegten Gigabyte."""
        zusaetzlich = max(0, gigabyte - freikontingent)
        return grundgebuehr + zusaetzlich * preis_pro_gb

    return monatspreis


def billigster_tarif(tarife, gigabyte):
    """Gibt den Namen des Tarifs zurück, der bei gigabyte am wenigsten kostet."""
    bester_name = None
    bester_preis = None
    for name, preisfunktion in tarife.items():
        preis = preisfunktion(gigabyte)
        if bester_preis is None or preis < bester_preis:
            bester_name = name
            bester_preis = preis
    return bester_name


basis = baue_tarif(500, 100, 4)
profi = baue_tarif(1500, 500, 2)
print(basis(130))
print(billigster_tarif({"Basis": basis, "Profi": profi}, 900))


# Idee: baue_tarif legt mit def eine innere Funktion monatspreis(gigabyte) an, die die Parameter von
# baue_tarif liest: Grundgebühr plus max(0, gigabyte - freikontingent) mal Preis pro GB. Dann gibt sie
# diese Funktion mit return monatspreis zurück, ohne sie aufzurufen. billigster_tarif geht die Einträge
# des Dictionarys durch, ruft jede Preisfunktion mit gigabyte auf und merkt sich den Namen mit dem
# kleinsten Preis; mit < statt <= bleibt bei Gleichstand der erste.
# Anderer Weg: return lambda gigabyte: grundgebuehr + max(0, gigabyte - freikontingent) * preis_pro_gb.
# Für billigster_tarif geht auch min(tarife, key=lambda name: tarife[name](gigabyte)); min liefert bei
# Gleichstand ebenfalls das erste Element.
# Typische Fehler: return monatspreis(...) statt return monatspreis (dann kommt eine Zahl statt einer
# Funktion zurück), die Werte in globalen Variablen ablegen (der zuletzt gebaute Tarif überschreibt alle
# anderen), das Freikontingent nicht abziehen oder unter dem Freikontingent einen negativen Zuschlag
# berechnen, und bei Gleichstand den letzten statt des ersten Tarifs nehmen.
# Laufzeit: baue_tarif und jede Preisfunktion brauchen O(1) Schritte, billigster_tarif O(n) bei n Tarifen,
# weil jede Preisfunktion genau einmal aufgerufen wird.
