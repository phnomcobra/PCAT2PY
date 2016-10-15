#!/usr/bin/python
################################################################################
# 25ce1e90-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "25ce1e90-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\System\CurrentControlSet\Control\Session Manager\Subsystems', 'Optional')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Control\Session Manager\Subsystems', ('Optional=')] + multi_sz

        if "NULL" in multi_sz:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\Session Manager'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\Session Manager\Subsystems'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Control\Session Manager\Subsystems' -name 'Optional' -Type MultiString -value NULL")
