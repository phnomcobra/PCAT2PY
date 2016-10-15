#!/usr/bin/python
################################################################################
# 22c75306-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "22c75306-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Auditpol Value
        enabled = cli.get_auditpol(r'Directory Service Access', 'Failure')

        # Output Lines
        self.output = [r'Directory Service Access', ('Failure=' + str(enabled))]

        if enabled:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.set_auditpol(r'Directory Service Access', 'Failure', True)
