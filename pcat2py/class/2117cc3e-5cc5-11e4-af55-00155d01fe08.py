#!/usr/bin/python
################################################################################
# 2117cc3e-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2117cc3e-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\Software\Policies\Microsoft\EMET\SysSettings', 'SEHOP')

        # Output Lines
        self.output = [r'HKLM:\Software\Policies\Microsoft\EMET\SysSettings', ('SEHOP=' + str(dword))]

        if dword == 2:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\Software\Policies\Microsoft'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Policies\Microsoft\EMET'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Policies\Microsoft\EMET\SysSettings'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\Software\Policies\Microsoft\EMET\SysSettings' -name 'SEHOP' -value 2 -Type DWord")
