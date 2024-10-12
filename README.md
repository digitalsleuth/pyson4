# pyson4
Mozilla JSON LZ4 parser

This is a python3 utility.
The Mozilla jsonlz4 'file-type' is unique in that the header (mozLz40\x00) is not a proper LZ4 frame.
Due to this, the first 8 bytes (the header) must be skipped, and the remainder of the file is treated as a block.

This script will essentially take an input file (jsonlz4 type file), read the block, and output to a json file.
Requirements: pip install lz4
Windows requires Visual Studio Build Tools 14+ be installed for lz4 to be installed.

Binaries compiled with the following command line:

`pyinstaller pyson4.spec`

Source Material:

https://dxr.mozilla.org/mozilla-central/source/toolkit/components/lz4/lz4.js
https://buildmedia.readthedocs.org/media/pdf/python-lz4/latest/python-lz4.pdf
