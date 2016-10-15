#!/usr/bin/python
################################################################################
# 212af1ec-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "212af1ec-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        set_hostname_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep sethostname /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if len(line.strip()) > 0:
                set_hostname_compliant = True
                
        set_domain_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep setdomainname /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                set_domain_compliant = True
                
        issue_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/issue /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                issue_compliant = True
                
        issue_dot_net_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/issue.net /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                issue_dot_net_compliant = True
                
        hosts_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/hosts /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                hosts_compliant = True
        
        network_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep /etc/sysconfig/network /etc/audit/audit.rules")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if len(line.strip()) > 0:
                network_compliant = True
        
        if set_hostname_compliant and set_domain_compliant and issue_compliant and issue_dot_net_compliant and hosts_compliant and network_compliant:
            self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system('echo "-a always,exit -F arch=ARCH -S sethostname -S setdomainname -k audit_network_modifications" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/issue -p wa -k audit_network_modifications" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/issue.net -p wa -k audit_network_modifications" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/hosts -p wa -k audit_network_modifications" >> /etc/audit/audit.rules')
        cli.system('echo "-w /etc/sysconfig/network -p wa -k audit_network_modifications" >> /etc/audit/audit.rules')
