# Automatisch erzeugt aus lehrkraft/muster/4_068_kontenpruefung.py - nicht von Hand ändern.
# vorlage-hash: 9dd55e2d1624d33e
# text-hash: 3157411274adc0b0
# thema: datenanalyse
# inhalt: pandas: .str-Methoden

import pandas as pd

SPALTEN = ["konto", "email", "gruppen"]
BEISPIEL = [
    ("  M.Meier", "M.Meier@Firma.de ", "mail;vpn"),
    ("svc_backup", "backup@firma.de", "admin;backup"),
    ("A.Schulz ", "a.schulz@partner-it.com", "mail;admin"),
    ("T.Kraus", "t.kraus@Partner-IT.com", "mail;sysadmin-lesen"),
    ("SVC_Monitor", "monitor@firma.de", "monitoring"),
    ("extern1", " Support@Partner-IT.com", "admin"),
]


def tabelle(zeilen):
    """Baut den DataFrame konten, auch wenn zeilen leer ist."""
    return pd.DataFrame(zeilen, columns=SPALTEN).astype(str)


def ergebnis_von(aufruf):
    """Führt den Aufruf aus; ein Fehler wird als Text zurückgegeben."""
    try:
        return aufruf()
    except Exception as fehler:
        return f"{type(fehler).__name__}: {fehler}"


def sauber(text):
    """Vergleichslösung: ein Text ohne Rand-Leerzeichen in Kleinbuchstaben."""
    return text.strip().lower()


def erwartet_bereinigt(zeilen):
    """Vergleichslösung für bereinigt als Liste von Dictionaries."""
    return [{"konto": sauber(k), "email": sauber(e), "gruppen": g} for k, e, g in zeilen]


def erwartet_mit_domain(zeilen):
    """Vergleichslösung für mit_domain als Liste von Dictionaries."""
    return [dict(zeile, domain=zeile["email"].partition("@")[2]) for zeile in erwartet_bereinigt(zeilen)]


def erwartet_dienst(zeilen):
    """Vergleichslösung für dienstkonten als Liste von Dictionaries."""
    return [zeile for zeile in erwartet_bereinigt(zeilen) if zeile["konto"][:4] == "svc_"]


def erwartet_admins(zeilen, eigene_domain):
    """Vergleichslösung für admins_extern."""
    namen = []
    for zeile in erwartet_mit_domain(zeilen):
        if "admin" in zeile["gruppen"].split(";") and zeile["domain"] != eigene_domain:
            namen.append(zeile["konto"])
    return sorted(namen)


def datensaetze(ergebnis):
    """Ein DataFrame als Liste von Dictionaries, sonst eine Beschreibung des Ergebnisses."""
    if isinstance(ergebnis, pd.DataFrame):
        return ergebnis.to_dict("records")
    if isinstance(ergebnis, str):
        return ergebnis
    return f"keinen DataFrame, sondern {type(ergebnis).__name__}: {ergebnis!r}"


def spalte(ergebnis, name):
    """Die Spalte name als Liste, sonst eine Beschreibung des Ergebnisses."""
    if isinstance(ergebnis, pd.DataFrame) and name in ergebnis.columns:
        return ergebnis[name].tolist()
    if isinstance(ergebnis, pd.DataFrame):
        return f"keine Spalte {name!r}, nur {list(ergebnis.columns)}"
    return datensaetze(ergebnis)


def zufallszeilen(zufall, anzahl):
    """Erzeugt unordentliche Kontozeilen mit Gruppen, Dienstkonten und fremden Domains."""
    zeilen = []
    for nummer in range(anzahl):
        name = zufall.choice(["svc_", "Svc_", "SVC_", "sv_", "", "x"]) + zufall.choice(["Ab", "cd", "EF"]) + str(nummer)
        domain = zufall.choice(["firma.de", "Firma.DE", "partner-it.com", "firma.de.example"])
        rand = zufall.choice(["", " ", "  "])
        gruppen = zufall.sample(["admin", "sysadmin-lesen", "mail", "vpn", "admins", "admin-alt"], zufall.randint(0, 3))
        zeilen.append((rand + name + zufall.choice(["", " "]), f"{rand}{name}@{domain}{rand}", ";".join(gruppen)))
    return zeilen


# bereinigt: konto im Beispiel
ergebnis = ergebnis_von(lambda: bereinigt(tabelle(BEISPIEL)))
werte = spalte(ergebnis, "konto")
erwartet = ["m.meier", "svc_backup", "a.schulz", "t.kraus", "svc_monitor", "extern1"]
assert werte == erwartet, (
    f"bereinigt(konten)['konto'] ergibt {werte!r}, erwartet war {erwartet}.\n"
    "Tipp: konten['konto'].str.strip().str.lower()."
)

# bereinigt: email im Beispiel
werte = spalte(ergebnis, "email")
erwartet = [zeile["email"] for zeile in erwartet_bereinigt(BEISPIEL)]
assert werte == erwartet, f"bereinigt(konten)['email'] ergibt {werte!r}, erwartet war {erwartet}."

# bereinigt: dieselben Spalten in derselben Reihenfolge, gruppen unverändert
assert datensaetze(ergebnis) == erwartet_bereinigt(BEISPIEL), (
    f"bereinigt(konten) ergibt\n{datensaetze(ergebnis)}\nerwartet war\n{erwartet_bereinigt(BEISPIEL)}"
)

# bereinigt verändert konten nicht
konten = tabelle(BEISPIEL)
ergebnis_von(lambda: bereinigt(konten))
assert konten.equals(tabelle(BEISPIEL)), (
    "Nach bereinigt(konten) hat sich konten verändert. Geben Sie mit assign oder copy() eine neue Tabelle zurück."
)

# bereinigt: leere Tabelle
ergebnis = ergebnis_von(lambda: bereinigt(tabelle([])))
assert isinstance(ergebnis, pd.DataFrame) and list(ergebnis.columns) == SPALTEN and len(ergebnis) == 0, (
    f"bereinigt einer leeren Tabelle ergibt {datensaetze(ergebnis)!r}; erwartet war eine leere Tabelle mit {SPALTEN}."
)

# mit_domain: die Domains im Beispiel
ergebnis = ergebnis_von(lambda: mit_domain(tabelle(BEISPIEL)))
werte = spalte(ergebnis, "domain")
erwartet = ["firma.de", "firma.de", "partner-it.com", "partner-it.com", "firma.de", "partner-it.com"]
assert werte == erwartet, (
    f"mit_domain(konten)['domain'] ergibt {werte!r}, erwartet war {erwartet}.\n"
    "Tipp: Die bereinigte email mit .str.split('@') zerlegen und mit .str[1] den Teil dahinter nehmen."
)

# mit_domain: domain ist die letzte Spalte, konto und email sind bereinigt
assert datensaetze(ergebnis) == erwartet_mit_domain(BEISPIEL), (
    f"mit_domain(konten) ergibt\n{datensaetze(ergebnis)}\nerwartet war\n{erwartet_mit_domain(BEISPIEL)}"
)

# mit_domain verändert konten nicht
konten = tabelle(BEISPIEL)
ergebnis_von(lambda: mit_domain(konten))
assert konten.equals(tabelle(BEISPIEL)), "Nach mit_domain(konten) hat sich konten verändert."

# dienstkonten: das Beispiel
ergebnis = ergebnis_von(lambda: dienstkonten(tabelle(BEISPIEL)))
werte = spalte(ergebnis, "konto")
assert werte == ["svc_backup", "svc_monitor"], (
    f"dienstkonten(konten)['konto'] ergibt {werte!r}, erwartet war ['svc_backup', 'svc_monitor'].\n"
    "Tipp: Prüfen Sie den bereinigten Namen mit .str.startswith('svc_'); SVC_Monitor zählt mit."
)

# dienstkonten: ganze Zeilen aus bereinigt, Index 0, 1, …
erwartet = erwartet_dienst(BEISPIEL)
assert datensaetze(ergebnis) == erwartet and list(ergebnis.index) == [0, 1], (
    f"dienstkonten(konten) ergibt\n{datensaetze(ergebnis)}\nmit dem Index "
    f"{list(ergebnis.index) if isinstance(ergebnis, pd.DataFrame) else '–'}; erwartet war\n{erwartet}\n"
    "mit dem Index [0, 1].\nTipp: reset_index(drop=True)."
)

# dienstkonten: der Name muss mit svc_ beginnen, nicht es nur enthalten
zeilen = [("altsvc_x", "a@firma.de", ""), ("svc-x", "b@firma.de", ""), (" svc_y ", "c@firma.de", "")]
ergebnis = ergebnis_von(lambda: dienstkonten(tabelle(zeilen)))
assert spalte(ergebnis, "konto") == ["svc_y"], (
    f"dienstkonten mit den Namen ['altsvc_x', 'svc-x', ' svc_y '] ergibt {spalte(ergebnis, 'konto')!r}, "
    "erwartet war ['svc_y'].\nTipp: startswith statt contains, und vorher strip()."
)

# dienstkonten: keine Dienstkonten
ergebnis = ergebnis_von(lambda: dienstkonten(tabelle(BEISPIEL[:1])))
assert isinstance(ergebnis, pd.DataFrame) and len(ergebnis) == 0, (
    f"dienstkonten ohne Dienstkonten ergibt {datensaetze(ergebnis)!r}; erwartet war eine leere Tabelle."
)

# admins_extern: das Beispiel
ergebnis = ergebnis_von(lambda: admins_extern(tabelle(BEISPIEL), "firma.de"))
assert ergebnis == ["a.schulz", "extern1"], (
    f"admins_extern(konten, 'firma.de') ergibt {ergebnis!r}, erwartet war ['a.schulz', 'extern1'].\n"
    "Tipp: Administratorrechte zeigt eine Gruppe, die genau admin heißt; vergleichen Sie die Domain aus mit_domain."
)

# admins_extern: andere eigene Domain (nicht fest hinschreiben!)
ergebnis = ergebnis_von(lambda: admins_extern(tabelle(BEISPIEL), "partner-it.com"))
assert ergebnis == ["svc_backup"], f"admins_extern(konten, 'partner-it.com') ergibt {ergebnis!r}, erwartet war ['svc_backup']."

# admins_extern: sysadmin-lesen und admins sind keine Administratorrechte
zeilen = [
    ("a", "a@x.de", "sysadmin-lesen"),
    ("b", "b@x.de", "admins"),
    ("c", "c@x.de", "admin-alt;mail"),
    ("d", "d@x.de", "mail;admin"),
    ("e", "e@x.de", "admin;mail"),
]
ergebnis = ergebnis_von(lambda: admins_extern(tabelle(zeilen), "firma.de"))
assert ergebnis == ["d", "e"], (
    f"Mit den Gruppen ['sysadmin-lesen', 'admins', 'admin-alt;mail', 'mail;admin', 'admin;mail'] ergibt "
    f"admins_extern {ergebnis!r}, erwartet war ['d', 'e'].\n"
    "Tipp: str.contains('admin') findet admin auch in sysadmin; suchen Sie mit (?:^|;)admin(?:;|$)."
)

# admins_extern: nur genau die eigene Domain ist intern
zeilen = [("a", "a@firma.de.example", "admin"), ("b", "b@Firma.de", "admin"), ("c", "c@partner-firma.de", "admin")]
ergebnis = ergebnis_von(lambda: admins_extern(tabelle(zeilen), "firma.de"))
assert ergebnis == ["a", "c"], (
    f"Mit den E-Mail-Adressen ['a@firma.de.example', 'b@Firma.de', 'c@partner-firma.de'] ergibt "
    f"admins_extern(…, 'firma.de') {ergebnis!r}, erwartet war ['a', 'c'].\n"
    "Tipp: Vergleichen Sie die ganze bereinigte Domain mit ==, nicht mit endswith oder in."
)

# admins_extern: leere Gruppen
ergebnis = ergebnis_von(lambda: admins_extern(tabelle([("a", "a@x.de", "")]), "firma.de"))
assert ergebnis == [], f"Ein Konto ohne Gruppen ergibt in admins_extern {ergebnis!r}, erwartet war []."

# admins_extern: leere Tabelle
ergebnis = ergebnis_von(lambda: admins_extern(tabelle([]), "firma.de"))
assert ergebnis == [], f"admins_extern einer leeren Tabelle ergibt {ergebnis!r}, erwartet war []."

# Die Ausgabe des Programms
erwartet = "\n".join(
    str(teil)
    for teil in [
        [zeile["domain"] for zeile in erwartet_mit_domain(BEISPIEL)],
        [zeile["konto"] for zeile in erwartet_dienst(BEISPIEL)],
        erwartet_admins(BEISPIEL, "firma.de"),
    ]
)
assert vergleichbar(AUSGABE) == vergleichbar(erwartet), f"Erwartete Ausgabe:\n{erwartet}\nIhr Programm:\n{AUSGABE}"

# Viele zufällige Kontenlisten
zufall = Zufall(4068)
for _ in range(60):
    zeilen = zufallszeilen(zufall, zufall.randint(0, 8))
    konten = tabelle(zeilen)
    for name, ergebnis, erwartet in [
        ("bereinigt", datensaetze(ergebnis_von(lambda: bereinigt(konten))), erwartet_bereinigt(zeilen)),
        ("mit_domain", datensaetze(ergebnis_von(lambda: mit_domain(konten))), erwartet_mit_domain(zeilen)),
        ("dienstkonten", datensaetze(ergebnis_von(lambda: dienstkonten(konten))), erwartet_dienst(zeilen)),
        ("admins_extern", ergebnis_von(lambda: admins_extern(konten, "firma.de")), erwartet_admins(zeilen, "firma.de")),
    ]:
        assert ergebnis == erwartet, f"Für die Zeilen\n{zeilen}\nergibt {name}\n{ergebnis}\nerwartet war\n{erwartet}"

# Obere Grenze: 10 000 Konten
zeilen = zufallszeilen(zufall, 10000)
konten = tabelle(zeilen)
assert datensaetze(ergebnis_von(lambda: dienstkonten(konten))) == erwartet_dienst(zeilen), (
    "Bei 10 000 Konten stimmt dienstkonten nicht."
)

# Obere Grenze: admins_extern bei 10 000 Konten
assert ergebnis_von(lambda: admins_extern(konten, "firma.de")) == erwartet_admins(zeilen, "firma.de"), (
    "Bei 10 000 Konten stimmt admins_extern nicht."
)
