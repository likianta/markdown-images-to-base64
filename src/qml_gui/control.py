import os
from os.path import exists

from lk_qtquick_scaffold import pyhandler


def main():
    my_handle = MyHandler()
    pyhandler.register_pyfunc(my_handle.calc_target)
    return my_handle


def _file_binding(io: str):
    """
    References:
        https://stackoverflow.com/questions/11731136/class-method-decorator-with
        -self-arguments
    Args:
        io ('ifile'|'ofile'): Declare it is 'ifile' or 'ofile'
    """
    
    def decor0(func):
        """
        Args:
            func: class methods of MyHandler, see decorator usages at
                `MyHandler.calc_target` and `MyHandler.open_target`.
        """
        
        def decor1(self, file):
            if io == 'ifile':
                self.ifile = file
            else:
                self.ofile = file
            return func(self, file)
        
        return decor1
    
    return decor0


# noinspection PyMethodMayBeStatic
class MyHandler:
    
    def __init__(self):
        self.ifile = ''
        self.ofile = ''
    
    @_file_binding(io='ifile')
    def calc_target(self, ifile: str):
        if ifile.endswith('.md'):
            self.ofile = ifile[:-3] + '.html'
        elif ifile.endswith('.html'):
            self.ofile = ifile[:-5] + '.base64.html'
        else:
            self.ofile = ''
        return self.ofile
    
    def target_file_exists(self):
        return exists(self.ofile)
    
    @_file_binding(io='ofile')
    def open_target(self, ofile):
        os.startfile(ofile)
    
    def run(self):
        print('src/qml_gui/control.py:57', 'This method is not ready...')
