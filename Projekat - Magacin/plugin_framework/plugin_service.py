import os
import json
import importlib

class PluginService:
    """
    Klasa koja manipulise nad prosirenjima (pluginovima) u prosirivom okviru.
    """
    def __init__(self):
        """
        Inicijalizator servisne klase za pluginove.
        """
        self._plugins = list()

    def get_by_symbolic_name(self, symbolic_name):
        """
        Vraca plugin koji ima naziv symbolic_name. Ukoliko se podesi da vise pluginova ima isti symbolic_name, vraca
        se samo prvi.

        :param symbolic_name: naziv spram kog pretrazujemo sve dostupne pluginove.
        :type symbolic_name: str
        :returns: Plugin -- pronadjeni plugin.
        :raises: IndexError -- ukoliko ne postoji ni jedan plugin koji je zadovoljio filter.
        """
        return list(filter(lambda x: x.symbolic_name == symbolic_name, self._plugins))[0]

    def set_enabled(self, plugin, value):
        """
        Postavlja status aktivnosti plugina na zadatu vrednost.

        :param plugin: instanca plugina kojem menjamo status.
        :type plugin: Plugin
        :param value: nova vrednost statusa
        :type value: bool
        :returns: bool -- podatak o uspesnosti promene.
        """
        if plugin in self._plugins:
            plugin.enabled = value
            return True
        return False

    def install(self, plugin):
        """
        Dodaje plugin u instalirane. Isti plugin se ne moze dodati dva puta.

        :param plugin: instanca plugina kojeg dodajemo.
        :type plugin: Plugin
        :returns: bool -- podatak o uspesnosti dodavanja.
        """
        if plugin not in self._plugins:
            self._plugins.append(plugin)
            return True
        return False

    def uninstall(self, plugin):
        """
        Brise plugin u instalirane. Isti plugin se ne moze brisati dva puta.

        :param plugin: instanca plugina kojeg brisemo.
        :type plugin: Plugin
        :returns: bool -- podatak o uspesnosti brisanja.
        """
        if plugin in self._plugins:
            self._plugins.remove(plugin)
            return True
        return False

    @property
    def plugins(self):
        return self._plugins

    def load_plugins(self, plugins_path="plugins"):
        """
        Ucitava sve pluginove spram zadate lokacije. Nakon ucitavanja svih modula i pronalaska njihovih specifikacija,
        plugin se instalira u sistem.

        :param plugins_path: putanja na kojoj se nalaze plugin paketi.
        :type plugins_path: str
        """
        for d in os.listdir(plugins_path):
            dir_path = os.path.join(plugins_path, d)
            if os.path.exists(os.path.join(dir_path, "__init__.py")):
                with open(os.path.join(dir_path, "spec.json"), "r") as fp:
                    spec = json.load(fp)
                    print(os.path.join(dir_path, "plugin"))
                    modul = importlib.import_module(os.path.join(dir_path, "plugin").replace(os.sep, "."))
                    obj = modul.Main(spec)
                    self.install(obj)