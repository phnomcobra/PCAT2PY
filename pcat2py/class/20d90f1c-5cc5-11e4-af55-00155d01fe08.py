#!/usr/bin/python
################################################################################
# 20d90f1c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20d90f1c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep '^vc/[0-9]' /etc/securetty")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if "vc/" in line:
                self.is_compliant = False
                
        return self.is_compliant

    def fix(self, cli):
        # Execute command and parse capture standard output
        stdout = cli.system("grep '^vc/[0-9]' /etc/securetty")
        
        # Split output lines
        output = stdout.split('\n')

        # Remove detected virtual consoles
        for line in output:
            if len(line.strip()) > 0:
                fixCommand = "sed -i '\#" + line.strip() + "#d' /etc/securetty"
                cli.system(fixCommand)
