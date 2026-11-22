# Automatisch erzeugt aus lehrkraft/muster/2_049_caesar.py - nicht von Hand ändern.
# vorlage-hash: 113d5a0c18cd63fa
# text-hash: 24697e81e11a3b5b
# thema: texte_zahlen
# inhalt: Cäsar mit ord und chr

import string


def ergebnis_von(text, schluessel):
    """Ruft verschluesseln auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return verschluesseln(text, schluessel)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich(text, schluessel):
    """Vergleichslösung mit einer Übersetzungstabelle statt ord und chr."""
    klein = string.ascii_lowercase
    gross = string.ascii_uppercase
    verschiebung = schluessel % 26
    tabelle = str.maketrans(klein + gross, klein[verschiebung:] + klein[:verschiebung] + gross[verschiebung:] + gross[:verschiebung])
    return text.translate(tabelle)


def pruefe(text, schluessel, tipp=""):
    """Vergleicht verschluesseln(text, schluessel) mit der Vergleichslösung; gibt die Meldung zurück oder ""."""
    ergebnis = ergebnis_von(text, schluessel)
    erwartet = vergleich(text, schluessel)
    if ergebnis == erwartet:
        return ""
    return f"verschluesseln({text!r}, {schluessel}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.{tipp}"


# Ein Großbuchstabe wird verschoben
meldung = pruefe("A", 3, "\nTipp: chr(ord(\"A\") + 3) ist \"D\"." + (
    "\nIhre Funktion gibt nichts zurück; fehlt das return?" if ergebnis_von("A", 3) is None else ""
))
assert meldung == "", meldung

# Mehrere Großbuchstaben mit einem anderen Schlüssel (nicht fest hinschreiben!)
meldung = pruefe("HALLO", 5)
assert meldung == "", meldung

# Kleinbuchstaben bleiben klein
meldung = pruefe("abc", 2, '\nTipp: Bei Kleinbuchstaben ist ord("a") der Anfang, nicht ord("A").')
assert meldung == "", meldung

# Nach Z geht es wieder bei A los
meldung = pruefe("XYZ xyz", 3, "\nTipp: Rechnen Sie die Position im Alphabet aus und nehmen Sie sie % 26.")
assert meldung == "", meldung

# Leerzeichen, Ziffern und Satzzeichen bleiben stehen
meldung = pruefe("Angriff um 9 Uhr!", 3, "\nTipp: Verschieben Sie nur Zeichen von A bis Z und von a bis z.")
assert meldung == "", meldung

# Entschlüsseln mit negativem Schlüssel
meldung = pruefe("Dqjulii xp 9 Xku!", -3, "\nTipp: (0 - 3) % 26 ist 23, % funktioniert auch bei negativen Zahlen.")
assert meldung == "", meldung

# Umlaute und ß bleiben unverändert, auch große Umlaute
meldung = pruefe("Grüße aus Köln, ÄÖÜ", 1, '\nTipp: isalpha() und isupper() sind auch für ü, ß und Ö wahr; prüfen Sie "a" <= zeichen <= "z".')
assert meldung == "", meldung

# Zeichen direkt neben den Buchstabenbereichen bleiben unverändert: @ [ ` {
meldung = pruefe("@[`{ A Z a z", 1, "\nTipp: Die Grenzen gehören dazu: A und Z, a und z werden verschoben, @ [ ` { nicht.")
assert meldung == "", meldung

# Schlüssel 0 und 26 ändern nichts, Schlüssel 27 wirkt wie 1
for schluessel in [0, 26, 27]:
    meldung = pruefe("Server Rack 7", schluessel)
    assert meldung == "", meldung

# Große Schlüssel an den Grenzen
for schluessel in [1000, -1000, 999, -999]:
    meldung = pruefe("Zugang Alpha zulu", schluessel)
    assert meldung == "", meldung

# Leerer Text
ergebnis = ergebnis_von("", 5)
assert ergebnis == "", f'verschluesseln("", 5) ergibt {ergebnis!r}, erwartet war "".'

# Hin und zurück ergibt wieder den Ausgangstext
geheim = ergebnis_von("Passwort ist Sommer2024!", 11)
zurueck = ergebnis_von(geheim, -11) if isinstance(geheim, str) else geheim
assert zurueck == "Passwort ist Sommer2024!", (
    f'Hin mit 11 und zurück mit -11 ergibt {zurueck!r}, erwartet war "Passwort ist Sommer2024!".'
)

# Die Ausgabe des Programms
erwartet = "Dqjulii xp 9 Xku!\nAngriff um 9 Uhr!"
assert AUSGABE == erwartet, f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Texte und Schlüssel
zufall = Zufall(2049)
zeichenvorrat = string.ascii_letters + string.digits + " .,;:!?-@[]`{}äöüÄÖÜß\n"
for _ in range(400):
    text = "".join(zufall.choice(zeichenvorrat) for _ in range(zufall.randint(0, 15)))
    meldung = pruefe(text, zufall.randint(-1000, 1000))
    assert meldung == "", meldung

# Obere Grenze: 100 000 Zeichen
text = "".join(zufall.choice(zeichenvorrat) for _ in range(100000))
schluessel = zufall.randint(-1000, 1000)
ergebnis = ergebnis_von(text, schluessel)
erwartet = vergleich(text, schluessel)
assert ergebnis == erwartet, (
    f"Bei 100 000 Zeichen und Schlüssel {schluessel} stimmt das Ergebnis nicht; erste Abweichung an Stelle "
    f"{next((i for i, (a, b) in enumerate(zip(ergebnis, erwartet)) if a != b), min(len(ergebnis), len(erwartet)))}."
)
