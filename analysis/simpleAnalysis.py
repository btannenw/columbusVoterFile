### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: script for analyzing voter file, e.g. calculate correlations, do linear regressions, etc

import json
from voterFile import voterFile, voterParser


# 0. *** Open JSON files of subsamples
with open('../makeSamples/masterFlatVoterFile_subSample_1.json') as data_file:
    subSample1 = json.load(data_file)
with open('../makeSamples/masterFlatVoterFile_subSample_2.json') as data_file:
    subSample2 = json.load(data_file)

# 1. ***  Create voterFile  ***
vFile1 = voterFile(subSample1)
vFile2 = voterFile(subSample2)
vFile1.printSimpleSummary()

# 2. ***  Calculate some correlations  ***
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General')
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General (R)',party='R')
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General (U)',party='U')
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General (D)',party='D')
#vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General (D, R)',party=['D','R'])
vFile1.calculateCorrelation('registered2012P', 'P_032012', 'G_112014', 'Testing 2012 Primary vs 2014 General (R)',party='R')
vFile1.calculateCorrelation('registered2012P', 'G_112013', 'G_112014', 'Testing 2013 General vs 2014 General (R)',party='R')
vFile1.calculateCorrelation('registered2012P', 'P_052014', 'G_112014', 'Testing 2014 Primary vs 2014 General (R)',party='R')

# 3. ***  Perform linear regressions  ***
vFile1.doLinearRegression(registered='registered2012P', elections=['P_032012', 'G_112013', 'P_052014', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2012P', elections=['P_032012', 'P_052014', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'P_052014', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'G_112014'], party='R')
vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'G_112014'], party='U')
w, resid = vFile1.doLinearRegression(registered='registered2012P', elections=['G_112013', 'G_112014'])

# 4. ***  Compare prediction to reality using second subsample  ***
vFile2.validateFit( registered='registered2012P', elections=['G_112013', 'G_112014'], fitParams=w, residual=resid, party='R' )
vFile2.validateFit( registered='registered2012P', elections=['G_112013', 'G_112014'], fitParams=w, residual=resid )

