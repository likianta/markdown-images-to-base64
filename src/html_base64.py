import re
from os.path import abspath

from common import encode_img, get_img_path


def main(ifile, ofile=''):
    """
    
    :param ifile: .html file.
    :param ofile: Output .html file. If empty, use '{ifilename}_base64.html'
        instead.
    :return:
    """
    ifile = abspath(ifile).replace('\\', '/')
    fdir, fname = ifile.rsplit('/', 1)  # filedir, filename
    with open(ifile, 'r', encoding='utf-8') as f:
        html = f.read()
    
    before_body, body, after_body = extract_html_body(html)
    
    links = fetch_image_links(body)
    for link, path in links.items():
        b64 = encode_img(get_img_path(fdir, path))
        new_link = link.replace(path, b64)
        body = body.replace(link, new_link)
    
    if ofile == '':
        ofile = ifile.replace('.html', '_base64.html')
    with open(ofile, 'w', encoding='utf-8') as f:
        f.write(before_body + body + after_body)
    return ofile


def extract_html_body(html: str):
    """ Markdown 的正文是在 <body> 标签中, 所以我们只提取 <body> 进行处理.
    
    :return:
    """
    try:
        a = html.index('<body>')
    except ValueError:
        a = html.index('<body ')
    b = html.index('</body>') + 7
    return (html[:a], html[a:b], html[b:])


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
    
    out = {}
    for img_tag in regex1.findall(content):
        img_path = regex2.findall(img_tag)[0]
        out[img_tag] = img_path
    return out


if __name__ == '__main__':
    main('../examples/demo.html', '../examples/demo_base64.html')
