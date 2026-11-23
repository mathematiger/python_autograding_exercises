"""Aufgabe 4_068 – Kontenprüfung                                 Stufe 4 ★★★★☆

Einmal im Quartal prüft die IT-Sicherheit eines Unternehmens alle
Benutzerkonten: Wer hat Administratorrechte, und gehört er überhaupt
zur eigenen Firma? Dienstkonten, unter denen Programme laufen (etwa die
Datensicherung), sollen getrennt aufgelistet werden. Der Export aus dem
Verzeichnisdienst ist leider unordentlich: Groß- und Kleinschreibung
wechseln, und manche Felder haben Leerzeichen am Rand.

    konto           email                       gruppen
    "  M.Meier"     "M.Meier@Firma.de "         "mail;vpn"
    "svc_backup"    "backup@firma.de"           "admin;backup"
    "A.Schulz "     "a.schulz@partner-it.com"   "mail;admin"
    "T.Kraus"       "t.kraus@Partner-IT.com"    "mail;sysadmin-lesen"
    "SVC_Monitor"   "monitor@firma.de"          "monitoring"
    "extern1"       " Support@Partner-IT.com"   "admin"

gruppen ist ein Text mit den Namen der Gruppen des Kontos, getrennt
durch Semikolons. Administratorrechte hat ein Konto, wenn eine seiner
Gruppen genau admin heißt; sysadmin-lesen zählt nicht. Ein Dienstkonto
erkennt man daran, dass sein bereinigter Name mit svc_ beginnt.

Schreiben Sie vier Funktionen. Jede bekommt den DataFrame konten mit
den drei Spalten oben und verändert ihn nicht. Benutzen Sie für die
Texte die .str-Methoden von pandas, keine Schleife über die Zeilen.

- `bereinigt(konten)` gibt eine Kopie zurück, in der konto und email
  ohne Leerzeichen am Rand und in Kleinbuchstaben stehen.
- `mit_domain(konten)` gibt wie bereinigt eine Kopie zurück, dazu eine
  letzte Spalte domain mit dem Teil der bereinigten E-Mail-Adresse
  hinter dem @.
- `dienstkonten(konten)` gibt die Zeilen der Dienstkonten aus bereinigt
  zurück, mit dem Index 0, 1, 2, …
- `admins_extern(konten, eigene_domain)` gibt die Liste der bereinigten
  Kontonamen mit Administratorrechten zurück, deren Domain nicht
  eigene_domain ist, alphabetisch sortiert.

    bereinigt(konten)["konto"].tolist()
    →  ["m.meier", "svc_backup", "a.schulz", "t.kraus", "svc_monitor", "extern1"]
    mit_domain(konten)["domain"].tolist()
    →  ["firma.de", "firma.de", "partner-it.com", "partner-it.com", "firma.de", "partner-it.com"]
    dienstkonten(konten)["konto"].tolist()    →  ["svc_backup", "svc_monitor"]
    admins_extern(konten, "firma.de")         →  ["a.schulz", "extern1"]

Grenzen: konten hat 0 bis 10 000 Zeilen und keine fehlenden Werte.
konto ist ein Text mit mindestens einem Zeichen außer Leerzeichen, email
enthält genau ein @ mit Zeichen davor und danach (außer Leerzeichen am
Rand). gruppen besteht aus 0 bis 10 Gruppennamen in Kleinbuchstaben
ohne Leerzeichen, getrennt durch ";", und kann leer sein ("").
eigene_domain ist in Kleinbuchstaben.

Hintergrund: Eine Textspalte in pandas hat das Attribut .str. Darüber
erreicht man fast alle Methoden, die Sie von Python-Texten kennen, nur
dass sie auf jede Zelle der Spalte zugleich wirken und eine neue Spalte
(Series) zurückgeben:

    namen = pd.Series(["  Ada ", "BOB", "carla"])
    namen.str.strip()                  →  ["Ada", "BOB", "carla"]
    namen.str.strip().str.lower()      →  ["ada", "bob", "carla"]
    namen.str.len()                    →  [6, 3, 5]
    namen.str.startswith("B")          →  [False, True, False]

Weil jede .str-Methode wieder eine Textspalte liefert, kann man sie
hintereinanderhängen; Methoden wie startswith oder contains liefern
eine Spalte aus True und False, also eine Maske wie in Aufgabe 3_041.
split zerlegt jede Zelle in eine Liste, und .str[i] holt aus jeder
Liste (oder jedem Text) das Element an der Stelle i:

    adressen = pd.Series(["a@x.de", "b@y.com"])
    adressen.str.split("@")            →  [["a", "x.de"], ["b", "y.com"]]
    adressen.str.split("@").str[1]     →  ["x.de", "y.com"]

contains(muster) fragt je Zelle, ob ein regulärer Ausdruck (Aufgabe
4_067) irgendwo passt; mit regex=False sucht es nur den Text selbst.
Soll ein Wort genau als eigener Eintrag vorkommen, hilft nur der
reguläre Ausdruck; regex=False findet es auch in sysadmin:

    rollen = pd.Series(["lesen;admin", "sysadmin", "admin"])
    rollen.str.contains("admin", regex=False)   →  [True, True, True]
    rollen.str.contains(r"(?:^|;)admin(?:;|$)") →  [True, False, True]

^ und $ stehen für Anfang und Ende des Texts, a|b passt auf a oder auf b,
und (?:...) fasst zusammen (Aufgabe 4_067); (?:^|;) heißt also
„Textanfang oder Semikolon“. Zusammen mit assign aus
Aufgabe 4_054 entsteht so eine Kette ohne eine einzige Schleife:

    df.assign(name=lambda d: d["name"].str.strip().str.lower())

Die .str-Methoden sind kürzer und lesbarer als apply mit einer eigenen
Funktion (schneller sind sie bei Texten kaum, denn auch sie gehen Zelle
für Zelle durch), und sie überspringen fehlende Werte, statt mit einem
Fehler abzubrechen.
"""

import pandas as pd


def bereinigt(konten):
    """Gibt eine Kopie mit bereinigten Spalten konto und email zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def mit_domain(konten):
    """Gibt die bereinigte Kopie mit der zusätzlichen Spalte domain zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def dienstkonten(konten):
    """Gibt die bereinigten Zeilen der Dienstkonten zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def admins_extern(konten, eigene_domain):
    """Gibt die sortierten Namen der Administratorkonten aus fremden Domains zurück."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


konten = pd.DataFrame(
    {
        "konto": ["  M.Meier", "svc_backup", "A.Schulz ", "T.Kraus", "SVC_Monitor", "extern1"],
        "email": [
            "M.Meier@Firma.de ",
            "backup@firma.de",
            "a.schulz@partner-it.com",
            "t.kraus@Partner-IT.com",
            "monitor@firma.de",
            " Support@Partner-IT.com",
        ],
        "gruppen": ["mail;vpn", "admin;backup", "mail;admin", "mail;sysadmin-lesen", "monitoring", "admin"],
    }
)
print(mit_domain(konten)["domain"].tolist())
print(dienstkonten(konten)["konto"].tolist())
print(admins_extern(konten, "firma.de"))
