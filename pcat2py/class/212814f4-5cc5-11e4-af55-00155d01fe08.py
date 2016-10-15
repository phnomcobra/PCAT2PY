#!/usr/bin/python
################################################################################
# 212814f4-5cc5-11e4-af55-00155d01fe08
#
# Justin Dierking
# justindierking@hardbitsolutions.com
# phnomcobra@gmail.com
#
# 10/24/2014 Original Construction
################################################################################

class Finding:
    def __init__(self):
        self.output = []
        self.is_compliant = False
        self.uuid = "212814f4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'', 'HideZoneInfoOnProperties')

        # Output Lines
        self.output = [r'', ('HideZoneInfoOnProperties=' + str(dword))]

        if dword == 1:
            self.is_compliant = True

        return self.is_compliant
