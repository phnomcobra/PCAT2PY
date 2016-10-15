#!/usr/bin/python
################################################################################
# 2133f90e-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2133f90e-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/audit/audit.rules")
        
        if "unlink" in stdout and "unlinkat" in stdout and "rename" in stdout and "renameat" in stdout:
            self.is_compliant = True
                
        return self.is_compliant

    def fix(self, cli):
        if "x86_64" in cli.system("uname -p"):
            cli.system('echo "-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=500 -F auid!=4294967295 -k delete" >> /etc/audit/audit.rules')
            cli.system('echo "-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid=0 -k delete   " >> /etc/audit/audit.rules')
        else:
            cli.system('echo "-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=500 -F auid!=4294967295 -k delete" >> /etc/audit/audit.rules')
            cli.system('echo "-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid=0 -k delete   " >> /etc/audit/audit.rules')
