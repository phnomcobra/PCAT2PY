#!/usr/bin/python
################################################################################
# 2128874a-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2128874a-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        sz = cli.get_reg_sz(r'HKCU:\Software\Policies\Microsoft\Windows\Control Panel\Desktop', 'ScreenSaveActive')

        # Output Lines
        self.output = [r'HKCU:\Software\Policies\Microsoft\Windows\Control Panel\Desktop', ('ScreenSaveActive=' + sz)]

        if sz == "1":
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Windows'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Windows\Control Panel'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\Windows\Control Panel\Desktop'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\Software\Policies\Microsoft\Windows\Control Panel\Desktop' -name 'ScreenSaveActive' -value 1")
