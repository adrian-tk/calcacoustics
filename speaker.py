import logging
import quantity as q

class Speaker:
    name=""
    r_pow=q.quantity(name='rated power',
                     value=0.0,
                     unit='W',
                     desc="A speaker's power rating details "
                     "the amount of power that it can safely handle.") 
    max_pow=q.quantity(name='maximum power',
                     value=0.0,
                     unit='W',
                     desc="Maximum power is the power that the speaker "
                       "can handle for short periods of time without "
                       "being damaged.")
    z=q.quantity(name='nominal impedance',
                     value=0.0,
                     unit='Ohm',
                     desc="nominal impedance is an estimate "
                     "of the minimum impedance for typical "
                     "audio ranges usually 4, 8, or 16 Ohms")
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
    Vas=q.quantity(name='equivalent volume',
                     value=0.0,
                     unit='l',
                     desc="The Vas measurement in litres "
                     "is the size of the ‘imaginary’ box "
                     "which has exactly the same restoring "
                     "force as the suspension of the driver.")
    EBP=0.0     # Efficiency Bandwidht Product
    # TODO add other
    def calEBP(self):
        self.EBP=self.fs/self.Qes
        logging.debug(f"calculated EBP is {self.EBP}")

        
    
    
if __name__=='__main__':
    visaton=Speaker()
    visaton.r_pow.value=75.0
    print(visaton.r_pow)
    visaton.max_pow.value=115
    print(visaton.max_pow)
    visaton.z.value=8
    print(visaton.z)
    visaton.Vas.value=63
    print(visaton.Vas)

