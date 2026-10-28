"""Aufgabe 4_006 – Virtuelle Maschinen                          Stufe 4 ★★★★☆

Auf den Servern eines Rechenzentrums laufen viele virtuelle Maschinen (VMs):
Rechner, die nur als Software existieren und sich die echte Hardware teilen.
Jede VM bekommt einen Namen, eine Zahl virtueller Prozessorkerne (vCPUs) und
Arbeitsspeicher in MiB. Die Klasse `VM` ist mit __init__ und __repr__ schon
fertig. VMs entstehen aber selten durch einen Aufruf wie VM("web01", 4, 8192):
Entweder kommen sie aus der Exportdatei der Virtualisierungssoftware, eine
Zeile pro VM, oder sie werden nach einer Größe aus dem Katalog bestellt.
Vervollständigen Sie zwei alternative Konstruktoren:

- `VM.aus_zeile(zeile)` erzeugt eine VM aus einer Zeile der Form
  "web01;4;8192". Leerzeichen um die Felder herum werden ignoriert. Hat die
  Zeile nicht genau drei Felder, löst die Methode einen ValueError aus.
- `VM.aus_katalog(name, groesse)` erzeugt eine VM mit den Werten aus dem
  Klassenattribut KATALOG, z. B. hat Größe "M" 2 vCPUs und 4096 MiB. Eine
  unbekannte Größe löst einen ValueError aus.

Beide geben ein neues Objekt der Klasse zurück, auf der sie aufgerufen werden;
auch für die Unterklasse `GpuVM` (unten vorgegeben) muss das klappen.

    VM.aus_zeile("web01;4;8192")       →  VM('web01', 4, 8192)
    VM.aus_zeile(" db02 ; 8 ; 32768")  →  VM('db02', 8, 32768)
    VM.aus_zeile("web01;4")            →  ValueError
    VM.aus_katalog("test07", "M")      →  VM('test07', 2, 4096)
    VM.aus_katalog("test07", "XXL")    →  ValueError
    GpuVM.aus_zeile("ki01;16;65536")   →  GpuVM('ki01', 16, 65536)

Grenzen: `zeile` ist ein Text mit beliebig vielen Feldern, getrennt durch ";".
Hat sie genau drei Felder, ist das erste ein nicht leerer Name aus Buchstaben,
Ziffern und "-", das zweite und dritte sind ganze Zahlen mit
0 ≤ vcpus ≤ 1024 und 0 ≤ ram_mib ≤ 4 194 304; um jedes Feld dürfen
Leerzeichen stehen. Eine 0 lehnt schon __init__ mit einem ValueError ab.
`groesse` ist ein beliebiger Text, `name` in aus_katalog ein nicht leerer
Text.

Hintergrund: __init__ legt fest, mit welchen Werten ein Objekt entsteht.
Oft liegen die Daten aber in einer anderen Form vor, etwa als Text. Statt
überall erst den Text zu zerlegen, gibt man der Klasse weitere „Konstruktoren“:
Methoden, die die Daten umwandeln und dann das Objekt erzeugen. Weil es noch
kein Objekt gibt, wenn man sie aufruft, ruft man sie auf der Klasse auf, und
dafür gibt es den Dekorator @classmethod. Eine solche Klassenmethode bekommt
als ersten Parameter nicht das Objekt self, sondern die Klasse selbst,
üblicherweise cls genannt:

    class Punkt:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        @classmethod
        def aus_text(cls, text):        # "3,4"
            x, y = text.split(",")
            return cls(int(x), int(y))  # wie Punkt(3, 4)

    p = Punkt.aus_text("3,4")           # cls ist hier Punkt

cls(...) ruft __init__ auf, also gelten alle Prüfungen von __init__ auch
für Objekte aus aus_text. Man könnte statt cls(...) auch Punkt(...) schreiben;
dann bekäme aber eine Unterklasse wie class Punkt3D(Punkt) beim Aufruf
Punkt3D.aus_text("3,4") ein Punkt-Objekt statt eines Punkt3D-Objekts. Mit cls
entsteht immer ein Objekt der Klasse, auf der man die Methode aufruft. Auch
Klassenattribute wie KATALOG erreicht man über cls, etwa cls.KATALOG.
Bekannte Beispiele aus der Standardbibliothek sind dict.fromkeys(...) und
datetime.fromisoformat(...).

Tipp: zeile.split(";") zerlegt die Zeile, text.strip() entfernt Leerzeichen
am Anfang und am Ende, int(...) wandelt die Zahlen um.
"""


class VM:
    """Eine virtuelle Maschine mit Name, vCPUs und Arbeitsspeicher in MiB."""

    KATALOG = {"S": (1, 2048), "M": (2, 4096), "L": (4, 8192), "XL": (8, 16384)}

    def __init__(self, name, vcpus, ram_mib):
        """Speichert die Werte; vCPUs und Arbeitsspeicher müssen positiv sein."""
        if vcpus <= 0 or ram_mib <= 0:
            raise ValueError("vCPUs und Arbeitsspeicher müssen positiv sein.")
        self.name = name
        self.vcpus = vcpus
        self.ram_mib = ram_mib

    def __repr__(self):
        """Liefert z. B. VM('web01', 4, 8192), bei Unterklassen mit deren Namen."""
        return f"{type(self).__name__}({self.name!r}, {self.vcpus}, {self.ram_mib})"

    @classmethod
    def aus_zeile(cls, zeile):
        """Erzeugt eine VM aus einer Zeile wie "web01;4;8192"."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code

    @classmethod
    def aus_katalog(cls, name, groesse):
        """Erzeugt eine VM der Größe groesse aus dem KATALOG."""
        pass  # ← Ersetzen Sie diese Zeile durch Ihren Code


class GpuVM(VM):
    """Eine VM mit Grafikprozessor, z. B. für KI-Anwendungen; im Katalog gibt es mehr Speicher."""

    KATALOG = {"M": (4, 16384), "L": (8, 65536)}


print(VM.aus_zeile("web01;4;8192"))
print(VM.aus_katalog("test07", "M"))
print(GpuVM.aus_zeile("ki01;16;65536"))
