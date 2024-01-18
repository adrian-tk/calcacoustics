import glob
import os
if __name__ == "__main__":
    from sys import path
    path.append('../')
from common import rootdir

def list_sections(
        path:str = '',
        hide:str = 'template') -> list:
    """list sections in calcualotors

    check .ini files in directory (solver/sections/ as default)
    and return list of thier basenames
    """


    if path == '':
        path = rootdir.prefix() + 'solver/sections'
        #print(path)
    # get list
    sections = glob.glob(path + '/*.ini')
    # remove directiories
    sections = [x for x in sections if os.path.isfile(x)]
    # remove trailing directory
    sections = [x.split('/')[-1] for x in sections]
    # remove .ini
    sections = [x[:-4] for x in sections]
    # remove hide parameter
    sections = [x for x in sections if x != hide]
    return sections

if __name__ == "__main__":
    print(rootdir.prefix())
    print(f"list sections: " + str(list_sections()))
    print(f"with hide = None: " + str(list_sections(hide = None)))
    if True:
        import sys
        sys.path.append('..')
        from common import testcases
        testcases.CallExternalFile('list_sections')
