#!/usr/bin/python
################################################################################
# 21064964-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21064964-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True

        # Get Registry MultiSZ 
        multi_sz = cli.get_reg_multi_sz(r'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedPaths', 'Machine')

        # Output Lines
        self.output = [r'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedPaths', ('Machine=')] + multi_sz
	
	# Recommended MultiSZ
	rec_multi_sz = ("Software\Microsoft\OLAP Server,Software\Microsoft\Windows NT\CurrentVersion\Perflib,Software\Microsoft\Windows NT\CurrentVersion\Print,Software\Microsoft\Windows NT\CurrentVersion\Windows,System\CurrentControlSet\Control\ContentIndex,System\CurrentControlSet\Control\Print\Printers,System\CurrentControlSet\Control\Terminal Server,System\CurrentControlSet\Control\Terminal Server\UserConfig,System\CurrentControlSet\Control\Terminal Server\DefaultUserConfiguration,System\CurrentControlSet\Services\Eventlog,System\CurrentControlSet\Services\Sysmonlog")

	for sz in multi_sz:
	    if sz.lower() not in rec_multi_sz.lower():
	        self.is_compliant = False

        return self.is_compliant

    def fix(self, cli):
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg'")
        cli.powershell(r"New-Item -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedPaths'")
        cli.powershell(r"Set-ItemProperty -path 'HKLM:\System\CurrentControlSet\Control\SecurePipeServers\Winreg\AllowedPaths' -name 'Machine' -Type MultiString -value Software\Microsoft\OLAP Server,Software\Microsoft\Windows NT\CurrentVersion\Perflib,Software\Microsoft\Windows NT\CurrentVersion\Print,Software\Microsoft\Windows NT\CurrentVersion\Windows,System\CurrentControlSet\Control\ContentIndex,System\CurrentControlSet\Control\Print\Printers,System\CurrentControlSet\Control\Terminal Server,System\CurrentControlSet\Control\Terminal Server\UserConfig,System\CurrentControlSet\Control\Terminal Server\DefaultUserConfiguration,System\CurrentControlSet\Services\Eventlog,System\CurrentControlSet\Services\Sysmonlog")
