### Author: Ben Tannenwald
### Date: Oct 18, 2017
### Purpose: make flat voter file JSON

import json

voterFile = open('CITY_OR_VILLAGE_COLUMBUS.txt', 'r')

i, voters, voterDict = 0, [], {}
with open('CITY_OR_VILLAGE_COLUMBUS.txt' , 'r') as voterFile:
    headerLine = voterFile.readline()
    print "Starting to process voter file....."
    #['STATE ID', 'COUNTY ID', 'REGISTERED', 'LASTNAME', 'FIRSTNAME', 'MIDDLE', 'SUFFIX', 'STATUS', 'PARTY', 'DATE OF BIRTH', 'RES_HOUSE', 'RES_FRAC', 'RES STREET', 'RES_APT', 'RES_CITY', 'RES_STATE', 'RES_ZIP', 'PRECINCT', 'PRECINCT SPLIT', 'PRECINCT_NAME_WITH_SPLIT', 'HOUSE', 'SENATE', 'CONGRESSIONAL', 'CITY OR VILLAGE', 'TOWNSHIP', 'SCHOOL', 'FIRE', 'POLICE', 'PARK', 'ROAD', '052017-P', '112016-G', '082016-S', '032016-P', '112015-G', '052015-P', '112014-G', '052014-P', '112013-G', '052013-P', '112012-G', '032012-P', '112011-G', '082011-L', '052011-P', '112010-G', '052010-P', '112009-G', '082009-S', '052009-P', '112008-G', '032008-P', '112007-G', '082007-S', '052007-P', '022007-L', '112006-G', '082006-L', '052006-P', '022006-L', '112005-G', '052005-P', '022005-L', '112004-G', '032004-P', '112003-G', '082003-S', '052003-L', '022003-S', '112002-G', '082002-S', '052002-P', '112001-G', '082001-S', '052001-L', '022001-S', '112000-G', '032000-P\r\n']
    for voterLine in voterFile:
        # **  Make general flat list  **
        voters.append(voterLine.split('\t'))
        
        ## **  Make dict sorted by State ID  **
        #tempDict = {}
        #stateID = voterLine.split('\t')[0]
        ## **  Make sub-dict of non-stateID elements  **
        ##print len(headerLine.split('\t')), len(voterLine.split('\t'))
        #for j, column in enumerate(headerLine.split('\t')):
        #    #print column, headerLine.index(column), j
        #    if j > 0:
        #       tempDict[column] = voterLine.split('\t')[j]
        #if i < 5:
        #    print j, tempDict
        ## **  Check if State ID already in keys [SHOULDN'T BE]  **
        #if stateID not in voterDict.keys():
        #    voterDict[stateID] = tempDict
        #else:
        #    print 'AHHHHH, non-unique State IDs. Not sure what to do about this !!!!!!!!!!!!!!!!!!!!!!!!!!'                     
        i=i+1
        if i%50000 == 0:
            print 'Processed', i, 'Voters'
            
print '\nSimple Summary\n=============================================================================='
nActive, nInactive, nActive_D, nActive_R, nActive_U, nActive_G, nActive_L = 0,0,0,0,0,0,0
for voter in voters:
    if voter[7] == 'A':
        nActive = nActive + 1
        if voter[8] == 'D':
            nActive_D = nActive_D + 1
        elif voter[8] == 'R':
            nActive_R = nActive_R + 1
        elif voter[8] == 'U':
            nActive_U = nActive_U + 1
        elif voter[8] == 'G':
            nActive_G = nActive_G + 1
        elif voter[8] == 'L':
            nActive_L = nActive_L + 1

        #else: # comment out so external users don't panic --> odd voters still get written to JSON
        #    print 'Active voter with PARTY =', voter[8], voter
    elif voter[7] == 'I':
        nInactive = nInactive + 1
    else:
        print 'Voter with Active State =', voter[7]
        
#print headerLine.split('\t')#, '\n\n', voters[1].split('\t'), '\n\n', voters[34].split('\t'), '\n\n', voters[456].split('\t')
print 'Number of voters on file:\t\t\t', len(voters)
print 'Number of inactive voters on file:\t\t', nInactive
print 'Number of active voters on file:\t\t', nActive

print 'Number of active voters on file (Democrat):\t', nActive_D,'\t({0:.1f}% of active voters)'.format(100*nActive_D/float(nActive))
print 'Number of active voters on file (Republican):\t', nActive_R,'\t({0:.1f}% of active voters)'.format(100*nActive_R/float(nActive))
print 'Number of active voters on file (Unaffiliated):\t', nActive_U,'\t({0:.1f}% of active voters)'.format(100*nActive_U/float(nActive))
print 'Number of active voters on file (Green):\t', nActive_G,'\t({0:.1f}% of active voters)'.format(100*nActive_G/float(nActive))
print 'Number of active voters on file (Libertarian):\t', nActive_L,'\t({0:.1f}% of active voters)'.format(100*nActive_L/float(nActive))
print '=============================================================================='

print '\nWriting flat JSON....'

with open('masterFlatVoterFile.json', 'w') as fp:
    json.dump(voters, fp)

