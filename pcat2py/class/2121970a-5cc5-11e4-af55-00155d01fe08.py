#!/usr/bin/python
################################################################################
# 2121970a-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2121970a-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\software\Microsoft\internet explorer\main\featurecontrol\feature_addon_management', 'visio.exe')

        # Output Lines
        self.output = [r'HKLM:\software\Microsoft\internet explorer\main\featurecontrol\feature_addon_management', ('visio.exe=' + str(dword))]

        if dword == 1:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\software\Microsoft\internet explorer\main'")
        cli.powershell(r"New-Item -path 'HKLM:\software\Microsoft\internet explorer\main\featurecontrol'")
        cli.powershell(r"New-Item -path 'HKLM:\software\Microsoft\internet explorer\main\featurecontrol\feature_addon_management'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\software\Microsoft\internet explorer\main\featurecontrol\feature_addon_management' -name 'visio.exe' -value 1 -Type DWord")
