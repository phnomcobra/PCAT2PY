#!/usr/bin/python
################################################################################
# 2174be12-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2174be12-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep bluetooth /etc/modprobe.d/blacklist.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        bluetooth = False
        for line in self.output:
            if len(line.strip()) > 0:
                bluetooth = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep net-pf-31 /etc/modprobe.d/blacklist.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        net_pf_31 = False
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                net_pf_31 = True
        
        if bluetooth and net_pf_31:
            self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "blacklist net-pf-31" >> /etc/modprobe.d/blacklist.conf')
        cli.system('echo "blacklist bluetooth" >> /etc/modprobe.d/blacklist.conf')
