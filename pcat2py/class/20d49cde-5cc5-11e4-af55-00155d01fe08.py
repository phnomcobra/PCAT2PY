#!/usr/bin/python
################################################################################
# 20d49cde-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20d49cde-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\System\CurrentControlSet\Services\LanmanWorkstation\Parameters', 'RequireSecuritySignature')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Services\LanmanWorkstation\Parameters', ('RequireSecuritySignature=' + str(dword))]

        if dword == 1:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\LanmanWorkstation'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\LanmanWorkstation\Parameters'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Services\LanmanWorkstation\Parameters' -name 'RequireSecuritySignature' -value 1 -Type DWord")