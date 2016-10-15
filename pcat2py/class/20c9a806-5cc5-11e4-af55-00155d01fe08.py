#!/usr/bin/python
################################################################################
# 20c9a806-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20c9a806-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Secedit Value
        value = cli.get_secedit_value('PasswordHistorySize')

        # Output Lines
        self.output = ["PasswordHistorySize=" + value]
	
	# Recommended Value
	rec_value = ("24")

	try:
            if int(value) >= int(rec_value):
                self.is_compliant = True
        except ValueError:
            None

        return self.is_compliant
