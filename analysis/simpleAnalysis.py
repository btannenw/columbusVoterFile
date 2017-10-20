### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: script for calculating simple correlations

import json
from voterFile import voterFile, voterParser


# 0. *** Open JSON files of subsamples
with open('../makeSamples/masterFlatVoterFile_subSample_1.json') as data_file:
    infile = json.load(data_file)

vFile = voterFile(infile)
vFile.printSimpleSummary()
