import re
from os.path import abspath, split, splitext

from lk_utils.read_and_write import read_file

from common import encode_img, get_img_path


def main(ifile: str, ofile=''):
    """
    Args:
        ifile: Input .md file.
        ofile: Output .html file. If empty, use '{ifilename}.html' instead.
    """
    ifile = abspath(ifile)
    fdir, fname = split(ifile)  # fdir, fname: filedir, filename
    
    with open(ifile, 'r', encoding='utf-8') as f:
        doc = f.read()
    
    for pattern, link in fetch_image_links(doc).items():
        if img_path := get_img_path(fdir, link):
            b64 = encode_img(img_path)
            new_pattern = pattern.replace(link, b64)
            doc = doc.replace(pattern, new_pattern, 1)
            ''' Note: 该方法不够稳定, 存在以下风险:
                如果 markdown 正文中出现
                    "The image format in markdown is `![alt](img_link title)`."
                这样的讲解性文字, 也会被误认为是一个图片链接, 导致被替换成 base64 (假如这个
                图片存在的话).
            '''
    
    if ofile == '':
        ofile = splitext(ifile)[0] + '.html'
    with open(ofile, 'w', encoding='utf-8') as f:
        f.write(
            compose_html(
                title=splitext(fname)[0],
                doc=doc,
            )
        )
    print('See output at "{}:0"'.format(ofile))


def fetch_image_links(doc: str) -> dict:
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
    
    out = {}
    for pattern in regex1.findall(doc):
        link = regex2.match(pattern)[2].strip()
        out[pattern] = link
    return out


def compose_html(title, doc):
    import markdown2
    html = markdown2.markdown(doc, extras={
        # https://github.com/trentm/python-markdown2/wiki/Extras
        'code-friendly'     : None, 'cuddled-lists': None,
        'fenced-code-blocks': None, 'header-ids': None, 'numbering': None,
        'strike'            : None, 'tables': None, 'task_list': None, 'toc': None,
        'html-classes'      : {
            # Refer to typora exported html tags
            # Note: 经测试发现, <ul>, <li>, <input> 标签设置 class 无效. 后面我会单独对
            #       它们做修正.
            'a': 'md-header-anchor',
        }
    })
    html = html.replace(
        '<li><input type="checkbox" class="task-list-item-checkbox" checked '
        'disabled>',
        '<li class="md-task-list-item task-list-item task-list-done"><input '
        'type="checkbox"/>'
    ).replace(
        '<li><input type="checkbox" class="task-list-item-checkbox" disabled>',
        '<li class="md-task-list-item task-list-item task-list-not-done">'
        '<input type="checkbox"/>'
    )
    
    # return html  # TEST Return
    
    # --------------------------------------------------------------------------
    
    # For now the html has no stylesheet applied.
    # We adjust it more compatible to Typora html format (like adding header and
    # footer, etc.), and apply a Typora theme onto it.
    
    import textwrap  # https://google.github.io/styleguide/pyguide.html#310-strings
    outframe = textwrap.dedent('''\
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
    style = f'<style type="text/css">' \
            f'{read_file("../assets/github-typora.css")}</style>'
    body = textwrap.dedent('''\
        <body class='typora-export'>
            <div id='write' class=''>
                {__content__}
            </div>
        </body>
    ''')
    content = html
    
    body = body.format(__content__=content)
    head = head.format(__title__=title, __style__=style)
    outframe = outframe.format(__head__=head, __body__=body)
    
    return outframe


if __name__ == '__main__':
    # main('../examples/demo.md', '../examples/demo_base64.md')
    main('/Users/Likianta/Desktop/documents/notebook/清单/博客文章.md',
         '/Users/Likianta/Desktop/temp/test_content.html')
