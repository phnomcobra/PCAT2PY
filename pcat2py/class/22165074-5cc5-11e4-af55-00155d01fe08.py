#!/usr/bin/python
################################################################################
# 22165074-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "22165074-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep action_mail_acct /etc/audit/auditd.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if line.startswith("action_mail_acct = root"):
                self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "action_mail_acct = root" >> /etc/audit/auditd.conf')
