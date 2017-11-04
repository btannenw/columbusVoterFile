import sqlite3
connection = sqlite3.connect("voterFile.db")

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

"""
cursor.execute("SELECT  PARTY,REGISTERED,DATE_OF_BIRTH,P_032000 FROM voterFile") 
result = cursor.fetchall() 
for r in result:
    print(r)

print "============================"
cursor.execute("SELECT  PARTY,REGISTERED,DATE_OF_BIRTH,P_032000 FROM voterFile where REGISTERED >= Datetime('2010-01-01 00:00:00')") 
result = cursor.fetchall() 
for r in result:
    print(r)
"""
print "======  # Voters In Each Sub-sample  ====="
cursor.execute("SELECT DISTINCT SUBSAMPLE, COUNT(SUBSAMPLE) FROM voterFile group by SUBSAMPLE") 
result = cursor.fetchall() 
for r in result:
    print(r)
print "=========     Voters By Party    ========="
cursor.execute("SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile group by PARTY") 
result = cursor.fetchall() 
for r in result:
    print(r)
print "=======    Active Voters By Party   ======"
cursor.execute("SELECT DISTINCT PARTY, COUNT(PARTY) FROM voterFile where STATUS like 'A' group by PARTY") 
result = cursor.fetchall() 
for r in result:
    print(r)
