#!/usr/bin/python
################################################################################
# 25bb2682-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "25bb2682-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep remember /etc/pam.d/system-auth")
        stdout += cli.system("grep remember /etc/pam.d/system-auth-ac")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if "remember=24" in line and line.startswith("password"):
                self.is_compliant = True
                 
        return self.is_compliant

    def fix(self, cli):
        # Desired PAM setting
        value_pair = "remember=24"
        sub_string = value_pair.split("=")
        name = sub_string[0]
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep 'password' /etc/pam.d/system-auth")
        
        # Split output lines
        output = stdout.split('\n')

        # Process standard output
        for line in output:
            password_pam_unix_line = ""
            
            if line.startswith("password") and "sufficient" in line and "pam_unix.so" in line:
                sub_string = (line.strip()).split(" ")
                
                for string in sub_string:
                    if name not in string:
                        password_pam_unix_line += string + " "
                
                password_pam_unix_line += value_pair
                
                cli.system("sed -i 's/" + line.strip() + "/" + password_pam_unix_line + "/' /etc/pam.d/system-auth")    
