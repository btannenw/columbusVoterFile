# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Script for analyzing SQL voter file, e.g. calculate correlations, do linear regressions, etc

import sqlite3
from voterFileSQL import *

# 0. ***  Connect to SQL database
connection = sqlite3.connect("../sql/voterFile.db")
connection.create_aggregate("stdev", 1, StdevFunc)
cursor = connection.cursor()

# 1. ***  Print some simple summaries
#printSimpleSummary(cursor)
printSimpleSummary(cursor, subsample='0')


# 2. ***  Calculate some correlations
#calculateCorrelation('registered2012P', 'P_032012', 'G_112013', 'Testing 2012 Primary vs 2012 General')
calculateCorrelation(cursor, 'P_052014 v G_112014', ['P_052014', 'G_112014'])
calculateCorrelation(cursor, 'P_052014 v G_112014 (Active)', ['P_052014', 'G_112014'], constraints="STATUS like 'A'")
calculateCorrelation(cursor, 'P_052014 v G_112014 (G0)', ['P_052014', 'G_112014'], subsample='0')
calculateCorrelation(cursor, 'P_052014 v G_112014 (Active, G0)', ['P_052014', 'G_112014'], "STATUS like 'A'", subsample='0')
calculateCorrelation(cursor, 'P_052014 v G_112014 (Active, G0, Registered 2010)', ['P_052014', 'G_112014'], "STATUS like 'A' and REGISTERED >= Datetime('2010-01-01 00:00:00')", subsample='0')
calculateCorrelation(cursor, 'P_052014 v G_112014 (Active, G0, Voted G)', ['P_052014', 'G_112014'], "STATUS like 'A' and P_052015 == 1", subsample='0')
             

