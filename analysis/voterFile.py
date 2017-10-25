### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: class to provide human-readable functions to parse each voter in the JSON'ed voter file AND class to hold dictionary of parsed voters

import numpy as np, matplotlib.pyplot as plt
from scipy import stats
from scipy.stats.stats import pearsonr

from numpy import arange,array,ones,linalg
from pylab import plot,show

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
        doLinearRegression:             perform linear correlation between elections
        validateFit:                    create plot showing comparison between prediction from fit (should come from different sample) and observed behavior
        makeCorrelationPlot:            show and save histogram of correlation values between elections
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

    def makeCorrelationPlots(self, registered, elections, title, party=[], activeOnly=True, nTimesVoted=0):
        """ show and save histogram of correlation values between elections """

        correlations = []
        #if type(party) is str: # make party list if single string
        #    party = [party]
        #print party
        for i, election in enumerate(elections):
            if i != len(elections)-1:
                correlations.append( self.calculateCorrelation(registered, election, elections[len(elections)-1], '{0}_{1}'.format(election, title), activeOnly, party, nTimesVoted) )

        fig = plt.figure( title )
        n, bins, patches = plt.hist(correlations, bins=40, range=(-1,1))
        plt.title(title, fontsize=18, fontweight='bold')
        plt.ylabel("Entries / Bin", fontsize=18)
        plt.ylim(0, max(n)*1.2)
        plt.xlabel("Correlation", fontsize=15)
        plt.savefig( '../figures/correlationsWith_{0}.png'.format(title))
        plt.savefig( '../figures/correlationsWith_{0}.pdf'.format(title))

    def validateFit(self, registered, elections, fitParams, residual, party = [], activeOnly=True, nTimesVoted=0):
        """ create plot showing comparison between prediction from fit (should come from different sample) and observed behavior"""

        for i, election in enumerate(elections):
            temp = self.makeElectionList(registered, election, activeOnly, party, nTimesVoted)
            if i == 0:
                electionArray = np.array( [temp])
            elif i != len(elections)-1:
                electionArray = np.vstack([electionArray, temp])
            else:
                finalElection = np.array( temp )

        #print electionArray.shape, finalElection.shape, fitParams.shape
        fit = np.matmul(electionArray.T, fitParams)
        #print fit, electionArray.T[0], fitParams, finalElection[0]
        nCorrectBySign, nIncorrectBySign, nCorrectBySign_voted, nCorrectBySign_didNotVote, nVoted, nDidNotVote = 0, 0, 0, 0, 0, 0
        for j, vote in enumerate(finalElection):
            if vote*fit[j] > 0:
                nCorrectBySign = nCorrectBySign + 1
                if vote > 0:
                    nCorrectBySign_voted = nCorrectBySign_voted + 1
                else:
                    nCorrectBySign_didNotVote = nCorrectBySign_didNotVote + 1
            elif vote*fit[j] < 0:
                nIncorrectBySign = nIncorrectBySign + 1

            if vote > 0:
                nVoted = nVoted+1
            else:
                nDidNotVote = nDidNotVote+1
        print 'nCorrectBySign: {0} ({1:.2f}%, {2:.2f}% of voters, {3:.2f}% of non-voters)\tnIncorrectBySign {4} ({5:.2f}%)'.format(nCorrectBySign, 100*float(nCorrectBySign)/float(len(fit)), 100*float(nCorrectBySign_voted)/float(nVoted), 100*float(nCorrectBySign_didNotVote)/float(nDidNotVote), nIncorrectBySign, 100*float(nIncorrectBySign)/float(len(fit)) )
        #fig = plt.figure( title.replace(' ','')+'_validation')
        #plt.title(title.replace(' ','')+'_validation', fontsize=18, fontweight='bold')
        #plt.plot(voted1, voted2, "o")
        #graph = fig.add_subplot(111)
        #indiv, = graph.scatter(array1,array2)
        #plt.show()
        
    def doLinearRegression(self, registered, elections, party=[], activeOnly=True, nTimesVoted=0):
        """ return linear regression between elections"""

        for i, election in enumerate(elections):
            temp = self.makeElectionList(registered, election, activeOnly, party, nTimesVoted)
            if i == 0:
                electionArray = np.array( [temp])
            elif i != len(elections)-1:
                electionArray = np.vstack([electionArray, temp])
            else:
                finalElection = np.array( temp )
        
        #print electionArray
        #print electionArray.shape, finalElection.shape

        # ***  A. scipy works for two variables
        #slope, intercept, r_value, p_value, std_err = stats.linregress(electionArray, finalElection)
        #print 'r-squared:', r_value**2, 'slope:', slope, 'intercept', intercept
        # ***  B. numpy works for n variables
        #w = linalg.lstsq(electionArray.T,finalElection)[0] # obtaining the parameters
        w, residuals, rank, s = linalg.lstsq(electionArray.T,finalElection) # obtaining the parameters
        r2 = 1 - residuals / sum((finalElection - finalElection.mean())**2) 
        
        print w, elections, residuals, rank, s, r2, party

        self.validateFit(registered, elections, w, residuals, party, activeOnly, nTimesVoted)
        
        return w, residuals
                
    def printSomeCorrelations(self):
        """dummy to hold correlations. NOTE: Unaffiliated voters almost never vote, and including them makes correlation calculation undersampled"""
        #self.calculateCorrelation('registered2016P', 'P_032016', 'G_112016', 'Testing 2016 Primary vs 2016 General')
        #self.calculateCorrelation('registered2015G', 'G_112015', 'G_112016', 'Testing 2015 General vs 2016 General')
        #self.calculateCorrelation('registered2015G', 'G_112015', 'P_032016', 'Testing 2015 General vs 2016 Primary')
        #self.calculateCorrelation('registered2015P', 'G_112015', 'P_032016', 'Testing 2015 General vs 2016 Primary')
        #self.calculateCorrelation('registered2012P', 'P_032012', 'G_112016', 'Testing 2012 Primary vs 2016 General')
        #self.calculateCorrelation('registered2012G', 'G_112012', 'G_112016', 'Testing 2012 Primary vs 2016 General')
        #self.calculateCorrelation('registered2015P', 'P_052015', 'G_112015', 'Testing 2015 Primary vs 2015 General')
        #self.calculateCorrelation('registered2014P', 'P_052014', 'G_112014', 'Testing 2014 Primary vs 2014 General')
        #self.calculateCorrelation('registered2013P', 'P_052013', 'G_112013', 'Testing 2013 Primary vs 2013 General')
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General')
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (R)',party='R')
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (U)',party='U')
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (D)',party='D')
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (D, R)',party=['D','R'])
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (D, U)',party=['D','U'])
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (U, R)',party=['R','U'])
        self.calculateCorrelation('registered2012P', 'P_032012', 'G_112012', 'Testing 2012 Primary vs 2012 General (D, R, U)',party=['D','R', 'U'])
        #self.calculateCorrelation('registered2011P', 'P_052011', 'G_112011', 'Testing 2011 Primary vs 2011 General')
        #self.calculateCorrelation('registered2010P', 'P_052010', 'G_112010', 'Testing 2010 Primary vs 2010 General')
        #self.calculateCorrelation('registered2009P', 'P_052009', 'G_112009', 'Testing 2009 Primary vs 2009 General')
        #self.calculateCorrelation('registered2008P', 'P_032008', 'G_112008', 'Testing 2008 Primary vs 2008 General')

    def calculateCorrelation(self, registered, election1, election2, title, activeOnly=True, party=[], nTimesVoted=0):
        """ function to calculate and print correlation between voting behavior in two elections"""

        voted1 = self.makeElectionList(registered, election1, activeOnly, party, nTimesVoted)
        voted2 = self.makeElectionList(registered, election2, activeOnly, party, nTimesVoted)

        array1 = np.array(voted1)
        array2 = np.array(voted2)
        corr, pvalue = pearsonr(array1, array2)
        print title, ', correlation =', corr, ', p-value =', pvalue, len(array1), len(array2)

        voteCount = [0,0,0,0]
        for i, vote in enumerate(voted1):
            if vote == 1 and voted2[i] == 1:
                voteCount[0] = voteCount[0]+1
            elif vote == 1 and voted2[i] == -1:
                voteCount[1] = voteCount[1]+1
            elif vote == -1 and voted2[i] == 1:
                voteCount[2] = voteCount[2]+1
            elif vote == -1 and voted2[i] == -1:
                voteCount[3] = voteCount[3]+1
        #print voteCount, '{0:.2f}% vote neither'.format(100*float(voteCount[3])/float(len(voted1)))

        return corr
    
    def makeElectionList(self, registered, election, activeOnly, party, nTimesVoted):
        """ function to return list of vote history for an election using only eligible voters"""

        electionList = []
        for voter in self.voters:
            activeStatus = True if voter.status=='A' or not activeOnly else False
            if type(party) is str: # make party list if single string
                party = [party]
            partyFilter  = True if len(party)==0 or (len(party)>0 and voter.party in party) else False 
            
            if getattr(voter, registered) and getattr(voter, election) and activeStatus and partyFilter and voter.hasVoted(nTimesVoted):
                #electionList.append(True)
                electionList.append(1)
            elif getattr(voter, registered) and not getattr(voter, election) and activeStatus and partyFilter and voter.hasVoted(nTimesVoted):
                #electionList.append(False)
                electionList.append(-1)

            #if voter.party == 'U' and activeStatus and partyFilter:
            #    print voter.name, voter.status, voter.party, getattr(voter, registered), getattr(voter, election), election
        
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
        hasVoted:         true if voter has ever voted. Takes argument (default=0) that can ask for a specific number of votes, e.g. has voted at least 3 times

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

        
    def hasVoted(self, n=0):
        """ function that returns true/false on whether a voter has voted at least n times"""

        nVotes = 0
        if self.P_052017:
            nVotes = nVotes + 1
        if self.G_112016:
            nVotes = nVotes + 1
        if self.S_082016:
            nVotes = nVotes + 1
        if self.P_032016:
            nVotes = nVotes + 1
        if self.G_112015:
            nVotes = nVotes + 1
        if self.P_052015:
            nVotes = nVotes + 1
        if self.G_112014:
            nVotes = nVotes + 1
        if self.P_052014:
            nVotes = nVotes + 1
        if self.G_112013:
            nVotes = nVotes + 1
        if self.P_052013:
            nVotes = nVotes + 1
        if self.G_112012:
            nVotes = nVotes + 1
        if self.P_032012:
            nVotes = nVotes + 1
        if self.G_112011:
            nVotes = nVotes + 1
        if self.L_082011:
            nVotes = nVotes + 1
        if self.P_052011:
            nVotes = nVotes + 1
        if self.G_112010:
            nVotes = nVotes + 1
        if self.P_052010:
            nVotes = nVotes + 1
        if self.G_112009:
            nVotes = nVotes + 1
        if self.P_082009:
            nVotes = nVotes + 1
        if self.P_052009:
            nVotes = nVotes + 1
        if self.G_112008:
            nVotes = nVotes + 1
        if self.P_032008:
            nVotes = nVotes + 1

        if nVotes >= n:
            return True
        else:
            return False
