"""
usage in cmd:
    python -m md_img_2_b64 --help
    python -m md_img_2_b64 md2md
    python -m md_img_2_b64 md2html
    python -m md_img_2_b64 html2html
"""
from argsense import cli
from lk_utils.filesniff import normpath


@cli.cmd()
def md2md(file_i, file_o=''):
    from . import md_2_md
    file_i = normpath(file_i)
    file_o = normpath(file_o) if file_o else file_i[:-3] + '.b64.md'
    return md_2_md(file_i, file_o)


@cli.cmd()
def md2html(file_i, file_o=''):
    from . import md_2_html
    file_i = normpath(file_i)
    file_o = normpath(file_o) if file_o else file_i[:-3] + '.b64.html'
    return md_2_html(file_i, file_o)


@cli.cmd()
def html2html(file_i, file_o=''):
    from . import html_2_html
    file_i = normpath(file_i)
    file_o = normpath(file_o) if file_o else file_i[:-5] + '.b64.html'
    return html_2_html(file_i, file_o)


if __name__ == '__main__':
    cli.run()
