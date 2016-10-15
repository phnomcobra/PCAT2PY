#!/usr/bin/python
################################################################################
# 2393a12c-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "2393a12c-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True

        # Get Registry MultiSZ 
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedExactPaths', 'Machine')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedExactPaths', ('Machine=')] + multi_sz
	
	# Recommended MultiSZ
	rec_multi_sz = ("System\CurrentControlSet\Control\ProductOptions,System\CurrentControlSet\Control\Server Applications,Software\Microsoft\Windows NT\CurrentVersion")

	for sz in multi_sz:
	    if sz.lower() not in rec_multi_sz.lower():
	        self.is_compliant = False

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedExactPaths'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedExactPaths' -name 'Machine' -Type MultiString -value System\CurrentControlSet\Control\ProductOptions,System\CurrentControlSet\Control\Server Applications,Software\Microsoft\Windows NT\CurrentVersion")
