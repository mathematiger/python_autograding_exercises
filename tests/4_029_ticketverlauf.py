# Automatisch erzeugt aus lehrkraft/muster/4_029_ticketverlauf.py - nicht von Hand ändern.
# vorlage-hash: 46314a65f987f563
# text-hash: fafacb5023b84398
# thema: funktionen
# inhalt: functools.reduce

EREIGNISSE = ["eskalieren", "zurueckstufen", "loesen", "wiedereroeffnen"]


def vergleich_stufe(ereignisse, start):
    """Vergleichslösung mit einer for-Schleife."""
    stufe = start
    for ereignis in ereignisse:
        stufe = wende_an(stufe, ereignis)
    return stufe


def vergleich_summen(zaehlungen):
    """Vergleichslösung mit zwei for-Schleifen."""
    summen = {}
    for zaehlung in zaehlungen:
        for kategorie in zaehlung:
            summen[kategorie] = summen.get(kategorie, 0) + zaehlung[kategorie]
    return summen


def kopie(zaehlungen):
    """Kopiert eine Liste von Dictionaries, um später Veränderungen zu erkennen."""
    return [dict(zaehlung) for zaehlung in zaehlungen]


def aufruf(funktion, *argumente, **schluesselwoerter):
    """Ruft funktion auf; liefert (Ergebnis, None) oder (None, Beschreibung der Ausnahme)."""
    try:
        return funktion(*argumente, **schluesselwoerter), None
    except Exception as fehler:
        return None, f"{type(fehler).__name__}: {fehler}"


# Das Beispiel: zweimal eskalieren, einmal zurückstufen
ergebnis, fehler = aufruf(endstufe, ["eskalieren", "eskalieren", "zurueckstufen"])
assert ergebnis == 2, (
    f'endstufe(["eskalieren", "eskalieren", "zurueckstufen"]) ergibt {ergebnis!r} {fehler or ""}, erwartet war 2.\n'
    "Tipp: reduce(wende_an, ereignisse, start) wendet die Ereignisse der Reihe nach an."
)

# Ein anderer Verlauf mit eigenem Start (nicht fest hinschreiben!)
ergebnis, fehler = aufruf(endstufe, ["loesen", "wiedereroeffnen"], start=3)
assert ergebnis == 1, (
    f'endstufe(["loesen", "wiedereroeffnen"], start=3) ergibt {ergebnis!r} {fehler or ""}, erwartet war 1.'
)

# start wird benutzt
ergebnis, fehler = aufruf(endstufe, ["zurueckstufen"], start=3)
assert ergebnis == 2, (
    f'endstufe(["zurueckstufen"], start=3) ergibt {ergebnis!r} {fehler or ""}, erwartet war 2.\n'
    "Tipp: start ist der Anfangswert, das dritte Argument von reduce."
)

# Ohne Ereignisse kommt start zurück
bekommen = [aufruf(endstufe, [])[0], aufruf(endstufe, [], start=0)[0], aufruf(endstufe, [], 3)[0]]
assert bekommen == [1, 0, 3], (
    f"endstufe([]), endstufe([], start=0) und endstufe([], 3) ergeben {bekommen}, erwartet war [1, 0, 3].\n"
    "Tipp: Ohne Anfangswert bricht reduce bei einer leeren Liste mit einem TypeError ab."
)

# Ein gelöstes Ticket bleibt gelöst, bis es wiedereröffnet wird
ergebnis, fehler = aufruf(endstufe, ["loesen", "eskalieren", "zurueckstufen"], start=2)
assert ergebnis == 0, (
    f'endstufe(["loesen", "eskalieren", "zurueckstufen"], start=2) ergibt {ergebnis!r} {fehler or ""}, erwartet war 0.'
)

# Das Beispiel: zwei Standorte
zaehlungen = [{"Drucker": 4, "Netz": 2}, {"Netz": 5, "Konto": 1}]
ergebnis, fehler = aufruf(zusammenfuehren, zaehlungen)
assert ergebnis == {"Drucker": 4, "Netz": 7, "Konto": 1}, (
    "zusammenfuehren([{'Drucker': 4, 'Netz': 2}, {'Netz': 5, 'Konto': 1}]) ergibt "
    f"{ergebnis!r} {fehler or ''}, erwartet war {{'Drucker': 4, 'Netz': 7, 'Konto': 1}}."
)

# Die Kategorien stehen in der Reihenfolge ihres ersten Vorkommens
ergebnis, fehler = aufruf(zusammenfuehren, [{"Netz": 1}, {"Konto": 2, "Netz": 3}, {"Drucker": 1}])
reihenfolge = list(ergebnis) if isinstance(ergebnis, dict) else ergebnis
assert reihenfolge == ["Netz", "Konto", "Drucker"], (
    "zusammenfuehren([{'Netz': 1}, {'Konto': 2, 'Netz': 3}, {'Drucker': 1}]) hat die Schlüssel "
    f"{reihenfolge!r} {fehler or ''}, erwartet war ['Netz', 'Konto', 'Drucker']."
)

# Drei Standorte (nicht fest hinschreiben!)
zaehlungen = [{"VPN": 3}, {"VPN": 1, "Mail": 2}, {"Mail": 10, "VPN": 6}]
ergebnis, fehler = aufruf(zusammenfuehren, zaehlungen)
assert ergebnis == {"VPN": 10, "Mail": 12}, (
    f"zusammenfuehren({zaehlungen}) ergibt {ergebnis!r} {fehler or ''}, erwartet war {{'VPN': 10, 'Mail': 12}}."
)

# Die übergebenen Dictionaries bleiben unverändert
zaehlungen = [{"Drucker": 4, "Netz": 2}, {"Netz": 5, "Konto": 1}]
vorher = kopie(zaehlungen)
ergebnis, fehler = aufruf(zusammenfuehren, zaehlungen)
assert zaehlungen == vorher and all(ergebnis is not zaehlung for zaehlung in zaehlungen), (
    f"Nach zusammenfuehren({vorher}) sind die Zählungen {zaehlungen}; sie dürfen sich nicht ändern, und das "
    "Ergebnis muss ein neues Dictionary sein.\n"
    "Tipp: Geben Sie reduce ein leeres Dictionary als Anfangswert und kopieren Sie in der Verrechnungsfunktion "
    "mit dict(bisher), bevor Sie addieren."
)

# Eine einzige Zählung: Ergebnis gleich, aber ein neues Dictionary
einzeln = {"Netz": 3}
ergebnis, fehler = aufruf(zusammenfuehren, [einzeln])
assert ergebnis == {"Netz": 3} and ergebnis is not einzeln, (
    f"zusammenfuehren([{{'Netz': 3}}]) ergibt {ergebnis!r} {fehler or ''}; erwartet war ein neues Dictionary "
    "{'Netz': 3}, nicht das übergebene selbst."
)

# Leere Liste und leere Zählungen
bekommen = [aufruf(zusammenfuehren, [])[0], aufruf(zusammenfuehren, [{}, {}])[0], aufruf(zusammenfuehren, [{"Netz": 0}])[0]]
assert bekommen == [{}, {}, {"Netz": 0}], (
    f"zusammenfuehren([]), zusammenfuehren([{{}}, {{}}]) und zusammenfuehren([{{'Netz': 0}}]) ergeben {bekommen}, "
    "erwartet war [{}, {}, {'Netz': 0}].\nTipp: Ohne Anfangswert bricht reduce bei einer leeren Liste ab."
)

# reduce wird benutzt
assert verwendet("reduce"), "Benutzen Sie functools.reduce in endstufe und zusammenfuehren."

# Viele zufällige Verläufe
zufall = Zufall(4029)
for _ in range(300):
    start = zufall.randint(0, 3)
    ereignisse = [zufall.choice(EREIGNISSE) for _ in range(zufall.randint(0, 12))]
    ergebnis, fehler = aufruf(endstufe, ereignisse, start)
    erwartet = vergleich_stufe(ereignisse, start)
    assert ergebnis == erwartet, f"endstufe({ereignisse}, {start}) ergibt {ergebnis!r} {fehler or ''}, erwartet war {erwartet}."

# Viele zufällige Monatszählungen
kategorien = ["Drucker", "Netz", "Konto", "Mail", "VPN", "Telefon"]
for _ in range(300):
    zaehlungen = [
        {kategorie: zufall.randint(0, 20) for kategorie in zufall.sample(kategorien, zufall.randint(0, 4))}
        for _ in range(zufall.randint(0, 5))
    ]
    vorher = kopie(zaehlungen)
    ergebnis, fehler = aufruf(zusammenfuehren, zaehlungen)
    erwartet = vergleich_summen(vorher)
    assert ergebnis == erwartet and list(ergebnis) == list(erwartet) and zaehlungen == vorher, (
        f"zusammenfuehren({vorher}) ergibt {ergebnis!r} {fehler or ''}, erwartet war {erwartet}; "
        f"die Zählungen danach: {zaehlungen}."
    )

# Obere Grenze: 100 000 Ereignisse
ereignisse = [EREIGNISSE[(nummer * 7) % 9 % 4] for nummer in range(100_000)]
ergebnis, fehler = aufruf(endstufe, ereignisse, 2)
assert ergebnis == vergleich_stufe(ereignisse, 2), (
    f"endstufe mit 100 000 Ereignissen ergibt {ergebnis!r} {fehler or ''}, erwartet war {vergleich_stufe(ereignisse, 2)}."
)
# Obere Grenze: 2000 Zählungen mit je 20 Kategorien
grosse = [{f"K{(nummer + spalte) % 50}": 10**6 for spalte in range(20)} for nummer in range(2000)]
ergebnis, fehler = aufruf(zusammenfuehren, grosse)
assert ergebnis == vergleich_summen(grosse), (
    f"zusammenfuehren mit 2000 Zählungen zu je 20 Kategorien ergibt eine falsche Summe {fehler or ''}."
)
