from plugin_framework.plugin_service import PluginService

import sys
from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from gui.main_window import MainWindow
                                     
if __name__ == "__main__":
    # instanciramo plugin servis
    plugin_service = PluginService() 
    # ucitamo sve plugin-ove sa putanje plugins/
    plugin_service.load_plugins() 

    # kreiramo Qt aplikaciju
    app = QtWidgets.QApplication(sys.argv)
    # napravimo glavni prozor
    main_window = MainWindow(plugin_service)
    # prikazemo glavni prozor
    main_window.show()
    # izvrsimo Qt aplikaciju. Nakon sto se zavrsi Qt aplikacija, zavrsava se i rad interpretera
    sys.exit(app.exec_())
