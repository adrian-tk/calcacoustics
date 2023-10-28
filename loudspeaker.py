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

import enclosure 
import speaker

box=enclosure.SealedEnclosure()
speaker=speaker.Speaker()
box.Vs=5
box.ext_w=0.15
box.ext_h=1.2
box.ext_d=0.30
box.thick=0.016
box.int_vol()
#box.stuff()
speaker.calEBP()

