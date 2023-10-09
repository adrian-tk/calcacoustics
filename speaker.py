import logging
from quantity import quantity 

class Speaker:

    def __init__(self, name="default speaker"):
        self.name=name
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
                    'it can work'),
            }

    u_fr=6000   # Upper frequency response
    SPL=88      # Mean sound pressure level (1W/1m) in dB
    exc=20      # excursion limit inmm
    fs=27.0     # Resonanse frequency in Hz
    mi=1.1      # Magnetic induction in Tesla
    mf=600      # Magnetic flux in uWebber
    Qms=3.4     # Mechanical Q factor
    Qes=0.32    # Electricat Q factor
    Qts=0.29    # Total Q factor
    Vas=63      # Equivalent volume in l
    EBP=0.0     # Efficiency Bandwidht Product
    # TODO add other
    def calEBP(self):
        self.EBP=self.fs/self.Qes
        logging.debug(f"calculated EBP is {self.EBP}")
    def key_as_short_name(self):
        for key, val in self.par.items():
            val.short_name=key

        
    
    
if __name__=='__main__':
    visaton=Speaker("Visaton")
    for key, val in visaton.par.items():
        print(key, val)
    visaton.key_as_short_name()
    print(f"long name: {visaton.par['z'].name}, "
          f"short name: {visaton.par['z'].short_name}")
