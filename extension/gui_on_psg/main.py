"""
pip install pysimplegui
"""
try:
    import PySimpleGUI as Gui  # noqa
except ImportError:
    print("pysimplegui is not installed, try `pip install pysimplegui`")
    exit(1)

from lk_logger import lk

if 1:
    Gui.theme('SandyBeach')
    # Gui.theme('SystemDefault')

if 2:
    from lk_utils import currdir, loads
    
    conf = loads(currdir() + '/config.json')


def main():
    # input: file address bar and a browse button.
    # selection: which format you want to convert to.
    # output: result location and process info (file size, processed pics, etc.)
    
    builder = GuiBuilder()
    layout = builder.add_layout(
        builder.add_row(
            Gui.Input(key='file_i'),
            Gui.FileBrowse(
                'browse',
                initial_folder=conf.get('default_dir'),
                key='browse'
            ),
            Gui.Button('run', key='run'),
        ),
        builder.add_row(
            # use relative path to define file_o location
            Gui.Text(
                '',
                tooltip='use relative path to define file_o location, empty to '
                        'use same location as file_i.',
                key='file_o_input'
            ),
            Gui.Button('open', key='file_o_open'),
        ).
        builder.add_col(
            Gui.Radio('md 2 html', '0', default=True, key='md_2_html'),
            Gui.Radio('md 2 md', '0', key='md_2_md'),
            Gui.Radio('html 2 html', '0', key='html_2_html'),
        ),
        builder.add_row(
            Gui.Text('', key='info'),
        ),
        builder.add_row(
            Gui.Text('', key='file_o_output'),
        )
    )
    
    win = Gui.Window('Markdown Images to Base64 Embedded', layout)
    
    while True:
        evt, val = win.read()
        if evt == Gui.WIN_CLOSED:
            break
        if evt == 'run':
            lk.logp(evt, val)
            if val['file_i']:
                file_i = val['file_i']
                file_o = file_i.replace('.md', '.html')


class GuiBuilder:
    
    def __init__(self):
        self.layout = []
    
    def add_layout(self, *rows):
        assert all(isinstance(i, list) for i in rows)
        self.layout.extend(rows)
        return self.layout
    
    # @staticmethod
    # def build(layout):
    #     return layout
    
    @staticmethod
    def add_row(*items):
        return list(items)
    
    @staticmethod
    def add_col(*items):
        out = []
        for i in items:
            if isinstance(i, list):
                out.append(i)
            else:
                out.append([i])
        return out


if __name__ == '__main__':
    main()
