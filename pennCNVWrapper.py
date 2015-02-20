"""
    pennCNVWrapper.py
    Usage:
        pennCNVWrapper.py --preprocess  -d <DATA> -o <BASE_OUTPUT> -n <NAME> [-x <EXCLUDED>]    [options]
        pennCNVWrapper.py --run                   -o <BASE_OUTPUT> -n <NAME>                    [options]
        pennCNVWrapper.py --postprocess -d <DATA> -o <OUTPUT_PATH> -n <NAME>                    [options]
        pennCNVWrapper.py --check       -d <DATA> -o <OUTPUT_PATH> -n <NAME>                    [options]

    Arguments:
        -d <DATA>, --data <DATA>                    Denotes the folder containing the gtc.txt files to use
        -o <OUTPUT_PATH>, --output <OUTPUT_PATH>    Provides the folder base for PennCNVWrapper
        -n <NAME>, --name <NAME>                    Names the run of pennCNVWrapper
        -x <EXCLUDED>, --exclude <EXCLUDED>         Excludes the list of samples in this file

    Options:
        --force                                     Forces reconstruction of all files, even if they are present
        --debug                                     Debug the bugs

"""
import os
from docopt import docopt
from types import *
from time import time


class projectDirectory:
    """This class handles the setup and maintenance of the folder structure
    Structure:
        [ Parent Folder] ---
                            Run_Name_1 ---
                                        bsublogs
                                        logs
                                        output
                                        scripts
                                        signalfiles
                            Run_Name_2 --- ...                          """
    def __init__(self, path, name):
        # check type correctness
        assert type(path) is StringType, "path is not a string"
        assert os.path.isdir(path)

        # strip an ending '/' if applicable
        if path[-1] == '/':
            path = path[:-1]

        self.path = path
        self.run_path = path + "/" + name
        self.bsublogs = self.run_path + "/bsublogs"
        self.logs = self.run_path + "/logs"
        self.output = self.run_path + "/output"
        self.scripts = self.run_path + "/scripts"
        self.signalfiles = self.run_path + "/signalfiles"

        # establish structure if it does not exist
        for folder in [self.run_path, self.bsublogs, self.logs, self.output, self.scripts, self.signalfiles]:
            try:
                if not os.path.isdir(folder):
                    os.mkdir(folder)
            except OSError:
                fatal("OSError with %s.  Check arguments and permissions" % folder)


def prepSignalFiles(dataFolder, outputFolder, force=False, debug=False):
    # CONVERT ILLUMINA FILES TO PENNCNV INPUT SIGNAL FILES
    gtcList = []
    try:
        for root, dirs, files in os.walk(dataFolder):
            for filename in files:
                if filename.endswith(".gtc.txt"):
                    gtcList.append(os.path.join(root, filename))
    except OSError:
        fatal("file structure exception")

    # Check if the signalfiles folder exists, or create if it doesn't
    signalPath = outputFolder + "/signalfiles"

    logPath = signalPath + "/processLog.txt"
    logFile = open(logPath, 'w')
    # if debug mode is not on, pipe standard out and standard error into processLog.txt

    begin = time()

    # convert each gtc file
    for number, gtcFile in enumerate(gtcList):
        # Grab the sample ID from the file path
        sampleID = gtcFile.split("/")[-1].split(".")[0]
        samplePath = signalPath + "/" + sampleID + ".gtc.txt.penncnv"
        if debug:
            print "DEBUG: Sample %d: Parsing %s into %s" % (number, gtcFile, samplePath)
        logFile.write("Sample %d: Parsing %s into %s" % (number, gtcFile, samplePath))
        if not (os.path.isfile(samplePath) and force is False):
            toWrite = open(samplePath, 'w')
            toWrite.write("%s\t%s\t%s\t%s\t%s\n" % ("Name", "Chr", "Position", sampleID+".Log R Ratio", sampleID+".B Allele Freq"))
            # simultaneously do a thing
            with open(gtcFile, 'r') as f:
                for count, line in enumerate(f):
                    if count < 12:
                        continue
                    line = line.split()
                    # Round floats or not?  **** NOTICE **** PennCNV takes nans in the format "NaN", the first line
                    #     will rewrite nans as "nan"

                    # toWrite.write("%s\t%s\t%s\t%.04f\t%.04f\n" % (line[0], line[1], line[2], float(line[15]), float(line[14])))
                    toWrite.write("%s\t%s\t%s\t%s\t%s\n" % (line[0], line[1], line[2], line[15], line[14]))
            toWrite.close()
    if debug:
        print "DEBUG: Done, took %s seconds" % str(round(time() - begin, ndigits=2))


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


def fatal(errorMessage):
    print "ERROR: " + errorMessage
    exit()



def main(args):
    # Deal with arguments, determine which run mode
    # Run mode 1: pre-run QC / file prep
    if args['--preprocess']:

        data = args['--data']
        output = args['--output']
        name = args['--name']

        # trim "/" off DATA and OUTPUT if included in argument
        if data[-1] == "/":
            data = data[:-1]
        if output[-1] == "/":
            output = output[:-1]

        # Step 1: Create directory structure
        dir = projectDirectory(output, name)
        # makeStructure(outputFolder=output)
        # Step 2: generate signal files
        prepSignalFiles(dataFolder=data, outputFolder=dir.run_path, force=args['--force'], debug=args['--debug'])

    elif args['--run']:
        pass
    elif args['--postprocess']:
        pass
    elif args['--check']:
        pass
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
    try:
        args = docopt(__doc__, version='0.1')
    except:
        print __doc__
        exit()
    main(args)