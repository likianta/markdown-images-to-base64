import re

from .common import encode_img
from .common import get_img_path
from .common import refmt_io


@refmt_io
def html_2_html(file_i, file_o=''):
    """
    Args:
        file_i: .html file.
        file_o: Output .html file
    """
    fdir, fname = file_i.rsplit('/', 1)  # filedir, filename
    with open(file_i, 'r', encoding='utf-8') as f:
        html = f.read()
    
    before_body, body, after_body = extract_html_body(html)
    
    for link, path in fetch_image_links(body):
        if local_path := get_img_path(fdir, path):
            b64 = encode_img(local_path)
            new_link = link.replace(path, b64)
            body = body.replace(link, new_link)
    
    with open(file_o, 'w', encoding='utf-8') as f:
        f.write(before_body + body + after_body)
    return file_o


def extract_html_body(html: str):
    """ Markdown 的正文是在 <body> 标签中, 所以我们只提取 <body> 进行处理.
    
    :return:
    """
    try:
        a = html.index('<body>')
    except ValueError:
        a = html.index('<body ')
    b = html.index('</body>') + 7
    return html[:a], html[a:b], html[b:]


def fetch_image_links(content: str):
    """ Get local image links from html body.
    
    Link extraction:
        IN: <img src=".assets/image-20201023191159409.png" referrerpolicy="no-
             referrer" alt="image-20201023191159409">
        OUT: ".assets/image-20201023191159409.png"
    
    :return out: {img_tag: img_path}
    """
    regex1 = re.compile(r'<img [^>]+>')
    regex2 = re.compile(r'(?<=src=")[^"]+|(?<=src=\')[^\']+')
    for img_tag in regex1.findall(content):
        img_path = regex2.findall(img_tag)[0]
        yield img_tag, img_path
