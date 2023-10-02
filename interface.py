"""interface between GUI and solver
gets python dict as input and output"""

import logging

#TODO: test script

class Interface():
    version="0.1"

    def speaker(self, val):
        match val:
            case "list_quantities":
                ans={"power": "dużo", "force": "mało"}
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

