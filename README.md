# Python-Aufgaben

Python lernen mit Textaufgaben aus dem IT-Berufsalltag, die sich selbst prüfen: Sie lösen eine Aufgabe in Ihrem Editor, starten `python pruefe.py` und sehen sofort, welche Tests bestehen und was noch fehlt. Kein Server, kein Konto nötig (außer Sie wollen über GitHub abgeben).

## Für wen

- **Lernende** in IT-Ausbildungen, an Berufs- und Fachschulen und alle, die Python im Selbststudium lernen. Stufe 1 setzt nichts voraus, Stufe 5 richtet sich an Fortgeschrittene, die verstehen wollen, wie Python intern arbeitet.
- **Lehrkräfte und Ausbilder**, die Übungsaufgaben mit automatischer Rückmeldung suchen oder eigene schreiben wollen (siehe [Für Lehrkräfte](#für-lehrkräfte)).
- **Alle, die mitmachen wollen:** Sie können eigene Aufgaben erstellen und für alle hochladen (siehe [Eigene Aufgaben erstellen](#eigene-aufgaben-erstellen)).

## Wie die Aufgaben entstehen

Die Aufgaben werden mit KI erstellt: Ein KI-Agent (Claude von Anthropic) hat sie nach einem festen Lehrplan geschrieben, jeweils mit Aufgabentext, Musterlösung und Tests. Lehrplan, Regeln und Prüfwerkzeuge legt die Lehrkraft fest. Damit die Aufgaben verlässlich sind, hat jede mehrere Prüfungen durchlaufen:

- **Automatisch beim Erzeugen:** Die Musterlösung muss alle Tests bestehen, die leere Vorlage darf sie nicht bestehen. Danach baut `erstelle_aufgaben.py` absichtlich kleine Fehler in die Musterlösung ein (`>=` statt `>`, eine Zahl um eins größer, …), und die Tests sollen jeden davon finden. Ab Stufe 2 prüfen die Tests außerdem viele zufällige Eingaben und die Ränder der erlaubten Werte. Eine verlangte Laufzeit prüfen sie über gezählte Schritte, nicht über die Uhr, damit langsame Rechner nicht durchfallen.
- **Gutachten:** Ein zweiter KI-Durchlauf hat jede Aufgabe mindestens einmal aus fünf Sichten gelesen: Informatikdidaktik, Python-Praxis, Testen, Fachlichkeit im IT-Alltag und Sprache. Er hat typische falsche Lösungen ausprobiert (sie müssen scheitern) und eine andere richtige (sie muss bestehen) und eindeutige Fehler behoben. Was sich nicht eindeutig entscheiden ließ, ging an die Lehrkraft. Zum Abschluss wurde der Kurs als Ganzes geprüft: lückenlose Nummern, Verweise nur auf frühere Aufgaben, Übergänge zwischen den Aufgaben jeder Stufe.
- **Durch Sie:** Lehnt ein Test eine richtige Lösung ab oder ist ein Text unklar, melden Sie es bitte (siehe [Kritik und Fehler melden](#kritik-und-fehler-melden)).

Trotz dieser Prüfungen kann eine Aufgabe Fehler enthalten. Wird sie deshalb überarbeitet, bleiben Funktionsnamen und vorgegebener Code gleich, und eine Lösung, die nach dem bisherigen Text richtig war, besteht weiterhin.

## Wie weit der Kurs ist

Der Kurs ist vollständig: 338 Aufgaben in fünf Stufen bilden zusammen einen Python-Kurs zum Selbststudium. Arbeiten Sie eine Stufe von oben nach unten durch. Jede Aufgabe baut nur auf frühere Aufgaben derselben Stufe oder auf Aufgaben einer niedrigeren Stufe auf. Was eine Aufgabe neu einführt, erklärt sie im Abschnitt „Hintergrund“; Sprachmittel aus früheren Aufgaben nennt sie dort mit deren Nummer.

## Aufgaben

Der Name jeder Aufgabe beginnt mit ihrer Stufe, danach folgt die Nummer innerhalb der Stufe: `2_005_wuerfel` ist die fünfte Aufgabe der Stufe 2. So stehen die Aufgaben im Ordner nach Schwierigkeit sortiert, und innerhalb einer Stufe baut jede Aufgabe auf den vorherigen auf.

Ihren Stand sehen Sie mit `python pruefe.py --liste`: alle Aufgaben nach Thema, mit ✓ bestanden, ✗ offen und ○ unbearbeitet. Mit `python pruefe.py --liste funktionen` oder `python pruefe.py --liste 2` nur ein Thema oder eine Stufe.

<!-- AUFGABEN-ANFANG: erzeugt von erstelle_aufgaben.py, nicht von Hand ändern -->

### Nach Thema

| Thema | Stufe 1 | Stufe 2 | Stufe 3 | Stufe 4 | Stufe 5 | Prüfen mit |
| --- | --- | --- | --- | --- | --- | --- |
| [Texte, Zahlen & Dateien](#thema-texte_zahlen) | 16 | 7 | 9 | 6 | 5 | `python pruefe.py texte_zahlen` |
| [Bedingungen & Schleifen](#thema-kontrollfluss) | 16 | 8 | 8 | 15 | 5 | `python pruefe.py kontrollfluss` |
| [Funktionen](#thema-funktionen) | 5 | 7 | 5 | 15 | 6 | `python pruefe.py funktionen` |
| [Algorithmen & Rekursion](#thema-algorithmen) | 1 | 16 | 27 | 9 | 3 | `python pruefe.py algorithmen` |
| [Datenstrukturen](#thema-datenstrukturen) | 9 | 14 | 3 | 11 | 4 | `python pruefe.py datenstrukturen` |
| [Fehler & Testen](#thema-fehler) |  | 5 | 11 | 5 | 4 | `python pruefe.py fehler` |
| [Klassen & Objekte](#thema-klassen) |  |  | 5 | 14 | 18 | `python pruefe.py klassen` |
| [Programmaufbau](#thema-programmaufbau) | 2 | 1 | 2 | 3 | 2 | `python pruefe.py programmaufbau` |
| [Nebenläufigkeit](#thema-nebenlaeufigkeit) |  |  |  | 1 | 10 | `python pruefe.py nebenlaeufigkeit` |
| [Datenanalyse](#thema-datenanalyse) |  | 2 | 7 | 10 | 6 | `python pruefe.py datenanalyse` |

<a name="thema-texte_zahlen"></a>
<details>
<summary><b>Texte, Zahlen & Dateien</b> (43 Aufgaben)</summary>

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
| [1_043_raidstatus](aufgaben/1_043_raidstatus.py) | ★☆☆☆☆ | Zeichen zählen mit for |
| [2_014_kuerzel](aufgaben/2_014_kuerzel.py) | ★★☆☆☆ | Texte durchlaufen und neu aufbauen |
| [2_015_namensabgleich](aufgaben/2_015_namensabgleich.py) | ★★☆☆☆ | `split` und `join` |
| [2_016_codemetrik](aufgaben/2_016_codemetrik.py) | ★★☆☆☆ | Tabellen mit f-String-Breiten |
| [2_017_arbeitspakete](aufgaben/2_017_arbeitspakete.py) | ★★☆☆☆ | Übung: Zeilen zerlegen, Tabelle ausgeben |
| [2_043_summenabgleich](aufgaben/2_043_summenabgleich.py) | ★★☆☆☆ | Kommazahlen vergleichen |
| [2_049_caesar](aufgaben/2_049_caesar.py) | ★★☆☆☆ | Cäsar mit ord und chr |
| [2_051_datenkontingent](aufgaben/2_051_datenkontingent.py) | ★★☆☆☆ | Schaltjahr, Tage im Monat |
| [3_046_artikelexport](aufgaben/3_046_artikelexport.py) | ★★★☆☆ | Textdatei zeilenweise lesen |
| [3_048_aktionsliste](aufgaben/3_048_aktionsliste.py) | ★★★☆☆ | Textdatei schreiben und anhängen |
| [3_049_datenbanklog](aufgaben/3_049_datenbanklog.py) | ★★★☆☆ | Übung: Logdatei auswerten |
| [3_050_codeanalyse](aufgaben/3_050_codeanalyse.py) | ★★★☆☆ | CSV von Hand, Summen je Spalte |
| [3_051_ticketexport](aufgaben/3_051_ticketexport.py) | ★★★☆☆ | csv.reader und DictReader |
| [3_052_alarmbericht](aufgaben/3_052_alarmbericht.py) | ★★★☆☆ | csv.writer und DictWriter |
| [3_054_angebotsfrist](aufgaben/3_054_angebotsfrist.py) | ★★★☆☆ | Datum zerlegen und prüfen |
| [3_055_scanbericht](aufgaben/3_055_scanbericht.py) | ★★★☆☆ | Tausendertrennzeichen und Prozent |
| [3_076_meldungstexte](aufgaben/3_076_meldungstexte.py) | ★★★☆☆ | Textstatistik: Wörter, Satzlängen |
| [4_066_statustafel](aufgaben/4_066_statustafel.py) | ★★★★☆ | format_spec, Ausrichtung, Datum |
| [4_067_funkknoten](aufgaben/4_067_funkknoten.py) | ★★★★☆ | re: Muster suchen, Gruppen |
| [4_069_datumsangaben](aufgaben/4_069_datumsangaben.py) | ★★★★☆ | re.sub mit Funktion, finditer |
| [4_070_wartungsplan](aufgaben/4_070_wartungsplan.py) | ★★★★☆ | json: eigene Objekte speichern |
| [4_071_neustartplan](aufgaben/4_071_neustartplan.py) | ★★★★☆ | datetime und timedelta, Fristen |
| [4_073_geheimnisscan](aufgaben/4_073_geheimnisscan.py) | ★★★★☆ | pathlib und tempfile |
| [5_037_ansichten](aufgaben/5_037_ansichten.py) | ★★★★★ | pickle mit __getstate__/__setstate__ |
| [5_053_angebotsexport](aufgaben/5_053_angebotsexport.py) | ★★★★★ | bytes und bytearray |
| [5_054_abdeckungsdatei](aufgaben/5_054_abdeckungsdatei.py) | ★★★★★ | struct und memoryview |
| [5_055_rechnungsmaske](aufgaben/5_055_rechnungsmaske.py) | ★★★★★ | decimal für Geldbeträge |
| [5_056_bandbreitenanteile](aufgaben/5_056_bandbreitenanteile.py) | ★★★★★ | fractions.Fraction |

</details>

<a name="thema-kontrollfluss"></a>
<details>
<summary><b>Bedingungen & Schleifen</b> (52 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_016_sprintplan](aufgaben/1_016_sprintplan.py) | ★☆☆☆☆ | Vergleiche mit `>`, `==`, `<` |
| [1_017_temperaturwarnung](aufgaben/1_017_temperaturwarnung.py) | ★☆☆☆☆ | if-Anweisung |
| [1_018_bewaesserung](aufgaben/1_018_bewaesserung.py) | ★☆☆☆☆ | if/else |
| [1_019_abc_analyse](aufgaben/1_019_abc_analyse.py) | ★☆☆☆☆ | if/elif/else |
| [1_020_eskalation](aufgaben/1_020_eskalation.py) | ★☆☆☆☆ | and, or, not |
| [1_021_leasing](aufgaben/1_021_leasing.py) | ★☆☆☆☆ | Übung: Bedingungen |
| [1_022_loeschen](aufgaben/1_022_loeschen.py) | ★☆☆☆☆ | for über range(n) |
| [1_023_adressbereich](aufgaben/1_023_adressbereich.py) | ★☆☆☆☆ | for über range(a, b) |
| [1_024_rack](aufgaben/1_024_rack.py) | ★☆☆☆☆ | range mit Schrittweite |
| [1_025_testlaufzeit](aufgaben/1_025_testlaufzeit.py) | ★☆☆☆☆ | Zähler in der Schleife |
| [1_026_formulartest](aufgaben/1_026_formulartest.py) | ★☆☆☆☆ | Übung: Schleifen |
| [1_028_fehlende_werte](aufgaben/1_028_fehlende_werte.py) | ★☆☆☆☆ | for über eine Liste |
| [1_033_schriftgroesse](aufgaben/1_033_schriftgroesse.py) | ★☆☆☆☆ | while-Schleife |
| [1_034_pingzeiten](aufgaben/1_034_pingzeiten.py) | ★☆☆☆☆ | Eingabeschleife bis stop |
| [1_035_altersangaben](aufgaben/1_035_altersangaben.py) | ★☆☆☆☆ | Übung: while |
| [1_042_zeittabelle](aufgaben/1_042_zeittabelle.py) | ★☆☆☆☆ | Verschachtelte Schleifen |
| [2_001_zaehlen](aufgaben/2_001_zaehlen.py) | ★★☆☆☆ | for-Schleife |
| [2_003_gerade](aufgaben/2_003_gerade.py) | ★★☆☆☆ | if und Funktionen |
| [2_004_countdown](aufgaben/2_004_countdown.py) | ★★☆☆☆ | while-Schleife |
| [2_007_transporter](aufgaben/2_007_transporter.py) | ★★☆☆☆ | Schleife mit break |
| [2_008_stromverbrauch](aufgaben/2_008_stromverbrauch.py) | ★★☆☆☆ | Schleife mit continue |
| [2_021_prozessschritte](aufgaben/2_021_prozessschritte.py) | ★★☆☆☆ | enumerate |
| [2_022_reaktionsfristen](aufgaben/2_022_reaktionsfristen.py) | ★★☆☆☆ | zip |
| [2_059_displaysymbole](aufgaben/2_059_displaysymbole.py) | ★★☆☆☆ | Dreieck und Raute aus Sternchen |
| [3_017_lastspitzen](aufgaben/3_017_lastspitzen.py) | ★★★☆☆ | List Comprehension |
| [3_018_sensorkarte](aufgaben/3_018_sensorkarte.py) | ★★★☆☆ | Dict Comprehension |
| [3_019_ereignisprotokoll](aufgaben/3_019_ereignisprotokoll.py) | ★★★☆☆ | Set Comprehension |
| [3_020_ticketstrom](aufgaben/3_020_ticketstrom.py) | ★★★☆☆ | iter() und next() |
| [3_021_kostenvergleich](aufgaben/3_021_kostenvergleich.py) | ★★★☆☆ | Verbrauchte Iteratoren |
| [3_022_lauflaengen](aufgaben/3_022_lauflaengen.py) | ★★★☆☆ | Generatoren mit yield |
| [3_023_mitschnitt](aufgaben/3_023_mitschnitt.py) | ★★★☆☆ | Generator-Ausdrücke |
| [3_024_stromeffizienz](aufgaben/3_024_stromeffizienz.py) | ★★★☆☆ | Übung: Comprehensions und Generatoren |
| [4_032_gleitender_schnitt](aufgaben/4_032_gleitender_schnitt.py) | ★★★★☆ | Iterator-Protokoll |
| [4_033_bandrotation](aufgaben/4_033_bandrotation.py) | ★★★★☆ | Iterable gegen Iterator |
| [4_034_amortisation](aufgaben/4_034_amortisation.py) | ★★★★☆ | Unendliche Generatoren |
| [4_035_tabreihenfolge](aufgaben/4_035_tabreihenfolge.py) | ★★★★☆ | __iter__ als Generator |
| [4_036_firewallprotokoll](aufgaben/4_036_firewallprotokoll.py) | ★★★★☆ | Generator-Pipeline |
| [4_038_testdatenquelle](aufgaben/4_038_testdatenquelle.py) | ★★★★☆ | iter() mit Endmarke |
| [4_039_messspruenge](aufgaben/4_039_messspruenge.py) | ★★★★☆ | Übung: Iteratoren und Generatoren |
| [4_040_moderationsplan](aufgaben/4_040_moderationsplan.py) | ★★★★☆ | count, cycle, repeat, islice |
| [4_042_rollenrechte](aufgaben/4_042_rollenrechte.py) | ★★★★☆ | chain und zip_longest |
| [4_043_trainingsverlauf](aufgaben/4_043_trainingsverlauf.py) | ★★★★☆ | accumulate: laufende Werte |
| [4_044_wissensdatenbank](aufgaben/4_044_wissensdatenbank.py) | ★★★★☆ | itertools.groupby |
| [4_046_sensortests](aufgaben/4_046_sensortests.py) | ★★★★☆ | product, permutations, combinations |
| [4_047_durchsatzmessung](aufgaben/4_047_durchsatzmessung.py) | ★★★★☆ | takewhile, dropwhile, compress |
| [4_048_rackzaehler](aufgaben/4_048_rackzaehler.py) | ★★★★☆ | pairwise und tee |
| [4_049_gpu_budget](aufgaben/4_049_gpu_budget.py) | ★★★★☆ | Übung: itertools |
| [5_027_platzierer](aufgaben/5_027_platzierer.py) | ★★★★★ | send: Generator als Koroutine |
| [5_028_budgetkonto](aufgaben/5_028_budgetkonto.py) | ★★★★★ | throw, close, finally in Generatoren |
| [5_029_formularassistent](aufgaben/5_029_formularassistent.py) | ★★★★★ | yield from, Rückgabewert |
| [5_030_netzscanner](aufgaben/5_030_netzscanner.py) | ★★★★★ | Iterable, Iterator, Generator typisieren |
| [5_057_gatewayspeicher](aufgaben/5_057_gatewayspeicher.py) | ★★★★★ | Generator-Pipelines und Speicher |

</details>

<a name="thema-funktionen"></a>
<details>
<summary><b>Funktionen</b> (38 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_036_reviewdauer](aufgaben/1_036_reviewdauer.py) | ★☆☆☆☆ | Funktion mehrfach aufrufen |
| [1_037_heizungsventile](aufgaben/1_037_heizungsventile.py) | ★☆☆☆☆ | Funktion ohne Rückgabe |
| [1_038_storypoints](aufgaben/1_038_storypoints.py) | ★☆☆☆☆ | Funktion mit return |
| [1_039_einsatzkosten](aufgaben/1_039_einsatzkosten.py) | ★☆☆☆☆ | Mehrere Parameter |
| [1_040_auslastung](aufgaben/1_040_auslastung.py) | ★☆☆☆☆ | Übung: Funktionen |
| [2_002_verdoppeln](aufgaben/2_002_verdoppeln.py) | ★★☆☆☆ | Funktionen mit return |
| [2_009_verfuegbarkeit](aufgaben/2_009_verfuegbarkeit.py) | ★★☆☆☆ | Hilfsfunktionen verwenden |
| [2_010_bearbeitungszeit](aufgaben/2_010_bearbeitungszeit.py) | ★★☆☆☆ | Mehrere Rückgabewerte als Tupel |
| [2_011_kontosperre](aufgaben/2_011_kontosperre.py) | ★★☆☆☆ | Standardwerte für Parameter |
| [2_012_aufwand](aufgaben/2_012_aufwand.py) | ★★☆☆☆ | Schlüsselwort-Argumente |
| [2_013_uebertragung](aufgaben/2_013_uebertragung.py) | ★★☆☆☆ | Lokale und globale Variablen |
| [2_037_kasse](aufgaben/2_037_kasse.py) | ★★☆☆☆ | Funktionen wiederverwenden |
| [3_025_stilregeln](aufgaben/3_025_stilregeln.py) | ★★★☆☆ | lambda-Ausdrücke |
| [3_026_verteiler](aufgaben/3_026_verteiler.py) | ★★★☆☆ | map und filter |
| [3_027_backlog_ordnen](aufgaben/3_027_backlog_ordnen.py) | ★★★☆☆ | sorted mit key |
| [3_028_datenpruefung](aufgaben/3_028_datenpruefung.py) | ★★★☆☆ | Funktionen als Argumente |
| [3_032_passwortregeln](aufgaben/3_032_passwortregeln.py) | ★★★☆☆ | Funktionen als Rückgabe |
| [4_018_abfrage](aufgaben/4_018_abfrage.py) | ★★★★☆ | *args und **kwargs |
| [4_019_logzeilen](aufgaben/4_019_logzeilen.py) | ★★★★☆ | Entpacken mit *rest |
| [4_020_aktorbefehle](aufgaben/4_020_aktorbefehle.py) | ★★★★☆ | Schlüsselwort-only-Parameter |
| [4_021_prozesskennzahlen](aufgaben/4_021_prozesskennzahlen.py) | ★★★★☆ | Closures und nonlocal |
| [4_022_ticketprotokoll](aufgaben/4_022_ticketprotokoll.py) | ★★★★☆ | Dekoratoren und functools.wraps |
| [4_023_nutzwert](aufgaben/4_023_nutzwert.py) | ★★★★☆ | Dekoratoren mit Argumenten |
| [4_024_pruefsummen](aufgaben/4_024_pruefsummen.py) | ★★★★☆ | Zähl- und Cache-Dekoratoren |
| [4_025_dns_cache](aufgaben/4_025_dns_cache.py) | ★★★★☆ | functools.lru_cache |
| [4_028_tastenfeld](aufgaben/4_028_tastenfeld.py) | ★★★★☆ | functools.partial |
| [4_029_ticketverlauf](aufgaben/4_029_ticketverlauf.py) | ★★★★☆ | functools.reduce |
| [4_030_pruefagent](aufgaben/4_030_pruefagent.py) | ★★★★☆ | Dekoratoren auf Methoden und Klassen |
| [4_065_zufriedenheit](aufgaben/4_065_zufriedenheit.py) | ★★★★☆ | itemgetter, attrgetter, methodcaller |
| [4_080_fehleranalyse](aufgaben/4_080_fehleranalyse.py) | ★★★★☆ | veränderliche Standardwerte |
| [4_081_schaltregeln](aufgaben/4_081_schaltregeln.py) | ★★★★☆ | späte Bindung in Closures |
| [4_082_aenderungsantraege](aufgaben/4_082_aenderungsantraege.py) | ★★★★☆ | LEGB, global, Klassenkörper |
| [5_032_schnittstellentypen](aufgaben/5_032_schnittstellentypen.py) | ★★★★★ | functools.singledispatch |
| [5_033_projektplan](aufgaben/5_033_projektplan.py) | ★★★★★ | functools.cached_property |
| [5_034_alarmdrossel](aufgaben/5_034_alarmdrossel.py) | ★★★★★ | Methoden-Dekorator, Zustand je Objekt |
| [5_049_uploadpruefung](aufgaben/5_049_uploadpruefung.py) | ★★★★★ | inspect.signature und bind |
| [5_050_typwaechter](aufgaben/5_050_typwaechter.py) | ★★★★★ | Argumente nach Annotationen prüfen |
| [5_062_messverdichtung](aufgaben/5_062_messverdichtung.py) | ★★★★★ | Strategie und Beobachter mit Funktionen |

</details>

<a name="thema-algorithmen"></a>
<details>
<summary><b>Algorithmen & Rekursion</b> (56 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_041_einmalcode](aufgaben/1_041_einmalcode.py) | ★☆☆☆☆ | Zufall mit randint und seed |
| [2_005_wuerfel](aufgaben/2_005_wuerfel.py) | ★★☆☆☆ | Raten und Prüfen |
| [2_039_inventarnummer](aufgaben/2_039_inventarnummer.py) | ★★☆☆☆ | Ziffern mit // und % |
| [2_040_lizenzmodule](aufgaben/2_040_lizenzmodule.py) | ★★☆☆☆ | Binärdarstellung von Hand |
| [2_042_seitenlaenge](aufgaben/2_042_seitenlaenge.py) | ★★☆☆☆ | Wurzel per Bisektion |
| [2_044_testreihenfolgen](aufgaben/2_044_testreihenfolgen.py) | ★★☆☆☆ | Rekursion: Fakultät |
| [2_045_zeitschlitze](aufgaben/2_045_zeitschlitze.py) | ★★☆☆☆ | Rekursion: Fibonacci |
| [2_046_spiegeldatum](aufgaben/2_046_spiegeldatum.py) | ★★☆☆☆ | Rekursion: Palindrom |
| [2_047_ersatzteillager](aufgaben/2_047_ersatzteillager.py) | ★★☆☆☆ | Rekursion: Türme von Hanoi |
| [2_048_fehlerregister](aufgaben/2_048_fehlerregister.py) | ★★☆☆☆ | Übung: Rekursion |
| [2_050_haeufigkeitsanalyse](aufgaben/2_050_haeufigkeitsanalyse.py) | ★★☆☆☆ | Cäsar knacken |
| [2_052_wuerfelsimulation](aufgaben/2_052_wuerfelsimulation.py) | ★★☆☆☆ | Würfel simulieren, Augensumme |
| [2_053_planabweichung](aufgaben/2_053_planabweichung.py) | ★★☆☆☆ | Maximum und Minimum mit Position |
| [2_054_alarmliste](aufgaben/2_054_alarmliste.py) | ★★☆☆☆ | Element entfernen von Hand |
| [2_055_modellrangliste](aufgaben/2_055_modellrangliste.py) | ★★☆☆☆ | Merge sortierter Listen |
| [2_056_plattentausch](aufgaben/2_056_plattentausch.py) | ★★☆☆☆ | Suchen, entfernen, zusammenführen |
| [2_058_stammkunden](aufgaben/2_058_stammkunden.py) | ★★☆☆☆ | Schleifen-Invariante, Wertetabelle |
| [3_001_suche](aufgaben/3_001_suche.py) | ★★★☆☆ | Lineare Suche |
| [3_002_binaere_suche](aufgaben/3_002_binaere_suche.py) | ★★★☆☆ | Binäre Suche |
| [3_003_selection_sort](aufgaben/3_003_selection_sort.py) | ★★★☆☆ | Selection Sort |
| [3_004_bubble_sort](aufgaben/3_004_bubble_sort.py) | ★★★☆☆ | Bubble Sort mit Abbruch |
| [3_005_merge_sort](aufgaben/3_005_merge_sort.py) | ★★★☆☆ | Merge Sort rekursiv |
| [3_006_adresskonflikt](aufgaben/3_006_adresskonflikt.py) | ★★★☆☆ | Laufzeit und O-Notation |
| [3_033_prozessvarianten](aufgaben/3_033_prozessvarianten.py) | ★★★☆☆ | Memoisierung mit Dictionary |
| [3_034_rackbaum](aufgaben/3_034_rackbaum.py) | ★★★☆☆ | Rekursion auf Listen |
| [3_035_zusatzmodule](aufgaben/3_035_zusatzmodule.py) | ★★★☆☆ | Backtracking: alle Teilmengen |
| [3_036_menuereihenfolge](aufgaben/3_036_menuereihenfolge.py) | ★★★☆☆ | Permutationen rekursiv |
| [3_058_kabelplan](aufgaben/3_058_kabelplan.py) | ★★★☆☆ | Graph als Dictionary, Breitensuche |
| [3_059_lizenzpfad](aufgaben/3_059_lizenzpfad.py) | ★★★☆☆ | Tiefensuche rekursiv, Pfad |
| [3_060_grenzwertpaare](aufgaben/3_060_grenzwertpaare.py) | ★★★☆☆ | Zwei-Zeiger-Technik |
| [3_061_hilfeseite](aufgaben/3_061_hilfeseite.py) | ★★★☆☆ | Sliding Window |
| [3_062_volumenportal](aufgaben/3_062_volumenportal.py) | ★★★☆☆ | Präfixsummen, Bereichssummen |
| [3_063_restkapazitaet](aufgaben/3_063_restkapazitaet.py) | ★★★☆☆ | Paarsumme mit Menge, O(n) |
| [3_064_replikatverzug](aufgaben/3_064_replikatverzug.py) | ★★★☆☆ | Intervalle zusammenführen |
| [3_065_testumgebung](aufgaben/3_065_testumgebung.py) | ★★★☆☆ | Greedy: Termine ohne Überschneidung |
| [3_066_stummschaltung](aufgaben/3_066_stummschaltung.py) | ★★★☆☆ | Greedy: Wechselgeld und Gegenbeispiel |
| [3_067_funkrahmen](aufgaben/3_067_funkrahmen.py) | ★★★☆☆ | Möglichkeiten zählen mit Tabelle |
| [3_068_integrationsplan](aufgaben/3_068_integrationsplan.py) | ★★★☆☆ | Wege im Gitter zählen |
| [3_069_angriffsbericht](aufgaben/3_069_angriffsbericht.py) | ★★★☆☆ | Übung: Algorithmen-Muster |
| [3_070_merkmalstabelle](aufgaben/3_070_merkmalstabelle.py) | ★★★☆☆ | Sieb des Eratosthenes |
| [3_071_serientickets](aufgaben/3_071_serientickets.py) | ★★★☆☆ | ggT und kgV, euklidischer Algorithmus |
| [3_072_blockverteilung](aufgaben/3_072_blockverteilung.py) | ★★★☆☆ | Schnelles Potenzieren modulo m |
| [3_073_kostenrisiko](aufgaben/3_073_kostenrisiko.py) | ★★★☆☆ | Monte-Carlo-Simulation, Pi schätzen |
| [3_074_zufallsbits](aufgaben/3_074_zufallsbits.py) | ★★★☆☆ | Galton-Brett simulieren |
| [4_026_vm_platzierung](aufgaben/4_026_vm_platzierung.py) | ★★★★☆ | Rucksackproblem mit Tabelle |
| [4_027_befehlsvorschlag](aufgaben/4_027_befehlsvorschlag.py) | ★★★★☆ | Editierdistanz mit Tabelle |
| [4_063_abfragestau](aufgaben/4_063_abfragestau.py) | ★★★★☆ | Monotoner Stack |
| [4_064_bauplan](aufgaben/4_064_bauplan.py) | ★★★★☆ | Topologische Sortierung (Kahn) |
| [4_075_linkkosten](aufgaben/4_075_linkkosten.py) | ★★★★☆ | Dijkstra mit heapq |
| [4_076_zeitleiste](aufgaben/4_076_zeitleiste.py) | ★★★★☆ | k Listen mit Heap mergen |
| [4_078_testimages](aufgaben/4_078_testimages.py) | ★★★★☆ | Binäre Suche auf der Antwort |
| [4_087_losvergabe](aufgaben/4_087_losvergabe.py) | ★★★★☆ | Backtracking mit Abschneiden |
| [4_088_sicherheitsaudit](aufgaben/4_088_sicherheitsaudit.py) | ★★★★☆ | Übung: Graphen |
| [5_058_backlogwerkzeug](aufgaben/5_058_backlogwerkzeug.py) | ★★★★★ | Kosten eingebauter Operationen |
| [5_060_syntaxbaum](aufgaben/5_060_syntaxbaum.py) | ★★★★★ | Aufrufstapel, Rekursion als Schleife |
| [5_061_wartungstour](aufgaben/5_061_wartungstour.py) | ★★★★★ | Bitmasken-DP, beste Reihenfolge |

</details>

<a name="thema-datenstrukturen"></a>
<details>
<summary><b>Datenstrukturen</b> (41 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_027_meilensteine](aufgaben/1_027_meilensteine.py) | ★☆☆☆☆ | Listen: Index und len |
| [1_029_cpu_alarme](aufgaben/1_029_cpu_alarme.py) | ★☆☆☆☆ | Liste mit append aufbauen |
| [1_030_geraeteliste](aufgaben/1_030_geraeteliste.py) | ★☆☆☆☆ | Listen verändern: ersetzen, remove |
| [1_031_auftragszeiten](aufgaben/1_031_auftragszeiten.py) | ★☆☆☆☆ | min, max, sum, sorted |
| [1_032_ticketbewertung](aufgaben/1_032_ticketbewertung.py) | ★☆☆☆☆ | Übung: Listen |
| [1_044_lebenszykluskosten](aufgaben/1_044_lebenszykluskosten.py) | ★☆☆☆☆ | Tupel bauen und auspacken |
| [1_045_beschriftung](aufgaben/1_045_beschriftung.py) | ★☆☆☆☆ | Wert zu einem Schlüssel |
| [1_046_tabellenspalte](aufgaben/1_046_tabellenspalte.py) | ★☆☆☆☆ | Eintrag hinzufügen, .items() |
| [1_047_rolllaeden](aufgaben/1_047_rolllaeden.py) | ★☆☆☆☆ | Tupel im Dictionary |
| [2_006_warteschlange](aufgaben/2_006_warteschlange.py) | ★★☆☆☆ | Listen und for über eine Liste |
| [2_018_abfrageseiten](aufgaben/2_018_abfrageseiten.py) | ★★☆☆☆ | Slicing und Kopien von Listen |
| [2_019_messreihe](aufgaben/2_019_messreihe.py) | ★★☆☆☆ | Liste in einer Funktion ändern |
| [2_020_sensorraster](aufgaben/2_020_sensorraster.py) | ★★☆☆☆ | Listen von Listen |
| [2_023_angebote](aufgaben/2_023_angebote.py) | ★★☆☆☆ | sort gegen sorted |
| [2_024_fehlversuche](aufgaben/2_024_fehlversuche.py) | ★★☆☆☆ | Übung: Listen |
| [2_025_dnsanfragen](aufgaben/2_025_dnsanfragen.py) | ★★☆☆☆ | Dictionaries zählen |
| [2_026_containerspeicher](aufgaben/2_026_containerspeicher.py) | ★★☆☆☆ | get mit Standardwert |
| [2_027_fehlerbericht](aufgaben/2_027_fehlerbericht.py) | ★★☆☆☆ | Dictionary als Datensatz |
| [2_028_menuepunkte](aufgaben/2_028_menuepunkte.py) | ★★☆☆☆ | Mengen: Schnitt, Vereinigung |
| [2_029_risikomatrix](aufgaben/2_029_risikomatrix.py) | ★★☆☆☆ | Tupel als Dictionary-Schlüssel |
| [2_030_kundenstamm](aufgaben/2_030_kundenstamm.py) | ★★☆☆☆ | Liste von Dictionaries filtern |
| [2_031_alarmauswertung](aufgaben/2_031_alarmauswertung.py) | ★★☆☆☆ | Übung: Dictionaries und Mengen |
| [2_057_klickraster](aufgaben/2_057_klickraster.py) | ★★☆☆☆ | Matrix transponieren, Summen |
| [3_056_regelklammern](aufgaben/3_056_regelklammern.py) | ★★★☆☆ | Stack, Klammern prüfen |
| [3_057_paketpuffer](aufgaben/3_057_paketpuffer.py) | ★★★☆☆ | Warteschlange mit deque |
| [3_075_dialogablauf](aufgaben/3_075_dialogablauf.py) | ★★★☆☆ | Zustandsautomat mit Dictionary |
| [4_059_barrierefreiheit](aufgaben/4_059_barrierefreiheit.py) | ★★★★☆ | collections.Counter |
| [4_060_wlan_anmeldungen](aufgaben/4_060_wlan_anmeldungen.py) | ★★★★☆ | collections.defaultdict |
| [4_061_stromkreise](aufgaben/4_061_stromkreise.py) | ★★★★☆ | namedtuple und NamedTuple |
| [4_062_velocity](aufgaben/4_062_velocity.py) | ★★★★☆ | deque mit maxlen und rotate |
| [4_074_ereignisschlange](aufgaben/4_074_ereignisschlange.py) | ★★★★☆ | heapq und Prioritätswarteschlange |
| [4_077_qualitaetsstufen](aufgaben/4_077_qualitaetsstufen.py) | ★★★★☆ | bisect: Stufen und Bereiche |
| [4_079_symbolleisten](aufgaben/4_079_symbolleisten.py) | ★★★★☆ | copy: flach gegen tief |
| [4_083_kategoriebaum](aufgaben/4_083_kategoriebaum.py) | ★★★★☆ | Baum als Klasse, Generator |
| [4_084_prozesskette](aufgaben/4_084_prozesskette.py) | ★★★★☆ | Verkettete Liste mit Iterator |
| [4_085_stoerungsgruppen](aufgaben/4_085_stoerungsgruppen.py) | ★★★★☆ | Union-Find mit Pfadkompression |
| [4_086_alarmzustaendigkeit](aufgaben/4_086_alarmzustaendigkeit.py) | ★★★★☆ | Trie, Präfixsuche, längstes Präfix |
| [5_021_messreihe](aufgaben/5_021_messreihe.py) | ★★★★★ | Eigene Sequenz mit Slices |
| [5_022_backlog](aufgaben/5_022_backlog.py) | ★★★★★ | Eigenes Mapping mit MutableMapping |
| [5_035_modellcache](aufgaben/5_035_modellcache.py) | ★★★★★ | weakref, WeakValueDictionary |
| [5_038_routingentwurf](aufgaben/5_038_routingentwurf.py) | ★★★★★ | __copy__ und __deepcopy__ |

</details>

<a name="thema-fehler"></a>
<details>
<summary><b>Fehler & Testen</b> (25 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [2_033_messwert](aufgaben/2_033_messwert.py) | ★★☆☆☆ | try/except in einer Funktion |
| [2_034_portfreigaben](aufgaben/2_034_portfreigaben.py) | ★★☆☆☆ | try/except in einer Schleife |
| [2_035_schrittdauer](aufgaben/2_035_schrittdauer.py) | ★★☆☆☆ | Mehrere Ausnahmen in einem except |
| [2_036_ticketaufwand](aufgaben/2_036_ticketaufwand.py) | ★★☆☆☆ | Übung: Fehler abfangen |
| [2_038_kasse_eingaben](aufgaben/2_038_kasse_eingaben.py) | ★★☆☆☆ | Eingaben prüfen und wiederholen |
| [3_007_durchlaufzeiten](aufgaben/3_007_durchlaufzeiten.py) | ★★★☆☆ | Fehler abfangen mit try/except |
| [3_008_stueckpreise](aufgaben/3_008_stueckpreise.py) | ★★★☆☆ | Mehrere except, else und finally |
| [3_009_raid](aufgaben/3_009_raid.py) | ★★★☆☆ | `raise` und Vorbedingungen |
| [3_010_reaktionszeit](aufgaben/3_010_reaktionszeit.py) | ★★★☆☆ | `assert` als Vertrag |
| [3_011_postleitzahl](aufgaben/3_011_postleitzahl.py) | ★★★☆☆ | Testfälle schreiben |
| [3_012_portbereich](aufgaben/3_012_portbereich.py) | ★★★☆☆ | Äquivalenzklassen und Grenzwerte |
| [3_015_burndown](aufgaben/3_015_burndown.py) | ★★★☆☆ | Debugging mit Wertetabelle |
| [3_016_kundenimport](aufgaben/3_016_kundenimport.py) | ★★★☆☆ | Traceback lesen |
| [3_029_alarmregeln](aufgaben/3_029_alarmregeln.py) | ★★★☆☆ | Ausnahmen über Funktionen hinweg |
| [3_030_sensorabfrage](aufgaben/3_030_sensorabfrage.py) | ★★★☆☆ | Stammbaum der Ausnahmen |
| [3_031_abfrageversuche](aufgaben/3_031_abfrageversuche.py) | ★★★☆☆ | Ausnahme weiterreichen mit `raise` |
| [4_051_trainingslauf](aufgaben/4_051_trainingslauf.py) | ★★★★☆ | with, __enter__ und __exit__ |
| [4_052_wartungsfenster](aufgaben/4_052_wartungsfenster.py) | ★★★★☆ | contextlib.contextmanager |
| [4_055_switchabfrage](aufgaben/4_055_switchabfrage.py) | ★★★★☆ | closing, suppress, Callback |
| [4_056_migrationsfehler](aufgaben/4_056_migrationsfehler.py) | ★★★★☆ | eigene Fehlerklassen, Hierarchie |
| [4_058_passworttresor](aufgaben/4_058_passworttresor.py) | ★★★★☆ | raise … from, Fehler umwandeln |
| [5_025_zugriffspruefung](aufgaben/5_025_zugriffspruefung.py) | ★★★★★ | __exit__ unterdrückt Ausnahmen |
| [5_026_quellensammler](aufgaben/5_026_quellensammler.py) | ★★★★★ | contextlib.ExitStack |
| [5_031_lagertransaktion](aufgaben/5_031_lagertransaktion.py) | ★★★★★ | contextmanager mit Fehlerpfad |
| [5_059_stundenabgleich](aufgaben/5_059_stundenabgleich.py) | ★★★★★ | Profiling mit cProfile und pstats |

</details>

<a name="thema-klassen"></a>
<details>
<summary><b>Klassen & Objekte</b> (37 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [3_037_switchport](aufgaben/3_037_switchport.py) | ★★★☆☆ | Klasse mit Methoden |
| [3_039_versionsnummer](aufgaben/3_039_versionsnummer.py) | ★★★☆☆ | __str__ und __eq__ |
| [3_040_sensornetz](aufgaben/3_040_sensornetz.py) | ★★★☆☆ | Objekte in Listen |
| [3_042_ticketarten](aufgaben/3_042_ticketarten.py) | ★★★☆☆ | Vererbung mit super() |
| [3_043_messstellen](aufgaben/3_043_messstellen.py) | ★★★☆☆ | Klassen- und Instanzattribute |
| [4_001_konto](aufgaben/4_001_konto.py) | ★★★★☆ | Klassen und Invarianten |
| [4_002_abfahrt](aufgaben/4_002_abfahrt.py) | ★★★★☆ | `__repr__` und `__str__` |
| [4_003_sitzplatz](aufgaben/4_003_sitzplatz.py) | ★★★★☆ | `__eq__` und `__hash__` |
| [4_004_engpass](aufgaben/4_004_engpass.py) | ★★★★☆ | `__lt__` und `total_ordering` |
| [4_005_sprint](aufgaben/4_005_sprint.py) | ★★★★☆ | `property` mit Setter |
| [4_006_beschaffung](aufgaben/4_006_beschaffung.py) | ★★★★☆ | Vererbung, `super()` und Polymorphie |
| [4_007_virtuelle_maschinen](aufgaben/4_007_virtuelle_maschinen.py) | ★★★★☆ | `classmethod` als Konstruktor |
| [4_008_ticketprioritaet](aufgaben/4_008_ticketprioritaet.py) | ★★★★☆ | `staticmethod` als Hilfsfunktion |
| [4_009_testfaelle](aufgaben/4_009_testfaelle.py) | ★★★★☆ | Klassenattribute als Zähler und Registry |
| [4_010_messreihen](aufgaben/4_010_messreihen.py) | ★★★★☆ | Mehrfachvererbung, Mixins und MRO |
| [4_011_sicherungen](aufgaben/4_011_sicherungen.py) | ★★★★☆ | `abc.ABC` und `@abstractmethod` |
| [4_012_lizenzen](aufgaben/4_012_lizenzen.py) | ★★★★☆ | `@dataclass` und `field` |
| [4_014_patchstand](aufgaben/4_014_patchstand.py) | ★★★★☆ | dataclass: frozen, order, `__post_init__` |
| [4_015_review_status](aufgaben/4_015_review_status.py) | ★★★★☆ | `enum.Enum` |
| [5_001_deskriptor](aufgaben/5_001_deskriptor.py) | ★★★★★ | Deskriptoren |
| [5_002_eigenschaft](aufgaben/5_002_eigenschaft.py) | ★★★★★ | `property` nachbauen |
| [5_004_nachbarn](aufgaben/5_004_nachbarn.py) | ★★★★★ | `__slots__` |
| [5_005_kostenzaehler](aufgaben/5_005_kostenzaehler.py) | ★★★★★ | `__getattr__`, Proxy-Objekt |
| [5_007_schnittstelle](aufgaben/5_007_schnittstelle.py) | ★★★★★ | `__setattr__`, `__delattr__` |
| [5_008_speicherinventar](aufgaben/5_008_speicherinventar.py) | ★★★★★ | `__new__`, Singleton, Unterklasse von int |
| [5_010_formularfelder](aufgaben/5_010_formularfelder.py) | ★★★★★ | `__init_subclass__` |
| [5_011_pakettypen](aufgaben/5_011_pakettypen.py) | ★★★★★ | Klassen mit type() erzeugen |
| [5_013_pruefregeln](aufgaben/5_013_pruefregeln.py) | ★★★★★ | Eigene Metaklasse |
| [5_014_sensorstapel](aufgaben/5_014_sensorstapel.py) | ★★★★★ | `__class_getitem__` |
| [5_016_benachrichtigung](aufgaben/5_016_benachrichtigung.py) | ★★★★★ | typing.Protocol |
| [5_017_lizenzinventar](aufgaben/5_017_lizenzinventar.py) | ★★★★★ | virtuelle Unterklassen |
| [5_019_datenmenge](aufgaben/5_019_datenmenge.py) | ★★★★★ | `__add__`, `__radd__`, `__iadd__` |
| [5_020_betriebsprotokoll](aufgaben/5_020_betriebsprotokoll.py) | ★★★★★ | `__call__` und Dekorator-Klassen |
| [5_023_wahrheitswert](aufgaben/5_023_wahrheitswert.py) | ★★★★★ | __bool__ und __len__ |
| [5_024_datenmenge_format](aufgaben/5_024_datenmenge_format.py) | ★★★★★ | __format__ mit eigener Spec |
| [5_036_altgeraete](aufgaben/5_036_altgeraete.py) | ★★★★★ | Hash-Vertrag, frozen dataclass |
| [5_051_funkprofil](aufgaben/5_051_funkprofil.py) | ★★★★★ | Deskriptoren in dataclasses |

</details>

<a name="thema-programmaufbau"></a>
<details>
<summary><b>Programmaufbau</b> (10 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [1_048_druckerwartung](aufgaben/1_048_druckerwartung.py) | ★☆☆☆☆ | Docstrings und Kommentare |
| [1_049_ratedauer](aufgaben/1_049_ratedauer.py) | ★☆☆☆☆ | main und __name__ |
| [2_060_materialliste](aufgaben/2_060_materialliste.py) | ★★☆☆☆ | Menüprogramm mit Dictionary |
| [3_045_kachelraster](aufgaben/3_045_kachelraster.py) | ★★★☆☆ | math, statistics, random nutzen |
| [3_077_guthabenbuch](aufgaben/3_077_guthabenbuch.py) | ★★★☆☆ | Kleines Projekt: Guthabenbuch |
| [4_016_formularpruefung](aufgaben/4_016_formularpruefung.py) | ★★★★☆ | Typannotationen, `X | None` |
| [4_017_backlog](aufgaben/4_017_backlog.py) | ★★★★☆ | TypeVar, generische Funktionen |
| [4_089_inventur](aufgaben/4_089_inventur.py) | ★★★★☆ | Projekt: Lager mit Inventur |
| [5_052_pruefplugins](aufgaben/5_052_pruefplugins.py) | ★★★★★ | Plugins mit importlib laden |
| [5_063_sensorsimulation](aufgaben/5_063_sensorsimulation.py) | ★★★★★ | Ereignisgesteuerte Simulation |

</details>

<a name="thema-nebenlaeufigkeit"></a>
<details>
<summary><b>Nebenläufigkeit</b> (11 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [4_053_linkpruefung](aufgaben/4_053_linkpruefung.py) | ★★★★☆ | ThreadPoolExecutor.map |
| [5_039_teilprojekte](aufgaben/5_039_teilprojekte.py) | ★★★★★ | async def, await, asyncio.run |
| [5_040_datenknoten](aufgaben/5_040_datenknoten.py) | ★★★★★ | asyncio.gather |
| [5_041_testzeitlimit](aufgaben/5_041_testzeitlimit.py) | ★★★★★ | create_task, wait_for, Abbruch |
| [5_042_logsammler](aufgaben/5_042_logsammler.py) | ★★★★★ | asyncio.Queue, Erzeuger, Verbraucher |
| [5_043_luefterschaltung](aufgaben/5_043_luefterschaltung.py) | ★★★★★ | async for, asynchrone Generatoren |
| [5_044_planungspoker](aufgaben/5_044_planungspoker.py) | ★★★★★ | threading: start, join, Ergebnisse |
| [5_045_prozessuebergaenge](aufgaben/5_045_prozessuebergaenge.py) | ★★★★★ | threading: Race Condition, Lock |
| [5_046_ferndiagnose](aufgaben/5_046_ferndiagnose.py) | ★★★★★ | submit, Future, as_completed |
| [5_047_anfragekennung](aufgaben/5_047_anfragekennung.py) | ★★★★★ | contextvars: Kontext ohne globale Variable |
| [5_048_stromvergleich](aufgaben/5_048_stromvergleich.py) | ★★★★★ | Übung: asyncio und Threads |

</details>

<a name="thema-datenanalyse"></a>
<details>
<summary><b>Datenanalyse</b> (25 Aufgaben)</summary>

| Aufgabe | Stufe | Inhalt |
| --- | --- | --- |
| [2_032_energiezaehler](aufgaben/2_032_energiezaehler.py) | ★★☆☆☆ | Tabelle als Liste von Dicts |
| [2_041_maskenzeiten](aufgaben/2_041_maskenzeiten.py) | ★★☆☆☆ | Summe je Kategorie |
| [3_013_testquoten](aufgaben/3_013_testquoten.py) | ★★★☆☆ | numpy: Arrays, elementweise rechnen |
| [3_014_usability](aufgaben/3_014_usability.py) | ★★★☆☆ | numpy: Masken, sum, mean, max |
| [3_038_kundenstamm](aufgaben/3_038_kundenstamm.py) | ★★★☆☆ | pandas: DataFrame, Spalten |
| [3_041_sprintauswahl](aufgaben/3_041_sprintauswahl.py) | ★★★☆☆ | pandas: Masken, sort_values |
| [3_044_speicherprognose](aufgaben/3_044_speicherprognose.py) | ★★★☆☆ | pandas: neue Spalten berechnen |
| [3_047_raumsensoren](aufgaben/3_047_raumsensoren.py) | ★★★☆☆ | pandas: fehlende Werte |
| [3_053_kuehltransport](aufgaben/3_053_kuehltransport.py) | ★★★☆☆ | pandas: read_csv und astype |
| [4_013_leitungsauslastung](aufgaben/4_013_leitungsauslastung.py) | ★★★★☆ | numpy: Achsen und Broadcasting |
| [4_031_anmeldungen](aufgaben/4_031_anmeldungen.py) | ★★★★☆ | polars select, filter, with_columns |
| [4_037_bestellabfrage](aufgaben/4_037_bestellabfrage.py) | ★★★★☆ | DuckDB: SQL auf DataFrame |
| [4_041_co2_bilanz](aufgaben/4_041_co2_bilanz.py) | ★★★★☆ | pandas: groupby und agg |
| [4_045_stoerungscodes](aufgaben/4_045_stoerungscodes.py) | ★★★★☆ | pandas: merge |
| [4_050_schwachstellen](aufgaben/4_050_schwachstellen.py) | ★★★★☆ | pandas: pivot_table |
| [4_054_kontrastpruefung](aufgaben/4_054_kontrastpruefung.py) | ★★★★☆ | assign, query, Method Chaining |
| [4_057_abnahme](aufgaben/4_057_abnahme.py) | ★★★★☆ | polars group_by und join |
| [4_068_kontenpruefung](aufgaben/4_068_kontenpruefung.py) | ★★★★☆ | pandas: .str-Methoden |
| [4_072_cloudkosten](aufgaben/4_072_cloudkosten.py) | ★★★★☆ | pandas: to_datetime, .dt, resample |
| [5_003_anmeldeprotokoll](aufgaben/5_003_anmeldeprotokoll.py) | ★★★★★ | numpy: Views, Kopien, Fancy Indexing |
| [5_006_anmelderisiko](aufgaben/5_006_anmelderisiko.py) | ★★★★★ | pandas: apply gegen vektorisiert |
| [5_009_testlaufzeiten](aufgaben/5_009_testlaufzeiten.py) | ★★★★★ | DuckDB: Fensterfunktionen |
| [5_012_kundenimport](aufgaben/5_012_kundenimport.py) | ★★★★★ | polars Lazy-Modus |
| [5_015_soll_ist](aufgaben/5_015_soll_ist.py) | ★★★★★ | pandas, polars und SQL im Vergleich |
| [5_018_loeschfristen](aufgaben/5_018_loeschfristen.py) | ★★★★★ | Projekt: bereinigen, verknüpfen, auswerten |

</details>

### Nach Stufe

<details>
<summary><b>Stufe 1 ★☆☆☆☆: Erste Schritte mit vorgegebenem Code</b> (49 Aufgaben)</summary>

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
| [1_017_temperaturwarnung](aufgaben/1_017_temperaturwarnung.py) | Bedingungen & Schleifen | if-Anweisung |
| [1_018_bewaesserung](aufgaben/1_018_bewaesserung.py) | Bedingungen & Schleifen | if/else |
| [1_019_abc_analyse](aufgaben/1_019_abc_analyse.py) | Bedingungen & Schleifen | if/elif/else |
| [1_020_eskalation](aufgaben/1_020_eskalation.py) | Bedingungen & Schleifen | and, or, not |
| [1_021_leasing](aufgaben/1_021_leasing.py) | Bedingungen & Schleifen | Übung: Bedingungen |
| [1_022_loeschen](aufgaben/1_022_loeschen.py) | Bedingungen & Schleifen | for über range(n) |
| [1_023_adressbereich](aufgaben/1_023_adressbereich.py) | Bedingungen & Schleifen | for über range(a, b) |
| [1_024_rack](aufgaben/1_024_rack.py) | Bedingungen & Schleifen | range mit Schrittweite |
| [1_025_testlaufzeit](aufgaben/1_025_testlaufzeit.py) | Bedingungen & Schleifen | Zähler in der Schleife |
| [1_026_formulartest](aufgaben/1_026_formulartest.py) | Bedingungen & Schleifen | Übung: Schleifen |
| [1_027_meilensteine](aufgaben/1_027_meilensteine.py) | Datenstrukturen | Listen: Index und len |
| [1_028_fehlende_werte](aufgaben/1_028_fehlende_werte.py) | Bedingungen & Schleifen | for über eine Liste |
| [1_029_cpu_alarme](aufgaben/1_029_cpu_alarme.py) | Datenstrukturen | Liste mit append aufbauen |
| [1_030_geraeteliste](aufgaben/1_030_geraeteliste.py) | Datenstrukturen | Listen verändern: ersetzen, remove |
| [1_031_auftragszeiten](aufgaben/1_031_auftragszeiten.py) | Datenstrukturen | min, max, sum, sorted |
| [1_032_ticketbewertung](aufgaben/1_032_ticketbewertung.py) | Datenstrukturen | Übung: Listen |
| [1_033_schriftgroesse](aufgaben/1_033_schriftgroesse.py) | Bedingungen & Schleifen | while-Schleife |
| [1_034_pingzeiten](aufgaben/1_034_pingzeiten.py) | Bedingungen & Schleifen | Eingabeschleife bis stop |
| [1_035_altersangaben](aufgaben/1_035_altersangaben.py) | Bedingungen & Schleifen | Übung: while |
| [1_036_reviewdauer](aufgaben/1_036_reviewdauer.py) | Funktionen | Funktion mehrfach aufrufen |
| [1_037_heizungsventile](aufgaben/1_037_heizungsventile.py) | Funktionen | Funktion ohne Rückgabe |
| [1_038_storypoints](aufgaben/1_038_storypoints.py) | Funktionen | Funktion mit return |
| [1_039_einsatzkosten](aufgaben/1_039_einsatzkosten.py) | Funktionen | Mehrere Parameter |
| [1_040_auslastung](aufgaben/1_040_auslastung.py) | Funktionen | Übung: Funktionen |
| [1_041_einmalcode](aufgaben/1_041_einmalcode.py) | Algorithmen & Rekursion | Zufall mit randint und seed |
| [1_042_zeittabelle](aufgaben/1_042_zeittabelle.py) | Bedingungen & Schleifen | Verschachtelte Schleifen |
| [1_043_raidstatus](aufgaben/1_043_raidstatus.py) | Texte, Zahlen & Dateien | Zeichen zählen mit for |
| [1_044_lebenszykluskosten](aufgaben/1_044_lebenszykluskosten.py) | Datenstrukturen | Tupel bauen und auspacken |
| [1_045_beschriftung](aufgaben/1_045_beschriftung.py) | Datenstrukturen | Wert zu einem Schlüssel |
| [1_046_tabellenspalte](aufgaben/1_046_tabellenspalte.py) | Datenstrukturen | Eintrag hinzufügen, .items() |
| [1_047_rolllaeden](aufgaben/1_047_rolllaeden.py) | Datenstrukturen | Tupel im Dictionary |
| [1_048_druckerwartung](aufgaben/1_048_druckerwartung.py) | Programmaufbau | Docstrings und Kommentare |
| [1_049_ratedauer](aufgaben/1_049_ratedauer.py) | Programmaufbau | main und __name__ |

</details>

<details>
<summary><b>Stufe 2 ★★☆☆☆: Kleine Programme selbst schreiben</b> (60 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [2_001_zaehlen](aufgaben/2_001_zaehlen.py) | Bedingungen & Schleifen | for-Schleife |
| [2_002_verdoppeln](aufgaben/2_002_verdoppeln.py) | Funktionen | Funktionen mit return |
| [2_003_gerade](aufgaben/2_003_gerade.py) | Bedingungen & Schleifen | if und Funktionen |
| [2_004_countdown](aufgaben/2_004_countdown.py) | Bedingungen & Schleifen | while-Schleife |
| [2_005_wuerfel](aufgaben/2_005_wuerfel.py) | Algorithmen & Rekursion | Raten und Prüfen |
| [2_006_warteschlange](aufgaben/2_006_warteschlange.py) | Datenstrukturen | Listen und for über eine Liste |
| [2_007_transporter](aufgaben/2_007_transporter.py) | Bedingungen & Schleifen | Schleife mit break |
| [2_008_stromverbrauch](aufgaben/2_008_stromverbrauch.py) | Bedingungen & Schleifen | Schleife mit continue |
| [2_009_verfuegbarkeit](aufgaben/2_009_verfuegbarkeit.py) | Funktionen | Hilfsfunktionen verwenden |
| [2_010_bearbeitungszeit](aufgaben/2_010_bearbeitungszeit.py) | Funktionen | Mehrere Rückgabewerte als Tupel |
| [2_011_kontosperre](aufgaben/2_011_kontosperre.py) | Funktionen | Standardwerte für Parameter |
| [2_012_aufwand](aufgaben/2_012_aufwand.py) | Funktionen | Schlüsselwort-Argumente |
| [2_013_uebertragung](aufgaben/2_013_uebertragung.py) | Funktionen | Lokale und globale Variablen |
| [2_014_kuerzel](aufgaben/2_014_kuerzel.py) | Texte, Zahlen & Dateien | Texte durchlaufen und neu aufbauen |
| [2_015_namensabgleich](aufgaben/2_015_namensabgleich.py) | Texte, Zahlen & Dateien | `split` und `join` |
| [2_016_codemetrik](aufgaben/2_016_codemetrik.py) | Texte, Zahlen & Dateien | Tabellen mit f-String-Breiten |
| [2_017_arbeitspakete](aufgaben/2_017_arbeitspakete.py) | Texte, Zahlen & Dateien | Übung: Zeilen zerlegen, Tabelle ausgeben |
| [2_018_abfrageseiten](aufgaben/2_018_abfrageseiten.py) | Datenstrukturen | Slicing und Kopien von Listen |
| [2_019_messreihe](aufgaben/2_019_messreihe.py) | Datenstrukturen | Liste in einer Funktion ändern |
| [2_020_sensorraster](aufgaben/2_020_sensorraster.py) | Datenstrukturen | Listen von Listen |
| [2_021_prozessschritte](aufgaben/2_021_prozessschritte.py) | Bedingungen & Schleifen | enumerate |
| [2_022_reaktionsfristen](aufgaben/2_022_reaktionsfristen.py) | Bedingungen & Schleifen | zip |
| [2_023_angebote](aufgaben/2_023_angebote.py) | Datenstrukturen | sort gegen sorted |
| [2_024_fehlversuche](aufgaben/2_024_fehlversuche.py) | Datenstrukturen | Übung: Listen |
| [2_025_dnsanfragen](aufgaben/2_025_dnsanfragen.py) | Datenstrukturen | Dictionaries zählen |
| [2_026_containerspeicher](aufgaben/2_026_containerspeicher.py) | Datenstrukturen | get mit Standardwert |
| [2_027_fehlerbericht](aufgaben/2_027_fehlerbericht.py) | Datenstrukturen | Dictionary als Datensatz |
| [2_028_menuepunkte](aufgaben/2_028_menuepunkte.py) | Datenstrukturen | Mengen: Schnitt, Vereinigung |
| [2_029_risikomatrix](aufgaben/2_029_risikomatrix.py) | Datenstrukturen | Tupel als Dictionary-Schlüssel |
| [2_030_kundenstamm](aufgaben/2_030_kundenstamm.py) | Datenstrukturen | Liste von Dictionaries filtern |
| [2_031_alarmauswertung](aufgaben/2_031_alarmauswertung.py) | Datenstrukturen | Übung: Dictionaries und Mengen |
| [2_032_energiezaehler](aufgaben/2_032_energiezaehler.py) | Datenanalyse | Tabelle als Liste von Dicts |
| [2_033_messwert](aufgaben/2_033_messwert.py) | Fehler & Testen | try/except in einer Funktion |
| [2_034_portfreigaben](aufgaben/2_034_portfreigaben.py) | Fehler & Testen | try/except in einer Schleife |
| [2_035_schrittdauer](aufgaben/2_035_schrittdauer.py) | Fehler & Testen | Mehrere Ausnahmen in einem except |
| [2_036_ticketaufwand](aufgaben/2_036_ticketaufwand.py) | Fehler & Testen | Übung: Fehler abfangen |
| [2_037_kasse](aufgaben/2_037_kasse.py) | Funktionen | Funktionen wiederverwenden |
| [2_038_kasse_eingaben](aufgaben/2_038_kasse_eingaben.py) | Fehler & Testen | Eingaben prüfen und wiederholen |
| [2_039_inventarnummer](aufgaben/2_039_inventarnummer.py) | Algorithmen & Rekursion | Ziffern mit // und % |
| [2_040_lizenzmodule](aufgaben/2_040_lizenzmodule.py) | Algorithmen & Rekursion | Binärdarstellung von Hand |
| [2_041_maskenzeiten](aufgaben/2_041_maskenzeiten.py) | Datenanalyse | Summe je Kategorie |
| [2_042_seitenlaenge](aufgaben/2_042_seitenlaenge.py) | Algorithmen & Rekursion | Wurzel per Bisektion |
| [2_043_summenabgleich](aufgaben/2_043_summenabgleich.py) | Texte, Zahlen & Dateien | Kommazahlen vergleichen |
| [2_044_testreihenfolgen](aufgaben/2_044_testreihenfolgen.py) | Algorithmen & Rekursion | Rekursion: Fakultät |
| [2_045_zeitschlitze](aufgaben/2_045_zeitschlitze.py) | Algorithmen & Rekursion | Rekursion: Fibonacci |
| [2_046_spiegeldatum](aufgaben/2_046_spiegeldatum.py) | Algorithmen & Rekursion | Rekursion: Palindrom |
| [2_047_ersatzteillager](aufgaben/2_047_ersatzteillager.py) | Algorithmen & Rekursion | Rekursion: Türme von Hanoi |
| [2_048_fehlerregister](aufgaben/2_048_fehlerregister.py) | Algorithmen & Rekursion | Übung: Rekursion |
| [2_049_caesar](aufgaben/2_049_caesar.py) | Texte, Zahlen & Dateien | Cäsar mit ord und chr |
| [2_050_haeufigkeitsanalyse](aufgaben/2_050_haeufigkeitsanalyse.py) | Algorithmen & Rekursion | Cäsar knacken |
| [2_051_datenkontingent](aufgaben/2_051_datenkontingent.py) | Texte, Zahlen & Dateien | Schaltjahr, Tage im Monat |
| [2_052_wuerfelsimulation](aufgaben/2_052_wuerfelsimulation.py) | Algorithmen & Rekursion | Würfel simulieren, Augensumme |
| [2_053_planabweichung](aufgaben/2_053_planabweichung.py) | Algorithmen & Rekursion | Maximum und Minimum mit Position |
| [2_054_alarmliste](aufgaben/2_054_alarmliste.py) | Algorithmen & Rekursion | Element entfernen von Hand |
| [2_055_modellrangliste](aufgaben/2_055_modellrangliste.py) | Algorithmen & Rekursion | Merge sortierter Listen |
| [2_056_plattentausch](aufgaben/2_056_plattentausch.py) | Algorithmen & Rekursion | Suchen, entfernen, zusammenführen |
| [2_057_klickraster](aufgaben/2_057_klickraster.py) | Datenstrukturen | Matrix transponieren, Summen |
| [2_058_stammkunden](aufgaben/2_058_stammkunden.py) | Algorithmen & Rekursion | Schleifen-Invariante, Wertetabelle |
| [2_059_displaysymbole](aufgaben/2_059_displaysymbole.py) | Bedingungen & Schleifen | Dreieck und Raute aus Sternchen |
| [2_060_materialliste](aufgaben/2_060_materialliste.py) | Programmaufbau | Menüprogramm mit Dictionary |

</details>

<details>
<summary><b>Stufe 3 ★★★☆☆: Probleme zerlegen und lösen</b> (77 Aufgaben)</summary>

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
| [3_013_testquoten](aufgaben/3_013_testquoten.py) | Datenanalyse | numpy: Arrays, elementweise rechnen |
| [3_014_usability](aufgaben/3_014_usability.py) | Datenanalyse | numpy: Masken, sum, mean, max |
| [3_015_burndown](aufgaben/3_015_burndown.py) | Fehler & Testen | Debugging mit Wertetabelle |
| [3_016_kundenimport](aufgaben/3_016_kundenimport.py) | Fehler & Testen | Traceback lesen |
| [3_017_lastspitzen](aufgaben/3_017_lastspitzen.py) | Bedingungen & Schleifen | List Comprehension |
| [3_018_sensorkarte](aufgaben/3_018_sensorkarte.py) | Bedingungen & Schleifen | Dict Comprehension |
| [3_019_ereignisprotokoll](aufgaben/3_019_ereignisprotokoll.py) | Bedingungen & Schleifen | Set Comprehension |
| [3_020_ticketstrom](aufgaben/3_020_ticketstrom.py) | Bedingungen & Schleifen | iter() und next() |
| [3_021_kostenvergleich](aufgaben/3_021_kostenvergleich.py) | Bedingungen & Schleifen | Verbrauchte Iteratoren |
| [3_022_lauflaengen](aufgaben/3_022_lauflaengen.py) | Bedingungen & Schleifen | Generatoren mit yield |
| [3_023_mitschnitt](aufgaben/3_023_mitschnitt.py) | Bedingungen & Schleifen | Generator-Ausdrücke |
| [3_024_stromeffizienz](aufgaben/3_024_stromeffizienz.py) | Bedingungen & Schleifen | Übung: Comprehensions und Generatoren |
| [3_025_stilregeln](aufgaben/3_025_stilregeln.py) | Funktionen | lambda-Ausdrücke |
| [3_026_verteiler](aufgaben/3_026_verteiler.py) | Funktionen | map und filter |
| [3_027_backlog_ordnen](aufgaben/3_027_backlog_ordnen.py) | Funktionen | sorted mit key |
| [3_028_datenpruefung](aufgaben/3_028_datenpruefung.py) | Funktionen | Funktionen als Argumente |
| [3_029_alarmregeln](aufgaben/3_029_alarmregeln.py) | Fehler & Testen | Ausnahmen über Funktionen hinweg |
| [3_030_sensorabfrage](aufgaben/3_030_sensorabfrage.py) | Fehler & Testen | Stammbaum der Ausnahmen |
| [3_031_abfrageversuche](aufgaben/3_031_abfrageversuche.py) | Fehler & Testen | Ausnahme weiterreichen mit `raise` |
| [3_032_passwortregeln](aufgaben/3_032_passwortregeln.py) | Funktionen | Funktionen als Rückgabe |
| [3_033_prozessvarianten](aufgaben/3_033_prozessvarianten.py) | Algorithmen & Rekursion | Memoisierung mit Dictionary |
| [3_034_rackbaum](aufgaben/3_034_rackbaum.py) | Algorithmen & Rekursion | Rekursion auf Listen |
| [3_035_zusatzmodule](aufgaben/3_035_zusatzmodule.py) | Algorithmen & Rekursion | Backtracking: alle Teilmengen |
| [3_036_menuereihenfolge](aufgaben/3_036_menuereihenfolge.py) | Algorithmen & Rekursion | Permutationen rekursiv |
| [3_037_switchport](aufgaben/3_037_switchport.py) | Klassen & Objekte | Klasse mit Methoden |
| [3_038_kundenstamm](aufgaben/3_038_kundenstamm.py) | Datenanalyse | pandas: DataFrame, Spalten |
| [3_039_versionsnummer](aufgaben/3_039_versionsnummer.py) | Klassen & Objekte | __str__ und __eq__ |
| [3_040_sensornetz](aufgaben/3_040_sensornetz.py) | Klassen & Objekte | Objekte in Listen |
| [3_041_sprintauswahl](aufgaben/3_041_sprintauswahl.py) | Datenanalyse | pandas: Masken, sort_values |
| [3_042_ticketarten](aufgaben/3_042_ticketarten.py) | Klassen & Objekte | Vererbung mit super() |
| [3_043_messstellen](aufgaben/3_043_messstellen.py) | Klassen & Objekte | Klassen- und Instanzattribute |
| [3_044_speicherprognose](aufgaben/3_044_speicherprognose.py) | Datenanalyse | pandas: neue Spalten berechnen |
| [3_045_kachelraster](aufgaben/3_045_kachelraster.py) | Programmaufbau | math, statistics, random nutzen |
| [3_046_artikelexport](aufgaben/3_046_artikelexport.py) | Texte, Zahlen & Dateien | Textdatei zeilenweise lesen |
| [3_047_raumsensoren](aufgaben/3_047_raumsensoren.py) | Datenanalyse | pandas: fehlende Werte |
| [3_048_aktionsliste](aufgaben/3_048_aktionsliste.py) | Texte, Zahlen & Dateien | Textdatei schreiben und anhängen |
| [3_049_datenbanklog](aufgaben/3_049_datenbanklog.py) | Texte, Zahlen & Dateien | Übung: Logdatei auswerten |
| [3_050_codeanalyse](aufgaben/3_050_codeanalyse.py) | Texte, Zahlen & Dateien | CSV von Hand, Summen je Spalte |
| [3_051_ticketexport](aufgaben/3_051_ticketexport.py) | Texte, Zahlen & Dateien | csv.reader und DictReader |
| [3_052_alarmbericht](aufgaben/3_052_alarmbericht.py) | Texte, Zahlen & Dateien | csv.writer und DictWriter |
| [3_053_kuehltransport](aufgaben/3_053_kuehltransport.py) | Datenanalyse | pandas: read_csv und astype |
| [3_054_angebotsfrist](aufgaben/3_054_angebotsfrist.py) | Texte, Zahlen & Dateien | Datum zerlegen und prüfen |
| [3_055_scanbericht](aufgaben/3_055_scanbericht.py) | Texte, Zahlen & Dateien | Tausendertrennzeichen und Prozent |
| [3_056_regelklammern](aufgaben/3_056_regelklammern.py) | Datenstrukturen | Stack, Klammern prüfen |
| [3_057_paketpuffer](aufgaben/3_057_paketpuffer.py) | Datenstrukturen | Warteschlange mit deque |
| [3_058_kabelplan](aufgaben/3_058_kabelplan.py) | Algorithmen & Rekursion | Graph als Dictionary, Breitensuche |
| [3_059_lizenzpfad](aufgaben/3_059_lizenzpfad.py) | Algorithmen & Rekursion | Tiefensuche rekursiv, Pfad |
| [3_060_grenzwertpaare](aufgaben/3_060_grenzwertpaare.py) | Algorithmen & Rekursion | Zwei-Zeiger-Technik |
| [3_061_hilfeseite](aufgaben/3_061_hilfeseite.py) | Algorithmen & Rekursion | Sliding Window |
| [3_062_volumenportal](aufgaben/3_062_volumenportal.py) | Algorithmen & Rekursion | Präfixsummen, Bereichssummen |
| [3_063_restkapazitaet](aufgaben/3_063_restkapazitaet.py) | Algorithmen & Rekursion | Paarsumme mit Menge, O(n) |
| [3_064_replikatverzug](aufgaben/3_064_replikatverzug.py) | Algorithmen & Rekursion | Intervalle zusammenführen |
| [3_065_testumgebung](aufgaben/3_065_testumgebung.py) | Algorithmen & Rekursion | Greedy: Termine ohne Überschneidung |
| [3_066_stummschaltung](aufgaben/3_066_stummschaltung.py) | Algorithmen & Rekursion | Greedy: Wechselgeld und Gegenbeispiel |
| [3_067_funkrahmen](aufgaben/3_067_funkrahmen.py) | Algorithmen & Rekursion | Möglichkeiten zählen mit Tabelle |
| [3_068_integrationsplan](aufgaben/3_068_integrationsplan.py) | Algorithmen & Rekursion | Wege im Gitter zählen |
| [3_069_angriffsbericht](aufgaben/3_069_angriffsbericht.py) | Algorithmen & Rekursion | Übung: Algorithmen-Muster |
| [3_070_merkmalstabelle](aufgaben/3_070_merkmalstabelle.py) | Algorithmen & Rekursion | Sieb des Eratosthenes |
| [3_071_serientickets](aufgaben/3_071_serientickets.py) | Algorithmen & Rekursion | ggT und kgV, euklidischer Algorithmus |
| [3_072_blockverteilung](aufgaben/3_072_blockverteilung.py) | Algorithmen & Rekursion | Schnelles Potenzieren modulo m |
| [3_073_kostenrisiko](aufgaben/3_073_kostenrisiko.py) | Algorithmen & Rekursion | Monte-Carlo-Simulation, Pi schätzen |
| [3_074_zufallsbits](aufgaben/3_074_zufallsbits.py) | Algorithmen & Rekursion | Galton-Brett simulieren |
| [3_075_dialogablauf](aufgaben/3_075_dialogablauf.py) | Datenstrukturen | Zustandsautomat mit Dictionary |
| [3_076_meldungstexte](aufgaben/3_076_meldungstexte.py) | Texte, Zahlen & Dateien | Textstatistik: Wörter, Satzlängen |
| [3_077_guthabenbuch](aufgaben/3_077_guthabenbuch.py) | Programmaufbau | Kleines Projekt: Guthabenbuch |

</details>

<details>
<summary><b>Stufe 4 ★★★★☆: Komplexere Zusammenhänge modellieren</b> (89 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [4_001_konto](aufgaben/4_001_konto.py) | Klassen & Objekte | Klassen und Invarianten |
| [4_002_abfahrt](aufgaben/4_002_abfahrt.py) | Klassen & Objekte | `__repr__` und `__str__` |
| [4_003_sitzplatz](aufgaben/4_003_sitzplatz.py) | Klassen & Objekte | `__eq__` und `__hash__` |
| [4_004_engpass](aufgaben/4_004_engpass.py) | Klassen & Objekte | `__lt__` und `total_ordering` |
| [4_005_sprint](aufgaben/4_005_sprint.py) | Klassen & Objekte | `property` mit Setter |
| [4_006_beschaffung](aufgaben/4_006_beschaffung.py) | Klassen & Objekte | Vererbung, `super()` und Polymorphie |
| [4_007_virtuelle_maschinen](aufgaben/4_007_virtuelle_maschinen.py) | Klassen & Objekte | `classmethod` als Konstruktor |
| [4_008_ticketprioritaet](aufgaben/4_008_ticketprioritaet.py) | Klassen & Objekte | `staticmethod` als Hilfsfunktion |
| [4_009_testfaelle](aufgaben/4_009_testfaelle.py) | Klassen & Objekte | Klassenattribute als Zähler und Registry |
| [4_010_messreihen](aufgaben/4_010_messreihen.py) | Klassen & Objekte | Mehrfachvererbung, Mixins und MRO |
| [4_011_sicherungen](aufgaben/4_011_sicherungen.py) | Klassen & Objekte | `abc.ABC` und `@abstractmethod` |
| [4_012_lizenzen](aufgaben/4_012_lizenzen.py) | Klassen & Objekte | `@dataclass` und `field` |
| [4_013_leitungsauslastung](aufgaben/4_013_leitungsauslastung.py) | Datenanalyse | numpy: Achsen und Broadcasting |
| [4_014_patchstand](aufgaben/4_014_patchstand.py) | Klassen & Objekte | dataclass: frozen, order, `__post_init__` |
| [4_015_review_status](aufgaben/4_015_review_status.py) | Klassen & Objekte | `enum.Enum` |
| [4_016_formularpruefung](aufgaben/4_016_formularpruefung.py) | Programmaufbau | Typannotationen, `X | None` |
| [4_017_backlog](aufgaben/4_017_backlog.py) | Programmaufbau | TypeVar, generische Funktionen |
| [4_018_abfrage](aufgaben/4_018_abfrage.py) | Funktionen | *args und **kwargs |
| [4_019_logzeilen](aufgaben/4_019_logzeilen.py) | Funktionen | Entpacken mit *rest |
| [4_020_aktorbefehle](aufgaben/4_020_aktorbefehle.py) | Funktionen | Schlüsselwort-only-Parameter |
| [4_021_prozesskennzahlen](aufgaben/4_021_prozesskennzahlen.py) | Funktionen | Closures und nonlocal |
| [4_022_ticketprotokoll](aufgaben/4_022_ticketprotokoll.py) | Funktionen | Dekoratoren und functools.wraps |
| [4_023_nutzwert](aufgaben/4_023_nutzwert.py) | Funktionen | Dekoratoren mit Argumenten |
| [4_024_pruefsummen](aufgaben/4_024_pruefsummen.py) | Funktionen | Zähl- und Cache-Dekoratoren |
| [4_025_dns_cache](aufgaben/4_025_dns_cache.py) | Funktionen | functools.lru_cache |
| [4_026_vm_platzierung](aufgaben/4_026_vm_platzierung.py) | Algorithmen & Rekursion | Rucksackproblem mit Tabelle |
| [4_027_befehlsvorschlag](aufgaben/4_027_befehlsvorschlag.py) | Algorithmen & Rekursion | Editierdistanz mit Tabelle |
| [4_028_tastenfeld](aufgaben/4_028_tastenfeld.py) | Funktionen | functools.partial |
| [4_029_ticketverlauf](aufgaben/4_029_ticketverlauf.py) | Funktionen | functools.reduce |
| [4_030_pruefagent](aufgaben/4_030_pruefagent.py) | Funktionen | Dekoratoren auf Methoden und Klassen |
| [4_031_anmeldungen](aufgaben/4_031_anmeldungen.py) | Datenanalyse | polars select, filter, with_columns |
| [4_032_gleitender_schnitt](aufgaben/4_032_gleitender_schnitt.py) | Bedingungen & Schleifen | Iterator-Protokoll |
| [4_033_bandrotation](aufgaben/4_033_bandrotation.py) | Bedingungen & Schleifen | Iterable gegen Iterator |
| [4_034_amortisation](aufgaben/4_034_amortisation.py) | Bedingungen & Schleifen | Unendliche Generatoren |
| [4_035_tabreihenfolge](aufgaben/4_035_tabreihenfolge.py) | Bedingungen & Schleifen | __iter__ als Generator |
| [4_036_firewallprotokoll](aufgaben/4_036_firewallprotokoll.py) | Bedingungen & Schleifen | Generator-Pipeline |
| [4_037_bestellabfrage](aufgaben/4_037_bestellabfrage.py) | Datenanalyse | DuckDB: SQL auf DataFrame |
| [4_038_testdatenquelle](aufgaben/4_038_testdatenquelle.py) | Bedingungen & Schleifen | iter() mit Endmarke |
| [4_039_messspruenge](aufgaben/4_039_messspruenge.py) | Bedingungen & Schleifen | Übung: Iteratoren und Generatoren |
| [4_040_moderationsplan](aufgaben/4_040_moderationsplan.py) | Bedingungen & Schleifen | count, cycle, repeat, islice |
| [4_041_co2_bilanz](aufgaben/4_041_co2_bilanz.py) | Datenanalyse | pandas: groupby und agg |
| [4_042_rollenrechte](aufgaben/4_042_rollenrechte.py) | Bedingungen & Schleifen | chain und zip_longest |
| [4_043_trainingsverlauf](aufgaben/4_043_trainingsverlauf.py) | Bedingungen & Schleifen | accumulate: laufende Werte |
| [4_044_wissensdatenbank](aufgaben/4_044_wissensdatenbank.py) | Bedingungen & Schleifen | itertools.groupby |
| [4_045_stoerungscodes](aufgaben/4_045_stoerungscodes.py) | Datenanalyse | pandas: merge |
| [4_046_sensortests](aufgaben/4_046_sensortests.py) | Bedingungen & Schleifen | product, permutations, combinations |
| [4_047_durchsatzmessung](aufgaben/4_047_durchsatzmessung.py) | Bedingungen & Schleifen | takewhile, dropwhile, compress |
| [4_048_rackzaehler](aufgaben/4_048_rackzaehler.py) | Bedingungen & Schleifen | pairwise und tee |
| [4_049_gpu_budget](aufgaben/4_049_gpu_budget.py) | Bedingungen & Schleifen | Übung: itertools |
| [4_050_schwachstellen](aufgaben/4_050_schwachstellen.py) | Datenanalyse | pandas: pivot_table |
| [4_051_trainingslauf](aufgaben/4_051_trainingslauf.py) | Fehler & Testen | with, __enter__ und __exit__ |
| [4_052_wartungsfenster](aufgaben/4_052_wartungsfenster.py) | Fehler & Testen | contextlib.contextmanager |
| [4_053_linkpruefung](aufgaben/4_053_linkpruefung.py) | Nebenläufigkeit | ThreadPoolExecutor.map |
| [4_054_kontrastpruefung](aufgaben/4_054_kontrastpruefung.py) | Datenanalyse | assign, query, Method Chaining |
| [4_055_switchabfrage](aufgaben/4_055_switchabfrage.py) | Fehler & Testen | closing, suppress, Callback |
| [4_056_migrationsfehler](aufgaben/4_056_migrationsfehler.py) | Fehler & Testen | eigene Fehlerklassen, Hierarchie |
| [4_057_abnahme](aufgaben/4_057_abnahme.py) | Datenanalyse | polars group_by und join |
| [4_058_passworttresor](aufgaben/4_058_passworttresor.py) | Fehler & Testen | raise … from, Fehler umwandeln |
| [4_059_barrierefreiheit](aufgaben/4_059_barrierefreiheit.py) | Datenstrukturen | collections.Counter |
| [4_060_wlan_anmeldungen](aufgaben/4_060_wlan_anmeldungen.py) | Datenstrukturen | collections.defaultdict |
| [4_061_stromkreise](aufgaben/4_061_stromkreise.py) | Datenstrukturen | namedtuple und NamedTuple |
| [4_062_velocity](aufgaben/4_062_velocity.py) | Datenstrukturen | deque mit maxlen und rotate |
| [4_063_abfragestau](aufgaben/4_063_abfragestau.py) | Algorithmen & Rekursion | Monotoner Stack |
| [4_064_bauplan](aufgaben/4_064_bauplan.py) | Algorithmen & Rekursion | Topologische Sortierung (Kahn) |
| [4_065_zufriedenheit](aufgaben/4_065_zufriedenheit.py) | Funktionen | itemgetter, attrgetter, methodcaller |
| [4_066_statustafel](aufgaben/4_066_statustafel.py) | Texte, Zahlen & Dateien | format_spec, Ausrichtung, Datum |
| [4_067_funkknoten](aufgaben/4_067_funkknoten.py) | Texte, Zahlen & Dateien | re: Muster suchen, Gruppen |
| [4_068_kontenpruefung](aufgaben/4_068_kontenpruefung.py) | Datenanalyse | pandas: .str-Methoden |
| [4_069_datumsangaben](aufgaben/4_069_datumsangaben.py) | Texte, Zahlen & Dateien | re.sub mit Funktion, finditer |
| [4_070_wartungsplan](aufgaben/4_070_wartungsplan.py) | Texte, Zahlen & Dateien | json: eigene Objekte speichern |
| [4_071_neustartplan](aufgaben/4_071_neustartplan.py) | Texte, Zahlen & Dateien | datetime und timedelta, Fristen |
| [4_072_cloudkosten](aufgaben/4_072_cloudkosten.py) | Datenanalyse | pandas: to_datetime, .dt, resample |
| [4_073_geheimnisscan](aufgaben/4_073_geheimnisscan.py) | Texte, Zahlen & Dateien | pathlib und tempfile |
| [4_074_ereignisschlange](aufgaben/4_074_ereignisschlange.py) | Datenstrukturen | heapq und Prioritätswarteschlange |
| [4_075_linkkosten](aufgaben/4_075_linkkosten.py) | Algorithmen & Rekursion | Dijkstra mit heapq |
| [4_076_zeitleiste](aufgaben/4_076_zeitleiste.py) | Algorithmen & Rekursion | k Listen mit Heap mergen |
| [4_077_qualitaetsstufen](aufgaben/4_077_qualitaetsstufen.py) | Datenstrukturen | bisect: Stufen und Bereiche |
| [4_078_testimages](aufgaben/4_078_testimages.py) | Algorithmen & Rekursion | Binäre Suche auf der Antwort |
| [4_079_symbolleisten](aufgaben/4_079_symbolleisten.py) | Datenstrukturen | copy: flach gegen tief |
| [4_080_fehleranalyse](aufgaben/4_080_fehleranalyse.py) | Funktionen | veränderliche Standardwerte |
| [4_081_schaltregeln](aufgaben/4_081_schaltregeln.py) | Funktionen | späte Bindung in Closures |
| [4_082_aenderungsantraege](aufgaben/4_082_aenderungsantraege.py) | Funktionen | LEGB, global, Klassenkörper |
| [4_083_kategoriebaum](aufgaben/4_083_kategoriebaum.py) | Datenstrukturen | Baum als Klasse, Generator |
| [4_084_prozesskette](aufgaben/4_084_prozesskette.py) | Datenstrukturen | Verkettete Liste mit Iterator |
| [4_085_stoerungsgruppen](aufgaben/4_085_stoerungsgruppen.py) | Datenstrukturen | Union-Find mit Pfadkompression |
| [4_086_alarmzustaendigkeit](aufgaben/4_086_alarmzustaendigkeit.py) | Datenstrukturen | Trie, Präfixsuche, längstes Präfix |
| [4_087_losvergabe](aufgaben/4_087_losvergabe.py) | Algorithmen & Rekursion | Backtracking mit Abschneiden |
| [4_088_sicherheitsaudit](aufgaben/4_088_sicherheitsaudit.py) | Algorithmen & Rekursion | Übung: Graphen |
| [4_089_inventur](aufgaben/4_089_inventur.py) | Programmaufbau | Projekt: Lager mit Inventur |

</details>

<details>
<summary><b>Stufe 5 ★★★★★: Verstehen, wie Python arbeitet</b> (63 Aufgaben)</summary>

| Aufgabe | Thema | Inhalt |
| --- | --- | --- |
| [5_001_deskriptor](aufgaben/5_001_deskriptor.py) | Klassen & Objekte | Deskriptoren |
| [5_002_eigenschaft](aufgaben/5_002_eigenschaft.py) | Klassen & Objekte | `property` nachbauen |
| [5_003_anmeldeprotokoll](aufgaben/5_003_anmeldeprotokoll.py) | Datenanalyse | numpy: Views, Kopien, Fancy Indexing |
| [5_004_nachbarn](aufgaben/5_004_nachbarn.py) | Klassen & Objekte | `__slots__` |
| [5_005_kostenzaehler](aufgaben/5_005_kostenzaehler.py) | Klassen & Objekte | `__getattr__`, Proxy-Objekt |
| [5_006_anmelderisiko](aufgaben/5_006_anmelderisiko.py) | Datenanalyse | pandas: apply gegen vektorisiert |
| [5_007_schnittstelle](aufgaben/5_007_schnittstelle.py) | Klassen & Objekte | `__setattr__`, `__delattr__` |
| [5_008_speicherinventar](aufgaben/5_008_speicherinventar.py) | Klassen & Objekte | `__new__`, Singleton, Unterklasse von int |
| [5_009_testlaufzeiten](aufgaben/5_009_testlaufzeiten.py) | Datenanalyse | DuckDB: Fensterfunktionen |
| [5_010_formularfelder](aufgaben/5_010_formularfelder.py) | Klassen & Objekte | `__init_subclass__` |
| [5_011_pakettypen](aufgaben/5_011_pakettypen.py) | Klassen & Objekte | Klassen mit type() erzeugen |
| [5_012_kundenimport](aufgaben/5_012_kundenimport.py) | Datenanalyse | polars Lazy-Modus |
| [5_013_pruefregeln](aufgaben/5_013_pruefregeln.py) | Klassen & Objekte | Eigene Metaklasse |
| [5_014_sensorstapel](aufgaben/5_014_sensorstapel.py) | Klassen & Objekte | `__class_getitem__` |
| [5_015_soll_ist](aufgaben/5_015_soll_ist.py) | Datenanalyse | pandas, polars und SQL im Vergleich |
| [5_016_benachrichtigung](aufgaben/5_016_benachrichtigung.py) | Klassen & Objekte | typing.Protocol |
| [5_017_lizenzinventar](aufgaben/5_017_lizenzinventar.py) | Klassen & Objekte | virtuelle Unterklassen |
| [5_018_loeschfristen](aufgaben/5_018_loeschfristen.py) | Datenanalyse | Projekt: bereinigen, verknüpfen, auswerten |
| [5_019_datenmenge](aufgaben/5_019_datenmenge.py) | Klassen & Objekte | `__add__`, `__radd__`, `__iadd__` |
| [5_020_betriebsprotokoll](aufgaben/5_020_betriebsprotokoll.py) | Klassen & Objekte | `__call__` und Dekorator-Klassen |
| [5_021_messreihe](aufgaben/5_021_messreihe.py) | Datenstrukturen | Eigene Sequenz mit Slices |
| [5_022_backlog](aufgaben/5_022_backlog.py) | Datenstrukturen | Eigenes Mapping mit MutableMapping |
| [5_023_wahrheitswert](aufgaben/5_023_wahrheitswert.py) | Klassen & Objekte | __bool__ und __len__ |
| [5_024_datenmenge_format](aufgaben/5_024_datenmenge_format.py) | Klassen & Objekte | __format__ mit eigener Spec |
| [5_025_zugriffspruefung](aufgaben/5_025_zugriffspruefung.py) | Fehler & Testen | __exit__ unterdrückt Ausnahmen |
| [5_026_quellensammler](aufgaben/5_026_quellensammler.py) | Fehler & Testen | contextlib.ExitStack |
| [5_027_platzierer](aufgaben/5_027_platzierer.py) | Bedingungen & Schleifen | send: Generator als Koroutine |
| [5_028_budgetkonto](aufgaben/5_028_budgetkonto.py) | Bedingungen & Schleifen | throw, close, finally in Generatoren |
| [5_029_formularassistent](aufgaben/5_029_formularassistent.py) | Bedingungen & Schleifen | yield from, Rückgabewert |
| [5_030_netzscanner](aufgaben/5_030_netzscanner.py) | Bedingungen & Schleifen | Iterable, Iterator, Generator typisieren |
| [5_031_lagertransaktion](aufgaben/5_031_lagertransaktion.py) | Fehler & Testen | contextmanager mit Fehlerpfad |
| [5_032_schnittstellentypen](aufgaben/5_032_schnittstellentypen.py) | Funktionen | functools.singledispatch |
| [5_033_projektplan](aufgaben/5_033_projektplan.py) | Funktionen | functools.cached_property |
| [5_034_alarmdrossel](aufgaben/5_034_alarmdrossel.py) | Funktionen | Methoden-Dekorator, Zustand je Objekt |
| [5_035_modellcache](aufgaben/5_035_modellcache.py) | Datenstrukturen | weakref, WeakValueDictionary |
| [5_036_altgeraete](aufgaben/5_036_altgeraete.py) | Klassen & Objekte | Hash-Vertrag, frozen dataclass |
| [5_037_ansichten](aufgaben/5_037_ansichten.py) | Texte, Zahlen & Dateien | pickle mit __getstate__/__setstate__ |
| [5_038_routingentwurf](aufgaben/5_038_routingentwurf.py) | Datenstrukturen | __copy__ und __deepcopy__ |
| [5_039_teilprojekte](aufgaben/5_039_teilprojekte.py) | Nebenläufigkeit | async def, await, asyncio.run |
| [5_040_datenknoten](aufgaben/5_040_datenknoten.py) | Nebenläufigkeit | asyncio.gather |
| [5_041_testzeitlimit](aufgaben/5_041_testzeitlimit.py) | Nebenläufigkeit | create_task, wait_for, Abbruch |
| [5_042_logsammler](aufgaben/5_042_logsammler.py) | Nebenläufigkeit | asyncio.Queue, Erzeuger, Verbraucher |
| [5_043_luefterschaltung](aufgaben/5_043_luefterschaltung.py) | Nebenläufigkeit | async for, asynchrone Generatoren |
| [5_044_planungspoker](aufgaben/5_044_planungspoker.py) | Nebenläufigkeit | threading: start, join, Ergebnisse |
| [5_045_prozessuebergaenge](aufgaben/5_045_prozessuebergaenge.py) | Nebenläufigkeit | threading: Race Condition, Lock |
| [5_046_ferndiagnose](aufgaben/5_046_ferndiagnose.py) | Nebenläufigkeit | submit, Future, as_completed |
| [5_047_anfragekennung](aufgaben/5_047_anfragekennung.py) | Nebenläufigkeit | contextvars: Kontext ohne globale Variable |
| [5_048_stromvergleich](aufgaben/5_048_stromvergleich.py) | Nebenläufigkeit | Übung: asyncio und Threads |
| [5_049_uploadpruefung](aufgaben/5_049_uploadpruefung.py) | Funktionen | inspect.signature und bind |
| [5_050_typwaechter](aufgaben/5_050_typwaechter.py) | Funktionen | Argumente nach Annotationen prüfen |
| [5_051_funkprofil](aufgaben/5_051_funkprofil.py) | Klassen & Objekte | Deskriptoren in dataclasses |
| [5_052_pruefplugins](aufgaben/5_052_pruefplugins.py) | Programmaufbau | Plugins mit importlib laden |
| [5_053_angebotsexport](aufgaben/5_053_angebotsexport.py) | Texte, Zahlen & Dateien | bytes und bytearray |
| [5_054_abdeckungsdatei](aufgaben/5_054_abdeckungsdatei.py) | Texte, Zahlen & Dateien | struct und memoryview |
| [5_055_rechnungsmaske](aufgaben/5_055_rechnungsmaske.py) | Texte, Zahlen & Dateien | decimal für Geldbeträge |
| [5_056_bandbreitenanteile](aufgaben/5_056_bandbreitenanteile.py) | Texte, Zahlen & Dateien | fractions.Fraction |
| [5_057_gatewayspeicher](aufgaben/5_057_gatewayspeicher.py) | Bedingungen & Schleifen | Generator-Pipelines und Speicher |
| [5_058_backlogwerkzeug](aufgaben/5_058_backlogwerkzeug.py) | Algorithmen & Rekursion | Kosten eingebauter Operationen |
| [5_059_stundenabgleich](aufgaben/5_059_stundenabgleich.py) | Fehler & Testen | Profiling mit cProfile und pstats |
| [5_060_syntaxbaum](aufgaben/5_060_syntaxbaum.py) | Algorithmen & Rekursion | Aufrufstapel, Rekursion als Schleife |
| [5_061_wartungstour](aufgaben/5_061_wartungstour.py) | Algorithmen & Rekursion | Bitmasken-DP, beste Reihenfolge |
| [5_062_messverdichtung](aufgaben/5_062_messverdichtung.py) | Funktionen | Strategie und Beobachter mit Funktionen |
| [5_063_sensorsimulation](aufgaben/5_063_sensorsimulation.py) | Programmaufbau | Ereignisgesteuerte Simulation |

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

Hochgeladen werden die zwei erzeugten Dateien aus `aufgaben/` und `tests/`. Die dritte, `loesungen/2_009_maximum.py`, ist freiwillig (für Stufe 4 und 5 erzeugt `erstelle_aufgaben.py` sie nicht, diese Lösungen bleiben privat): Laden Sie sie mit hoch, wenn andere nach dem Lösen Ihren Weg sehen sollen (die Prüfung beim Hochladen kontrolliert dann, dass sie die Tests besteht). **Ihre Musterdatei behalten Sie** in jedem Fall. Ohne sie muss die Lehrkraft die Musterdatei später nachbauen, um die Aufgabe zu pflegen (siehe [Aufgaben von SuS übernehmen](#aufgaben-von-sus-übernehmen)). Wenn Sie mögen, schicken Sie sie deshalb per E-Mail an [mathematiger.contact@gmail.com](mailto:mathematiger.contact@gmail.com); sie bleibt privat. Mit dem Hochladen stimmen Sie den [Bedingungen für Einreichungen](#bedingungen-für-einreichungen) zu.

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
| `vergleichbar(text)` | Der Text klein geschrieben, ohne Leerzeichen und Zeilenumbrüche (außer zwischen zwei Ziffern) und ohne Satzzeichen, runde Klammern und Gedankenstriche; ganze Zahlen ohne `.0`. Punkte zwischen Ziffern, Minus, Bindestriche sowie eckige und geschweifte Klammern bleiben. Mit `vergleichbar(AUSGABE) == vergleichbar("Die Diagonale ist 100.0 cm lang.")` fällt `100.0cm` statt `100.0 cm` nicht durch. Nehmen Sie es für jede Ausgabe, die die SuS selbst formulieren, außer Leerzeichen oder Groß-/Kleinschreibung sind gerade Thema der Aufgabe. |
| `verwendet("for")` | `True`, wenn `for`, `while`, `if`, `def`, `return`, `class` oder ein Aufruf wie `range` im Code vorkommt, auch Methoden: `verwendet("sort")` findet `liste.sort()`. Kommentare zählen nicht. |
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

Alles in diesem Repo (Code, Aufgaben, Tests, Lösungen, README) steht unter [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de), siehe [LICENSE](LICENSE). Kurz gesagt: Sie dürfen es kopieren, verändern und weitergeben, wenn Sie die Quelle nennen, es nicht kommerziell nutzen und Ihre veränderte Fassung unter derselben Lizenz weitergeben. Verbindlich ist der Lizenztext.

Nutzungen, die über diese Lizenz hinausgehen, etwa eine kommerzielle Nutzung, sind auf Anfrage möglich: [mathematiger.contact@gmail.com](mailto:mathematiger.contact@gmail.com).

### Bedingungen für Einreichungen

Mit einem Pull Request bestätigen Sie, dass Sie die Aufgabe selbst geschrieben haben oder Quelle und Lizenz einer Vorlage im Aufgabentext angeben. Ihr Beitrag steht dann unter CC BY-NC-SA 4.0 (eine Aufgabe nach einer Vorlage unter CC BY-SA unter deren Lizenz). Ihr Urheberrecht bleibt bei Ihnen. Sind Sie unter 18 Jahre alt, brauchen Sie für das Einreichen die Zustimmung Ihrer Eltern.
