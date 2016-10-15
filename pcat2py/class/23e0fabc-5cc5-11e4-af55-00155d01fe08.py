#!/usr/bin/python
################################################################################
# 23e0fabc-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "23e0fabc-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("ls -lL /var/log/messages")
        stdout += cli.system("ls -lL /var/log/secure")
        stdout += cli.system("ls -lL /var/log/maillog")
        stdout += cli.system("ls -lL /var/log/cron")
        stdout += cli.system("ls -lL /var/log/spooler")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if len(line.strip()) > 0:
                sub_string = (line.strip()).split(' ')
                if not "root" == sub_string[2]:
                    self.is_compliant = False
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("chown root /var/log/messages")
        cli.system("chown root /var/log/secure")
        cli.system("chown root /var/log/maillog")
        cli.system("chown root /var/log/cron")
        cli.system("chown root /var/log/spooler")
