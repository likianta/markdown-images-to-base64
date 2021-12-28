"""
pip install pysimplegui
"""

try:
    import PySimpleGUI as Gui  # noqa
except ImportError:
    print("pysimplegui is not installed, try `pip install pysimplegui`")
    exit(1)
else:
    import os.path
    
    from lk_logger import lk  # noqa
    from lk_utils import currdir
    from lk_utils import loads
    from lk_utils.filesniff import normpath
    
    import md_img_2_b64
    
    Gui.theme('SandyBeach')
    # Gui.theme('SystemDefault')
    
    conf = loads(currdir() + '/config.json')


def main():
    # input: file address bar and a browse button.
    # selection: which format you want to convert to.
    # output: result location and process info (file size, processed pics, etc.)
    
    builder = GuiBuilder()
    layout = builder.add_layout(
        builder.add_row(
            Gui.Input(
                change_submits=True,
                enable_events=True,
                key='file_i_input'
            ),
            Gui.FileBrowse(
                'browse',
                initial_folder=conf.get('default_dir'),
                key='file_i_browse'
            ),
            Gui.Button('run', key='run'),
        ),
        builder.add_row(
            # use relative path to define file_o location
            Gui.Input(
                '',
                tooltip=(
                    'the output file path. you can use "~" to refer to the '
                    'same directory with the input file.'
                ),
                key='file_o_input'
            ),
            Gui.FileBrowse(
                'browse',
                enable_events=True,
                initial_folder=conf.get('default_dir'),
                key='file_o_browse'
            ),
            Gui.Button('open', key='file_o_open'),
        ),
        builder.add_row(
            Gui.Radio(
                'md 2 html', '0',
                enable_events=True,
                default=True,
                key='md_2_html'
            ),
            Gui.Radio(
                'md 2 md', '0',
                enable_events=True,
                key='md_2_md'
            ),
            Gui.Radio(
                'html 2 html', '0',
                enable_events=True,
                key='html_2_html'
            ),
        ),
        builder.add_row(
            Gui.Text('', key='info'),
            Gui.Button('clear info', visible=False, key='clear_info'),
        ),
        builder.add_row(
            Gui.Text('', key='file_o_output'),
            Gui.Button(
                'open', visible=False, key='file_oo_open'
            ),
        )
    )
    
    win = Gui.Window('Markdown Images to Base64 Embedded', layout)
    controls = {
        'auto_update_file_o': True,
        'radio_selected'    : 'md_2_html',
    }
    
    while True:
        key, val = win.read()
        # lk.logp(key, val, controls)
        
        if key == Gui.WIN_CLOSED:
            break
        
        try:
            if key == 'clear_info':
                win['info'].update('')
                win['file_o_output'].update('')
                win['file_oo_open'].update(visible=False)
                win['clear_info'].update(visible=False)
            
            elif key == 'file_i_input':
                if not val['file_i_input']:
                    continue
                else:
                    file_i_path = normpath(val['file_i_input'])
                    name, _ = os.path.splitext(os.path.basename(file_i_path))
                
                if not val['file_o_input']:
                    controls['auto_update_file_o'] = True
                if controls['auto_update_file_o']:
                    file_i_path = normpath(val['file_i_input'])
                    basename, _ = os.path.splitext(
                        os.path.basename(file_i_path)
                    )
                    if controls['radio_selected'] == 'md_2_html':
                        file_o_path = '~/' + basename + '.base64.html'
                    elif controls['radio_selected'] == 'md_2_md':
                        file_o_path = '~/' + basename + '.base64.md'
                    elif controls['radio_selected'] == 'html_2_html':
                        file_o_path = '~/' + basename + '.base64.html'
                    else:
                        raise Exception
                    win['file_o_input'].update(file_o_path)
            
            elif key == 'file_o_browse':
                controls['auto_update_file_o'] = False
            
            elif key == 'file_o_open':
                file_o_path = val['file_o_input']
                if file_o_path.startswith('~/'):
                    file_o_path = file_o_path.replace(
                        '~', os.path.dirname(val['file_i_input'])
                    )
                if os.path.exists(file_o_path):
                    _open_file(file_o_path)
                else:
                    raise FileNotFoundError(file_o_path)
            
            elif key == 'file_oo_open':
                if f := win['file_o_output'].get():
                    _open_file(f)
            
            elif key == 'run':
                if val['file_i_input'] and val['file_o_input']:
                    file_i = normpath(val['file_i_input'])
                    file_o = normpath(val['file_o_input']).replace(
                        '~', os.path.dirname(file_i)
                    )
                    assert file_o != file_i, (file_i, file_o)
                    
                    # lk.logt('[I0557]', file_i, file_o)
                    # if input('confirm: ') != 'y': continue
                    
                    if controls['radio_selected'] == 'md_2_html':
                        assert file_i.endswith('.md'), file_i
                        md_img_2_b64.md_2_html(file_i, file_o)
                    elif controls['radio_selected'] == 'md_2_md':
                        assert file_i.endswith('.md'), file_i
                        md_img_2_b64.md_2_md(file_i, file_o)
                    elif controls['radio_selected'] == 'html_2_html':
                        assert file_i.endswith('.html'), file_i
                        md_img_2_b64.html_2_html(file_i, file_o)
                    else:
                        win['info'].update('invalid radio selected')
                        continue
                    
                    win['info'].update('successfully converted!')
                    win['file_oo_open'].update(visible=True)
                    win['file_o_output'].update(file_o)
                    win['file_oo_open'].update(visible=True)
            
            elif key in ('md_2_html', 'md_2_md', 'html_2_html'):
                controls['radio_selected'] = key
        
        except Exception as e:
            win['info'].update(str(e))


def _open_file(file_path):
    from lk_utils import run_cmd_args
    run_cmd_args('start', file_path)


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
