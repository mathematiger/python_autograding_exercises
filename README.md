# Python-Aufgaben

Programmieraufgaben mit automatischer Prüfung. Kein Server, kein Konto nötig (außer Sie wollen über GitHub abgeben). Sie können Aufgaben **lösen** und auch **eigene Aufgaben erstellen** und für alle hochladen.

Die Aufgaben bilden zusammen einen vollständigen Python-Kurs zum Selbststudium in fünf Stufen. Jeden Morgen kommen zu jeder Stufe 1 bis 5 zwei neue Aufgaben hinzu. Jede Aufgabe erklärt im Abschnitt „Hintergrund“ das, was neu ist; wer eine Stufe von oben nach unten löst, hat ihren Stoff gesehen.

## Aufgaben

Der Name jeder Aufgabe beginnt mit ihrer Stufe, danach folgt die Nummer innerhalb der Stufe: `2_005_wuerfel` ist die fünfte Aufgabe der Stufe 2. So stehen die Aufgaben im Ordner nach Schwierigkeit sortiert, und innerhalb einer Stufe baut jede Aufgabe auf den vorherigen auf.

Ihren Stand sehen Sie mit `python pruefe.py --liste`: alle Aufgaben nach Thema, mit ✓ bestanden, ✗ offen und ○ unbearbeitet. Mit `python pruefe.py --liste funktionen` oder `python pruefe.py --liste 2` nur ein Thema oder eine Stufe.

<!-- AUFGABEN-ANFANG: erzeugt von erstelle_aufgaben.py, nicht von Hand ändern -->

### Nach Thema

| Thema | Stufe 1 | Stufe 2 | Stufe 3 | Stufe 4 | Stufe 5 | Prüfen mit |
| --- | --- | --- | --- | --- | --- | --- |
| [Texte, Zahlen & Dateien](#thema-texte_zahlen) | 15 | 3 |  |  |  | `python pruefe.py texte_zahlen` |
| [Bedingungen & Schleifen](#thema-kontrollfluss) | 1 | 5 |  |  |  | `python pruefe.py kontrollfluss` |
| [Funktionen](#thema-funktionen) |  | 6 |  |  |  | `python pruefe.py funktionen` |
| [Algorithmen & Rekursion](#thema-algorithmen) |  | 1 | 6 |  |  | `python pruefe.py algorithmen` |
| [Fehler & Testen](#thema-fehler) |  |  | 6 |  |  | `python pruefe.py fehler` |
| [Klassen & Objekte](#thema-klassen) |  |  |  | 12 | 3 | `python pruefe.py klassen` |
| [Datenanalyse](#thema-datenanalyse) |  |  |  |  | 1 | `python pruefe.py datenanalyse` |

<a name="thema-texte_zahlen"></a>
<details>
<summary><b>Texte, Zahlen & Dateien</b> (18 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_001_hallo_welt](aufgaben/1_001_hallo_welt.py) | ★☆☆☆☆ | Text ausgeben |
| [1_002_begruessung](aufgaben/1_002_begruessung.py) | ★☆☆☆☆ | Eingabe und Ausgabe |
| [1_003_rechteck](aufgaben/1_003_rechteck.py) | ★☆☆☆☆ | Rechnen mit Variablen |
| [1_004_fahrenheit](aufgaben/1_004_fahrenheit.py) | ★☆☆☆☆ | Eingabe in Zahl umwandeln |
| [1_005_fahrzeit](aufgaben/1_005_fahrzeit.py) | ★☆☆☆☆ | Ganzzahldivision und Rest |
| [1_006_bildschirm](aufgaben/1_006_bildschirm.py) | ★☆☆☆☆ | Potenz und Wurzel |
| [1_007_usv](aufgaben/1_007_usv.py) | ★☆☆☆☆ | Runden mit round |
| [1_008_ticketnummer](aufgaben/1_008_ticketnummer.py) | ★☆☆☆☆ | Texte zusammensetzen mit + |
| [1_009_umgedrehte_uhr](aufgaben/1_009_umgedrehte_uhr.py) | ★☆☆☆☆ | Im Kreis zählen mit % |
| [1_010_testbericht](aufgaben/1_010_testbericht.py) | ★☆☆☆☆ | f-Strings mit Nachkommastellen |
| [1_011_lizenzschluessel](aufgaben/1_011_lizenzschluessel.py) | ★☆☆☆☆ | Länge und Indizes |
| [1_012_seriennummer](aufgaben/1_012_seriennummer.py) | ★☆☆☆☆ | Slicing und negative Indizes |
| [1_013_benutzername](aufgaben/1_013_benutzername.py) | ★☆☆☆☆ | String-Methoden `upper`, `lower`, `strip` |
| [1_014_protokoll](aufgaben/1_014_protokoll.py) | ★☆☆☆☆ | `replace`, `count` und `in` |
| [1_015_sensornachricht](aufgaben/1_015_sensornachricht.py) | ★☆☆☆☆ | Übung: Text zerlegen, rechnen, ausgeben |
| [2_013_kuerzel](aufgaben/2_013_kuerzel.py) | ★★☆☆☆ | Texte durchlaufen und neu aufbauen |
| [2_014_namensabgleich](aufgaben/2_014_namensabgleich.py) | ★★☆☆☆ | `split` und `join` |
| [2_015_codemetrik](aufgaben/2_015_codemetrik.py) | ★★☆☆☆ | Tabellen mit f-String-Breiten |

</details>

<a name="thema-kontrollfluss"></a>
<details>
<summary><b>Bedingungen & Schleifen</b> (6 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_016_sprintplan](aufgaben/1_016_sprintplan.py) | ★☆☆☆☆ | Vergleiche mit `>`, `==`, `<` |
| [2_001_zaehlen](aufgaben/2_001_zaehlen.py) | ★★☆☆☆ | for-Schleife |
| [2_003_gerade](aufgaben/2_003_gerade.py) | ★★☆☆☆ | if und Funktionen |
| [2_004_countdown](aufgaben/2_004_countdown.py) | ★★☆☆☆ | while-Schleife |
| [2_006_transporter](aufgaben/2_006_transporter.py) | ★★☆☆☆ | Schleife mit break |
| [2_007_stromverbrauch](aufgaben/2_007_stromverbrauch.py) | ★★☆☆☆ | Schleife mit continue |

</details>

<a name="thema-funktionen"></a>
<details>
<summary><b>Funktionen</b> (6 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [2_002_verdoppeln](aufgaben/2_002_verdoppeln.py) | ★★☆☆☆ | Funktionen mit return |
| [2_008_verfuegbarkeit](aufgaben/2_008_verfuegbarkeit.py) | ★★☆☆☆ | Hilfsfunktionen verwenden |
| [2_009_bearbeitungszeit](aufgaben/2_009_bearbeitungszeit.py) | ★★☆☆☆ | Mehrere Rückgabewerte als Tupel |
| [2_010_kontosperre](aufgaben/2_010_kontosperre.py) | ★★☆☆☆ | Standardwerte für Parameter |
| [2_011_aufwand](aufgaben/2_011_aufwand.py) | ★★☆☆☆ | Schlüsselwort-Argumente |
| [2_012_uebertragung](aufgaben/2_012_uebertragung.py) | ★★☆☆☆ | Lokale und globale Variablen |

</details>

<a name="thema-algorithmen"></a>
<details>
<summary><b>Algorithmen & Rekursion</b> (7 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [2_005_wuerfel](aufgaben/2_005_wuerfel.py) | ★★☆☆☆ | Raten und Prüfen |
| [3_001_suche](aufgaben/3_001_suche.py) | ★★★☆☆ | Lineare Suche |
| [3_002_binaere_suche](aufgaben/3_002_binaere_suche.py) | ★★★☆☆ | Binäre Suche |
| [3_003_selection_sort](aufgaben/3_003_selection_sort.py) | ★★★☆☆ | Selection Sort |
| [3_004_bubble_sort](aufgaben/3_004_bubble_sort.py) | ★★★☆☆ | Bubble Sort mit Abbruch |
| [3_005_merge_sort](aufgaben/3_005_merge_sort.py) | ★★★☆☆ | Merge Sort rekursiv |
| [3_006_adresskonflikt](aufgaben/3_006_adresskonflikt.py) | ★★★☆☆ | Laufzeit und O-Notation |

</details>

<a name="thema-fehler"></a>
<details>
<summary><b>Fehler & Testen</b> (6 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [3_007_durchlaufzeiten](aufgaben/3_007_durchlaufzeiten.py) | ★★★☆☆ | Fehler abfangen mit try/except |
| [3_008_stueckpreise](aufgaben/3_008_stueckpreise.py) | ★★★☆☆ | Mehrere except, else und finally |
| [3_009_raid](aufgaben/3_009_raid.py) | ★★★☆☆ | `raise` und Vorbedingungen |
| [3_010_reaktionszeit](aufgaben/3_010_reaktionszeit.py) | ★★★☆☆ | `assert` als Vertrag |
| [3_011_postleitzahl](aufgaben/3_011_postleitzahl.py) | ★★★☆☆ | Testfälle schreiben |
| [3_012_portbereich](aufgaben/3_012_portbereich.py) | ★★★☆☆ | Äquivalenzklassen und Grenzwerte |

</details>

<a name="thema-klassen"></a>
<details>
<summary><b>Klassen & Objekte</b> (15 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [4_001_konto](aufgaben/4_001_konto.py) | ★★★★☆ | Klassen und Invarianten |
| [4_002_abfahrt](aufgaben/4_002_abfahrt.py) | ★★★★☆ | `__repr__` und `__str__` |
| [4_003_sitzplatz](aufgaben/4_003_sitzplatz.py) | ★★★★☆ | `__eq__` und `__hash__` |
| [4_004_engpass](aufgaben/4_004_engpass.py) | ★★★★☆ | `__lt__` und `total_ordering` |
| [4_005_sprint](aufgaben/4_005_sprint.py) | ★★★★☆ | `property` mit Setter |
| [4_006_virtuelle_maschinen](aufgaben/4_006_virtuelle_maschinen.py) | ★★★★☆ | `classmethod` als Konstruktor |
| [4_007_ticketprioritaet](aufgaben/4_007_ticketprioritaet.py) | ★★★★☆ | `staticmethod` als Hilfsfunktion |
| [4_008_testfaelle](aufgaben/4_008_testfaelle.py) | ★★★★☆ | Klassenattribute als Zähler und Registry |
| [4_009_beschaffung](aufgaben/4_009_beschaffung.py) | ★★★★☆ | Vererbung, `super()` und Polymorphie |
| [4_010_messreihen](aufgaben/4_010_messreihen.py) | ★★★★☆ | Mehrfachvererbung, Mixins und MRO |
| [4_011_sicherungen](aufgaben/4_011_sicherungen.py) | ★★★★☆ | `abc.ABC` und `@abstractmethod` |
| [4_012_lizenzen](aufgaben/4_012_lizenzen.py) | ★★★★☆ | `@dataclass` und `field` |
| [5_001_deskriptor](aufgaben/5_001_deskriptor.py) | ★★★★★ | Deskriptoren |
| [5_002_eigenschaft](aufgaben/5_002_eigenschaft.py) | ★★★★★ | `property` nachbauen |
| [5_004_nachbarn](aufgaben/5_004_nachbarn.py) | ★★★★★ | `__slots__` |

</details>

<a name="thema-datenanalyse"></a>
<details>
<summary><b>Datenanalyse</b> (1 Aufgabe)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [5_003_anmeldeprotokoll](aufgaben/5_003_anmeldeprotokoll.py) | ★★★★★ | numpy: Views, Kopien, Fancy Indexing |

</details>

### Nach Stufe

<details>
<summary><b>Stufe 1 ★☆☆☆☆: Erste Schritte mit vorgegebenem Code</b> (16 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [1_001_hallo_welt](aufgaben/1_001_hallo_welt.py) | Texte, Zahlen & Dateien | Text ausgeben |
| [1_002_begruessung](aufgaben/1_002_begruessung.py) | Texte, Zahlen & Dateien | Eingabe und Ausgabe |
| [1_003_rechteck](aufgaben/1_003_rechteck.py) | Texte, Zahlen & Dateien | Rechnen mit Variablen |
| [1_004_fahrenheit](aufgaben/1_004_fahrenheit.py) | Texte, Zahlen & Dateien | Eingabe in Zahl umwandeln |
| [1_005_fahrzeit](aufgaben/1_005_fahrzeit.py) | Texte, Zahlen & Dateien | Ganzzahldivision und Rest |
| [1_006_bildschirm](aufgaben/1_006_bildschirm.py) | Texte, Zahlen & Dateien | Potenz und Wurzel |
| [1_007_usv](aufgaben/1_007_usv.py) | Texte, Zahlen & Dateien | Runden mit round |
| [1_008_ticketnummer](aufgaben/1_008_ticketnummer.py) | Texte, Zahlen & Dateien | Texte zusammensetzen mit + |
| [1_009_umgedrehte_uhr](aufgaben/1_009_umgedrehte_uhr.py) | Texte, Zahlen & Dateien | Im Kreis zählen mit % |
| [1_010_testbericht](aufgaben/1_010_testbericht.py) | Texte, Zahlen & Dateien | f-Strings mit Nachkommastellen |
| [1_011_lizenzschluessel](aufgaben/1_011_lizenzschluessel.py) | Texte, Zahlen & Dateien | Länge und Indizes |
| [1_012_seriennummer](aufgaben/1_012_seriennummer.py) | Texte, Zahlen & Dateien | Slicing und negative Indizes |
| [1_013_benutzername](aufgaben/1_013_benutzername.py) | Texte, Zahlen & Dateien | String-Methoden `upper`, `lower`, `strip` |
| [1_014_protokoll](aufgaben/1_014_protokoll.py) | Texte, Zahlen & Dateien | `replace`, `count` und `in` |
| [1_015_sensornachricht](aufgaben/1_015_sensornachricht.py) | Texte, Zahlen & Dateien | Übung: Text zerlegen, rechnen, ausgeben |
| [1_016_sprintplan](aufgaben/1_016_sprintplan.py) | Bedingungen & Schleifen | Vergleiche mit `>`, `==`, `<` |

</details>

<details>
<summary><b>Stufe 2 ★★☆☆☆: Kleine Programme selbst schreiben</b> (15 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [2_001_zaehlen](aufgaben/2_001_zaehlen.py) | Bedingungen & Schleifen | for-Schleife |
| [2_002_verdoppeln](aufgaben/2_002_verdoppeln.py) | Funktionen | Funktionen mit return |
| [2_003_gerade](aufgaben/2_003_gerade.py) | Bedingungen & Schleifen | if und Funktionen |
| [2_004_countdown](aufgaben/2_004_countdown.py) | Bedingungen & Schleifen | while-Schleife |
| [2_005_wuerfel](aufgaben/2_005_wuerfel.py) | Algorithmen & Rekursion | Raten und Prüfen |
| [2_006_transporter](aufgaben/2_006_transporter.py) | Bedingungen & Schleifen | Schleife mit break |
| [2_007_stromverbrauch](aufgaben/2_007_stromverbrauch.py) | Bedingungen & Schleifen | Schleife mit continue |
| [2_008_verfuegbarkeit](aufgaben/2_008_verfuegbarkeit.py) | Funktionen | Hilfsfunktionen verwenden |
| [2_009_bearbeitungszeit](aufgaben/2_009_bearbeitungszeit.py) | Funktionen | Mehrere Rückgabewerte als Tupel |
| [2_010_kontosperre](aufgaben/2_010_kontosperre.py) | Funktionen | Standardwerte für Parameter |
| [2_011_aufwand](aufgaben/2_011_aufwand.py) | Funktionen | Schlüsselwort-Argumente |
| [2_012_uebertragung](aufgaben/2_012_uebertragung.py) | Funktionen | Lokale und globale Variablen |
| [2_013_kuerzel](aufgaben/2_013_kuerzel.py) | Texte, Zahlen & Dateien | Texte durchlaufen und neu aufbauen |
| [2_014_namensabgleich](aufgaben/2_014_namensabgleich.py) | Texte, Zahlen & Dateien | `split` und `join` |
| [2_015_codemetrik](aufgaben/2_015_codemetrik.py) | Texte, Zahlen & Dateien | Tabellen mit f-String-Breiten |

</details>

<details>
<summary><b>Stufe 3 ★★★☆☆: Probleme zerlegen und lösen</b> (12 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [3_001_suche](aufgaben/3_001_suche.py) | Algorithmen & Rekursion | Lineare Suche |
| [3_002_binaere_suche](aufgaben/3_002_binaere_suche.py) | Algorithmen & Rekursion | Binäre Suche |
| [3_003_selection_sort](aufgaben/3_003_selection_sort.py) | Algorithmen & Rekursion | Selection Sort |
| [3_004_bubble_sort](aufgaben/3_004_bubble_sort.py) | Algorithmen & Rekursion | Bubble Sort mit Abbruch |
| [3_005_merge_sort](aufgaben/3_005_merge_sort.py) | Algorithmen & Rekursion | Merge Sort rekursiv |
| [3_006_adresskonflikt](aufgaben/3_006_adresskonflikt.py) | Algorithmen & Rekursion | Laufzeit und O-Notation |
| [3_007_durchlaufzeiten](aufgaben/3_007_durchlaufzeiten.py) | Fehler & Testen | Fehler abfangen mit try/except |
| [3_008_stueckpreise](aufgaben/3_008_stueckpreise.py) | Fehler & Testen | Mehrere except, else und finally |
| [3_009_raid](aufgaben/3_009_raid.py) | Fehler & Testen | `raise` und Vorbedingungen |
| [3_010_reaktionszeit](aufgaben/3_010_reaktionszeit.py) | Fehler & Testen | `assert` als Vertrag |
| [3_011_postleitzahl](aufgaben/3_011_postleitzahl.py) | Fehler & Testen | Testfälle schreiben |
| [3_012_portbereich](aufgaben/3_012_portbereich.py) | Fehler & Testen | Äquivalenzklassen und Grenzwerte |

</details>

<details>
<summary><b>Stufe 4 ★★★★☆: Komplexere Zusammenhänge modellieren</b> (12 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [4_001_konto](aufgaben/4_001_konto.py) | Klassen & Objekte | Klassen und Invarianten |
| [4_002_abfahrt](aufgaben/4_002_abfahrt.py) | Klassen & Objekte | `__repr__` und `__str__` |
| [4_003_sitzplatz](aufgaben/4_003_sitzplatz.py) | Klassen & Objekte | `__eq__` und `__hash__` |
| [4_004_engpass](aufgaben/4_004_engpass.py) | Klassen & Objekte | `__lt__` und `total_ordering` |
| [4_005_sprint](aufgaben/4_005_sprint.py) | Klassen & Objekte | `property` mit Setter |
| [4_006_virtuelle_maschinen](aufgaben/4_006_virtuelle_maschinen.py) | Klassen & Objekte | `classmethod` als Konstruktor |
| [4_007_ticketprioritaet](aufgaben/4_007_ticketprioritaet.py) | Klassen & Objekte | `staticmethod` als Hilfsfunktion |
| [4_008_testfaelle](aufgaben/4_008_testfaelle.py) | Klassen & Objekte | Klassenattribute als Zähler und Registry |
| [4_009_beschaffung](aufgaben/4_009_beschaffung.py) | Klassen & Objekte | Vererbung, `super()` und Polymorphie |
| [4_010_messreihen](aufgaben/4_010_messreihen.py) | Klassen & Objekte | Mehrfachvererbung, Mixins und MRO |
| [4_011_sicherungen](aufgaben/4_011_sicherungen.py) | Klassen & Objekte | `abc.ABC` und `@abstractmethod` |
| [4_012_lizenzen](aufgaben/4_012_lizenzen.py) | Klassen & Objekte | `@dataclass` und `field` |

</details>

<details>
<summary><b>Stufe 5 ★★★★★: Verstehen, wie Python arbeitet</b> (4 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [5_001_deskriptor](aufgaben/5_001_deskriptor.py) | Klassen & Objekte | Deskriptoren |
| [5_002_eigenschaft](aufgaben/5_002_eigenschaft.py) | Klassen & Objekte | `property` nachbauen |
| [5_003_anmeldeprotokoll](aufgaben/5_003_anmeldeprotokoll.py) | Datenanalyse | numpy: Views, Kopien, Fancy Indexing |
| [5_004_nachbarn](aufgaben/5_004_nachbarn.py) | Klassen & Objekte | `__slots__` |

</details>

<!-- AUFGABEN-ENDE -->

---

## Aufgaben lösen

### Variante A: Auf dem eigenen Rechner

1. **Einmalig:** Python installieren (python.org, Version 3.11 oder neuer) und diesen Ordner herunterladen (auf GitHub: grüner Knopf **Code → Download ZIP**, dann entpacken). Danach die [Bibliotheken installieren](#bibliotheken-installieren).
2. Öffnen Sie eine Datei im Ordner `aufgaben`, z. B. `1_001_hallo_welt.py`. Oben steht die Aufgabe. Ersetzen Sie die Zeile `pass  # ← Ersetzen Sie diese Zeile durch Ihren Code` durch Ihre Lösung. Speichern!
3. Abgeben und prüfen: Öffnen Sie ein Terminal im Projektordner und tippen Sie

   ```
   python pruefe.py 1_001
   ```

   (Unter macOS/Linux evtl. `python3`.) Mehrere Aufgaben auf einmal: `python pruefe.py 1_001 1_003`. Alle Aufgaben einer Stufe: `python pruefe.py 2`. Sie können auch einfach `pruefe.py` in Ihrem Editor starten, dann werden alle Aufgaben geprüft, die Sie schon bearbeitet haben.

So sieht das Ergebnis aus:

```
── 1_002_begruessung ──
✓ Begrüßung bei Eingabe "Anna"
✗ Begrüßung bei Eingabe "Bo" (nicht fest "Anna" eintippen!)
    Bei Eingabe "Bo" erwartet: "Hallo Bo!" – Ihr Programm: "Hallo Anna!"
✗ Ränder: ein Name aus einem einzigen Buchstaben und einer aus 30 Buchstaben
    Bei Eingabe "X" erwartet: "Hallo X!" – Ihr Programm: "Hallo Anna!"
✗ 40 zufällige Namen
    Bei Eingabe "FXiqhEfÜAoÜcbChEs" erwartet: "Hallo FXiqhEfÜAoÜcbChEs!" – Ihr Programm: "Hallo Anna!"
    Tipp: Fügen Sie die Variable name zwischen "Hallo " und "!" ein.
→ 1 von 4 Tests bestanden.
```

### Lösungen zum Vergleich

Zu jeder Aufgabe der Stufen 1 bis 3 liegt im Ordner `loesungen` eine Musterlösung mit einem kurzen Lösungsweg: wie man auf die Idee kommt, welche anderen Wege es gibt und wie schnell sie sind. Sehen Sie sie sich erst an, wenn Ihre eigene Lösung alle Tests besteht. `pruefe.py` zeigt Ihnen dann den Weg dorthin. Ihre Lösung darf anders aussehen, wenn sie besteht, ist sie richtig. Gerade dann lohnt der Vergleich. Die Lösungen der Stufen 4 und 5 bleiben privat.

Manche Tests prüfen auch, wie viel Arbeit Ihre Lösung macht, z. B. wie oft sie in eine Liste schaut. Steht in der Aufgabe unter `Grenzen:`, wie groß die Eingaben werden können, reicht eine Lösung, die nur bei kleinen Eingaben schnell ist, nicht aus.

### Bibliotheken installieren

Einige Aufgaben verwenden Bibliotheken für die Datenanalyse (numpy, pandas, polars, DuckDB). Installieren Sie diese einmalig. Öffnen Sie dazu ein Terminal im Projektordner ([so geht das](#erst-selbst-testen-dann-abgeben)) und tippen Sie

```
python -m pip install -r requirements.txt
```

(Unter macOS/Linux evtl. `python3`.) Das dauert ein paar Minuten. Fehlt eine Bibliothek, sagt `pruefe.py` Ihnen das. Der erste Start nach der Installation dauert etwas länger.

- **Thonny** bringt ein eigenes Python mit. Installieren Sie die Bibliotheken dort über **Extras → Pakete verwalten** (`numpy`, `pandas`, `polars`, `duckdb`), oder starten Sie `pruefe.py` im Terminal.
- **Meldung `externally-managed-environment`** (Linux, Python aus Homebrew): Legen Sie im Projektordner eine eigene Umgebung an mit `python3 -m venv .venv` und aktivieren Sie sie mit `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`). Dann den Befehl oben noch einmal. Die Umgebung aktivieren Sie in jedem neuen Terminal erneut.
- **Mit Poetry** (optional, wenn Sie es schon kennen): `poetry install`, danach `poetry run python pruefe.py 1_001`. Die Bibliotheken stehen auch in `pyproject.toml`.

### Erst selbst testen, dann abgeben

Sie können Ihre Lösung jederzeit selbst prüfen, so oft Sie wollen, bevor Sie sie über GitHub abgeben (Variante B). Dafür brauchen Sie Python und den Projektordner auf Ihrem Rechner (siehe Variante A, Schritt 1).

1. Öffnen Sie ein Terminal im Projektordner (der Ordner, in dem `pruefe.py` liegt):
   - **Windows:** Ordner im Explorer öffnen, oben in die Adresszeile `cmd` tippen, Enter.
   - **macOS:** Rechtsklick auf den Ordner → **Dienste → Neues Terminal beim Ordner**.
   - **Im Editor (z. B. VS Code, Thonny):** Ordner öffnen und dort das Terminal starten.
2. Tippen Sie `python pruefe.py 1_001` (bzw. `python3 pruefe.py 1_001`) und drücken Sie Enter. Statt `1_001` den Anfang des Namens Ihrer Aufgabe.
3. Lesen Sie die Meldungen bei ✗, ändern Sie Ihre Datei, **speichern**, und starten Sie den Befehl noch einmal.
4. Erst wenn überall ✓ steht, laden Sie die Datei hoch.

**Tipp:** Verstehen Sie nicht, was Ihr Programm macht? Kopieren Sie Ihren Code in [Python Tutor](https://pythontutor.com/visualize.html#mode=edit) und klicken Sie auf **Visualize Execution**. Dort gehen Sie Zeile für Zeile durch und sehen nach jedem Schritt, welchen Wert jede Variable hat.

Auf GitHub laufen dieselben Tests. Laden Sie neue Aufgaben am besten zusammen mit ihrer Datei aus `tests` herunter, damit Sie auch sie selbst prüfen können.

### Variante B: Über GitHub (im Browser)

1. **Einmalig:** GitHub-Konto anlegen. Auf der Seite dieses Repos oben rechts **Fork → Create fork**. Das ist jetzt Ihr eigenes Repo. Ein Fork ist öffentlich: Alle können Ihre Lösungen sehen.
2. **Einmalig:** In Ihrem Fork den Reiter **Actions** öffnen → **I understand my workflows, go ahead and enable them**. Ohne diesen Klick prüft GitHub nichts.
3. Aufgabe bearbeiten, zwei Wege:
   - **Direkt im Browser:** In Ihrem Fork `aufgaben/1_001_hallo_welt.py` öffnen → Stift-Symbol → Lösung schreiben → **Commit changes**.
   - **Datei hochladen:** Lokal bearbeiten und [selbst testen](#erst-selbst-testen-dann-abgeben), dann in Ihrem Fork den Ordner `aufgaben` öffnen → **Add file → Upload files** → Datei hineinziehen → **Commit changes**. Der Dateiname muss gleich bleiben.
4. Ergebnis ansehen: Reiter **Actions** → oberster Eintrag → unten bei **Ergebnis** steht die Auswertung. Grüner Haken = alles bestanden, rotes ✗ = noch etwas zu tun.

**Neue Aufgaben** holen Sie auf der Startseite Ihres Forks mit **Sync fork → Update branch**. Bietet GitHub dort nur **Discard commits** an, klicken Sie das **nicht** an, denn das löscht Ihre Lösungen. Das passiert nur, wenn im Original eine Aufgabe geändert wurde, die Sie schon bearbeitet haben. Fragen Sie dann Ihre Lehrkraft.

### Variante C: Mit git auf dem eigenen Rechner

Sie arbeiten in Ihrem Editor, prüfen selbst mit `pruefe.py` und laden mit `git push` hoch. GitHub prüft danach automatisch, genau wie in Variante B.

1. **Einmalig:** Python und git (git-scm.com) installieren und einen Fork anlegen wie in Variante B, Schritte 1 und 2. Dann im Terminal:

   ```
   git clone https://github.com/<Ihr-Name>/python_autograding_exercises.git
   cd python_autograding_exercises
   python -m pip install -r requirements.txt
   ```

   Der letzte Befehl installiert die [Bibliotheken](#bibliotheken-installieren).

2. Aufgabe lösen und [selbst prüfen](#erst-selbst-testen-dann-abgeben): `python pruefe.py 1_001`.
3. Hochladen:

   ```
   git add aufgaben
   git commit -m "1_001 gelöst"
   git push
   ```

   Beim ersten `git push` fragt git nach einer Anmeldung. Unter Windows öffnet sich dafür ein Browserfenster. Fragt git nach einem Passwort, funktioniert Ihr GitHub-Passwort nicht. Melden Sie sich dann einmal mit der GitHub CLI (cli.github.com) an: `gh auth login`.
4. Ergebnis ansehen wie in Variante B, Schritt 4.

**Neue Aufgaben:** Erst alles pushen, dann im Browser **Sync fork** wie in Variante B, dann im Terminal `git pull`.

### Kritik und Fehler melden

Ist eine Aufgabe unklar, zu leicht, zu schwer, oder lehnt ein Test eine richtige Lösung ab? Kritik ist ausdrücklich erwünscht: Auf der Seite dieses Repos **Issues → New issue** öffnen, die Aufgabe nennen und kurz beschreiben, was Ihnen aufgefallen ist.

### Bestehende Aufgabe verbessern

Wissen Sie schon, wie es besser geht, z. B. ein fehlender Test oder ein Tippfehler im Aufgabentext, ändern Sie die Aufgabe direkt im Browser. Eine eigene Lösung oder Python brauchen Sie dafür nicht.

1. Auf der Seite dieses Repos `tests/1_003_rechteck.py` (Tests) oder `aufgaben/1_003_rechteck.py` (Aufgabentext) öffnen → Stift-Symbol.
2. Ändern, z. B. einen Test ergänzen. Wie Tests aussehen, steht unter „Tests schreiben“ weiter unten.
3. **Commit changes… → Propose changes → Create pull request**. GitHub legt dabei automatisch einen Fork an.

GitHub prüft den Pull Request automatisch. Die Lehrkraft übernimmt die Änderung in ihre Musterlösung und prüft, ob die Musterlösung die neuen Tests besteht.

---

## Eigene Aufgaben erstellen

Dafür brauchen Sie Python auf Ihrem Rechner (siehe Variante A).

### Ideen für Aufgaben

Sie müssen sich nicht alles selbst ausdenken. Auf diesen deutschsprachigen Seiten finden Sie Aufgaben, die Sie hier mit Tests umsetzen können:

| Seite | Inhalt | Lizenz |
|---|---|---|
| [inf-schule.de](https://inf-schule.de/imperative-programmierung/python) | Python für die Schule: Miniprojekte und Übungen zu Variablen, Schleifen, Funktionen, Listen | CC BY-SA 4.0 |
| [pythonbuch.com](https://pythonbuch.com/aufgabensammlung.html) | Einführung ins Programmieren mit Python, mit Aufgabensammlung | CC BY-SA 4.0 |
| [python-kurs.eu](https://www.python-kurs.eu/python3_kurs.php) | Python-Kurs mit Beispielen und Übungen | keine freie Lizenz, nur als Anregung |

Übernehmen Sie eine Aufgabe, schreiben Sie die Quelle und die Lizenz in den Aufgabentext, z. B. `Nach inf-schule.de, CC BY-SA 4.0`. Das verlangen diese Lizenzen, und Ihre Aufgabe steht dann ebenfalls unter CC BY-SA 4.0. Bei Seiten ohne freie Lizenz schreiben Sie die Aufgabe nicht ab, sondern denken sich mit eigenen Worten eine ähnliche aus.

### 1. Musterdatei schreiben

Legen Sie im Projektordner einen Ordner `eigene_aufgaben` an und darin eine **Musterdatei**, z. B. `2_009_maximum.py`. Der Name beginnt mit der Stufe (1 bis 5), dann folgt die nächste freie Nummer dieser Stufe aus den Tabellen oben, dreistellig. In die Musterdatei kommt alles: Aufgabenstellung, Ihre Lösung und Tests.

```python
# Thema: funktionen
# Inhalt: Größere von zwei Zahlen
"""Aufgabe 2_009 – Maximum                                    Stufe 2 ★★☆☆☆

Vervollständigen Sie die Funktion `maximum`, die die größere von zwei Zahlen zurückgibt.
"""


def maximum(a, b):
    ### BEGIN SOLUTION
    if a > b:
        return a
    return b
    ### END SOLUTION


### BEGIN TESTS
# maximum(3, 5) ist 5
assert maximum(3, 5) == 5, f"maximum(3, 5) ergibt {maximum(3, 5)!r}, erwartet war 5."

# maximum(5, 3) ist 5
assert maximum(5, 3) == 5, f"maximum(5, 3) ergibt {maximum(5, 3)!r}, erwartet war 5."
### END TESTS
```

Die zwei Zeilen ganz oben sind Pflicht. Nach `# Thema:` steht eines der Themen, die `python pruefe.py --help` auflistet, z. B. `texte_zahlen`, `kontrollfluss`, `funktionen` oder `klassen`. Wählen Sie das Thema, das Ihre Aufgabe neu einführt. Nach `# Inhalt:` steht eine kurze Beschreibung, die in den Tabellen oben erscheint. Beide Zeilen kommen nur in die Testdatei, nicht in die Vorlage.

### 2. Aufgabe erzeugen

```
python erstelle_aufgaben.py
```

Das erzeugt `aufgaben/2_009_maximum.py` (die Vorlage zum Lösen), `tests/2_009_maximum.py` und `loesungen/2_009_maximum.py` (Ihre Lösung zum Nachlesen, ohne Tests). Dabei wird automatisch geprüft, dass **Ihre Lösung alle Tests besteht** und **die leere Vorlage nicht**:

```
✓ 2_009_maximum.py (2 Tests, 2 von 3 Änderungen bemerkt)
    ⚠ Kein Test bemerkt: Zeile 11: a > b  →  a >= b
```

Steht dort ein ✗, steht darunter, was nicht stimmt. Ändern Sie die Musterdatei und starten Sie das Skript noch einmal. Die Dateien in `aufgaben/` und `tests/` nie von Hand ändern, sie werden jedes Mal neu erzeugt.

Solange die Aufgabe neu ist (noch nicht mit `git` committet), baut das Skript außerdem absichtlich kleine Fehler in Ihre Lösung ein, je einen pro Durchgang: `>=` statt `>`, `-` statt `+`, eine Zahl um eins größer, eine Zeile gestrichen. Jeden davon sollte mindestens ein Test finden. Ein ⚠ zeigt einen, den kein Test findet. Überlegen Sie, ob die veränderte Lösung wirklich falsch wäre. Wenn ja, ergänzen Sie einen Test. Manchmal verhält sie sich aber genau gleich, im Beispiel oben etwa, wenn bei gleichen Zahlen egal ist, welche zurückkommt. Dann ist das ⚠ harmlos.

### 3. Tests mit falschen Lösungen ausprobieren

Das ✓ zeigt nur, dass Ihre Lösung besteht und die leere Vorlage nicht. Ob Ihre Tests auch **typische Fehler** finden, prüfen Sie selbst: Schreiben Sie in `aufgaben/2_009_maximum.py` eine falsche Lösung, so wie sie beim Lösen entstehen könnte, und prüfen Sie sie wie eine normale Aufgabe:

```
python pruefe.py 2_009
```

Gute falsche Lösungen sind z. B. ein fest hingeschriebenes Ergebnis (`return 5`), vertauschte Fälle oder eine vergessene Kleinigkeit wie das `!` am Satzende. Jede davon sollte mindestens ein ✗ bekommen, und die Meldung darunter sollte helfen, den Fehler zu finden. Probieren Sie auch eine **andere richtige** Lösung aus: Sie muss alle Tests bestehen. Wenn nicht, sind Ihre Tests zu streng.

Findet ein Test einen Fehler nicht, ergänzen Sie Tests in der Musterdatei. Zum Schluss `python erstelle_aufgaben.py` noch einmal starten. Das stellt auch die Vorlage in `aufgaben/` wieder her.

**Für Fortgeschrittene:** Wollen Sie mehrere falsche Lösungen aufheben, ohne `aufgaben/` zu ändern, legen Sie sie in eigene Ordner. Der Dateiname muss derselbe sein wie in `aufgaben/`, sonst findet `pruefe.py` die passenden Tests nicht. Zwei falsche Lösungen zur selben Aufgabe brauchen deshalb zwei Ordner. Benennen Sie die Ordner nach dem Fehler, den sie enthalten, z. B. `varianten/fest/2_009_maximum.py` (Ergebnis fest hingeschrieben) und `varianten/vertauscht/2_009_maximum.py`.

Alle Aufgaben in einem Ordner prüfen Sie mit

```
python pruefe.py --aufgaben varianten/fest
```

Einzelne Aufgaben prüfen Sie wieder über den Anfang des Namens, z. B. alle, die mit `2_009` beginnen:

```
python pruefe.py 2_009 --aufgaben varianten/fest
```

Für den Anfang ist es einfacher, die Datei in `aufgaben/` direkt zu bearbeiten wie oben beschrieben.

### 4. Für alle hochladen

Hochgeladen werden die zwei erzeugten Dateien aus `aufgaben/` und `tests/`. Die dritte, `loesungen/2_009_maximum.py`, ist freiwillig (für Stufe 4 und 5 erzeugt `erstelle_aufgaben.py` sie nicht, diese Lösungen bleiben privat): Laden Sie sie mit hoch, wenn andere nach dem Lösen Ihren Weg sehen sollen (die Prüfung beim Hochladen kontrolliert dann, dass sie die Tests besteht). **Ihre Musterdatei behalten Sie** in jedem Fall. Ich freue mich gerne über die Musterlösung für meine Notizen, bspw. durch Teilen Ihrer privaten Repos. Mit dem Hochladen stimmen Sie den [Bedingungen für Einreichungen](#bedingungen-für-einreichungen) zu.

Ihre Lösungen in Ihrem Fork dürfen dabei nicht mitkommen. Laden Sie deshalb über die Seite **dieses Repos** hoch, nicht über Ihren Fork. GitHub legt die Dateien dann in einem neuen Zweig Ihres Forks ab, in dem Ihre Lösungen nicht enthalten sind.

1. Auf der Seite dieses Repos den Ordner `aufgaben` öffnen → **Add file → Upload files** → `aufgaben/2_009_maximum.py` hineinziehen → **Propose changes** → **Create pull request**.
2. In Ihrem Fork oben links auf den Knopf mit dem Zweignamen klicken und den neuen Zweig wählen (z. B. `patch-1`). Dort den Ordner `tests` öffnen → **Add file → Upload files** → `tests/2_009_maximum.py` hineinziehen → **Commit changes**. Die Datei kommt automatisch in Ihren Pull Request.
3. Die Tabellen in `README.md` müssen Sie nicht ändern. `erstelle_aufgaben.py` erzeugt sie aus den Kopfzeilen `# Thema:` und `# Inhalt:`, nachdem die Lehrkraft Ihre Aufgabe übernommen hat.

Mit git geht es so (die beiden erzeugten Dateien bleiben beim Wechsel des Zweigs erhalten):

```
git fetch https://github.com/mathematiger/python_autograding_exercises.git main
git switch -c aufgabe-2_009 FETCH_HEAD
git add aufgaben/2_009_maximum.py tests/2_009_maximum.py   # freiwillig auch loesungen/2_009_maximum.py
git commit -m "Neue Aufgabe 2_009_maximum"
git push -u origin aufgabe-2_009
git switch main
```

Danach auf der Seite Ihres Forks **Compare & pull request** → **Create pull request**.

Die Lehrkraft schaut drüber und übernimmt die Aufgabe. Danach können alle sie lösen.

### Die Marker

| Marker | Wirkung |
|---|---|
| `### BEGIN SOLUTION` … `### END SOLUTION` | Lösung. In der Vorlage wird daraus `pass  # ← Ersetzen Sie diese Zeile durch Ihren Code` (mit gleicher Einrückung). |
| `### BEGIN TESTS` … `### END TESTS` | Tests. Kommen nur in die Testdatei. |
| `### BEGIN LOESUNGSWEG` … `### END LOESUNGSWEG` | Nur Kommentarzeilen (`#`). Kommen nur in `loesungen/`: Idee, andere Wege, Laufzeit. Gehört meist ans Ende der Datei. |

Alles außerhalb der Marker steht in der Vorlage, also Aufgabentext, vorgegebener Code und Funktionsköpfe. `### BEGIN HIDDEN TESTS` wird wie `TESTS` behandelt: Ohne Server lassen sich Tests nicht wirklich verstecken.

### Tests schreiben

Tests sind normale `assert`-Zeilen, wie in nbgrader. Jedes `assert` (oder jeder Block, der eines enthält, z. B. eine `for`-Schleife) zählt als ein Test.

- **Name eines Tests:** der Kommentar direkt über dem Test (oder über der Vorbereitungszeile davor). Ohne Kommentar wird die Bedingung angezeigt.
- **Meldung bei Fehlschlag:** der Text nach dem Komma im `assert`. Schreiben Sie hier, was beim Lösen geändert werden soll.
- Die Tests laufen *nach* dem Programm, im selben Namensraum: Alle Variablen und Funktionen der Lösung sind verfügbar.
- Testen Sie mit mehreren Werten, damit niemand das Ergebnis einfach fest hinschreiben kann.
- Die Tests haben hilfreiche Fehlerausgaben, was falsch ist, und evtl. Tipps für den nächsten Versuch.
- **Bibliotheken:** Aufgaben und Tests dürfen nur die Bibliotheken aus `requirements.txt` importieren (`import pandas as pd`). Andere Importe, auch aus der Standardbibliothek, lehnt die Prüfung beim Hochladen ab. Testen Sie Werte (`df["preis"].tolist() == [3, 5]`), nicht die Ausgabe von `print(df)`: Wie breit pandas eine Tabelle druckt, hängt vom Terminal ab.

Zusätzlich gibt es in den Tests:

| Name | Bedeutung |
|---|---|
| `AUSGABE` | Alles, was das Programm mit `print` ausgegeben hat. Leerzeichen am Zeilenende und Leerzeilen am Schluss sind schon entfernt. Der Text von `input("…")` gehört nicht dazu. |
| `EINGABEN = ["Anna"]` | In den Tests setzen: Diese Werte bekommt `input()` beim ersten Lauf. |
| `starte("Bo")` | Startet das Programm neu mit anderen Eingaben und gibt dessen Ausgabe zurück. Gut gegen fest eingetippte Ergebnisse. |
| `verwendet("for")` | `True`, wenn `for`, `while`, `if`, `def`, `return`, `class` oder ein Aufruf wie `range` im Code vorkommt. Kommentare zählen nicht. |
| `Zaehlliste([3, 8, 15])` | Verhält sich beim Lesen und Schreiben über den Index wie eine Liste und zählt mit: `liste.lesezugriffe`, `liste.schreibzugriffe`, die Werte in `liste.werte`. Auch `for` und `in` zählen jedes angesehene Element. Für Aufgaben wie „höchstens etwa 20 Zugriffe bei 1000 Einträgen“. |
| `zaehle_schritte(f, 1000)` | Ruft `f(1000)` auf und gibt `(ergebnis, schritte)` zurück. `schritte` ist die Anzahl der ausgeführten Zeilen im Programm (nicht in Builtins wie `sorted` oder `in`). Prüfen Sie damit, wie die Arbeit mit der Eingabe wächst, z. B. ob sich die Schritte bei doppelter Eingabe höchstens verdoppeln. |

Endlosschleifen werden nach 5 Sekunden abgebrochen (`ZEITLIMIT_SEKUNDEN` in `pruefe.py`). Prüfen Sie die Laufzeit lieber mit `Zaehlliste` oder `zaehle_schritte` als über die Zeit: Die Zahlen sind auf jedem Rechner gleich, die Zeit nicht.

---

## Für Lehrkräfte

### Eigene Aufgaben

Genauso wie oben bei „Eigene Aufgaben erstellen“, nur liegen Ihre Musterdateien in `lehrkraft/muster/` statt in `eigene_aufgaben/`. `python erstelle_aufgaben.py` verarbeitet beide Ordner. Danach `aufgaben/` und `tests/` committen und pushen.

### Der Ordner `lehrkraft/`

`lehrkraft/` ist ein **privates Git-Submodul** (eigenes privates Repo). Musterlösungen, Notizen und die `CLAUDE.md` gehören dorthin. Für alle anderen ist der Ordner leer. Auf einem neuen Rechner holen mit

```
git clone --recurse-submodules <url dieses Repos>
```

Änderungen in `lehrkraft/` dort committen und pushen, danach im Hauptordner `git add lehrkraft` committen.

### Aufgaben von SuS übernehmen

Eingereichte Aufgaben kommen als **Pull Request**. Auf GitHub unter **Pull requests** öffnen, unter **Files changed** Aufgabentext und Tests ansehen, dann **Merge pull request**. Die Musterlösung hat nur die Person, die die Aufgabe geschrieben hat.

Pull Requests, die eine **bestehende** Aufgabe ändern, nicht direkt mergen. Erst lokal mit `gh pr checkout <Nummer>` holen, die Änderung in die Musterdatei übernehmen und `python erstelle_aufgaben.py` starten. Besteht Ihre Musterlösung die neuen Tests, mergen und die neu erzeugten Dateien committen. Besteht sie nicht, im Pull Request nachfragen. Fehlt die Musterdatei, weil SuS die Aufgabe geschrieben haben, bauen Sie sie aus Vorlage und Tests nach und schreiben Ihre eigene Lösung hinein. Vergessen Sie das Übernehmen, meldet es `python3 -m pytest entwicklung` (`test_aktuell_erzeugt`).

Vorher prüft GitHub jeden Pull Request automatisch (`.github/workflows/einreichung.yml`): Geändert sind nur `aufgaben/`, `tests/`, `loesungen/`, `README.md` und die Werkzeuge (siehe unten), bei neuen Aufgaben gehören Vorlage und Tests zusammen, die leere Vorlage besteht die Tests nicht, eine beigelegte Lösung besteht sie, und es steht nichts darin wie `import` (außer den Bibliotheken aus `requirements.txt`), `open` oder `eval`, womit Code auf den Rechnern der SuS Schaden anrichten könnte. Das Ergebnis steht als ✓ oder ✗ am Pull Request, Einzelheiten unter **Details**.

- Bei der ersten Einreichung einer Person fragt GitHub, ob der Workflow laufen darf: **Approve and run**.
- Ein ✓ ersetzt nicht das Ansehen. Ändert ein Pull Request etwas unter `.github/`, nicht übernehmen: Dann ist auch das ✓ nicht verlässlich.
- Bei Aufgaben mit Bibliotheken besonders genau hinsehen: pandas, polars und DuckDB können selbst Dateien lesen und schreiben (`read_csv`, `to_csv`, SQL mit `COPY`). Das findet die automatische Prüfung nicht.
- Neue Bibliotheken kommen nur über Sie: in `requirements.txt`, `pyproject.toml` und `BIBLIOTHEKEN` in `pruefe.py` eintragen (ein Test prüft, dass alle drei gleich sind). Pull Requests, die `requirements.txt` oder `pyproject.toml` ändern, lehnt die Prüfung ab.

### Werkzeuge weiterentwickeln

`pruefe.py`, `erstelle_aufgaben.py` und `.github/pruefe_einreichung.py` haben eigene Tests in `entwicklung/`. Vor einem Pull Request bitte lokal ausführen (`pip install -r requirements.txt pytest ruff mypy`):

```
python3 -m pytest entwicklung
ruff check . && ruff format --check .
mypy --strict pruefe.py erstelle_aufgaben.py .github/pruefe_einreichung.py
```

GitHub führt dasselbe bei jedem Pull Request unter Python 3.11 und der neuesten Python-Version aus (`.github/workflows/entwicklung.yml`). Tests, die die privaten Musterdateien in `lehrkraft/muster/` brauchen, werden ohne diesen Ordner übersprungen. Ein ✓ ersetzt nicht das Ansehen: Änderungen an den Werkzeugen landen beim Mergen auf den Rechnern aller SuS.


### Gut zu wissen

- Die Tests liegen offen im Repo. Wer will, kann sie lesen. Für Selbstkontrolle ist das in Ordnung.
- `eigene_aufgaben/` steht in `.gitignore`, damit Musterlösungen von SuS nicht versehentlich mit `git` hochgeladen werden.
- Löschen Sie eine Musterdatei, löschen Sie auch die zugehörigen Dateien in `aufgaben/`, `tests/` und `loesungen/` von Hand.
- Die Musterlösungen in `loesungen/` (Stufe 1 bis 3) sind öffentlich. Wer will, kann sie vor dem Lösen lesen, wie bei den Tests. Für eine bewertete Abgabe taugen diese Aufgaben deshalb nicht ohne eigene Variante.

---

## Lizenz

© [mathematiger](https://github.com/mathematiger) und alle, die Aufgaben beigetragen haben.

| Teil | Lizenz |
|---|---|
| Code: `pruefe.py`, `erstelle_aufgaben.py`, `.github/`, `.githooks/`, `entwicklung/` | [MIT](LICENSE-CODE) |
| Inhalte: `aufgaben/`, `tests/`, `loesungen/`, diese README | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de), siehe [LICENSE](LICENSE) |

Kurz gesagt: Den Code dürfen Sie für jeden Zweck nutzen, verändern und weitergeben, auch kommerziell, solange der Lizenzhinweis erhalten bleibt. Die Inhalte dürfen Sie kopieren, verändern und weitergeben, wenn Sie die Quelle nennen, sie nicht kommerziell nutzen und Ihre veränderte Fassung unter derselben Lizenz weitergeben. Verbindlich ist jeweils der Lizenztext.

Nutzungen, die über diese Lizenzen hinausgehen, etwa eine kommerzielle Nutzung der Inhalte, sind auf Anfrage möglich: [mathematiger.contact@gmail.com](mailto:mathematiger.contact@gmail.com).

Ausnahmen: Aufgaben nach einer Vorlage unter CC BY-SA (siehe „Ideen für Aufgaben“) stehen weiter unter CC BY-SA 4.0, Quelle und Lizenz stehen dann im Aufgabentext. Bis zum 29.10.2026 stand das ganze Repo unter [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de); für Kopien aus dieser Zeit gilt diese Lizenz weiter.

### Bedingungen für Einreichungen

Mit einem Pull Request bestätigen Sie, dass Sie die Aufgabe selbst geschrieben haben oder Quelle und Lizenz einer Vorlage im Aufgabentext angeben. Ihre Aufgabe steht dann unter CC BY-NC-SA 4.0 (nach einer Vorlage unter CC BY-SA unter deren Lizenz), Änderungen am Code unter MIT. Ihr Urheberrecht bleibt bei Ihnen. Sind Sie unter 18 Jahre alt, brauchen Sie für das Einreichen die Zustimmung Ihrer Eltern.
