#!/usr/bin/python
################################################################################
# 20def36e-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20def36e-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True

        # Get Accounts
        usernames = cli.get_secedit_account('SeAssignPrimaryTokenPrivilege')

        # Output Lines
        self.output = [("SeAssignPrimaryTokenPrivilege=")] + usernames
	
	# Recommended MultiSZ
	rec_usernames = ("NT AUTHORITY\Local Service,NT AUTHORITY\Network Service")

	for user in usernames:
	    if user.lower() not in rec_usernames.lower():
	        self.is_compliant = False

        return self.is_compliant
