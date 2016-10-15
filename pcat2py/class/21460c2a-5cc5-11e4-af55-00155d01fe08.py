#!/usr/bin/python
################################################################################
# 21460c2a-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21460c2a-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Subsystems\Posix', '')

        # Output Lines
        self.output = [r'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Subsystems\Posix', ('=' + str(dword))]

        if dword == -1:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager'")
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Subsystems'")
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Subsystems\Posix'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Subsystems\Posix' -name '' -value -Type DWord")
