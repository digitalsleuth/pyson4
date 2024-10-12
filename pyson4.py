#!/usr/bin/env python3

"""
This is a Python 3 script for converting the Mozilla lz4 type file header to readable JSON.
The Mozilla jsonlz4 'file-type' is unique in that the header (mozLz40\x00) is not a standard LZ4 frame type.
Due to this, the first 8 bytes (the header) must be skipped, and the remainder of the file is treated as a block.

This script will essentially take an input file (jsonlz4 type file), read the block, and output to a json file.
Requirements: pip install lz4
Windows requirement: lz4 requires Visual Studio Build Tools 14 + to install
Source Material:

https://dxr.mozilla.org/mozilla-central/source/toolkit/components/lz4/lz4.js
https://buildmedia.readthedocs.org/media/pdf/python-lz4/latest/python-lz4.pdf
"""
import lz4.block
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
import json
import os.path

__author__ = "Corey Forman"
__date__ = "12 Oct 2024"
__version__ = "1.2"
__description__ = "Mozilla JSON LZ4 Parsing Tool"


class LZ4Error(Exception):
    pass


class HeaderMismatch(LZ4Error):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def decompress(jlz4_file):
    jsonlz4_header = b"mozLz40\x00"
    if jlz4_file.read(8) != jsonlz4_header:
        raise HeaderMismatch("Invalid jsonlz4 Header")
    extracted = lz4.block.decompress(jlz4_file.read())
    json_load = json.loads(extracted)
    return json_load


def compress(file_block):
    compressed_block = lz4.block.compress(file_block.read())
    return b"mozLz40\x00" + compressed_block


if __name__ == "__main__":
    arg_parse = ArgumentParser(
        description="Mozilla JSON LZ4 parsing tool",
        epilog="This tool will only work with the Mozilla lz4 format.\nThis includes the jsonlz4 and mozlz4 file extensions.\nFor other LZ4 utilities, try the python-lz4 library",
        formatter_class=RawTextHelpFormatter,
    )
    arg_parse.add_argument(
        "input_file",
        metavar="<input_file>",
        help="Input file including path (if necessary)",
    )
    arg_parse.add_argument(
        "output_file",
        metavar="<output_file>",
        help="Output file name including path (if necessary)",
    )
    arg_parse.add_argument("-d", action="store_true", help="Decompress the input file.")
    arg_parse.add_argument("-c", action="store_true", help="Compress the input file.")
    arg_parse.add_argument(
        "-v", action="version", version="%(prog)s" + " v" + str(__version__)
    )
    arg_parse.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose - prints output path and size.\nBetter to not use if iterating through files",
    )
    args = arg_parse.parse_args()

    try:
        input_file = open(args.input_file, "rb")
    except IOError as e:
        print(f"Unable to read '{args.input_file}': {e}", file=sys.stderr)
        raise SystemExit(1)

    try:
        output_file = open(args.output_file, "w", encoding="utf-8")
    except IOError as e:
        print(f"Unable to write to '{args.output_file}': {e}", file=sys.stderr)
        raise SystemExit(1)

    try:
        if args.d:
            blob = decompress(input_file)
            try:
                json.dump(
                    blob,
                    output_file,
                    indent=4,
                    ensure_ascii=False,
                    separators=(",", ": "),
                )
                output_file.write("\n")
            except IOError as e:
                print(f"Unable to write to '{args.output_file}': {e}", file=sys.stderr)
                raise SystemExit(1)
            else:
                output_file.close()
                file_size = int(os.path.getsize(args.output_file))
                if args.verbose:
                    print(
                        f"Output file '{args.output_file}' created. {file_size} bytes output."
                    )
            finally:
                output_file.close()
        elif args.c:
            blob = compress(input_file)
            try:
                output_file = open(args.output_file, "wb")
                output_file.write(blob)
            except IOError as e:
                print(f"Unable to write to '{args.output_file}': {e}", file=sys.stderr)
                raise SystemExit(1)
            else:
                output_file.close()
                file_size = int(os.path.getsize(args.output_file))
                if args.verbose:
                    print(
                        f"Output file '{args.output_file}' created. {file_size} bytes output."
                    )
        else:
            print(
                "Please choose either the -d (decompress) or -c (compress) option to proceed."
            )
            raise SystemExit(0)
    except Exception as e:
        print(
            f"Unable to perform operations on file '{args.input_file}': {e}",
            file=sys.stderr,
        )
        raise SystemExit(1)
