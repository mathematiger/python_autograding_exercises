# Automatisch erzeugt aus lehrkraft/muster/2_060_materialliste.py - nicht von Hand ändern.
# vorlage-hash: 8e2f9df28863bca1
# text-hash: 38b891294bda6a2f
# thema: programmaufbau
# inhalt: Menüprogramm mit Dictionary

EINGABEN = ["0"]

MENUE = """==============================
         MATERIALLISTE
==============================
1 – Material hinzufügen
2 – Material entnehmen
3 – Liste anzeigen
0 – Programm beenden"""


def ohne_striche(text):
    """Vergleicht locker wie vergleichbar, übergeht zusätzlich Bindestriche und die Länge der Zeilen aus =."""
    text = vergleichbar(text).replace("-", "")
    while "==" in text:
        text = text.replace("==", "=")
    return text


def rufe_auf(funktion, *argumente):
    """Ruft funktion(*argumente) auf; liefert Rückgabewert, Ausgabe, Zahl der input-Aufrufe und Ausnahme (sonst None)."""
    global print, input
    ausgabe = []
    fragen = []

    def merke(*werte, sep=" ", end="\n", **_):
        """Wie print, merkt sich die Ausgabe aber nur."""
        ausgabe.append(sep.join(str(wert) for wert in werte) + end)

    def keine_eingabe(aufforderung=""):
        """Wie input, merkt sich aber nur, dass gefragt wurde."""
        fragen.append(aufforderung)
        return "0"

    altes_print, altes_input = print, input
    print, input = merke, keine_eingabe
    try:
        ergebnis, fehler = funktion(*argumente), None
    except Exception as ausnahme:
        ergebnis, fehler = None, ausnahme
    finally:
        print, input = altes_print, altes_input
    return ergebnis, "".join(ausgabe), len(fragen), fehler


def absturz(aufruf, fehler):
    """Baut die Meldung, wenn ein Aufruf abgestürzt ist."""
    return f"{aufruf} ist mit {type(fehler).__name__}: {fehler} abgestürzt."


def anzahl_menues(ausgabe):
    """Zählt, wie oft das Menü in der Ausgabe steht."""
    return ohne_striche(ausgabe).count(ohne_striche(MENUE))


def abschnitte(ausgabe):
    """Zerlegt die Ausgabe an den Zeilen „Programm beenden“; liefert die Zeilen nach jedem Menü."""
    teile = [[]]
    for zeile in ausgabe.splitlines():
        if "programm beenden" in zeile.casefold():
            teile.append([])
        else:
            teile[-1].append(zeile)
    return teile[1:]


def angezeigt(ausgabe):
    """Liefert die Positionen und die Gesamtzahl, die die letzte Aktion vor der 0 ausgegeben hat."""
    teile = abschnitte(ausgabe)
    if len(teile) < 2:
        return [], None
    gefunden = []
    gesamt = None
    for zeile in teile[-2]:
        zeile = zeile.strip()
        if zeile.casefold().startswith("gesamt"):
            for teil in zeile.replace(":", " ").split():
                if teil.isdigit():
                    gesamt = int(teil)
                    break
            continue
        if ":" not in zeile:
            continue
        artikel, _, rest = zeile.partition(":")
        worte = rest.split()
        if worte and worte[0].isdigit():
            gefunden.append((artikel.strip(), int(worte[0])))
    return gefunden, gesamt


def vergleich(befehle):
    """Langsame Vergleichslösung: spielt die Befehle mit zwei Listen nach; liefert Positionen und Gesamtzahl."""
    namen = []
    anzahlen = []
    for befehl, artikel, anzahl in befehle:
        if artikel in namen:
            stelle = namen.index(artikel)
        else:
            stelle = -1
        if befehl == "1" and stelle == -1:
            namen.append(artikel)
            anzahlen.append(anzahl)
        elif befehl == "1":
            anzahlen[stelle] += anzahl
        elif befehl == "2" and stelle != -1:
            anzahlen[stelle] -= anzahl
            if anzahlen[stelle] <= 0:
                namen.pop(stelle)
                anzahlen.pop(stelle)
    paare = sorted(zip(namen, anzahlen))
    return paare, sum(anzahlen)


def als_eingaben(befehle):
    """Macht aus Befehlen (auswahl, artikel, anzahl) die Eingaben, mit Anzeige und 0 am Ende."""
    eingaben = []
    for befehl, artikel, anzahl in befehle:
        eingaben = eingaben + [befehl, artikel, str(anzahl)]
    return eingaben + ["3", "0"]


def meldung_lauf(eingaben, ausgabe, erwartet, gesamt):
    """Baut die Meldung, wenn die angezeigte Liste nicht stimmt."""
    zeilen = "\n".join(f"{artikel}: {anzahl}" for artikel, anzahl in erwartet)
    kurz = eingaben if len(eingaben) <= 40 else eingaben[:40] + ["…"]
    if len(ausgabe) > 3000:
        ausgabe = ausgabe[:3000] + "\n…"
    return (
        f"Mit den Eingaben {kurz} erwartet bei 3 (Liste anzeigen):\n{zeilen}\nGesamt: {gesamt} Teile\n"
        f"Ihr Programm gibt aus:\n{ausgabe}"
    )


BEISPIEL = ["1", "Patchkabel", "6", "1", "SSD", "2", "1", "Patchkabel", "4", "2", "SSD", "1", "3", "0"]

# hinzufuegen: ein neuer Artikel kommt in die Liste
liste = {}
_, _, _, fehler = rufe_auf(hinzufuegen, liste, "Patchkabel", 6)
assert fehler is None and liste == {"Patchkabel": 6}, (
    absturz('hinzufuegen({}, "Patchkabel", 6)', fehler)
    if fehler
    else f'Nach hinzufuegen(liste, "Patchkabel", 6) mit liste = {{}} ist liste {liste!r}, '
    "erwartet war {'Patchkabel': 6}.\nTipp: Ändern Sie das übergebene Dictionary selbst: "
    "liste[artikel] = ... (Aufgabe 2_019); ein neues Dictionary mit return reicht nicht."
)

# hinzufuegen: ein vorhandener Artikel wird aufaddiert
liste = {"Patchkabel": 6}
_, _, _, fehler = rufe_auf(hinzufuegen, liste, "Patchkabel", 4)
assert fehler is None and liste == {"Patchkabel": 10}, (
    absturz('hinzufuegen({"Patchkabel": 6}, "Patchkabel", 4)', fehler)
    if fehler
    else f'Nach hinzufuegen(liste, "Patchkabel", 4) mit liste = {{"Patchkabel": 6}} ist liste {liste!r}, '
    "erwartet war {'Patchkabel': 10}.\nTipp: Addieren Sie zur bisherigen Anzahl, statt sie zu überschreiben: "
    "liste.get(artikel, 0) + anzahl (Aufgabe 2_026)."
)

# hinzufuegen: andere Artikel bleiben, wie sie sind (nicht fest hinschreiben!)
liste = {"SSD": 2, "Netzteil": 1}
_, _, _, fehler = rufe_auf(hinzufuegen, liste, "Kabelbinder", 50)
assert fehler is None and liste == {"SSD": 2, "Netzteil": 1, "Kabelbinder": 50}, (
    absturz('hinzufuegen(..., "Kabelbinder", 50)', fehler)
    if fehler
    else f'Nach hinzufuegen(liste, "Kabelbinder", 50) mit liste = {{"SSD": 2, "Netzteil": 1}} ist liste '
    f"{liste!r}, erwartet war {{'SSD': 2, 'Netzteil': 1, 'Kabelbinder': 50}}."
)

# entnehmen: einen Teil eines Artikels entnehmen
liste = {"Patchkabel": 10, "SSD": 2}
ergebnis, _, _, fehler = rufe_auf(entnehmen, liste, "Patchkabel", 3)
assert fehler is None and liste == {"Patchkabel": 7, "SSD": 2}, (
    absturz('entnehmen(..., "Patchkabel", 3)', fehler)
    if fehler
    else f'Nach entnehmen(liste, "Patchkabel", 3) mit liste = {{"Patchkabel": 10, "SSD": 2}} ist liste '
    f"{liste!r}, erwartet war {{'Patchkabel': 7, 'SSD': 2}}."
)

# entnehmen: gibt True zurück, wenn der Artikel auf der Liste stand
assert ergebnis is True, (
    f'entnehmen(liste, "Patchkabel", 3) gibt {ergebnis!r} zurück, erwartet war True, weil Patchkabel auf der Liste '
    "standen." + ("\nTipp: Am Ende fehlt return True." if ergebnis is None else "")
)

# entnehmen: wer alles entnimmt, entfernt den Artikel ganz
liste = {"Patchkabel": 10, "SSD": 2}
_, _, _, fehler = rufe_auf(entnehmen, liste, "SSD", 2)
assert fehler is None and liste == {"Patchkabel": 10}, (
    absturz('entnehmen(..., "SSD", 2)', fehler)
    if fehler
    else f'Nach entnehmen(liste, "SSD", 2) mit liste = {{"Patchkabel": 10, "SSD": 2}} ist liste {liste!r}, '
    "erwartet war {'Patchkabel': 10}.\nTipp: Bleibt 0 übrig, entfernen Sie den Artikel mit del liste[artikel]."
)

# entnehmen: mehr als vorhanden entfernt den Artikel, es bleibt keine negative Anzahl
liste = {"Patchkabel": 10, "SSD": 2}
_, _, _, fehler = rufe_auf(entnehmen, liste, "SSD", 5)
assert fehler is None and liste == {"Patchkabel": 10}, (
    absturz('entnehmen(..., "SSD", 5)', fehler)
    if fehler
    else f'Nach entnehmen(liste, "SSD", 5) mit liste = {{"Patchkabel": 10, "SSD": 2}} ist liste {liste!r}, '
    "erwartet war {'Patchkabel': 10}.\nTipp: Bleibt 0 oder weniger übrig, verschwindet der Artikel ganz."
)

# entnehmen: ein Artikel, der nicht auf der Liste steht, ergibt False
liste = {"Patchkabel": 10}
ergebnis, _, _, fehler = rufe_auf(entnehmen, liste, "Maus", 1)
assert fehler is None and ergebnis is False, (
    absturz('entnehmen({"Patchkabel": 10}, "Maus", 1)', fehler)
    + '\nTipp: Prüfen Sie zuerst mit artikel in liste, ob der Artikel da ist; liste["Maus"] gibt sonst einen KeyError.'
    if fehler
    else f'entnehmen(liste, "Maus", 1) mit liste = {{"Patchkabel": 10}} gibt {ergebnis!r} zurück, erwartet war False.'
)

# entnehmen: ein unbekannter Artikel lässt die Liste unverändert
assert ergebnis is not None and liste == {"Patchkabel": 10}, (
    f'Nach entnehmen(liste, "Maus", 1) mit liste = {{"Patchkabel": 10}} ist liste {liste!r}, erwartet war '
    "sie unverändert."
)

# gesamtzahl: das Beispiel
ergebnis, _, _, fehler = rufe_auf(gesamtzahl, {"Patchkabel": 10, "SSD": 1})
assert fehler is None and ergebnis == 11, (
    absturz('gesamtzahl({"Patchkabel": 10, "SSD": 1})', fehler)
    if fehler
    else f'gesamtzahl({{"Patchkabel": 10, "SSD": 1}}) ergibt {ergebnis!r}, erwartet war 11.'
    + ("\nTipp: Summieren Sie die Werte (liste.values()), nicht die Zahl der Artikel." if ergebnis == 2 else "")
)

# gesamtzahl: andere Werte und die leere Liste
ergebnis, _, _, fehler = rufe_auf(gesamtzahl, {"Kabelbinder": 50, "Netzteil": 3, "SSD": 2})
leer, _, _, fehler_leer = rufe_auf(gesamtzahl, {})
assert ergebnis == 55 and leer == 0, (
    f"gesamtzahl({{'Kabelbinder': 50, 'Netzteil': 3, 'SSD': 2}}) ergibt {ergebnis!r} (erwartet 55), "
    f"gesamtzahl({{}}) ergibt {leer!r} (erwartet 0)."
    + (f" Fehler: {fehler or fehler_leer!r}" if fehler or fehler_leer else "")
)

# positionen: das Beispiel
ergebnis, _, _, fehler = rufe_auf(positionen, {"SSD": 1, "Patchkabel": 10})
assert fehler is None and ergebnis is not None and list(ergebnis) == [("Patchkabel", 10), ("SSD", 1)], (
    absturz('positionen({"SSD": 1, "Patchkabel": 10})', fehler)
    if fehler
    else f'positionen({{"SSD": 1, "Patchkabel": 10}}) ergibt {ergebnis!r}, erwartet war '
    "[('Patchkabel', 10), ('SSD', 1)].\nTipp: sorted(liste.items()) sortiert die Paare nach dem Artikel."
)

# positionen: mehr Artikel und die leere Liste
ergebnis, _, _, fehler = rufe_auf(positionen, {"Netzteil": 3, "Kabelbinder": 50, "SSD": 2, "Adapter": 1})
leer, _, _, _ = rufe_auf(positionen, {})
erwartet = [("Adapter", 1), ("Kabelbinder", 50), ("Netzteil", 3), ("SSD", 2)]
assert ergebnis is not None and list(ergebnis) == erwartet and leer is not None and list(leer) == [], (
    f"positionen({{'Netzteil': 3, 'Kabelbinder': 50, 'SSD': 2, 'Adapter': 1}}) ergibt {ergebnis!r}, "
    f"erwartet war {erwartet!r}; positionen({{}}) ergibt {leer!r}, erwartet war []."
)

# Die vier Funktionen fragen nichts und geben nichts aus
stoerungen = []
for name, funktion, argumente in [
    ("hinzufuegen", hinzufuegen, ({}, "SSD", 1)),
    ("entnehmen", entnehmen, ({"SSD": 2}, "SSD", 1)),
    ("gesamtzahl", gesamtzahl, ({"SSD": 2},)),
    ("positionen", positionen, ({"SSD": 2},)),
]:
    _, ausgabe, fragen, _ = rufe_auf(funktion, *argumente)
    if ausgabe or fragen:
        stoerungen.append(name)
assert stoerungen == [], (
    f"Diese Funktionen benutzen print oder input: {', '.join(stoerungen)}.\n"
    "Tipp: Die Funktionen bekommen alles über ihre Parameter; Fragen und Ausgeben gehört ins Hauptprogramm."
)

# Beim Start erscheint das Menü
assert ohne_striche(MENUE) in ohne_striche(AUSGABE), f"Beim Start erwartet:\n{MENUE}\nIhr Programm gibt aus:\n{AUSGABE}"

# Bei 0 endet das Programm sofort
ausgabe = starte("0")
assert anzahl_menues(ausgabe) == 1, (
    f"Mit der Eingabe 0 soll das Menü genau einmal erscheinen, dann endet das Programm. Ihr Programm gibt aus:\n"
    f"{ausgabe}"
)

# Hinzufügen und anzeigen: ein Artikel
eingaben = ["1", "Patchkabel", "6", "3", "0"]
ausgabe = starte(*eingaben)
gefunden, gesamt = angezeigt(ausgabe)
assert gefunden == [("Patchkabel", 6)], meldung_lauf(eingaben, ausgabe, [("Patchkabel", 6)], 6) + (
    "\nTipp: Geben Sie jede Position als Zeile „Artikel: Anzahl“ aus, etwa f\"{artikel}: {anzahl}\"."
)

# Die Anzeige endet mit der Gesamtzahl
assert gesamt == 6, meldung_lauf(eingaben, ausgabe, [("Patchkabel", 6)], 6) + (
    "\nTipp: Unter den Positionen fehlt eine Zeile, die mit „Gesamt“ beginnt."
)

# Das Beispiel aus der Aufgabe
ausgabe = starte(*BEISPIEL)
gefunden, gesamt = angezeigt(ausgabe)
erwartet = [("Patchkabel", 10), ("SSD", 1)]
if gefunden == [("Patchkabel", 4), ("SSD", 1)]:
    tipp = "\nTipp: Ein vorhandener Artikel wird aufaddiert, nicht überschrieben."
elif gefunden == [("SSD", 1)] or gefunden == []:
    tipp = "\nTipp: Legen Sie liste = {} einmal vor der while-Schleife an, nicht in jedem Durchlauf."
else:
    tipp = ""
assert gefunden == erwartet and gesamt == 11, meldung_lauf(BEISPIEL, ausgabe, erwartet, 11) + tipp

# Die Liste bleibt über mehrere Menüdurchläufe erhalten (nicht fest hinschreiben!)
eingaben = ["1", "Netzteil", "2", "1", "Kabelbinder", "40", "1", "Netzteil", "1", "3", "0"]
ausgabe = starte(*eingaben)
gefunden, gesamt = angezeigt(ausgabe)
erwartet = [("Kabelbinder", 40), ("Netzteil", 3)]
assert gefunden == erwartet and gesamt == 43, meldung_lauf(eingaben, ausgabe, erwartet, 43)

# Die Anzeige ist nach dem Artikel sortiert
eingaben = ["1", "SSD", "1", "1", "Adapter", "2", "1", "Maus", "3", "3", "0"]
ausgabe = starte(*eingaben)
gefunden, gesamt = angezeigt(ausgabe)
erwartet = [("Adapter", 2), ("Maus", 3), ("SSD", 1)]
assert gefunden == erwartet, meldung_lauf(eingaben, ausgabe, erwartet, 6) + (
    "\nTipp: Geben Sie die Positionen in der Reihenfolge von positionen(liste) aus."
    if sorted(gefunden) == erwartet
    else ""
)

# Entnehmen über das Menü, auch bis der Artikel verschwindet
eingaben = ["1", "SSD", "2", "1", "Maus", "3", "2", "Maus", "1", "2", "SSD", "5", "3", "0"]
ausgabe = starte(*eingaben)
gefunden, gesamt = angezeigt(ausgabe)
assert gefunden == [("Maus", 2)] and gesamt == 2, meldung_lauf(eingaben, ausgabe, [("Maus", 2)], 2)

# Entnehmen eines unbekannten Artikels gibt einen Hinweis mit dem Artikel
eingaben = ["1", "SSD", "2", "2", "Kabeltester", "1", "0"]
try:
    ausgabe, fehler = starte(*eingaben), None
except Exception as ausnahme:
    ausgabe, fehler = "", ausnahme
teile = abschnitte(ausgabe)
hinweis = "\n".join(teile[-2]) if len(teile) >= 2 else ""
assert fehler is None and "kabeltester" in hinweis.casefold(), (
    f"Mit den Eingaben {eingaben} erwartet: nach dem Entnehmen ein Hinweis, der Kabeltester nennt. "
    + (f"Ihr Programm ist abgestürzt: {fehler}" if fehler else f"Ihr Programm gibt aus:\n{ausgabe}")
    + "\nTipp: entnehmen gibt dann False zurück; geben Sie in diesem Fall einen Hinweis aus."
)

# Eine leere Liste wird als „leer“ angezeigt
ausgabe = starte("3", "0")
teile = abschnitte(ausgabe)
anzeige = "\n".join(teile[0]) if teile else ""
assert "leer" in anzeige.casefold(), (
    f"Mit den Eingaben ['3', '0'] erwartet: ein Satz mit dem Wort „leer“. Ihr Programm gibt aus:\n{ausgabe}"
)

# Nach jeder Aktion erscheint das Menü wieder
ausgabe = starte(*BEISPIEL)
assert anzahl_menues(ausgabe) == 6, (
    f"Mit den Eingaben {BEISPIEL} soll das Menü sechsmal erscheinen (vor jeder der fünf Aktionen und vor der 0). "
    f"Ihr Programm gibt aus:\n{ausgabe}"
)

# Bei einer ungültigen Zahl als Auswahl (9) gibt es einen Hinweis, dann wieder das Menü
nur_ende = ohne_striche(starte("0")).replace(ohne_striche(MENUE), "")
ausgabe = starte("9", "0")
rest = ohne_striche(ausgabe).replace(ohne_striche(MENUE), "")
assert anzahl_menues(ausgabe) == 2 and len(rest) > len(nur_ende), (
    f"Mit den Eingaben ['9', '0'] erwartet: Menü, ein Hinweis, Menü. Ihr Programm gibt aus:\n{ausgabe}\n"
    "Tipp: Fangen Sie alle anderen Eingaben mit else ab und geben Sie dort einen Hinweis aus."
)

# Bei einem Text als Auswahl (abc) stürzt das Programm nicht ab
try:
    ausgabe, fehler = starte("abc", "0"), None
except Exception as ausnahme:
    ausgabe, fehler = "", ausnahme
rest = ohne_striche(ausgabe).replace(ohne_striche(MENUE), "")
assert fehler is None and anzahl_menues(ausgabe) == 2 and len(rest) > len(nur_ende), (
    "Mit den Eingaben ['abc', '0'] erwartet: Menü, ein Hinweis, Menü. "
    + (
        f"Ihr Programm ist abgestürzt: {fehler}\nTipp: Lesen Sie die Auswahl als Text und vergleichen Sie mit "
        '"1", "2", "3" und "0", statt sie mit int(...) umzuwandeln.'
        if fehler
        else f"Ihr Programm gibt aus:\n{ausgabe}"
    )
)

# Das Hauptprogramm benutzt die vier Funktionen
fehlend = []
for name in ["hinzufuegen", "entnehmen", "gesamtzahl", "positionen"]:
    if not verwendet(name):
        fehlend.append(name)
assert fehlend == [], (
    f"Diese Funktionen ruft Ihr Programm nicht auf: {', '.join(fehlend)}.\n"
    "Tipp: Ändern und werten Sie die Liste im Hauptprogramm nur über die vier Funktionen aus."
)

# Das Menü ist eine while-Schleife
assert verwendet("while"), "Benutzen Sie für das Menü eine while-Schleife (Aufgabe 2_037)."

# 200 zufällige Befehlsfolgen, verglichen mit einer Lösung ohne Dictionary
zufall = Zufall(2060)
artikelnamen = ["Patchkabel", "SSD", "ssd", "Netzteil", "Kabelbinder", "Maus", "USB-Stick", "Adapter HDMI"]
for _ in range(200):
    befehle = []
    for _ in range(zufall.randint(0, 12)):
        befehle.append((zufall.choice(["1", "1", "2"]), zufall.choice(artikelnamen), zufall.randint(1, 8)))
    erwartet, summe = vergleich(befehle)
    eingaben = als_eingaben(befehle)
    ausgabe = starte(*eingaben)
    gefunden, gesamt = angezeigt(ausgabe)
    if erwartet:
        assert gefunden == erwartet and gesamt == summe, meldung_lauf(eingaben, ausgabe, erwartet, summe)
    else:
        teile = abschnitte(ausgabe)
        assert len(teile) >= 2 and "leer" in "\n".join(teile[-2]).casefold(), (
            f"Mit den Eingaben {eingaben} ist die Liste am Ende leer; erwartet war ein Satz mit „leer“. "
            f"Ihr Programm gibt aus:\n{ausgabe}"
        )

# An der oberen Grenze: 1000 Aktionen mit 300 verschiedenen Artikeln
befehle = []
for nummer in range(1000):
    artikel = f"Teil {nummer % 300:03d}"
    befehle.append(("2" if nummer % 7 == 6 else "1", artikel, 1000))
eingaben = als_eingaben(befehle[:-1])
ausgabe = starte(*eingaben)
gefunden, gesamt = angezeigt(ausgabe)
erwartet, summe = vergleich(befehle[:-1])
assert gefunden == erwartet and gesamt == summe, (
    f"Bei 999 Aktionen mit 300 Artikeln erwartet: {len(erwartet)} Positionen, Gesamt {summe} - gefunden: "
    f"{len(gefunden)} Positionen, Gesamt {gesamt}."
)
