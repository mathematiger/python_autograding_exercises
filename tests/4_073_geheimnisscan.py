# Automatisch erzeugt aus lehrkraft/muster/4_073_geheimnisscan.py - nicht von Hand ändern.
# vorlage-hash: 379e07b73e833907
# text-hash: 047f0db9fefc728b
# thema: texte_zahlen
# inhalt: pathlib und tempfile

import os

BEISPIEL = {
    "README.txt": "Werkzeug zum Zählen von Tickets\n",
    ".env": "TOKEN=abc123\n",
    "src/app.py": 'import sqlite3\n\nDB_NAME = "tickets.db"\nDB_PASSWORT = "geheim"\n',
    "src/config.cfg": "[datenbank]\npassword=admin123\n",
    "zertifikate/server.pem": "-----BEGIN PRIVATE KEY-----\n",
    "zertifikate/server.crt": "-----BEGIN CERTIFICATE-----\n",
    "bilder/logo.png": b"\x89PNG\r\n\x1a\n\xff\xfe",
}


def baue(wurzel, dateien):
    """Legt in wurzel die Dateien an (relativer Pfad → Text oder Bytes), samt Unterordnern."""
    for relativ, inhalt in dateien.items():
        pfad = wurzel / relativ
        pfad.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(inhalt, bytes):
            pfad.write_bytes(inhalt)
        else:
            pfad.write_text(inhalt, encoding="utf-8")


def mit_projekt(dateien, funktion, ordner=()):
    """Baut ein Projekt in einem temporären Ordner und ruft funktion(projekt) auf; Fehler als Text."""
    with tempfile.TemporaryDirectory() as name:
        projekt = Path(name) / "projekt"
        projekt.mkdir()
        for unterordner in ordner:
            (projekt / unterordner).mkdir(parents=True)
        baue(projekt, dateien)
        try:
            return funktion(projekt)
        except Exception as fehler:
            return f"{type(fehler).__name__}: {fehler}"


def vergleich_verdaechtig(dateien):
    """Vergleichslösung für verdaechtige_dateien, nur über die Namen im Dictionary."""
    treffer = []
    for relativ in dateien:
        name = relativ.split("/")[-1]
        if name == ".env" or name.endswith(".pem") or name.endswith(".key"):
            treffer.append(relativ)
    return sorted(treffer)


def vergleich_funde(dateien):
    """Vergleichslösung für fundstellen, nur über die Texte im Dictionary."""
    funde = {}
    for relativ in sorted(dateien):
        if not relativ.endswith((".py", ".cfg", ".ini", ".txt")):
            continue
        nummern = []
        for nummer, zeile in enumerate(dateien[relativ].split("\n"), start=1):
            kompakt = "".join(zeile.split()).casefold()
            if "passwort=" in kompakt or "password=" in kompakt:
                nummern.append(nummer)
        if nummern:
            funde[relativ] = nummern
    return funde


BERICHTSORDNER = []


def bericht_von(funde, vorher=None):
    """Ruft schreibe_bericht in einem leeren Ordner auf; liefert (Inhalt von ziel, Dateien danach, Fehler)."""
    with tempfile.TemporaryDirectory() as name:
        ordner = Path(name)
        BERICHTSORDNER.append(ordner)
        ziel = ordner / "bericht.txt"
        if vorher is not None:
            ziel.write_text(vorher, encoding="utf-8")
        try:
            schreibe_bericht(dict(funde), ziel)
            fehler = None
        except Exception as ausnahme:
            fehler = f"{type(ausnahme).__name__}: {ausnahme}"
        inhalt = ziel.read_text(encoding="utf-8") if ziel.exists() else None
        return inhalt, sorted(os.listdir(ordner)), fehler


def zufallsprojekt(zufall):
    """Erzeugt zufällige Dateien in Unterordnern, manche mit Passwörtern."""
    dateien = {}
    namen = ["app", "main", "daten", "notiz", "server", "test", ".env", "x"]
    endungen = [".py", ".cfg", ".ini", ".txt", ".pem", ".key", ".crt", ".md", ""]
    zeilen = ["x = 1", "password=1", "PASSWORT = 'a'", "pass word=2", "# kein passwort", "Password  =x", ""]
    for _ in range(zufall.randint(0, 8)):
        tiefe = [zufall.choice(["src", "conf", "a", "b"]) for _ in range(zufall.randint(0, 3))]
        name = zufall.choice(namen)
        name = name if name == ".env" else name + zufall.choice(endungen)
        inhalt = "\n".join(zufall.choice(zeilen) for _ in range(zufall.randint(0, 5)))
        relativ = "/".join(tiefe + [name])
        if not any(relativ.startswith(vorhanden + "/") or vorhanden.startswith(relativ + "/") for vorhanden in dateien):
            dateien[relativ] = inhalt
    return dateien


# verdaechtige_dateien: das Beispiel
ergebnis = mit_projekt(BEISPIEL, verdaechtige_dateien)
assert ergebnis == [".env", "zertifikate/server.pem"], (
    f"verdaechtige_dateien(projekt) ergibt {ergebnis!r}, erwartet war ['.env', 'zertifikate/server.pem'].\n"
    'Tipp: ordner.rglob("*") liefert alle Einträge in allen Unterordnern; pfad.suffix ist die Endung.'
)

# verdaechtige_dateien: relative Pfade mit /
ergebnis = mit_projekt({"a/b/c/geheim.key": "x"}, verdaechtige_dateien)
assert ergebnis == ["a/b/c/geheim.key"], (
    f"Für die Datei a/b/c/geheim.key ergibt verdaechtige_dateien {ergebnis!r}, erwartet war ['a/b/c/geheim.key'].\n"
    "Tipp: pfad.relative_to(ordner).as_posix() macht daraus den relativen Pfad mit /."
)

# verdaechtige_dateien: alphabetisch sortiert
dateien = {"z.pem": "", "b/a.key": "", "a.key": "", "b/.env": ""}
ergebnis = mit_projekt(dateien, verdaechtige_dateien)
assert ergebnis == sorted(dateien), f"verdaechtige_dateien ergibt {ergebnis!r}, erwartet war die sortierte Liste {sorted(dateien)}."

# verdaechtige_dateien: nur genau .env und nur Dateien
dateien = {"beispiel.env.txt": "", "env": "", ".envrc": "", "server.pem.bak": "", "schluessel.key/liesmich.txt": ""}
ergebnis = mit_projekt(dateien, verdaechtige_dateien)
assert ergebnis == [], (
    f"Für {sorted(dateien)} ergibt verdaechtige_dateien {ergebnis!r}, erwartet war []: keine Datei heißt genau .env "
    "oder endet auf .pem oder .key, und schluessel.key ist ein Ordner.\nTipp: pfad.is_file() und pfad.suffix."
)

# verdaechtige_dateien: leerer Projektordner
ergebnis = mit_projekt({}, verdaechtige_dateien)
assert ergebnis == [], f"Für einen leeren Ordner ergibt verdaechtige_dateien {ergebnis!r}, erwartet war []."

# fundstellen: das Beispiel
ergebnis = mit_projekt(BEISPIEL, fundstellen)
assert ergebnis == {"src/app.py": [4], "src/config.cfg": [2]}, (
    f"fundstellen(projekt) ergibt {ergebnis!r}, erwartet war {{'src/app.py': [4], 'src/config.cfg': [2]}}.\n"
    "Tipp: Lesen Sie nur Dateien mit den vier Endungen; zeile.lower().replace(' ', '') macht den Vergleich einfach."
)

# fundstellen: mehrere Funde in einer Datei, Zeilen ab 1
dateien = {"setup.ini": "password=a\n[x]\nPassword = b\n\npasswort=c"}
ergebnis = mit_projekt(dateien, fundstellen)
assert ergebnis == {"setup.ini": [1, 3, 5]}, (
    f"Für eine Datei mit Funden in den Zeilen 1, 3 und 5 ergibt fundstellen {ergebnis!r}, "
    "erwartet war {'setup.ini': [1, 3, 5]}.\nTipp: enumerate(zeilen, start=1)."
)

# fundstellen: Groß- und Kleinschreibung und Leerzeichen zählen nicht
dateien = {"a.py": 'ADMIN_PASSWORD    =  "x"\n', "b.py": "passwort ='y'\n", "c.py": "pass_wort = 1\n"}
ergebnis = mit_projekt(dateien, fundstellen)
assert ergebnis == {"a.py": [1], "b.py": [1]}, (
    f"fundstellen ergibt {ergebnis!r}, erwartet war {{'a.py': [1], 'b.py': [1]}}.\n"
    "Tipp: Entfernen Sie erst die Leerzeichen und vergleichen Sie in Kleinbuchstaben."
)

# fundstellen: andere Dateien werden nicht gelesen
dateien = {"logo.png": b"password=\xff\xfe", "notiz.md": "password=x", "liesmich.txt": "nichts"}
ergebnis = mit_projekt(dateien, fundstellen)
assert ergebnis == {}, (
    f"fundstellen ergibt {ergebnis!r}, erwartet war {{}}: .png und .md gehören nicht zu den vier Endungen.\n"
    "Tipp: Prüfen Sie pfad.suffix, bevor Sie die Datei lesen; Bilder sind kein UTF-8-Text."
)

# fundstellen: Umlaute werden als UTF-8 gelesen
dateien = {"hinweis.txt": "Größe = 3\nÄnderung: passwort=über\n"}
ergebnis = mit_projekt(dateien, fundstellen)
assert ergebnis == {"hinweis.txt": [2]}, (
    f"fundstellen ergibt {ergebnis!r}, erwartet war {{'hinweis.txt': [2]}}.\n"
    'Tipp: read_text(encoding="utf-8").'
)

# fundstellen: Schlüssel sortiert, auch aus Unterordnern
dateien = {"z.py": "password=1", "a/b.py": "password=1", "a.cfg": "password=1"}
ergebnis = mit_projekt(dateien, fundstellen)
schluessel = list(ergebnis) if isinstance(ergebnis, dict) else ergebnis
assert schluessel == ["a.cfg", "a/b.py", "z.py"], f"Die Schlüssel von fundstellen sind {schluessel!r}, erwartet war ['a.cfg', 'a/b.py', 'z.py']."

# fundstellen: leerer Projektordner
ergebnis = mit_projekt({}, fundstellen)
assert ergebnis == {}, f"Für einen leeren Ordner ergibt fundstellen {ergebnis!r}, erwartet war {{}}."

# schreibe_bericht: das Beispiel
inhalt, danach, fehler = bericht_von({"src/app.py": [4], "src/config.cfg": [2]})
assert inhalt is not None and vergleichbar(inhalt) == vergleichbar("src/app.py: 4\nsrc/config.cfg: 2"), (
    f"Nach schreibe_bericht steht in ziel {inhalt!r}{f' (Fehler: {fehler})' if fehler else ''}, "
    "erwartet waren die Zeilen 'src/app.py: 4' und 'src/config.cfg: 2'."
)

# schreibe_bericht: eine Zeile je Datei
inhalt, danach, fehler = bericht_von({"a.py": [1, 3, 5], "b/c.ini": [2]})
zeilen = inhalt.strip().split("\n") if isinstance(inhalt, str) else inhalt
assert zeilen is not None and len(zeilen) == 2 and vergleichbar(zeilen[0]) == vergleichbar("a.py: 1, 3, 5"), (
    f"Für {{'a.py': [1, 3, 5], 'b/c.ini': [2]}} steht in ziel {inhalt!r}, erwartet waren zwei Zeilen, die erste "
    "'a.py: 1, 3, 5'."
)

# schreibe_bericht: keine Funde
inhalt, danach, fehler = bericht_von({})
assert inhalt is not None and vergleichbar(inhalt) == vergleichbar("keine Funde"), (
    f"Ohne Funde steht in ziel {inhalt!r}, erwartet war 'keine Funde'."
)

# schreibe_bericht: keine temporäre Datei bleibt liegen
inhalt, danach, fehler = bericht_von({"a.py": [1]})
assert danach == ["bericht.txt"], (
    f"Nach schreibe_bericht liegen im Ordner {danach}, erwartet war nur ['bericht.txt'].\n"
    "Tipp: Ersetzen Sie ziel mit Path(datei.name).replace(ziel) durch die temporäre Datei."
)

# schreibe_bericht: ein alter Bericht wird ersetzt
inhalt, danach, fehler = bericht_von({"neu.py": [7]}, vorher="alt.py: 1\nnoch.py: 2\n")
assert inhalt is not None and vergleichbar(inhalt) == vergleichbar("neu.py: 7") and danach == ["bericht.txt"], (
    f"Nach schreibe_bericht über einen alten Bericht steht in ziel {inhalt!r}, im Ordner liegen {danach}; "
    "erwartet war nur 'neu.py: 7' in bericht.txt."
)

# schreibe_bericht: erst in eine temporäre Datei, dann ersetzen
assert (verwendet("NamedTemporaryFile") or verwendet("mkstemp")) and (verwendet("replace") or verwendet("rename")), (
    "schreibe_bericht soll erst mit tempfile.NamedTemporaryFile(…, dir=ziel.parent, delete=False) in eine "
    "temporäre Datei schreiben und sie dann mit replace an die Stelle von ziel setzen."
)

# schreibe_bericht: die temporäre Datei liegt im selben Ordner wie ziel
erzeugt = []
eigenes_tempfile = tempfile


class Beobachter:
    """Reicht alles an tempfile weiter und merkt sich, in welchem Ordner temporäre Dateien entstehen."""

    def __getattr__(self, name):
        """Gibt die Funktion aus tempfile zurück, bei NamedTemporaryFile und mkstemp eine beobachtete."""
        original = getattr(eigenes_tempfile, name)
        if name not in ("NamedTemporaryFile", "mkstemp"):
            return original

        def beobachtet(*argumente, **schluesselwerte):
            """Merkt sich den Ordner dir= und ruft die echte Funktion auf."""
            erzeugt.append(schluesselwerte.get("dir"))
            return original(*argumente, **schluesselwerte)

        return beobachtet


tempfile = Beobachter()
inhalt, danach, fehler = bericht_von({"a.py": [1]})
tempfile = eigenes_tempfile
richtig = [ordner is not None and Path(ordner).resolve() == BERICHTSORDNER[-1].resolve() for ordner in erzeugt]
assert erzeugt and all(richtig) and danach == ["bericht.txt"], (
    f"schreibe_bericht hat temporäre Dateien mit dir={erzeugt} angelegt, ziel lag in {BERICHTSORDNER[-1]}; "
    "erwartet war dir=ziel.parent, damit "
    "replace nur einen Namen im selben Ordner umträgt."
)

# Die Ausgabe des Programms
erwartet = (
    "['.env', 'zertifikate/server.pem']\n{'src/app.py': [4], 'src/config.cfg': [2]}\nsrc/app.py: 4\nsrc/config.cfg: 2"
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Projektordner
zufall = Zufall(4073)
for _ in range(40):
    dateien = zufallsprojekt(zufall)
    ergebnis = mit_projekt(dateien, verdaechtige_dateien)
    assert ergebnis == vergleich_verdaechtig(dateien), (
        f"Für die Dateien {sorted(dateien)}\nergibt verdaechtige_dateien {ergebnis!r},\nerwartet war {vergleich_verdaechtig(dateien)}."
    )
    ergebnis = mit_projekt(dateien, fundstellen)
    assert ergebnis == vergleich_funde(dateien), (
        f"Für die Dateien {dateien}\nergibt fundstellen {ergebnis!r},\nerwartet war {vergleich_funde(dateien)}."
    )

# Obere Grenze: fundstellen bei 500 Dateien in fünf Ebenen
dateien = {}
for nummer in range(500):
    ebenen = "/".join(f"e{(nummer >> stelle) % 3}" for stelle in range(nummer % 6))
    name = f"d{nummer}" + [".py", ".txt", ".key", ".dat", ".pem"][nummer % 5]
    zeilen = ["x = 1"] * 999 + ["password = 'x'" if nummer % 7 == 0 else "y = 2"]
    dateien[f"{ebenen}/{name}".lstrip("/")] = "\n".join(zeilen)
ergebnis = mit_projekt(dateien, fundstellen)
assert ergebnis == vergleich_funde(dateien), "Bei 500 Dateien mit je 1000 Zeilen stimmt fundstellen nicht."

# Obere Grenze: verdaechtige_dateien bei 500 Dateien
ergebnis = mit_projekt(dateien, verdaechtige_dateien)
assert ergebnis == vergleich_verdaechtig(dateien), "Bei 500 Dateien stimmt verdaechtige_dateien nicht."
