"""Provide calculations and values for cables.

This module allows the user to work with cables.

Examples:
    >>> import cable
    >>> cable

Contains the following functions:
- `Impedance(lenght, diameter)` returns resistance
"""
# search path to import all

import sys
sys.path.append('../')

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

def calR(ro: float, lenght: float, area: float) -> float:
    """Calculate resistance of cable

    Examples:
        >>> calR(0.32, 2.0, 2,5)
        84.375 TODO
    
    Args:
        ro:     resistivity of material
        lenght: lenght of cable
        area:   area of cable

    Returns:
        Resistance of cable

    Raises:
        ZeroDivisionError: trying to divide by area == 0
    """

    if area == 0:
        raise ZeroDivisionError("division by zero")

    resistance = float(ro)*float(lenght)/float(area)

    return resistance


class Cable:
    """cable parameters and calculations 
    """

    def __init__(self, name="default"):
        self.name=name
        self.par={
            's': Quant(
                name='section area',
                value=0.0,
                unit='mm2',
                desc="section area of cable",
                calculate=False
                ),
            'l': Quant(
                name='lenght',
                value=0.0,
                unit='m',
                desc="lenght of cable",
                calculate=False,
                ),
            'ro': Quant(
                name='coefficient of resistivity',
                value=0.0,
                unit='Ohm*m',
                desc="resistivity of cable material",
                calculate = False
                ),
            'R': Quant(
                name='resistance',
                value=0.0,
                unit='Ohm',
                desc="resistane of cable",
                calculate=True,
                ),
            }

    def recalculate(self):
        # TODO recurency of tables for calculate only updated
        if self.par['R'].calculate:
            self.setR()

    def setR(self):
        """set R (resistance) of cable"""

        try:
            self.par['R'].value = calR(
                    float(self.par['ro'].value),
                    float(self.par['l'].value),
                    float(self.par['s'].value),
                    )
            logger.debug(f"calculated resistance is \
                    {self.par['R'].value}")
        except:
            self.par['R'].value = 0.0
            logger.exception("can't calculate resistance")

    def key_as_short_name(self):
        for key, val in self.par.items():
            val.short_name=key

    def save_to_file(self, filename=""):
        """save speakers data to .ini file
        """

        # TODO test cases

        PATH = 'cables/'

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

        logger.debug(f"filename to save cable: {filename}")
        save_cable = configparser.ConfigParser()
        save_cable['general'] = {
                'name': self.name,
                }
        for key, val in self.par.items():
            logger.debug(f"keys to save: {key}")
            save_cable[key] = val.dictionary(
                    to_rem=('short_name', 'desc')
                    )
        with open(filename, 'w') as file:
            save_cable.write(file)

    def read_from_file(self, file=""):
        """read cable data from file
        """
        # TODO test cases
        rspeak = configparser.ConfigParser()
        rspeak.read(file)
        logger.debug(f"start reading file: {file}")
        logger.debug(f"sections in file: {rspeak.sections()}")
        for section in rspeak.sections():
            if section == "general":
                logger.debug("general section readed")
                self.name = rspeak[section]['name']
            else:
                if section in self.par:
                    self.par[section].value=rspeak[section]['value']
                    self.par[section].unit=rspeak[section]['unit']
                    logger.debug(f"section {section} readed from file")
                else:
                    logger.warning(
                            f"unknown section: {section} in {file}"
                            )
        logger.debug("end of reading cable config file")
    
if __name__=='__main__':
    logger.setLevel=(logging.DEBUG)
    cable = Cable()
   # print(f"speaker rated power from file: {spkr.par['r_pow'].value}")
    cable.par['ro'].value=1.0
    cable.par['l'].value=1.0
    cable.par['s'].value=1.0
   # spkr.save_to_file)
   # visaton=Speaker("Visaton")
   # for key, val in visaton.par.items():
   #     print(key, val)
   # visaton.key_as_short_name()
   # print(f"long name: {visaton.par['z'].name}, "
   #       f"short name: {visaton.par['z'].short_name}")
   # visaton.par['fs'].value=27.0
   # visaton.par['Qes'].value=0.32
    print (f"R = {cable.par['R'].value}")
    print (calR(0.32, 27.0, 4))
    print (f"R = {cable.par['R'].value}")
    print (cable.setR())
    print (f"R = {cable.par['R'].value}")
    cable.par['ro'].value=30.0
    cable.par['l'].value=0.32
    cable.par['s'].value=0.32
    cable.recalculate()
    print (f"R recalculated = {cable.par['R'].value}")
