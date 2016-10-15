#!/usr/bin/python
################################################################################
# 20e9c0c8-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20e9c0c8-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKCU:\Software\Policies\Microsoft\Windows\System\Power', 'PromptPasswordOnResume')

        # Output Lines
        self.output = [r'HKCU:\Software\Policies\Microsoft\Windows\System\Power', ('PromptPasswordOnResume=' + str(dword))]

        if dword == 1:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Windows'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Windows\System'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Windows\System\Power'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\Software\Policies\Microsoft\Windows\System\Power' -name 'PromptPasswordOnResume' -value 1 -Type DWord")