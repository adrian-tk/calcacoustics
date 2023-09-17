import logging

class Speaker:
    name="example speaker"
    r_power=75  # rated power in Watt
    max_power=115   #maximum power in Watt
    z=8         # Nominal impedance in Ohm
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

        
    
    

