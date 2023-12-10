import sys
sys.path.append("..")
import common.quantity as q


class Quant (q.quantity):
    """ adding calculate attribute to quantity"""

    def __init__(self, *args, calculate = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate = calculate

#only for fast testing purpose
if __name__ == "__main__":
    val = Quant(234, "kg", "mass", "some values", "m", calculate = True)
    print(str(val.dictionary()).replace(", ", ",\n"))
