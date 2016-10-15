#!/usr/bin/python
################################################################################
# 241e7284-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "241e7284-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep PermitUserEnvironment /etc/ssh/sshd_config")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if line.startswith("PermitUserEnvironment no"):
                self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i '/PermitUserEnvironment/d' /etc/ssh/sshd_config")
        cli.system('echo "PermitUserEnvironment no" >> /etc/ssh/sshd_config')
