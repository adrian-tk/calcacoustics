"""Provide template for bundle calculations

Copy it with new section name, 
and copy ini file with this same new name

This template is used also for testing scripts.
"""

#TODO  move class to other file, and inheritance them 

# search path to import all
import sys
# file shall be in solver/sections subfolder - add main folder
sys.path.append('../../')

try:
    from solver.logger import logging
    from solver.logger import logger
    from solver.logger import logcom
    # set this logger as a child of main logger
    logger = logger.getChild(__name__)
    logger.debug("imported loggers")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("Maybe You shall be in env?")



import os
import configparser
from solver.quant import Quant


class CalcBundle:
    """calculator parameters and functions
    """

    def __init__(self, name="just template"):
        filename = os.path.basename(__file__)
        self.section_name = os.path.splitext(filename)[0]
        self.section_description = ""
        self.name=name
        # dictionary of dependencies for calculations
        self.par={}
        self.load_parameters()
        # dictionary of parameters for solver
        self.dep={}
        self.load_dependencies()
        logger.debug(f"{self.section_name} section initialised")

    # here create functions for calculation
    def cal_sum(self, first: float, second: float) -> float:
        """Calculate sum of two numbers

        Examples:
            >>> cal_sum(3.0, 0.14 )
            3.14
        
        Args:
            first:  first number to add
            second: second number to add

        Returns:
            sum of two numbers

        Raises:
            don't rises any error
        """

        ans = float(first) + float(second)

        return ans

    def load_parameters(self):
        """ loads parameters from .ini file

        ini shall has this same name as module
        """
        ininame = self.section_name + '.ini'
        inifile = configparser.ConfigParser()
        ininame =[
                '../solver/sections/' + ininame,
                'solver/sections/' + ininame,
                ininame,
                ]
        logger.info(f"fileconfig: {ininame}")

        inifile.read(ininame, encoding='utf-8')
        logger.debug(f"reading section config file: {ininame}")
        logger.debug(f"sections in file: {inifile.sections()}")
        if inifile.sections() == []:
            logger.error(f"can't read data from {ininame}")
        for section in inifile.sections():
            if section == "general":
                #logger.debug("general section read")
                self.section_description = inifile[section]['description']
            else:
                self.par[section] = Quant(
                    name=inifile.get(section, 'name'),
                    value=inifile.getfloat(section, 'value'),
                    unit=inifile.get(section, 'unit'),
                    desc=inifile.get(section, 'desc'),
                    calculate=inifile.getboolean(section, 'calculate'),
                    dependencies=inifile.get(section,
                        'dependencies', fallback=''),
                    )
                #logger.debug(f"section {section} read from file")
        #logger.debug("end of reading section config file")

    def load_dependencies(self):
        """save dependencies from 'par' to 'dep' dictionary"""

        for pkey, pval in self.par.items():
            if pval.dependencies != '':
                tmp_list = [s.strip() \
                        for s in pval.dependencies.split(',')]
                self.dep[pkey] = tmp_list
        logger.debug(f"list of dependencies: {self.dep}")



    def recalculate(self, val:str='all') -> list:
        """Decide what to calculate after values are updated.
        
        Examples:
            >>> recalculate("fs")
            ['EBP']

        Args:
            val:    value that was changed, probably in GUI
                    "all" updated all values

        Returns:
            list of values need to be updated, probably in GUI
        """

        ans = []
        for dkey, dval in self.dep.items():
            if self.par[dkey].calculate:
                if val in dval or val == 'all':
                    # TODO to replace funcion name
                    logger.debug(f"{dkey} needs to be recalculated")
                    to_cal_item = getattr(self, 'cal_'+dkey)
                    # list with values
                    tmp_val = [self.par[x].value for x in dval] 
                    self.par[dkey].value = to_cal_item(*tmp_val)
                    logger.debug(f"{dkey} for {dval} " 
                            f"is {self.par[dkey].value}")
                    ans.append(dkey)
        logger.debug(f"{ans} list need to be updated")
        return(ans)


    def key_as_short_name(self):
        for key, val in self.par.items():
            val.short_name=key

    def save_to_file(self, filename=""):
        """save data to .ini file
        """

        # TODO test cases

        PATH = 'speakers/'

        # create filename
        if filename == "":
            filename = self.name + ".ini"
        if filename[-4:] != ".ini":
            filename = filename + ".ini"

        # create path
        if not os.path.isdir(PATH):
            os.mkdir(PATH)
            logger.debug(f"directory {PATH} created")
        else:
            logger.debug(f"using existed {PATH} directory")
        filename = PATH + filename

        # create new filename when actual existed already
        i=1
        while os.path.isfile(filename):
            if i == 1:
                filename = filename[:-4] + '_' + str(i) + '.ini'
            else:
                filename = filename[:filename.rfind('_')+1] \
                        + str(i) + '.ini'
            i+=1

        logger.debug(f"filename to save speaker: {filename}")
        save_speaker = configparser.ConfigParser()
        save_speaker['general'] = {
                'name': self.name,
                }
        for key, val in self.par.items():
            logger.debug(f"keys to save: {key}")
            save_speaker[key] = val.dictionary(
                    to_rem=('short_name', 'desc')
                    )
        with open(filename, 'w') as file:
            save_speaker.write(file)

    def read_from_file(self, file=""):
        """read speakers data from file
        """
        # TODO test cases
        #FILETOREAD = 'speakers/Visaton_W200SC8OHM.ini'
        rspeak = configparser.ConfigParser()
        rspeak.read(file, encoding='utf-8')
        logger.debug(f"start reading file: {file}")
        logger.debug(f"sections in file: {rspeak.sections()}")
        for section in rspeak.sections():
            if section == "general":
                logger.debug("general section readed")
                self.name = rspeak[section]['name']
                self.description = rspeak[section]['description']
            else:
                if section in self.par:
                    self.par[section].value=rspeak[section]['value']
                    self.par[section].unit=rspeak[section]['unit']
                    logger.debug(f"section {section} readed from file")
                else:
                    logger.warning(
                            f"unknown section: {section} in {file}"
                            )
        logger.debug("end of reading speaker config file")

    
if __name__=='__main__':
    obj = CalcBundle()
    #obj.load_attributes()
   # obj.read_from_file()
    for element in obj.par:
        print(f"{obj.par[element].name}: {obj.par[element].value}")
    print('changing non calculating values')
    for element in obj.par:
        if not obj.par[element].calculate:
            obj.par[element].value=0.32
    for element in obj.par:
        print(f"{obj.par[element].name}: {obj.par[element].value}")
    # TODO testing for attr 'all' and 'sum'
    obj.recalculate('first')
    print('calculate values')
    for element in obj.par:
        print(f"{obj.par[element].name}: {obj.par[element].value}")
    # TODO testing for calculate = False
   # spkr.save_to_file()
   # visaton=Speaker("Visaton")
   # for key, val in visaton.par.items():
   #     print(key, val)
   # visaton.key_as_short_name()
   # print(f"long name: {visaton.par['z'].name}, "
   #       f"short name: {visaton.par['z'].short_name}")
   # visaton.par['fs'].value=27.0
   # visaton.par['Qes'].value=0.32
