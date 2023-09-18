import logging

def convert(value, ufrom, uto):
    """convert value's unit from ufrom to uto"""
    newval=from_SI(to_SI(value, ufrom), uto)
    logging.debug(f"convert {value} {ufrom} to {newval} {uto}")
    return newval

def to_SI(value, ufrom):
    """convert to SI"""
    match ufrom:
    # volume
        case "m3":
            return value
        case "l":
            return (value/1000.0)
    # lenght
        case "m":
            return value
        case "cm":
            return (value/100.0)
        case "mm":
            return (value/1000.0)
        case _:
            logging.error(f"unknow unit {ufrom}, can't convert")
            return value

def from_SI(value, uto):
    """convert from SI"""
    match uto:
    # volume
        case "m3":
            return value
        case "l":
            return (value*1000)
    # lenght
        case "m":
            return value
        case "cm":
            return (value*100.0)
        case "mm":
            return (value*1000.0)
        case _:
            logging.error(f"unknow unit {uto}, can't convert")
