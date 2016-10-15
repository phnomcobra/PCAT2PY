#!/usr/bin/python
################################################################################
# 20bdcef0-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "20bdcef0-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True

        # Get Registry MultiSZ 
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\SYSTEM\CurrentControlSet\control\SecurePipeServers\winreg\allowedExactPaths', 'Machine')

        # Output Lines
        self.output = [r'HKLM:\SYSTEM\CurrentControlSet\control\SecurePipeServers\winreg\allowedExactPaths', ('Machine=')] + multi_sz
	
	# Recommended MultiSZ
	rec_multi_sz = ("System\CurrentControlSet\Control\ProductOptions,System\CurrentControlSet\Control\Server Applications,Software\Microsoft\Windows NT\CurrentVersion")

	for sz in multi_sz:
	    if sz.lower() not in rec_multi_sz.lower():
	        self.is_compliant = False

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\control\SecurePipeServers'")
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\control\SecurePipeServers\winreg'")
        cli.powershell(r"New-Item -path 'HKLM:\SYSTEM\CurrentControlSet\control\SecurePipeServers\winreg\allowedExactPaths'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\SYSTEM\CurrentControlSet\control\SecurePipeServers\winreg\allowedExactPaths' -name 'Machine' -Type MultiString -value System\CurrentControlSet\Control\ProductOptions,System\CurrentControlSet\Control\Server Applications,Software\Microsoft\Windows NT\CurrentVersion")
