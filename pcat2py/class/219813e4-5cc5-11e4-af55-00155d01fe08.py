#!/usr/bin/python
################################################################################
# 219813e4-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "219813e4-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\software\policies\Microsoft\office\15.0\common\officeupdate', 'EnableAutomaticUpdates')

        # Output Lines
        self.output = [r'HKLM:\software\policies\Microsoft\office\15.0\common\officeupdate', ('EnableAutomaticUpdates=' + str(dword))]

        if dword == 1:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\software\policies\Microsoft\office\15.0'")
        cli.powershell(r"New-Item -path 'HKLM:\software\policies\Microsoft\office\15.0\common'")
        cli.powershell(r"New-Item -path 'HKLM:\software\policies\Microsoft\office\15.0\common\officeupdate'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\software\policies\Microsoft\office\15.0\common\officeupdate' -name 'EnableAutomaticUpdates' -value 1 -Type DWord")
