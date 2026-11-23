# Automatisch erzeugt aus lehrkraft/muster/4_070_wartungsplan.py - nicht von Hand ändern.
# vorlage-hash: ab0119c3219240c7
# text-hash: ffefd748c8ed1fd4
# thema: texte_zahlen
# inhalt: json: eigene Objekte speichern

import os
import tempfile

USV = Wartung("USV Serverraum", 180, {"Kaya", "Berg"}, Status.GEPLANT)
KLIMA = Wartung("Klimagerät Büro 2", 90, set())
PLAN = {"stand": "2026-11-23", "wartungen": [USV, KLIMA]}
USV_DICT = {
    "typ": "Wartung",
    "geraet": "USV Serverraum",
    "intervall_tage": 180,
    "zustaendig": ["Berg", "Kaya"],
    "status": "GEPLANT",
}
KLIMA_DICT = {"typ": "Wartung", "geraet": "Klimagerät Büro 2", "intervall_tage": 90, "zustaendig": [], "status": "OFFEN"}
ORDNER = tempfile.mkdtemp()


def kopie(wert):
    """Tiefe Kopie eines Plans, die die Wartung-Objekte mitkopiert."""
    if isinstance(wert, Wartung):
        return Wartung(wert.geraet, wert.intervall_tage, set(wert.zustaendig), wert.status)
    if isinstance(wert, dict):
        return {schluessel: kopie(inhalt) for schluessel, inhalt in wert.items()}
    if isinstance(wert, list):
        return [kopie(inhalt) for inhalt in wert]
    return wert


def wert_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def datei(name):
    """Ein Pfad im temporären Ordner der Tests."""
    return os.path.join(ORDNER, name)


def inhalt(pfad):
    """Der Text einer Datei, oder eine Meldung, wenn es sie nicht gibt."""
    try:
        with open(pfad, encoding="utf-8") as datei_:
            return datei_.read()
    except Exception as fehler:
        return f"(nicht lesbar: {type(fehler).__name__}: {fehler})"


def hin_und_zurueck(plan, name):
    """Speichert eine Kopie des Plans und lädt ihn wieder; ein Fehler wird als Text zurückgegeben."""
    pfad = datei(name)
    ergebnis = wert_von(lambda: speichern(kopie(plan), pfad))
    if isinstance(ergebnis, str):
        return f"speichern: {ergebnis}"
    return wert_von(lambda: laden(pfad))


def kurz(wert):
    """Kürzt lange Werte für die Meldung."""
    text = repr(wert)
    return text if len(text) <= 400 else text[:300] + " …"


def zufallswartung(zufall):
    """Erzeugt eine Wartung mit schwierigen Zeichen."""
    namen = ["Kaya", "Berg", "Öztürk", 'Max "Mo" Nowak', "Weiß\\Schwarz", "Ünal"]
    geraet = zufall.choice(["USV", "Klimagerät", "Brandmeldeanlage", 'Switch "Kern"', "Pfad C:\\Daten"])
    return Wartung(
        geraet + f" {zufall.randint(1, 99)}",
        zufall.randint(1, 3650),
        set(zufall.sample(namen, zufall.randint(0, 4))),
        zufall.choice(list(Status)),
    )


def zufallsplan(zufall, tiefe):
    """Erzeugt einen verschachtelten Plan mit Wartungen, Listen, Dictionaries und einfachen Werten."""
    auswahl = zufall.randint(0, 7 if tiefe > 0 else 4)
    if auswahl == 0:
        return zufallswartung(zufall)
    if auswahl == 1:
        return zufall.choice(["Text", "Prüfung", "", "a\nb"])
    if auswahl == 2:
        return zufall.choice([0, -5, 3650, 2.5])
    if auswahl == 3:
        return zufall.choice([True, False, None])
    if auswahl == 4:
        return zufallswartung(zufall)
    if auswahl == 5:
        return [zufallsplan(zufall, tiefe - 1) for _ in range(zufall.randint(0, 3))]
    return {f"k{nummer}": zufallsplan(zufall, tiefe - 1) for nummer in range(zufall.randint(0, 3))}


# als_dict: eine Wartung wird ein Dictionary
ergebnis = wert_von(lambda: als_dict(kopie(USV)))
assert ergebnis == USV_DICT, (
    f"als_dict(usv) ergibt\n{kurz(ergebnis)}\nerwartet war\n{USV_DICT}\n"
    "Tipp: Die Menge als sorted(…), den Status als objekt.status.name."
)

# als_dict: eine andere Wartung (nicht fest hinschreiben!)
ergebnis = wert_von(lambda: als_dict(kopie(KLIMA)))
assert ergebnis == KLIMA_DICT, f"als_dict(klima) ergibt\n{kurz(ergebnis)}\nerwartet war\n{KLIMA_DICT}"

# als_dict: mit json.dumps entsteht gültiges JSON
text = wert_von(lambda: json.dumps(kopie(USV), default=als_dict))
zurueck = wert_von(lambda: json.loads(text))
assert zurueck == USV_DICT, f"json.dumps(usv, default=als_dict) ergibt {kurz(text)}; daraus liest json.loads {kurz(zurueck)}."

# als_dict: andere Objekte ergeben einen TypeError
for fremd in [{1, 2}, Status.OFFEN, object()]:
    try:
        als_dict(fremd)
        fehler = None
    except Exception as ausnahme:
        fehler = ausnahme
    assert isinstance(fehler, TypeError), (
        f"als_dict({fremd!r}) löst {type(fehler).__name__ if fehler else 'keinen Fehler'} aus, erwartet war TypeError.\n"
        "Tipp: Was keine Wartung ist, beantworten Sie mit raise TypeError(…); json meldet dann den Fehler."
    )

# aus_dict: ein Wartung-Dictionary wird eine Wartung
ergebnis = wert_von(lambda: aus_dict(dict(USV_DICT, zustaendig=["Berg", "Kaya"])))
assert ergebnis == USV, (
    f"aus_dict({USV_DICT}) ergibt\n{kurz(ergebnis)}\nerwartet war\n{USV!r}\n"
    "Tipp: set(daten['zustaendig']) und Status[daten['status']]."
)

# aus_dict: andere Dictionaries bleiben, wie sie sind
daten = {"stand": "2026-11-23", "anzahl": 2}
ergebnis = wert_von(lambda: aus_dict(daten))
assert ergebnis is daten or ergebnis == daten, (
    f"aus_dict({daten}) ergibt {kurz(ergebnis)}; erwartet war dasselbe Dictionary.\n"
    "Tipp: Ohne den Eintrag 'typ' geben Sie daten unverändert zurück; daten.get('typ') vermeidet einen KeyError."
)

# aus_dict: mit json.loads werden auch verschachtelte Wartungen wieder Objekte
text = json.dumps({"liste": [USV_DICT], "leer": {}})
ergebnis = wert_von(lambda: json.loads(text, object_hook=aus_dict))
erwartet = {"liste": [USV], "leer": {}}
assert ergebnis == erwartet, f"json.loads({text!r}, object_hook=aus_dict) ergibt\n{kurz(ergebnis)}\nerwartet war\n{erwartet}"

# speichern und laden: der Plan kommt unverändert zurück
ergebnis = hin_und_zurueck(PLAN, "plan.json")
assert ergebnis == PLAN, f"Nach speichern(plan, pfad) liefert laden(pfad)\n{kurz(ergebnis)}\nerwartet war\n{PLAN}"

# speichern: die Datei enthält gültiges JSON mit "typ": "Wartung"
text = inhalt(datei("plan.json"))
gelesen = wert_von(lambda: json.loads(text))
erwartet = {"stand": "2026-11-23", "wartungen": [USV_DICT, KLIMA_DICT]}
assert gelesen == erwartet, (
    f"Die Datei enthält\n{kurz(text)}\njson.loads macht daraus\n{kurz(gelesen)}\nerwartet war\n{erwartet}\n"
    "Tipp: json.dump(plan, datei, default=als_dict, …)."
)

# speichern: Umlaute stehen lesbar in der Datei
assert "Klimagerät Büro 2" in text, (
    f"In der Datei steht\n{kurz(text)}\nerwartet war 'Klimagerät Büro 2' im Klartext.\n"
    "Tipp: ensure_ascii=False, und die Datei mit encoding='utf-8' öffnen."
)

# speichern: eingerückt mit zwei Leerzeichen
erwartet = json.dumps(gelesen, ensure_ascii=False, indent=2)
assert text.strip() == erwartet, f"In der Datei steht\n{kurz(text)}\nerwartet war (mit indent=2)\n{kurz(erwartet)}"

# speichern verändert den Plan nicht
plan = kopie(PLAN)
wert_von(lambda: speichern(plan, datei("unveraendert.json")))
assert plan == PLAN, f"Nach speichern ist plan {kurz(plan)}; er sollte unverändert bleiben."

# speichern und laden: ein Plan ohne Wartungen
ergebnis = hin_und_zurueck({"stand": "2026-12-01", "wartungen": []}, "leer.json")
assert ergebnis == {"stand": "2026-12-01", "wartungen": []}, f"Ein Plan ohne Wartungen kommt als {kurz(ergebnis)} zurück."

# speichern und laden: Anführungszeichen, Backslashes und Zeilenumbrüche
wartung = Wartung('Switch "Kern"\\Etage 1\nRaum 3', 3650, {"Weiß\\Schwarz"}, Status.ERLEDIGT)
ergebnis = hin_und_zurueck({"w": wartung}, "zeichen.json")
assert ergebnis == {"w": wartung}, f"Die Wartung {wartung!r} kommt als {kurz(ergebnis)} zurück."

# speichern: eine Datei überschreibt die alte ganz
wert_von(lambda: speichern(kopie(PLAN), datei("zweimal.json")))
ergebnis = hin_und_zurueck({"stand": "x"}, "zweimal.json")
assert ergebnis == {"stand": "x"}, f"Nach zweimaligem Speichern liefert laden {kurz(ergebnis)}, erwartet war {{'stand': 'x'}}."

# Die Ausgabe des Programms
zeile = wert_von(lambda: json.loads(AUSGABE))
erwartet = {"typ": "Wartung", "geraet": "USV", "intervall_tage": 180, "zustaendig": ["Berg", "Kaya"], "status": "GEPLANT"}
assert zeile == erwartet, f"Erwartete Ausgabe:\n{json.dumps(erwartet)}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Pläne
zufall = Zufall(4070)
for nummer in range(150):
    plan = {"stand": f"2026-11-{nummer % 28 + 1:02d}", "inhalt": zufallsplan(zufall, 3)}
    ergebnis = hin_und_zurueck(plan, "zufall.json")
    assert ergebnis == plan, f"Der Plan\n{kurz(plan)}\nkommt zurück als\n{kurz(ergebnis)}"

# Obere Grenze: 1000 Wartungen
plan = {"stand": "2026-11-23", "wartungen": [zufallswartung(zufall) for _ in range(1000)]}
ergebnis = hin_und_zurueck(plan, "gross.json")
assert ergebnis == plan, "Ein Plan mit 1000 Wartungen kommt nicht unverändert zurück."
