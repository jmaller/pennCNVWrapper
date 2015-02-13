"""
    pennCNVWrapper.py
    Usage:
        pennCNVWrapper.py --preprocess  -d <DATA> -o <BASE_OUTPUT> -n <NAME> [options]
        pennCNVWrapper.py --run -o <BASE_OUTPUT> -n <NAME> [options]
        pennCNVWrapper.py --postprocess -d <DATA> -i <RESULTS_BASE> -o <OUTPUT_PATH> -n <NAME> [options]
        pennCNVWrapper.py --check -o <OUTPUT_PATH>
    Options:
        -n NAME, --name=NAME                Names the run of pennCNVWrapper

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
    # Deal with arguments, determine which run mode


    # Run mode 1: pre-run QC / file prep
    # Create directory structure
    # Locate .gtc.txt files
    # Generate signal files
    # Sample-level signal file QC
    # SNP-level signal file QC
    # Generate PFB file
    # Generate GC file

    # Run mode 2: run PennCNV
    # Pre-run checks
    # Run PennCNV
    # Create job array script and parameter set

    # Run mode 3: post-run QC
    # Internally run mode 4
    # Output QC summary of raw calls
    # Filter and merge
    # Summarize merged / filtered dataset
    # plots and things as requested

    # Run mode 4: check run progress
    pass


if __name__ == "__main__":
    args = docopt(__doc__, version='0.1')
    main(args)