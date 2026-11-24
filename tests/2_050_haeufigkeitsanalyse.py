# Automatisch erzeugt aus lehrkraft/muster/2_050_haeufigkeitsanalyse.py - nicht von Hand ändern.
# vorlage-hash: 9f3b2b7b0e06c67f
# text-hash: 084967dcdbc64b16
# thema: algorithmen
# inhalt: Cäsar knacken

WOERTER = (
    "der die das eine einer ein ist sind werden wurde neue neuen fehler meldung server kunde kunden "
    "lieferung termin bestellung erledigt wieder geprueft bitte ersetzen netzteil wechsel rechner leere "
    "liste test zentrale benutzer wegen gesendet erneut kommentar"
).split()


def ergebnis_von(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def vergleich_haeufigkeiten(text):
    """Vergleichslösung: zählt jeden Buchstaben mit count."""
    klein = text.lower()
    return [klein.count(chr(ord("a") + stelle)) for stelle in range(26)]


def vergleich_schluessel(text):
    """Vergleichslösung: probiert alle Buchstaben der Reihe nach und merkt sich den ersten häufigsten."""
    zaehler = vergleich_haeufigkeiten(text)
    if sum(zaehler) == 0:
        return 0
    bester = 0
    for stelle in range(26):
        if zaehler[stelle] > zaehler[bester]:
            bester = stelle
    return (bester - 4) % 26


def deutscher_text(zufall, anzahl_woerter):
    """Ein zufälliger Text aus deutschen Wörtern, in dem e echt häufiger ist als jeder andere Buchstabe."""
    while True:
        woerter = [zufall.choice(WOERTER) for _ in range(anzahl_woerter)]
        woerter = [wort.capitalize() if zufall.random() < 0.3 else wort for wort in woerter]
        text = " ".join(woerter) + zufall.choice([".", "!", " 42.", ""])
        zaehler = vergleich_haeufigkeiten(text)
        if all(zaehler[4] > anzahl for stelle, anzahl in enumerate(zaehler) if stelle != 4):
            return text


# haeufigkeiten gibt eine Liste mit 26 Zählern zurück
ergebnis = ergebnis_von(haeufigkeiten, "abba")
assert isinstance(ergebnis, list) and len(ergebnis) == 26, (
    f'haeufigkeiten("abba") ergibt {ergebnis!r}, erwartet war eine Liste mit 26 Zahlen.\n'
    "Tipp: [0] * 26 legt eine Liste mit 26 Nullen an."
)

# haeufigkeiten zählt die Kleinbuchstaben
ergebnis = ergebnis_von(haeufigkeiten, "abba zz")
erwartet = vergleich_haeufigkeiten("abba zz")
assert ergebnis == erwartet, (
    f'haeufigkeiten("abba zz") ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    'Tipp: Die Stelle eines Buchstabens ist ord(zeichen) - ord("a").'
)

# haeufigkeiten zählt Großbuchstaben mit und ignoriert andere Zeichen
ergebnis = ergebnis_von(haeufigkeiten, "Abba! ÄÖÜ ß 123")
erwartet = vergleich_haeufigkeiten("Abba! ÄÖÜ ß 123")
assert ergebnis == erwartet, (
    f'haeufigkeiten("Abba! ÄÖÜ ß 123") ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n'
    "Tipp: Machen Sie den Buchstaben mit lower() klein und zählen Sie nur Zeichen von a bis z."
)

# haeufigkeiten eines leeren Texts
ergebnis = ergebnis_von(haeufigkeiten, "")
assert ergebnis == [0] * 26, f'haeufigkeiten("") ergibt {ergebnis!r}, erwartet waren 26 Nullen.'

# schluessel_schaetzen im Beispiel
ergebnis = ergebnis_von(schluessel_schaetzen, "Hlq Ohhuhu Whvw")
assert ergebnis == 3, (
    f'schluessel_schaetzen("Hlq Ohhuhu Whvw") ergibt {ergebnis!r}, erwartet war 3 (h ist am häufigsten, e + 3 = h).'
)

# schluessel_schaetzen mit einem anderen häufigsten Buchstaben (nicht fest hinschreiben!)
ergebnis = ergebnis_von(schluessel_schaetzen, "kkkk xy")
assert ergebnis == 6, f'schluessel_schaetzen("kkkk xy") ergibt {ergebnis!r}, erwartet war 6 (e + 6 = k).'

# schluessel_schaetzen liegt zwischen 0 und 25, auch wenn der häufigste Buchstabe vor e liegt
ergebnis = ergebnis_von(schluessel_schaetzen, "bbb c")
assert ergebnis == 23, (
    f'schluessel_schaetzen("bbb c") ergibt {ergebnis!r}, erwartet war 23 (von e 23 Stellen vorwärts zu b).\n'
    "Tipp: Nehmen Sie die Differenz % 26, dann wird aus -3 die Zahl 23."
)

# schluessel_schaetzen: e am häufigsten heißt Schlüssel 0
ergebnis = ergebnis_von(schluessel_schaetzen, "Eeee")
assert ergebnis == 0, f'schluessel_schaetzen("Eeee") ergibt {ergebnis!r}, erwartet war 0.'

# schluessel_schaetzen bei Gleichstand: der Buchstabe, der im Alphabet zuerst kommt
ergebnis = ergebnis_von(schluessel_schaetzen, "zz mm a b")
assert ergebnis == 8, (
    f'schluessel_schaetzen("zz mm a b") ergibt {ergebnis!r}, erwartet war 8 (m und z sind gleich häufig, m kommt zuerst).\n'
    "Tipp: Ersetzen Sie den bisher häufigsten nur bei einer echt größeren Zahl, oder nehmen Sie index(max(...))."
)

# schluessel_schaetzen ohne Buchstaben
ergebnis = [ergebnis_von(schluessel_schaetzen, ""), ergebnis_von(schluessel_schaetzen, "123 !?")]
assert ergebnis == [0, 0], f'schluessel_schaetzen("") und schluessel_schaetzen("123 !?") ergeben {ergebnis!r}, erwartet war [0, 0].'

# knacken im Beispiel
ergebnis = ergebnis_von(knacken, "Hlq Ohhuhu Whvw")
assert ergebnis == "Ein Leerer Test", f'knacken("Hlq Ohhuhu Whvw") ergibt {ergebnis!r}, erwartet war "Ein Leerer Test".'

# knacken mit einem anderen Schlüssel (nicht fest hinschreiben!)
klar = "Der Server meldet erneut einen Fehler beim Netzteil."
geheim = verschiebe(klar, 17)
ergebnis = ergebnis_von(knacken, geheim)
assert ergebnis == klar, (
    f"knacken({geheim!r}) ergibt {ergebnis!r}, erwartet war {klar!r}.\n"
    "Tipp: Entschlüsselt wird mit dem negativen Schlüssel: verschiebe(text, -schluessel)."
)

# knacken eines Texts ohne Buchstaben lässt ihn unverändert
ergebnis = ergebnis_von(knacken, "2024-11-22 ?!")
assert ergebnis == "2024-11-22 ?!", f'knacken("2024-11-22 ?!") ergibt {ergebnis!r}, erwartet war "2024-11-22 ?!".'

# Die Ausgabe des Programms
erwartet = "3\nEin Leerer Test"
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# haeufigkeiten: viele zufällige Texte aus beliebigen Zeichen
zufall = Zufall(2050)
texte = []
for _ in range(300):
    texte.append("".join(zufall.choice("abcdeXYZ e!? 7äß") for _ in range(zufall.randint(0, 12))))
for text in texte:
    ergebnis = ergebnis_von(haeufigkeiten, text)
    erwartet = vergleich_haeufigkeiten(text)
    assert ergebnis == erwartet, f"haeufigkeiten({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# schluessel_schaetzen: dieselben zufälligen Texte
for text in texte:
    ergebnis = ergebnis_von(schluessel_schaetzen, text)
    erwartet = vergleich_schluessel(text)
    assert ergebnis == erwartet, f"schluessel_schaetzen({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Viele zufällige deutsche Texte mit zufälligem Schlüssel werden geknackt
for _ in range(200):
    klar = deutscher_text(zufall, zufall.randint(3, 12))
    schluessel = zufall.randint(0, 25)
    geheim = verschiebe(klar, schluessel)
    ergebnis = [ergebnis_von(schluessel_schaetzen, geheim), ergebnis_von(knacken, geheim)]
    assert ergebnis == [schluessel, klar], (
        f"Für {geheim!r} ergeben schluessel_schaetzen und knacken {ergebnis!r}, erwartet war [{schluessel}, {klar!r}]."
    )

# Obere Grenze: 100 000 Zeichen
klar = deutscher_text(zufall, 12000)[:100000]
geheim = verschiebe(klar, 11)
ergebnis = ergebnis_von(knacken, geheim)
assert ergebnis == klar, f"Bei einem Text mit {len(geheim)} Zeichen und Schlüssel 11 ergibt knacken nicht den Klartext."

# Laufzeit: haeufigkeiten geht den Text nur einmal durch
klar = deutscher_text(zufall, 2500)[:20000]
ergebnis, schritte = zaehle_schritte(haeufigkeiten, klar)
assert schritte < 200_000, (
    f"haeufigkeiten braucht bei {len(klar)} Zeichen {schritte} Programmschritte; erwartet waren deutlich weniger als 200 000.\n"
    "Tipp: Gehen Sie den Text in haeufigkeiten nur einmal durch, nicht einmal für jeden Buchstaben."
)
