import logging

def convert(value, ufrom, uto):
    """convert value's unit from ufrom to uto"""
    return from_SI(to_SI(value, ufrom), uto)

def to_SI(value, ufrom):
    """convert to SI"""
    match ufrom:
        case "m3":
            return value
        case "l":
            return (value/1000.0)
        case _:
            logging.error(f"unknow unit {ufrom}, can't convert")
            return value

def from_SI(value, uto):
    """convert from SI"""
    match uto:
        case "m3":
            return value
        case "l":
            return (value*1000)
        case _:
            logging.error(f"unknow unit {uto}, can't convert")
