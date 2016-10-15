#!/usr/bin/python
################################################################################
# 215d00c4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "215d00c4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep pam_faillock /etc/pam.d/system-auth-ac")
        stdout += cli.system("grep pam_faillock /etc/pam.d/password-auth-ac")

        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if "fail_interval" in line:
                self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "auth [default=die] pam_faillock.so authfail deny=3 unlock_time=604800 fail_interval=900" >> /etc/pam.d/system-auth-ac')
        cli.system('echo "auth required pam_faillock.so authsucc deny=3 unlock_time=604800 fail_interval=900" >> /etc/pam.d/system-auth-ac')
