import re
from os.path import abspath

from common import convert_image_2_base64, convert_relpath_2_abspath


def main(ifile, ofile=''):
    """
    Args:
        ifile: .md file.
        ofile: Output .html file. If empty, use '{ifilename}.html' instead.
    
    """
    ifile = abspath(ifile).replace('\\', '/')
    fdir, fname = ifile.rsplit('/', 1)  # filedir, filename
    with open(ifile, 'r', encoding='utf-8') as f:
        doc = f.read()
    
    links = fetch_image_links(doc)
    for link, path in links.items():
        b64 = convert_image_2_base64(convert_relpath_2_abspath(fdir, path))
        new_link = link.replace(path, b64)
        doc = doc.replace(link, new_link)
    
    if ofile == '':
        ofile = ifile.replace('.md', '.html')
    with open(ofile, 'w', encoding='utf-8') as f:
        f.write(compose_html(doc))
    return ofile


def fetch_image_links(doc: str) -> dict:
    """ Get local image links from markdown.
    
    Returns:
        out: {img_link: img_path, ...}
            e.g. {
                '![image-20201023121704430](.assets/image-20201023121704430.png
                "desc")': '.assets/image-20201023121704430.png',
                ...
            }
    """
    regex1 = re.compile(r'!\[[^]]*]\([^)]+\)')
    #                     ^ ^-----^ ^------^
    regex2 = re.compile(r'(!\[[^]]*]\()([^"\')]+)')
    #                     ^-----0-----^^----1---^
    #   '![image-20201023121704430](.assets/image-20201023121704430.png "desc")'
    #   -> ['![image-20201023121704430](',
    #       '.assets/image-20201023121704430.png ']
    
    out = {}
    for img_link in regex1.findall(doc):
        img_path = regex2.match(img_link)[2].strip()
        out[img_link] = img_path
    return out


def compose_html(doc):
    import markdown2
    html = markdown2.markdown(doc, extras={
        # https://github.com/trentm/python-markdown2/wiki/Extras
        'code-friendly': None, 'cuddled-lists': None,
        'fenced-code-blocks': None, 'header-ids': None, 'numbering': None,
        'strike': None, 'tables': None, 'task-list': None, 'toc': None,
        'html-classes': {
            # refer to typora exported html tags
        }
    })
    
    # css: TODO
    
    return html


if __name__ == '__main__':
    main('../examples/demo.md', '../examples/demo_base64.md')
