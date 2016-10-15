#!/usr/bin/python
################################################################################
# 2254df56-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2254df56-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/audit/audit.rules")
        
        if "/etc/sudoers" in stdout:
            self.is_compliant = True
                
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "-w /etc/sudoers -p wa -k actions" >> /etc/audit/audit.rules')
