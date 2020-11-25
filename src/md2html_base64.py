import re
from os.path import abspath, split, splitext

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
        f.write(compose_html(doc, enable_checkbox=True))
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


def compose_html(doc, enable_checkbox=False):
    import markdown2
    html = markdown2.markdown(doc, extras={
        # https://github.com/trentm/python-markdown2/wiki/Extras
        'code-friendly': None, 'cuddled-lists': None,
        'fenced-code-blocks': None, 'header-ids': None, 'numbering': None,
        'strike': None, 'tables': None, 'task_list': None, 'toc': None,
        'html-classes': {
            # Refer to typora exported html tags
        }
    })
    
    # Some modifications
    if enable_checkbox is True:
        # This allow us to switch states of checkboxes in browser.
        html = re.sub(
            r'<(input type="checkbox" class="task-list-item-checkbox"'
            r'(?: checked)?) disabled>', r'<\1>', html
        )
    
    # css: TODO
    
    return html


if __name__ == '__main__':
    # main('../examples/demo.md', '../examples/demo_base64.md')
    main('/Users/Likianta/Desktop/temp/test_20201126_000445.md')
