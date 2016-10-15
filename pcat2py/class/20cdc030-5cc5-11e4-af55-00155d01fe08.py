#!/usr/bin/python
################################################################################
# 20cdc030-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20cdc030-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        sz = cli.get_reg_sz(r'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping\Autorun.inf', '(Default)')

        # Output Lines
        self.output = [r'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping\Autorun.inf', ('(Default)=' + sz)]

        if sz == "@SYS:DoesNotExist":
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping\Autorun.inf'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping\Autorun.inf' -name '(Default)' -value @SYS:DoesNotExist")
