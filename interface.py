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

from importlib import import_module

try:
    from solver.logger import logging
    from solver.logger import logger
    from solver.logger import logcom
    # set this logger as a child of main logger
    logger = logger.getChild(__name__)
    #logger.setLevel(logging.DEBUG)
    logcom = logcom.getChild(__name__)
    logger.debug("imported loggers in interface")
except Exception as err:
    print("Can't import loggers")
    print(err)
    print("Maybe You shall be in env?")

from solver.list_sections import list_sections

class Interface():
    """interface between GUI and solver"""

    def __init__(self, sections:dict = {}):
        if sections == {}:
            for sec in list_sections(hide = None):
                logger.info(f"load section: {sec}")
                secpath = 'solver.sections.' + sec
                sections[sec] = import_module(secpath).CalcBundle()
        # dict for holding interfaces
        self.sections = sections
        # for version etc.
        self.sections['interface'] = self
        logger.debug(
                f"interfaces initialized: {list(self.sections.keys())}"
                )
        # dicts for holding query form gui
        self.query={}
        # dicts for preparing andswer to gui
        self.answer={}
        # list for multiple answers
        self.answers=[]
        # list for update object
        self.update_list = []

    def ask(self, query):
        """get query from GUI or other sources"""

        # empty answers
        self.answers=[]
        self.query = query
        logcom.debug(f"solver input: {self.query}")
        self.convey()
        self.update()
        logcom.debug(f"solver output: {self.answers}")
        return self.answers

    def update(self):
        self.answers.append(self.answer)
        for ans in self.update_list:
            self.answers.append(
                {
                    "section": self.query["section"],
                    "item": ans,
                    "action": "answer",
                    "value": str(self.section().par[ans].value)
                }
            )

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

    def solver_list_quantities(self):
        match self.query['action']:
            case "get":
                self.answer['action'] = 'answer'
                ans={}
                for key, val in self.section().par.items():
                    ans[key]=self.section().par[key].dictionary()
                    #print (ans[key])
                logcom.debug(f"solver send to GUI: {ans}")
                self.answer['value'] = ans
            case _:
                logger.error(f"there is no {self.query['action']} \
                        or {self.query['section']} for list_quantities")
                ans = None

    def solver_list_sections(self):
        if self.query['action'] == 'get' and \
                    self.query['section'] == 'interface':
            self.answer['action'] = 'answer'
            self.answer['section'] = 'interface'
            #ans = list_sections()
            ans = list_sections(hide = None)
            logcom.debug(f"solver send to GUI: {ans}")
            self.answer['value'] = ans
        else:
            logger.error(f"there is no {self.query['action']} \
                    for list_sections")
            ans = None

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
        #logger.debug(f"section to ask: {ans}")
        return(ans)

    def convey(self):
        """get data from query and convey them to attribute or method"""
        match self.query["item"]:
            case "version":
                self.answer["item"]=self.query["item"]
                self.solver_attribute("version")
                logger.debug("solver was asked about version")
            case "name":
                self.answer["item"]=self.query["item"]
                self.solver_attribute("name") 
                logger.debug("solver was asked about name")
            case "list_quantities":
                self.answer["item"]=self.query["item"]
                self.solver_list_quantities()
                logger.debug("solver was asked about list quantities")
            case "list_sections":
                self.answer["item"]=self.query["item"]
                self.solver_list_sections()
                logger.debug("solver was asked about list sections")
            case "file.ini":
                self.section().read_from_file(self.query['value'])
                logger.debug("read ini file")
                logger.debug("solver was asked about ini file")
                #data['action'] = 'answer'
                #return data
            case "input_dir":
                self.answer["item"]=self.query["item"]
                self.solver_attribute("")
                logger.debug("solver was asked about input directory")
                logger.debug("read ini file")
                logger.debug("solver was asked about ini file")
                #data['action'] = 'answer'
                #return data
            case _:
                try:
                    if self.query["item"] in self.section().par:
                        logger.debug(f"solver was asked about "
                                f"{self.query['item']} parameter")
                        self.answer["item"]=self.query["item"]
                        self.solver_attribute(self.query['item'])
                        self.update_list = self.section().recalculate(
                                self.query['item'])
                except Exception as err:
                    logger.exception(f"can't get {self.query['item']} item")
                    
if __name__=="__main__":
    if False:
    #if False:
        inf=Interface()
        query = {
            "section": "interface",
            "item": "list_sections",
            "action": "get",
            "value": "5",
        }
        ans = (inf.ask(query))
        print("answer:")
        print(ans)

        query = {
            "section": "template",
            "item": "list_quantities",
            "action": "get",
            "value": "5",
        }
        ans = (inf.ask(query))
        print("answer:")
        print(ans)

    else:
        # full test from unittest in tests directory
        import unittest
        from tests import unittest_interface_template
        suite = unittest.TestSuite()
        suite.addTest(
                unittest.TestLoader().loadTestsFromModule(
                    unittest_interface_template
                )
        )
        unittest.TextTestRunner(verbosity=2).run(suite)
