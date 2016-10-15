#!/usr/bin/python
################################################################################
# 20eabba4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20eabba4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep ClientAliveInterval /etc/ssh/sshd_config")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if line.startswith("ClientAliveInterval 900"):
                self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i '/ClientAliveInterval/d' /etc/ssh/sshd_config")
        cli.system('echo "ClientAliveInterval 900" >> /etc/ssh/sshd_config')
