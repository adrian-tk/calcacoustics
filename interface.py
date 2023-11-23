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
    from solver.logger import logging
    from solver.logger import logger
    from solver.logger import logcom
    # set this logger as a child of main logger
    logger = logger.getChild(__name__)
    logcom = logcom.getChild(__name__)
    logger.debug("imported loggers")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("Maybe You shall be in env?")


#import speaker
from solver import speaker
#TODO: test script

class Interface():

    def __init__(self):
        self.version="0.1"
        logger.debug("interface initialised")
        self.sp=speaker.Speaker()
        logger.debug("interface for speaker")
        self.sp.key_as_short_name()

    def simple_attr(self, data, case):
        """get data as dictrionary and create answer as dictionary
        for attributes in speaker data
        """
        if data["action"] == "get":
            data["action"] = "answer"
            try:
                data["value"] = getattr(self.sp, case)
            except Exception as err:
                logger.error("cant find atribute {case}")
                logger.error(err)
            #data["value"] = self.sp.name
            logcom.debug(f"calc send to GUI: {data}")
            return(data)
        elif data["action"] == "set":
            data["action"] = "answer"
            try:
                setattr(self.sp, case, data['value'])
            except Exception as err:
                logger.error("cant find atribute {case}")
                logger.error(err)
            #self.sp.name = data["value"]
            logcom.debug(f"calc send to GUI: {data}")
            return(data)
        else:
            logger.error(f"wrong action")
            return("error")

    def speaker(self, data):
        ans={}
        match data["item"]:
            case "version":
                data['action'] = 'answer'
                data['value'] =  str(self.version)
                logcom.debug(f"calc send to GUI: {data}")
                return (data)
                
            case "list_quantities":
                for key, val in self.sp.par.items():
                    ans[key]=self.sp.par[key].dictionary()
                logcom.debug(f"calc send to GUI: {ans}")
                return(ans)

            case "name":
                return (self.simple_attr(data, data["item"]))
            
            case "producer":
                return (self.simple_attr(data, data["item"]))

            case "model":
                return (self.simple_attr(data, data["item"]))

            case "speaker.ini":
                self.sp.read_from_file(data['value'])
                logger.debug("read ini file")
                data['action'] = 'answer'
                return data
                """
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
                    """
            case _:
                if data["item"] in self.sp.par:
                    if data["action"] == "set":
                        data["action"] = "answer"
                        #setattr(self.sp, data["item"], data["value"])
                        if data['value']=="": data['value']=0
                        self.sp.par[data["item"]].value = float(data["value"])
                       # print(self.sp.par[data["item"]].value)
                        logcom.debug(f"calc send to GUI: {data}")
                    elif data["action"] == "get":
                        data["action"] = "answer"
                        data['value'] = str(self.sp.par[data["item"]].value)
                        logcom.debug(f"calc send to GUI: {data}")
                        return(data)
                    elif data["action"] == "calculate":
                        data["action"] = "answer"
                        if data["item"] == "EBP":
                            ans=self.sp.setEBP()
                            logger.debug(f"calculate EBP")
                            data["value"] =str(self.sp.par[data["item"]].value)
                            logcom.debug(f"calc send to GUI: {data}")
                            return(data)

                else:
                    logger.error(f"there is no {val} value "
                                  "for {val} values that GUI sent")


    def send(self, data):
        """check to which module shall be directed query, and
        direct it there
        """

        logcom.debug(f"calc get from GUI: {data}")
        match data["section"]:
            case "speaker":
                return (self.speaker(data))
            case _:
                err = (f"there is no {data['section']} " 
                        "for section GUI sent")
                logger.error(err)
                return (err)

if __name__=="__main__":
    logcom.setLevel(logging.DEBUG)
    inf=Interface()
    print(inf.send({
        "section": "speaker",
        "item": "EBP",
        "action": "calculate",
        "value": None,
        }))
