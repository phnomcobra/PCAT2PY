#!/usr/bin/python
################################################################################
# 210d8ecc-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "210d8ecc-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters', 'NullSessionShares')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters', ('NullSessionShares=')] + multi_sz

        if multi_sz == ['']:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\LanManServer'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters' -name 'NullSessionShares' -Type MultiString -value $null")
