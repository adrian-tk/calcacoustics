import logging
import convert

class quantity:
    def __init__(self, value=0.0, unit="", name='', desc=''):
        self.name=name
        self.value=value
        self.unit=unit
        self.desc=desc
    def getval(self, unit):
        return convert.convert(self.value, self.unit, unit)
    def setval(self, value, unit):
        self.value=value
        self.unit=unit
    def convert(self, unit):
        logging.debug(f"old value {self.value} {self.unit}")
        self.value=convert.convert(self.value, self.unit, unit)
        self.unit=unit
        logging.debug(f"new value {self.value} {self.unit}")
        return self.value
    def __str__(self):
        return (f"{self.name} is: {self.value} {self.unit} "
                f"\n{self.desc}")


    
if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    volume=quantity()
    volume.name="enclosure"
    volume.value=10
    volume.unit="l"
    volume.desc="this is volume of some box or something else"
    print(volume)
    volume.convert("m3")
