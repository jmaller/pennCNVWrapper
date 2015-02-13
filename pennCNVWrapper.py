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
import os
import subprocess


from docopt import docopt


def prepSignalFiles(dataFolder, outputFolder, force=False):
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
    if not os.path.isdir(signalPath):
        os.mkdir(signalPath)
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