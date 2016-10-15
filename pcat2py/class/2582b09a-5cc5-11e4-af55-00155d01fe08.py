#!/usr/bin/python
################################################################################
# 2582b09a-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2582b09a-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False

        # Get Registry DWORD
        dword = cli.get_reg_dword(r'HKLM:\Software\Policies\Microsoft\office\15.0\InfoPath\security', 'APTCA_AllowList')

        # Output Lines
        self.output = [r'HKLM:\Software\Policies\Microsoft\office\15.0\InfoPath\security', ('APTCA_AllowList=' + str(dword))]

        if dword == 1:
            self.is_compliant = True

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\Software\Policies\Microsoft\office\15.0'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Policies\Microsoft\office\15.0\InfoPath'")
        cli.powershell(r"New-Item -path 'HKLM:\Software\Policies\Microsoft\office\15.0\InfoPath\security'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\Software\Policies\Microsoft\office\15.0\InfoPath\security' -name 'APTCA_AllowList' -value 1 -Type DWord")
