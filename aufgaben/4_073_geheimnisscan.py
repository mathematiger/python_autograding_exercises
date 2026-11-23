"""Aufgabe 4_073 – Geheimnisscan                                 Stufe 4 ★★★★☆

Eine Firma will ein internes Werkzeug als Open Source veröffentlichen.
Bevor der Projektordner hochgeladen wird, prüft die IT-Sicherheit, ob
darin Geheimnisse stecken, die nicht an die Öffentlichkeit dürfen:
private Schlüssel (Dateien mit der Endung .pem oder .key), Dateien
namens .env, in denen Zugangsdaten für den Entwicklungsrechner stehen,
und Passwörter, die jemand direkt in den Quelltext oder eine
Konfigurationsdatei geschrieben hat. Ein Projektordner sieht etwa so
aus:

    projekt/
        README.txt
        .env
        src/
            app.py           (Zeile 4: DB_PASSWORT = "geheim")
            config.cfg       (Zeile 2: password=admin123)
        zertifikate/
            server.pem
            server.crt
        bilder/
            logo.png

Schreiben Sie mit pathlib und tempfile drei Funktionen. Pfade im
Ergebnis sind relativ zum Projektordner und mit / geschrieben, auch
unter Windows.

- `verdaechtige_dateien(ordner)` gibt die alphabetisch sortierte Liste
  aller Dateien in ordner und allen Unterordnern zurück, die auf .pem
  oder .key enden oder genau .env heißen. Ordner zählen nicht mit.
- `fundstellen(ordner)` liest alle Dateien mit der Endung .py, .cfg,
  .ini oder .txt und gibt ein Dictionary zurück, das jeder Datei mit
  Fund die Liste der Zeilennummern (ab 1) zuordnet, in denen passwort=
  oder password= steht. Groß- und Kleinschreibung und Leerzeichen zählen
  dabei nicht: Auch DB_PASSWORT = "geheim" ist ein Fund. Die Schlüssel
  stehen alphabetisch sortiert im Dictionary, Dateien ohne Fund fehlen.
- `schreibe_bericht(funde, ziel)` schreibt den Bericht in die Datei
  ziel: eine Zeile je Datei aus funde in der Form pfad: 3, 7, oder die
  eine Zeile keine Funde. Damit nie ein halber Bericht herumliegt, falls
  das Programm mittendrin abbricht, schreibt sie erst in eine temporäre
  Datei im selben Ordner wie ziel und ersetzt danach ziel durch diese
  Datei. Danach liegt außer ziel keine neue Datei im Ordner.

    verdaechtige_dateien(projekt)   →  [".env", "zertifikate/server.pem"]
    fundstellen(projekt)            →  {"src/app.py": [4], "src/config.cfg": [2]}
    schreibe_bericht(fundstellen(projekt), projekt / "bericht.txt")
    bericht.txt:
        src/app.py: 4
        src/config.cfg: 2

Grenzen: ordner und ziel sind pathlib.Path-Objekte; ordner existiert,
der Ordner von ziel auch. Der Projektordner enthält 0 bis 500 Dateien in
bis zu fünf Ebenen von Unterordnern, Namen aus Buchstaben, Ziffern, ._-
und ohne Leerzeichen, Endungen klein geschrieben. Die Dateien mit den
vier Endungen sind Text in UTF-8 mit bis zu 1000 Zeilen; alle anderen
können beliebige Bytes enthalten und werden nicht gelesen. ziel darf
schon existieren und wird dann ersetzt.

Hintergrund: Mit open und with haben Sie in Aufgabe 3_046 und 3_048
Dateien gelesen und geschrieben, Pfade waren dort Texte. Das Modul
pathlib macht einen Pfad zu einem Objekt, das seine Teile kennt und
mit dem Operator / zusammengesetzt wird, ohne dass man sich um \\ oder /
kümmern muss:

    from pathlib import Path

    pfad = Path("projekt") / "src" / "app.py"
    pfad.name, pfad.suffix, pfad.stem     →  ("app.py", ".py", "app")
    pfad.parent                           →  Path("projekt/src")
    pfad.relative_to("projekt")           →  Path("src/app.py")
    pfad.relative_to("projekt").as_posix()  →  "src/app.py"
    pfad.exists(), pfad.is_file(), pfad.is_dir()

ordner.iterdir() liefert den Inhalt eines Ordners, ordner.glob("*.py")
die passenden Einträge darin und ordner.rglob("*") alles in allen
Unterordnern, jeweils als Path-Objekte in beliebiger Reihenfolge (also
sortieren). rglob findet auch Dateien, deren Name mit einem Punkt
beginnt. Ein Path kann sich selbst lesen und schreiben; das öffnet und
schließt die Datei in einem Schritt:

    text = pfad.read_text(encoding="utf-8")
    pfad.write_text("Hallo\\n", encoding="utf-8")
    pfad.replace(anderer_pfad)            # umbenennen, ein vorhandenes Ziel wird ersetzt

Das Modul tempfile legt Dateien und Ordner mit Namen an, die es noch
nicht gibt. tempfile.TemporaryDirectory() als with-Block ist ein
Ordner, der am Ende samt Inhalt gelöscht wird; das Programm unten und
die Tests bauen darin ihre Projektordner. tempfile.NamedTemporaryFile
öffnet eine neue Datei; mit dir= liegt sie in einem bestimmten Ordner,
mit delete=False bleibt sie nach dem Schließen erhalten:

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=ordner,
                                     suffix=".tmp", delete=False) as datei:
        datei.write(inhalt)
    Path(datei.name).replace(ordner / "fertig.txt")

datei.name ist der volle Pfad der temporären Datei. Weil replace im
selben Ordner nur einen Namen umträgt, sieht jedes andere Programm
entweder den alten oder den ganzen neuen Inhalt, nie einen halben. So
speichern auch Editoren und Datenbanken ihre Dateien.
"""

import tempfile
from pathlib import Path

ENDUNGEN_GEHEIM = (".pem", ".key")
ENDUNGEN_TEXT = (".py", ".cfg", ".ini", ".txt")
MERKMALE = ("passwort=", "password=")


def verdaechtige_dateien(ordner):
    """Gibt die sortierten relativen Pfade aller Schlüsseldateien und .env-Dateien zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def fundstellen(ordner):
    """Gibt für jede Textdatei mit Passwort-Fund die Zeilennummern zurück, nach Pfad sortiert."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def schreibe_bericht(funde, ziel):
    """Schreibt den Bericht über eine temporäre Datei im selben Ordner nach ziel."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def baue_beispiel(projekt):
    """Legt den Beispiel-Projektordner aus dem Aufgabentext an."""
    (projekt / "src").mkdir()
    (projekt / "zertifikate").mkdir()
    (projekt / "bilder").mkdir()
    (projekt / "README.txt").write_text("Werkzeug zum Zählen von Tickets\n", encoding="utf-8")
    (projekt / ".env").write_text("TOKEN=abc123\n", encoding="utf-8")
    (projekt / "src" / "app.py").write_text(
        'import sqlite3\n\nDB_NAME = "tickets.db"\nDB_PASSWORT = "geheim"\n', encoding="utf-8"
    )
    (projekt / "src" / "config.cfg").write_text("[datenbank]\npassword=admin123\n", encoding="utf-8")
    (projekt / "zertifikate" / "server.pem").write_text("-----BEGIN PRIVATE KEY-----\n", encoding="utf-8")
    (projekt / "zertifikate" / "server.crt").write_text("-----BEGIN CERTIFICATE-----\n", encoding="utf-8")
    (projekt / "bilder" / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n\xff\xfe")


with tempfile.TemporaryDirectory() as name:
    projekt = Path(name)
    baue_beispiel(projekt)
    print(verdaechtige_dateien(projekt))
    funde = fundstellen(projekt)
    print(funde)
    schreibe_bericht(funde, projekt / "bericht.txt")
    print((projekt / "bericht.txt").read_text(encoding="utf-8"))
