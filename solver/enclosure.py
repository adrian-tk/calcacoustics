"""Provide calculations and values for enclosure.

This module allows the user to work with enclosure.
    ____
   /   /|   x = width of enclosure
  +---+ |   y = depth of enclosure
  | o | |   z = height of enclosure 
 z| O | +   v = volume from box dimensions
  |   |/y
  +---+
    x

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
    # atrribute for locking of values
    # locked values will not be calculated
    locked = False
    def dictionary(self):
        ans = super().dictionary()
        ans.update({'locked': self.locked})
        return(ans)

class Enclosure:

    def __init__(self):
        logger.debug("Object of SealedEnclosure created")

        self.Vs=Quant(name='internal volume of enclosure',
                     value=0.0,
                     unit='l',
                     desc="internal volume for calculation "
                          "with volume adjusted acc. to speaker "
                          "volume, BR port, stuff, etc.")

        self.ext_dims = {'x': Quant(
                            name='ext. width',
                            value=0.0,
                            unit="m",
                            desc="external width of enclosure"),
                        'y': Quant(
                            name='ext depth',
                            value=0.0,
                            unit="m",
                            desc="external depth of enclosure"),
                        'z': Quant(
                            name='ext. height',
                            value=0.0,
                            unit="m",
                            desc="external height of enclosure"),
                        'v': Quant(
                            name='ext. volume',
                            value=0.0,
                            unit="m3",
                            desc="external volume of enclosure "
                                "calculated from box dimensions")
                        }
        self.int_dims = {'x': Quant(
                            name='int. width',
                            value=0.0,
                            unit="m",
                            desc="internal width of enclosure"),
                        'y': Quant(
                            name='int depth',
                            value=0.0,
                            unit="m",
                            desc="internal depth of enclosure"),
                        'z': Quant(
                            name='int. height',
                            value=0.0,
                            unit="m",
                            desc="internal height of enclosure"),
                        'v': Quant(
                            name='int. volume',
                            value=0.0,
                            unit="m3",
                            desc=("internal volume of enclosure" 
                                  "calculated from box dimensions"))
                        }
        self.thick=Quant(name='thickness of board',
                      value=0.0,
                      unit="m",
                      desc="thickness of matierial for box produce")

        self.stuffed=Quant(name='percentage of stufffed',
                      value=0.0,
                      unit="%",
                      desc="how much material is stuffed into enclosure "
                           "0 is none, 100 is full")
    def calc_int_dim(self):
        """calculate internal box linear dimension

        internal value is external - 2 * thickness
        be aware, that ext_dim and thick shall has the same unit.
        """

        for i in ('x', 'y', 'z'):
            self.int_dims[i].setval(
                    self.ext_dims[i].getval('m')-2*self.thick.getval('m'),
                    'm')
            self.int_dims['v'].setval(
                    self.int_dims['x'].getval('m')*
                    self.int_dims['y'].getval('m')*
                    self.int_dims['z'].getval('m')*
                    1000,        # m3 to liters
                    'l'
                    )
        logger.debug(f"volume from internal dimension: "
                      f"{self.int_dims['v'].getval('l'):.5} l")

    def dictionary(self, scope: str) -> dict:
        ans = []
        for key, val in self.ext_dims.items():
            ans.append(val.dictionary())
        for key, val in self.int_dims.items():
            ans.append(val.dictionary())
            ans.append(self.thick.dictionary())
            ans.append(self.Vs.dictionary())

        return(ans)

                    
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
    box.thick.setval(16, "mm")
    box.ext_dims['x'].setval(30, "cm")
    box.ext_dims['y'].setval(15, "cm")
    box.ext_dims['z'].setval(120, "cm")
    box.calc_int_dim()
    print(box.dictionary("all"))

    #box.int_box_vol()
    #print(box.v_int.getval('l'))
