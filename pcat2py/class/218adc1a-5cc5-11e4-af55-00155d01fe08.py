#!/usr/bin/python
################################################################################
# 218adc1a-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "218adc1a-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("find -L /lib \! -user root")
        stdout += cli.system("find -L /lib64 \! -user root")
        stdout += cli.system("find -L /usr/lib \! -user root")
        stdout += cli.system("find -L /usr/lib64 \! -user root")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if len(line.strip()) > 0:
                subString = line.split(' ')
                if not subString[2] == "root":
                    self.is_compliant = False
                
        return self.is_compliant

    def fix(self, cli):
        stdout = cli.system("find -L /lib \! -user root")
        stdout += cli.system("find -L /lib64 \! -user root")
        stdout += cli.system("find -L /usr/lib \! -user root")
        stdout += cli.system("find -L /usr/lib64 \! -user root")
        
        # Split output lines
        output = stdout.split('\n')
        
        # Process output
        for line in output:
            if len(line.strip()) > 0:
                fixCommand = "chown root " + line.strip()
                cli.system(fixCommand)
