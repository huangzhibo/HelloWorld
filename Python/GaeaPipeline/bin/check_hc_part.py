#!/usr/bin/env python
# encoding: utf-8
import os
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import time

from gaeautils import printtime

__all__ = []
__version__ = '0.1'
__date__ = '2018-05-21'
__updated__ = '2018-05-21'


def result_check(data, size_threshold=3):
    if not os.path.exists(data) or os.path.getsize(data) / 1024 < size_threshold:
        printtime('ERROR: (data: %s) - Is incomplete!!!' % data)
        return False
    return True


def check_part_vcf(bed_prefix, part_vcf_dir, vcf_suffix):
    status = True
    for p in bed_prefix:
        tmp_vcf = os.path.join(part_vcf_dir, p + vcf_suffix)
        vcf_status = result_check(tmp_vcf)
        if not vcf_status:
            status = False
            break
    return status


def link_vcf(bed_prefix, part_vcf_dir, vcf_suffix, out_dir):
    for p in bed_prefix:
        tmp_vcf = os.path.join(part_vcf_dir, p + vcf_suffix)
        dst_tmp_vcf = os.path.join(out_dir, p + vcf_suffix)
        os.symlink(tmp_vcf, dst_tmp_vcf)


def main():
    program_name = os.path.basename(sys.argv[0])
    program_license = '''{0}
      Created by huangzhibo on {1}.
      Last updated on {2}.
      Copyright 2017 BGI bigData. All rights reserved.
    USAGE'''.format(" v".join([program_name, __version__]), str(__date__), str(__updated__))

    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-b", "--bedlist", help="the bed.list to run HC streaming,[default: %(default)s]", required=True)
    parser.add_argument("-o", "--outdir",
                        help="outdir of part_vcf's symbolic link [default: %(default)s]", )
    parser.add_argument("-s", "--suffix", help="part_vcf file suffix [default: %(default)s]", default='.hc.vcf.gz', )
    parser.add_argument("-p", "--part_vcf_dir", help="the tmpfir of part_vcf [default: %(default)s]", required=True)
    parser.add_argument("-i", "--index_check", action="store_true", default=True,
                        help="check vcf index [default: %(default)s]", )

    if len(sys.argv) == 1:
        parser.print_help()
        exit(1)

    # Process arguments
    args = parser.parse_args()
    if not os.path.exists(args.bedlist):
        printtime('ERROR: (--bedlist: %s) - No such file or directory' % args.state)
        return 1

    if not os.path.exists(args.part_vcf_dir):
        printtime('ERROR: (--part_vcf_dir: %s) - No such file or directory' % args.state)
        return 1

    bed_prefix = []
    with open(args.bedlist, 'r') as beds:
        for bed in beds:
            bed_prefix.append(os.path.splitext(os.path.basename(bed))[0])

    status = False
    i = 30
    while i:
        status = check_part_vcf(bed_prefix, args.part_vcf_dir, args.suffix)
        if status:
            if args.index_check:
                vcf_index_suffix = "{}.tbi".format(args.suffix)
                status = check_part_vcf(bed_prefix, args.part_vcf_dir, vcf_index_suffix)
            break
        time.sleep(5)
        i -= 1

    if args.outdir:
        link_vcf_dir = os.path.abspath(args.outdir)
        if os.path.exists(link_vcf_dir):
            printtime('ERROR: (--outdir: %s) - This directory is already exists! Please remove it and check again!' % link_vcf_dir)
            return -1
        os.makedirs(link_vcf_dir)

    if status:
        print("part_vcf_dir is good!")
        if args.outdir:
            link_vcf(bed_prefix, args.part_vcf_dir, args.suffix, os.path.abspath(args.outdir))
    else:
        print("part_vcf_dir is bad!")
        return -1

    return 0


if __name__ == "__main__":
    sys.exit(main())
