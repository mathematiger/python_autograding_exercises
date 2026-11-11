# Automatisch erzeugt aus lehrkraft/muster/2_011_kontosperre.py - nicht von Hand ändern.
# vorlage-hash: 24f9f966f28fd477
# text-hash: db5ddde2bc191b9a
# thema: funktionen
# inhalt: Standardwerte für Parameter

TIPP_RETURN = (
    "\nTipp: Ihre Funktion gibt nichts zurück. Fehlt ein return (auch return 0, wenn es keine Sperre gibt), "
    "oder steht dort print?"
)


def tipp_zum_ergebnis(argumente, ergebnis):
    """Sucht zum falschen Ergebnis von sperrzeit(*argumente) den Tipp, der zum Fehlerbild passt; sonst ""."""
    standardwerte = (3, 5)
    fehlversuche, erlaubt, minuten = argumente + standardwerte[len(argumente) - 1 :]
    # Mit vertauschten Parametern landet das zweite Argument in minuten und das dritte in erlaubt.
    if len(argumente) == 3:
        erlaubt_vertauscht = minuten
    else:
        erlaubt_vertauscht = 3
    if ergebnis is None:
        return TIPP_RETURN
    if not isinstance(ergebnis, int):
        return ""
    if ergebnis < 0:
        return "\nTipp: Bei höchstens erlaubt vielen Fehlversuchen ist die Sperrzeit 0, nicht negativ."
    if ergebnis == max(0, fehlversuche - 3) * minuten:
        return "\nTipp: Rechnen Sie mit dem Parameter erlaubt, nicht fest mit 3."
    if ergebnis == max(0, fehlversuche - erlaubt_vertauscht) * erlaubt:
        return (
            "\nTipp: Die Argumente werden von links nach rechts verteilt. "
            "Steht im Funktionskopf erst erlaubt und dann minuten?"
        )
    if ergebnis == max(0, fehlversuche - erlaubt) * 5:
        return "\nTipp: Rechnen Sie mit dem Parameter minuten, nicht fest mit 5."
    return ""


# Mit den Standardwerten sperren 5 Fehlversuche 10 Minuten lang
try:
    ergebnis = sperrzeit(5)
    fehler = None
except TypeError as ausnahme:
    ergebnis = None
    fehler = ausnahme
if fehler is None:
    meldung = (
        f"sperrzeit(5) ergibt {ergebnis!r}, erwartet war 10 (2 Fehlversuche mehr als die 3 erlaubten, je 5 Minuten)."
        + tipp_zum_ergebnis((5,), ergebnis)
    )
elif "positional argument" in str(fehler):
    meldung = (
        f"Der Aufruf sperrzeit(5) löst {fehler!r} aus.\n"
        "Tipp: Stehen die Standardwerte erlaubt=3 und minuten=5 im Funktionskopf?"
    )
else:
    meldung = f"Der Aufruf sperrzeit(5) löst {fehler!r} aus."
assert fehler is None and ergebnis == 10, meldung

# Bis zur erlaubten Zahl gibt es keine Sperre
for fehlversuche in [0, 1, 2, 3]:
    ergebnis = sperrzeit(fehlversuche)
    if ergebnis is None:
        hinweis = TIPP_RETURN
    else:
        hinweis = (
            "\nTipp: Gesperrt wird erst, wenn fehlversuche größer als erlaubt ist; "
            "genau 3 Fehlversuche sind noch erlaubt."
        )
    assert ergebnis == 0, f"sperrzeit({fehlversuche}) ergibt {ergebnis!r}, erwartet war 0.{hinweis}"

# Weitere Fehlversuche mit den Standardwerten (nicht fest 10 hinschreiben!)
for fehlversuche, erwartet in [(4, 5), (6, 15), (13, 50)]:
    ergebnis = sperrzeit(fehlversuche)
    assert ergebnis == erwartet, (
        f"sperrzeit({fehlversuche}) ergibt {ergebnis!r}, erwartet war {erwartet}."
        + tipp_zum_ergebnis((fehlversuche,), ergebnis)
    )

# Ein angegebener Wert für erlaubt ersetzt den Standardwert
for argumente, erwartet in [((5, 4), 5), ((5, 5), 0), ((8, 0), 40), ((2, 1), 5), ((4, 6), 0)]:
    ergebnis = sperrzeit(*argumente)
    assert ergebnis == erwartet, (
        f"sperrzeit{argumente} ergibt {ergebnis!r}, erwartet war {erwartet}." + tipp_zum_ergebnis(argumente, ergebnis)
    )

# Auch minuten lässt sich angeben
for argumente, erwartet in [((5, 1, 30), 120), ((4, 3, 60), 60), ((2, 3, 60), 0)]:
    ergebnis = sperrzeit(*argumente)
    assert ergebnis == erwartet, (
        f"sperrzeit{argumente} ergibt {ergebnis!r}, erwartet war {erwartet}." + tipp_zum_ergebnis(argumente, ergebnis)
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Normales Konto, 5 Fehlversuche: 10 Minuten\n"
    "Administratorkonto, 5 Fehlversuche: 120 Minuten"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Aufrufe mit einem, zwei oder drei Argumenten
zufall = Zufall(2010)


def langsame_sperrzeit(fehlversuche, erlaubt, minuten):
    """Vergleichsrechnung: geht jeden Fehlversuch einzeln durch und zählt ab dem ersten zu viel Minuten dazu."""
    gesamt = 0
    for versuch in range(1, fehlversuche + 1):
        if versuch > erlaubt:
            gesamt = gesamt + minuten
    return gesamt


for _ in range(300):
    fehlversuche = zufall.randint(0, 30)
    erlaubt = zufall.randint(0, 10)
    minuten = zufall.randint(1, 60)
    for aufruf, ergebnis, erwartet in [
        (f"sperrzeit({fehlversuche})", sperrzeit(fehlversuche), langsame_sperrzeit(fehlversuche, 3, 5)),
        (
            f"sperrzeit({fehlversuche}, {erlaubt})",
            sperrzeit(fehlversuche, erlaubt),
            langsame_sperrzeit(fehlversuche, erlaubt, 5),
        ),
        (
            f"sperrzeit({fehlversuche}, {erlaubt}, {minuten})",
            sperrzeit(fehlversuche, erlaubt, minuten),
            langsame_sperrzeit(fehlversuche, erlaubt, minuten),
        ),
    ]:
        assert ergebnis == erwartet, f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet}."

# An den Grenzen
for aufruf, ergebnis, erwartet in [
    ("sperrzeit(100)", sperrzeit(100), 485),
    ("sperrzeit(100, 0, 60)", sperrzeit(100, 0, 60), 6000),
    ("sperrzeit(100, 99, 1)", sperrzeit(100, 99, 1), 1),
    ("sperrzeit(100, 100, 60)", sperrzeit(100, 100, 60), 0),
    ("sperrzeit(0, 0, 1)", sperrzeit(0, 0, 1), 0),
]:
    assert ergebnis == erwartet, f"{aufruf} ergibt {ergebnis!r}, erwartet war {erwartet}."
