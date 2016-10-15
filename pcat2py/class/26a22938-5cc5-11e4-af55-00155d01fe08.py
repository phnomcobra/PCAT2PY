#!/usr/bin/python
################################################################################
# 26a22938-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "26a22938-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep PASS_WARN_AGE /etc/login.defs")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if line.startswith("PASS_WARN_AGE"):
                if int(line[13:]) == 7:
                    self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i /^PASS_WARN_AGE/d /etc/login.defs")
        cli.system('echo "PASS_WARN_AGE 7" >> /etc/login.defs')
