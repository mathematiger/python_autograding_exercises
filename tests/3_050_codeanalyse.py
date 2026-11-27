# Automatisch erzeugt aus lehrkraft/muster/3_050_codeanalyse.py - nicht von Hand ändern.
# vorlage-hash: f767f64527c2bc59
# text-hash: c1828d86e7c5174b
# thema: texte_zahlen
# inhalt: CSV von Hand, Summen je Spalte

BEISPIEL = "modul,stil,fehler,sicherheit\nlogin.py,12,0,1\nkasse.py,3,2,0\nbericht.py,0,0,0\n"


def aufruf(funktion, *argumente):
    """Ruft die Funktion auf; ein Fehler wird als Text zurückgegeben."""
    try:
        return funktion(*argumente)
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def tabelle(text):
    """Vergleichslösung: zerlegt den Text in Kopf und Datenzeilen (als Listen von Feldern)."""
    zeilen = [zeile for zeile in text.split("\n") if zeile.strip() != ""]
    kopf = zeilen[0].split(",")
    daten = [zeile.split(",") for zeile in zeilen[1:]]
    return kopf, daten


def vergleich_summen(text):
    """Vergleichslösung: summiert Spalte für Spalte über ihre Stelle."""
    kopf, daten = tabelle(text)
    summen = {}
    for stelle in range(1, len(kopf)):
        summen[kopf[stelle]] = sum(int(felder[stelle]) for felder in daten)
    return summen


def vergleich_summenzeile(text):
    """Vergleichslösung für mit_summenzeile."""
    zeilen = [zeile for zeile in text.split("\n") if zeile.strip() != ""]
    summen = [str(summe) for summe in vergleich_summen(text).values()]
    return "\n".join(zeilen + ["gesamt," + ",".join(summen)]) + "\n"


def vergleich_auffaellige(text, spalte, grenze):
    """Vergleichslösung für auffaellige_module."""
    kopf, daten = tabelle(text)
    stelle = kopf.index(spalte)
    return [felder[0] for felder in daten if int(felder[stelle]) >= grenze]


def meldung(aufruf_text, text, ergebnis, erwartet, tipp=""):
    """Fehlermeldung mit dem CSV-Text, dem Ergebnis und dem erwarteten Wert."""
    gezeigt = text if len(text) <= 500 else text[:500] + " …"
    return f"Für den Text\n{gezeigt!r}\nergibt {aufruf_text} {ergebnis!r},\nerwartet war {erwartet!r}.{tipp}"


# spaltensummen im Beispiel: die Schlüssel sind die Spalten außer modul
ergebnis = aufruf(spaltensummen, BEISPIEL)
assert isinstance(ergebnis, dict) and list(ergebnis) == ["stil", "fehler", "sicherheit"], meldung(
    "spaltensummen(text)", BEISPIEL, ergebnis, vergleich_summen(BEISPIEL),
    '\nTipp: Zerlegen Sie die erste Zeile mit split(","); die Namen ab der zweiten Stelle sind die Schlüssel.',
)

# spaltensummen im Beispiel: die Summen
assert ergebnis == vergleich_summen(BEISPIEL), meldung(
    "spaltensummen(text)", BEISPIEL, ergebnis, vergleich_summen(BEISPIEL),
    "\nTipp: Zerlegen Sie jede weitere Zeile und addieren Sie int(wert) zur Summe der passenden Spalte.",
)

# spaltensummen mit anderen Spalten (nicht fest hinschreiben!)
text = "datei,warnungen,todo\napi.py,7,1\ndb.py,5,4"
ergebnis = aufruf(spaltensummen, text)
assert ergebnis == vergleich_summen(text), meldung(
    "spaltensummen(text)", text, ergebnis, vergleich_summen(text), "\nTipp: Die Spalten stehen nur in der Kopfzeile, nicht fest im Code."
)

# spaltensummen: Leerzeichen um die Zahlen und leere Zeilen
text = "modul,stil,fehler\n\nlogin.py, 4 ,1\n   \nkasse.py,10, 0\n\n"
ergebnis = aufruf(spaltensummen, text)
assert ergebnis == vergleich_summen(text), meldung(
    "spaltensummen(text)", text, ergebnis, vergleich_summen(text), '\nTipp: Überspringen Sie Zeilen, für die zeile.strip() == "" ist.'
)

# spaltensummen: nur die Kopfzeile, alle Summen 0
text = "modul,stil,fehler,sicherheit\n"
ergebnis = aufruf(spaltensummen, text)
assert ergebnis == vergleich_summen(text), meldung("spaltensummen(text)", text, ergebnis, vergleich_summen(text))

# spaltensummen: nur eine Zahlenspalte und große Werte
text = "modul,fehler\na.py,100000\nb.py,99999"
ergebnis = aufruf(spaltensummen, text)
assert ergebnis == vergleich_summen(text), meldung("spaltensummen(text)", text, ergebnis, vergleich_summen(text))

# mit_summenzeile im Beispiel: die letzte Zeile enthält gesamt und die Summen
ergebnis = aufruf(mit_summenzeile, BEISPIEL)
letzte = ergebnis.strip().splitlines()[-1] if isinstance(ergebnis, str) and ergebnis.strip() else ""
assert vergleichbar(letzte) == vergleichbar("gesamt,15,2,1"), meldung(
    "mit_summenzeile(text)", BEISPIEL, ergebnis, vergleich_summenzeile(BEISPIEL),
    '\nTipp: Bauen Sie aus "gesamt" und den Summen (mit str) eine Liste und setzen Sie sie mit ",".join(...) zusammen.',
)

# mit_summenzeile im Beispiel: genau so, mit Kommas ohne Leerzeichen und Zeilenumbruch am Ende jeder Zeile
assert ergebnis == vergleich_summenzeile(BEISPIEL), meldung(
    "mit_summenzeile(text)", BEISPIEL, ergebnis, vergleich_summenzeile(BEISPIEL),
    '\nTipp: Die alten Zeilen bleiben unverändert; hängen Sie an jede Zeile "\\n" an, auch an die Summenzeile.',
)

# mit_summenzeile mit anderen Spalten, letzte Zeile ohne Zeilenumbruch und leeren Zeilen
text = "datei,warnungen,todo\n\napi.py,7,1\ndb.py, 5 ,4"
ergebnis = aufruf(mit_summenzeile, text)
assert ergebnis == vergleich_summenzeile(text), meldung(
    "mit_summenzeile(text)", text, ergebnis, vergleich_summenzeile(text), "\nTipp: Leere Zeilen fallen weg, die übrigen bleiben, wie sie sind."
)

# mit_summenzeile: nur die Kopfzeile
text = "modul,stil,fehler"
ergebnis = aufruf(mit_summenzeile, text)
assert ergebnis == vergleich_summenzeile(text), meldung("mit_summenzeile(text)", text, ergebnis, vergleich_summenzeile(text))

# mit_summenzeile: Zeilen nur aus Leerzeichen zählen als leer
text = "modul,stil\na.py,3\n   \nb.py,5\n  "
ergebnis = aufruf(mit_summenzeile, text)
assert ergebnis == vergleich_summenzeile(text), meldung(
    "mit_summenzeile(text)", text, ergebnis, vergleich_summenzeile(text),
    '\nTipp: Prüfen Sie zeile.strip() == "", dann fallen auch Zeilen nur aus Leerzeichen weg.',
)

# auffaellige_module im Beispiel
ergebnis = aufruf(auffaellige_module, BEISPIEL, "stil", 3)
assert ergebnis == ["login.py", "kasse.py"], meldung(
    'auffaellige_module(text, "stil", 3)', BEISPIEL, ergebnis, ["login.py", "kasse.py"],
    '\nTipp: kopf.index(spalte) ist die Stelle der Spalte; vergleichen Sie int(felder[stelle]) >= grenze.',
)

# auffaellige_module mit einer anderen Spalte (nicht fest hinschreiben!)
ergebnis = aufruf(auffaellige_module, BEISPIEL, "sicherheit", 1)
assert ergebnis == ["login.py"], meldung('auffaellige_module(text, "sicherheit", 1)', BEISPIEL, ergebnis, ["login.py"])

# auffaellige_module: genau auf der Grenze zählt mit
text = "modul,stil,fehler\na.py,5,2\nb.py,4,2\nc.py,6,1\n"
ergebnis = aufruf(auffaellige_module, text, "fehler", 2)
assert ergebnis == vergleich_auffaellige(text, "fehler", 2), meldung(
    'auffaellige_module(text, "fehler", 2)', text, ergebnis, vergleich_auffaellige(text, "fehler", 2),
    "\nTipp: „mindestens grenze“ heißt >=.",
)

# auffaellige_module: Zahlen werden als Zahlen verglichen, nicht als Text
text = "modul,stil\na.py,10\nb.py,9\nc.py, 12\n"
ergebnis = aufruf(auffaellige_module, text, "stil", 9)
assert ergebnis == vergleich_auffaellige(text, "stil", 9), meldung(
    'auffaellige_module(text, "stil", 9)', text, ergebnis, vergleich_auffaellige(text, "stil", 9),
    '\nTipp: Als Text ist "10" kleiner als "9"; wandeln Sie mit int(...) um.',
)

# auffaellige_module: Grenze 0 liefert alle
text = "modul,stil\n\na.py,0\nb.py,3\n\n"
ergebnis = aufruf(auffaellige_module, text, "stil", 0)
assert ergebnis == ["a.py", "b.py"], meldung('auffaellige_module(text, "stil", 0)', text, ergebnis, ["a.py", "b.py"])

# auffaellige_module: nur die Kopfzeile, also keine Module
ergebnis = aufruf(auffaellige_module, "modul,stil\n", "stil", 1)
assert ergebnis == [], meldung('auffaellige_module(text, "stil", 1)', "modul,stil\n", ergebnis, [])

# auffaellige_module: Zeilen nur aus Leerzeichen zählen als leer
text = "modul,stil\na.py,3\n   \nb.py,5\n  "
ergebnis = aufruf(auffaellige_module, text, "stil", 4)
assert ergebnis == ["b.py"], meldung(
    'auffaellige_module(text, "stil", 4)', text, ergebnis, ["b.py"],
    '\nTipp: Prüfen Sie zeile.strip() == "", dann fallen auch Zeilen nur aus Leerzeichen weg.',
)

# Viele zufällige Berichte
zufall = Zufall(3050)
namen = ["stil", "fehler", "sicherheit", "doku", "komplex", "todo"]
berichte = []
for _ in range(150):
    spalten = ["modul"] + zufall.sample(namen, zufall.randint(1, 6))
    zeilen = [",".join(spalten)]
    for nummer in range(zufall.randint(0, 8)):
        werte = []
        for _ in spalten[1:]:
            wert = str(zufall.choice([0, 1, 2, 9, 10, 99, zufall.randint(0, 100000)]))
            werte.append(zufall.choice([wert, " " + wert, wert + " "]))
        zeilen.append(",".join([f"m{nummer}.py"] + werte))
        if zufall.random() < 0.2:
            zeilen.append(zufall.choice(["", "  "]))
    text = "\n".join(zeilen) + zufall.choice(["", "\n", "\n\n"])
    berichte.append((text, zufall.choice(spalten[1:]), zufall.choice([0, 1, 9, 10, 100, 50000])))

# Viele zufällige Berichte: spaltensummen
for text, _, _ in berichte:
    ergebnis = aufruf(spaltensummen, text)
    assert ergebnis == vergleich_summen(text), meldung("spaltensummen(text)", text, ergebnis, vergleich_summen(text))

# Viele zufällige Berichte: mit_summenzeile
for text, _, _ in berichte:
    ergebnis = aufruf(mit_summenzeile, text)
    assert ergebnis == vergleich_summenzeile(text), meldung("mit_summenzeile(text)", text, ergebnis, vergleich_summenzeile(text))

# Viele zufällige Berichte: auffaellige_module
for text, spalte, grenze in berichte:
    ergebnis = aufruf(auffaellige_module, text, spalte, grenze)
    erwartet = vergleich_auffaellige(text, spalte, grenze)
    assert ergebnis == erwartet, meldung(f"auffaellige_module(text, {spalte!r}, {grenze})", text, ergebnis, erwartet)

# Obere Grenze: 10 000 Module mit 20 Spalten
spalten = ["modul"] + [f"kategorie{nummer}" for nummer in range(19)]
zeilen = [",".join(spalten)]
for nummer in range(10000):
    zeilen.append(",".join([f"modul{nummer}.py"] + [str((nummer * 7 + stelle * 13) % 100001) for stelle in range(19)]))
text = "\n".join(zeilen) + "\n"
ergebnis = aufruf(mit_summenzeile, text)
assert ergebnis == vergleich_summenzeile(text), (
    f"Bei 10 000 Modulen endet mit_summenzeile mit {str(ergebnis)[-150:]!r}, erwartet war {vergleich_summenzeile(text)[-150:]!r}."
)
# Obere Grenze: auffaellige_module bei 10 000 Modulen
ergebnis = aufruf(auffaellige_module, text, "kategorie18", 99000)
assert ergebnis == vergleich_auffaellige(text, "kategorie18", 99000), "Bei 10 000 Modulen stimmt auffaellige_module nicht."
