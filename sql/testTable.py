# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Run simple tests on SQLite DB 

import sqlite3, math

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

    
def runQuery(db, label, string):
    """Run query using passed string"""
    print "=====   {0}   =====".format(label)
    db.execute(string) 
    result = cursor.fetchall() 
    for r in result:
        print(list(r))

    return



connection = sqlite3.connect("voterFile.db")
connection.create_aggregate("stdev", 1, StdevFunc)
cursor = connection.cursor()

"""
cursor.execute("SELECT * FROM voterFile") 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print(r)
cursor.execute("SELECT * FROM voterFile") 
print("\nfetch one:")
res = cursor.fetchone() 
print(res)
"""

#runQuery(cursor, 'Voters Registered after Jan 1, 2010', "SELECT  PARTY,REGISTERED,DATE_OF_BIRTH,P_032000 FROM voterFile where REGISTERED >= Datetime('2010-01-01 00:00:00')")
         
runQuery(cursor, '# Voters In Each Sub-sample', 'SELECT DISTINCT SUBSAMPLE, COUNT(SUBSAMPLE) FROM voterFile group by SUBSAMPLE')
runQuery(cursor, 'Voters By Party', 'SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile group by PARTY')
runQuery(cursor, 'Active Voters By Party', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' group by PARTY")
runQuery(cursor, 'Active Voters By Party (G0)', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' and SUBSAMPLE==0 group by PARTY")
#runQuery(cursor, 'Active Voters By Party (G1)', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' and SUBSAMPLE==1 group by PARTY") 
runQuery(cursor, 'Active Voters By Party (G2)', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' and SUBSAMPLE==2 group by PARTY") 
#runQuery(cursor, 'Active Voters By Party (G3)', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' and SUBSAMPLE==3 group by PARTY") 
#runQuery(cursor, 'Active Voters By Party (G4)', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' and SUBSAMPLE==4 group by PARTY") 
#runQuery(cursor, 'Active Voters By Party (G5)', "SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' and SUBSAMPLE==5 group by PARTY") 
runQuery(cursor, 'Active Voters Who Voted in P_052015', "SELECT DISTINCT P_052015, COUNT(P_052015) FROM voterFile where STATUS like 'A' group by P_052015") 
runQuery(cursor, 'Active Voters Who Voted in G_112014', "SELECT DISTINCT G_112014, COUNT(G_112014) FROM voterFile where STATUS like 'A' group by G_112014") 
runQuery(cursor, 'Voter Behavior in 2015 General If Voted in 2015 Primary', "SELECT DISTINCT G_112015, COUNT(G_112015) FROM voterFile where STATUS like 'A' and P_052015 not like '' group by G_112015") 
runQuery(cursor, 'Voter Behavior in 2015 Primary If Voted in 2015 General', "SELECT DISTINCT P_052015, COUNT(P_052015) FROM voterFile where STATUS like 'A' and G_112015 not like '' group by P_052015")
runQuery(cursor, 'Voter Behavior in 2014 General If Voted in 2015 General', "SELECT DISTINCT G_112014, COUNT(G_112014) FROM voterFile where STATUS like 'A' and G_112015 not like '' group by G_112014") 
runQuery(cursor, 'Voter Behavior in 2014 Primary If Voted in 2015 General', "SELECT DISTINCT P_052014, COUNT(P_052014) FROM voterFile where STATUS like 'A' and G_112015 not like '' group by P_052014") 

#runQuery(cursor, 'Correlation?', "SELECT (Avg(P_052014 * G_112014) - Avg(P_052014) * Avg(G_112014)) / (stdev(P_052014) * stdev(G_112014)) AS Correlation FROM voterFile where STATUS like 'A'")



