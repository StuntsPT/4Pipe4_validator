#!/usr/bin/python2
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#Usage: python2 validator.py infile.bam min_depth(int)

import pysam
import re
from sys import argv

infile = pysam.Samfile(argv[1], "rb" )
min_depth = int(argv[2])
Valid_snps = 0
Invalid_snps = 0
Invalidable_snps = 0

for ref in infile.references:
    SNPs = {}
    raw_snps = ref.split("#")[1:]
    for i in raw_snps:
        proc_snps = re.split("(\d+)", i)
        SNPs[int(proc_snps[1])-1]=set(list(proc_snps[2])) #-1 due to index 0!
        how_many = len(SNPs)
    for pileupcolumn in infile.pileup(ref):
        if pileupcolumn.pos in SNPs:
            how_many -= 1
            depth = pileupcolumn.n
            if depth < min_depth:
                Invalidable_snps += 1
                continue
            bases = set()
            for pileupread in pileupcolumn.pileups:
                bases.add(pileupread.alignment.seq[pileupread.qpos])
            if len(SNPs[pileupcolumn.pos].intersection(bases)) >= 2:
                Valid_snps += 1
            else:
                Invalid_snps += 1
    if how_many != 0:
        Invalidable_snps += how_many

print "Validated SNPs: %s\n" % (Valid_snps)
print "Non validated SNPs: %s\n" % (Invalid_snps)
print "Not validable SNPs: %s\n" % (Invalidable_snps)