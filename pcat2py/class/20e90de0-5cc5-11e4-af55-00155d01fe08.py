#!/usr/bin/python
################################################################################
# 20e90de0-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20e90de0-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Secedit Value
        value = cli.get_secedit_value('SeSyncAgentPrivilege')

        # Output Lines
        self.output = ["SeSyncAgentPrivilege=" + value]
	
	# Recommended Value
	rec_value = ("")

	if value.lower() == rec_value.lower():
	    self.is_compliant = True

        return self.is_compliant
