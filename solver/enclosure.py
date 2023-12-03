"""Provide calculations and values for enclosure.

This module allows the user to work with enclosure.

Examples:
    >>> import enclosure
    TODO >>> speaker.calEBP(1.0, 1.0)
    1.0

Contains the following functions:
- `calEBP(Qes, fs)` returns EPB
"""
import sys
sys.path.append('../')

# import logging stuff at first
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

import common.quantity as q

class Quant (q.quantity):
    # atrr for locking of values
    # locked values will not be calculated
    locked = False
    pass

class Enclosure:

    def __init__(self):
        logger.debug("Object of SealedEnclosure created")

        self.Vs=Quant(name='internal volume of enclosure',
                     value=0.0,
                     unit='l',
                     desc="internal volume for calculation "
                          "with volume adjusted acc. to speaker "
                          "volume, BR port, stuff, etc.")

        self.we=Quant(name='external width of enclosure',
                      value=0.0,
                      unit="m",
                      desc="external width of enclosure")
        self.he=Quant(name='external height of enclosure',
                      value=0.0,
                      unit="m",
                      desc="external height of enclosure")
        self.de=Quant(name='external depth of enclosure',
                      value=0.0,
                      unit="m",
                      desc="external depth of enclosure")
        self.thick=Quant(name='thickness of board',
                      value=0.0,
                      unit="m",
                      desc="thickness of matierial for box produce")
        self.wi=Quant(name='internal width of enclosure',
                      value=0.0,
                      unit="m",
                      desc="internal width of enclosure")
        self.hi=Quant(name='internal height of enclosure',
                      value=0.0,
                      unit="m",
                      desc="internal height of enclosure")
        self.di=Quant(name='internal depth of enclosure',
                      value=0.0,
                      unit="m",
                      desc="internal depth of enclosure")
        self.v_int=Quant(name='raw internal volume of enclosure',
                      value=0.0,
                      unit="l",
                      desc="volume calculated from internal dimensions")
        self.stuffed=Quant(name='percentage of stufffed',
                      value=0.0,
                      unit="%",
                      desc="how much material is stuffed into enclosure "
                           "0 is none, 100 is full")
    def int_dim(self):
        """calculate internal box linear dimension

        internal value is external - 2 * thickness
        be aware, that ext_dim and thick shall has the same unit.
        """

        self.wi.setval(
                (self.we.getval('m')-2*self.thick.getval('m')),
                'm'
                )
        self.di.setval(
                (self.de.getval('m')-2*self.thick.getval('m')),
                'm'
                )
        self.hi.setval(
                (self.he.getval('m')-2*self.thick.getval('m')),
                'm'
                )


    def int_box_vol(self):
        """calculate internal volume of empty box"""
        self.int_dim()
        self.v_int.setval(self.wi.getval("m")*
                          self.hi.getval("m")*
                          self.di.getval("m")*1000, "l")
        logger.debug(f"volume from internal dimension: "
                      f"{self.v_int.getval('l'):.5} l")
    """
    def stuff(self):
        st_wage=0.15        #whent 100% volume is increased 15%
        self.Vs = (self.stuffed/100*st_wage+1)*self.v_int
        return self.Vs
        """

if __name__=="__main__":
    """only for fast testing"""
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger("fast_test")
    logger.setLevel(logging.DEBUG)
    box=Enclosure()
    box.we.setval(300, "mm")
    box.he.setval(1200, "mm")
    box.de.setval(180, "mm")
    box.thick.setval(16, "mm")
    box.int_box_vol()
    print(box.v_int.getval('l'))
