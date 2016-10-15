#!/usr/bin/python
################################################################################
# 2188af26-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2188af26-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        ftpd_installed = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('find /etc/vsftpd -name vsftpd.conf')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if len(line.strip()) > 0:
                ftpd_installed = True
        
        # Execute command and parse capture standard output
        stdout = cli.system('grep "banner_file" /etc/vsftpd/vsftpd.conf')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if line.startswith("banner_file=/etc/issue"):
                self.is_compliant = True
        
        if not ftpd_installed:
            self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        ftpd_installed = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('find /etc/vsftpd -name vsftpd.conf')
        
        # Split output lines
        output = stdout.split('\n')

        # Process standard output
        for line in output:
            if len(line.strip()) > 0:
                ftpd_installed = True
        
        if ftpd_installed:
            cli.system("sed -i '/banner_file/d' /etc/vsftpd/vsftpd.conf")
            cli.system('echo "banner_file=/etc/issue" >> /etc/vsftpd/vsftpd.conf')
