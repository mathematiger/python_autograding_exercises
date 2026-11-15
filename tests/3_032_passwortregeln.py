# Automatisch erzeugt aus lehrkraft/muster/3_032_passwortregeln.py - nicht von Hand ändern.
# vorlage-hash: de9916c339c66370
# text-hash: 7526a65a7b6d1c17
# thema: funktionen
# inhalt: Funktionen als Rückgabe

def ist_funktion(wert, aufruf):
    """Gibt eine Meldung zurück, wenn wert keine Funktion ist, sonst einen leeren Text."""
    if callable(wert):
        return ""
    return (
        f"{aufruf} soll eine Funktion zurückgeben, liefert aber {wert!r}.\n"
        "Tipp: Definieren Sie innen mit def eine Funktion regel(passwort) und geben Sie sie mit return regel zurück, ohne Klammern."
    )


# mindestlaenge gibt eine Funktion zurück
ergebnis = mindestlaenge(10)
assert ist_funktion(ergebnis, "mindestlaenge(10)") == "", ist_funktion(ergebnis, "mindestlaenge(10)")

# Das Beispiel: mindestlaenge(10)
regel = mindestlaenge(10)
bekommen = (regel("sommer2025"), regel("kurz1"))
assert bekommen == (True, False), (
    f'mindestlaenge(10) liefert für "sommer2025" und "kurz1" {bekommen}, erwartet war (True, False).'
)

# Genau n Zeichen sind lang genug, n - 1 nicht
regel = mindestlaenge(5)
bekommen = (regel("abcde"), regel("abcd"))
assert bekommen == (True, False), (
    f'mindestlaenge(5) liefert für "abcde" und "abcd" {bekommen}, erwartet war (True, False).\n'
    "Tipp: Mindestens n Zeichen heißt len(passwort) >= n."
)

# Zwei Regeln mit verschiedenem n stören sich nicht (nicht fest hinschreiben!)
kurz = mindestlaenge(3)
lang = mindestlaenge(12)
bekommen = (kurz("abcd"), lang("abcd"), kurz("ab"), lang("abcdefghijkl"))
if bekommen[0] == bekommen[1]:
    hinweis = "\nTipp: Jede Regel muss ihr eigenes n benutzen; speichern Sie n nicht in einer globalen Variablen."
else:
    hinweis = ""
assert bekommen == (True, False, False, True), (
    f'kurz = mindestlaenge(3), lang = mindestlaenge(12): kurz("abcd"), lang("abcd"), kurz("ab"), '
    f'lang("abcdefghijkl") liefern {bekommen}, erwartet war (True, False, False, True).{hinweis}'
)

# mindestlaenge(0) nimmt auch das leere Passwort an
assert mindestlaenge(0)("") is True, f'mindestlaenge(0)("") liefert {mindestlaenge(0)("")!r}, erwartet war True.'

# enthaelt_eines gibt eine Funktion zurück
ergebnis = enthaelt_eines("0123456789")
assert ist_funktion(ergebnis, 'enthaelt_eines("0123456789")') == "", ist_funktion(ergebnis, 'enthaelt_eines("0123456789")')

# Das Beispiel: enthaelt_eines mit Ziffern
regel = enthaelt_eines("0123456789")
bekommen = (regel("ohneziffer"), regel("sommer2025"))
assert bekommen == (False, True), (
    f'enthaelt_eines("0123456789") liefert für "ohneziffer" und "sommer2025" {bekommen}, erwartet war (False, True).'
)

# Das Zeichen darf irgendwo stehen, auch ganz vorn oder ganz hinten
regel = enthaelt_eines("!?#")
bekommen = (regel("!abc"), regel("abc#"), regel("ab?c"), regel("abc"))
assert bekommen == (True, True, True, False), (
    f'enthaelt_eines("!?#") liefert für "!abc", "abc#", "ab?c" und "abc" {bekommen}, erwartet war (True, True, True, False).\n'
    "Tipp: Geben Sie False erst zurück, wenn Sie alle Zeichen des Passworts angesehen haben."
)

# Ein einziges passendes Zeichen genügt; nicht alle Zeichen müssen vorkommen
regel = enthaelt_eines("xyz")
assert regel("box") is True, (
    f'enthaelt_eines("xyz")("box") liefert {regel("box")!r}, erwartet war True: ein x genügt.'
)

# Leeres Passwort und leerer Zeichenvorrat
bekommen = (enthaelt_eines("abc")(""), enthaelt_eines("")("abc"))
assert bekommen == (False, False), (
    f'enthaelt_eines("abc")("") und enthaelt_eines("")("abc") liefern {bekommen}, erwartet war (False, False).'
)

# alle gibt eine Funktion zurück
ergebnis = alle([mindestlaenge(1)])
assert ist_funktion(ergebnis, "alle([mindestlaenge(1)])") == "", ist_funktion(ergebnis, "alle([mindestlaenge(1)])")

# Das Beispiel: alle mit zwei Regeln
normal = alle([mindestlaenge(10), enthaelt_eines("0123456789")])
bekommen = (normal("sommer2025"), normal("sommersonne"), normal("kurz1"))
assert bekommen == (True, False, False), (
    'normal = alle([mindestlaenge(10), enthaelt_eines("0123456789")]) liefert für "sommer2025", '
    f'"sommersonne" und "kurz1" {bekommen}, erwartet war (True, False, False).'
)

# Auch die letzte Regel der Liste zählt
streng = alle([mindestlaenge(1), mindestlaenge(2), enthaelt_eines("!")])
assert streng("ab") is False, (
    f'alle([mindestlaenge(1), mindestlaenge(2), enthaelt_eines("!")])("ab") liefert {streng("ab")!r}, erwartet war False.\n'
    "Tipp: Geben Sie True erst zurück, wenn alle Regeln geprüft sind."
)

# Leere Liste: jedes Passwort ist in Ordnung
assert alle([])("") is True, f'alle([])("") liefert {alle([])("")!r}, erwartet war True.'

# Regeln lassen sich verschachteln
admin = alle([alle([mindestlaenge(16)]), enthaelt_eines("0123456789"), enthaelt_eines("!?#$%&")])
bekommen = (admin("Rechenzentrum#2025"), admin("Rechenzentrum2025"), admin("kurz#1"))
assert bekommen == (True, False, False), (
    "admin = alle([alle([mindestlaenge(16)]), enthaelt_eines(Ziffern), enthaelt_eines(\"!?#$%&\")]) liefert für "
    f'"Rechenzentrum#2025", "Rechenzentrum2025" und "kurz#1" {bekommen}, erwartet war (True, False, False).'
)

# Viele zufällige Regeln und Passwörter, verglichen mit einer direkten Prüfung
zufall = Zufall(3032)
vorrat = "abcXYZ0129!?# "
for _ in range(300):
    n = zufall.randint(0, 12)
    zeichen = "".join(zufall.choice(vorrat) for _ in range(zufall.randint(0, 4)))
    passwort = "".join(zufall.choice(vorrat) for _ in range(zufall.randint(0, 14)))
    lang_ok = len(passwort) >= n
    zeichen_ok = any(buchstabe in zeichen for buchstabe in passwort)
    bekommen = (mindestlaenge(n)(passwort), enthaelt_eines(zeichen)(passwort), alle([mindestlaenge(n), enthaelt_eines(zeichen)])(passwort))
    erwartet = (lang_ok, zeichen_ok, lang_ok and zeichen_ok)
    assert bekommen == erwartet, (
        f"Für n = {n}, zeichen = {zeichen!r} und passwort = {passwort!r} liefern mindestlaenge(n), "
        f"enthaelt_eines(zeichen) und alle([beide]) {bekommen}, erwartet war {erwartet}."
    )

# Obere Grenze: 20 Regeln, Passwörter mit 100 Zeichen, viele Aufrufe derselben Regel
regeln = [mindestlaenge(laenge) for laenge in range(0, 100, 10)]
regeln = regeln + [enthaelt_eines(chr(ord("a") + nummer) * 5) for nummer in range(10)]
gesamt = alle(regeln)
gut = "abcdefghij" * 10
fehlt_j = "abcdefghi" + "x" * 91
bekommen = [gesamt(gut), gesamt(fehlt_j), gesamt(gut[:89])]
for _ in range(200):
    bekommen.append(gesamt(gut))
assert bekommen[:3] == [True, False, False] and all(bekommen[3:]), (
    "alle mit 20 Regeln (Mindestlängen 0 bis 90 und je ein Buchstabe von a bis j): erwartet True für "
    "\"abcdefghij\" * 10, False ohne j und False bei 89 Zeichen, und bei 200 weiteren Aufrufen immer True; "
    f"bekommen {bekommen[:3]}, danach {'immer True' if all(bekommen[3:]) else 'nicht immer True'}."
)
