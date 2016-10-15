#!/usr/bin/python
################################################################################
# PCAT2PY
#
# Justin Dierking
# justindierking@hardbitsolutions.com
# phnomcobra@gmail.com
#
# Python implementation of PCAT by Hardbit Solutions:
# The purpose of this exercise is to gain a working understanding for capturing
# standard out and processing output line by line while being backwards
# compatible to Python 2.6.6.
#
# 05/28/2014 Original construction
# 06/29/2014 Added help page
#            Added remote switch for scanning remote hosts
#            Added automatic CLI selection and object instantiation
#            Added remarks
# 07/01/2014 Added HTML report generation
# 07/09/2014 Version Control Test
# 07/13/2014 Moved all compliance evaluation code into the PCAT2PY session
#            object class. This code now serves as a command line wrapper for
#            a session object. Arguments and modes have been collapsed. List, 
#            verbose, and show arguments have been removed. Debug switch has 
#            been rewritten to set the debugging level for the session object.
# 07/19/2014 Changed appending findings and setting debug mode to direct access
#            to members instead of mutation methods.
# 07/26/2014 Add password switch to supply passwords as an argument
# 08/17/2014 Collapsed lib sub-directory
# 09/13/2014 Replace remote switch with ssh and winrm switches
# 09/17/2014 Corrected logon string bug in switches
# 09/19/2014 Added posture switch and removed all "findings selected if none
#            specified" logic. Findings will only be appended if an os or
#            finding switch has been set
# 09/20/2014 Added syntax exception handling to loading findings
# 10/09/2014 Fixed logical bug in load findings block
# 10/11/2014 Updated the help message
# 10/26/2014 Added metabase. Metadata housed as static methods inside the 
#            finding classes has been stored inside the metabase. To minimize 
#            code duplication of the finding classes, class definitions are 
#            assigned and referenced by UUIDs. Finding definitions in the 
#            metadata are also assigned and referenced by UUIDs. The load
#            findings block has been re-written to queue findings by their
#            definition UUIDs. Afterwords finding objects are populated from
#            the indicated class UUIDs referenced in the queued definitions.
#            Even if a class UUID is referenced multiple times, only one
#            object of the class is appended into the session object.
################################################################################

import os
import sys
import getpass
import session
import presentation
import xml.etree.ElementTree as et

selected_findings = None
selected_postures = None
logon_strings = []
html_filename = ''
current_session = session.Session()
protocol = 0



#### User Dialog #############################
def help_message():
    print """
PCAT2PY - Pre-Compliance Accreditation Tool for Python

usage: pcat2py scan [arguments]       evaluate compliance for finding(s)
   or: pcat2py remediate [arguments]  remediate finding(s)
   or: pcat2py list                   list postures

Arguments:
   --debug <level>       Print debugging information during remediate/scan
                           0: No debugging output (default)
                           1: Displays class UUID and compliance status
                           2: Displays standard output
   --finding <finding>   Scan or remediate a specific finding or findings
                           This switch can accept group id, rule id, ...
                           group title, rule version, or severity.
                           Specify multiple findings by inserting commas.
   --posture <posture>   Scan or remediate finding(s) of a specific os.
   --ssh <user@host>     Scan or remediate finding(s) on a ssh connection
                           Remote user must be root or have sudo
                           Defaults !requiretty must be in the sudoers
                           User will be prompted for password
   --winrm <user@host>   Scan or remediate finding(s) on a winrm connection
                           User will be prompted for password
   --password <password> Supply password as an argument. If this switch ...
                           is not called in addition to the remote switch, ...
                           the user will be prompted for a password.
   --html <filename>     Generate html report

Examples:
    ./pcat2py.py scan --finding V-38623 --debug 3
    ./pcat2py.py scan --posture RHEL6 --debug 1 --html me
    ./pcat2py.py scan --ssh cobra@192.168.1.60 --finding V-38644 --debug 3
    ./pcat2py.py scan --winrm administrator@pcat2pytest2.phnomlab.net --finding 
        HBSPCAT2K8R2MS0000186 --debug 3
    """



#### Setup and Configure PCAT2PY Session #####
# Create a PCAT2PY session object and configure it based on the provided
# command line arguments. Switches have been setup for debugging, remote hosts,
# selected findings, and HTML report generation. If no arguments have been
# provided, the help message is displayed. If the remote switch has been set,
# start the SSH CLI inside of the session object. Loop through all the command 
# line arguments and look for switch statements. Check to see if a string is 
# prepended by '-' for single character switches or '--' for multi-character 
# switches signalling options.

# If no command line arguments are present then display help message and exit.
if len(sys.argv) == 1:
    help_message()
    sys.exit(1)

for i in range(1, len(sys.argv)):
    if str(sys.argv[i]).startswith("-"):
        if str(sys.argv[i])[1] == "-":
            # Debug level switch
            if str(sys.argv[i])[2:] == "debug" and i + 1 < len(sys.argv):
                if int(sys.argv[i + 1]) in range(0, 4):
                    current_session.debug_mode = int(sys.argv[i + 1])
            
            # Finding switch
            if str(sys.argv[i])[2:] == "finding" and i + 1 < len(sys.argv):
                selected_findings = []
                for element in str(sys.argv[i + 1]).split(','): 
                    selected_findings.append(element)
                    
            # Posture switch
            if str(sys.argv[i])[2:] == "posture" and i + 1 < len(sys.argv):
                selected_postures = str(sys.argv[i + 1]).split(',') 
            
            # SSH switch
            if str(sys.argv[i])[2:] == "ssh" and i + 1 < len(sys.argv):
                logon_strings = str(sys.argv[i + 1]).split('@')
                protocol = 1
                
            # WINRM switch
            if str(sys.argv[i])[2:] == "winrm" and i + 1 < len(sys.argv):
                logon_strings = str(sys.argv[i + 1]).split('@')
                protocol = 2
            
            # Password switch
            if str(sys.argv[i])[2:] == "password" and i + 1 < len(sys.argv):
                if len(logon_strings) == 2:
                    logon_strings.append(str(sys.argv[i + 1]).strip())
                
            # HTML report switch
            if str(sys.argv[i])[2:] == "html" and i + 1 < len(sys.argv):
                html_filename = str(sys.argv[i + 1])
                if ".html" not in html_filename: html_filename += ".html"

# Setup remote connection if logon_strings has been populated.
# logon_string[0]: username
# logon_string[1]: remote host
# logon_string[2]: password
if len(logon_strings) == 2 and protocol == 1:
    current_session.connect_ssh_cli(logon_strings[1], 
                                    logon_strings[0], 
                                    getpass.getpass('Password: '))
if len(logon_strings) == 3 and protocol == 1:
    current_session.connect_ssh_cli(logon_strings[1], 
                                    logon_strings[0], 
                                    logon_strings[2])
if len(logon_strings) == 2 and protocol == 2:
    current_session.connect_winrm_cli(logon_strings[1], 
                                      logon_strings[0], 
                                      getpass.getpass('Password: '))
if len(logon_strings) == 3 and protocol == 2:
    current_session.connect_winrm_cli(logon_strings[1], 
                                      logon_strings[0], 
                                      logon_strings[2])

                

#### Queue Findings ##########################
# Based on the finding and/or posture switches arguments, query the metabase XML
# for finding elements that are member of a selected posture(s). Additionally,
# query the metabase for findings containing a selected finding(s). If both
# switches are thrown, the queried results from both are anded. 
# Parse and mount the metabase
tree = et.parse('metabase.xml')
metabase_root = tree.getroot()

# Loop through the findings keys in the metabase
queued_findings = []
for finding in metabase_root:
    if selected_postures:
        if finding.find('posture').text in selected_postures:
            if selected_findings:
                # Both a posture and finding switch was given to queue findings
                for element in finding:
                    if element.text in selected_findings:
                        queued_findings.append(finding)
                        break
            else:
                # Only a posture switch was given to queue findings
                queued_findings.append(finding)
    elif selected_findings:
        # Only a finding switch was given to queue findings
        for element in finding:
            if element.text in selected_findings:
                queued_findings.append(finding)
                break



#### Instantiate Objects #####################
# In each of the queued findings, import the indicated module by it's class 
# UUID. Once imported, append a finding object of that class into the session
# object.
sys.path.insert(0, os.getcwd() + "/class")
for finding in queued_findings:            
    try:
        current_session.findings[finding.find('class').attrib['uuid']] = \
            __import__(finding.find('class').attrib['uuid']).Finding()
    except AttributeError:
        pass



#### Scan ####################################
# Execute the scan method in the session object. If an HTML filename was
# specified, execute the create HTML report method as well. Exit after
# completing scan and HTML report.
if(sys.argv[1] == "scan"):
    current_session.scan()
    
    if html_filename:
        presentation.create_html_report(current_session,  
                                        queued_findings, 
                                        html_filename)
    
    sys.exit(0)



#### Remediate ###############################
# Execute the remediate method in the session object. If an HTML filename was
# specified, execute the create HTML report method as well. Exit after
# completing scan and HTML report.
elif(sys.argv[1] == "remediate"):
    current_session.remediate()
    
    if html_filename:
        presentation.create_html_report(current_session,  
                                        queued_findings, 
                                        html_filename)


    
#### List Postures in Metabase ###############
elif(sys.argv[1] == "list"):
    postures = []
    
    for finding in metabase_root:
        if not finding.find('posture').text in postures:
            print finding.find('posture').text
            postures.append(finding.find('posture').text)
    
    sys.exit(0)