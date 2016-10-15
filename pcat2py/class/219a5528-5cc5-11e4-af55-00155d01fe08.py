#!/usr/bin/python
################################################################################
# 219a5528-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "219a5528-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("mount")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        mount_points = []
        for line in self.output:
            if len(line.strip()) > 0:
                sub_string = (line.strip()).split(" ")
                mount_points.append(sub_string[2])
                
        stdout = ""
        for mount_point in mount_points:
            stdout += cli.system("find " + mount_point + " -xdev -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null")
            
        # Split output lines
        self.output = stdout.split('\n')
            
        # Retreive existing audit rules into a string    
        audit_rules = cli.system("cat /etc/audit/audit.rules")
            
        # Process standard output
        for line in self.output:
        
            
            if line.strip() not in audit_rules:
                self.is_compliant = False
                
        return self.is_compliant

    def fix(self, cli):
        # Execute command and parse capture standard output
        stdout = cli.system("mount")
        
        # Split output lines
        self.__output = stdout.split('\n')

        # Process standard output
        mount_points = []
        for line in self.__output:
            if len(line.strip()) > 0:
                sub_string = (line.strip()).split(" ")
                mount_points.append(sub_string[2])
                
        stdout = ""
        for mount_point in mount_points:
            stdout += cli.system("find " + mount_point + " -xdev -type f \( -perm -4000 -o -perm -2000 \) 2>/dev/null")
            
        # Split output lines
        self.__output = stdout.split('\n')
            
        # Retreive existing audit rules into a string    
        audit_rules = cli.system("cat /etc/audit/audit.rules")
            
        # Process standard output
        for line in self.__output:
            if line.strip() not in audit_rules:
                cli.system('echo "-a always,exit -F path=' + line.strip() + ' -F perm=x -F auid>=500 -F auid!=4294967295 -k privileged" >> /etc/audit/audit.rules')
