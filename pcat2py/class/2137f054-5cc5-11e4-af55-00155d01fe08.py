#!/usr/bin/python
################################################################################
# 2137f054-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2137f054-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry BINARY
        binary = cli.get_reg_binary(r'HKLM:\Software\Microsoft\Driver Signing', 'Policy')

        # Output Lines
        self.output = [r'HKLM:\Software\Microsoft\Driver Signing', ('Policy=')] + binary

        if len(binary) == 1:
            if int(binary[0], 0) == 1:
                self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\Software'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Microsoft'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Microsoft\Driver Signing'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\Software\Microsoft\Driver Signing' -name 'Policy' -Type Binary -value 1")
