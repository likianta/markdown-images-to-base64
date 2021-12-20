"""
To run in CMD: see '/md_img_2_b64/__main__.py'.
To run in IDE: use this script.
"""
from textwrap import dedent

import md_img_2_b64


def mainloop():
    print(dedent('''
        Input `<file_i>;<file_o>` to convert markdown file to html base64 file.
        Input `<file_i>` to convert markdown file to html base64 file with auto
            generated output file (in the same dir with a "~.base64.<ext>"
            suffix).
        Input `<file_i>;<file_o>;<mode>` to convert markdown file into the
            specific format. Available modes are:
                - md2html
                - md2md
                - html2html
        Input `x` to exit.
    ''').strip())
    
    print('-' * (80 - 8))
    
    while True:
        args = input('Input command here: ').split(';')
        if args[0] == 'x':
            exit(0)
            
        if len(args) == 1:
            file_i = args[0]
            if file_i.endswith('.md'):
                file_o = args[0][:-3] + '.base64.html'
                mode = 'md_2_html'
            elif file_i.endswith('.html'):
                file_o = args[0][:-4] + '.base64.html'
                mode = 'html_2_html'
        elif len(args) == 2:
            file_i = args[0]
            file_o = args[1]
            if file_i.endswith('.md'):
                if file_o.endswith('.html'):
                    mode = 'md_2_html'
                elif file_o.endswith('.md'):
                    mode = 'md_2_md'
            elif file_i.endswith('.html'):
                if file_o.endswith('.html'):
                    mode = 'html_2_html'
        else:
            file_i = args[0]
            file_o = args[1]
            mode = args[2].replace('2', '_2_')
            if file_o == '':
                if mode == 'md_2_html':
                    file_o = file_i[:-3] + '.base64.html'
                elif mode == 'md_2_md':
                    file_o = file_i[:-3] + '.base64.md'
                elif mode == 'html_2_html':
                    file_o = file_i[:-4] + '.base64.html'
        
        assert all((file_i, file_o, mode))  # noqa
        file_i = file_i.replace('\\', '/')
        file_o = file_o.replace('\\', '/')
        
        getattr(md_img_2_b64, mode)(file_i, file_o)
        print('    see output:', file_o)
        
        
if __name__ == '__main__':
    mainloop()
