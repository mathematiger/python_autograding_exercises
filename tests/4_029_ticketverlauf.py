# Automatisch erzeugt aus lehrkraft/muster/4_029_ticketverlauf.py - nicht von Hand ändern.
# vorlage-hash: 646bd06613d50d24
# text-hash: 1d2c18cfa2611af0
# thema: funktionen
# inhalt: functools.reduce

def neuer_start():
    """Frischer Anfangszustand wie im Beispiel."""
    return {"status": "neu", "prioritaet": 3, "bearbeiter": None, "kommentare": ()}


def nachgerechnet(start, ereignisse):
    """Vergleichslösung mit einer Schleife, die eine Kopie Schritt für Schritt verändert."""
    zustand = dict(start)
    kommentare = list(start["kommentare"])
    for feld, wert in ereignisse:
        if feld == "kommentar":
            kommentare.append(wert)
        else:
            zustand[feld] = wert
    zustand["kommentare"] = tuple(kommentare)
    return zustand


def versuche(funktion, *argumente):
    """Ruft funktion auf; liefert das Ergebnis oder eine Beschreibung des Abbruchs."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"(Abbruch: {type(fehler).__name__}: {fehler})"


# anwenden ersetzt den Status
ergebnis = versuche(anwenden, neuer_start(), ("status", "in Arbeit"))
erwartet = {"status": "in Arbeit", "prioritaet": 3, "bearbeiter": None, "kommentare": ()}
assert ergebnis == erwartet, f"anwenden(start, ('status', 'in Arbeit')) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# anwenden ersetzt auch Priorität und Bearbeiter
ergebnis = (versuche(anwenden, neuer_start(), ("prioritaet", 1)), versuche(anwenden, neuer_start(), ("bearbeiter", "Ola")))
erwartet = (
    {"status": "neu", "prioritaet": 1, "bearbeiter": None, "kommentare": ()},
    {"status": "neu", "prioritaet": 3, "bearbeiter": "Ola", "kommentare": ()},
)
assert ergebnis == erwartet, (
    f"anwenden(start, ('prioritaet', 1)) und anwenden(start, ('bearbeiter', 'Ola')) ergeben {ergebnis!r}, "
    f"erwartet war {erwartet!r}."
)

# Ein Kommentar wird an das Tupel kommentare angehängt
zustand = {"status": "neu", "prioritaet": 3, "bearbeiter": None, "kommentare": ("erster",)}
ergebnis = versuche(anwenden, zustand, ("kommentar", "zweiter"))
erwartet = {"status": "neu", "prioritaet": 3, "bearbeiter": None, "kommentare": ("erster", "zweiter")}
assert ergebnis == erwartet, (
    f"anwenden(zustand mit kommentare ('erster',), ('kommentar', 'zweiter')) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Beim Feld 'kommentar' gibt es keinen Schlüssel 'kommentar'; verlängern Sie das Tupel unter 'kommentare'."
)

# anwenden verändert den alten Zustand nicht
zustand = neuer_start()
neu = versuche(anwenden, zustand, ("status", "gelöst"))
neu_kommentar = versuche(anwenden, zustand, ("kommentar", "Notiz"))
assert zustand == neuer_start() and neu is not zustand and neu_kommentar is not zustand, (
    f"Nach anwenden(zustand, ...) ist zustand {zustand!r}, erwartet war der unveränderte Anfangszustand "
    "und ein neues Dictionary als Ergebnis.\nTipp: Legen Sie zuerst mit dict(zustand) eine Kopie an und ändern Sie nur sie."
)

# Das Beispiel aus der Aufgabe: endzustand
start = neuer_start()
ereignisse = [
    ("bearbeiter", "Kim"),
    ("status", "in Arbeit"),
    ("kommentar", "Drucker neu gestartet"),
    ("prioritaet", 2),
    ("status", "gelöst"),
]
ergebnis = versuche(endzustand, start, ereignisse)
erwartet = nachgerechnet(start, ereignisse)
assert ergebnis == erwartet, f"endzustand(start, ereignisse) aus dem Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Nur die ersten beiden Ereignisse
ergebnis = versuche(endzustand, neuer_start(), ereignisse[:2])
erwartet = nachgerechnet(neuer_start(), ereignisse[:2])
assert ergebnis == erwartet, f"endzustand(start, ereignisse[:2]) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Mehrere Kommentare bleiben in ihrer Reihenfolge
kommentare = [("kommentar", "a"), ("status", "warten"), ("kommentar", "b"), ("kommentar", "c")]
ergebnis = versuche(endzustand, neuer_start(), kommentare)
erwartet = nachgerechnet(neuer_start(), kommentare)
assert ergebnis == erwartet, f"endzustand(start, {kommentare!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Ohne Ereignisse kommt der Startzustand heraus
ergebnis = versuche(endzustand, neuer_start(), [])
assert ergebnis == neuer_start(), (
    f"endzustand(start, []) ergibt {ergebnis!r}, erwartet war der Startzustand {neuer_start()!r}.\n"
    "Tipp: Geben Sie reduce den Startwert als drittes Argument mit, sonst scheitert es an der leeren Liste."
)

# endzustand verändert start nicht, und derselbe start geht mehrmals
start = neuer_start()
erster = versuche(endzustand, start, ereignisse)
zweiter = versuche(endzustand, start, ereignisse[:1])
assert start == neuer_start() and zweiter == nachgerechnet(neuer_start(), ereignisse[:1]), (
    f"Nach endzustand(start, ereignisse) ist start {start!r} und endzustand(start, ereignisse[:1]) ergibt "
    f"{zweiter!r}; erwartet waren der unveränderte Start und {nachgerechnet(neuer_start(), ereignisse[:1])!r}."
)

# reduce wird benutzt
assert verwendet("reduce"), "Falten Sie die Ereignisse in endzustand mit functools.reduce zusammen, nicht mit einer Schleife."

# Viele zufällige Ticketverläufe
zufall = Zufall(4029)
for _ in range(300):
    start = {
        "status": zufall.choice(["neu", "in Arbeit"]),
        "prioritaet": zufall.randint(1, 5),
        "bearbeiter": zufall.choice([None, "Kim"]),
        "kommentare": tuple(zufall.choice(["x", "y"]) for _ in range(zufall.randint(0, 2))),
    }
    kopie = dict(start)
    folge = []
    for _ in range(zufall.randint(0, 12)):
        feld = zufall.choice(["status", "prioritaet", "bearbeiter", "kommentar"])
        wert = {
            "status": zufall.choice(["neu", "in Arbeit", "warten", "gelöst"]),
            "prioritaet": zufall.randint(1, 5),
            "bearbeiter": zufall.choice([None, "Kim", "Ola", "Mia"]),
            "kommentar": zufall.choice(["Neustart", "Rückruf", "Ersatzteil bestellt"]),
        }[feld]
        folge.append((feld, wert))
    ergebnis = versuche(endzustand, start, folge)
    erwartet = nachgerechnet(kopie, folge)
    assert ergebnis == erwartet and start == kopie, (
        f"endzustand({kopie!r}, {folge!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}"
        + ("" if start == kopie else f"; außerdem wurde start verändert zu {start!r}") + "."
    )

# Obere Grenze: 10 000 Ereignisse, davon 5000 Kommentare
folge = []
for nummer in range(10000):
    if nummer % 2:
        folge.append(("kommentar", f"Notiz {nummer}"))
    else:
        folge.append(("prioritaet", nummer % 5 + 1))
ergebnis = versuche(endzustand, neuer_start(), folge)
erwartet = nachgerechnet(neuer_start(), folge)
assert ergebnis == erwartet, (
    "endzustand mit 10 000 Ereignissen (abwechselnd Priorität und Kommentar) ergibt nicht das erwartete Ergebnis; "
    f"bekommen: {str(ergebnis)[:200]} …"
)
