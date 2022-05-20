# Tempus Technical Challenge for Bioinformatics
## Goal
Prototype a software to annotate a VCF file.

## Why Python
Python is commonly used in the bioinformatics space and was familiar to me so it was the right tool for the job. The best tool is usually the one you know how to use.

## Challenges
#### VCF File Structure
VCF file formatting created a couple of hurdles in that each record did not represent a single variant, sometimes records are shared by variants thus producing minor challenges to basic parsing techniques. I was not able to fully handle the complexity but created a solution that allowed me to process the majority of the data provided in the time I was alloted. 

#### VEP API Utilization
This part of the script threw me for a loop as I wasn't able to dicern how to extract a region to use the API. The NULLS in the annoated VCF file are placeholders for Gene,Type, and Effect

#### Larger File Sizes
Even though VCF files are in a semi compressed(~100gb) in comparison to GFF files for example, handling multiple files or larger ones may be demanding depending on the resources of your local machine ([BCFs](https://samtools.github.io/bcftools/howtos/index.html) are compressed versions of VCFs and there are approaches to handling those as well). In this techincal challenge I did not run into that issue but without access to large parallelization one might need to split the files into smaller chunks for processing.

## Installation
At least Python3.6 is required due to f-String usage.
The requests package will need to be installed to handle API calls

## Usage
Just pass the args (-i, -o) with paths to the input vcf file and output file respectively.
Ex.
```
python3 pathto/tbioinfochallenge_d.py -i 'pathto/test_vcf_data.txt' -o 'pathto/outputfile.tsv'
```

## Credits
Thanks to Tempus for allowing me to take a stab at a fun problem even though I didn't complete it fully I learned a big on the way.
