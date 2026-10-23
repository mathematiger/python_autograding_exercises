# Automatisch erzeugt aus lehrkraft/muster/24_ticketnummer.py - nicht von Hand ändern.
# vorlage-hash: 270bf060d1e48919

EINGABEN = ["Meier", "4711"]

# Bei Eingabe Meier und 4711 bekommt die Störung die Nummer INC-4712
assert AUSGABE == "Hallo Meier, Ihre Störung hat die Nummer INC-4712.", (
    'Bei Eingabe Meier und 4711 erwartet: "Hallo Meier, Ihre Störung hat die Nummer INC-4712."\n'
    f'Ihr Programm: "{AUSGABE}"\n'
    "Tipp: Mit + kommt kein Leerzeichen dazu. Vor dem Komma und hinter INC- darf keines stehen, "
    "hinter Hallo und vor INC- muss eines im Text stehen."
)

# Ein anderer Name erscheint in der Ausgabe (nicht fest Meier hinschreiben!)
ausgabe_name = starte("Yılmaz", "4711")
assert ausgabe_name == "Hallo Yılmaz, Ihre Störung hat die Nummer INC-4712.", (
    'Bei Eingabe Yılmaz und 4711 erwartet: "Hallo Yılmaz, Ihre Störung hat die Nummer INC-4712."\n'
    f'Ihr Programm: "{ausgabe_name}"\n'
    "Tipp: Hängen Sie die Variable name an, nicht einen festen Namen."
)

# Die Nummer ist um eins größer als die letzte (nicht fest 4712 hinschreiben!)
ausgabe_nummer = starte("Schulz", "99")
assert ausgabe_nummer == "Hallo Schulz, Ihre Störung hat die Nummer INC-100.", (
    'Bei Eingabe Schulz und 99 erwartet: "Hallo Schulz, Ihre Störung hat die Nummer INC-100."\n'
    f'Ihr Programm: "{ausgabe_nummer}"\n'
    'Tipp: Die neue Nummer steht schon in der Variablen nummer. Mit str(nummer) wird sie zu einem Text, den Sie an "INC-" hängen können.'
)

# Eine größere Nummer wird ebenso zusammengesetzt
ausgabe_gross = starte("Nowak", "20399")
assert ausgabe_gross == "Hallo Nowak, Ihre Störung hat die Nummer INC-20400.", (
    'Bei Eingabe Nowak und 20399 erwartet: "Hallo Nowak, Ihre Störung hat die Nummer INC-20400."\n'
    f'Ihr Programm: "{ausgabe_gross}"'
)
