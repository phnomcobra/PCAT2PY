#!/usr/bin/python
################################################################################
# 243b0d68-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "243b0d68-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep pam_cracklib /etc/pam.d/system-auth")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if line.startswith("password") and "difok=4" in line:
                self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        # Desired PAM setting
        value_pair = "difok=4"
        sub_string = value_pair.split("=")
        name = sub_string[0]
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep pam_cracklib /etc/pam.d/system-auth")
        
        # Split output lines
        output = stdout.split('\n')

        # Process standard output
        for line in output:
            password_pam_cracklib_line = ""
            
            if line.startswith("password"):
                sub_string = (line.strip()).split(" ")
                
                for string in sub_string:
                    if name not in string:
                        password_pam_cracklib_line += string + " "
                
                password_pam_cracklib_line += value_pair
                
                cli.system("sed -i 's/.*pam_cracklib.*/" + password_pam_cracklib_line + "/' /etc/pam.d/system-auth")    
