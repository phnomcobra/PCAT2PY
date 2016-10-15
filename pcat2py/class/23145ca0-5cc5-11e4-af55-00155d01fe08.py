#!/usr/bin/python
################################################################################
# 23145ca0-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "23145ca0-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep -r ipv6 /etc/modprobe.conf")
        stdout += cli.system("grep -r ipv6 /etc/modprobe.d")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if (line.strip()).startswith("options ipv6 disable"):
                sub_string = (line.strip()).split('=')
                if int(sub_string[1]) == 1:
                    self.is_compliant = True
        
        return self.is_compliant
