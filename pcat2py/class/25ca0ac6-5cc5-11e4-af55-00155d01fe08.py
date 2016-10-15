#!/usr/bin/python
################################################################################
# 25ca0ac6-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "25ca0ac6-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKCU:\Software\Policies\Microsoft\office\15.0\excel\security\fileblock', 'XL9597WorkbooksandTemplates')

        # Output Lines
        self.output = [r'HKCU:\Software\Policies\Microsoft\office\15.0\excel\security\fileblock', ('XL9597WorkbooksandTemplates=' + str(dword))]

        if dword == 5:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\office\15.0\excel'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\office\15.0\excel\security'")
        cli.powershell(r"New-Item -path 'HKCU:\Software\Policies\Microsoft\office\15.0\excel\security\fileblock'")
        cli.powershell(r"Set-ItemProperty -path 'HKCU:\Software\Policies\Microsoft\office\15.0\excel\security\fileblock' -name 'XL9597WorkbooksandTemplates' -value 5 -Type DWord")
