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
    section: name of the solver module to work with
    item: name of some value
    action: set, get, answer, confirm, calculate, error
    value: used for set, answer or error
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
    logger.debug("imported loggers in interface")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("Maybe You shall be in env?")

# add module here
from solver import speaker
from solver import cable
#TODO: test script

class Version():
    """class for versioning of interface"""
    def __init__(self):
        self.version = 0.1
    def get_version(self):
        return(self.version)

class Interface():

    def __init__(
            self,
            sections = {
                # add solvers here
                'speaker': speaker.Speaker(),
                'cable': cable.Cable(),
                }
            ):
        # dict for holding interfaces
        self.sections = sections
        self.version="0.2" # to REMOVE
        self.sp=speaker.Speaker() # to REMOVE
        self.sp.key_as_short_name()
        self.cable=cable.Cable()
        # for version etc.
        self.sections['interface'] = self
        logger.debug(
                f"interfaces initialized: {list(self.sections.keys())}"
                )
        # dicts for holding query form gui
        self.query={}
        # dicts for preparing andswer to gui
        self.answer={}

    def ask(self, query):
        """get query from GUI or other sources"""
        self.query = query
        logcom.debug(f"solver input: {self.query}")
        self.convey()
        logcom.debug(f"solver output: {self.answer}")
        return self.answer

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

    def solver_attribute(self, attr):
        match self.query['action']:
            case "get":
                self.answer['action'] = 'answer'
                if hasattr(self.section(), attr):
                    self.answer['value'] = getattr(self.section(), attr)
                elif attr in self.section().par:
                    self.answer['value'] = self.section().par[attr].value
                else:
                    logger.error(f"can't get attribute {attr}")
            case "set":
                self.answer['action'] = 'confirm'
                if hasattr(self.section(), attr):
                    setattr(self.section(), attr, self.query['value'])
                    self.answer['value'] = getattr(self.section(), attr)
                elif attr in self.section().par:
                    self.section().par[attr].value = self.query['value']
                    self.answer['value'] = self.section().par[attr].value
                else:
                    logger.error(f"can't set attribute {attr}")
            case "calculate":
                return (f"There is nothing to calculate in "
                    f"attr. {item(data)} in {data}")
            case "answer":
                logger.error(f"answer {data} shall not be sent do solver")
            case _:
                logger.error(f"unknown action in: {data}")

    def get_list_quantities(data):
        """old"""
        match data['action']:
            case "get":
                for key, val in self.sp.par.items():
                    ans[key]=section(data).par[key].dictionary()
                logcom.debug(f"solver sent to GUI: {ans}")
            case _:
                logger.error(
                        f"there is no {data['action']} for list_quantities"
                        )
                ans = None
        return(ans)
        
    def section(self):
        """try to connect section from qurey to section object

        returns: object from sections dictionary
        """
        ans = None
        for key, val in self.sections.items():
            if key == self.query['section']:
                ans = val
                self.answer['section']=key
        if ans == None:
            logger.error(
                    f"No solver initialized for {self.query['section']}"
                    )
        return(ans)

    def convey(self):
        """get data from query and convey them to attribute or method"""
        match self.query["item"]:
            case "version":
                self.answer["item"]=self.query["item"]
                self.solver_attribute("version")
            case "name":
                self.answer["item"]=self.query["item"]
                self.solver_attribute("name") 
            case "list_quantities":
                ans={}
                for key, val in self.section().par.items():
                    ans[key]=self.section().par[key].dictionary()
                logcom.debug(f"solver send to GUI: {ans}")
                return(ans)
            case "file.ini":
                self.section().read_from_file(self.query['value'])
                logger.debug("read ini file")
                #data['action'] = 'answer'
                #return data

            case _:
                if self.query["item"] in self.section().par:
                    self.answer["item"]=self.query["item"]
                    self.solver_attribute(self.query['item'])
                
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
    if True:
        import logging
        logging.basicConfig(level="DEBUG")
        logger.setLevel(level="DEBUG")
        logcom.setLevel(level="DEBUG")
        
        inf=Interface()
        query = {
            "section": "speaker",
            "item": "file.ini",
            "action": "get",
            "value": "d",
        }
        print(inf.ask(query))

    # full test from unittest in tests directory
    if False:
        import unittest
        from tests import unittest_interface
        suite = unittest.TestSuite()
        suite.addTest(
                unittest.TestLoader().loadTestsFromModule(
                    unittest_interface
                )
        )
        unittest.TextTestRunner(verbosity=2).run(suite)
