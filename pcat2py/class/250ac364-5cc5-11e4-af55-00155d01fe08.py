#!/usr/bin/python
################################################################################
# 250ac364-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "250ac364-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKCU:\Software\Microsoft\Internet Explorer\Download', 'CheckExeSignatures')

        # Output Lines
        self.output = [r'HKCU:\Software\Microsoft\Internet Explorer\Download', ('CheckExeSignatures=' + str(dword))]

        if dword == yes:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\Software\Microsoft'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Microsoft\Internet Explorer'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Microsoft\Internet Explorer\Download'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\Software\Microsoft\Internet Explorer\Download' -name 'CheckExeSignatures' -value yes -Type DWord")
