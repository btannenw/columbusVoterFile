# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Run simple tests on SQLite DB 

import sqlite3

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
    

