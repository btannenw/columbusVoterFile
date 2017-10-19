### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: script for calculating simple correlations

import json
from voterParser import voterParser

# 0. *** Open JSON files of subsamples
with open('../makeSamples/masterFlatVoterFile_subSample_1.json') as data_file:
    voterFile = json.load(data_file)

nActive, nInactive, nActive_U, nActive_D, nActive_R = 0, 0, 0, 0, 0
for line in voterFile:
    voter = voterParser(line)
    #print voter.name, voter.party, voter.status, voter.P_052017, '_', line[30], '_'
    if voter.status == 'A':
        nActive = nActive + 1
        if voter.party == 'U':
            nActive_U = nActive_U + 1
        if voter.party == 'D':
            nActive_D = nActive_D + 1
        if voter.party == 'R':
            nActive_R = nActive_R + 1
    elif voter.status == 'U':
        nInactive = nInactive + 1

print 'Number of voters on file:\t\t\t', len(voterFile)
print 'Number of inactive voters on file:\t\t', nInactive
print 'Number of active voters on file:\t\t', nActive

print 'Number of active voters on file (Democrat):\t', nActive_D,'\t({0:.1f}% of active voters)'.format(100*nActive_D/float(nActive))
print 'Number of active voters on file (Republican):\t', nActive_R,'\t({0:.1f}% of active voters)'.format(100*nActive_R/float(nActive))
print 'Number of active voters on file (Unaffiliated):\t', nActive_U,'\t({0:.1f}% of active voters)'.format(100*nActive_U/float(nActive))
print '=============================================================================='
