#!/usr/bin/python
################################################################################
# 23b0c48c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "23b0c48c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep num_logs /etc/audit/auditd.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if (line.strip()).startswith("num_logs"):
                sub_string = (line.strip()).split('=')
                if int(sub_string[1]) >= 5:
                    self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i 's/^num_logs.*/num_logs = 5/g' /etc/audit/auditd.conf")
