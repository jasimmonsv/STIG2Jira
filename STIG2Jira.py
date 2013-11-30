#! /usr/bin/python
"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
See LICENSE file from git repository
https://github.com/jasimmonsv/STIG2Jira


This app will takes DISA formated XML STIG from iase.disa.mil and will parse 
into a data structure for the purpose of further manipulating the data.

The end result at this time is to take the data and import it into test cases
in a Jira system.

Args:
XML_FILE: file of the xml document
"""
import xml.dom.minidom
from xml.dom.minidom import parse, parseString
import unittest

XML_FILE = 'U_Windows_7_V1R13_STIG_Manual-xccdf.xml' #TODO jsimmons@jasimmonsv.com set this from command line

class StigReference(object):
    """A Reference data structure
    
    Attributes:
        title: Title of the Reference
        publisher: Who is publishing this reference
        type: What type of reference does this correspond to.
        subject: What subject (e.g., OS, hardware device, etc)
        identifier: DISA provided identifier
    """
    title = ''
    publisher = ''
    type = ''
    subject = ''
    identifier = ''
    
    def __init__(self, title, pub, type, subject, id):
        self.title = title
        self.publisher = pub
        self.type = type
        self.subject = subject
        self.identifier = id
        
class StigCheck(object):
    """
    This a private class is an internal class built to store the specific check data for
    a given STIG rule.
    """
    SYSTEM=''
    NAME=''
    HREF=''
    CONTENT = ''
    def __init__(self, name, sys = '', href = '', content = ''):
        """
        This class is built to easily store and manipulate the various checks within
        a single STIG.
    
        Args:
            name:
            system:
            href:
            content:
    
        Raises:
        """
        self.SYSTEM = sys
        self.NAME = name
        self.HREF = href
        self.CONTENT = content
        
class StigRule(object):
    """This class is built to easily store and manipulate the various rules 
    within a single STIG.
    
    Attributes:
        ID: id number of the rule
        VERSION: DISA defined version number
        TITLE: Summary title of the Rule
        DESCRIPTION: Longer description of the rule
        REFERENCE: references for the rule
        FIXTEXT: directions on how to fix this finding when realized
        _disa_severity: var to hold the default DISA severity
        severity: default DISA severity, allowed to be altered
        _disa_weight: var to hold the default DISA weight
        weight: default DISA weight, allowed to be altered
        checks: array of checks to perform to determine if a finding exists
    
    """
    ID = ''
    VERSION = ''
    TITLE = ''
    DESCRIPTION = ''
    REFERENCE = '' 
    FIXTEXT = ''
    _DISA_SEVERITY = 0
    severity = 0
    _DISA_WEIGHT = 0
    weight = 0
    checks = []
    
    def __init__(self, id, ver, title, desc, ref, fixtext, severity = 0, weight=0):
        """Inits StigGroup with id, title, desc and a null array of Rules
    
        Args:
            
        """
        self.ID = id
        self.VERSION = ver
        self.TITLE = title
        self.DESCRIPTION = desc
        if isinstance(ref, StigReference):
            self.REFERENCE = ref        
        else: 
            raise Exception('Expecting StigReference type for StigRule')
        self.FIXTEXT = '' #TODO jsimmons@jasimmonsv.com figure out purpose of 
                          #fixtext and fixID
        self.severity = severity
        self._DISA_SEVERITY = severity
        self.weight = weight
        self._DISA_WEIGHT = weight
        
    
    def add_check(self, check):
        self.checks.append(check)
        return True
        
    def change_severity(self, severity):
        self.severity = severity
        return True
    
    def reset_severity(self):
        self.severity = self._DISA_SEVERITY
        return True
        
    def change_weight(self, weight):
        self.weight = weight
        return True
        
    def reset_weight(self):
        self.weight = self._DISA_WEIGHT
        return True
        
        
class StigGroup(object):
    """Class for Group data structure
    
    This class is built to easily store and manipulate the various checks within
    a single STIG.
    
    Attributes:
    ID: specific group ID
    TITLE: Summary of the group purpose
    DESCRIPTION: longer description of group
    RULES: array of rules to check specific group
    """
    ID = ''
    TITLE=''
    DESCRIPTION=''
    rules=[]
    
    def __init__(self, id, title, desc):
        """Inits StigGroup with id, title, desc and a null array of Rules
    
        Args:
            ID: Predefined ID of the specific STIG Group
            TITLE: The title of the STIG Group 
            DESCRIPTION: Description of the STIG Group
            RULES: Array of individual rules that belong to this STIG group
        """
        self.ID = id
        self.TITLE = title
        self.DESCRIPTION = desc
        self.rules = []
    
    def add_rule(self, rule):
        """Add a pre-build rule to the STIG Group
    
        Args:
            rule: this is a prebuilt rule class
        
        Returns:
            Returns True if successful and an error if failure
        
        Raises:
            N/A
        """
        self.rules.append(rule)
        return True
        
    
def main():
    """
    
    Args:
    
    Returns:
    
    Raises:
    """
    doc = parse(XML_FILE)
    groups = doc.getElementsByTagName('Group')
    for node in groups:
        id = node.getAttribute('id')
        for x in node.childNodes:
            if x.nodeType == 3: #if node is a Text node
                node.removeChild(x)
            else:
                if x.nodeName == 'title': 
                    title = ''
                elif x.nodeName == 'description':
                    description = ''
                elif x.nodeName == 'Rule':
                    rules = ''
    pass
    print(doc)
    #TODO jsimmons@jasimmonsv.com read in xml file
    #TODO jsimmons@jasimmonsv.com parse XML FILE
    #TODO jsimmons@jasimmonsv.com move parsed files into data structure
    #TODO jsimmons@jasimmonsv.com using data structure, build JIRA Test Cases
 
if __name__ == '__main__':
    main()