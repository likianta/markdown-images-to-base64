import base64
from os.path import splitext
from pathlib import Path


def convert_relpath_2_abspath(base: Path, path: str) -> str:
    """
    Args:
        base: Path to html's folder
        path: Path from `md2html_base64.fetch_image_links`
    """
    if path.startswith('http'):
        return path
    else:
        return str(base.joinpath(path).resolve())


def convert_image_2_base64(path: str) -> str:
    """
    References:
        https://blog.csdn.net/u013055678/article/details/71406746
        
    Notes:
        对 base64 编码后的图片加一个前缀 'data:image/{image_type};base64, ', 这样
        markdown 编辑器和浏览器才能正常显示.
    
    Args:
        path: Image (absolute) path.
    
    Returns:
        Base64 encoded string of image.
    """
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read())
    ext = splitext(path)[1][1:]  # e.g. '.gif' -> 'gif'
    data = data.decode('utf-8')
    return 'data:image/{};base64, {}'.format(ext, data)
