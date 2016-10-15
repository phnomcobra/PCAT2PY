#!/usr/bin/python
################################################################################
# 2718a680-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2718a680-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKCU:\Software\Policies\Microsoft\Cryptography\Defaults\Provider\ Microsoft Exchange Cryptographic Provider v1.0', 'DefPwdTime')

        # Output Lines
        self.output = [r'HKCU:\Software\Policies\Microsoft\Cryptography\Defaults\Provider\ Microsoft Exchange Cryptographic Provider v1.0', ('DefPwdTime=' + str(dword))]

        if dword == 30:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Cryptography\Defaults'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Cryptography\Defaults\Provider'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Cryptography\Defaults\Provider\ Microsoft Exchange Cryptographic Provider v1.0'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\Software\Policies\Microsoft\Cryptography\Defaults\Provider\ Microsoft Exchange Cryptographic Provider v1.0' -name 'DefPwdTime' -value 30 -Type DWord")
