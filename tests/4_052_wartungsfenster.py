# Automatisch erzeugt aus lehrkraft/muster/4_052_wartungsfenster.py - nicht von Hand ändern.
# vorlage-hash: 49319ee0153d6a51
# text-hash: 22f237c76998de0e
# thema: fehler
# inhalt: contextlib.contextmanager

class Testfehler(Exception):
    """Eine Ausnahme, die nur im Test vorkommt."""


def im_block(manager, block):
    """Führt block(wert) im with-Block aus; gibt ("ok", Ergebnis) zurück oder beschreibt die Ausnahme."""
    try:
        with manager as wert:
            ergebnis = block(wert)
    except Testfehler as fehler:
        return ("weitergeflogen", str(fehler))
    except Exception as fehler:
        return (type(fehler).__name__, str(fehler))
    return ("ok", ergebnis)


def scheitert(_):
    """Ein with-Block, der mit einem Testfehler abbricht."""
    raise Testfehler("Update fehlgeschlagen")


def neues_ticket(nummer=4711, bearbeiter=None):
    """Ein Ticket wie im Beispiel."""
    return {"nummer": nummer, "bearbeiter": bearbeiter, "notizen": []}


# wartung im Beispiel: im Block steht "Wartung"
statusseite = {"VPN": "in Betrieb"}
protokoll = []
ergebnis = im_block(wartung(statusseite, "VPN", protokoll), lambda wert: (wert, statusseite["VPN"]))
assert ergebnis == ("ok", (None, "Wartung")), (
    f"Im with-Block von wartung ergibt (as, statusseite['VPN']) {ergebnis!r}, erwartet war ('ok', (None, 'Wartung')).\n"
    "Tipp: Setzen Sie den Status vor dem yield; ein yield ohne Wert liefert None."
)

# wartung im Beispiel: danach steht wieder der alte Status da
assert statusseite == {"VPN": "in Betrieb"}, (
    f"Nach dem with-Block ist statusseite {statusseite!r}, erwartet war {{'VPN': 'in Betrieb'}}.\n"
    "Tipp: Merken Sie sich den alten Status vor dem yield und setzen Sie ihn danach zurück."
)

# wartung im Beispiel: Beginn und Ende im Protokoll
assert protokoll == [("beginn", "VPN"), ("ende", "VPN")], (
    f"Nach dem with-Block ist protokoll {protokoll!r}, erwartet war [('beginn', 'VPN'), ('ende', 'VPN')]."
)

# wartung mit einem anderen Dienst und Status (nicht fest hinschreiben!)
statusseite = {"VPN": "in Betrieb", "E-Mail": "Störung"}
protokoll = [("beginn", "VPN"), ("ende", "VPN")]
ergebnis = im_block(wartung(statusseite, "E-Mail", protokoll), lambda _: dict(statusseite))
assert ergebnis == ("ok", {"VPN": "in Betrieb", "E-Mail": "Wartung"}) and statusseite == {"VPN": "in Betrieb", "E-Mail": "Störung"}, (
    f"wartung für E-Mail ergibt im Block {ergebnis!r} und danach {statusseite!r}; erwartet war im Block nur E-Mail auf 'Wartung', danach 'Störung'."
)
# wartung hängt seine Einträge hinten an das Protokoll an
assert protokoll[2:] == [("beginn", "E-Mail"), ("ende", "E-Mail")], f"protokoll ist {protokoll!r}; die Einträge sollen hinten angehängt werden."

# wartung: ein Dienst, der vorher fehlte, wird danach wieder entfernt
statusseite = {"VPN": "in Betrieb"}
im_block(wartung(statusseite, "Drucker", []), lambda _: None)
assert statusseite == {"VPN": "in Betrieb"}, (
    f"Nach einer Wartung des vorher fehlenden Diensts Drucker ist statusseite {statusseite!r}, erwartet war {{'VPN': 'in Betrieb'}}.\n"
    "Tipp: Merken Sie sich mit in, ob der Dienst vorher da war."
)

# wartung: auch nach einer Ausnahme steht der alte Status wieder da
statusseite = {"VPN": "in Betrieb"}
protokoll = []
ergebnis = im_block(wartung(statusseite, "VPN", protokoll), scheitert)
assert statusseite == {"VPN": "in Betrieb"}, (
    f"Nach einer Ausnahme im Block ist statusseite {statusseite!r}, erwartet war {{'VPN': 'in Betrieb'}}.\n"
    "Tipp: Schreiben Sie yield in ein try und stellen Sie den Status in finally wieder her."
)

# wartung: nach einer Ausnahme steht der Abbruch mit der Meldung im Protokoll
assert protokoll == [("beginn", "VPN"), ("abbruch", "VPN", "Update fehlgeschlagen")], (
    f"Nach einer Ausnahme ist protokoll {protokoll!r}, erwartet war [('beginn', 'VPN'), ('abbruch', 'VPN', 'Update fehlgeschlagen')].\n"
    'Tipp: except Exception as fehler: protokoll.append(("abbruch", dienst, str(fehler))), dann raise.'
)

# wartung: die Ausnahme fliegt weiter
assert ergebnis == ("weitergeflogen", "Update fehlgeschlagen"), (
    f"Die Ausnahme aus dem Block ergibt {ergebnis!r}, erwartet war, dass der Testfehler weiterfliegt.\n"
    "Tipp: Ohne raise im except-Zweig gilt die Ausnahme als verschluckt."
)

# wartung: ein vorher fehlender Dienst wird auch nach einer Ausnahme entfernt
statusseite = {}
im_block(wartung(statusseite, "WLAN", []), scheitert)
assert statusseite == {}, f"Nach einer abgebrochenen Wartung des vorher fehlenden Diensts WLAN ist statusseite {statusseite!r}, erwartet war {{}}."

# wartung verschachtelt: zwei Dienste zugleich
statusseite = {"VPN": "in Betrieb", "E-Mail": "in Betrieb"}
protokoll = []
gesehen = []
with wartung(statusseite, "VPN", protokoll):
    with wartung(statusseite, "E-Mail", protokoll):
        gesehen.append(dict(statusseite))
    gesehen.append(dict(statusseite))
erwartet = [{"VPN": "Wartung", "E-Mail": "Wartung"}, {"VPN": "Wartung", "E-Mail": "in Betrieb"}]
assert gesehen == erwartet and statusseite == {"VPN": "in Betrieb", "E-Mail": "in Betrieb"}, (
    f"Verschachtelt sieht man {gesehen!r} und danach {statusseite!r}; erwartet war {erwartet!r} und danach beide 'in Betrieb'."
)
# wartung verschachtelt: Beginn und Ende im Protokoll von außen nach innen und zurück
assert protokoll == [("beginn", "VPN"), ("beginn", "E-Mail"), ("ende", "E-Mail"), ("ende", "VPN")], f"Verschachtelt ist protokoll {protokoll!r}."

# bearbeitung im Beispiel: im Block ist person Bearbeiter, as bekommt das Ticket
ticket = neues_ticket()
ergebnis = im_block(bearbeitung(ticket, "Kim"), lambda wert: (wert is ticket, ticket["bearbeiter"]))
assert ergebnis == ("ok", (True, "Kim")), (
    f"Im with-Block von bearbeitung ergibt (as ist das Ticket, bearbeiter) {ergebnis!r}, erwartet war ('ok', (True, 'Kim')).\n"
    "Tipp: Tragen Sie person vor dem yield ein und schreiben Sie yield ticket."
)

# bearbeitung im Beispiel: danach ist das Ticket wieder frei
assert ticket["bearbeiter"] is None and ticket["notizen"] == [], (
    f"Nach dem with-Block ist das Ticket {ticket!r}, erwartet war bearbeiter None und keine Notiz."
)

# bearbeitung mit einer anderen Person und einer Notiz (nicht fest hinschreiben!)
ticket = neues_ticket(815)
ergebnis = im_block(bearbeitung(ticket, "Ole"), lambda t: (t["bearbeiter"], t["notizen"].append("Passwort zurückgesetzt")))
assert ergebnis == ("ok", ("Ole", None)) and ticket == {"nummer": 815, "bearbeiter": None, "notizen": ["Passwort zurückgesetzt"]}, (
    f"bearbeitung(ticket, 'Ole') ergibt im Block {ergebnis!r} und danach {ticket!r}."
)

# bearbeitung: ein Ticket in Bearbeitung löst RuntimeError aus
ticket = neues_ticket(bearbeiter="Kim")
ergebnis = im_block(bearbeitung(ticket, "Ole"), lambda _: "Block lief")
assert ergebnis[0] == "RuntimeError", (
    f"bearbeitung(ticket, 'Ole') für ein Ticket, das Kim bearbeitet, ergibt {ergebnis!r}, erwartet war ein RuntimeError.\n"
    "Tipp: Prüfen Sie vor dem yield, ob ticket['bearbeiter'] nicht None ist, und lösen Sie dann den Fehler aus."
)

# bearbeitung: die Meldung nennt die bearbeitende Person, und nichts ändert sich
assert "Kim" in ergebnis[1] and ticket == neues_ticket(bearbeiter="Kim"), (
    f"Die Meldung ist {ergebnis[1]!r} und das Ticket danach {ticket!r}; erwartet war eine Meldung mit Kim und ein unverändertes Ticket.\n"
    "Tipp: Lösen Sie den Fehler vor dem try aus, sonst gibt finally das Ticket frei."
)

# bearbeitung: nach einer Ausnahme eine Notiz, und das Ticket ist frei
ticket = neues_ticket()
ergebnis = im_block(bearbeitung(ticket, "Kim"), scheitert)
assert ticket == {"nummer": 4711, "bearbeiter": None, "notizen": ["Abbruch: Update fehlgeschlagen"]}, (
    f"Nach einer Ausnahme im Block ist das Ticket {ticket!r}, erwartet war bearbeiter None und die Notiz 'Abbruch: Update fehlgeschlagen'."
)
# bearbeitung: die Ausnahme fliegt weiter
assert ergebnis == ("weitergeflogen", "Update fehlgeschlagen"), f"Die Ausnahme aus dem Block ergibt {ergebnis!r}, erwartet war, dass sie weiterfliegt."

# bearbeitung: nach dem Block kann die nächste Person übernehmen
ticket = neues_ticket()
ergebnisse = [im_block(bearbeitung(ticket, "Kim"), lambda t: t["bearbeiter"]), im_block(bearbeitung(ticket, "Ole"), lambda t: t["bearbeiter"])]
assert ergebnisse == [("ok", "Kim"), ("ok", "Ole")], f"Zwei Bearbeitungen nacheinander ergeben {ergebnisse!r}, erwartet war [('ok', 'Kim'), ('ok', 'Ole')]."

# Beide zusammen: ein Ticket während einer Wartung, die abbricht
statusseite = {"Drucker": "Störung"}
protokoll = []
ticket = neues_ticket(99)
try:
    with wartung(statusseite, "Drucker", protokoll), bearbeitung(ticket, "Kim"):
        raise Testfehler("Toner fehlt")
except Testfehler:
    pass
assert (statusseite, protokoll[-1], ticket["bearbeiter"], ticket["notizen"]) == (
    {"Drucker": "Störung"},
    ("abbruch", "Drucker", "Toner fehlt"),
    None,
    ["Abbruch: Toner fehlt"],
), f"Nach einer abgebrochenen Wartung mit Ticket ist statusseite {statusseite!r}, protokoll {protokoll!r}, ticket {ticket!r}."

# Die Ausgabe des Programms
erwartet = (
    "Wartung\n{'VPN': 'in Betrieb'}\n[('beginn', 'VPN'), ('ende', 'VPN')]\nKim\n"
    "{'nummer': 4711, 'bearbeiter': None, 'notizen': ['Drucker neu gestartet']}"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Statusseiten und Wartungen
zufall = Zufall(4052)
dienste = ["VPN", "E-Mail", "Drucker", "WLAN", "Wiki", "Telefonie"]
for runde in range(300):
    statusseite = {name: zufall.choice(["in Betrieb", "Störung", "eingeschränkt"]) for name in zufall.sample(dienste, zufall.randint(0, 6))}
    vorher = dict(statusseite)
    dienst = zufall.choice(dienste)
    protokoll = []
    fehlschlag = runde % 3 == 0
    ergebnis = im_block(wartung(statusseite, dienst, protokoll), scheitert if fehlschlag else (lambda _: statusseite.get(dienst)))
    ende = ("abbruch", dienst, "Update fehlgeschlagen") if fehlschlag else ("ende", dienst)
    erwartet = ("weitergeflogen", "Update fehlgeschlagen") if fehlschlag else ("ok", "Wartung")
    assert (ergebnis, statusseite, protokoll) == (erwartet, vorher, [("beginn", dienst), ende]), (
        f"wartung({vorher}, {dienst!r}, []) {'mit' if fehlschlag else 'ohne'} Fehler ergibt {ergebnis!r}, danach {statusseite!r} und {protokoll!r}."
    )

# Obere Grenze: 1000 Dienste, jeder einmal gewartet
statusseite = {f"dienst{nummer}": "in Betrieb" for nummer in range(1000)}
protokoll = []
for nummer in range(1000):
    im_block(wartung(statusseite, f"dienst{nummer}", protokoll), scheitert if nummer % 2 else (lambda _: None))
assert statusseite == {f"dienst{nummer}": "in Betrieb" for nummer in range(1000)} and len(protokoll) == 2000, (
    "Nach 1000 Wartungen stimmt die Statusseite oder das Protokoll nicht."
)
