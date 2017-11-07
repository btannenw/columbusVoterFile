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
        return math.sqrt(self.S / (self.k-1))


# ***  II.  Functions
def runQuery(db, label, string, quiet = False):
    """Run query using passed string"""

    #print string
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

        # **  a. calculate stdev of one election
        #runQuery(db, 'Stdev(P_052014)', "SELECT stdev(P_052014) FROM voterFile where STATUS like 'A'")

        # **  b. calculate correlation between two elections
        corr = runQuery(db, 'Correlation: {0} v {1}'.format(elections[0], elections[1]), "SELECT (Avg({0} * {1}) - Avg({0}) * Avg({1})) / (stdev({0}) * stdev({1})) AS Correlation FROM voterFile {2}".format(elections[0], elections[1], constraints), quiet=True)

        print 'Correlation for {0}:\t {1:.3f}'.format(title, corr[0][0])
        
        return corr[0]


def returnBayesianProbability(db, title, elections, constraints='', subsample='', quiet=True, voted=True):
        """ function to calculate and print Bayesian probability of voting behavior between two elections given user-specified constraints """
        #  ***  P(A|B) = P(A) * P(B|A) / P(B)

        if constraints != '':
            constraints = 'where ' + constraints
            if subsample != '':
                constraints = constraints + ' and SUBSAMPLE == {0}'.format(subsample)
        else:
            if subsample != '':
                constraints = 'where SUBSAMPLE == {0}'.format(subsample)

        # ***  I. calculate bayesian relation between two elections
        # **  A. P(A)
        q_pA = runQuery(db, 'Bayesian P({0}):'.format(elections[0]), "SELECT DISTINCT {0}, count({0}) FROM voterFile {1} group by {0}".format(elections[0], constraints), quiet)
        pA = calcProbability(q_pA)
        # **  B. P(B)
        q_pB = runQuery(db, 'Bayesian P({0}):'.format(elections[1]), "SELECT DISTINCT {0}, count({0}) FROM voterFile {1} group by {0}".format(elections[1], constraints), quiet)
        pB = calcProbability(q_pB)
        # **  C. P(B|A)
        q_pBA=''
        voted = '1' if voted else '-1'
        q_pBA = runQuery(db, 'Bayesian P({0}):'.format(elections[1]), "SELECT DISTINCT {0}, count({0}) FROM voterFile {1} and {2} == {3} group by {0}".format(elections[1], constraints, elections[0], voted), quiet)
            
        pBA = calcProbability(q_pBA)

        if not quiet:
            print 'P({0}): {1:.3f}\t P({2}): {3:.3f}\t P({2}|{0}): {4:.3f}'.format(elections[0], pA, elections[1], pB, pBA)

        
        return pBA * pA / float(pB)



def calcProbability(input, voted='1'):
    """ helper function to calculate voting probability from numbers returned from SQL query"""

    num, denom = 0, 0

    for line in input:
        if line[0] == 1:
            if str(voted)=='1':
                num = line[1]
            denom = denom + line[1]
        elif line[0] == -1:
            if str(voted)=='-1':
                num = line[1]
            denom = denom + line[1]
        else:
            print "Voting info DNE 1 or -1... it's {0} ... WHAT IS HAPPENING?!?!".format(line[0])

    #print num, denom, num/float(denom)
    return num/float(denom)
                        

def returnBayesianRelation(db, title, electionTypes, yearGap, voted, constraints='', subsample='', quiet=True):
    """ function to automate calculating relation between two elections depending on whether each is primary or general (electionTypes), the years between the two elections (yearGap), and whether a voter voted in the earlier election (voted) """

    # ** 0. Start analysis in 2008. this is arbitrary choice and can be adjusted
    probabilities = []
    firstYear, lastYear = 2008, 2008 + yearGap 

    # ** 1. Loop over years
    while lastYear <= 2016:
        # make election strings
        s_lastElection  = returnElectionString(electionTypes[0], lastYear)
        s_firstElection = returnElectionString(electionTypes[1], firstYear)

        # ** 2. Set registration month
        if electionTypes[1] == 'G':
            registrationMonth = '11'
        elif electionTypes[1] == 'P' and firstYear %4 == 0:
            registrationMonth = '03'
        elif electionTypes[1] == 'P' and firstYear %4 != 0:
            registrationMonth = '05'

        # ** 3. Add registration date to constraints
        if constraints !='':
            constraintsTemp = constraints + "and REGISTERED <= Datetime('{0}-{1}-01 00:00:00')".format(str(firstYear), registrationMonth)
        else:
            constraintsTemp = "REGISTERED <= Datetime('{0}-{1}-01 00:00:00')".format(str(firstYear), registrationMonth)
             
        # ** 4. Get bayesian probability
        probabilities.append( returnBayesianProbability(db, 'P( {0} | {1} )'.format(s_lastElection, s_firstElection), [s_lastElection, s_firstElection], constraintsTemp, subsample, quiet, voted) )

        # ** 5. Increase year by one
        firstYear = firstYear + 1
        lastYear = lastYear + 1

    print 'P( {0} ) -\t Avg: {1:.3f}\t StDev: {2:.3f}'.format(title, np.mean(probabilities), np.std(probabilities))

    return np.mean(probabilities), np.std(probabilities)
    
def returnBayesianHistory(db, title, elections, voted, constraints='', subsample='', quiet=True):
    """ function to automate calculating relation between multiple elections depending on the elections (elections), the voting pattern (voted). the first election/voted pair is the election in question"""


    #  ***  P(A|B) = P(A) * P(B|A) / P(B)

    # ** 0. Make election constraint string
    electionConstraints = ''
    for i, election in enumerate(elections):
        if i == 1:
            electionConstraints = '{0} == {1}'.format(str(election), str(voted[i]))
        elif i > 1:
            electionConstraints = electionConstraints + ' and {0} == {1}'.format(str(election), str(voted[i]))

            
    # ** 1. Handle rest of constraints
    if constraints != '':
        constraints = 'where ' + constraints
        if subsample != '':
            constraints = constraints + ' and SUBSAMPLE == {0}'.format(subsample)
    else:
        if subsample != '':
            constraints = 'where SUBSAMPLE == {0}'.format(subsample)

    # ***  2. calculate bayesian relation between election and complete election history
    # **  A. P(A)
    q_pA = runQuery(db, 'Bayesian P( {0} == {1} ):'.format(elections[0], voted[0]), "SELECT DISTINCT {0}, count({0}) FROM voterFile {1} group by {0}".format(elections[0], constraints), quiet)
    pA = calcProbability(q_pA, voted[0])
    # **  B. P(B)
    case = "(CASE WHEN {0} THEN 1 ELSE -1 END)".format(electionConstraints)
    q_pB = runQuery(db, 'Bayesian P( {0} ):'.format(electionConstraints), "SELECT DISTINCT {0}, count({0}) FROM voterFile {1} group by {0}".format(case, constraints), quiet)
    pB = calcProbability(q_pB, voted[1])
    # **  C. P(B|A)
    q_pBA=''
    q_pBA = runQuery(db, 'Bayesian P( {0} | {1} == {2} ):'.format(electionConstraints, elections[0], voted[0]), "SELECT DISTINCT {0}, count({0}) FROM voterFile {1} and {2} == {3} group by {0}".format(case, constraints, elections[0], voted[0]), quiet)
            
    pBA = calcProbability(q_pBA)

    if not quiet:
        print 'P({0}): {1:.3f}\t P({2}): {3:.3f}\t P({2}|{0}): {4:.3f}'.format(elections[0], pA, elections[1], pB, pBA)

        
    return pBA * pA / float(pB)


    
def returnElectionString(generalOrPrimary, year):
    """ function for returning full election string """
    election = generalOrPrimary
    
    if generalOrPrimary == 'G':
        election = election + '_11' + str(year)
    if generalOrPrimary == 'P':
        if year%4 == 0: # presidential year and primary in march
            election = election + '_03' + str(year)
        else: # primary in may
            election = election + '_05' + str(year)

    return election
