from plugin import Plugin

class ConcretePlugin(Plugin):
    def __init__(self, name, size, category, version, enabled, description):
        super().__init__(name, size, category, version, enabled, description)

    def hello(self):
        print("Plugin Name:",self.name,
        "\nPlugin Size:",self.size,
        "\nPlugin Category:",self.category,
        "\nPlugin Version:",self.version,
        "\nPlugin Enabled:",self.enabled,
        "\nPlugin Description:",self.description,end="\n\n")
