"""
Change 'highlight' class to 'codehilite' in 'assets/syntax_highlight/*'.
"""
from lk_utils.filesniff import findall_files
from lk_utils.read_and_write import read_file, write_file


def main(idir, odir):
    print(':i0')
    for path, name in findall_files(idir, suffix='.css'):
        print(':i', name)
        ifile, ofile = path, f'{odir}/{name}'
        rdata = read_file(ifile)
        wdata = rdata.replace('.highlight', '.codehilite')
        write_file(wdata, ofile)


if __name__ == '__main__':
    main('./richleland-pygments-css', '../../tests/css_modified')
