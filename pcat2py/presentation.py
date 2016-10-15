#!/usr/bin/python
################################################################################
# PRESENTATION
# 
# Justin Dierking
# justindierking@hardbitsolutions.com
# phnomcobra@gmail.com
#
# Presentation module containing functions for generating HTML reports and 
# printing verbose finding information.
#
# 07/19/2014 Original construction
# 10/25/2014 Standart output method has been removed
# 10/26/2014 Added metabase. Metadata housed as static methods inside the 
#            finding classes has been stored inside the metabase. To minimize 
#            code duplication of the finding classes, class definitions are 
#            assigned and referenced by UUIDs. Finding definitions in the 
#            metadata are also assigned and referenced by UUIDs. The load
#            findings block has been re-written to queue findings by their
#            definition UUIDs. Afterwords finding objects are populated from
#            the indicated class UUIDs referenced in the queued definitions.
#            Even if a class UUID is referenced multiple times, only one
#            object of the class is appended into the session object. Create
#            html report has been re-written to source metadata from the queued
#            findings (xml elements from the metabase) and source the compliance
#            and standard output from the session object.
################################################################################

def create_html_report(session_object, queued_findings, html_filename):
    html_file = open(html_filename, 'w')

    # HTML Header
    html_file.write('<!DOCTYPE html><html><head><style>\
                    .findings{border:1px solid black;border-collapse:collapse;}\
                    th,td{padding:5px;}\
                    </style></head><body>')

    # Title and uname table
    html_file.write('<table><tr><th><h1>PCAT2PY</h1></th><th>' + \
                    session_object.cli.system("hostname") + \
                    '</th></tr></table>')

    # Start of findings table. Define the headings for compliance, id, h/f
    # and details.
    html_file.write('<table class="findings"><tr>\
                    <th class="findings">COMPLIANCE</th>\
                    <th class="findings" style="width:250px">ID</th>\
                    <th class="findings">H/F</th>\
                    <th class="findings">DETAILS</th></tr>')

    for finding in queued_findings:
        try:
            if session_object.findings[finding.find('class').attrib['uuid']].is_compliant:
                status = 'COMPLIANT'
            else:
                status = 'NON-COMPLIANT'
        except AttributeError:
            status = 'MANUAL'
        
        
        
        # Compliance        
        try:
            if status == 'COMPLIANT':
                html_file.write('<tr><td class="findings" style="background-color:rgb(0,255,0)">Closed</td>')
            elif status == 'NON-COMPLIANT' and finding.find('severity').text == 'CAT I':
                html_file.write('<tr><td class="findings" style="background-color:rgb(255,0,0)">Open</td>')
            elif status == 'NON-COMPLIANT' and finding.find('severity').text == 'CAT II': 
                html_file.write('<tr><td class="findings" style="background-color:rgb(255,127,0)">Open</td>')
            elif status == 'NON-COMPLIANT' and finding.find('severity').text == 'CAT III': 
                html_file.write('<tr><td class="findings" style="background-color:rgb(255,255,0)">Open</td>')
            else: 
                html_file.write('<tr><td class="findings">Manual</td>')
        except AttributeErrot:
            html_file.write('<tr><td class="findings">Manual</td>')



        # Id
        html_file.write('<td class="findings">')
        
        try:
            html_file.write("<b>POSTURE:</b> " + finding.find('posture').text + "<br>")
        except AttributeError:
            pass
        
        try:
            html_file.write("<b>GROUP ID:</b> " + finding.find('group_id').text + "<br>")
        except AttributeError:
            pass
        
        try:
            html_file.write("<b>HBS ID:</b> " + finding.find('hbs_id').text + "<br>")
        except AttributeError:
            pass
        
        try:
            html_file.write("<b>NIST 800 53:</b> " + finding.find('nist_800_53').text + "<br>")
        except AttributeError:
            pass
        
        try:
            html_file.write("<b>ISO 27001:</b> " + finding.find('iso_27001').text + "<br>")
        except AttributeError:
            pass
        
        try:
            html_file.write("<b>PCI:</b> " + finding.find('pci').text + "<br>")
        except AttributeError:
            pass
        
        try:
            html_file.write("<b>HIPPA:</b> " + finding.find('hippa').text + "<br>")
        except AttributeError:
            pass

        html_file.write('</td>')
        
        

        # Does finding have a fix method
        try:
            if hasattr(session_object.findings[finding.find('class').attrib['uuid']], "fix"): 
                html_file.write('<td class="findings">Yes</td>')
            else: 
                html_file.write('<td class="findings">No</td>')
        except AttributeError:
            html_file.write('<td class="findings">No</td>')
            


        # Title and discussion
        html_file.write('<td class="findings"><b>')
        
        try:
            html_file.write(finding.find('rule_title').text + '</b><br>')
        except AttributeError:
            pass
        
        try:
            html_file.write(finding.find('vulnerability_discussion').text)
        except AttributeError:
            pass
        
        html_file.write('<i>')



        # Verbose output
        try:
            if finding.find('class').attrib['uuid']: 
                for line in session_object.findings[finding.find('class').attrib['uuid']].output: 
                    html_file.write('<br>' + line)
        except AttributeError:
            pass



        # Conclude row
        html_file.write('</i></td></tr>')

    # Close remaining html tags
    html_file.write('</table></body></html>')

    html_file.close()