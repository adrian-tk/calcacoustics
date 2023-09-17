LOGFORMAT="%(levelname)-8s[%(name)s][%(filename)s][%(funcName)s] %(message)s"
LOGFILEFORMAT="%(asctime)s - %(levelname)-8s[%(name)s][%(filename)s:%(lineno)d][%(funcName)s] %(message)s"

import logging
logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
#logging.basicConfig(format=LOGFORMAT, level=logging.INFO)
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

