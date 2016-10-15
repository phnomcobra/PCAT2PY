#!/usr/bin/python
################################################################################
# 2114f20c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2114f20c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('chkconfig "telnet" --list')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if "telnet off" in line or "error reading information on service telnet: No such file or directory":    
                self.is_compliant = True
                
        return self.is_compliant

    def fix(self, cli):
        cli.system('chkconfig telnet off')      
