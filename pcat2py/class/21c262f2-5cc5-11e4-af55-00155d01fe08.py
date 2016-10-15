#!/usr/bin/python
################################################################################
# 21c262f2-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21c262f2-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('chkconfig "rexec" --list')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if len(line.strip()) == 0 or ("rexec off" in line or "error reading information on service rexec: No such file or directory" in line):    
                self.is_compliant = True
                
        return self.is_compliant

    def fix(self, cli):
        cli.system('chkconfig rexec off')     
