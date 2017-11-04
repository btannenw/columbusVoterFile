### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: script for analyzing voter file, e.g. calculate correlations, do linear regressions, etc

import json, matplotlib.pyplot as plt
from voterFile import voterFile, voterParser


# 0. *** Open JSON files of subsamples
with open('../makeSamples/masterFlatVoterFile_subSample_1.json') as data_file:
    subSample1 = json.load(data_file)
with open('../makeSamples/masterFlatVoterFile_subSample_2.json') as data_file:
    subSample2 = json.load(data_file)
with open('../makeSamples/masterFlatVoterFile_subSample_3.json') as data_file:
    subSample3 = json.load(data_file)

# 1. ***  Create voterFile  ***
vFile1 = voterFile(subSample1)
vFile2 = voterFile(subSample2)
vFile3 = voterFile(subSample3)
vFile1.printSimpleSummary()

# 2. ***  Calculate some correlations  ***
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General')
#vFile1.calculateCorrelation('registered2012P', 'P_052014', 'G_112014', 'Testing 2014 Primary vs 2014 General')
#vFile2.calculateCorrelation('registered2012P', 'P_052014', 'G_112014', 'Testing 2014 Primary vs 2014 General')
#vFile3.calculateCorrelation('registered2012P', 'P_052014', 'G_112014', 'Testing 2014 Primary vs 2014 General')
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General (R)',party='R')
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General (D, R)',party=['D','R'])
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (U)',party='U',nTimesVoted=1)
#vFile1.makeCorrelationPlots('registered2012P', ['P_032012', 'G_112012'], 'G2012_R', party = 'R')
#vFile1.makeCorrelationPlots('registered2012P', ['P_032012', 'G_112012', 'P_052013', 'G_112013', 'P_052014', 'G_112014'], 'G2014_R', party = 'R')
#vFile1.makeCorrelationPlots('registered2012P', ['P_032012', 'G_112012', 'P_052013', 'G_112013', 'P_052014', 'G_112014', 'P_052015', 'G_112015'], 'G2015_R', party = 'R')
#vFile1.makeCorrelationPlots('registered2012P', ['P_032012', 'G_112012', 'P_052013', 'G_112013', 'P_052014', 'G_112014', 'P_052015', 'G_112015', 'P_032016', 'G_112016'], 'G2016_R', party = 'R')
#vFile1.makeCorrelationPlots('registered2012P', ['P_032012', 'G_112012', 'P_052013', 'G_112013', 'P_052014', 'G_112014', 'P_052015', 'G_112015', 'P_032016', 'G_112016', 'P_052017'], 'P2017_R', party = 'R')

# 3. ***  Perform linear regressions  ***
vFile1.doLinearRegression(registered='registered2012P', elections=['P_032012', 'G_112013', 'P_052014', 'G_112014'])
vFile1.doLinearRegression(registered='registered2012P', elections=['P_032012', 'G_112013', 'P_052014', 'G_112014'], party = 'R')
vFile1.doLinearRegression(registered='registered2012P', elections=['P_032012', 'G_112013', 'P_052014', 'G_112014'], party = 'D')
#vFile1.doLinearRegression(registered='registered2012P', elections=['P_032012', 'P_052014', 'G_112014'], party='R')
#vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'P_052014', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2013G', elections=['G_112013', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2014P', elections=['P_052014', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2013G', elections=['G_112013', 'P_052014', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2013G', elections=['G_112013', 'G_112014'], party='D')
vFile1.doLinearRegression(registered='registered2014P', elections=['P_052014', 'G_112014'], party='D')
vFile1.doLinearRegression(registered='registered2013G', elections=['G_112013', 'P_052014', 'G_112014'], party='D')

#vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'G_112014'], party='U', nTimesVoted=1)
w, resid = vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'G_112014'])

# 4. ***  Compare prediction to reality using second subsample  ***
#vFile2.validateFit( registered='registered2012P', elections=['G_112013', 'G_112014'], fitParams=w, residual=resid, party='R' )
prediction = vFile2.validateFit( registered='registered2012P', elections=['G_112013', 'G_112014'], fitParams=w, residual=resid )

# 5. ***  Dump .txt file printing out # likely voters in analyzed precincts  ***
vFile2.dumpLikelyVotersByPrecinct(prediction, 'subsample2', registered='registered2012P', election='G_112014')
vFile3.dumpLikelyVotersByPrecinct(prediction, 'subsample3', registered='registered2012P', election='G_112014')

plt.show()

