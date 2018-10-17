from plugin import Plugin
from concrete_plugin import ConcretePlugin
from plugin_service import PluginService


plugin1 = ConcretePlugin("Plugin 1", 8.4, "Category 1", "1.0.0", True, "My first plugin")
plugin2 = ConcretePlugin("Plugin 2", 4.4, "Category 1", "1.0.0", False, "My second plugin")
plugins = PluginService()

plugins.install(plugin1)
plugins.install(plugin2)

plugins.set_enabled(plugin1, False)

plugin1.hello()
plugin2.hello()
