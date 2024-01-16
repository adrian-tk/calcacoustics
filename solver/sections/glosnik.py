# files might be run from different directory
# mostly as script
try:
    from solver import genericsection as gs
except:
    print("can't import, trying modify sys.path")
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

    def cal_EBP(self, Qes: float, fs: float) -> float:
        """Calculate EBP (Efficiency Bandwidth Product)

        Examples:
            >>> calEBP(0.32, 27.0)
            84.375
        
        Args:
            Qes:    Electrical Q factor, unitless
            fs:     Resonance frequency, Hz

        Returns:
            Efficiency Bandwidth Product

        Raises:
            ZeroDivisionError: trying to divide by Qes == 0
        """

        if Qes == 0:
            raise ZeroDivisionError("division by zero")

        EBP = float(fs)/Qes

        return EBP

    #===========end editing section===========#
if __name__=='__main__':
    # set to true for fast checking
    # set to False for using test script in tests
    if True:
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
        obj.recalculate('EBP')
        print('calculate values')
        for element in obj.par:
            print(f"{obj.par[element].name}: {obj.par[element].value}")
        ## TODO testing for calculate = False
    else:
        # use full test from file in tests directory
        import common.testcases
        common.testcases.CallExternalFile(__file__)
