# Automatisch erzeugt aus lehrkraft/muster/2_025_dnsanfragen.py - nicht von Hand ändern.
# vorlage-hash: 0b3c3d118b7549e2
# text-hash: 7d57061da188d457
# thema: datenstrukturen
# inhalt: Dictionaries zählen

BEISPIEL = "intranet.firma.de mail.firma.de Intranet.Firma.de x7q.example.org intranet.firma.de"

# zaehle_anfragen zählt die Namen (hier alle schon klein geschrieben)
text = "web.firma.de mail.firma.de web.firma.de"
ergebnis = zaehle_anfragen(text)
assert ergebnis == {"web.firma.de": 2, "mail.firma.de": 1}, (
    f"zaehle_anfragen({text!r}) ergibt {ergebnis!r}, erwartet war {{'web.firma.de': 2, 'mail.firma.de': 1}}.\n"
    "Tipp: Ist ein Name schon im Dictionary, erhöhen Sie seinen Wert um 1, sonst legen Sie ihn mit 1 an."
)

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

# zaehle_anfragen bei einem leeren Mitschnitt und einem nur aus Leerzeichen und Zeilenumbrüchen
for text in ["", "   \n  "]:
    ergebnis = zaehle_anfragen(text)
    assert ergebnis == {}, f"zaehle_anfragen({text!r}) ergibt {ergebnis!r}, erwartet war {{}}."

# haeufige_namen bei einem leeren Mitschnitt und einem nur aus Leerzeichen und Zeilenumbrüchen
for text in ["", "   \n  "]:
    ergebnis = haeufige_namen(text, 1)
    assert ergebnis == [], f"haeufige_namen({text!r}, 1) ergibt {ergebnis!r}, erwartet war []."

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

# haeufige_namen findet die richtigen Namen (die Reihenfolge zählt hier noch nicht)
ergebnis = haeufige_namen("c-1.de b.de A.de b.de a.de a.de", 2)
assert isinstance(ergebnis, list) and sorted(ergebnis) == ["a.de", "b.de"], (
    f"haeufige_namen('c-1.de b.de A.de b.de a.de a.de', 2) ergibt {ergebnis!r}, erwartet waren a.de und b.de.\n"
    "Tipp: Rufen Sie zaehle_anfragen auf und nehmen Sie die Namen, deren Anzahl mindestens so groß ist (>=)."
)

# mindestens zählt mit: genau mindestens Anfragen reichen (die Reihenfolge zählt hier noch nicht)
for grenze, erwartet in [(1, ["a.de", "b.de", "c-1.de"]), (2, ["a.de", "b.de"]), (3, ["a.de"]), (4, [])]:
    ergebnis = haeufige_namen("c-1.de b.de A.de b.de a.de a.de", grenze)
    assert sorted(ergebnis) == erwartet, (
        f"haeufige_namen('c-1.de b.de A.de b.de a.de a.de', {grenze}) ergibt {ergebnis!r}, erwartet waren {erwartet!r}.\n"
        "Tipp: Gesucht sind Namen mit mindestens so vielen Anfragen (>=), nicht mit mehr (>)."
    )

# haeufige_namen gibt die Namen alphabetisch sortiert zurück
ergebnis = haeufige_namen("c-1.de b.de A.de b.de a.de a.de", 1)
assert ergebnis == ["a.de", "b.de", "c-1.de"], (
    f"haeufige_namen('c-1.de b.de A.de b.de a.de a.de', 1) ergibt {ergebnis!r}, erwartet war ['a.de', 'b.de', 'c-1.de'].\n"
    "Tipp: Sortieren Sie die Namen am Ende mit sorted."
)

# zaehle_anfragen bei einem einzelnen Namen, der 100 000-mal kommt
text = " ".join(["Ziel.de"] * 100000)
ergebnis = zaehle_anfragen(text)
assert ergebnis == {"ziel.de": 100000}, (
    f"Bei 100 000-mal 'Ziel.de' ergibt zaehle_anfragen {ergebnis!r}, erwartet war {{'ziel.de': 100000}}."
)

# haeufige_namen bei einem einzelnen Namen, der 100 000-mal kommt (obere Grenze von mindestens)
ergebnis = haeufige_namen(text, 100000)
assert ergebnis == ["ziel.de"], (
    f"Bei 100 000-mal 'Ziel.de' ergibt haeufige_namen(…, 100000) {ergebnis!r}, erwartet war ['ziel.de']."
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


# 300 zufällige Mitschnitte für zaehle_anfragen
zufall = Zufall(2025)
for _ in range(300):
    namen = [zufall.choice(["a.de", "B.de", "b.DE", "mail.x", "MAIL.X", "db-2.y", "q"]) for _ in range(zufall.randint(0, 12))]
    trenner = [zufall.choice([" ", "  ", "\n", " \n "]) for _ in namen]
    text = zufall.choice(["", " ", "\n"]) + "".join(name + trenner[i] for i, name in enumerate(namen))
    grenze = zufall.randint(1, 5)
    erwartet = zaehle_von_hand(text)
    ergebnis = zaehle_anfragen(text)
    assert ergebnis == erwartet, f"zaehle_anfragen({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige Mitschnitte für haeufige_namen
zufall = Zufall(2025)
for _ in range(300):
    namen = [zufall.choice(["a.de", "B.de", "b.DE", "mail.x", "MAIL.X", "db-2.y", "q"]) for _ in range(zufall.randint(0, 12))]
    trenner = [zufall.choice([" ", "  ", "\n", " \n "]) for _ in namen]
    text = zufall.choice(["", " ", "\n"]) + "".join(name + trenner[i] for i, name in enumerate(namen))
    grenze = zufall.randint(1, 5)
    erwartet = zaehle_von_hand(text)
    erwartet = sorted([name for name in erwartet if erwartet[name] >= grenze])
    ergebnis = haeufige_namen(text, grenze)
    assert ergebnis == erwartet, f"haeufige_namen({text!r}, {grenze}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 100 000 Anfragen an 5000 verschiedene Namen
namen = [f"host{(nummer * 7919) % 5000}.firma.de" for nummer in range(100000)]
text = "\n".join(namen)
ergebnis = zaehle_anfragen(text)
erwartet = zaehle_von_hand(text)
assert ergebnis == erwartet, (
    f"Bei 100 000 Anfragen an 5000 Namen liefert zaehle_anfragen {len(ergebnis) if isinstance(ergebnis, dict) else ergebnis!r} Einträge, "
    f"erwartet waren {len(erwartet)} Namen mit je 20 Anfragen.\n"
    "Tipp: Gehen Sie die Namen nur einmal durch; text.count(name) für jeden Namen ist bei so vielen Namen zu langsam."
)

# haeufige_namen an der oberen Grenze: alle Namen erreichen genau die Grenze
ergebnis = haeufige_namen(text, 20)
assert ergebnis == sorted(erwartet), (
    "Bei 100 000 Anfragen an 5000 Namen mit je 20 Anfragen soll haeufige_namen(…, 20) alle 5000 Namen sortiert "
    f"liefern, Ihre Funktion liefert {len(ergebnis)} Namen, die ersten: {ergebnis[:3]!r}."
)

# haeufige_namen an der oberen Grenze: kein Name erreicht die Grenze
ergebnis = haeufige_namen(text, 21)
assert ergebnis == [], (
    "Bei 100 000 Anfragen an 5000 Namen mit je 20 Anfragen soll haeufige_namen(…, 21) die leere Liste liefern, "
    f"Ihre Funktion liefert {len(ergebnis)} Namen, die ersten: {ergebnis[:3]!r}."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = "{'intranet.firma.de': 3, 'mail.firma.de': 1, 'x7q.example.org': 1}\n['intranet.firma.de']"
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
