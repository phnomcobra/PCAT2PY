PCAT2PY
=======

ABOUT
=====

Pre-Compliance Accreditation Tool for Python

PCAT2PY is a Python based program for scanning and remediating security
findings. This implementation is capable of running locally or remotely
against Red Hat and Windows based operating systems. PCAT2PY
generates standard out debugging and html indicating status, documentation,
and standard output of findings that have been scanned and remediated.

For remote use PCAT2PY uses Windows Remote Management and Secure Shell.
Remote scanning and remediation against Windows based environments requires
WINRM with HTTP, Basic Auth, and Unencrypted traffic enabled. For Red Hat
based environments, SSH has to be enabled and either root login permitted
or a account with sudoers rights must be available. Sudoers must have the
requiretty directive disabled.

CONTENT
=======

PCAT2PY is designed to run as a self-contained executable or run as a script on
the Python interpreter. 

When running as a script, Python 2.6.6 or later is required. In addition, the
following python modules must be installed: pywinrm, ecdsa, paramiko, and pycrypto.
When running as a self-contained executable, no Python interpreter is required.

pcat2py.py - entry point for execution (PCAT2PY starts from this script)
local_cli.py - local command line interface class definition
ssh_cli.py - secure shell command line interface class definition
winrm_cli.py - windows remote management command line interface class definition
session.py - PCAT2PY session class definition
presentation.py - standard output and HTML functions
findings - finding(s) class definitions

HOWTO
=====

PCAT2PY has two modes of operation. It can be used to scan or remediate systems using
findings from the above listed postures. Findings can be individually selected for 
scanning or remediation by supplying the --finding switch. Entire postures can be
selected by supplying the --posture switch. 

Be default, not standard output is generated during runtime. Supplying the --debug 
switch allows different verbosities of output to be generated. Results of a PCAT2PY
session can also be written in HTML by supplying the --html switch.

To scan or remediate a remote system, the --winrm or --ssh switches can be supplied
to run PCAT2PY against a remote system. Passwords will be prompted for unless the
--password switch is supplied.

C:\PCAT2PY>python pcat2py.py

PCAT2PY - Pre-Compliance Accreditation Tool for Python

usage: pcat2py scan [arguments]       evaluate compliance for finding(s)
   or: pcat2py remediate [arguments]  remediate finding(s)
   or: pcat2py list                   list available postures

Arguments:
   --debug <level>       Print debugging information during remediate/scan
                           0: No debugging output (default)
                           1: Displays finding identification and compliance status
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

EXAMPLES
========

./pcat2py.py scan --finding V-38623 --debug 2
./pcat2py.py scan --ssh cobra@192.168.1.60 --posture RHEL6 --html test.html
./pcat2py.py scan --ssh cobra@192.168.1.60 --finding V-38644 --debug 1
./pcat2py.py scan --winrm administrator@pcat2pytest2.phnomlab.net --finding 
HBSPCAT2K8R2MS0000186 --debug 2