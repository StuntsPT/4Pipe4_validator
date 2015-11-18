#!/usr/bin/python3
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
#Usage:

def compare_parser(comparer_file, snps={}):
    """
    Parses a comparer file and returns a dictionary with {contig#SNP:[locations]}.
    """
    contig = ""
    counter = 0
    with open(comparer_file, 'r') as infile:
        for lines in infile:
            lines = lines.split()
            if lines[2].rstrip() == contig:
                counter -= 1
            else:
                contig = lines[2].rstrip()
                split_contig = contig.split("#")
                counter = len(split_contig)
            snp = split_contig[0] + "#" + split_contig[-counter + 1]
            if snp in snps:
                snps[snp].append(" ".join(lines[:2]))
            else:
                snps[snp] = [" ".join(lines[:2])]

    return snps


def ref_parser(ref_file):
    """
    Parses the ref file and returns a tuple with the data.
    """
    with open(ref_file, 'r') as infile:
        refs = infile.readlines()
        rfs = [x.rstrip() for x in refs]

    return rfs

def main(comparer1, comparer2, ref1, ref2):
    """
    Main function.
    """
    snps = compare_parser(comparer1)
    snps = compare_parser(comparer2, snps)

    ref1_raw = ref_parser(ref1)
    ref2_raw = ref_parser(ref2)

    snpset = set()
    for k, v in snps.items():
        for s in v:
            if s in ref1_raw or s in ref2_raw:
                snpset.add(k)

    return len(snpset)

# Fazer set de SNPs se as coordenadas dos comparers baterem com as refs!!!

if __name__ == "__main__":
    # Usage: python3 counter.py comparer1.txt compaer2.txt ref_1.txt ref_2.txt
    from sys import argv
    print(main(argv[1], argv[2], argv[3], argv[4]))
