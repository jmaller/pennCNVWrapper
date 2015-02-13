"""
    pennCNVWrapper.py
    Usage:
        pennCNVWrapper.py [options]

    Options:
        -d DATASET, --data=DATASET          Specify data to use.  Default is DBS wave 1 recluster
        -s, --spread                        Plots an alternate style focusing on SNP cluster density
        -c, --cnv                           Includes CNV definition information in the figure header

"""



from docopt import docopt



def prepSignalFiles():
    pass


def prepPFBFile():
    pass

def prepGCFile():
    pass

def preRunQC():

    pass

def runPennCNV():
    pass

def postRunQC():
    pass

def postRunMerge():
    pass

def postRunSummary():
    pass






def main():
    pass


if __name__ == "__main__":
    args = docopt(__doc__, version='0.1')
    main(args)