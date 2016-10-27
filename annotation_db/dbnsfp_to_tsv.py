#!/usr/bin/env python
"""
---------------------------------------------------------------------------------------
Note:    transfer dbNSFP.txt format to spec tsv for Hbase.
dbNSFP:  ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFPv3.2a.zip
Usage:   dbnsfp_to_tsv.py ./dbNSFP3.2a
------------------------------------------------------------------------------------------
"""

import os
import sys

dbdsfp_dir = sys.argv[1]
chrs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
        "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "M", "X", "Y"]
header = []

with open("dbNSFP.tsv", "w") as out_handle, \
        open("dbNSFP_index_hg19_chr_pos_alt.tsv", "w") as hg19_index_handle, \
        open("dbNSFP_index_hg38_chr_pos_alt.tsv", "w") as hg38_index_handle:
    for chr_n in chrs:
        infile_name = "dbNSFP3.2a_variant.chr{}".format(chr_n)
        infile = os.path.join(dbdsfp_dir, infile_name)

        with open(infile) as in_handle:
            n = 0
            for line in in_handle:
                if line.startswith("#"):
                    if len(header) == 0 and n == 0:
                        header = line.split("\t")
                        header[8] = "hg19_pos_1_based"
                        header.pop(9)
                        header.pop(10)
                        header = header[1:]
                        header[1] = "id"
                    continue
                n += 1
                fields = line.split("\t")
                hg19_index_handle.write("chr{chr}-{pos}-{alt}\t{id}\n".format(
                    chr=fields[7], pos=fields[8], alt=fields[3], id=n))
                hg38_index_handle.write("chr{chr}-{pos}-{alt}\t{id}\n".format(
                    chr=fields[0], pos=fields[1], alt=fields[3], id=n))

                fields.pop(9)
                fields.pop(10)

                out_handle.write("{0}\t{1}".format(n, "\t".join(fields[2:])))

with open("dbNSFP_header.tsv", "w") as header:
    header.write("\t".join(header))
