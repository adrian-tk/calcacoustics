"""interface between GUI and solver
gets json file as input and output"""

import json
import logging

#TODO: test script

class Interface():
    version="0.1"

    def speaker(self, val):
        match val:
            case "list_quantities":
                ans={"power": "dużo", "force": "mało"}
                logging.debug(f"json send to GUI: {ans}")
                return(json.dumps(ans))
            case _:
                logging.error(f"there is no {val} value "
                              "for {val} values that GUI sent")

    def send(self, data):
        dec=json.loads(data)
        logging.debug(f"json get from GUI: {dec}")
        for key, val in dec.items():
            match key:
                case "speaker":
                    return (self.speaker(val))
                case _:
                    logging.error(f"there is no {key} value GUI sent")

