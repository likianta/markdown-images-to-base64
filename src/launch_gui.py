def launch_enaml():
    import enaml
    from enaml.qt.qt_application import QtApplication
    
    with enaml.imports():
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from enaml_gui.view import Main
    
    app = QtApplication()
    view = Main()
    view.show()
    app.start()


def launch_qml():
    pass


def debug():
    from qml_gui import control
    control.main()
    
    # noinspection PyPackageRequirements
    from lk_qtquick_scaffold.debugger import HotReloader
    reloader = HotReloader('./qml_gui/view.qml')
    reloader.launch()


if __name__ == '__main__':
    # from lk_utils.easy_launcher import launch
    # launch(launch_enaml)
    
    debug()
