import logging
logger = logging.getLogger(__name__)

# different places to import from
try:
    from common import convert
except:
    # impoort from local directory
    import convert

class quantity:
    def __init__(self,
                 value=0.0,
                 unit="",
                 name='',
                 desc='',
                 short_name=''):
        self.name=name
        self.value=value
        self.unit=unit
        self.desc=desc
        self.short_name=short_name
    def getval(self, unit):
        return convert.convert(self.value, self.unit, unit)
    def setval(self, value, unit):
        self.value=value
        self.unit=unit
    def convert(self, unit):
        logger.debug(f"old value {self.value} {self.unit}")
        self.value=convert.convert(self.value, self.unit, unit)
        self.unit=unit
        logger.debug(f"new value {self.value} {self.unit}")
        return self.value
    def dictionary(self, to_rem=()):
        """change values do dictionary

        as parameter tuple of values do remove from dic
        return dictionary
        """
        """
        dic={
             "name": self.name,
             "short_name": self.short_name,
             "value": self.value,
             "unit": self.unit,
             "desc": self.desc,
             }
             """
        dic = self.__dict__
        for key in to_rem:
            del dic[key]
        return dic

    def __str__(self):
        return (f"{self.name} ({self.short_name})is: "
                f"{self.value} {self.unit} "
                f"\n{self.desc}")
    
if __name__=="__main__":
    logger.setLevel(logging.DEBUG)
    volume=quantity()
    volume.name="enclosure"
    volume.value=10
    volume.unit="l"
    volume.desc="this is volume of some box or something else"
    volume.short_name="vol"
    print(volume)
    volume.convert("m3")
    print(volume.dictionary())
    print(volume.dictionary(('desc',)))
