# Automatisch erzeugt aus lehrkraft/muster/4_016_formularpruefung.py - nicht von Hand ändern.
# vorlage-hash: a206df2da987b321
# text-hash: 44563867b66eab4e
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
    ({"a": "x", "b": "", "c": "   "}, ["c", "b", "a"], ["c", "b"]),
    ({"a": "x"}, [], []),
    ({}, [], []),
    ({"a": " x "}, ["a"], []),
]:
    ergebnis = fehlende_felder(formular, pflicht)
    assert ergebnis == erwartet, f"fehlende_felder({formular}, {pflicht}) ergibt {ergebnis!r}, erwartet war {erwartet}."

def alter_aus(text):
    """Ruft lies_alter(text) auf; ein ValueError wird zum Text, damit die Meldung ihn zeigen kann."""
    try:
        return lies_alter(text)
    except ValueError as fehler:
        return f"ValueError: {fehler}"


TIPP_ALTER = (
    "Tipp: Erst strip(), dann isdecimal(), dann die Obergrenze 150 prüfen "
    "(isdigit() lässt auch Zeichen wie ² durch, mit denen int() nichts anfangen kann)."
)

# lies_alter aus dem Beispiel
for text, erwartet in [(" 36 ", 36), ("zwölf", None)]:
    ergebnis = alter_aus(text)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"lies_alter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n{TIPP_ALTER}"
    )

# lies_alter an den Rändern 0 und 150, mit führenden Nullen
for text, erwartet in [("0", 0), ("150", 150), ("007", 7), ("151", None)]:
    ergebnis = alter_aus(text)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"lies_alter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n{TIPP_ALTER}"
    )

# lies_alter: leere Texte
for text, erwartet in [("", None), ("   ", None)]:
    ergebnis = alter_aus(text)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"lies_alter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n{TIPP_ALTER}"
    )

# lies_alter: negative Zahlen, Kommazahlen und Rechnungen
for text, erwartet in [("-5", None), ("3.5", None), ("3 6", None), ("10**9", None)]:
    ergebnis = alter_aus(text)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"lies_alter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n{TIPP_ALTER}"
    )

# lies_alter: Zeichen, die int() durchgehen lässt oder an denen int() scheitert
for text, erwartet in [("²", None), (" +5 ", None), ("1_0", None)]:
    ergebnis = alter_aus(text)
    assert ergebnis == erwartet and type(ergebnis) is type(erwartet), (
        f"lies_alter({text!r}) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n{TIPP_ALTER}"
    )

# meldungen aus dem Beispiel
formular = {"name": "Ada Lovelace", "alter": "zwölf", "email": "  "}
ergebnis = meldungen(formular, ["name", "email"], {"email": "Ohne E-Mail können wir nicht antworten."})
erwartet = [
    ("email", "Ohne E-Mail können wir nicht antworten."),
    ("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an."),
]
assert vergleichbar(str(ergebnis)) == vergleichbar(str(erwartet)), f"meldungen(...) aus dem Beispiel ergibt\n{ergebnis!r}\nerwartet war\n{erwartet!r}"

# Ohne hinweise kommt der Standardtext
try:
    ergebnis = meldungen({"alter": "36"}, ["name", "email"])
except AttributeError as fehler:
    ergebnis = f"AttributeError: {fehler}"
erwartet = [("name", "Bitte füllen Sie das Feld „name“ aus."), ("email", "Bitte füllen Sie das Feld „email“ aus.")]
assert vergleichbar(str(ergebnis)) == vergleichbar(str(erwartet)), (
    f"meldungen({{'alter': '36'}}, ['name', 'email']) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Ist hinweise None, gibt es keine eigenen Meldungen; hinweise.get(...) geht dann nicht."
)

# Ein Hinweis nur für manche Felder, Hinweise für ausgefüllte Felder erscheinen nicht
ergebnis = meldungen({"name": "Bo"}, ["name", "email", "telefon"], {"name": "Name?", "telefon": "Nummer bitte."})
erwartet = [("email", "Bitte füllen Sie das Feld „email“ aus."), ("telefon", "Nummer bitte.")]
assert vergleichbar(str(ergebnis)) == vergleichbar(str(erwartet)), f"meldungen mit Hinweisen für name und telefon ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Das Alter: leer oder fehlend ergibt keine Altersmeldung
for formular, pflicht, erwartet in [({"alter": ""}, [], []), ({"alter": "  "}, [], []), ({}, [], [])]:
    ergebnis = meldungen(formular, pflicht, None)
    assert vergleichbar(str(ergebnis)) == vergleichbar(str(erwartet)), (
        f"meldungen({formular}, {pflicht}, None) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
        "Tipp: Die Altersmeldung gibt es nur, wenn das Feld alter ausgefüllt ist."
    )

# Das Alter als Pflichtfeld: gültig ergibt keine Meldung, 151 die Altersmeldung
for formular, pflicht, erwartet in [
    ({"alter": " 99 "}, ["alter"], []),
    ({"alter": "151"}, ["alter"], [("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an.")]),
]:
    ergebnis = meldungen(formular, pflicht, None)
    assert vergleichbar(str(ergebnis)) == vergleichbar(str(erwartet)), f"meldungen({formular}, {pflicht}, None) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# Fehlt das Alter als Pflichtfeld, kommt nur die Pflichtmeldung
formular, pflicht = {"alter": " "}, ["alter"]
erwartet = [("alter", "Bitte füllen Sie das Feld „alter“ aus.")]
ergebnis = meldungen(formular, pflicht, None)
assert vergleichbar(str(ergebnis)) == vergleichbar(str(erwartet)), (
    f"meldungen({formular}, {pflicht}, None) ergibt {ergebnis!r}, erwartet war {erwartet!r}.\n"
    "Tipp: Ein Alter aus Leerzeichen fehlt nur; eine zweite Meldung zum Alter gibt es dann nicht."
)

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
fehler_bei = {}  # Name der Funktion → Meldung zum ersten falschen Ergebnis
for _ in range(300):
    formular = {}
    for feld in zufall.sample(FELDER, zufall.randint(0, 5)):
        formular[feld] = zufall.choice(["", " ", "Ada", " x ", str(zufall.randint(0, 200)), "-3", "1.5", " 42 "])
    pflicht = zufall.sample(FELDER, zufall.randint(0, 5))
    hinweise = zufall.choice([None, {}, {zufall.choice(FELDER): "Eigener Hinweis."}])
    fehlend = [feld for feld in pflicht if not formular.get(feld, "").split()]
    erwartet = [(feld, (hinweise or {}).get(feld, f"Bitte füllen Sie das Feld „{feld}“ aus.")) for feld in fehlend]
    alter = formular.get("alter", "").strip()
    if alter and not (alter.isdecimal() and int(alter) <= 150):
        erwartet.append(("alter", "Bitte geben Sie das Alter als ganze Zahl von 0 bis 150 an."))
    ergebnis = fehlende_felder(formular, pflicht)
    if ergebnis != fehlend and "fehlende_felder" not in fehler_bei:
        fehler_bei["fehlende_felder"] = f"fehlende_felder({formular}, {pflicht}) ergibt {ergebnis!r}, erwartet war {fehlend}."
    ergebnis = meldungen(formular, pflicht, hinweise)
    if vergleichbar(str(ergebnis)) != vergleichbar(str(erwartet)) and "meldungen" not in fehler_bei:
        fehler_bei["meldungen"] = f"meldungen({formular}, {pflicht}, {hinweise}) ergibt {ergebnis!r}, erwartet war {erwartet!r}."

# 300 zufällige Formulare: fehlende_felder
assert "fehlende_felder" not in fehler_bei, fehler_bei.get("fehlende_felder")

# 300 zufällige Formulare: meldungen
assert "meldungen" not in fehler_bei, fehler_bei.get("meldungen")

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
assert vergleichbar(AUSGABE) == vergleichbar(erwartete_ausgabe), f"Erwartete Ausgabe:\n{erwartete_ausgabe}\nIhr Programm:\n{AUSGABE}"
