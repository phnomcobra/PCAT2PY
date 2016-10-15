#!/usr/bin/python
################################################################################
# 274f8024-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "274f8024-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("grep Ciphers /etc/ssh/sshd_config")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        for line in self.output:
            if line.startswith("Ciphers"):
                ciphers = line[7:].strip(' ').split(',')
                
                # Remove approved ciphers from list
                ciphers.remove('aes128-ctr')
                ciphers.remove('aes192-ctr')
                ciphers.remove('aes256-ctr')
                ciphers.remove('aes128-cbc')
                ciphers.remove('3des-cbc')
                ciphers.remove('aes192-cbc')
                ciphers.remove('aes256-cbc')
                
                # If there are no remaining ciphers then finding is compliant
                if len(ciphers) == 0:
                    self.is_compliant = True
        
        return self.is_compliant
