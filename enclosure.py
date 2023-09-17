import logging
from textwrap import dedent

class SealedEnclosure:
    def __init__(self):
        logging.debug("Object of SealedEnclosure created")
    Vs=0        # internal volume of box in l
    ext_w=0.0   # external width of box in m
    ext_h=0.0   # external height of box in m
    ext_d=0.0   # external depht of box in m
    thick=0.0   # thickness of box material
    int_w=0.0   # internal width of box in m
    int_h=0.0   # internal height of box in m
    int_d=0.0   # internal depth of box in m
    v_int=0.0   # internal raw volume
    stuffed=100  # percentage of stuffed
    def int_dim(self, ext_x):
        return ext_x-2*self.thick

    def int_vol(self):
        self.int_w=self.int_dim(self.ext_w)
        self.int_h=self.int_dim(self.ext_h)
        self.int_d=self.int_dim(self.ext_d)
        self.v_int=self.int_w*self.int_h*self.int_d*1000.0
        logging.debug(f"V from internal dimension: {self.v_int:.4} l")
        return(self.v_int)
    def stuff(self):
        st_wage=0.15        #whent 100% volume is increased 15%
        self.Vs = (self.stuffed/100*st_wage+1)*self.v_int
        logging.debug(f"Vs with stuffed internal: {self.Vs:.4} l")
        return self.Vs


