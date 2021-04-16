def isNum( number ):
    try:
        float(number)
        return True
    except ValueError:
        return False