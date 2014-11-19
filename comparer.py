#!/usr/bin/python2
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#
#Usage: python2 comparer.py infile.bam

'''This program will compare the SNPs in 4Pipe4 contigs against a reference.
It will output the locations of the SNPs the match the "#" tag with the position
of the difference from the reference it was aligned against.
This script is not perfect as some SNPs are getting an offset of +/- 1 base. I 
don't know why this happens yet...'''

import pysam
import re
from sys import argv

infile = pysam.Samfile(argv[1], "rb" )

old_contig_name = ""

for alignedread in infile.fetch():
	new_contig_name = str(alignedread).split()[0]
	if new_contig_name != old_contig_name:
		old_contig_name = new_contig_name
		align_pos = alignedread.pos
		putative_snps = re.split("#", new_contig_name)[1:]
		putative_snps = map(lambda x: re.sub("\D+","",x), putative_snps) #Brutal!

		if alignedread.is_reverse: #inverse math if sequence is reversed
			snps_location = map(lambda x: int(alignedread.aend) - int(x) + 1, putative_snps)
		else:
			snps_location = map(lambda x: int(x) + align_pos, putative_snps)

		ref = infile.getrname(alignedread.tid)

		for snps in snps_location:
			print(ref + "\t" + str(snps) + "\t" + new_contig_name)
