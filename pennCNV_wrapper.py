"""
    pennCNV_wrapper.py
    Usage:
        pennCNV_wrapper.py --preprocess  -d <DATA> -o <BASE_OUTPUT> -n <NAME> [-x <EXCLUDED>]    [options]
        pennCNV_wrapper.py --run                   -o <BASE_OUTPUT> -n <NAME>                    [options]
        pennCNV_wrapper.py --postprocess -d <DATA> -o <OUTPUT_PATH> -n <NAME>                    [options]
        pennCNV_wrapper.py --check       -d <DATA> -o <OUTPUT_PATH> -n <NAME>                    [options]

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
import numpy as np
from numpy import std
from numpy import average
from numpy import median
from wrapper_helper_functions import *


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


def prep_signal_files(data_folder, output_folder, force=False, debug=False):
    # CONVERT ILLUMINA FILES TO PENNCNV INPUT SIGNAL FILES
    gtcList = []
    try:
        for root, dirs, files in os.walk(data_folder):
            for filename in files:
                if filename.endswith(".gtc.txt"):
                    gtcList.append(os.path.join(root, filename))
    except OSError:
        fatal("file structure exception")

    # Check if the signalfiles folder exists, or create if it doesn't
    signalPath = output_folder + "/signalfiles"

    logPath = signalPath + "/processLog.txt"
    logFile = open(logPath, 'w')

    if debug:
        begin = time()
        print "DEBUG: ***** STARTING SIGNAL FILE PREP *****"

    # convert each gtc file
    for number, gtcFile in enumerate(gtcList):
        # Grab the sample ID from the file path
        sampleID = gtcFile.split("/")[-1].split(".")[0]
        samplePath = signalPath + "/" + sampleID + ".gtc.txt.penncnv"

        if force is False and os.path.isfile(samplePath):
            logFile.write("Sample (%d): [ %s ] exists at [ %s ]\n" % (number + 1, sampleID, samplePath))
            if debug:
                print "DEBUG: Sample (%d): [ %s ] exists at [ %s ]" % (number + 1, sampleID, samplePath)
        # else if force is true OR the file does not exist OR both
        else:
            logFile.write("Sample (%d): Parsing [ %s ] into [ %s ]\n" % (number + 1, gtcFile, samplePath))
            if debug:
                print "DEBUG: Sample (%d): Parsing [ %s ] into [ %s ]" % (number + 1, gtcFile, samplePath)
            toWrite = open(samplePath, 'w')
            toWrite.write("%s\t%s\t%s\t%s\t%s\n" % ("Name", "Chr", "Position", sampleID+".Log R Ratio", sampleID+".B Allele Freq"))
            # simultaneously do a thing
            with open(gtcFile, 'r') as f:
                for count, line in enumerate(f):
                    if count < 12:
                        continue
                    line = line.split()
                    # Round floats or not?  NOTICE: PennCNV takes nans in the format "NaN", the first line
                    #     will rewrite nans as "nan"

                    # toWrite.write("%s\t%s\t%s\t%.04f\t%.04f\n" % (line[0], line[1], line[2], float(line[15]), float(line[14])))
                    toWrite.write("%s\t%s\t%s\t%s\t%s\n" % (line[0], line[1], line[2], line[15], line[14]))
            toWrite.close()
    if debug:
        print "DEBUG: ***** SAMPLE PREP DONE, TOOK %s SECONDS *****" % str(round(time() - begin, ndigits=2))


def prepPFBFile():
    pass


def prepGCFile():
    pass


def prerun_sample_qc(directory, debug=False):
    """What to do with NaN-i-ness?"""

    if debug:
        begin = time()
        print "DEBUG: ***** STARTING PRERUN SAMPLE QC *****"

    sample_folder = directory.signalfiles
    signal_file_list = []

    qc_log = open(sample_folder + "/qc_log.txt", 'w')
    qc_log.write("SAMPLE\tLRR_MEDIAN\tLRR_STD\tBAF_DRIFT\tPASS/FAIL\n")
    qc_list = open(sample_folder + "/qc_list.txt", 'w')
    if debug:
        print "DEBUG: SAMPLE_ID             LRR_MED\tLRR_STD\tBAF_DFT\t QC"

    # populate signal_file_list with list of signal files
    try:
        for root, dirs, files in os.walk(sample_folder):
            for file_name in files:
                if file_name.endswith(".gtc.txt.penncnv"):
                    signal_file_list.append(os.path.join(root, file_name))
    except OSError:
        fatal("OS error in %s" % directory.signalfiles)

    # iterate through the samples and extract QC parameters

    for number, sample in enumerate(signal_file_list):
        # parse the 1234567890_R12C34 format
        sample_id = sample.split("/")[-1].split(".")[0]
        sample_lrrs = []
        sample_bafs = []
        with open(sample, 'r') as sample_file:
            for count, line in enumerate(sample_file):
                if count == 0:
                    continue
                line = line.split("\t")

                # don't do anything for X, Y, MT
                if chromosome_as_int(line[1]) > 22:
                    continue

                lrr = float(line[3])
                baf = float(line[4])
                sample_bafs.append(baf)
                if not np.isnan(lrr):
                    sample_lrrs.append(lrr)

        # average_lrr = average(sample_lrrs)
        std_lrr = std(sample_lrrs)
        median_lrr = median(sample_lrrs)
        baf_drift = 0
        for baf in sample_bafs:
            if .20 < baf < .25 or .75 < baf < .8:
                baf_drift += 1
        baf_drift /= float(count)

        # some stuff here to pass qc
        qc_list.write("%s\tPASS\n" % sample_id)
        qc_log.write("%s\t%.3f\t%.3f\t%.3f\tPASS\n" % (sample_id, median_lrr, std_lrr, baf_drift))

        # DEBUG
        if debug:
            if median_lrr > 0:
                median_lrr = " %.3f" % median_lrr
            else:
                median_lrr = "%.3f" % median_lrr
            print "DEBUG: %s     %s  \t%.3f  \t%.3f  \tPASS" % (sample_id, median_lrr, std_lrr, baf_drift)

        # # some stuff here to fail qc
        # qc_list.write("%s\tFAIL\t" % sample_id)
        # qc_log.write("%s\t%.3f\t%.3f\t%.3f\tFAIL\n" % (sample_id, median_lrr, std_lrr, baf_drift))
        # if debug:
        #     print "DEBUG: %s\t%.3f\t%.3f\t%.3f\tFAIL" % (sample_id, median_lrr, std_lrr, baf_drift)


    qc_list.close()
    qc_log.close()
    print "DEBUG: ***** PRERUN SAMPLE QC DONE, TOOK %s SECONDS *****" % str(round(time() - begin, ndigits=2))


def prerun_snp_qc():
    pass


def preRunQC():
    # Generate QC report for samples
    # Generate QC report for SNPs
    # record this stuff so you don't have to do it multiple times
    # record samples and snps used and QC metrics
    pass


def runPennCNV():
    pass


def postRunQC():
    pass


def postRunMerge():
    pass


def postRunSummary():
    pass


def main(args):
    # Deal with arguments, determine which run mode
    # Run mode 1: pre-run QC / file prep
    # Locate .gtc.txt files
    # Generate signal files
    # Sample-level signal file QC
    # SNP-level signal file QC
    # Generate PFB file
    # Generate GC file
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
        prep_signal_files(data_folder=data, output_folder=dir.run_path, force=args['--force'], debug=args['--debug'])

        prerun_sample_qc(directory=dir, debug=args['--debug'])
    elif args['--run']:
        pass
    elif args['--postprocess']:
        pass
    elif args['--check']:
        pass

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


if __name__ == "__main__":
    try:
        args = docopt(__doc__, version='0.1')
    except:
        print __doc__
        exit()
    main(args)