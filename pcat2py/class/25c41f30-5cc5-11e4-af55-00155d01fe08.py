#!/usr/bin/python
################################################################################
# 25c41f30-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "25c41f30-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep pam_faillock /etc/pam.d/system-auth-ac")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        system_auth_ac_deny_3 = False
        for line in self.output:
            if "deny=3" in line and line.startswith("auth"):
                system_auth_ac_deny_3 = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep pam_faillock /etc/pam.d/password-auth-ac")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        password_auth_ac_deny_3 = False
        for line in self.output:
        
            
            if "deny=3" in line and line.startswith("auth"):
                password_auth_ac_deny_3 = True
        
        if password_auth_ac_deny_3 and system_auth_ac_deny_3:
                self.is_compliant = True
                
        return self.is_compliant
