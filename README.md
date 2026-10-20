# Python-Aufgaben

Programmieraufgaben mit automatischer Prüfung. Kein Server, kein Konto nötig (außer Sie wollen über GitHub abgeben). Sie können Aufgaben **lösen** und auch **eigene Aufgaben erstellen** und für alle hochladen.

Die Aufgaben bilden zusammen einen vollständigen Python-Kurs zum Selbststudium in fünf Stufen. Jeden Morgen kommt zu jeder Stufe 1 bis 4 eine neue Aufgabe hinzu, sonntags auch zu Stufe 5. Jede Aufgabe erklärt im Abschnitt „Hintergrund“ das, was neu ist; wer eine Stufe von oben nach unten löst, hat ihren Stoff gesehen.

## Aufgaben

### Stufe 1 ★☆☆☆☆: Erste Schritte mit vorgegebenem Code

| Aufgabe | Thema | Stufe |
|---|---|---|
| 01_hallo_welt | Text ausgeben | ★☆☆☆☆ |
| 02_begruessung | Eingabe und Ausgabe | ★☆☆☆☆ |
| 03_rechteck | Rechnen mit Variablen | ★☆☆☆☆ |
| 07_fahrenheit | Eingabe in Zahl umwandeln | ★☆☆☆☆ |
| 12_fahrzeit | Ganzzahldivision und Rest | ★☆☆☆☆ |

### Stufe 2 ★★☆☆☆: Kontrollfluss, Funktionen, Datenstrukturen

| Aufgabe | Thema | Stufe |
|---|---|---|
| 04_zaehlen | for-Schleife | ★★☆☆☆ |
| 05_verdoppeln | Funktionen mit return | ★★☆☆☆ |
| 06_gerade | if und Funktionen | ★★☆☆☆ |
| 08_countdown | while-Schleife | ★★☆☆☆ |
| 13_wuerfel | Raten und Prüfen | ★★☆☆☆ |

### Stufe 3 ★★★☆☆: Algorithmen, Fehlerbehandlung, Programmorganisation

| Aufgabe | Thema | Stufe |
|---|---|---|
| 09_suche | Lineare Suche | ★★★☆☆ |
| 14_binaere_suche | Binäre Suche | ★★★☆☆ |

### Stufe 4 ★★★★☆: Die Sprache beherrschen

| Aufgabe | Thema | Stufe |
|---|---|---|
| 10_konto | Klassen und Invarianten | ★★★★☆ |
| 15_abfahrt | `__repr__` und `__str__` | ★★★★☆ |

### Stufe 5 ★★★★★: Unter der Haube

| Aufgabe | Thema | Stufe |
|---|---|---|
| 11_deskriptor | Deskriptoren | ★★★★★ |

---

## Aufgaben lösen

### Variante A: Auf dem eigenen Rechner

1. **Einmalig:** Python installieren (python.org, Version 3.9 oder neuer) und diesen Ordner herunterladen (auf GitHub: grüner Knopf **Code → Download ZIP**, dann entpacken).
2. Öffnen Sie eine Datei im Ordner `aufgaben`, z. B. `01_hallo_welt.py`. Oben steht die Aufgabe. Ersetzen Sie die Zeile `pass  # ← Ersetzen Sie diese Zeile durch Ihren Code` durch Ihre Lösung. Speichern!
3. Abgeben und prüfen: Öffnen Sie ein Terminal im Projektordner und tippen Sie

   ```
   python pruefe.py 01
   ```

   (Unter macOS/Linux evtl. `python3`.) Mehrere Aufgaben auf einmal: `python pruefe.py 01 03`. Sie können auch einfach `pruefe.py` in Ihrem Editor starten, dann werden alle Aufgaben geprüft, die Sie schon bearbeitet haben.

So sieht das Ergebnis aus:

```
── 02_begruessung ──
✓ Begrüßung bei Eingabe "Anna"
✗ Begrüßung bei Eingabe "Bo" (nicht fest "Anna" eintippen!)
    Bei Eingabe "Bo" erwartet: "Hallo Bo!" – Ihr Programm: "Hallo Anna!"
→ 1 von 2 Tests bestanden.
```

### Erst selbst testen, dann abgeben

Sie können Ihre Lösung jederzeit selbst prüfen, so oft Sie wollen, bevor Sie sie über GitHub abgeben (Variante B). Dafür brauchen Sie Python und den Projektordner auf Ihrem Rechner (siehe Variante A, Schritt 1).

1. Öffnen Sie ein Terminal im Projektordner (der Ordner, in dem `pruefe.py` liegt):
   - **Windows:** Ordner im Explorer öffnen, oben in die Adresszeile `cmd` tippen, Enter.
   - **macOS:** Rechtsklick auf den Ordner → **Dienste → Neues Terminal beim Ordner**.
   - **Im Editor (z. B. VS Code, Thonny):** Ordner öffnen und dort das Terminal starten.
2. Tippen Sie `python pruefe.py 01` (bzw. `python3 pruefe.py 01`) und drücken Sie Enter. Statt `01` die Nummer Ihrer Aufgabe.
3. Lesen Sie die Meldungen bei ✗, ändern Sie Ihre Datei, **speichern**, und starten Sie den Befehl noch einmal.
4. Erst wenn überall ✓ steht, laden Sie die Datei hoch.

**Tipp:** Verstehen Sie nicht, was Ihr Programm macht? Kopieren Sie Ihren Code in [Python Tutor](https://pythontutor.com/visualize.html#mode=edit) und klicken Sie auf **Visualize Execution**. Dort gehen Sie Zeile für Zeile durch und sehen nach jedem Schritt, welchen Wert jede Variable hat.

Auf GitHub laufen dieselben Tests. Laden Sie neue Aufgaben am besten zusammen mit ihrer Datei aus `tests` herunter, damit Sie auch sie selbst prüfen können.

### Variante B: Über GitHub (im Browser)

1. **Einmalig:** GitHub-Konto anlegen. Auf der Seite dieses Repos **Use this template → Create a new repository**, Sichtbarkeit **Private** wählen. Das ist jetzt Ihr eigenes Repo.
2. Aufgabe bearbeiten, zwei Wege:
   - **Direkt im Browser:** In Ihrem Repo `aufgaben/01_hallo_welt.py` öffnen → Stift-Symbol → Lösung schreiben → **Commit changes**.
   - **Datei hochladen:** Lokal bearbeiten und [selbst testen](#erst-selbst-testen-dann-abgeben), dann in Ihrem Repo den Ordner `aufgaben` öffnen → **Add file → Upload files** → Datei hineinziehen → **Commit changes**. Der Dateiname muss gleich bleiben.
3. Ergebnis ansehen: Reiter **Actions** → oberster Eintrag → unten bei **Ergebnis** steht die Auswertung. Grüner Haken = alles bestanden, rotes ✗ = noch etwas zu tun.

**Neue Aufgaben** kommen in Ihrem Repo nicht automatisch an. Laden Sie die neue Datei aus dem Ordner `aufgaben` des Original-Repos herunter und laden Sie sie in Ihren Ordner `aufgaben` hoch. Die Tests dafür holt GitHub automatisch.

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

Übernehmen Sie eine Aufgabe, schreiben Sie die Quelle und die Lizenz in den Aufgabentext, z. B. `Nach inf-schule.de, CC BY-SA 4.0`. Das verlangen diese Lizenzen. Bei Seiten ohne freie Lizenz schreiben Sie die Aufgabe nicht ab, sondern denken sich mit eigenen Worten eine ähnliche aus.

### 1. Musterdatei schreiben

Legen Sie im Projektordner einen Ordner `eigene_aufgaben` an und darin eine **Musterdatei**, z. B. `07_maximum.py`. Nehmen Sie als Nummer die nächste freie aus den Tabellen oben. In die Musterdatei kommt alles: Aufgabenstellung, Ihre Lösung und Tests.

```python
"""Aufgabe 07 – Maximum                                       Stufe 2 ★★☆☆☆

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

### 2. Aufgabe erzeugen

```
python erstelle_aufgaben.py
```

Das erzeugt `aufgaben/07_maximum.py` (die Vorlage zum Lösen) und `tests/07_maximum.py`. Dabei wird automatisch geprüft, dass **Ihre Lösung alle Tests besteht** und **die leere Vorlage nicht**:

```
✓ 07_maximum.py (2 Tests)
```

Steht dort ein ✗, steht darunter, was nicht stimmt. Ändern Sie die Musterdatei und starten Sie das Skript noch einmal. Die Dateien in `aufgaben/` und `tests/` nie von Hand ändern, sie werden jedes Mal neu erzeugt.

### 3. Tests mit falschen Lösungen ausprobieren

Das ✓ zeigt nur, dass Ihre Lösung besteht und die leere Vorlage nicht. Ob Ihre Tests auch **typische Fehler** finden, prüfen Sie selbst: Schreiben Sie in `aufgaben/07_maximum.py` eine falsche Lösung, so wie sie beim Lösen entstehen könnte, und prüfen Sie sie wie eine normale Aufgabe:

```
python pruefe.py 07
```

Gute falsche Lösungen sind z. B. ein fest hingeschriebenes Ergebnis (`return 5`), vertauschte Fälle oder eine vergessene Kleinigkeit wie das `!` am Satzende. Jede davon sollte mindestens ein ✗ bekommen, und die Meldung darunter sollte helfen, den Fehler zu finden. Probieren Sie auch eine **andere richtige** Lösung aus: Sie muss alle Tests bestehen. Wenn nicht, sind Ihre Tests zu streng.

Findet ein Test einen Fehler nicht, ergänzen Sie Tests in der Musterdatei. Zum Schluss `python erstelle_aufgaben.py` noch einmal starten. Das stellt auch die Vorlage in `aufgaben/` wieder her.

**Für Fortgeschrittene:** Wollen Sie mehrere falsche Lösungen aufheben, ohne `aufgaben/` zu ändern, legen Sie sie in eigene Ordner. Der Dateiname muss derselbe sein wie in `aufgaben/`, sonst findet `pruefe.py` die passenden Tests nicht. Zwei falsche Lösungen zur selben Aufgabe brauchen deshalb zwei Ordner. Benennen Sie die Ordner nach dem Fehler, den sie enthalten, z. B. `varianten/fest/07_maximum.py` (Ergebnis fest hingeschrieben) und `varianten/vertauscht/07_maximum.py`.

Alle Aufgaben in einem Ordner prüfen Sie mit

```
python pruefe.py --aufgaben varianten/fest
```

Einzelne Aufgaben prüfen Sie wieder über den Anfang des Namens, z. B. alle, die mit `07` beginnen:

```
python pruefe.py 07 --aufgaben varianten/fest
```

Für den Anfang ist es einfacher, die Datei in `aufgaben/` direkt zu bearbeiten wie oben beschrieben.

### 4. Für alle hochladen

Hochgeladen werden nur die zwei erzeugten Dateien. **Ihre Musterdatei behalten Sie**, sonst steht die Lösung im Netz. Ich freue mich gerne über die Musterlösung für meine Notizen, bspw. durch Teilen Ihrer privaten Repos.

1. Auf der Seite dieses Repos oben rechts **Fork → Create fork**. Das ist eine Kopie, in die Sie schreiben dürfen.
2. In Ihrem Fork den Ordner `aufgaben` öffnen → **Add file → Upload files** → `aufgaben/07_maximum.py` hineinziehen → **Commit changes**.
3. Dasselbe im Ordner `tests` mit `tests/07_maximum.py`.
4. Optional: `README.md` öffnen → Stift-Symbol → Ihre Aufgabe in die Tabelle eintragen → **Commit changes**.
5. Oben **Contribute → Open pull request** → kurz beschreiben, worum es geht → **Create pull request**.

Die Lehrkraft schaut drüber und übernimmt die Aufgabe. Danach können alle sie lösen.

### Die Marker

| Marker | Wirkung |
|---|---|
| `### BEGIN SOLUTION` … `### END SOLUTION` | Lösung. In der Vorlage wird daraus `pass  # ← Ersetzen Sie diese Zeile durch Ihren Code` (mit gleicher Einrückung). |
| `### BEGIN TESTS` … `### END TESTS` | Tests. Kommen nur in die Testdatei. |

Alles außerhalb der Marker steht in der Vorlage, also Aufgabentext, vorgegebener Code und Funktionsköpfe. `### BEGIN HIDDEN TESTS` wird wie `TESTS` behandelt: Ohne Server lassen sich Tests nicht wirklich verstecken.

### Tests schreiben

Tests sind normale `assert`-Zeilen, wie in nbgrader. Jedes `assert` (oder jeder Block, der eines enthält, z. B. eine `for`-Schleife) zählt als ein Test.

- **Name eines Tests:** der Kommentar direkt über dem Test (oder über der Vorbereitungszeile davor). Ohne Kommentar wird die Bedingung angezeigt.
- **Meldung bei Fehlschlag:** der Text nach dem Komma im `assert`. Schreiben Sie hier, was beim Lösen geändert werden soll.
- Die Tests laufen *nach* dem Programm, im selben Namensraum: Alle Variablen und Funktionen der Lösung sind verfügbar.
- Testen Sie mit mehreren Werten, damit niemand das Ergebnis einfach fest hinschreiben kann.
- Die Tests haben hilfreiche Fehlerausgaben, was falsch ist, und evtl. Tipps für den nächsten Versuch.

Zusätzlich gibt es in den Tests:

| Name | Bedeutung |
|---|---|
| `AUSGABE` | Alles, was das Programm mit `print` ausgegeben hat. Leerzeichen am Zeilenende und Leerzeilen am Schluss sind schon entfernt. Der Text von `input("…")` gehört nicht dazu. |
| `EINGABEN = ["Anna"]` | In den Tests setzen: Diese Werte bekommt `input()` beim ersten Lauf. |
| `starte("Bo")` | Startet das Programm neu mit anderen Eingaben und gibt dessen Ausgabe zurück. Gut gegen fest eingetippte Ergebnisse. |
| `verwendet("for")` | `True`, wenn `for`, `while`, `if`, `def`, `return`, `class` oder ein Aufruf wie `range` im Code vorkommt. Kommentare zählen nicht. |

Endlosschleifen werden nach 5 Sekunden abgebrochen (`ZEITLIMIT_SEKUNDEN` in `pruefe.py`).

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

Vorher prüft GitHub jeden Pull Request automatisch (`.github/workflows/einreichung.yml`): Geändert sind nur `aufgaben/`, `tests/` und `README.md`, Vorlage und Tests gehören zusammen, die leere Vorlage besteht die Tests nicht, und es steht nichts darin wie `import`, `open` oder `eval`, womit Code auf den Rechnern der SuS Schaden anrichten könnte. Das Ergebnis steht als ✓ oder ✗ am Pull Request, Einzelheiten unter **Details**.

- Bei der ersten Einreichung einer Person fragt GitHub, ob der Workflow laufen darf: **Approve and run**.
- Ein ✓ ersetzt nicht das Ansehen. Ändert ein Pull Request etwas unter `.github/`, nicht übernehmen: Dann ist auch das ✓ nicht verlässlich.


### Gut zu wissen

- Die Tests liegen offen im Repo. Wer will, kann sie lesen. Für Selbstkontrolle ist das in Ordnung.
- `eigene_aufgaben/` steht in `.gitignore`, damit Musterlösungen von SuS nicht versehentlich mit `git` hochgeladen werden.
- Löschen Sie eine Musterdatei, löschen Sie auch die zugehörigen Dateien in `aufgaben/` und `tests/` von Hand.

---

## Lizenz

© [mathematiger](https://github.com/mathematiger) und alle, die Aufgaben beigetragen haben. Alles in diesem Repo (Code, Aufgaben, Tests, README) steht unter [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.de), siehe `LICENSE`. Sie dürfen es kopieren, verändern und weitergeben, auch kommerziell, wenn Sie die Quelle nennen und Ihre veränderte Fassung unter derselben Lizenz weitergeben.

Mit einem Pull Request stellen Sie Ihre Aufgabe ebenfalls unter CC BY-SA 4.0. Stammt eine Aufgabe aus einer anderen Quelle, steht die Quelle im Aufgabentext.
