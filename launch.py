import sys
from os.path import exists
from os.path import isfile
from textwrap import dedent

from md_img_2_b64 import md_2_html


def mainloop():
    while True:
        print('---------------------------------------------------------------')
        print(dedent('''
            Command List:
                <markdown_file>
                    - input a markdown file (abspath), output html file in
                      the same dir.
                <markdown_file>;<html_file>
                    - input a markdown file and appoint a html file path
                      as output.
                    - use a semicolon symbol to split the two paths.
                    - if the html file exists, it will be overwritten.
                x   - exit and close the window
        ''').strip())
        
        cmd = input('Input command here: ')
        
        if cmd == 'x':
            sys.exit(0)
        
        if ';' in cmd:
            i, o = cmd.split(';')
        else:
            i, o = cmd, ''
        if exists(i) and isfile(i):
            md_2_html(i, o)
        else:
            continue


if __name__ == '__main__':
    mainloop()
    # md_2_html(
    #     # r'E:\documents\notebook\工作\discussions\technical-details-about-new-packaging-tool-20210923.zh.md',
    #     # r'E:\documents\notebook\工作\discussions\usb-dongle-gui-meeting-summary-20210923.zh.md',
    #     r'E:\documents\notebook\临时\temp-2021-09-23.md',
    # )
