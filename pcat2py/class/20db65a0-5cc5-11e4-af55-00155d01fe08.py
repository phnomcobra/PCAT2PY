#!/usr/bin/python
################################################################################
# 20db65a0-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20db65a0-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        passwd_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/passwd /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if len(line.strip()) > 0:
                passwd_compliant = True
                
        shadow_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep etc/shadow /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                shadow_compliant = True
                
        group_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/group /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                group_compliant = True
                
        gshadow_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/gshadow /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                gshadow_compliant = True
                
        opasswd_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/security/opasswd /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                opasswd_compliant = True
        
        if passwd_compliant and shadow_compliant and group_compliant and gshadow_compliant and opasswd_compliant:
            self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "-w /etc/group -p wa -k audit_account_changes" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/passwd -p wa -k audit_account_changes" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/gshadow -p wa -k audit_account_changes" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/shadow -p wa -k audit_account_changes" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules')
