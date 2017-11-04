### Author: Ben Tannenwald
### Date: Nov 4, 2017
### Purpose: make SQLite voter table

import os, sqlite3
os.system("rm voterFile.db")
connection = sqlite3.connect("voterFile.db")
cursor = connection.cursor()


sql_command = """
CREATE TABLE voterFile ( 

STATE_ID TEXT,
COUNTY_ID TEXT,
REGISTERED DateTime,
LASTNAME TEXT,
FIRSTNAME TEXT, 
MIDDLE TEXT,
SUFFIX TEXT, 
STATUS TEXT,
PARTY TEXT,
DATE_OF_BIRTH INT,
RES_HOUSE TEXT,
RES_FRAC TEXT,
RES_STREET TEXT,
RES_APT TEXT,
RES_CITY TEXT,
RES_STATE TEXT,
RES_ZIP TEXT,
PRECINCT TEXT,
PRECINCT_SPLIT TEXT,
PRECINCT_NAME_WITH_SPLIT TEXT,
HOUSE TEXT,
SENATE TEXT,
CONGRESSIONAL TEXT,
CITY_OR_VILLAGE TEXT,
TOWNSHIP TEXT,
SCHOOL TEXT,
FIRE TEXT,
POLICE TEXT,
PARK TEXT,
ROAD TEXT,
P_052017 INT,
G_112016 INT,
S_082016 INT,
P_032016 INT,
G_112015 INT,
P_052015 INT,
G_112014 INT,
P_052014 INT,
G_112013 INT,
P_052013 INT,
G_112012 INT,
P_032012 INT,
G_112011 INT,
L_082011 INT,
P_052011 INT,
G_112010 INT,
P_052010 INT,
G_112009 INT,
S_082009 INT,
P_052009 INT,
G_112008 INT,
P_032008 INT,
G_112007 INT,
S_082007 INT,
P_052007 INT,
L_022007 INT,
G_112006 INT,
L_082006 INT,
P_052006 INT,
L_022006 INT,
G_112005 INT,
P_052005 INT,
L_022005 INT,
G_112004 INT,
P_032004 INT,
G_112003 INT,
S_082003 INT,
L_052003 INT,
S_022003 INT,
G_112002 INT,
S_082002 INT,
P_052002 INT,
G_112001 INT,
S_082001 INT,
L_052001 INT,
S_022001 INT,
G_112000 INT,
P_032000 INT,
SUBSAMPLE INT
);"""


cursor.execute(sql_command)

voterFile = open('../makeSamples/CITY_OR_VILLAGE_COLUMBUS.txt', 'r')
print "Starting to process voter file....."
    #['STATE ID', 'COUNTY ID', 'REGISTERED', 'LASTNAME', 'FIRSTNAME', 'MIDDLE', 'SUFFIX', 'STATUS', 'PARTY', 'DATE OF BIRTH', 'RES_HOUSE', 'RES_FRAC', 'RES STREET', 'RES_APT', 'RES_CITY', 'RES_STATE', 'RES_ZIP', 'PRECINCT', 'PRECINCT SPLIT', 'PRECINCT_NAME_WITH_SPLIT', 'HOUSE', 'SENATE', 'CONGRESSIONAL', 'CITY OR VILLAGE', 'TOWNSHIP', 'SCHOOL', 'FIRE', 'POLICE', 'PARK', 'ROAD', '052017-P', '112016-G', '082016-S', '032016-P', '112015-G', '052015-P', '112014-G', '052014-P', '112013-G', '052013-P', '112012-G', '032012-P', '112011-G', '082011-L', '052011-P', '112010-G', '052010-P', '112009-G', '082009-S', '052009-P', '112008-G', '032008-P', '112007-G', '082007-S', '052007-P', '022007-L', '112006-G', '082006-L', '052006-P', '022006-L', '112005-G', '052005-P', '022005-L', '112004-G', '032004-P', '112003-G', '082003-S', '052003-L', '022003-S', '112002-G', '082002-S', '052002-P', '112001-G', '082001-S', '052001-L', '022001-S', '112000-G', '032000-P\r\n']
for i,voterLine in enumerate(voterFile):

    if i == 0: # skip first line
        print voterLine.split('\t')
        print len(voterLine.split('\t'))
        continue
    
    #if i < 10:
    #print voterLine.split('\t')
    #print i, len(voterLine.split('\t'))
    format_str = """INSERT INTO voterFile (STATE_ID, COUNTY_ID, REGISTERED, LASTNAME, FIRSTNAME, MIDDLE, SUFFIX, STATUS, PARTY, DATE_OF_BIRTH, RES_HOUSE, RES_FRAC, RES_STREET, RES_APT, RES_CITY, RES_STATE, RES_ZIP, PRECINCT, PRECINCT_SPLIT, PRECINCT_NAME_WITH_SPLIT, HOUSE, SENATE, CONGRESSIONAL, CITY_OR_VILLAGE, TOWNSHIP, SCHOOL, FIRE, POLICE, PARK, ROAD, P_052017, G_112016, S_082016, P_032016, G_112015, P_052015, G_112014, P_052014, G_112013, P_052013, G_112012, P_032012, G_112011, L_082011, P_052011, G_112010, P_052010, G_112009, S_082009, P_052009, G_112008, P_032008, G_112007, S_082007, P_052007, L_022007, G_112006, L_082006, P_052006, L_022006, G_112005, P_052005, L_022005, G_112004, P_032004, G_112003, S_082003, L_052003, S_022003, G_112002, S_082002, P_052002, G_112001, S_082001, L_052001, S_022001, G_112000, P_032000, SUBSAMPLE)
        VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}","{16}","{17}","{18}","{19}","{20}","{21}","{22}","{23}","{24}","{25}","{26}","{27}","{28}","{29}","{30}","{31}","{32}","{33}","{34}","{35}","{36}","{37}","{38}","{39}","{40}","{41}","{42}","{43}","{44}","{45}","{46}","{47}","{48}","{49}","{50}","{51}","{52}","{53}","{54}","{55}","{56}","{57}","{58}","{59}","{60}","{61}","{62}","{63}","{64}","{65}","{66}","{67}","{68}","{69}","{70}","{71}","{72}","{73}","{74}","{75}","{76}","{77}","{78}");"""

    # a few fixes by hand
    inputs = voterLine.split('\t')
    month = inputs[2].split('/')[0] if len(inputs[2].split('/')[0]) == 2 else '0'+inputs[2].split('/')[0]
    day   = inputs[2].split('/')[1] if len(inputs[2].split('/')[1]) == 2 else '0'+inputs[2].split('/')[1]
    inputs[2] = '{0}-{1}-{2}'.format(inputs[2].split('/')[2], month, day)
    inputs[9] = int(inputs[9])
    inputs[77] = inputs[77].split('\r')[0]
    # make election history numeric
    for j,input in enumerate(inputs):
        if j >= 30 and j <78:
            inputs[j] = 1 if input != '' else -1


    inputs.append(i%6)
    sql_command = format_str.format(*inputs)
    cursor.execute(sql_command)    
        
    if i%50000 == 0:
        print 'Processed {0} Voters'.format(i)

# never forget this, if you want the changes to be saved:
connection.commit()

connection.close()
