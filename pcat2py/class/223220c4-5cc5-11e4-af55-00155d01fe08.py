#!/usr/bin/python
################################################################################
# 223220c4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "223220c4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("sysctl net.ipv4.conf.default.secure_redirects")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if (line.strip()).startswith("net.ipv4.conf.default.secure_redirects"):
                sub_string = (line.strip()).split('=')
                if int(sub_string[1]) == 0:
                    self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("sysctl -w net.ipv4.conf.default.secure_redirects=0")
        cli.system("sed -i '/^net.ipv4.conf.default.secure_redirects.*/d' /etc/sysctl.conf")
        cli.system('echo "net.ipv4.conf.default.secure_redirects = 0" >> /etc/sysctl.conf')
