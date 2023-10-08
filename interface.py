"""interface between GUI and solver
gets python dict as input and output
example looks like:
    {
    section: speaker,
    item: name,
    action: set
    value: 5
    }
where:
    section: name of function to work with
    item: name of some value
    action: set, get, answer
    value: used for set or answer
any additional value possible
"""

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

    def speaker(self, data):
        ans={}
        match data["item"]:
            case "list_quantities":
                for key, val in self.sp.par.items():
                    ans[key]=self.sp.par[key].dictionary()
                logging.debug(f"calc send to GUI: {ans}")
                return(ans)
            case "name":
                if data["action"] == "get":
                    data["action"] = "answer"
                    data["value"] = self.sp.name
                    logging.debug(f"calc send to GUI: {data}")
                    return(data)
                elif data["action"] == "set":
                    data["action"] = "answer"
                    self.sp.name = data["value"]
                    logging.debug(f"calc send to GUI: {data}")
                    logging.debug(f"calc set name to: {data['value']}")
                    return(data)
                else:
                    logging.error(f"wront action")
                    return("error")
            case _:
                logging.error(f"there is no {val} value "
                              "for {val} values that GUI sent")

    def send(self, data):
        logging.debug(f"calc get from GUI: {data}")
        match data["section"]:
            case "speaker":
                return (self.speaker(data))
            case _:
                logging.error(f"there is no {val} for section GUI sent")

if __name__=="__main__":
    inf=Interface()
    print(inf.send({
        "section": "speaker",
        "item": "name",
        "action": "get",
        "value": None,
        }))
