#!/usr/bin/python
################################################################################
# LOCAL_CLI
# 
# Justin Dierking
# justindierking@hardbitsolutions.com
# phnomcobra@gmail.com
#
# Local command line interface class. This class is a wrapper for os.popen.
#
# 06/05/2014 Original construction
# 10/01/2014 Added methods from winrm_cli as os.popen calls. System is the only
#            agnostic method between Unix-like and Windows-like operating
#            systems. All other methods require Windows exclusively.
# 10/03/2014 Fixed escape sequences to strip \r and delimit with \n
################################################################################

import os

class Console:
    #### Shell Methods ######################
    # System and Powershell commands are exposed through the following methods.
    # Stdout is returned for both methods after execution is returned.
    def system(self, command):
        return os.popen(command).read()
    
    def powershell(self, command):
        output = os.popen("powershell -c " + command).read()
        return output
    
    
    
    #### Registry Inspection Methods ########
    # The following registry methods have be implemented for use with PCAT CSV
    # based finding check functions: DWORDS, QWORDS, SZ, MULTISZ, and BINARY.
    # DWORDS and QWORDS are returned as type int and long respectively. If a
    # registry key or word (DWORD, QWORD) does not exist, an invalid value of -1
    # is returned. MULTISZs are returned as lists of strings. BINARYs are
    # returned as lists of hex strings. If a SZ, MULTISZ, or BINARY does not
    # exist and empty string or list is returned. If a type mismatch occurs 
    # while getting DWORDs, QWORDs, or BINARYs ValueError exceptions will caught
    # and the return values will be -1 or empty lists respectively. The commands
    # stderr will be outputed along with the offending key and value.
    def get_reg_dword(self, key, value):
        v = -1
        cmd = os.popen("powershell -c (Get-ItemProperty '" + key + "').'" + value + "'").read()
        if not cmd.strip() == "":
            try:
                v = int(cmd.strip())
            except ValueError:
                print "\n***********************"
                print "get_reg_dword ValueError:"
                print "winrm: powershell -c (Get-ItemProperty '" + key + "').'" + value + "'"
                print "key: ", key
                print "value: ", value
                print "***********************\n"
        return v
    
    def get_reg_qword(self, key, value):
        v = -1
        cmd = os.popen("powershell -c (Get-ItemProperty '" + key + "').'" + value + "'").read()
        if not cmd.strip() == "":
            try:
                v = long(cmd.strip())
            except ValueError:
                print "\n***********************"
                print "get_reg_qword ValueError:"
                print "winrm: powershell -c (Get-ItemProperty '" + key + "').'" + value + "'"
                print "key: ", key
                print "value: ", value
                print "***********************\n"
        return v
    
    def get_reg_binary(self, key, value):
        numbers = []
        strings = []
        std_out = os.popen("powershell -c (Get-ItemProperty '" + \
                           key + \
                           "').'" + value + "'").read().strip()
        strings = std_out.strip('\r').split('\n')
        if not strings == []:
            try:
                for i in range(0, len(strings)):
                    numbers.append(hex(int(strings[i])))
        
            except ValueError:
                print "\n***********************"
                print "get_reg_binary ValueError:"
                print "winrm: powershell -c (Get-ItemProperty '" + key + "').'" + value + "'"
                print "key: ", key
                print "value: ", value
                print "***********************\n"
        return numbers
    
    def get_reg_sz(self, key, value):
        return os.popen("powershell -c (Get-ItemProperty '" + \
                        key + \
                        "').'" + value + "'").read().strip()
    
    def get_reg_multi_sz(self, key, value):
        return os.popen("powershell -c (Get-ItemProperty '" + \
                        key + \
                        "').'" + value + "'").read().strip().strip('\r').split('\n')
    
    
    
    #### Auditpol Inspection/Mutation Methods
    # Inspection and mutation methods have been implemented for manipulating
    # success and failure settings for audit subcategories.
    def get_auditpol(self, subcategory, sof):
        std_out = os.popen('auditpol /get /subcategory:"' + \
                           subcategory + '"').read()
        return sof in std_out.strip('\r').split('\n')[3]
        
    def set_auditpol(self, subcategory, sof, enable):
        if enable:
            std_out = os.popen('auditpol /set /subcategory:"' + \
                               subcategory + \
                               '" /' + sof.lower() + ':enable').read()
        else:
            std_out = os.popen('auditpol /set /subcategory:"' + \
                               subcategory + \
                               '" /' + sof.lower() + ':disable').read()
        return "The command was successfully executed." in std_out
    
    
    
    #### Secedit Inspection Methods #########
    # Secedit values can be retrieved by specifying the value in question as a
    # prefix. Getting accounts will attempt to resolve values as sids against
    # the remote hosts LSA.
    def get_secedit_value(self, prefix):
        value = ''
        
        os.popen('secedit /export /cfg dump.inf')
        sec_dump = os.popen('type dump.inf').read()
        os.popen('del dump.inf')
        
        sec_lines = sec_dump.strip('\r').split('\n')
        for line in sec_lines:
            if prefix == line.split('=')[0].strip().strip(' '):
                value = line.split('=')[1].strip().strip(' ')
                
        return value
    
    def get_secedit_account(self, prefix):
        tokens = []
        sids = []
        
        os.popen('secedit /export /cfg dump.inf')
        sec_dump = os.popen('type dump.inf').read()
        os.popen('del dump.inf')
        
        sec_lines = sec_dump.strip('\r').split('\n')
        for line in sec_lines:
            if prefix == line.split('=')[0].strip().strip(' '):
                tokens = line.split('=')[1].strip().strip(' ').split(',')
                
        for token in tokens:
            sid = os.popen("powershell -c ([Security.Principal.SecurityIdentifier]'" + token.strip('*') + \
                           "').Translate([Security.Principal.NTAccount]).Value").read().strip()
            if not sid == '':
                sids.append(sid)
            else:
                sids.append(token)
                
        return sids