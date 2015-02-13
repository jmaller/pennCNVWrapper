"""
    pennCNVWrapper.py
    Usage:
        pennCNVWrapper.py --preprocess  -d <DATA> -o <BASE_OUTPUT> -n <NAME> [options]
        pennCNVWrapper.py --run -o <BASE_OUTPUT> -n <NAME> [options]
        pennCNVWrapper.py --postprocess -d <DATA> -i <RESULTS_BASE> -o <OUTPUT_PATH> -n <NAME> [options]
        pennCNVWrapper.py --check -d <DATA> -o <OUTPUT_PATH>

    Arguments:
        -d <DATA>, --data <DATA>            Denotes the folder containing the gtc.txt files to use
        -n <NAME>, --name <NAME>            Names the run of pennCNVWrapper

    Options:
        --force                             Forces reconstruction of all files, even if they are present

"""
import os
from docopt import docopt


def makeStructure(outputFolder):
    # creates the intended output structure if it does not exist:
    # in outputFolder:
    #       logs
    #       output
    #       run1
    #       scripts
    #       signalFiles
    toCheck = []
    toCheck.append(outputFolder)
    toCheck.append(outputFolder + "/logs")
    toCheck.append(outputFolder + "/output")
    toCheck.append(outputFolder + "/run1")
    toCheck.append(outputFolder + "/scripts")
    toCheck.append(outputFolder + "/signalfiles")

    for folder in toCheck:
        try:
            if not os.path.isdir(folder):
                os.mkdir(folder)
        except OSError:
            fatal("OSError with %s.  Check arguments and permissions" % folder)


def prepSignalFiles(dataFolder, outputFolder, force):
    # CONVERT ILLUMINA FILES TO PENNCNV INPUT SIGNAL FILES
    gtcList = []
    try:
        for root, dirs, files in os.walk(dataFolder):
            for file in files:
                if file.endswith(".gtc.txt"):
                    gtcList.append(os.path.join(root, file))
    except OSError:
        fatal("file structure exception")

    # Check if the signalfiles folder exists, or create if it doesn't
    signalPath = outputFolder + "/signalfiles"
    logPath = signalPath + "/processLog.txt"
    logFile = open(logPath, 'w')

    # convert each gtc file
    for gtcFile in gtcList:
        # Grab the sample ID from the file path
        sampleID = gtcFile.split("/")[-1].split(".")[0]
        samplePath = signalPath + "/" + sampleID + ".gtc.txt.penncnv"
        if not (os.path.isfile(samplePath) and force is False):
            toWrite = open(samplePath, 'w')
            toWrite.write("%s\t%s\t%s\t%s\t%s\n" % ("Name", "Chr", "Position", sampleID+".Log R Ratio", sampleID+".B Allele Freq"))
            os.system("awk -v OFS='\t' 'NR>12 {print $1, $2, $3, $16, $15}' " + gtcFile + " + >>" + samplePath)


    # do
    #    bname=`basename $i .gtc.txt`
    #    outfile=${base}/data/signalfiles/${i}.penncnv
    #    rm $outfile
    #    printf "%s\t%s\t%s\t%s\t%s\t%s\n" "Name" "Chr" "Position" "${bname}.GType"  "${bname}.Log R Ratio"  "${bname}.B Allele Freq" > $outfile
    #    cat ${base}/data/wave1/$i | awk -v OFS='\t' 'NR>12 {print $1, $2, $3, $7 $8, $16, $15}' >>$outfile
    # done
    #find $dpath/signalfiles/ -iname '*.g


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
        makeStructure(outputFolder=output)
        # Step 2: generate signal files
        prepSignalFiles(datafolder=data, outputFolder=output, force=args['--force'])

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