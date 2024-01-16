import glob

def list_sections(
        path:str = 'sections/',
        hide:str = 'template') -> list:
    """list sections in calcualotors

    check .ini files in directory (sections as default)
    and return list of thier basenames
    """

    # remove trailing directory
    sections = [x.split('/')[-1] for x in glob.glob(path + '/*.ini')]
    # remove .ini
    sections = [x.split('.')[0] for x in sections]
    # remove hide parameter
    sections = [x for x in sections if x != hide]
    return sections

if __name__ == "__main__":
    if False:
        print(list_sections())
    else:
         import sys
         sys.path.append('..')
         from common import testcases
         testcases.CallExternalFile('list_sections')
