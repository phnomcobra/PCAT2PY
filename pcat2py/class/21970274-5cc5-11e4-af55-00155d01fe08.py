#!/usr/bin/python
################################################################################
# 21970274-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21970274-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True

        # Get Registry MultiSZ 
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters', 'nullSessionPipes')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters', ('nullSessionPipes=')] + multi_sz
	
	# Recommended MultiSZ
	rec_multi_sz = ("NETLOGON,SAMR,LSARPC")

	for sz in multi_sz:
	    if sz.lower() not in rec_multi_sz.lower():
	        self.is_compliant = False

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\LanManServer'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Services\LanManServer\Parameters' -name 'nullSessionPipes' -Type MultiString -value NETLOGON,SAMR,LSARPC")
