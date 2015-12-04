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


import re


def fasta_parser(fasta_file):
    """
    Parses a DiscoSNP fasta, and converts the name to something akin to what
    4Pipe4 provides.
    """
    fasta = open(fasta_file, 'r')
    include = True

    for lines in fasta:
        if lines.startswith('>'):
            if "_lower_" in lines or "/" not in lines.split("|")[1]:
                include = False
            else:
                include = True
                data = lines.split("|")
                left_contig_length = int(re.sub(".*_", "", data[6]))
                orig_snp_pos = int(re.search(":\d*?_", data[1]).group()[1:-1])
                new_snp_pos = str(left_contig_length + orig_snp_pos + 1)
                snp_bases = re.search("./.$", data[1]).group().replace("/","")
                new_name = data[0] + "#" + new_snp_pos + snp_bases
                print(new_name)


        elif include is True:
            print(lines.strip())
    fasta.close()


if __name__ == "__main__":
    # Usage: python3 DiscoSNP24Pipe4.py file.fasta
    from sys import argv
    fasta_parser(argv[1])
