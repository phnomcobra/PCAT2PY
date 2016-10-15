#!/usr/bin/python
################################################################################
# 21d3cc7c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21d3cc7c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep kernel /etc/grub.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if "audit=1" in line:
                self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        # Desired value pair setting
        value_pair = "audit=1"
        sub_string = value_pair.split("=")
        name = sub_string[0]
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/grub.conf")
        
        # Clear existing grub.conf
        cli.system("/dev/null > /etc/grub.conf")
        
        # Split output lines
        output = stdout.split('\n')

        # Process standard output
        for line in output:
            kernel_line = ""
            
            if not line.startswith("#") and "kernel" in line:
                sub_string = (line.strip()).split(" ")
                
                for string in sub_string:
                    if name not in string:
                        kernel_line += string + " "
                
                kernel_line += value_pair
                
                cli.system('echo "' + kernel_line + '" >> /etc/grub.conf')
            else:
                cli.system('echo "' + line + '" >> /etc/grub.conf')
