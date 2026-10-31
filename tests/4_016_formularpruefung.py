# Automatisch erzeugt aus lehrkraft/muster/4_016_formularpruefung.py - nicht von Hand ändern.
# vorlage-hash: a206df2da987b321
# text-hash: 99a577a36dca3caf
# thema: programmaufbau
# inhalt: Typannotationen, `X | None`

import inspect
import types
import typing


def form(typ):
    """Bringt eine Annotation in eine vergleichbare Form, sodass Optional[int] und int | None gleich sind."""
    herkunft = typing.get_origin(typ)
    if herkunft is None:
        return typ
    teile = [form(teil) for teil in typing.get_args(typ)]
    if herkunft in (typing.Union, types.UnionType):
        return ("oder", frozenset(teile))
    return (herkunft, tuple(teile))


def annotationen(funktion):
    """Gibt die Annotationen der Funktion in vergleichbarer Form zurück, bei einem Fehler dessen Text."""
    try:
        return {name: form(typ) for name, typ in typing.get_type_hints(funktion).items()}
    except Exception as fehler:
        return f"nicht lesbar ({fehler})"


def zeige(typen):
    """Schreibt erwartete Annotationen lesbar auf."""
    return ", ".join(f"{name}: {text}" for name, text in typen.items())


# fehlende_felder ist annotiert
ergebnis = annotationen(fehlende_felder)
erwartet = {"formular": form(dict[str, str]), "pflicht": form(list[str]), "return": form(list[str])}
assert ergebnis == erwartet, (
    f"Die Annotationen von fehlende_felder sind {typing.get_type_hints(fehlende_felder) if isinstance(ergebnis, dict) else ergebnis}; "
    f"erwartet war {zeige({'formular': 'dict[str, str]', 'pflicht': 'list[str]', 'return': 'list[str]'})}.\n"
    "Tipp: Die Rückgabe annotieren Sie mit -> vor dem Doppelpunkt der def-Zeile."
)

# lies_alter ist annotiert, die Rückgabe kann None sein
ergebnis = annotationen(lies_alter)
erwartet = {"text": str, "return": form(int | None)}
assert ergebnis == erwartet, (
    f"Die Annotationen von lies_alter sind {typing.get_type_hints(lies_alter) if isinstance(ergebnis, dict) else ergebnis}; "
    "erwartet war text: str und eine Rückgabe, die eine ganze Zahl oder None ist.\n"
    "Tipp: „Zahl oder None“ schreibt man int | None."
)

# meldungen ist annotiert, hinweise darf None sein
ergebnis = annotationen(meldungen)
erwartet = {
    "formular": form(dict[str, str]),
    "pflicht": form(list[str]),
    "hinweise": form(dict[str, str] | None),
    "return": form(list[tuple[str, str]]),
}
assert ergebnis == erwartet, (
    f"Die Annotationen von meldungen sind {typing.get_type_hints(meldungen) if isinstance(ergebnis, dict) else ergebnis}; "
    "erwartet waren formular und pflicht wie bei fehlende_felder, hinweise als Dictionary von Texten auf Texte "
    "oder None, und als Rückgabe eine Liste von Paaren aus zwei Texten.\n"
    "Tipp: Ein Paar aus zwei Texten ist tuple[str, str]."
)

# Der Standardwert von hinweise ist None
standard = inspect.signature(meldungen).parameters["hinweise"].default if "hinweise" in inspect.signature(meldungen).parameters else "fehlt"
assert standard is None, f"Der Parameter hinweise von meldungen soll den Standardwert None haben, hat aber {standard!r}."

# fehlende_felder aus dem Beispiel
formular = {"name": "Ada Lovelace", "alter": "zwölf", "email": "  "}
ergebnis = fehlende_felder(formular, ["name", "email", "telefon"])
assert ergebnis == ["email", "telefon"], (
    f"fehlende_felder(formular, ['name', 'email', 'telefon']) ergibt {ergebnis!r}, erwartet war ['email', 'telefon'].\n"
    "Tipp: Ein Feld fehlt auch, wenn es nur Leerzeichen enthält; formular.get(feld, \"\").strip() hilft."
)

# Reihenfolge von pflicht, leere Fälle
for formular, pflicht, erwartet in [
    ({}, ["c", "a", "b"], ["c", "a", "b"]),
    ({"a": "x", "b": "", "c": "\t"}, ["c", "b", "a"], ["c", "b"]),
    ({"a": "x"}, [], []),
    ({}, [], []),
    ({"a": " x "}, ["a"], []),
]:
    ergebnis = fehlende_felder(formular, pflicht)
    assert ergebnis == erwartet, f"fehlende_felder({formular}, {pflicht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

# lies_alter: gültige und ungültige Texte
for text, erwartet in [
    (" 36 ", 36), ("0", 0), ("150", 150), ("007", 7), ("151", None), ("zwölf", None),
    ("", None), ("   ", None), ("-5", None), ("3.5", None), ("3 6", None), ("10**9", None),
]:
    ergebnis = lies_alter(text)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"lies_alter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Erst strip(), dann isdigit(), dann die Obergrenze 150 prüfen."
    )

# meldungen aus dem Beispiel
formular = {"name": "Ada Lovelace", "alter": "zwölf", "email": "  "}
ergebnis = meldungen(formular, ["name", "email"], {"email": "Ohne E-Mail können wir nicht antworten."})
erwartet = [
    ("email", "Ohne E-Mail können wir nicht antworten."),
    ("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an."),
]
assert ergebnis == erwartet, f"meldungen(...) aus dem Beispiel ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# Ohne hinweise kommt der Standardtext
ergebnis = meldungen({"alter": "36"}, ["name", "email"])
erwartet = [("name", "Bitte füllen Sie das Feld „name“ aus."), ("email", "Bitte füllen Sie das Feld „email“ aus.")]
assert ergebnis == erwartet, (
    f"meldungen({{'alter': '36'}}, ['name', 'email']) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Ist hinweise None, gibt es keine eigenen Meldungen; hinweise.get(...) geht dann nicht."
)

# Ein Hinweis nur für manche Felder, Hinweise für ausgefüllte Felder erscheinen nicht
ergebnis = meldungen({"name": "Bo"}, ["name", "email", "telefon"], {"name": "Name?", "telefon": "Nummer bitte."})
erwartet = [("email", "Bitte füllen Sie das Feld „email“ aus."), ("telefon", "Nummer bitte.")]
assert ergebnis == erwartet, f"meldungen mit Hinweisen für name und telefon ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Das Alter: leer, fehlend und gültig ergibt keine Altersmeldung; fehlt es als Pflichtfeld, nur die Pflichtmeldung
for formular, pflicht, erwartet in [
    ({"alter": ""}, [], []),
    ({"alter": "  "}, [], []),
    ({}, [], []),
    ({"alter": " 99 "}, ["alter"], []),
    ({"alter": " "}, ["alter"], [("alter", "Bitte füllen Sie das Feld „alter“ aus.")]),
    ({"alter": "151"}, ["alter"], [("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an.")]),
]:
    ergebnis = meldungen(formular, pflicht, None)
    assert ergebnis == erwartet, f"meldungen({formular}, {pflicht}, None) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# meldungen ändert hinweise und formular nicht
formular = {"alter": "x"}
hinweise = {"name": "Name?"}
meldungen(formular, ["name"], hinweise)
assert formular == {"alter": "x"} and hinweise == {"name": "Name?"}, (
    f"Nach meldungen(...) sind formular {formular!r} und hinweise {hinweise!r}; beide sollen unverändert bleiben."
)

# 300 zufällige Formulare
zufall = Zufall(4016)
FELDER = ["name", "email", "telefon", "firma", "alter"]
for _ in range(300):
    formular = {}
    for feld in zufall.sample(FELDER, zufall.randint(0, 5)):
        formular[feld] = zufall.choice(["", " ", "Ada", " x ", str(zufall.randint(0, 200)), "-3", "1.5", " 42 "])
    pflicht = zufall.sample(FELDER, zufall.randint(0, 5))
    hinweise = zufall.choice([None, {}, {zufall.choice(FELDER): "Eigener Hinweis."}])
    fehlend = [feld for feld in pflicht if not formular.get(feld, "").split()]
    erwartet = [(feld, (hinweise or {}).get(feld, f"Bitte füllen Sie das Feld „{feld}“ aus.")) for feld in fehlend]
    alter = formular.get("alter", "").strip()
    if alter and not (alter.isdigit() and int(alter) <= 150):
        erwartet.append(("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an."))
    ergebnis = fehlende_felder(formular, pflicht)
    assert ergebnis == fehlend, f"fehlende_felder({formular}, {pflicht}) ergibt {ergebnis!r}, erwartet war {fehlend}."
    ergebnis = meldungen(formular, pflicht, hinweise)
    assert ergebnis == erwartet, f"meldungen({formular}, {pflicht}, {hinweise}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# An der oberen Grenze: 1000 Felder, jedes zweite leer
formular = {f"feld{nummer}": ("x" if nummer % 2 else " " * 100) for nummer in range(1000)}
pflicht = [f"feld{nummer}" for nummer in range(999, -1, -1)]
ergebnis = meldungen(formular, pflicht)
assert len(ergebnis) == 500 and ergebnis[0][0] == "feld998" and ergebnis[-1][0] == "feld0", (
    f"Bei 1000 Pflichtfeldern, von denen jedes zweite leer ist, liefert meldungen {len(ergebnis)} Meldungen, "
    f"die erste für {ergebnis[0][0] if ergebnis else None!r}; erwartet waren 500, die erste für 'feld998'."
)

# Die Ausgabe des Programms stimmt
erwartete_ausgabe = (
    "['email', 'telefon']\n"
    "36 None\n"
    "email: Ohne E-Mail können wir nicht antworten.\n"
    "alter: Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an."
)
assert AUSGABE == erwartete_ausgabe, f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
