#!/bin/env python3

'''
Prototype variant annotation tool created for techinical challenge
Author: duy

-i vcf file
-o tsv

'''

import requests, sys
import argparse
import os.path
from pprint import pprint

'''
#IDEA create list of files to initiate batch preprocessing or if file needs to
be split to handle in memory locally if needed, ...to be fleshed out..

numFiles = []
pathName = os.getcwd()
fileNames = os.listdir(pathName)
for fileNames in fileNames:
    if fileNames.endswith("copy.txt"):
        numFiles.append(fileNames)
print('files being processed ' + str(numFiles))

'''

#Add arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="VCF file path.")
parser.add_argument("-o", type=str, help="Name of output file")
args = parser.parse_args()

#Check if VCF file exists
if not args.i:
	print("No input file specified.")
	exit()

elif not os.path.isfile(args.i):
	print("File specified does not exist.")
	exit()

def get_annotations(vcff):

	#parse variant info from VCF file, need a func to handle multiple alts
	variant = vcff.split("\t")
	chrom = variant[0]
	pos = variant[1]
	varID = variant[2]
	ref = variant[3]
	alt = variant[4]

	#create list from format col
	#len of variant = 10, need last two items of [9] for coverage + percent calc
	samplelist = variant[9].split(":")

	#checking vals
	#print (samplelist[4]) #NR
	#print (samplelist[5]) #NV

	#depth of coverage at variant position NR from FORMAT
	Tdepth = samplelist[4].strip("\n")

	#reads supporting the variant, assuming NV from FORMAT however I did friends
	#literature on support meaning forward+reverse strand coverage
	varReads = samplelist[5].strip("\n")

	#variant/reference read percentages assuming if not variant read then ref read
	'''
	revisit this area, e.g. line 41 (not couting meta) of VCF has multiple ALTs
	therefore there are multiple varReads and Tdepth vals. This is a common
	shortcoming of VCF files and preprocessing should include spliting the
	record by all ALTs. Based on ValueError, 35 records total with multiple ALTs
	in current VCF
	'''
	try:

		varPercent = int(varReads)/int(Tdepth)
		#print(varPercent)

        #rounded to 2 decimals
		varPercent = str(round(varPercent*100,2)) + '%'
		#print(varPercent)

	except ValueError: #var percent >1 and catches records with multiple ALTS
		varPercent = "valerr"

'''
API results
'''
    server = "https://grch37.rest.ensembl.org"
    ext = "/vep/human/hgvs"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    chrom=["NC_000002.11","NC_000009.11"]
    pos=["120885310","97209066"]

    for record in chrom:
    #example inputs
	r = requests.post(server+ext, headers=headers, data='{ "hgvs_notations" : ["NC_000009.11:g.97209066T>C","GL000192.1:g.160087C>T","MT:g.7965T>C","NC_000023.10:g.2724760T>C"] }')


    if not r.ok:
	r.raise_for_status()
	sys.exit()


    decoded = r.json()
    #pprint (decoded)
    #print("checking length")
    #pprint(print(decoded[i]['colocated_variants'][0]))
    for i,e in enumerate(decoded):
	print (decoded[i]['most_severe_consequence'])
	most_severe_consequence = decoded[i]['most_severe_consequence']
	if 'colocated_variants' in decoded[i]:
	    if len(decoded[i]['colocated_variants']) > 1:
		if 'minor_allele' in decoded[i]['colocated_variants'][1]:
		    print (decoded[i]['colocated_variants'][1]['minor_allele'])
		    minor_allele = decoded[i]['colocated_variants'][1]['minor_allele']
		else:
		    minor_allele = "NULL"

	if 'minor_allele_freq' in decoded[i]['colocated_variants'][1]:
	    print (decoded[i]['colocated_variants'][1]['minor_allele_freq'])
	    minor_allele_freq = decoded[i]['colocated_variants'][1]['minor_allele_freq']
	else:
	    minor_allele_freq = "NULL"
	else:
	    minor_allele = "NULL"
	    minor_allele_freq = "NULL"


    #place holders for values
	Gene = "NULL"
	#Type = "NULL"
	#Effect = "NULL"

	return f"{chrom}\t{pos}\t{varID}\t{Tdepth}\t{varReads}\t{varPercent}\t{Gene}\t{Type}\t{Effect}\n"


#output below============================================================================================

#output table structure
output_table = "Chrom\tPos\tID\tCoverage depth\tReads supporting variant\tVariant/Reference reads\tGene\tType\tEffect\n"

#vcf ingest
with open(args.i, "r") as vcf_file:

	line = vcf_file.readline()

	while line.startswith("##"): #skip header lines
		line = vcf_file.readline()

	#write to output file if arg supplied else print it
	if args.o:
		output = open(args.o, "w")
		output.write(output_table)

		for line in vcf_file:
			output.write(get_annotations(line))

		output.close()

	else:
		print(output_table)
		for line in vcf_file:
			print(get_annotations(line))

vcf_file.close()

'''
thanks for the opportunity
-d
'''
