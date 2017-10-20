### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: class to provide human-readable functions to parse each voter in the JSON'ed voter file AND class to hold dictionary of parsed voters

import numpy as np
from scipy.stats.stats import pearsonr

class voterFile(object):
    """A class for parsing voter file information.

    Attributes:
        nInactive:         number of inactive voters
        nActive:           number of active voters
        nActive_U:         number of active voters registered as Unaffiliated
        nActive_R:         number of active voters registered as Republican
        nActive_D:         number of active voters registered as Democrat
        nActive_L:         number of active voters registered as Libertarian
        nActive_G:         number of active voters registered as Green

        countVotersByStatusAndParty:    return number of voters by status and party
        printSimpleSummary:             print summary of counts of simple voter categories
        makeElectionList:               return list of vote history for an election using only eligible voters
        calculateCorrelation:           calculate and print correlation between voting behavior in two elections
    """
    
    # Members

    # Functions
    def __init__(self, infile):
        self.voters = []
        for line in infile:
            voter = voterParser(line)
            self.voters.append(voter)

        self.nInactive = self.countVotersByStatusAndParty(status='I')
        self.nActive = self.countVotersByStatusAndParty(status='A')
        self.nActive_R = self.countVotersByStatusAndParty(status='A', party='R')
        self.nActive_D = self.countVotersByStatusAndParty(status='A', party='D')
        self.nActive_L = self.countVotersByStatusAndParty(status='A', party='L')
        self.nActive_G = self.countVotersByStatusAndParty(status='A', party='G')
        self.nActive_U = self.countVotersByStatusAndParty(status='A', party='U')

    def calculateCorrelation(self, registered, election1, election2, title, activeOnly=True, party=[]):
        """ function to calculate and print correlation between voting behavior in two elections"""

        voted1 = self.makeElectionList(registered, election1, activeOnly, party)
        voted2 = self.makeElectionList(registered, election2, activeOnly, party)

        array1 = np.array(voted1)
        array2 = np.array(voted2)
        corr, pvalue = pearsonr(array1, array2)
        print title, ', correlation =', corr, ', p-value =', pvalue
        
    def makeElectionList(self, registered, election, activeOnly, party):
        """ function to return list of vote history for an election using only eligible voters"""

        electionList = []
        for voter in self.voters:
            activeStatus = True if voter.status=='A' or not activeOnly else False
            if party is str: # make party list if single string
                party = [party]
            partyFilter  = True if len(party)==0 or (len(party)>0 and voter.party in party) else False 
            
            if getattr(voter, registered) and getattr(voter, election) and activeStatus and partyFilter:
                #electionList.append(True)
                electionList.append(1)
            elif getattr(voter, registered) and not getattr(voter, election) and activeStatus and partyFilter:
                #electionList.append(False)
                electionList.append(-1)
            
            #elif not getattr(voter, registered): ### only for debugging!!!
            #    electionList.append('X')
            #    temp = 'X'
            #print voter.name, voter.registrationDate, voter.registered2016P, int(voter.registrationDate.split('/')[2].split(' ')[0]), voter.G_112016, temp
            
        return electionList
    
    def countVotersByStatusAndParty(self, status, party=''):
        """function for returning voters of a specified status (Active/Inactive) and party(U/R/D/L/G)"""

        nVoters = 0
        
        for voter in self.voters:
            if party == '':
                if voter.status == status:
                    nVoters = nVoters + 1
            else:
                if voter.status == status and voter.party == party:
                    nVoters = nVoters + 1

        return nVoters

    def printSimpleSummary(self):
        """ function to print simple summary of voter-type counts"""

        print '================================================================================='
        print 'Number of voters on file:\t\t\t', len(self.voters)
        print 'Number of inactive voters on file:\t\t', self.nInactive
        print 'Number of active voters on file:\t\t', self.nActive
        
        print 'Number of active voters on file (Democrat):\t', self.nActive_D,'\t({0:.1f}% of active voters)'.format(100*self.nActive_D/float(self.nActive))
        print 'Number of active voters on file (Republican):\t', self.nActive_R,'\t({0:.1f}% of active voters)'.format(100*self.nActive_R/float(self.nActive))
        print 'Number of active voters on file (Unaffiliated):\t', self.nActive_U,'\t({0:.1f}% of active voters)'.format(100*self.nActive_U/float(self.nActive))
        print '=================================================================================\n\n'


####################################  Class for parsing voter list  ####################################
        
class voterParser(object):
    """A class for parsing voter file information.

    Attributes:
        stateID:           state ID of voter
        countyID:          county ID of voter
        registrationDate:  date of voter registration 
        name:              voter name (first, middle, last)
        status:            voter status: Active or Inactive
        party:             registered party of voter
        dob:               date of birth of voter
        street:            street of voter's address
        zipcode:           zipcode of voter
        precint:           ohio precint of voter
        house:             ohio state house district of voter
        senate:            ohio state senate district of voter
        congress:          US congressional district of voter

        P_052017:          true if voter voted in May 2017 primary
        X_MMYYYY:          true if voter voted in X (P=primary, G= general, S=special, L=local?) election in month MM in year YYYY

        registered2008P:    true if voter registered before primary month in 2008
        registered2008G:    true if voter registered before general month in 2008
        registered2009P:    true if voter registered before primary month in 2009
        registered2009G:    true if voter registered before general month in 2009
        registered2010P:    true if voter registered before primary month in 2010
        registered2010G:    true if voter registered before primary month in 2010
        registered2011P:    true if voter registered before primary month in 2011
        registered2011G:    true if voter registered before primary month in 2011
        registered2012P:    true if voter registered before primary month in 2012
        registered2012G:    true if voter registered before primary month in 2012
        registered2013P:    true if voter registered before primary month in 2013
        registered2013G:    true if voter registered before primary month in 2013
        registered2014P:    true if voter registered before primary month in 2014
        registered2014G:    true if voter registered before primary month in 2014
        registered2015P:    true if voter registered before primary month in 2015
        registered2015G:    true if voter registered before primary month in 2015
        registered2016P:    true if voter registered before primary month in 2016
        registered2016G:    true if voter registered before primary month in 2016
        registered2017P:    true if voter registered before primary month in 2017
        registered2017G:    true if voter registered before primary month in 2017      
    """

    # Members
    #['STATE ID', 'COUNTY ID', 'REGISTERED', 'LASTNAME', 'FIRSTNAME', 'MIDDLE', 'SUFFIX', 'STATUS', 'PARTY', 'DATE OF BIRTH', 'RES_HOUSE', 'RES_FRAC', 'RES STREET', 'RES_APT', 'RES_CITY', 'RES_STATE', 'RES_ZIP', 'PRECINCT', 'PRECINCT SPLIT', 'PRECINCT_NAME_WITH_SPLIT', 'HOUSE', 'SENATE', 'CONGRESSIONAL', 'CITY OR VILLAGE', 'TOWNSHIP', 'SCHOOL', 'FIRE', 'POLICE', 'PARK', 'ROAD', '052017-P', '112016-G', '082016-S', '032016-P', '112015-G', '052015-P', '112014-G', '052014-P', '112013-G', '052013-P', '112012-G', '032012-P', '112011-G', '082011-L', '052011-P', '112010-G', '052010-P', '112009-G', '082009-S', '052009-P', '112008-G', '032008-P', '112007-G', '082007-S', '052007-P', '022007-L', '112006-G', '082006-L', '052006-P', '022006-L', '112005-G', '052005-P', '022005-L', '112004-G', '032004-P', '112003-G', '082003-S', '052003-L', '022003-S', '112002-G', '082002-S', '052002-P', '112001-G', '082001-S', '052001-L', '022001-S', '112000-G', '032000-P\r\n']
    
    # Functions
    def __init__(self, voter):
        self.stateID = voter[0]
        self.countyID = voter[1]
        self.registrationDate = voter[2]
        # formatting for middle name
        self.name = voter[4] + ' '
        if voter[5] != '':
            self.name = self.name + voter[5] + ' '
        self.name = self.name + voter[3]
        # end name
        self.status = voter[7]
        self.party = voter[8]
        self.dob = voter[9]
        self.street = voter[12] 
        self.zipcode = voter[16]
        self.precint = voter[17]
        self.house = voter[20]
        self.senate = voter[21]
        self.congress = voter[22]
        self.P_052017 = True if voter[30].isalpha() else False
        self.G_112016 = True if voter[31].isalpha() else False
        self.S_082016 = True if voter[32].isalpha() else False
        self.P_032016 = True if voter[33].isalpha() else False
        self.G_112015 = True if voter[34].isalpha() else False
        self.P_052015 = True if voter[35].isalpha() else False
        self.G_112014 = True if voter[36].isalpha() else False
        self.P_052014 = True if voter[37].isalpha() else False
        self.G_112013 = True if voter[38].isalpha() else False
        self.P_052013 = True if voter[39].isalpha() else False
        self.G_112012 = True if voter[40].isalpha() else False
        self.P_032012 = True if voter[41].isalpha() else False
        self.G_112011 = True if voter[42].isalpha() else False
        self.L_082011 = True if voter[43].isalpha() else False
        self.P_052011 = True if voter[44].isalpha() else False
        self.G_112010 = True if voter[45].isalpha() else False
        self.P_052010 = True if voter[46].isalpha() else False
        self.G_112009 = True if voter[47].isalpha() else False
        self.P_082009 = True if voter[48].isalpha() else False
        self.P_052009 = True if voter[49].isalpha() else False
        self.G_112008 = True if voter[50].isalpha() else False
        self.P_032008 = True if voter[51].isalpha() else False

        monthRegistered = int(self.registrationDate.split('/')[0])
        yearRegistered= int(self.registrationDate.split('/')[2].split(' ')[0])

        self.registered2017G = True if (yearRegistered == 2017 and monthRegistered <= 11) or yearRegistered < 2017 else False
        self.registered2017P = True if (yearRegistered == 2017 and monthRegistered <= 5) or yearRegistered < 2017 else False
        self.registered2016G = True if (yearRegistered == 2016 and monthRegistered <= 11) or yearRegistered < 2016 else False
        self.registered2016P = True if (yearRegistered == 2016 and monthRegistered <= 3) or yearRegistered < 2016 else False
        self.registered2015G = True if (yearRegistered <= 2015 and monthRegistered <= 11) or yearRegistered < 2015 else False
        self.registered2015P = True if (yearRegistered <= 2015 and monthRegistered <= 5) or yearRegistered < 2015 else False
        self.registered2014G = True if (yearRegistered <= 2014 and monthRegistered <= 11) or yearRegistered < 2014 else False
        self.registered2014P = True if (yearRegistered <= 2014 and monthRegistered <= 5) or yearRegistered < 2014 else False
        self.registered2013G = True if (yearRegistered <= 2013 and monthRegistered <= 11) or yearRegistered < 2013 else False
        self.registered2013P = True if (yearRegistered <= 2013 and monthRegistered <= 5) or yearRegistered < 2013 else False
        self.registered2012G = True if (yearRegistered <= 2012 and monthRegistered <= 11) or yearRegistered < 2012 else False
        self.registered2012P = True if (yearRegistered <= 2012 and monthRegistered <= 3) or yearRegistered < 2012 else False
        self.registered2011G = True if (yearRegistered <= 2011 and monthRegistered <= 11) or yearRegistered < 2011 else False
        self.registered2011P = True if (yearRegistered <= 2011 and monthRegistered <= 5) or yearRegistered < 2011 else False
        self.registered2010G = True if (yearRegistered <= 2010 and monthRegistered <= 11) or yearRegistered < 2010 else False
        self.registered2010P = True if (yearRegistered <= 2010 and monthRegistered <= 5) or yearRegistered < 2010 else False
        self.registered2009G = True if (yearRegistered <= 2009 and monthRegistered <= 11) or yearRegistered < 2009 else False
        self.registered2009P = True if (yearRegistered <= 2009 and monthRegistered <= 5) or yearRegistered < 2009 else False
        self.registered2008G = True if (yearRegistered <= 2008 and monthRegistered <= 11) or yearRegistered < 2008 else False
        self.registered2008P = True if (yearRegistered <= 2008 and monthRegistered <= 3) or yearRegistered < 2008 else False
        
