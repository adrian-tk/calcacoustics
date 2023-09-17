import unittest
import sys
sys.path.append("..")
import logging
#uncomment next line for more info about testing
logging.basicConfig(level=logging.DEBUG)
import convert
import csv

FILEWITHTESTDATA="./testdata.csv"

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


if __name__=='__main__':
    unittest.main()
