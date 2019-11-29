# pyson4
Firefox JSONLZ4 parser

The Firefox jsonlz4 'file-type' is unique in that the header (mozLz40\x00) is not a proper LZ4 frame.
Due to this, the first 8 bytes (the header) must be skipped, and the remainder of the file is treated as a block.

This script will essentially take an input file (jsonlz4 type file), read the block, and output to a json file.
Requirements: pip install python-lz4

Source Material:

https://dxr.mozilla.org/mozilla-central/source/toolkit/components/lz4/lz4.js
https://buildmedia.readthedocs.org/media/pdf/python-lz4/latest/python-lz4.pdf
