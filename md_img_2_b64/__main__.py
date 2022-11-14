"""
usage in cmd:
    python -m md_img_2_b64 --help
    python -m md_img_2_b64 md2md
    python -m md_img_2_b64 md2html
    python -m md_img_2_b64 html2html
"""

from argsense import cli


@cli.cmd()
def md2md(file_i, file_o=''):
    from . import md_2_md
    return md_2_md(file_i, file_o or file_i[:-3] + '.b64.md')


@cli.cmd()
def md2html(file_i, file_o=''):
    from . import md_2_html
    return md_2_html(file_i, file_o or file_i[:-3] + '.b64.html')


@cli.cmd()
def html2html(file_i, file_o=''):
    from . import html_2_html
    return html_2_html(file_i, file_o or file_i[:-5] + '.b64.html')


if __name__ == '__main__':
    cli.run()
