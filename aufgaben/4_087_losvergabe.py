"""Aufgabe 4_087 – Losvergabe                                    Stufe 4 ★★★★☆

Ein Landkreis stattet seine Schulen mit neuer IT aus und schreibt den
Auftrag öffentlich aus. Damit auch kleine Firmen mitbieten können, ist
die Ausschreibung in Lose geteilt: Hardware, Verkabelung, Wartung,
Schulung … Jede Firma (ein Anbieter) gibt für die Lose, die sie
übernehmen kann, ein Angebot mit einem Preis in Euro ab. Jedes Los geht
an genau einen Anbieter, der dafür ein Angebot abgegeben hat. Weil
keine Firma zu viel auf einmal stemmen soll, hat jeder Anbieter eine
Kapazität: Er bekommt höchstens so viele Lose. Gesucht ist die
günstigste vollständige Vergabe.

Einfach jedem Los das billigste Angebot zu geben, scheitert oft an den
Kapazitäten. Alle Vergaben durchzuprobieren, dauert bei zwölf Losen mit
je vier Angeboten 4**12, also fast 17 Millionen Fälle. Darum sucht ein
Backtracking, das aussichtslose Zweige früh abschneidet (siehe
Hintergrund). Schreiben Sie:

- `untergrenzen(lose, angebote)` gibt eine Liste mit len(lose) + 1
  Zahlen zurück: An Stelle i steht die Summe der billigsten Preise der
  Lose lose[i:], am Ende also 0. Das ist eine Untergrenze dafür, was die
  restlichen Lose ab i mindestens kosten.
- `sackgasse(lose, ab, angebote, frei)` gibt True zurück, wenn eines der
  Lose lose[ab:] keinen Anbieter mehr hat, der noch freie Kapazität hat
  (frei[anbieter] > 0), sonst False.
- `guenstigste_vergabe(lose, angebote, kapazitaet)` gibt das Paar
  (kosten, vergabe) einer günstigsten vollständigen Vergabe zurück, oder
  None, wenn es keine gibt. vergabe ordnet jedem Los seinen Anbieter zu.
  Gehen Sie die Lose in der Reihenfolge von lose durch, probieren Sie die
  Angebote eines Loses vom billigsten zum teuersten und brechen Sie
  einen Zweig ab, sobald die bisherigen Kosten plus die Untergrenze für
  die restlichen Lose mindestens so groß sind wie die beste bisher
  gefundene Vergabe, oder sobald sackgasse True ergibt. Gibt es mehrere
  günstigste Vergaben, ist jede richtig. angebote und kapazitaet bleiben
  unverändert.

angebote ordnet jedem Los ein Dictionary Anbieter → Preis zu,
kapazitaet jedem Anbieter die Zahl der Lose, die er höchstens bekommt:

    lose = ["Hardware", "Verkabelung", "Wartung", "Schulung"]
    angebote = {
        "Hardware": {"Nordtech": 52000, "Datenwerk": 49000},
        "Verkabelung": {"Nordtech": 18000, "Kabelprofi": 21000, "Datenwerk": 19500},
        "Wartung": {"Datenwerk": 12000, "Servicepunkt": 15000},
        "Schulung": {"Servicepunkt": 4000, "Datenwerk": 3500, "Nordtech": 5000},
    }
    kapazitaet = {"Nordtech": 2, "Datenwerk": 2, "Kabelprofi": 1, "Servicepunkt": 1}

    untergrenzen(lose, angebote)  →  [82500, 33500, 15500, 3500, 0]
    frei = {"Nordtech": 2, "Datenwerk": 0, "Kabelprofi": 1, "Servicepunkt": 0}
    sackgasse(lose, 2, angebote, frei)  →  True    (Wartung findet niemanden mehr)
    sackgasse(lose, 3, angebote, frei)  →  False   (Schulung kann an Nordtech)
    guenstigste_vergabe(lose, angebote, kapazitaet)
        →  (83000, {"Hardware": "Datenwerk", "Verkabelung": "Nordtech",
                    "Wartung": "Datenwerk", "Schulung": "Servicepunkt"})

Jedes Los billig vergeben würde 82500 Euro kosten, aber dann bekäme
Datenwerk drei Lose. Am wenigsten verliert man, wenn die Schulung für
500 Euro mehr an Servicepunkt geht.

Grenzen: 0 ≤ len(lose) ≤ 12, die Lose sind verschiedene, nicht leere
Texte, und jedes steht in angebote. Jedes Los hat 1 bis 4 Angebote, die
Preise sind ganze Zahlen von 1 bis 10**6. Jeder Anbieter aus angebote
steht in kapazitaet, mit einer ganzen Zahl von 0 bis 12 (0 heißt: Der
Anbieter ist ausgeschlossen). frei hat dieselbe Form wie kapazitaet,
und 0 ≤ ab ≤ len(lose). Backtracking bleibt im schlimmsten Fall
exponentiell; die Tests verlangen aber, dass Ihre Suche beide
Abkürzungen nutzt und dadurch bei den Prüffällen nur einen winzigen
Bruchteil der Vergaben ansieht.

Hintergrund: Backtracking kennen Sie aus Aufgabe 3_035 (alle Teilmengen)
und 3_036 (alle Reihenfolgen): Eine rekursive Funktion trifft eine
Entscheidung nach der anderen, ruft sich für den Rest auf und nimmt die
Entscheidung danach wieder zurück, damit die nächste Möglichkeit von
einem sauberen Zustand ausgeht. Hier ist eine Entscheidung „Los i geht
an Anbieter a“; zurücknehmen heißt, frei[a] wieder um 1 zu erhöhen und
das Los aus vergabe zu löschen.

Wer jede Möglichkeit bis zum Ende verfolgt, sieht alle Blätter des
Entscheidungsbaums an, und der wächst mit jedem Los um den Faktor der
Angebote. Schneller wird es nur, wenn man ganze Teilbäume gar nicht erst
betritt. Dafür gibt es zwei Fragen, die man bei jedem Aufruf stellt,
bevor man weitermacht:

1. Kann dieser Zweig noch besser werden als das Beste, was ich schon
   habe? Die restlichen Lose kosten mindestens die Summe ihrer
   billigsten Preise, egal wie die Kapazitäten aussehen. Ist schon
   kosten + untergrenze[i] >= bestes, lohnt sich der Zweig nicht mehr:
   Er kann höchstens gleich gut werden, und eine gleich gute Vergabe
   haben wir schon. Dieses Abschneiden über eine Schranke heißt
   englisch branch and bound („verzweigen und beschränken“).
2. Kann dieser Zweig überhaupt noch fertig werden? Hat ein späteres Los
   nur Anbieter, deren Kapazität schon verbraucht ist, endet jeder Weg
   unter diesem Knoten in einer Sackgasse. Ohne die Prüfung merkt die
   Suche das erst, wenn sie bei diesem Los ankommt, und probiert davor
   alle Möglichkeiten für die Lose dazwischen aus.

Die Untergrenzen rechnet man einmal vorher aus, von hinten nach vorn,
denn untergrenze[i] ist untergrenze[i + 1] plus der billigste Preis von
Los i (min(angebote[los].values())). Damit Abschneiden früh greift,
braucht man schnell eine gute erste Vergabe; darum probiert man die
billigen Angebote zuerst (sorted mit key, Aufgabe 3_027). Das Gerüst
sieht so aus; bestes ist None oder das Paar (kosten, vergabe), und weil
die innere Funktion es neu zuweist, braucht sie nonlocal (Aufgabe 4_021):

    def suche(i, kosten):
        nonlocal bestes
        if bestes is not None and kosten + grenzen[i] >= bestes[0]:
            return                       # wird nicht mehr besser
        if sackgasse(lose, i, angebote, frei):
            return                       # wird nicht mehr fertig
        if i == len(lose):
            bestes = (kosten, dict(vergabe))      # Kopie, vergabe ändert sich weiter
            return
        for anbieter, preis in ...:      # billigste zuerst, nur mit freier Kapazität
            ...                          # entscheiden
            suche(i + 1, kosten + preis)
            ...                          # zurücknehmen

Bei einem Schichtplan, einem Stundenplan oder einem Sudoku funktioniert
es genauso: Schranke für „kann nicht besser werden“, Prüfung für „kann
nicht fertig werden“, und die vielversprechenden Möglichkeiten zuerst.
Wichtig ist das Gleichheitszeichen in >=: Mit > würde die Suche bei
gleich teuren Angeboten jeden gleich guten Zweig bis zum Ende verfolgen.
"""


def untergrenzen(lose, angebote):
    """Gibt für jedes i die Summe der billigsten Preise von lose[i:] zurück, am Ende 0."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def sackgasse(lose, ab, angebote, frei):
    """Gibt True zurück, wenn ein Los aus lose[ab:] keinen Anbieter mit freier Kapazität mehr hat."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


def guenstigste_vergabe(lose, angebote, kapazitaet):
    """Gibt (kosten, vergabe) einer günstigsten vollständigen Vergabe zurück, oder None."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


lose = ["Hardware", "Verkabelung", "Wartung", "Schulung"]
angebote = {
    "Hardware": {"Nordtech": 52000, "Datenwerk": 49000},
    "Verkabelung": {"Nordtech": 18000, "Kabelprofi": 21000, "Datenwerk": 19500},
    "Wartung": {"Datenwerk": 12000, "Servicepunkt": 15000},
    "Schulung": {"Servicepunkt": 4000, "Datenwerk": 3500, "Nordtech": 5000},
}
kapazitaet = {"Nordtech": 2, "Datenwerk": 2, "Kabelprofi": 1, "Servicepunkt": 1}
print(untergrenzen(lose, angebote))
frei = {"Nordtech": 2, "Datenwerk": 0, "Kabelprofi": 1, "Servicepunkt": 0}
print(sackgasse(lose, 2, angebote, frei), sackgasse(lose, 3, angebote, frei))
print(guenstigste_vergabe(lose, angebote, kapazitaet))
