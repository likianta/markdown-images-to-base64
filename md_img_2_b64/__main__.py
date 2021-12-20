"""
requirements:
    pip install fire

usage in cmd:
    python -m md_img_2_b64 --help
    python -m md_img_2_b64 md2md
    python -m md_img_2_b64 md2html
    python -m md_img_2_b64 html2html
"""
import os.path

import md_img_2_b64


def _auto_get_output_path(func):
    def wrapper(*args, **kwargs):
        if 'file_o' in kwargs:
            file_o = kwargs['file_o']
        else:
            file_o = args[1]
        if not file_o:  # file_o is None or file_o == ''
            file_i = kwargs.get('file_i') or args[0]
            ext_i = os.path.splitext(file_i)[1]
            ext_o = {
                'md2md'    : '.base64.md',
                'md2html'  : '.base64.html',
                'html2html': '.base64.html',
            }[func.__name__]
            file_o = file_i.removesuffix(ext_i) + ext_o
        
        if 'file_o' in kwargs:
            kwargs['file_o'] = file_o
        else:
            args = (args[0], file_o)
        
        file_o = func(*args, **kwargs)
        print('output:', file_o)
        return file_o
    
    return wrapper


class Cli:
    """
    the method names don't inclulde underlines, this is friendly for user input.
    """
    
    @_auto_get_output_path
    def md2md(self, file_i, file_o=''):
        return md_img_2_b64.md_2_md(file_i, file_o)
    
    @_auto_get_output_path
    def md2html(self, file_i, file_o=''):
        return md_img_2_b64.md_2_html(file_i, file_o)
    
    @_auto_get_output_path
    def html2html(self, file_i, file_o=''):
        return md_img_2_b64.html_2_html(file_i, file_o)


if __name__ == '__main__':
    from fire import Fire
    
    Fire(Cli())
