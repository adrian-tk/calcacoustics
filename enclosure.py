# import logging
# import logging stuff at first
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

import quantity as q

class Enclosure:

    def __init__(self):
        logger.debug("Object of SealedEnclosure created")

        self.Vs=q.quantity(name='internal volume of enclosure',
                     value=0.0,
                     unit='l',
                     desc="internal volume for calculation "
                          "with volume adj acc to speaker "
                          "volume, stuff, etc.")

        self.we=q.quantity(name='external width of enclosure',
                      value=0.0,
                      unit="m",
                      desc="external width of enclosure")
        self.he=q.quantity(name='external height of enclosure',
                      value=0.0,
                      unit="m",
                      desc="external height of enclosure")
        self.de=q.quantity(name='external depth of enclosure',
                      value=0.0,
                      unit="m",
                      desc="external depth of enclosure")
        self.thick=q.quantity(name='thickness of board',
                      value=0.0,
                      unit="m",
                      desc="thickness of matierial for box produce")
        self.wi=q.quantity(name='internal width of enclosure',
                      value=0.0,
                      unit="m",
                      desc="internal width of enclosure")
        self.hi=q.quantity(name='internal height of enclosure',
                      value=0.0,
                      unit="m",
                      desc="internal height of enclosure")
        self.di=q.quantity(name='internal depth of enclosure',
                      value=0.0,
                      unit="m",
                      desc="internal depth of enclosure")
        self.v_int=q.quantity(name='raw internal volume of enclosure',
                      value=0.0,
                      unit="l",
                      desc="volume calculated from internal dimensions")
        self.stuffed=q.quantity(name='percentage of stufffed',
                      value=0.0,
                      unit="%",
                      desc="how much material is stuffed into enclosure "
                           "0 is none, 100 is full")
    def int_dim(self, ext_x: float) -> float:
        """calculate internal box linear dimension
        internal value is external - 2 * thickness"""
        return ext_x-2*self.thick.getval('m')

    def int_vol(self) -> float:
        """calculate internal volume of empty box"""
        self.wi.setval(self.int_dim(self.we.getval("m")), "m")
        self.hi.setval(self.int_dim(self.he.getval("m")), "m")
        self.di.setval(self.int_dim(self.de.getval("m")), "m")
        self.v_int.setval(self.wi.getval("m")*
                          self.hi.getval("m")*
                          self.di.getval("m")*1000, "l")
        logger.debug(f"volume from internal dimension: "
                      f"{self.v_int.getval('l'):.5} l")
        return(self.v_int)
    """
    def stuff(self):
        st_wage=0.15        #whent 100% volume is increased 15%
        self.Vs = (self.stuffed/100*st_wage+1)*self.v_int
        return self.Vs
        """

if __name__=="__main__":
    """only for fast testing"""
    box=Enclosure()
    box.we.setval(300, "mm")
    box.he.setval(1200, "mm")
    box.de.setval(180, "mm")
    box.thick.setval(16, "mm")
    print(box.int_vol())

