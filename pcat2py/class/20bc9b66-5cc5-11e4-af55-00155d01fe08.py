#!/usr/bin/python
################################################################################
# 20bc9b66-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20bc9b66-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Secedit Value
        value = cli.get_secedit_value('LockoutBadCount')

        # Output Lines
        self.output = ["LockoutBadCount=" + value]
	
	# Recommended Value
	rec_value = ("1 to 3")

	try:
            if int(value) >= int(rec_value.split("to")[0]) and int(value) <= int(rec_value.split("to")[1]):
                self.is_compliant = True
        except ValueError:
            None

        return self.is_compliant
