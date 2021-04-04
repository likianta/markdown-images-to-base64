import os
from functools import wraps
from os.path import exists, isfile

from lk_logger import lk
from lk_qtquick_scaffold import pyhandler


def main():
    my_handle = MyHandler()
    pyhandler.register_pyfunc(my_handle.calc_target)
    pyhandler.register_pyfunc(my_handle.target_file_exists)
    pyhandler.register_pyfunc(my_handle.open_target)
    pyhandler.register_pyfunc(my_handle.run)
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
        
        @wraps(func)
        def decor1(self, file):
            from env import SYSTEM
            if SYSTEM == 1:  # macOS
                if file != '' and file[0] != '/':
                    file = '/' + file  # e.g. 'Users/A/B/C' -> '/Users/A/B/C'
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
    
    @_file_binding(io='ofile')
    def target_file_exists(self, ofile: str):
        """
        FIXME:
            关于不同操作系统之间的困扰:
                对于 Windows 系统, QML 的文件对话框返回的是:
                    file:///d:/A/B/C
                我们去掉 'file:///', 就能判断文件已存在;
                对于 macOS 系统, QML 的文件对话框返回的是:
                    file:///Users/A/B/C
                如果去掉 'file:///', macOS 判断 'Users/A/B/C' 是不存在的,
                而 '/Users/A/B/C' 才是存在的.
                换句话说, 前者要求我们去掉 'file:///', 后者要求我们去掉 'file://', 该怎么
                统一操作呢?
        """
        lk.loga(ofile)
        return exists(ofile) and isfile(ofile)
    
    @_file_binding(io='ofile')
    def open_target(self, ofile):
        from env import SYSTEM
        
        if SYSTEM == 0:
            os.startfile(ofile)
        else:
            # A (not work for me)
            # https://blog.csdn.net/bmw601055/article/details/77619271
            # import subprocess
            # subprocess.call(['open', ofile])
            
            # B (not work for me)
            # https://www.runoob.com/python/os-open.html
            # os.open('/' + ofile, os.O_RDONLY)
            
            # C (worked)
            # https://apple.stackexchange.com/questions/321043/open-html-file
            # -with-google-chrome-using-command-line
            os.popen(f'open "{ofile}"')
    
    @_file_binding(io='ifile')
    def run(self, ifile):
        from converter import md_2_html
        ofile = md_2_html.main(ifile)
        return ofile
