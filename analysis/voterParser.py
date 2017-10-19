### Author: Ben Tannenwald
### Date: Oct 19, 2017
### Purpose: class to provide human-readable functions to parse each voter in the JSON'ed voter file

import operator

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
