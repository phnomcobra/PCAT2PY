#!/usr/bin/python
################################################################################
# 24556924-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "24556924-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        samba_installed = False
        
        # Execute command and parse capture standard output
        stdout = cli.system('find /etc/samba -name smb.conf')
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if len(line.strip()) > 0:
                samba_installed = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep signing /etc/samba/smb.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
        
            
            if line.startswith("client signing = mandatory"):
                self.is_compliant = True
        
        if not samba_installed:
            self.is_compliant = True
            
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i '/client signing/d' /etc/samba/smb.conf")
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/samba/smb.conf")
        
        # Split output lines
        self.__output = stdout.split('\n')

        # Process standard output
        cli.system("/dev/null > /etc/samba/smb.conf")
        for line in self.__output:
            cli.system('echo "' + line + '" >> /etc/samba/smb.conf')
            
            if line.startswith("[global]"):
                cli.system('echo "client signing = mandatory" >> /etc/samba/smb.conf')
