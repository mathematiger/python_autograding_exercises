# Automatisch erzeugt aus lehrkraft/muster/1_023_adressbereich.py - nicht von Hand ändern.
# vorlage-hash: 6658d1c86a2fd7fd
# text-hash: 5bf0d10055ef3589
# thema: kontrollfluss
# inhalt: for über range(a, b)

EINGABEN = ["20", "23"]


def erwartete_ausgabe(erste, letzte):
    """Baut die erwartete Ausgabe mit einer while-Schleife statt mit range."""
    zeilen = []
    nummer = erste
    while nummer <= letzte:
        zeilen.append("192.168.10." + str(nummer))
        nummer = nummer + 1
    zeilen.append(f"{letzte - erste + 1} Adressen im Bereich.")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, erste, letzte):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if "192.168.10. " in ausgabe:
        return "\nTipp: print mit Kommas setzt ein Leerzeichen vor die Zahl; setzen Sie die Adresse mit einem f-String zusammen."
    if f"192.168.10.{letzte}\n" not in ausgabe + "\n":
        return f"\nTipp: Die letzte Adresse 192.168.10.{letzte} fehlt; range(a, b) hört vor b auf, schreiben Sie letzte + 1."
    if f"192.168.10.{erste}\n" not in ausgabe:
        return f"\nTipp: Die erste Adresse 192.168.10.{erste} fehlt; range soll bei erste anfangen."
    if f"192.168.10.{erste - 1}\n" in ausgabe:
        return "\nTipp: Es sind Adressen vor der ersten Endnummer dabei; range soll bei erste anfangen, nicht bei 0."
    return ""


# Das Beispiel aus der Aufgabe: 20 bis 23
assert AUSGABE == erwartete_ausgabe(20, 23), (
    f"Bei den Eingaben 20 und 23 erwartet:\n{erwartete_ausgabe(20, 23)}\nIhr Programm gibt aus:\n{AUSGABE}"
    f"{hinweis_zu(AUSGABE, 20, 23)}"
)

# Ein anderer Bereich (nicht fest hinschreiben!)
ausgabe = starte("100", "107")
assert ausgabe == erwartete_ausgabe(100, 107), (
    f"Bei den Eingaben 100 und 107 erwartet:\n{erwartete_ausgabe(100, 107)}\nIhr Programm gibt aus:\n{ausgabe}"
    f"{hinweis_zu(ausgabe, 100, 107)}"
)

# Erste und letzte Endnummer gleich: genau eine Adresse
ausgabe = starte("50", "50")
assert ausgabe == erwartete_ausgabe(50, 50), (
    f"Bei den Eingaben 50 und 50 erwartet:\n{erwartete_ausgabe(50, 50)}\nIhr Programm gibt aus:\n{ausgabe}"
    f"{hinweis_zu(ausgabe, 50, 50)}"
)

# Eine for-Schleife mit range wird benutzt
assert verwendet("for") and verwendet("range"), "Benutzen Sie für diese Aufgabe eine for-Schleife mit range(…, …)."

# Die Ränder: der ganze Bereich von 1 bis 254 und nur die 254
for erste, letzte in [(1, 254), (254, 254), (1, 1), (1, 2)]:
    ausgabe = starte(str(erste), str(letzte))
    zeilen = ausgabe.split("\n")
    assert ausgabe == erwartete_ausgabe(erste, letzte), (
        f"Bei den Eingaben {erste} und {letzte} erwartet: {letzte - erste + 2} Zeilen von 192.168.10.{erste} bis "
        f"192.168.10.{letzte} und dann „{letzte - erste + 1} Adressen im Bereich.“. Ihr Programm gibt {len(zeilen)} "
        f"Zeilen aus, die ersten: {zeilen[:2]}, die letzten: {zeilen[-2:]}{hinweis_zu(ausgabe, erste, letzte)}"
    )

# 40 zufällige Bereiche
zufall = Zufall(1023)
for _ in range(40):
    erste = zufall.randint(1, 254)
    letzte = zufall.randint(erste, min(254, erste + 30))
    ausgabe = starte(str(erste), str(letzte))
    assert ausgabe == erwartete_ausgabe(erste, letzte), (
        f"Bei den Eingaben {erste} und {letzte} erwartet:\n{erwartete_ausgabe(erste, letzte)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis_zu(ausgabe, erste, letzte)}"
    )
