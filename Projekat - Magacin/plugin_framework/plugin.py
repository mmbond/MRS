class Plugin:
    """
    .. inheritance-diagram:: plugin_framework.plugin.Plugin plugins.rs_ac_singidunum_prvi.plugin.Main plugins.rs_ac_singidunum_drugi.plugin.Main plugins.rs_ac_singidunum_imenik.plugin.Main

    Ova klasa predstavlja osnovu za svaki konkretan plugin.
    Klasa treba da je apstraktna (spram modela) ali ovde smo je realizovali kao konkretnu
    kako bismo specificirali atribut _spec. U apstraktnim klasama u Pythonu ne postoji inicijalizator
    pa samim tim, atribute na nivou objekta ne mozemo da definisemo drugacije sem kao metode (property),
    tako da je ovo realizovano kao regularna klasa.
    """
    def __init__(self, spec):
        """
        Inicijalizator plugina.

        :param spec: recnik sa kljucevima (str) i vrednostima iz json datoteke
        :type ps: dict
        """
        self._spec = spec

    @property
    def symbolic_name(self):
        """
        Property za dobavljanje simbolickog imena iz metapodataka specifikacije.
        """
        return self._spec.get("symbolic_name", "rs.ac.singidunum.name")

    @symbolic_name.setter
    def symbolic_name(self, value):
        self._spec["symbolic_name"] = value
    
    @property
    def name(self):
        """
        Property za dobavljanje imena iz metapodataka specifikacije.
        """
        return self._spec.get("name", "")

    @name.setter
    def name(self, value):
        self._spec["name"] = value
    
    @property
    def size(self):
        """
        Property za dobavljanje velicine iz metapodataka specifikacije.
        """
        return self._spec.get("size", 0)

    @size.setter
    def size(self, value):
        self._spec["size"] = value
    
    @property
    def category(self):
        """
        Property za dobavljanje kategorije iz metapodataka specifikacije.
        """
        return self._spec.get("category", "cat1")

    @category.setter
    def category(self, value):
        self._spec["category"] = value

    @property
    def version(self):
        """
        Property za dobavljanje verzije iz metapodataka specifikacije.
        """
        return self._spec.get("version", "1.0.0")
    
    @version.setter
    def version(self, value):
        self._spec["version"] = value

    @property
    def enabled(self):
        """
        Property za dobavljanje podatka o dostupnosti iz metapodataka specifikacije.
        """
        return self._spec.get("enabled", False)

    @enabled.setter
    def enabled(self, value):
        self._spec["enabled"] = value

    @property
    def description(self):
        """
        Property za dobavljanje opisa iz metapodataka specifikacije.
        """
        return self._spec.get("description", "")
    
    @description.setter
    def description(self, value):
        self._spec["description"] = value

    def get_widget(self, parent=None):
        """
        Ova metoda treba da vraca konkretni widget koji ce biti smesten u centralni deo aplikacije i njenog 
        glavnog prozora. Može da vrati toolbar, kao i meni, koji će biti smešten u samu aplikaciju.
        Treba da vrati widget, toolbar, menu. Ukoliko su ne postoji dodatni toolbar ili meni, potrebno je za njih
        vratiti None.
        """
        raise NotImplementedError("Ova metoda metoda mora biti realizovana u podklasi!")
    
