# Automatisch erzeugt aus lehrkraft/muster/2_025_dnsanfragen.py - nicht von Hand ändern.
# vorlage-hash: 0b3c3d118b7549e2
# text-hash: 7d57061da188d457
# thema: datenstrukturen
# inhalt: Dictionaries zählen

BEISPIEL = "intranet.firma.de mail.firma.de Intranet.Firma.de x7q.example.org intranet.firma.de"

# zaehle_anfragen aus dem Beispiel
ergebnis = zaehle_anfragen(BEISPIEL)
erwartet = {"intranet.firma.de": 3, "mail.firma.de": 1, "x7q.example.org": 1}
if isinstance(ergebnis, dict) and "Intranet.Firma.de" in ergebnis:
    hinweis = "\nTipp: Groß- und Kleinschreibung zählt nicht; wandeln Sie die Namen mit lower() in Kleinbuchstaben um."
else:
    hinweis = ""
assert ergebnis == erwartet, f"zaehle_anfragen(mitschnitt) aus dem Beispiel ergibt {ergebnis!r}, erwartet war {erwartet!r}.{hinweis}"

# haeufige_namen aus dem Beispiel
ergebnis = haeufige_namen(BEISPIEL, 2)
assert ergebnis == ["intranet.firma.de"], (
    f"haeufige_namen(mitschnitt, 2) aus dem Beispiel ergibt {ergebnis!r}, erwartet war ['intranet.firma.de']."
)

# Ein leerer Mitschnitt und einer nur aus Leerzeichen und Zeilenumbrüchen
for text in ["", "   \n  "]:
    ergebnis = (zaehle_anfragen(text), haeufige_namen(text, 1))
    assert ergebnis == ({}, []), f"zaehle_anfragen({text!r}) und haeufige_namen({text!r}, 1) ergeben {ergebnis!r}, erwartet war ({{}}, [])."

# Mehrere Leerzeichen und Zeilenumbrüche als Trenner, auch am Anfang und Ende
text = "  web.firma.de\n\nweb.firma.de   db.firma.de \n"
ergebnis = zaehle_anfragen(text)
assert ergebnis == {"web.firma.de": 2, "db.firma.de": 1}, (
    f"zaehle_anfragen({text!r}) ergibt {ergebnis!r}, erwartet war {{'web.firma.de': 2, 'db.firma.de': 1}}.\n"
    "Tipp: split() ohne Argument trennt an beliebig vielen Leerzeichen und Zeilenumbrüchen; split(' ') nicht."
)

# Andere Namen (nicht fest hinschreiben!) und gemischte Schreibweise
text = "A.de b.de B.DE a.DE c-1.de A.de"
ergebnis = zaehle_anfragen(text)
assert ergebnis == {"a.de": 3, "b.de": 2, "c-1.de": 1}, (
    f"zaehle_anfragen({text!r}) ergibt {ergebnis!r}, erwartet war {{'a.de': 3, 'b.de': 2, 'c-1.de': 1}}."
)

# mindestens zählt mit: genau mindestens Anfragen reichen, und das Ergebnis ist alphabetisch sortiert
for grenze, erwartet in [(1, ["a.de", "b.de", "c-1.de"]), (2, ["a.de", "b.de"]), (3, ["a.de"]), (4, [])]:
    ergebnis = haeufige_namen("c-1.de b.de A.de b.de a.de a.de", grenze)
    assert ergebnis == erwartet, (
        f"haeufige_namen('c-1.de b.de A.de b.de a.de a.de', {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Gesucht sind Namen mit mindestens so vielen Anfragen (>=), alphabetisch sortiert mit sorted."
    )

# Ein einzelner Name, der 100 000-mal kommt (obere Grenze von mindestens)
text = " ".join(["Ziel.de"] * 100000)
ergebnis = (zaehle_anfragen(text), haeufige_namen(text, 100000))
assert ergebnis == ({"ziel.de": 100000}, ["ziel.de"]), (
    "Bei 100 000-mal 'Ziel.de' erwartet ({'ziel.de': 100000}, ['ziel.de']) für zaehle_anfragen und "
    f"haeufige_namen(…, 100000), bekommen: {ergebnis!r}"
)


# Vergleichslösung: sortieren und gleiche Nachbarn zusammenfassen
def zaehle_von_hand(text):
    """Zählt über eine sortierte Liste der Namen, ohne in zu benutzen."""
    namen = sorted(text.lower().split())
    ergebnis = {}
    anfang = 0
    for index in range(1, len(namen) + 1):
        if index == len(namen) or namen[index] != namen[anfang]:
            ergebnis[namen[anfang]] = index - anfang
            anfang = index
    return ergebnis


# 300 zufällige Mitschnitte
zufall = Zufall(2025)
for _ in range(300):
    namen = [zufall.choice(["a.de", "B.de", "b.DE", "mail.x", "MAIL.X", "db-2.y", "q"]) for _ in range(zufall.randint(0, 12))]
    trenner = [zufall.choice([" ", "  ", "\n", " \n "]) for _ in namen]
    text = zufall.choice(["", " ", "\n"]) + "".join(name + trenner[i] for i, name in enumerate(namen))
    grenze = zufall.randint(1, 5)
    erwartet = zaehle_von_hand(text)
    ergebnis = zaehle_anfragen(text)
    assert ergebnis == erwartet, f"zaehle_anfragen({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."
    erwartet = sorted([name for name in erwartet if erwartet[name] >= grenze])
    ergebnis = haeufige_namen(text, grenze)
    assert ergebnis == erwartet, f"haeufige_namen({text!r}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 000 Anfragen an 5000 verschiedene Namen
namen = [f"host{(nummer * 7919) % 5000}.firma.de" for nummer in range(100000)]
text = "\n".join(namen)
ergebnis = zaehle_anfragen(text)
erwartet = zaehle_von_hand(text)
assert ergebnis == erwartet, (
    f"Bei 100 000 Anfragen an 5000 Namen liefert zaehle_anfragen {len(ergebnis)} Einträge, "
    f"erwartet waren {len(erwartet)} Namen mit je 20 Anfragen.\n"
    "Tipp: Gehen Sie die Namen nur einmal durch; text.count(name) für jeden Namen ist bei so vielen Namen zu langsam."
)

# haeufige_namen an der oberen Grenze
assert haeufige_namen(text, 20) == sorted(erwartet) and haeufige_namen(text, 21) == [], (
    "Bei 100 000 Anfragen an 5000 Namen mit je 20 Anfragen soll haeufige_namen(…, 20) alle 5000 Namen sortiert "
    "liefern und haeufige_namen(…, 21) die leere Liste."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{'intranet.firma.de': 3, 'mail.firma.de': 1, 'x7q.example.org': 1}\n['intranet.firma.de']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
