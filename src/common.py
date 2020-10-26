import base64
from os.path import splitext


def convert_relpath_2_abspath(stub: str, path: str):
    """

    :param stub: an abspath of the html's folder
    :param path: comes from `fetch_image_links`
    :return:
    """
    if path.startswith('http'):
        return path
    elif path[1:2] == ':/':
        # e.g. 'D:/A/B/C.png'
        return path
    elif path.startswith('/'):
        return stub + path
    elif path.startswith('./'):
        return stub + path[1:]
    elif path.startswith('../'):
        backward = -path.count('../')
        stub_nodes = stub.split('/')
        return '/'.join(stub_nodes[:backward]) + '/' + path.lstrip('../')
    else:
        return stub + '/' + path


def convert_image_2_base64(img_path):
    """
    Refer: https://blog.csdn.net/u013055678/article/details/71406746
    注意: 对 base64 编码后的图片加一个前缀 'data:image/{image_type};base64, ',
        这样 markdown 编辑器和浏览器才能正常显示.
    
    :param img_path:
    :return:
    """
    with open(img_path, 'rb') as f:
        data = base64.b64encode(f.read())
    ext = splitext(img_path)[1][1:]  # e.g. '.gif' -> 'gif'
    data = data.decode('utf-8')
    return 'data:image/{};base64, {}'.format(ext, data)
