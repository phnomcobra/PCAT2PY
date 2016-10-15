#!/usr/bin/python
################################################################################
# WINRM_CLI
# 
# Justin Dierking
# justindierking@hardbitsolutions.com
# phnomcobra@gmail.com
#
# Winrm command line interface class. This class is a wrapper for os.popen. Each
# console object maitains a continuous ssh session to the specified remote host
# using specified credentials.
#
# 09/13/2014 Original construction
# 09/15/2014 Added inspection methods for DWORD, QWORD, SZ, and MULTI SZ
#            Added powershell method
# 09/17/2014 Added STDERR printing to powershell method
# 09/19/2014 Added exception handling to DWORD and QWORD methods
# 09/21/2014 Fixed Get-ItemProperty strings
#            Upgraded DWORD and QWORD exceptions
# 09/23/2014 Added BINARY inspection method
# 09/25/2014 Added Auditpol inspection and mutation methods
# 09/26/2014 Added secedit value and account inpection methods
# 09/30/2014 Fixed quoting bug in auditpol methods
# 10/02/2014 Added connect_https method (untested)
#            Removed domain mutation method
################################################################################

import winrm

class Console:
    #### Console Members #########################
    def __init__(self):
        self.__session = None
        self.__username = None
        self.__password = None
        self.__remote = None
    
    
    #### Connection Methods ######################
    # Set credential, remote host, and domain members. Http connections for 
    # basic auth, non-encrypted winrm sessions only at this point :(
    def set_username(self, username):
        self.__username = username;
        
    def set_password(self, password):
        self.__password = password;

    def set_remote_host(self, remote):
        self.__remote = remote;
            
    def connect_http(self):
        self.__session = winrm.Session(("http://" + self.__remote + ":5985/wsman"), \
                                        auth = (self.__username, self.__password))
    
    def connect_https(self):
        self.__session = winrm.Session(("https://" + self.__remote + ":5986/wsman"), \
                                        auth = (self.__username, self.__password), \
                                        transport = "ssl")


    #### Shell Methods ######################
    # System and Powershell commands are exposed through the following methods.
    # Stdout is returned for both methods after execution is returned.
    def system(self, command):
        return self.__session.run_cmd(command).std_out
    
    def powershell(self, command):
        output = self.__session.run_cmd("powershell -c " + command)
        # print output.std_err
        return output.std_out
    
    
    
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
        cmd = self.__session.run_cmd("powershell -c (Get-ItemProperty '" + key + "').'" + value + "'")
        if not cmd.std_out.strip() == "":
            try:
                v = int(cmd.std_out.strip())
            except ValueError:
                print "\n***********************"
                print "get_reg_dword ValueError:"
                print "winrm: powershell -c (Get-ItemProperty '" + key + "').'" + value + "'"
                print "key: ", key
                print "value: ", value
                print "std_err: ", cmd.std_err.strip()
                print "***********************\n"
        return v
    
    def get_reg_qword(self, key, value):
        v = -1
        cmd = self.__session.run_cmd("powershell -c (Get-ItemProperty '" + key + "').'" + value + "'")
        if not cmd.std_out.strip() == "":
            try:
                v = long(cmd.std_out.strip())
            except ValueError:
                print "\n***********************"
                print "get_reg_qword ValueError:"
                print "winrm: powershell -c (Get-ItemProperty '" + key + "').'" + value + "'"
                print "key: ", key
                print "value: ", value
                print "std_err: ", cmd.std_err.strip()
                print "***********************\n"
        return v
    
    def get_reg_binary(self, key, value):
        numbers = []
        strings = []
        std_out = self.__session.run_cmd("powershell -c (Get-ItemProperty '" + \
                                          key + \
                                         "').'" + value + "'").std_out.strip()
        strings = std_out.split('\r\n')
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
                print "std_err: ", cmd.std_err.strip()
                print "***********************\n"
        return numbers
    
    def get_reg_sz(self, key, value):
        return self.__session.run_cmd("powershell -c (Get-ItemProperty '" + \
                                      key + \
                                      "').'" + value + "'").std_out.strip()
    
    def get_reg_multi_sz(self, key, value):
        return self.__session.run_cmd("powershell -c (Get-ItemProperty '" + \
                                      key + \
                                      "').'" + value + "'").std_out.strip().split('\r\n')
    
    
    
    #### Auditpol Inspection/Mutation Methods
    # Inspection and mutation methods have been implemented for manipulating
    # success and failure settings for audit subcategories.
    def get_auditpol(self, subcategory, sof):
        std_out = self.__session.run_cmd('auditpol /get /subcategory:"' + \
                                         subcategory + '"').std_out
        return sof in std_out.split('\r\n')[3]
        
    def set_auditpol(self, subcategory, sof, enable):
        if enable:
            std_out = self.__session.run_cmd('auditpol /set /subcategory:"' + \
                                             subcategory + \
                                             '" /' + sof.lower() + ':enable').std_out
        else:
            std_out = self.__session.run_cmd('auditpol /set /subcategory:"' + \
                                             subcategory + \
                                             '" /' + sof.lower() + ':disable').std_out
        return "The command was successfully executed." in std_out
    
    
    
    #### Secedit Inspection Methods #########
    # Secedit values can be retrieved by specifying the value in question as a
    # prefix. Getting accounts will attempt to resolve values as sids against
    # the remote hosts LSA.
    def get_secedit_value(self, prefix):
        value = ''
        
        self.__session.run_cmd('secedit /export /cfg dump.inf')
        sec_dump = self.__session.run_cmd('type dump.inf').std_out
        self.__session.run_cmd('del dump.inf')
        
        sec_lines = sec_dump.split('\r\n')
        for line in sec_lines:
            if prefix == line.split('=')[0].strip().strip(' '):
                value = line.split('=')[1].strip().strip(' ')
                
        return value
    
    def get_secedit_account(self, prefix):
        tokens = []
        sids = []
        
        self.__session.run_cmd('secedit /export /cfg dump.inf')
        sec_dump = self.__session.run_cmd('type dump.inf').std_out
        self.__session.run_cmd('del dump.inf')
        
        sec_lines = sec_dump.split('\r\n')
        for line in sec_lines:
            if prefix == line.split('=')[0].strip().strip(' '):
                tokens = line.split('=')[1].strip().strip(' ').split(',')
                
        for token in tokens:
            sid = self.__session.run_cmd("powershell -c ([Security.Principal.SecurityIdentifier]'" + token.strip('*') + \
                                       "').Translate([Security.Principal.NTAccount]).Value").std_out.strip()
            if not sid == '':
                sids.append(sid)
            else:
                sids.append(token)
                
        return sids