import enaml
from enaml.qt.qt_application import QtApplication


def launch_enaml():
    with enaml.imports():
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from enaml_gui.view import Main
    
    app = QtApplication()
    view = Main()
    view.show()
    app.start()


def launch_qml():
    pass


if __name__ == '__main__':
    launch_enaml()
