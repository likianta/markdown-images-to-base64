import re
from os.path import abspath
from os.path import split
from os.path import splitext

from lk_utils.read_and_write import read_file

from .common import encode_img
from .common import get_img_path
from .common import refmt_io


@refmt_io
def md_2_html(file_i: str, file_o=''):
    """
    Args:
        file_i: *.md. use abspath
        file_o: *.html
    """
    filedir, filename = split(file_i)
    
    with open(file_i, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for pattern, link in fetch_image_links(content):
        if img_path := get_img_path(filedir, link):
            b64 = encode_img(img_path)
            new_pattern = pattern.replace(link, b64)
            content = content.replace(pattern, new_pattern, 1)
            ''' Note: 该方法不够稳定, 存在以下风险:
                如果 markdown 正文中出现
                    "The image format in markdown is `![alt](img_link title)`."
                这样的讲解性文字, 也会被误认为是一个图片链接, 导致被替换成
                base64.
            '''
    
    with open(file_o, 'w', encoding='utf-8') as f:
        f.write(
            compose_html(
                title=splitext(filename)[0],
                md=content,
            )
        )
    print('See output at "{}:0"'.format(file_o))
    return file_o


def fetch_image_links(content: str) -> dict:
    """ Get local image links from markdown.
    
    Returns:
        out: {pattern: link, ...}
            e.g. {
                '![landscape](beautiful_sea.png "The Sea")': 'beautiful_sea.png',
                ...
            }
    """
    regex1 = re.compile(r'!\[[^]]*]\([^)]+\)')
    #                       |^--^ | |^--^  |
    #                       ^-----^ ^------^
    regex2 = re.compile(r'(!\[[^]]*]\()([^"\')]+)')
    #                     |  ^-----^  |^--------^
    #                     ^-----------^
    for pattern in regex1.findall(content):
        link = regex2.match(pattern)[2].strip()
        yield pattern, link


_STYLES_DIR = abspath(f'{__file__}/../../../styles')


def compose_html(
        title: str, md: str,
        css=f'{_STYLES_DIR}/github-markdown.css',
        syntax_highlight=f'{_STYLES_DIR}/syntax_highlight/richleland-pygments'
                         f'-css/default.css'
):
    """ Convert markdown to pure html, then rendered by github-markdown-css.
    
    Args:
        title: Suggest passing filename (without suffix) or the first line of
            `md` as title.
        md: The markdown text.
        css: For now (2020-11-26) we only support Github flavored markdown theme
            (see https://github.com/sindresorhus/github-markdown-css), in
            theoretically, any class-less markdown stylesheets can also be
            available (thus Typora themes not meet the requirements.)
        syntax_highlight: You can download syntax highlight css from
            http://richleland.github.io/pygments-css/, and put it in 'assets/
            syntax_highlight' folder.
        
    References:
        https://github.com/trentm/python-markdown2
        https://github.com/sindresorhus/github-markdown-css
    """
    import markdown2
    import textwrap
    #   https://google.github.io/styleguide/pyguide.html#310-strings
    
    # 1/3: Templates
    html = textwrap.dedent('''\
        <!doctype html>
        <html>
            {__head__}
            {__body__}
        </html>
    ''')
    head = textwrap.dedent('''\
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width initial-scale=1'>
            {__title__}
            {__style__}
        </head>
    ''')
    title = f'<title>{title}</title>'
    style = textwrap.dedent('''\
        <style>
            /* GitHub theme uses 980px width and 45px padding, and 15px padding
               for mobile. */
               
            .markdown-body {{
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }}
            
            @media (max-width: 767px) {{
                .markdown-body {{
                    padding: 15px;
                }}
            }}
            
            {__main_style__}
            {__syntax_highlight__}
        </style>
    ''')
    body = textwrap.dedent('''\
        <body>
            <div id='write' class='markdown-body'>
                {__content__}
            </div>
        </body>
    ''')
    content = markdown2.markdown(md, extras=[
        # https://github.com/trentm/python-markdown2/wiki/Extras
        'code-friendly',
        'cuddled-lists',
        'fenced-code-blocks',
        'header-ids',
        'numbering',
        'strike',
        'tables',
        'task_list',
        'toc',
    ])
    content = re.sub(  # Remove 'disabled' from checkbox elements.
        r'<(input type="checkbox" class="task-list-item-checkbox"(?: checked)?)'
        r' disabled>', r'<\1>', content
    )
    
    # 2/3: Interpolates
    body = body.format(__content__=content)
    style = style.format(__main_style__=read_file(css),
                         __syntax_highlight__=read_file(syntax_highlight))
    head = head.format(__title__=title, __style__=style)
    html = html.format(__head__=head, __body__=body)
    
    # 3/3: Return full html
    return html
