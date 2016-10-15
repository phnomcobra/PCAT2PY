#!/usr/bin/python
################################################################################
# 221cbf7c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "221cbf7c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        if "init_module" in stdout and "delete_module" in stdout:
            self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "-w /sbin/insmod -p x -k modules" >> /etc/audit/audit.rules')
        cli.system('echo "-w /sbin/rmmod -p x -k modules" >> /etc/audit/audit.rules')
        cli.system('echo "-w /sbin/modprobe -p x -k modules" >> /etc/audit/audit.rules')
        
        if "x86_64" in cli.system("uname -p"):
            cli.system('echo "-a always,exit -F arch=b64 -S init_module -S delete_module -k modules" >> /etc/audit/audit.rules')
        else:
            cli.system('echo "-a always,exit -F arch=b32 -S init_module -S delete_module -k modules" >> /etc/audit/audit.rules')
