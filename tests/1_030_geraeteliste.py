# Automatisch erzeugt aus lehrkraft/muster/1_030_geraeteliste.py - nicht von Hand ändern.
# vorlage-hash: e7d7569b84617959
# text-hash: cff7322d68805210
# thema: datenstrukturen
# inhalt: Listen verändern: ersetzen, remove

EINGABEN = ["Thermostat,Rauchmelder,Fensterkontakt,Bewegungsmelder", "2", "Rauchmelder Pro", "Fensterkontakt"]


def erwartete_ausgabe(namen, nummer, neu, defekt):
    """Baut die erwartete Ausgabe, indem sie eine neue Liste Element für Element zusammensetzt."""
    ergebnis = []
    for stelle in range(len(namen)):
        if stelle == nummer - 1:
            ergebnis.append(neu)
        elif namen[stelle] != defekt:
            ergebnis.append(namen[stelle])
    zeilen = [f"Verbundene Geräte: {len(ergebnis)}"]
    for name in ergebnis:
        zeilen.append(f"- {name}")
    return "\n".join(zeilen)


def hinweis_zu(ausgabe, namen, nummer, neu, defekt):
    """Gibt einen Tipp zu häufigen Fehlern, sonst einen leeren Text."""
    if nummer < len(namen) and f"- {namen[nummer - 1]}\n" in ausgabe + "\n" and f"- {neu}" in ausgabe:
        return (
            f"\nTipp: Das Gerät mit Nummer {nummer} steht noch in der Liste. Die Liste zählt ab 0, die Nummer ab 1: "
            "Ersetzen Sie geraete[nummer - 1]."
        )
    if f"- {neu}" not in ausgabe:
        return "\nTipp: Das neue Gerät fehlt. Ersetzen Sie mit geraete[nummer - 1] = neu das alte Gerät."
    if defekt in namen and f"- {defekt}\n" in ausgabe + "\n":
        return "\nTipp: Das defekte Gerät steht noch in der Liste. Entfernen Sie es mit geraete.remove(defekt)."
    return ""


def meldung(namen, nummer, neu, defekt, ausgabe, hinweis=""):
    """Baut die Fehlermeldung mit Eingaben, erwarteter und tatsächlicher Ausgabe."""
    return (
        f"Bei den Eingaben {','.join(namen)} und {nummer} und {neu} und {defekt} erwartet:\n"
        f"{erwartete_ausgabe(namen, nummer, neu, defekt)}\n"
        f"Ihr Programm gibt aus:\n{ausgabe}{hinweis or hinweis_zu(ausgabe, namen, nummer, neu, defekt)}"
    )


def pruefe_wartung(namen, nummer, neu, defekt):
    """Startet das Programm mit dieser Wartung; liefert die Ausgabe oder eine Beschreibung des Abbruchs und einen Tipp."""
    try:
        return starte(",".join(namen), str(nummer), neu, defekt), ""
    except Exception as fehler:
        if "ValueError" in str(fehler):
            return f"(Abbruch: {fehler})", (
                "\nTipp: remove bricht mit ValueError ab, wenn der Wert nicht in der Liste steht. "
                "Fragen Sie vorher mit if defekt in geraete: nach."
            )
        if "IndexError" in str(fehler):
            return f"(Abbruch: {fehler})", (
                "\nTipp: IndexError heißt, der Index ist zu groß. Gerät Nummer 1 ist geraete[0], "
                "also gehört an geraete[nummer - 1] das neue Gerät."
            )
        raise


# Das Beispiel aus der Aufgabe
BEISPIEL = ["Thermostat", "Rauchmelder", "Fensterkontakt", "Bewegungsmelder"]
assert AUSGABE == erwartete_ausgabe(BEISPIEL, 2, "Rauchmelder Pro", "Fensterkontakt"), meldung(
    BEISPIEL, 2, "Rauchmelder Pro", "Fensterkontakt", AUSGABE
)

# Andere Wartung (nicht fest hinschreiben!)
anlage = ["Heizkörperventil", "Steckdose Küche", "Lampe Flur", "Rollladen", "Wassersensor"]
ausgabe, hinweis = pruefe_wartung(anlage, 4, "Rollladen Funk", "Steckdose Küche")
assert ausgabe == erwartete_ausgabe(anlage, 4, "Rollladen Funk", "Steckdose Küche"), meldung(
    anlage, 4, "Rollladen Funk", "Steckdose Küche", ausgabe, hinweis
)

# Das defekte Gerät steht nicht in der Liste: nichts entfernen, kein Abbruch
anlage = ["Thermostat", "Rauchmelder", "Lampe"]
ausgabe, hinweis = pruefe_wartung(anlage, 1, "Thermostat 2", "Kamera")
assert ausgabe == erwartete_ausgabe(anlage, 1, "Thermostat 2", "Kamera"), meldung(
    anlage, 1, "Thermostat 2", "Kamera", ausgabe, hinweis
)

# Das letzte Gerät wird getauscht, das erste ist defekt
anlage = ["Klingel", "Türschloss", "Sirene"]
ausgabe, hinweis = pruefe_wartung(anlage, 3, "Sirene Plus", "Klingel")
assert ausgabe == erwartete_ausgabe(anlage, 3, "Sirene Plus", "Klingel"), meldung(
    anlage, 3, "Sirene Plus", "Klingel", ausgabe, hinweis
)

# Nur ein einziges Gerät
anlage = ["Router"]
ausgabe, hinweis = pruefe_wartung(anlage, 1, "Router Neu", "Repeater")
assert ausgabe == erwartete_ausgabe(anlage, 1, "Router Neu", "Repeater"), meldung(
    anlage, 1, "Router Neu", "Repeater", ausgabe, hinweis
)

# 40 zufällige Wartungen, mal mit, mal ohne defektes Gerät in der Liste
VORRAT = ["Thermostat", "Rauchmelder", "Fensterkontakt", "Bewegungsmelder", "Lampe", "Steckdose", "Rollladen",
          "Wassersensor", "Kamera", "Türschloss", "Sirene", "Klingel", "Heizkörperventil", "Luftsensor"]
zufall = Zufall(1030)
for _ in range(40):
    anlage = zufall.sample(VORRAT, zufall.randint(1, 10))
    nummer = zufall.randint(1, len(anlage))
    neu = anlage[nummer - 1] + " Neu"
    andere = [name for name in VORRAT if name != anlage[nummer - 1]]
    defekt = zufall.choice(andere)
    ausgabe, hinweis = pruefe_wartung(anlage, nummer, neu, defekt)
    assert ausgabe == erwartete_ausgabe(anlage, nummer, neu, defekt), meldung(
        anlage, nummer, neu, defekt, ausgabe, hinweis
    )

# Obere Grenze: 20 Geräte, Nummer 20, defekt ist Gerät 10
anlage = [f"Sensor {zahl}" for zahl in range(1, 21)]
ausgabe, hinweis = pruefe_wartung(anlage, 20, "Sensor 20b", "Sensor 10")
assert ausgabe == erwartete_ausgabe(anlage, 20, "Sensor 20b", "Sensor 10"), meldung(
    anlage, 20, "Sensor 20b", "Sensor 10", ausgabe, hinweis
)

# remove wird benutzt
assert verwendet("remove"), "Entfernen Sie das defekte Gerät mit geraete.remove(defekt)."
