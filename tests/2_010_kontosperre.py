# Automatisch erzeugt aus lehrkraft/muster/2_010_kontosperre.py - nicht von Hand ändern.
# vorlage-hash: 9502258bbd361e3a
# thema: funktionen
# inhalt: Standardwerte für Parameter

# Mit den Standardwerten sperren 5 Fehlversuche 10 Minuten lang
try:
    ergebnis = sperrzeit(5)
    fehler = None
except TypeError as ausnahme:
    ergebnis = None
    fehler = ausnahme
if fehler is not None:
    hinweis = f"\nIhr Aufruf löst {fehler!r} aus. Stehen die Standardwerte erlaubt=3 und minuten=5 im Funktionskopf?"
else:
    hinweis = ""
assert ergebnis == 10, f"sperrzeit(5) ergibt {ergebnis!r}, erwartet war 10 (2 Versuche über 3, je 5 Minuten).{hinweis}"

# Bis zur erlaubten Zahl gibt es keine Sperre
for fehlversuche in [0, 1, 2, 3]:
    ergebnis = sperrzeit(fehlversuche)
    assert ergebnis == 0, (
        f"sperrzeit({fehlversuche}) ergibt {ergebnis!r}, erwartet war 0.\n"
        "Tipp: Gesperrt wird erst, wenn fehlversuche größer als erlaubt ist; genau 3 Fehlversuche sind noch erlaubt."
    )

# Weitere Fehlversuche mit den Standardwerten (nicht fest 10 hinschreiben!)
for fehlversuche, erwartet in [(4, 5), (6, 15), (13, 50)]:
    ergebnis = sperrzeit(fehlversuche)
    assert ergebnis == erwartet, f"sperrzeit({fehlversuche}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# Ein angegebener Wert für erlaubt ersetzt den Standardwert
for argumente, erwartet in [((5, 4), 5), ((5, 5), 0), ((8, 0), 40)]:
    ergebnis = sperrzeit(*argumente)
    assert ergebnis == erwartet, (
        f"sperrzeit{argumente} ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Rechnen Sie mit dem Parameter erlaubt, nicht fest mit 3."
    )

# Auch minuten lässt sich angeben
for argumente, erwartet in [((5, 1, 30), 120), ((4, 3, 60), 60), ((2, 3, 60), 0)]:
    ergebnis = sperrzeit(*argumente)
    assert ergebnis == erwartet, (
        f"sperrzeit{argumente} ergibt {ergebnis!r}, erwartet war {erwartet}.\n"
        "Tipp: Rechnen Sie mit dem Parameter minuten, nicht fest mit 5."
    )

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "Normales Konto, 5 Fehlversuche: 10 Minuten\n"
    "Administratorkonto, 5 Fehlversuche: 120 Minuten"
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
