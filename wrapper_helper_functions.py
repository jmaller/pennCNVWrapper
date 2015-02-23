

def chromosome_as_int(chromosome):
    if chromosome == 'X':
        return 23
    elif chromosome == 'Y':
        return 24
    elif chromosome == 'MT':
        return 25
    else:
        return int(chromosome)


def fatal(errorMessage):
    print "ERROR: " + errorMessage
    exit()