"""Provide template for bundle calculations

Copy it with new section name, 
and copy ini file with this same new name

This template is used also for testing scripts,
so leave it here better.
"""
# files might be run from different directory
try:
    import solver.genericsection as gs
except:
    import sys
    sys.path.append('../')
    import genericsection as gs

class CalcBundle(gs.GenericSection):
    """calculator parameters and functions
    """

    # get all generic data from GenericSection's init
    def __init__(self, name="just template"):
        super().__init__(name, __file__)

    #==========start editing section==========#
    
    # here create functions for calculation
    # every function shall has name cal_ and name
    # from .ini file

    def cal_sum(self, first: float, second: float) -> float:
        """Calculate sum of two numbers

        Examples:
            >>> cal_sum(3.0, 0.14 )
            3.14
        
        Args:
            first:  first number to add
            second: second number to add

        Returns:
            sum of two numbers

        Raises:
            don't rises any error
        """

        ans = float(first) + float(second)

        return ans

    #===========end editing section===========#

if __name__=='__main__':
    # set to true for fast checking
    # set to False for using test script in tests
    if False:
        obj = CalcBundle()
        #obj.read_from_file("../../input/template/some_template.ini")
        for element in obj.par:
            print(f"{obj.par[element].name}: {obj.par[element].value}")
        print('changing non calculating values')
        for element in obj.par:
            if not obj.par[element].calculate:
                obj.par[element].value=0.32
        for element in obj.par:
            print(f"{obj.par[element].name}: {obj.par[element].value}")
        # TODO testing for attr 'all' and 'sum'
        obj.recalculate('first')
        print('calculate values')
        for element in obj.par:
            print(f"{obj.par[element].name}: {obj.par[element].value}")
        ## TODO testing for calculate = False
    else:
        # use full test from file in tests directory
        import common.testcases
        common.testcases.CallExternalFile(__file__)
