try:
    from logger import logging
    from logger import logger
    from logger import logcom
    # set this logger as a child of main logger
    logger = logger.getChild(__name__)
    logger.debug("imported loggers")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("Maybe You shall be in env?")

import os
import configparser
from quantity import quantity 

class Speaker:

    def __init__(self,
                 producer="ACME",
                 model="over9000",
                 description="some usual speaker",
                 ):
        self.producer = producer
        self.model = model
        self.description = description
        self.name=self.producer + '_' + self.model
        self.par={
            'r_pow': quantity(name='rated power',
                        value=0.0,
                        unit='W',
                        desc="A speaker's power rating details "
                            "the amount of power that it can safely handle."), 
            'max_pow': quantity(name='maximum power',
                         value=0.0,
                         unit='W',
                         desc="Maximum power is the power that the speaker "
                           "can handle for short periods of time without "
                           "being damaged."),
            'z': quantity(name='nominal impedance',
                         value=0.0,
                         unit='Ohm',
                         desc="nominal impedance is an estimate "
                             "of the minimum impedance for typical "
                             "audio ranges usually 4, 8, or 16 Ohms"),
            'Vas': quantity(name='equivalent volume',
                         value=0.0,
                         unit='l',
                         desc="The Vas measurement in litres "
                         "is the size of the ‘imaginary’ box "
                         "which has exactly the same restoring "
                         "force as the suspension of the driver."),
            'u_fr': quantity(
                name = 'Upper frequency response',
                value = 0.0,
                unit = "Hz",
                desc = 'Upper frequecy of the driver in which'
                    'it shall work'),
            'SPL': quantity(
                name = 'Sound Pressure Level',
                value = 0.0,
                unit = "dB",
                desc = 'Mean sound pressure level measured'
                    'at power 1 W and 1m from speaker'),
            'fs': quantity(
                name = 'Resonance frequency',
                value = 0.0,
                unit = "Hz",
                desc = 'Mechanical resonance frequency'
                    'of freely mounted speaker'),
            'Qts': quantity(
                name = 'Total Q factor',
                value = 0.0,
                unit = "Unitless",
                desc = 'inverse of damping ratio of speaker'
                    'lower Q means more control'
                    'Qts<0.4 is usually for drivers for ported'
                    'enclosure, 0.4<Qts>0.7 for closed, and Qts>0.7'
                    'for free-air or infite baffle type'
                    ),
            'Qes': quantity(
                name = 'Electrical Q factor',
                value = 0.0,
                unit = "Unitless",
                desc = 'is the amount of control coming from'
                    'the electrical components of a speaker'
                    '(the voice coil and magnet) which contribute'
                    'to the suspension system'
                    ),
            'EBP': quantity(
                name = 'Efficiency Bandwidth Product',
                value = 0.0,
                unit = "Unitless",
                desc = 'shows the trade-off between efficiency'
                    'and bandwidth of a driver.'
                    'EBP < 50 - use only for a sealed box'
                    'EBP 50 - 100 - can be used in either'
                    'EBP > 100 - vented box only'
                    ),
            }

    exc=20      # excursion limit inmm
    mi=1.1      # Magnetic induction in Tesla
    mf=600      # Magnetic flux in uWebber
    Qms=3.4     # Mechanical Q factor
    # TODO add other
    def calEBP(self):
        if self.par['Qes'].value == 0.0:
            self.par['EBP'].value = 0.0
        else:
            self.par['EBP'].value=float(self.par['fs'].value)/float(self.par['Qes'].value)
        logger.debug(f"calculated EBP is {self.par['EBP'].value}")
        return(self.par['EBP'].value)
    def key_as_short_name(self):
        for key, val in self.par.items():
            val.short_name=key

    def save_to_file(self, filename=""):
        """save speakers data to .ini file
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
                'producer': self.producer,
                'model': self.model,
                'description': self.description,
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
        FILETOREAD = 'speakers/Visaton_W200SC8OHM.ini'
        rspeak = configparser.ConfigParser()
        rspeak.read(FILETOREAD)
        logger.debug(f"readed file: {FILETOREAD}")
        logger.debug(f"sections in file: {rspeak.sections()}")
        for section in rspeak.sections():
            if section == "general":
                self.producer = rspeak[section]['producer']
                self.model = rspeak[section]['model']
                self.description = rspeak[section]['description']
            else:
                if section in self.par:
                    self.par[section].value=rspeak[section]['value']
                    self.par[section].unit=rspeak[section]['unit']
                    logger.debug(f"section {section} readed from file")
                else:
                    logger.warning(
                            f"unknown section: {section} in {FILETOREAD}"
                            )
        logger.debug("end of reading speaker config file")

    
if __name__=='__main__':
    logger.setLevel=(logging.DEBUG)
    spkr = Speaker()
    spkr.read_from_file()
    print(f"speaker producer from file: {spkr.producer}")
    print(f"speaker rated power from file: {spkr.par['r_pow'].value}")
   # spkr.par['fs'].value=27.0
   # spkr.par['Qes'].value=0.32
   # spkr.save_to_file()
   # visaton=Speaker("Visaton")
   # for key, val in visaton.par.items():
   #     print(key, val)
   # visaton.key_as_short_name()
   # print(f"long name: {visaton.par['z'].name}, "
   #       f"short name: {visaton.par['z'].short_name}")
   # visaton.par['fs'].value=27.0
   # visaton.par['Qes'].value=0.32
   # print (visaton.calEBP())
