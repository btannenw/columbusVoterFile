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

vFile.calculateCorrelation('registered2016P', 'P_032016', 'G_112016', 'Testing 2016 Primary vs 2016 General')
vFile.calculateCorrelation('registered2015G', 'G_112015', 'G_112016', 'Testing 2015 General vs 2016 General')
vFile.calculateCorrelation('registered2015G', 'G_112015', 'P_032016', 'Testing 2015 General vs 2016 Primary')
vFile.calculateCorrelation('registered2015P', 'G_112015', 'P_032016', 'Testing 2015 General vs 2016 Primary')
vFile.calculateCorrelation('registered2012P', 'P_032012', 'G_112016', 'Testing 2012 Primary vs 2016 General')
vFile.calculateCorrelation('registered2012G', 'G_112012', 'G_112016', 'Testing 2012 Primary vs 2016 General')
vFile.calculateCorrelation('registered2015P', 'P_052015', 'G_112015', 'Testing 2015 Primary vs 2015 General')
vFile.calculateCorrelation('registered2014P', 'P_052014', 'G_112014', 'Testing 2014 Primary vs 2014 General')
vFile.calculateCorrelation('registered2013P', 'P_052013', 'G_112013', 'Testing 2013 Primary vs 2013 General')
vFile.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General')
vFile.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (R)',party='R')
vFile.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (U)',party='U')
vFile.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (D)',party='D')
vFile.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (D, R)',party=['D','R'])
vFile.calculateCorrelation('registered2011P', 'P_052011', 'G_112011', 'Testing 2011 Primary vs 2011 General')
vFile.calculateCorrelation('registered2010P', 'P_052010', 'G_112010', 'Testing 2010 Primary vs 2010 General')
vFile.calculateCorrelation('registered2009P', 'P_052009', 'G_112009', 'Testing 2009 Primary vs 2009 General')
vFile.calculateCorrelation('registered2008P', 'P_032008', 'G_112008', 'Testing 2008 Primary vs 2008 General')
