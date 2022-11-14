import base64
import os


def refmt_io(func):  # a decorator
    assert func.__name__ in ('md_2_html', 'md_2_md', 'html_2_html'), (
        'the function name is not support to extract its conversion type. '
        'you need to provide function names like "md_2_md", "md_2_html", etc.',
        func.__name__
    )
    
    def _refmt_io(file_i, file_o='', *args, **kwargs):
        ext_i, ext_o = func.__name__.split('_2_')
        assert os.path.exists(file_i) and file_i.endswith(ext_i)
        if not file_o:
            file_o = '{}/{}.base64.{}'.format(
                os.path.dirname(file_i),
                os.path.splitext(os.path.basename(file_i))[0],
                ext_o
            )
        print(file_i, file_o)
        if os.path.exists(file_o):
            print('the target file already exists, it will be overriden')
        return func(file_i, file_o, *args, **kwargs)
    
    return _refmt_io


def get_img_path(base: str, link: str) -> str:
    """ Get the full path from the markdown image link.
    Args:
        base: Path of html's folder
        link: Path from `md2html_base64.fetch_image_links`
    
    Returns: [str abspath | str empty]
        empty: It means the `link` is a weblink, not a local file path.
    """
    if link.startswith('http'):
        return ''
    else:
        out = os.path.abspath(f'{base}/{link}')
        if os.path.exists(out):
            return out
        else:
            return ''


def encode_img(file: str) -> str:
    """
    References:
        https://blog.csdn.net/u013055678/article/details/71406746
        
    Notes:
        对 base64 编码后的图片加一个前缀 'data:image/{image_type};base64, ', 这样
        markdown 编辑器和浏览器才能正常显示.
    
    Args:
        file: Image (absolute) path.
    
    Returns:
        Base64 encoded string of image.
    """
    with open(file, 'rb') as f:
        data = base64.b64encode(f.read())
    ext = os.path.splitext(file)[1][1:]  # e.g. '.gif' -> 'gif'
    data = data.decode('utf-8')  # convert bytes to str
    return 'data:image/{};base64, {}'.format(ext, data)
