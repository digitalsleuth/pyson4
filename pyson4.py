#!/usr/bin/env python3

"""
The Firefox jsonlz4 'file-type' is unique in that the header (mozLz40\x00) is not a proper LZ4 frame.
Due to this, the first 8 bytes (the header) must be skipped, and the remainder of the file is treated as a block.

This script will essentially take an input file (jsonlz4 type file), read the block, and output to a json file.
Requirements: pip install python-lz4

Source Material:

https://dxr.mozilla.org/mozilla-central/source/toolkit/components/lz4/lz4.js
https://buildmedia.readthedocs.org/media/pdf/python-lz4/latest/python-lz4.pdf

TODO:

Might add option to ignore incorrect header and attempt to parse as block.
"""
import lz4.block
import sys
from argparse import ArgumentParser

__author__ = 'Corey Forman'
__date__ = '28 Nov 2019'
__version__ = '0.2'
__description__ = 'Firefox JSONLZ4 Parsing Tool'

class LZ4Error(Exception):
    pass

class HeaderMismatch(LZ4Error):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def decompress(jlz4_file):
    jsonlz4_header = b'mozLz40\x00'
    if jlz4_file.read(8) != jsonlz4_header:
        raise HeaderMismatch("Invalid jsonlz4 Header")
    return lz4.block.decompress(jlz4_file.read())

def compress(file_block):
    compressed_block = lz4.block.compress(file_block.read())
    return b'mozLz40\x00' + compressed_block

if __name__ == "__main__":
    arg_parse = ArgumentParser(description='Firefox JSONLZ4 Compression/Decompression tool.', epilog='This tool will only work with the .jsonlz4 format with Firefox.\nFor other LZ4 utilities, try the python-lz4 library')
    arg_parse.add_argument("input_file", metavar="<input_file>", help="Input file, including path if necessary")
    arg_parse.add_argument("output_file", metavar="<output_file>", help="Output file name, including path if necessary")
    arg_parse.add_argument("-d", action="store_true", help="Decompress the input file.")
    arg_parse.add_argument("-c", action="store_true", help="Compress the input file.")
    arg_parse.add_argument("-v", action="version", version='%(prog)s' +str(__version__))
    args = arg_parse.parse_args()

    try:
        input_file = open(args.input_file, 'rb')
    except IOError as e:
        print("Unable to read '%s': %s" % (args.input_file, e), file=sys.stderr)
        raise SystemExit(1)
    
    try:
        output_file = open(args.output_file, 'wb')
    except IOError as e:
        print("Unable to write to '%s': %s" % (args.output_file, e), file=sys.stderr)
        raise SystemExit(1)

    try:
        if args.d:
            blob = decompress(input_file)
        else:
            blob = compress(input_file)
    except Exception as e:
        print("Unable to perform operations on file '%s': %s" % (args.input_file, e), file=sys.stderr)
        raise SystemExit(1)

    try:
        output_file.write(blob)
        file_size = len(blob)
    except IOError as e:
        print("Unable to write to '%s': %s" % (args.output_file, e), file=sys.stderr)
        raise SystemExit(1)
    else:
        print("File '%s' created. Resulting file is %s bytes, and is in JSON format." % (args.output_file, file_size))
    finally:
        output_file.close()

