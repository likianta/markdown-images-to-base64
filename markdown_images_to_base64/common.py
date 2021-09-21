import base64
from os.path import splitext, abspath


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
        ''' os.path's trick
        Examples:
            base = 'a/b/c'
            link = '../d'
                -> os.path.abspath(f'{base}/{link}')
                    -> 'a/b/c/../d'
                        -> 'a/b/d'
            PS: 'a/b/c/' + '/' + '../d' has the same result.
        '''
        return abspath(f'{base}/{link}')


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
    ext = splitext(file)[1][1:]  # e.g. '.gif' -> 'gif'
    data = data.decode('utf-8')  # convert bytes to str
    return 'data:image/{};base64, {}'.format(ext, data)
