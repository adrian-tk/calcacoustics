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
    action: set, get, answer, calculate
    value: used for set or answer
any additional value possible
"""

#LOGFORMAT="%(levelname)-8s[%(name)s]\
#    [%(filename)s][%(funcName)s] %(message)s"
#LOGFILEFORMAT="%(asctime)s - %(levelname)-8s\
#        [%(name)s][%(filename)s:%(lineno)d]\
#        [%(funcName)s] %(message)s"

#import logging
#logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
#logcom = logging.getLogger(f"calac.com.{__name__}")
#logger = logging.getLogger(f"calac.{__name__}")
try:
    from logger import logging
    from logger import logger
    from logger import logcom
    # set this logger as a child of main logger
    logger = logger.getChild(__name__)
    logcom = logcom.getChild(__name__)
    logger.debug("imported loggers")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("Maybe You shall be in env?")


import speaker
#TODO: test script

class Interface():
    version="0.1"

    def __init__(self):
        self.sp=speaker.Speaker()
        self.sp.key_as_short_name()

    def speaker(self, data):
        ans={}
        match data["item"]:
            case "list_quantities":
                for key, val in self.sp.par.items():
                    ans[key]=self.sp.par[key].dictionary()
                logcom.debug(f"calc send to GUI: {ans}")
                return(ans)
            case "name":
                if data["action"] == "get":
                    data["action"] = "answer"
                    data["value"] = self.sp.name
                    logcom.debug(f"calc send to GUI: {data}")
                    return(data)
                elif data["action"] == "set":
                    data["action"] = "answer"
                    self.sp.name = data["value"]
                    logcom.debug(f"calc send to GUI: {data}")
                    logcom.debug(f"calc set name to: {data['value']}")
                    return(data)
                else:
                    logger.error(f"wrong action")
                    return("error")
            case _:
                if data["item"] in self.sp.par:
                    if data["action"] == "set":
                        data["action"] = "answer"
                        #setattr(self.sp, data["item"], data["value"])
                        if data['value']=="": data['value']=0
                        self.sp.par[data["item"]].value = float(data["value"])
                       # print(self.sp.par[data["item"]].value)
                        logcom.debug(f"calc send to GUI: {data}")
                    elif data["action"] == "calculate":
                        data["action"] = "answer"
                        if data["item"] == "EBP":
                            ans=self.sp.calEBP()
                            logger.debug(f"calculate EBP")
                            data["value"] = ans
                            logcom.debug(f"calc send to GUI: {data}")
                            return(data)

                else:
                    logger.error(f"there is no {val} value "
                                  "for {val} values that GUI sent")


    def send(self, data):
        logcom.debug(f"calc get from GUI: {data}")
        match data["section"]:
            case "speaker":
                return (self.speaker(data))
            case _:
                logger.error(f"there is no {val} for section GUI sent")

if __name__=="__main__":
    inf=Interface()
    print(inf.send({
        "section": "speaker",
        "item": "name",
        "action": "get",
        "value": None,
        }))
