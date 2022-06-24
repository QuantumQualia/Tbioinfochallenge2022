#split on multiple alleles

import sys
import os


#Check the number of command line arguments
if not len(sys.argv)==3:
    print ("\nError:\tincorrect number of command-line arguments")
    print ("Syntax:\tAsplitter.py [Input VCF] [Output VCF]\n")
    sys.exit()

if sys.argv[1]==sys.argv[2]:
    print ("Error:\tInput file is the same as the output file - choose a different output file\n")
    sys.exit()

#File input
fileInput = open(sys.argv[1], "r")

#File output for split multi-alleles
fileOutput = open(sys.argv[2], "w")
#Loop through each line in the input file, and split multiallelic sites
print ("Splitting multi-allelic sites...")
for strLine in fileInput:
    #Strip the endline character from each input line
    strLine = strLine.rstrip("\n")

    #Ignore VCF header lines
    if strLine.startswith("#"):
        fileOutput.write(strLine + "\n")
    else:
        #Split the tab-delimited line into an array
        strArray = [splits for splits in strLine.split("\t") if splits != ""]

        #Check first if it's multiallelic
        #Multi-allelic variants will have 2 calls in the VAR field, separated by a comma (',')
        if "," in strArray[4]:
            strVars = [splits for splits in strArray[4].split(",") if splits != ""]
            iNumMultialleles = len(strVars)

            for i in range(0, (iNumMultialleles)):
                strArray[4] = strVars[i]
                fileOutput.write("\t".join(strArray) + "\n")
        else:
            fileOutput.write("\t".join(strArray) + "\n")
print ("Done.")

#Close the files
fileInput.close()
fileOutput.close()
