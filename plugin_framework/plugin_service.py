class PluginService:
    def __init__(self):
        self._plugins = list()

    def set_enabled(self, plugin, value):
        if plugin in self._plugins:
            plugin.enabled = value
            return True
        return False

    def install(self, plugin):
        self._plugins.append(plugin)

    def uninstall(self, plugin):
        self._plugins.remove(plugin)