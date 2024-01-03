"""Provide calculations and values for speaker.

This module allows the user to work with speaker.

Examples:
    >>> import speaker
    >>> speaker.calEBP(1.0, 1.0)
    1.0

Contains the following functions:
- `calEBP(Qes, fs)` returns EPB
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
#from quantity import quantity 
#from common.quantity import quantity 
from solver.quant import Quant

def calEBP(Qes: float, fs: float) -> float:
    """Calculate EBP (Efficiency Bandwidth Product)

    Examples:
        >>> calEBP(0.32, 27.0)
        84.375
    
    Args:
        Qes:    Electrical Q factor, unitless
        fs:     Resonance frequency, Hz

    Returns:
        Efficiency Bandwidth Product

    Raises:
        ZeroDivisionError: trying to divide by Qes == 0
    """

    if Qes == 0:
        raise ZeroDivisionError("division by zero")

    EBP = float(fs)/Qes

    return EBP


class Speaker:
    """Speaker parameters and calculations (without enclosure)
    """

    def __init__(self, name="speaker"):
        #self.producer = producer
        #self.model = model
        #self.description = description
        self.name="default name for speaker"
        self.par={
            'r_pow': Quant(
                name='rated power',
                value=0.0,
                unit='W',
                desc=("A speaker's power rating details "
                    "the amount of power that it can safely handle."), 
                calculate=False
                ),
            'max_pow': Quant(
                name='maximum power',
                value=0.0,
                unit='W',
                desc="Maximum power is the power that the speaker "
                     "can handle for short periods of time without "
                     "being damaged.",
                calculate=False,
                ),
            'z': Quant(
                name='nominal impedance',
                value=0.0,
                unit='Ohm',
                desc="nominal impedance is an estimate "
                     "of the minimum impedance for typical "
                     "audio ranges usually 4, 8, or 16 Ohms",
                calculate = False
                ),
            'Vas': Quant(
                name='equivalent volume',
                value=0.0,
                unit='l',
                desc="The Vas measurement in litres "
                     "is the size of the ‘imaginary’ box "
                     "which has exactly the same restoring "
                     "force as the suspension of the driver.",
                calculate=False,
                ),
            'u_fr': Quant(
                name = 'Upper frequency response',
                value = 0.0,
                unit = "Hz",
                desc = 'Upper frequecy of the driver in which'
                       'it shall work',
                calculate = False
                ),
            'SPL': Quant(
                name = 'Sound Pressure Level',
                value = 0.0,
                unit = "dB",
                desc = 'Mean sound pressure level measured'
                    'at power 1 W and 1m from speaker',
                calculate = False
                ),
            'fs': Quant(
                name = 'Resonance frequency',
                value = 0.0,
                unit = "Hz",
                desc = 'Mechanical resonance frequency'
                    'of freely mounted speaker',
                calculate = False,
                ),
            'Qts': Quant(
                name = 'Total Q factor',
                value = 0.0,
                unit = "Unitless",
                desc = 'inverse of damping ratio of speaker'
                    'lower Q means more control'
                    'Qts<0.4 is usually for drivers for ported'
                    'enclosure, 0.4<Qts>0.7 for closed, and Qts>0.7'
                    'for free-air or infite baffle type',
                calculate = False,
                    ),
            'Qes': Quant(
                name = 'Electrical Q factor',
                value = 0.0,
                unit = "Unitless",
                desc = 'is the amount of control coming from'
                    'the electrical components of a speaker'
                    '(the voice coil and magnet) which contribute'
                    'to the suspension system',
                calculate = False,
                    ),
            'EBP': Quant(
                name = 'Efficiency Bandwidth Product',
                value = 0.0,
                unit = "Unitless",
                desc = 'shows the trade-off between efficiency'
                    'and bandwidth of a driver.'
                    'EBP < 50 - use only for a sealed box'
                    'EBP 50 - 100 - can be used in either'
                    'EBP > 100 - vented box only',
                calculate = True,
                    ),
            }

    exc=20      # excursion limit inmm
    mi=1.1      # Magnetic induction in Tesla
    mf=600      # Magnetic flux in uWebber
    Qms=3.4     # Mechanical Q factor
    # TODO add other

    def recalculate(self, val:str) -> list:
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

        # set ignore repetition of values
        calc_set = set()
        if val in ("Qes", "fs", "all"):
            calc_set.add("EBP")
            if self.par['EBP'].calculate:
                self.setEBP()
                logger.debug(f"after '{val}' was changed, "
                    f"{calc_set} shall be updated")
        return (list(calc_set))

    def setEBP(self):
        """set EBP (Efficiency Bandwidth Product) in speaker class
        """

        try:
            self.par['EBP'].value = calEBP(
                    float(self.par['Qes'].value),
                    float(self.par['fs'].value)
                    )
            logger.debug(f"calculated EBP is {self.par['EBP'].value}")
        except:
            self.par['EBP'].value = 0.0
            logger.exception("can't calculate EBP")

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
    logger.setLevel(level='DEBUG')
    spkr = Speaker()
   # spkr.read_from_file()
   # print(f"speaker producer from file: {spkr.producer}")
   # print(f"speaker rated power from file: {spkr.par['r_pow'].value}")
    spkr.par['fs'].value=27.0
    spkr.par['Qes'].value=0.32
   # spkr.save_to_file()
   # visaton=Speaker("Visaton")
   # for key, val in visaton.par.items():
   #     print(key, val)
   # visaton.key_as_short_name()
   # print(f"long name: {visaton.par['z'].name}, "
   #       f"short name: {visaton.par['z'].short_name}")
   # visaton.par['fs'].value=27.0
   # visaton.par['Qes'].value=0.32
    print (f"EBP = {spkr.par['EBP'].value}")
    print (calEBP(0.32, 27.0))
    print (f"EBP = {spkr.par['EBP'].value}")
    print (spkr.setEBP())
    print (f"EBP = {spkr.par['EBP'].value}")
    spkr.par['fs'].value=30.0
    spkr.par['Qes'].value=0.32
    print(spkr.recalculate("all"))
    print (f"EBP recalculated = {spkr.par['EBP'].value}")
