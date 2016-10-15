#!/usr/bin/python
################################################################################
# 24d24c3c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "24d24c3c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKCU:\software\policies\Microsoft\office\15.0\outlook\options\autoformat', 'pgrfafo_25_1')

        # Output Lines
        self.output = [r'HKCU:\software\policies\Microsoft\office\15.0\outlook\options\autoformat', ('pgrfafo_25_1=' + str(dword))]

        if dword == 0:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\software\policies\Microsoft\office\15.0\outlook'")
        cli.powershell(r"New-Item -path 'HKCU:\software\policies\Microsoft\office\15.0\outlook\options'")
        cli.powershell(r"New-Item -path 'HKCU:\software\policies\Microsoft\office\15.0\outlook\options\autoformat'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\software\policies\Microsoft\office\15.0\outlook\options\autoformat' -name 'pgrfafo_25_1' -value 0 -Type DWord")
