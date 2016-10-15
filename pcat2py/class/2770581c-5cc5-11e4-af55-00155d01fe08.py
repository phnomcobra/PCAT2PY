#!/usr/bin/python
################################################################################
# 2770581c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2770581c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('grep disk_error_action /etc/audit/auditd.conf')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if line.startswith("disk_error_action = SYSLOG"):
                self.is_compliant = True
            elif line.startswith("disk_error_action = EXEC"):
                self.is_compliant = True
            elif line.startswith("disk_error_action = SINGLE"):
                self.is_compliant = True
            elif line.startswith("disk_error_action = HALT"):
                self.is_compliant = True
                
        return self.is_compliant
