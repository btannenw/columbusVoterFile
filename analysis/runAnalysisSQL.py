# Author:  Ben Tannenwald
# Date:    November 4, 2017
# Purpose: Script for analyzing SQL voter file, e.g. calculate correlations, do linear regressions, etc

import sqlite3

connection = sqlite3.connect("voterFile.db")
cursor = connection.cursor()
