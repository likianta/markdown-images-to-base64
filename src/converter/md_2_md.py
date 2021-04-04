import re

from src.common import encode_img, get_img_path


def main(file_i, file_o, target_format='markdown_image_link'):
    """
    
    Args:
        file_i: *.md
        file_o: *.md
        target_format: 'markdown_image_link'|'html_img_tag'
            'markdown_image_link': 在输出文件中, 使用 `![]({base64})` 格式
            'html_img_tag': 在输出文件中, 使用 `<img src="{base64}">` 格式
    """
    assert target_format in ('markdown_image_link', 'html_img_tag')
    
    filedir, filename = file_i.rsplit('/', 1)
    with open(file_i, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for link, path in fetch_image_links(content):
        b64 = encode_img(get_img_path(filedir, path))
        if target_format == 'markdown_image_link':
            new_link = link.replace(path, b64)
        else:
            new_link = f'<img src="{b64}">'
        content = content.replace(link, new_link)
    
    with open(file_o, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_o


def fetch_image_links(content: str):
    """ Get local image links from markdown.
    
    Returns:
        out: {img_link: img_path}
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
    for img_link in regex1.findall(content):
        img_path = regex2.match(img_link)[2].strip()
        yield img_link, img_path


if __name__ == '__main__':
    main('../../examples/demo.md', '../examples/demo_base64.md')
