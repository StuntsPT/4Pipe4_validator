#4Pipe4 Validator

##This program will validate the results of the 4Pipe4 analysis pipeline.

##Usage:
    python2 validator.py infile.bam min_depth(int)

##Input:
The input file is a sorted and indexed bam file, of the sequence data aligned
against the file.SNPs.fasta output of *4Pipe4*.
The second argument is an integer that represents the minimum depth required to
perform a validation check.