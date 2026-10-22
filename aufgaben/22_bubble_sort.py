"""Aufgabe 22 – Löschfristen                                     Stufe 3 ★★★☆☆

Nach dem Datenschutzrecht dürfen personenbezogene Daten nur so lange
gespeichert werden, wie sie gebraucht werden. Für jeden Datenbestand einer
Firma (Bewerbungen, Rechnungen, Videoaufnahmen …) steht deshalb fest, in wie
vielen Tagen er gelöscht werden muss. Die Datenschutzbeauftragte möchte die
Restlaufzeiten aufsteigend sortiert sehen, die dringendste zuerst.
Vervollständigen Sie die Funktion `sortiere`, die die Liste mit Bubble Sort
sortiert. Die Funktion verändert die übergebene Liste selbst und gibt nichts
zurück.

    fristen = [30, 7, 365, 90]
    sortiere(fristen)
    print(fristen)  →  [7, 30, 90, 365]

Benutzen Sie dafür Schleifen und nicht sorted(...) oder liste.sort(). Meist
ist die Liste schon fast sortiert, weil sich seit gestern nur wenig geändert
hat. Deshalb soll Ihre Funktion aufhören, sobald ein Durchgang nichts mehr
tauschen musste.

Hintergrund: Bubble Sort geht die Liste von vorn nach hinten durch und
vergleicht immer zwei Nachbarn. Steht der größere vorn, werden die beiden
getauscht. Nach einem solchen Durchgang ist das größte Element ganz nach
hinten „aufgestiegen“ wie eine Blase im Wasser; der nächste Durchgang bringt
das zweitgrößte an die vorletzte Stelle und so weiter:

    [30, 7, 365, 90]   Durchgang 1: 30↔7 tauschen, 30 und 365 bleiben, 365↔90 tauschen
    [7, 30, 90, 365]   Durchgang 2: kein Tausch nötig → fertig

Ohne Abbruch braucht Bubble Sort immer len(liste) - 1 Durchgänge mit jeweils
bis zu n Vergleichen, also O(n²), auch wenn die Liste längst sortiert ist.
Merkt man sich aber in einer Variablen, ob im aktuellen Durchgang getauscht
wurde, kann man aufhören, sobald ein Durchgang ohne Tausch bleibt: Dann
stehen alle Nachbarn richtig, also ist die ganze Liste sortiert. Für eine
schon sortierte Liste reicht so ein einziger Durchgang, O(n):

    getauscht = True
    while getauscht:
        getauscht = False
        for i in range(len(liste) - 1):
            ...  # Nachbarn liste[i] und liste[i + 1] vergleichen, ggf. tauschen
                 # und getauscht = True setzen

Tipp: Tauschen Sie nur, wenn der linke Nachbar echt größer ist (>). Mit >=
würden zwei gleiche Fristen in jedem Durchgang die Plätze wechseln, und die
Schleife hörte nie auf.
"""


def sortiere(liste):
    """Sortiert liste an Ort und Stelle aufsteigend mit Bubble Sort und Abbruch."""
    pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


fristen = [30, 7, 365, 90]
sortiere(fristen)
print(fristen)
