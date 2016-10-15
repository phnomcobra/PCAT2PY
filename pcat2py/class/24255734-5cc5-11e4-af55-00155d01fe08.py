#!/usr/bin/python
################################################################################
# 24255734-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "24255734-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True

        # Get Registry MultiSZ 
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\SYSTEM\CurrentControlSet\services\LanmanServer\Parameters', 'NullSessionPipes')

        # Output Lines
        self.output = [r'HKLM:\SYSTEM\CurrentControlSet\services\LanmanServer\Parameters', ('NullSessionPipes=')] + multi_sz
	
	# Recommended MultiSZ
	rec_multi_sz = ("COMNAP,COMNODE,SQL\QUERY,SPOOLSS,NETLOGON,LSARPC,SAMR,BROWSER")

	for sz in multi_sz:
	    if sz.lower() not in rec_multi_sz.lower():
	        self.is_compliant = False

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\services'")
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\services\LanmanServer'")
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\services\LanmanServer\Parameters'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\services\LanmanServer\Parameters' -name 'NullSessionPipes' -Type MultiString -value COMNAP,COMNODE,SQL\QUERY,SPOOLSS,NETLOGON,LSARPC,SAMR,BROWSER")
