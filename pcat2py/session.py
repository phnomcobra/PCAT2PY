#!/usr/bin/python
################################################################################
# SESSION
# 
# Justin Dierking
# justindierking@hardbitsolutions.com
# phnomcobra@gmail.com
#
# PCAT2PY Session class. This class contains all methods and members for 
# encapsulating individual PCAT2PY sessions. This class has methods for 
# scanning, remediating, HTML report generation, local or SSH CLI objects, and 
# finding debugging.
#
# 07/09/2014 Original construction
# 07/13/2014 Implemented debugging levels, local and SSH CLI, and HTML
# 07/18/2014 Renamed filename to session.py
# 07/19/2014 Switched to all public methods and members
#            Offloaded print_verbose and create_html_report to presentation.py
# 09/13/2014 Added connect_winrm_cli :)
# 09/21/2014 Added NameError exception handling to scan and remediate methods
# 10/26/2014 Added metabase. Metadata housed as static methods inside the 
#            finding classes has been stored inside the metabase. To minimize 
#            code duplication of the finding classes, class definitions are 
#            assigned and referenced by UUIDs. Finding definitions in the 
#            metadata are also assigned and referenced by UUIDs. The load
#            findings block has been re-written to queue findings by their
#            definition UUIDs. Afterwords finding objects are populated from
#            the indicated class UUIDs referenced in the queued definitions.
#            Even if a class UUID is referenced multiple times, only one
#            object of the class is appended into the session object. As a
#            consequence of using a metabase, the metadata for a finding is no
#            longer exposed to the session object. The debug finding has been
#            reduced to displaying compliance and standard output of the
#            finding class object.
################################################################################

import ssh_cli
import local_cli
import winrm_cli
import traceback

class Session:
    def __init__(self):
        self.cli = local_cli.Console()
	self.findings = {}
        self.debug_mode = 0
    
    def debug_finding(self, finding):
        # Print debugging information based on debug level
        # Level 1: uuid and compliance status
        # Level 2: standard output from check method
        status = None
        if finding.is_compliant:
            status = 'COMPLIANT'
        else: 
            status = 'NON-COMPLIANT'
        
        if self.debug_mode > 1:
            for line in finding.output:
                print line.strip()
            print ""
        
        print finding.uuid + " " + status
        
    def scan(self):
        for finding in self.findings.itervalues():
            if (hasattr(finding, "check")): 
                try:
                    finding.check(self.cli)

                    if self.debug_mode:
                        self.debug_finding(finding)
                except NameError:
                    print "\n***********************"
                    print "scan NameError:"
                    print traceback.format_exc()
                    print "***********************\n"
                
        
    def remediate(self):
        for finding in self.findings.itervalues():
            if (hasattr(finding, "check")): 
                try:
                    if not finding.check(self.cli):
                        if (hasattr(finding, "fix")): 
                            finding.fix(self.cli)
                            finding.check(self.cli)

                    if self.debug_mode:
                        self.debug_finding(finding)
                except NameError:
                    print "\n***********************"
                    print "remediate NameError:"
                    print traceback.format_exc()
                    print "***********************\n"

        
    def connect_ssh_cli(self, host, username, password):
        self.cli = ssh_cli.Console()
        self.cli.set_username(username)
        self.cli.set_password(password)
        self.cli.set_remote_host(host)
        self.cli.connect()
        
    def connect_winrm_cli(self, host, username, password):
        self.cli = winrm_cli.Console()
        self.cli.set_username(username)
        self.cli.set_password(password)
        self.cli.set_remote_host(host)
        self.cli.connect_http()