#!/usr/bin/python
################################################################################
# 20ef99e4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20ef99e4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('grep -i PermitEmptyPasswords /etc/ssh/sshd_config')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if len(line.strip()) == 0 or line[0] == "#" or "PermitEmptyPasswords no" in line:
                self.is_compliant = True
                
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i 's/PermitEmptyPasswords no/PermitEmptyPasswords yes/g' /etc/ssh/sshd_config")
