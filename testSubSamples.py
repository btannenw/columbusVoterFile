### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: test split sub-samples of voter file

import json


def printSummary(voterList, split):
    """ print simple summary of input list"""
    
    print '\nSimple Summary:',split,'\n=============================================================================='
    nActive, nInactive, nActive_D, nActive_R, nActive_U, nActive_G, nActive_L = 0,0,0,0,0,0,0
    for voter in voterList:
        if voter[7] == 'A':
            nActive = nActive + 1
            if voter[8] == 'D':
                nActive_D = nActive_D + 1
            elif voter[8] == 'R':
                nActive_R = nActive_R + 1
            elif voter[8] == 'U':
                nActive_U = nActive_U + 1
            elif voter[8] == 'G':
                nActive_G = nActive_G + 1
            elif voter[8] == 'L':
                nActive_L = nActive_L + 1
                
        elif voter[7] == 'I':
            nInactive = nInactive + 1
        else:
            print 'Voter with Active State =', voter[7]
                
    print 'Number of voters on file:\t\t\t', len(voterList)
    print 'Number of inactive voters on file:\t\t', nInactive
    print 'Number of active voters on file:\t\t', nActive

    print 'Number of active voters on file (Democrat):\t', nActive_D,'\t({0:.1f}% of active voters)'.format(100*nActive_D/float(nActive))
    print 'Number of active voters on file (Republican):\t', nActive_R,'\t({0:.1f}% of active voters)'.format(100*nActive_R/float(nActive))
    print 'Number of active voters on file (Unaffiliated):\t', nActive_U,'\t({0:.1f}% of active voters)'.format(100*nActive_U/float(nActive))
    print 'Number of active voters on file (Green):\t', nActive_G,'\t({0:.1f}% of active voters)'.format(100*nActive_G/float(nActive))
    print 'Number of active voters on file (Libertarian):\t', nActive_L,'\t({0:.1f}% of active voters)'.format(100*nActive_L/float(nActive))
    print '=============================================================================='



# 0. *** Open JSON files of subsamples
with open('masterFlatVoterFile.json') as data_file:
    data0 = json.load(data_file)
with open('masterFlatVoterFile_subSample_1.json') as data_file:
    data1 = json.load(data_file)
with open('masterFlatVoterFile_subSample_2.json') as data_file:
    data2 = json.load(data_file)
with open('masterFlatVoterFile_subSample_3.json') as data_file:
    data3 = json.load(data_file)
with open('masterFlatVoterFile_subSample_4.json') as data_file:
    data4 = json.load(data_file)
with open('masterFlatVoterFile_subSample_5.json') as data_file:
    data5 = json.load(data_file)
with open('masterFlatVoterFile_subSample_6.json') as data_file:
    data6 = json.load(data_file)

printSummary(data0, '0')   
printSummary(data1, '1')
printSummary(data2, '2')
printSummary(data3, '3')
printSummary(data4, '4')
printSummary(data5, '5')
printSummary(data5, '6')
