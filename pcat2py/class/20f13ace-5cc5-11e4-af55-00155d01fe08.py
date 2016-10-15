#!/usr/bin/python
################################################################################
# 20f13ace-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20f13ace-5cc5-11e4-af55-00155d01fe08"
        
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
                if not "-rw-------" in sub_string[0]:
                    self.is_compliant = False
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("chmod 600 /var/log/messages")
        cli.system("chmod 600 /var/log/secure")
        cli.system("chmod 600 /var/log/maillog")
        cli.system("chmod 600 /var/log/cron")
        cli.system("chmod 600 /var/log/spooler")
