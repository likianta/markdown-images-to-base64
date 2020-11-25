import re
from os.path import abspath

from common import encode_img, get_img_path


def main(ifile, ofile=''):
    """
    
    :param ifile: .md file.
    :param ofile: Output .md file. If empty, use '{ifilename}_base64.md'
        instead.
    :return:
    """
    ifile = abspath(ifile).replace('\\', '/')
    fdir, fname = ifile.rsplit('/', 1)  # filedir, filename
    with open(ifile, 'r', encoding='utf-8') as f:
        doc = f.read()
    
    links = fetch_image_links(doc)
    for link, path in links.items():
        b64 = encode_img(get_img_path(fdir, path))
        new_link = link.replace(path, b64)
        doc = doc.replace(link, new_link)
    
    if ofile == '':
        ofile = ifile.replace('.md', '_base64.md')
    with open(ofile, 'w', encoding='utf-8') as f:
        f.write(doc)
    return ofile


def fetch_image_links(doc: str):
    """ Get local image links from markdown.
    :return out: {img_link: img_path}
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


if __name__ == '__main__':
    main('../examples/demo.md', '../examples/demo_base64.md')
