#!/usr/bin/python
################################################################################
# 2400abb4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2400abb4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep umask /etc/bashrc")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if "umask 077" not in line and len(line.strip()) > 0:
                self.is_compliant = False
                
        return self.is_compliant

    def fix(self, cli):
        # Execute command and parse capture standard output
        stdout = cli.system("grep umask /etc/bashrc")
        
        # Split output lines
        self.__output = stdout.split('\n')

        # Process standard output
        for line in self.__output:
            if "umask 077" not in line:
                cli.system("sed -i 's/umask.*/umask 077/g' /etc/bashrc")
