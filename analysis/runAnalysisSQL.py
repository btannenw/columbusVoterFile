# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Script for analyzing SQL voter file, e.g. calculate correlations, do linear regressions, etc

import sqlite3
from voterFileSQL import *

# 0. ***  Connect to SQL database
connection = sqlite3.connect("../sql/voterFile.db")
cursor = connection.cursor()


# 1. ***  Print some simple summaries
#printSimpleSummary(cursor)
printSimpleSummary(cursor, subsample='0')


# 2. ***  Print some simple summaries

