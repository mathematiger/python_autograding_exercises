# Automatisch erzeugt aus lehrkraft/muster/2_006_warteschlange.py - nicht von Hand ändern.
# vorlage-hash: 26d2857dce999e39
# text-hash: e18dc639a5d77e4a
# thema: datenstrukturen
# inhalt: Listen und for über eine Liste

# Das Beispiel aus der Aufgabe
ergebnis = ueberfaellig([95, 40, 61, 12], 60)
assert ergebnis == 2, (
    f"ueberfaellig([95, 40, 61, 12], 60) ergibt {ergebnis!r}, erwartet war 2 (95 und 61 warten länger als 60)."
)

# Weitere Warteschlangen (nicht fest 2 hinschreiben!)
for wartezeiten, frist, erwartet in [
    ([10, 20, 30], 5, 3),
    ([10, 20, 30], 25, 1),
    ([120], 30, 1),
    ([5, 500, 5, 500, 5], 100, 2),
]:
    ergebnis = ueberfaellig(wartezeiten, frist)
    assert ergebnis == erwartet, f"ueberfaellig({wartezeiten}, {frist}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Genau die Frist ist noch nicht überfällig
ergebnis = ueberfaellig([60, 59], 60)
assert ergebnis == 0, (
    f"ueberfaellig([60, 59], 60) ergibt {ergebnis!r}, erwartet war 0.\n"
    "Tipp: Überfällig ist nur, wer länger als die Frist wartet; vergleichen Sie mit > statt mit >=."
)

# Auch das letzte Ticket der Liste zählt mit
ergebnis = ueberfaellig([1, 2, 300], 60)
assert ergebnis == 1, (
    f"ueberfaellig([1, 2, 300], 60) ergibt {ergebnis!r}, erwartet war 1.\n"
    "Tipp: for wartezeit in wartezeiten geht alle Elemente bis zum letzten durch."
)

# Eine leere Warteschlange hat kein überfälliges Ticket
ergebnis = ueberfaellig([], 60)
assert ergebnis == 0, f"ueberfaellig([], 60) ergibt {ergebnis!r}, erwartet war 0."

# Frist 0: jedes Ticket, das überhaupt wartet, ist überfällig
ergebnis = ueberfaellig([0, 1, 0, 7], 0)
assert ergebnis == 2, f"ueberfaellig([0, 1, 0, 7], 0) ergibt {ergebnis!r}, erwartet war 2."

# Eine for-Schleife wird benutzt
assert verwendet("for"), "Gehen Sie die Wartezeiten mit einer for-Schleife durch."

# Die Ausgabe des Programms stimmt
erwartet = "Offene Tickets: 4\nÄltestes Ticket wartet seit 95 Minuten\nÜberfällig: 2"
assert AUSGABE == erwartet, f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm gibt aus:\n{AUSGABE}"

# Viele zufällige Warteschlangen
zufall = Zufall(2006)
for _ in range(500):
    frist = zufall.randint(0, 100)
    # Wartezeiten nahe an der Frist, damit die Grenze oft getroffen wird
    wartezeiten = [zufall.randint(0, 2 * frist + 2) for _ in range(zufall.randint(0, 10))]
    # Vergleichsrechnung: die nicht überfälligen abziehen
    erwartet = len(wartezeiten) - len([zeit for zeit in wartezeiten if zeit <= frist])
    ergebnis = ueberfaellig(wartezeiten, frist)
    assert ergebnis == erwartet, f"ueberfaellig({wartezeiten}, {frist}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# An der oberen Grenze: 10 000 Tickets
for wartezeiten, frist, erwartet in [
    ([10**6] * 10_000, 0, 10_000),
    ([10**6] * 10_000, 10**6, 0),
    ([0, 10**6] * 5000, 999_999, 5000),
]:
    ergebnis = ueberfaellig(wartezeiten, frist)
    assert ergebnis == erwartet, (
        f"Bei 10 000 Tickets, beginnend mit {wartezeiten[:2]}, und frist {frist} ergibt ueberfaellig "
        f"{ergebnis!r}, erwartet war {erwartet}."
    )
