#!/usr/bin/python
################################################################################
# SSH_CLI
# 
# Justin Dierking
# justindierking@hardbitsolutions.com
# 
# phnomcobra@gmail.com
#
# SSH command line interface class. This class is a wrapper for os.popen. Each
# console object maitains a continuous ssh session to the specified remote host
# using specified credentials.
#
# 06/05/2014 Original construction
# 06/29/2014 Updated system method to execute commands as root or through sudo.
#            If sudoed command utililizes redirection, bash -c is invoked.
# 07/26/2014 Added sudo testing. test_sudo was created to test execution of 
#            sudo. test_sudo gets called locally by the system and connect
#            methods. If sudo fails, and exception is thrown.
# 09/13/2014 Changed initialization to None(s)
################################################################################

import paramiko

class Console:
    def __init__(self):
        self.__ssh = paramiko.SSHClient()
        self.__username = None
        self.__password = None
        self.__remote = None
                
    def set_username(self, username):
        self.__username = username;
        
    def set_password(self, password):
        self.__password = password;

    def set_remote_host(self, remote):
        self.__remote = remote;
    
    def __test_sudo(self):
        # Test sudo if not connected as root
        if not self.__username == "root":
            stdin, stdout, stderr = self.__ssh.exec_command('sudo -S whoami')
            stdin.write(self.__password + '\n')
            stdin.flush()
            if 0 != int(stdout.channel.recv_exit_status()):
                raise NameError('Sudo test failed with ' + self.__username + '@' + self.__remote)
        
    def connect(self):
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh.connect(self.__remote, username = self.__username, password = self.__password)
        self.__test_sudo()

    def system(self, command):
        self.__test_sudo()
        
        if self.__username == "root":
            stdin, stdout, stderr = self.__ssh.exec_command(command)
        else:
            # run sudoed redirection commands through bash -c
            if " > " in command or " >> " in command:
                stdin, stdout, stderr = self.__ssh.exec_command('sudo -S bash -c ' + r"'" + command + r"'")
            else:
                stdin, stdout, stderr = self.__ssh.exec_command('sudo -S ' + command)
            stdin.write(self.__password + '\n')
            stdin.flush()
            
        return stdout.read()