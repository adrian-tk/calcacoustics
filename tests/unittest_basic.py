#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import logging
#uncomment next line for more info about testing
#logging.basicConfig(level=logging.DEBUG)
import convert
import quantity
import speaker
import enclosure
import csv

FILEWITHTESTDATA="./testdata.csv"

def some_val(a):
    match str(type(a))[8:-2]:
        case "str":
            logging.debug("some_val return string")
            return "satan"
        case "float":
            logging.debug("some_val return float")
            return 666.0
        case "float":
            logging.debug("some_val return int")
            return 666
        case other:
            logging.error("some_val has no such type")
            return a
        
        


logging.debug("================start=testing=procedure=============")
testdata=[]
with open(FILEWITHTESTDATA, "r") as file:
    csvreader=csv.reader(file)
    for row in csvreader:
        testdata.append(row)
    logging.debug(f"loaded {len(testdata)} lines from {FILEWITHTESTDATA}")

del testdata[:2]

def allunit(testdata):
    allunitset=set()
    for line in testdata:
            allunitset.add(line[1])
            allunitset.add(line[3])
    allunitlist=list(allunitset)
    allunitlist.remove("")
    logging.debug(f"list of complete unit to test: {allunitlist}")
    return list(allunitlist)       

def unitlist(testdata, iunit):
    """list unit to convert from testdata
    looking for any unit at line with iunit""" 
    unitset=set()
    for line in testdata:
        if line[1]==iunit: 
            unitset.add(line[3])
        if line[3]==iunit: 
            unitset.add(line[1])
    logging.debug(f"list of unit to convert: {unitset}")
    return list(unitset)       

def searchtd(testdata, cfrom, cto):
    cinput=[]
    coutput=[]
    for line in testdata:
        if line[1]==cfrom and line[3]==cto:
            cinput.append(line[0])
            coutput.append(line[2])
        if line[3]==cfrom and line[1]==cto:
            cinput.append(line[2])
            coutput.append(line[0])
    return (cinput, coutput)

class TestConversion(unittest.TestCase):

    def test_conversion(self):
        for aunit in allunit(testdata): #all unit to test
            for u in unitlist(testdata, aunit):
                logging.debug(f"+++++testing from {aunit} to {u}")

                (inputval, outputval)=searchtd(testdata, aunit, u)
                for i in range(0, len(inputval)):
                    with self.subTest(i=i):
                        #shall return this same value
                        logging.debug(f"check: {inputval[i]} {aunit} = {inputval[i]} {aunit}")
                        self.assertEqual(convert.convert(float(inputval[i]), aunit, aunit),
                                         float(inputval[i]))
                        #shall convert input value to output
                        logging.debug(f"check: {inputval[i]} {aunit} = {outputval[i]} {u}")
                        self.assertEqual(convert.convert(float(inputval[i]), aunit, u),
                                         float(outputval[i]))

class TestQuantity(unittest.TestCase):
    def setUp(self):
        self.q=quantity.quantity()
        logging.debug("object of quantity type created")

    def test_default(self):
        self.assertEqual(self.q.name, '')
        self.assertEqual(self.q.value, 0.0 )
        self.assertEqual(self.q.unit, '')
        self.assertEqual(self.q.desc, '')
        self.assertEqual(self.q.short_name, '')
        logging.debug("default values tested")

    def test_getval(self):
        self.q.value=1000
        self.q.unit="l"
        self.assertEqual(self.q.getval("l"), 1000)
        self.assertEqual(self.q.getval("m3"), 1.0)
        logging.debug("getval tested")

    def test_setval(self):
        self.q.setval(50, "l")
        self.assertEqual(self.q.value, 50)
        self.assertEqual(self.q.unit, "l")
        logging.debug("setval tested")

    def test_convert(self):
        self.q.value=1000
        self.q.unit="l"
        self.q.convert("l")
        self.assertEqual(self.q.value, 1000)
        self.assertEqual(self.q.unit, "l")
        self.q.convert("m3")
        self.assertEqual(self.q.value, 1)
        self.assertEqual(self.q.unit, "m3")
        self.q.setval(500, "l")
        self.assertEqual(self.q.getval("m3"), 0.5)
        logging.debug("convert tested")
    def test_dictionary(self):
        #put a attributes to test here
        names=['name', 'short_name', 'value', 'unit', 'desc']

        dic=self.q.dictionary()
        for name in names:
            with self.subTest(i=name):
                #check def value
                obj=getattr(self.q, name)
                self.assertEqual(obj, dic[name])
                #set some val, and check again
                setattr(self.q, name, some_val(obj))
                obj=getattr(self.q, name)
                dic=self.q.dictionary()
                self.assertEqual(obj, dic[name])
        logging.debug("dictionary tested")


class TestSpeaker(unittest.TestCase):
    def setUp(self):
        self.s=speaker.Speaker()
        logging.debug("object of speaker type created")

    def test_default(self):
        for key, y in self.s.par.items():
            with self.subTest(x=key):
                #check if default is 0
                self.assertEqual(self.s.par[key].value, 0.0,
                                 f"default value in {key} is not 0.0")
                #check if name and desc are not empty
                self.assertNotEqual(self.s.par[key].name, "",
                                    f"name in {key} is empty")
                self.assertEqual(self.s.par[key].short_name, "")
                self.assertNotEqual(self.s.par[key].desc, "",
                                    f"description in {key} is empty")
        logging.debug("default values tested")

    def test_key_as_short_name(self):
        for key, val in self.s.par.items():
            with self.subTest(x=key):
                self.assertEqual(self.s.par[key].short_name, "")
        self.s.key_as_short_name()
        for key, val in self.s.par.items():
            with self.subTest(x=key):
                self.assertEqual(self.s.par[key].short_name, key)

class TestEnclosures(unittest.TestCase):
    def setUp(self):
        self.e=enclosure.Enclosure()
        logging.debug("object of enclosure type created")

    def test_default(self):
        #check if all val are present and set to zero
        names=['Vs', 'we', 'he', 'de', 'thick',
               'we','he','de','v_int','stuffed']
        for name in names:
            with self.subTest(i=name):
                obj=getattr(self.e, name)
                self.assertEqual(getattr(obj, "value"), 0.0,
                                 f"{name} is not zero")
        logging.debug("default values tested")

    def test_int_dim(self):
        self.e.thick.setval(1, 'cm')
        ans=self.e.int_dim(1)
        self.assertEqual(ans, 0.98)
        self.e.thick.setval(10, 'cm')
        ans=self.e.int_dim(1)
        self.assertEqual(ans, 0.8)

    def test_int_vol(self):
        self.e.thick.setval(1.6, 'cm')
        self.e.we.setval(20, 'cm')
        self.e.he.setval(1.2, 'm')
        self.e.de.setval(100, 'mm')
        self.e.int_vol()
        self.assertAlmostEqual(self.e.v_int.getval('l'), 13.343232)





if __name__=='__main__':
    unittest.main()
