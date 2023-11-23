#!../env/bin/python

import unittest
import sys
sys.path.append("..")
import common.convert as convert
import common.quantity as quantity
import csv

FILEWITHTESTDATA="./testdata.csv"

def some_val(a):
    """Return some values of the desired type

    Examples:
        >>> some_val(0.0)
        666.0
        >>> some_val(34)
        666
        >>> some_val("15")
        "lorem ipsum"

    Args:
        a (str or float or int), only the type is important

    Returns:
        str or float or int: this same type as args
    """

    match str(type(a))[8:-2]:
        case "str":
            return "lorem ipsum"
        case "float":
            return 666.0
        case "int":
            return 666
        case other:
            return a
        
testdata=[]
with open(FILEWITHTESTDATA, "r") as file:
    csvreader=csv.reader(file)
    for row in csvreader:
        testdata.append(row)

del testdata[:2]

def allunit(testdata):
    allunitset=set()
    for line in testdata:
            allunitset.add(line[1])
            allunitset.add(line[3])
    allunitlist=list(allunitset)
    allunitlist.remove("")
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

class TestConvert(unittest.TestCase):

    def test_conversion(self):
        for aunit in allunit(testdata): #all unit to test
            for u in unitlist(testdata, aunit):

                (inputval, outputval)=searchtd(testdata, aunit, u)
                for i in range(0, len(inputval)):
                    with self.subTest(i=i):
                        #shall return this same value
                        self.assertEqual(convert.convert(float(inputval[i]), aunit, aunit),
                                         float(inputval[i]))
                        #shall convert input value to output
                        self.assertEqual(convert.convert(float(inputval[i]), aunit, u),
                                         float(outputval[i]))

if __name__=='__main__':
    unittest.main()
