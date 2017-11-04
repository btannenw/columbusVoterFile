# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: File to store functions for SQL-based analysis of Frankling County voting behaviors

import sqlite3, math, numpy as np, matplotlib.pyplot as plt, operator
from scipy import stats
from scipy.stats.stats import pearsonr
from numpy import arange,array,ones,linalg
from pylab import plot,show


# ***  I. Class to add stdev calculation to sqlite
class StdevFunc:
    def __init__(self):
        self.M = 0.0
        self.S = 0.0
        self.k = 1

    def step(self, value):
        if value is None:
            return
        tM = self.M
        self.M += (value - tM) / self.k
        self.S += (value - tM) * (value - self.M)
        self.k += 1

    def finalize(self):
        if self.k < 3:
            return None
        return math.sqrt(self.S / (self.k-2))


# ***  II.  Functions
def runQuery(db, label, string, quiet = False):
    """Run query using passed string"""

    db.execute(string) 
    result = db.fetchall() 
    if not quiet:
        print "=====   {0}   =====".format(label)
        for r in result:
            print(list(r))

    #runQuery(cursor, 'Active Voters Who Voted in P_052015', "SELECT DISTINCT P_052015, COUNT(P_052015) FROM voterFile where STATUS like 'A' group by P_052015") 

    return result

def returnPartyName(party):
    """ function for returning full party name"""

    if party == 'D':
        return 'Democratic'
    elif party == 'R':
        return 'Republican'
    elif party == 'U':
        return 'Unaffiliated'
    elif party == 'G':
        return 'Green'
    elif party == 'L':
        return 'Libertarian'
    else:
        return 'Unknown'

    
def printSimpleSummary(db, subsample=''):
    """ print summary of simple information for DB """

    print '================================================================================='
    if subsample != '':
        print '===============                   Sub-sample {0}                    ==============='.format(subsample)
        subsample = 'where SUBSAMPLE == {0}'.format(subsample)
        subsamplePlus = subsample + ' and'
    else:
        print '=================                   All Voters                  ================='
        subsamplePlus = 'where'
    print '================================================================================='
    
    nVoters = runQuery(db, '# Voters', 'SELECT DISTINCT COUNT(SUBSAMPLE) FROM voterFile {0};'.format(subsample), quiet=True)
    nActiveVoters = runQuery(db, '# Active Voters', "SELECT DISTINCT COUNT(SUBSAMPLE) FROM voterFile {0} STATUS like 'A';".format(subsamplePlus), quiet=True)
    nActiveVotersByParty = runQuery(db, '# Active Voters By Party', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile {0} STATUS like 'A' group by PARTY;".format(subsamplePlus), quiet=True)

    print 'Number of voters on file:\t\t\t', nVoters[0][0]
    print 'Number of active voters on file:\t\t', nActiveVoters[0][0]
    for query in nActiveVotersByParty:
        print 'Number of active voters on file ({0}):\t {1} \t({2:.1f}% of active voters)'.format( returnPartyName(query[0]), query[1], 100*query[1]/nActiveVoters[0][0] )
    print '=================================================================================\n'
    

def calculateCorrelation(db, title, elections, constraints='', subsample=''):
        """ function to calculate and print correlation between voting behavior given user-specified constraints """

        if constraints != '':
            constraints = 'where ' + constraints
            if subsample != '':
                constraints = constraints + ' and SUBSAMPLE == {0}'.format(subsample)
        else:
            if subsample != '':
                constraints = 'where SUBSAMPLE == {0}'.format(subsample)

        print constraints
        # **  a. calculate stdev of one election
        #runQuery(db, 'Stdev(P_052014)', "SELECT stdev(P_052014) FROM voterFile where STATUS like 'A'")

        # **  b. calculate correlation between two elections
        corr = runQuery(db, 'Correlation: {0} v {1}'.format(elections[0], elections[1]), "SELECT (Avg({0} * {1}) - Avg({0}) * Avg({1})) / (stdev({0}) * stdev({1})) AS Correlation FROM voterFile {2}".format(elections[0], elections[1], constraints), quiet=False)

        print 'Correlation for {0}:\t {1:.2f}'.format(title, corr[0][0])
        
        return corr[0]

