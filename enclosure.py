import logging
import quantity as q

class SealedEnclosure:
    def __init__(self):
        logging.debug("Object of SealedEnclosure created")

    Vs=q.quantity(name='internal volume of enclosure',
                 value=0.0,
                 unit='l',
                 desc="internal volume for calculation "
                      "with volume adj acc to speaker "
                      "volume, stuff, etc.")

    we=q.quantity(name='external width of enclosure',
                  value=0.0,
                  unit="m",
                  desc="external width of enclosure")
    he=q.quantity(name='external height of enclosure',
                  value=0.0,
                  unit="m",
                  desc="external height of enclosure")
    de=q.quantity(name='external depth of enclosure',
                  value=0.0,
                  unit="m",
                  desc="external depth of enclosure")
    thick=q.quantity(name='thickness of board',
                  value=0.0,
                  unit="m",
                  desc="thickness of matierial for box produce")
    wi=q.quantity(name='internal width of enclosure',
                  value=0.0,
                  unit="m",
                  desc="internal width of enclosure")
    hi=q.quantity(name='internal height of enclosure',
                  value=0.0,
                  unit="m",
                  desc="internal height of enclosure")
    di=q.quantity(name='internal depth of enclosure',
                  value=0.0,
                  unit="m",
                  desc="internal depth of enclosure")
    v_int=q.quantity(name='raw internal volume of enclosure',
                  value=0.0,
                  unit="l",
                  desc="volume calculated from internal dimensions")
    stuffed=q.quantity(name='percentage of stufffed',
                  value=0.0,
                  unit="%",
                  desc="how much material is stuffed into enclosure "
                       "0 is none, 100 is full")
    def int_dim(self, ext_x):
        return ext_x-2*self.thick.getval('m')

    def int_vol(self):
        self.wi.setval(self.int_dim(self.we.getval("m")), "m")
        self.hi.setval(self.int_dim(self.he.getval("m")), "m")
        self.di.setval(self.int_dim(self.de.getval("m")), "m")
        self.v_int.setval(self.wi.getval("m")*
                          self.hi.getval("m")*
                          self.di.getval("m")*1000, "l")
        logging.debug(f"V from internal dimension: {self.v_int.getval('l'):.5} l")
        return(self.v_int)
    """
    def stuff(self):
        st_wage=0.15        #whent 100% volume is increased 15%
        self.Vs = (self.stuffed/100*st_wage+1)*self.v_int
        return self.Vs
        """

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    box=SealedEnclosure()
    box.we.setval(3, "m")
    box.he.setval(2, "m")
    box.de.setval(1, "m")
    box.int_vol()

