# SPDX-License-Identifier: MIT
#
# Copyright The SCons Foundation

"""
Phony compiler for testing SCons.

Copies its source file to the target file, dropping lines that match
a pattern, so we can recognize the tool has made a modification.

The first argument is the language (cc, c__, g77, etc.).

Recognizes a -x option to append the language to 'mygcc.out'
for tracing purposes.

Intended for use as $CC, $CXX, etc.
"""

import getopt
import sys

def fake_gcc():

    # The gcc tool has this comment:
    #>    is executable, and is a GNU compiler (or accepts '--version' at least)
    # So to pretend to be gcc, we need to recognize.  Parrot what
    # test/CC/CCVERSION-fixture/versioned.py does.
    if '-dumpversion' in sys.argv:
        print('3.9.9')
        sys.exit(0)
    if '--version' in sys.argv:
        print('this is version 2.9.9 with extra text')
        sys.exit(0)

    compiler = sys.argv[1].encode('utf-8')
    opts, args = getopt.getopt(sys.argv[2:], 'co:xf:K:')
    for opt, arg in opts:
        if opt == '-o':
            out = arg
        elif opt == '-x':
            with open('mygcc.out', 'ab') as logfile:
                logfile.write(compiler + b"\n")

    with open(out, 'wb') as ofp, open(args[0], 'rb') as ifp:
        for line in ifp:
            if not line.startswith(b'#' + compiler):
                ofp.write(line)

if __name__ == '__main__':
    fake_gcc()
    sys.exit(0)
