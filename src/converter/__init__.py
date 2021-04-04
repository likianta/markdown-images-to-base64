from os.path import abspath, basename, exists


def _common(file_i, file_o, target_suffix, conv_func, **kwargs):
    """
    
    Args:
        file_i: *.md
        file_o: *.md or *.html. if empty, use '{filename_i}.base64.md' or
            '{filename_i}.base64.html' instead
        target_suffix: 'md'|'html'
        **kwargs:
            'target_format': see `md_2_md.py:main:params:target_format`
    """
    assert exists(file_i)
    file_i = abspath(file_i).replace('\\', '/')
    if file_o == '':
        file_o = basename(file_i) + f'.base64.{target_suffix}'
    return conv_func(file_i, file_o, **kwargs)


def html_2_html(file_i, file_o):
    from .html_2_html import main
    return _common(file_i, file_o, 'html', conv_func=main)


def md_2_html(file_i, file_o):
    from .md_2_html import main
    return _common(file_i, file_o, 'html', conv_func=main)


def md_2_md(file_i, file_o, target_format='markdown_image_link'):
    """
    Args:
        file_i
        file_o
        target_format: see `md_2_md.py:main:params:target_format`
    """
    from .md_2_md import main
    return _common(file_i, file_o, 'md', conv_func=main,
                   target_format=target_format)


__all__ = [
    'html_2_html',
    'md_2_html',
    'md_2_md'
]
