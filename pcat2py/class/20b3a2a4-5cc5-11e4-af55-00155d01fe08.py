#!/usr/bin/python
################################################################################
# 20b3a2a4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20b3a2a4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\System\CurrentControlSet\Services\Eventlog\Security', 'WarningLevel')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Services\Eventlog\Security', ('WarningLevel=' + str(dword))]

        if dword <= 90:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\Eventlog'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\Eventlog\Security'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Services\Eventlog\Security' -name 'WarningLevel' -value 90 -Type DWord")
