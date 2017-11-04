# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Run simple tests on SQLite DB 

import sqlite3

def runQuery(db, label, string):
    """Run query using passed string"""
    print "=====   {0}   =====".format(label)
    db.execute(string) 
    result = cursor.fetchall() 
    for r in result:
        print(list(r))

    return

#runQuery(cursor, 'Active Voters Who Voted in P_052015', "SELECT DISTINCT P_052015, COUNT(P_052015) FROM voterFile where STATUS like 'A' group by P_052015") 

connection = sqlite3.connect("voterFile.db")
cursor = connection.cursor()
