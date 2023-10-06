"""interface between GUI and solver
gets python dict as input and output"""

LOGFORMAT="%(levelname)-8s[%(name)s]\
    [%(filename)s][%(funcName)s] %(message)s"
LOGFILEFORMAT="%(asctime)s - %(levelname)-8s\
        [%(name)s][%(filename)s:%(lineno)d]\
        [%(funcName)s] %(message)s"

import logging
logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)

import logging
import speaker
#TODO: test script

class Interface():
    version="0.1"

    def __init__(self):
        self.sp=speaker.Speaker()

    def speaker(self, val):
        match val.split()[0]:
            case "list_quantities":
                #ans={"power": "dużo", "force": "mało"}
                ans={}
                for key, val in self.sp.par.items():
                    ans[key]=self.sp.par[key].dictionary()
                logging.debug(f"calc send to GUI: {ans}")
                return(ans)
            case "name":
                if " " in val:
                    self.sp.name=val.split()[1]
                ans={}
                ans["name"]=self.sp.name
                logging.debug(f"calc send to GUI: {ans}")
                return(ans)
            case _:
                logging.error(f"there is no {val} value "
                              "for {val} values that GUI sent")

    def send(self, data):
        logging.debug(f"calc get from GUI: {data}")
        for key, val in data.items():
            match key:
                case "speaker":
                    return (self.speaker(val))
                case _:
                    logging.error(f"there is no {key} value GUI sent")

if __name__=="__main__":
    inf=Interface()
    #print(inf.send({"speaker": "list_quantities"}))
    print(inf.send({"speaker": "list_quantities"}))
