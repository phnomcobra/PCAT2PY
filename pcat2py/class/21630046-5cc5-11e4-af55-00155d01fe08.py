#!/usr/bin/python
################################################################################
# 21630046-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "21630046-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = False
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/issue")
        
        # Split stdout
        self.output = stdout.split('\n')
        
        # Process standard output
        if "attorneys, psychotherapists, or clergy" in stdout:
            self.is_compliant = True
        
        return self.is_compliant

    def fix(self, cli):
        cli.system("/dev/null > /etc/issue")
        cli.system('echo "You are accessing a U.S. Government (USG) Information System (IS) that is provided for USG-authorized use only. By using this IS (which includes any device attached to this IS), you consent to the following conditions:" >> /etc/issue')
        cli.system('echo "-The USG routinely intercepts and monitors communications on this IS for purposes including, but not limited to, penetration testing, COMSEC monitoring, network operations and defense, personnel misconduct (PM), law enforcement (LE), and counterintelligence (CI) investigations." >> /etc/issue')
        cli.system('echo "-At any time, the USG may inspect and seize data stored on this IS." >> /etc/issue')
        cli.system('echo "-Communications using, or data stored on, this IS are not private, are subject to routine monitoring, interception, and search, and may be disclosed or used for any USG-authorized purpose." >> /etc/issue')
        cli.system('echo "-This IS includes security measures (e.g., authentication and access controls) to protect USG interests -- not for your personal benefit or privacy." >> /etc/issue')
        cli.system('echo "-Notwithstanding the above, using this IS does not constitute consent to PM, LE or CI investigative searching or monitoring of the content of privileged communications, or work product, related to personal representation or services by attorneys, psychotherapists, or clergy, and their assistants. Such communications and work product are private and confidential. See User Agreement for details." >> /etc/issue')
