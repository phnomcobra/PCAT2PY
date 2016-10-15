#!/usr/bin/python
################################################################################
# 21598408-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21598408-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        sz = cli.get_reg_sz(r'HKCU:\Software\Policies\Microsoft\Office\14.0\common\security', 'DefaultEncryption12')

        # Output Lines
        self.output = [r'HKCU:\Software\Policies\Microsoft\Office\14.0\common\security', ('DefaultEncryption12=' + sz)]

        if sz == "Microsoft Enhanced RSA and AES Cryptographic Provider,AES 256,256":
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Office\14.0'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Office\14.0\common'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Office\14.0\common\security'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\Software\Policies\Microsoft\Office\14.0\common\security' -name 'DefaultEncryption12' -value Microsoft Enhanced RSA and AES Cryptographic Provider,AES 256,256")
