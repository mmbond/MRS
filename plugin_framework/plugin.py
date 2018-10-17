class Plugin:
    def __init__(self, name, size, category, version, enabled, description):
        self._name = name
        self._size = size
        self._category = category
        self._version = version
        self._enabled = enabled
        self._description = description
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
    
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, value):
        self._version = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
    
