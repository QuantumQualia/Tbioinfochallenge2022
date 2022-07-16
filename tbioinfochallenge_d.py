#!/bin/env python3

'''
Prototype variant annotation tool created for techinical challenge
Author: duy

-i vcf file
-o tsv or view in terminal

'''

import sys
import requests
import argparse
import os.path
import pprint


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

def parse_vcf(vcff):

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

    #depth of coverage at variant position NR from FORMAT
    Tdepth = samplelist[4].strip("\n")

    #reads supporting the variant, assuming NV from FORMAT however I did find
    #literature on support meaning forward+reverse strand coverage.
    varReads = samplelist[5].strip("\n")

    #variant/reference read percentages assuming if not variant read then ref read

    try:

        varPercent = int(varReads)/int(Tdepth)
        #print(varPercent)

        #rounded to 2 decimals
        varPercent = str(round(varPercent*100,2)) + '%'
        #print(varPercent)

        #var percent >1 and catches records with multiple ALTS if not split
    except ValueError:
        varPercent = "valerr"

    return f"{chrom}:g.{pos}{ref}>{alt}\t{Tdepth}\t{varReads}\t{varPercent}\t"

#VEP API
def vep_anno(hgvs):

	server = "https://grch37.rest.ensembl.org"
    for i,e in enumerate(hgvs):

        ext =f"/vep/human/hgvs/{hgvs}?"

        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"}, params="variant_class=1")

        if not r.ok:
            svr_conseq= "NULL"
            vClass ="NULL"
            minor_allele ="NULL"
            minor_allele_freq ="NULL"
            id ="NULL"
            gene ="NULL"
            return f"{svr_conseq}\t{vClass}\t{minor_allele}\t{minor_allele_freq}\t{id}\t{gene}\n"
            continue

        decoded = r.json()
        svr_conseq = decoded[0]['most_severe_consequence']
        vClass = decoded[0]['variant_class']
        gene='NULL'
        if 'colocated_variants' in decoded[0]:
            colen = len(decoded[0]['colocated_variants']) - 1
            if 'minor_allele' in decoded[0]['colocated_variants'][colen]:
                minor_allele = decoded[0]['colocated_variants'][colen]['minor_allele']
            else:
                minor_allele='NULL'

            if 'id' in decoded[0]['colocated_variants'][colen]:
                id = decoded[0]['colocated_variants'][colen]['id']
            else:
                id = "NULL"
            if 'minor_allele_freq' in decoded[0]['colocated_variants'][colen]:
                minor_allele_freq = decoded[0]['colocated_variants'][colen]['minor_allele_freq']
            else:
                minor_allele_freq = "NULL"
        else:
            minor_allele = "NULL"
            minor_allele_freq = "NULL"
            id = "NULL"
        if 'transcript_consequences' in decoded[0]:
            if 'gene_symbol' in decoded[0]['transcript_consequences'][0]:
                gene=decoded[0]['transcript_consequences'][0]['gene_symbol']
            else:
                gene='NULL'
        else:
            pass
            #gene='NULL'
        #print (svr_conseq,vClass,minor_allele,minor_allele_freq,id,gene)
        return f"{svr_conseq}\t{vClass}\t{minor_allele}\t{minor_allele_freq}\t{id}\t{gene}\n"


#output below============================================================================================

#output table structure
output_table = "hgvs\tcoverage_depth\treads_supporting_variant\tvariant/reference_ratio\tvariant_type\tvariant_class\tminor_allele_freq\tgene_id\tgene_symbol\n"

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
            output.write(parse_vcf(line))
            hgvs=str(parse_vcf(line)).split("\t")[0] # hgvs
            #print(hgvs)
            output.write(vep_anno(hgvs))
        output.close()

    else:
        print(output_table)
        for line in vcf_file:
            print(parse_vcf(line))

vcf_file.close()

'''
thanks for the opportunity
-d
'''
