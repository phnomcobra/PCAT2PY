#!/usr/bin/python
################################################################################
# 273edb2a-5cc5-11e4-af55-00155d01fe08
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
        self.uuid = "273edb2a-5cc5-11e4-af55-00155d01fe08"
        
    def check(self, cli):
        # Initialize Compliance
        self.is_compliant = True
        
        # Execute command and parse capture standard output
        stdout = cli.system("cat /etc/init/control-alt-delete.conf")
        
        # Split output lines
        self.output = stdout.split('\n')

        # Process standard output
        lineNumber = 0	
        for line in self.output:
            lineNumber += 1
        
            if "exec /sbin/shutdown -r now" in line:
                self.is_compliant = False
                
        return self.is_compliant

    def fix(self, cli):
        cli.system("sed -i '/^exec/d' /etc/init/control-alt-delete.conf")
        cli.system('echo "exec /usr/bin/logger -p security.info Ctrl-Alt-Delete pressed" > /etc/init/control-alt-delete.conf')
