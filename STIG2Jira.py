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
import sys

DEF_SEVERITY = 'high'
DEF_WEIGHT = '10'
XML_FILE = 'U_Windows_7_V1R13_STIG_Manual-xccdf.xml' #TODO jsimmons@jasimmonsv.com set this from command line
stig_groups = []

class StigFixtext(object):
    """A Fixtext data structure
    
    Attributes:
        fixref: a cross reference to DISA tracking
        content: the actual content of the fixtext
    """
    fixref = ''
    content = ''
    
    def __init__(self, fixref, content):
        self.fixref = fixref
        self.content = content
        
class StigFix(object):
    """A Fix data structure
    
    Attributes:
        fix_id: a cross reference DISA id
    """
    fix_id = ''
    
    def __init__(self, fix_id):
        self.fix_id = fix_id

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
    FIX = ''
    _DISA_SEVERITY = DEF_SEVERITY
    severity = DEF_SEVERITY
    _DISA_WEIGHT = DEF_WEIGHT
    weight = DEF_WEIGHT
    checks = []
    
    def __init__(self, id, ver, title, desc, ref, fixtext, fix, severity = DEF_SEVERITY, weight=DEF_WEIGHT):
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
        self.FIXTEXT = fixtext
        self.FIX = fix
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
        
def parse_fixtext(fixtext):
    fixref = fixtext.getAttribute('fixref')
    content = fixtext.firstChild.nodeValue
    #TODO jasimmonsv@jasimmonsv.com build fixtext
    pass
    
def parse_rules(rules):
    """
    
    Args:
        rules: an XML Element containing all the rules for a given Group
        
    Returns:
        an array of StigRule()
    
    Raises:
        Exception 'Node not recognized' if there is a childNode that has not 
        been seen before
    """
    #TODO jsimmons@jasimmosnv.com Build Rules from xml blob
    try:
        rule_id = rules.getAttribute('id')
        rule_severity = rules.getAttribute('severity')
        rule_weight = rules.getAttribute('weight')
    except:
        print(sys.exc_info()[0])
    for x in rules.childNodes:
        if x.nodeType == 3:
            rules.removeChild(x)
        else:
            if x.nodeName == 'version':
                rule_version = x.firstChild.nodeValue
            elif x.nodeName == 'title':
                rule_title = x.firstChild.nodeValue
            elif x.nodeName == 'description':
                rule_desc = x #TODO jasimmonsv@jasimmonsv.com build description
            elif x.nodeName == 'reference':
                rule_ref = x #TODO jasimmonsv@jasimmonsv.com build reference
            elif x.nodeName == 'fixtext':
                rule_fixtext = parse_fixtext(x)
            elif x.nodeName == 'fix':
                rule_fix = x.getAttribute('id')
            elif x.nodeName == 'check':
                rule_check = x #TODO jasimmonsv@jasimmonsv.com build check
            else:
                raise Exception('Node not recognized')
                print(x)
        return_rules.append(Stig_Rule(rule_id, rule_version, rule_title, 
                            rule_desc, rule_ref, rule_fixtext, rule_fix, 
                            rule_severity, rule_weight))
    return return_rules
def main():
    """
    
    Args:
    
    Returns:
    
    Raises:
    """
    doc = parse(XML_FILE)
    group_title = ''
    group_description = ''
    group_rules = ''
    groups = doc.getElementsByTagName('Group')
    for node in groups:
        id = node.getAttribute('id')
        for x in node.childNodes:
            if x.nodeType == 3: #if node is a Text node
                node.removeChild(x)
            else:
                if x.nodeName == 'title': 
                    group_title = x.firstChild.nodeValue
                elif x.nodeName == 'description':
                    group_description = x.firstChild.nodeValue
                elif x.nodeName == 'Rule':
                    group_rules = x
        tmp_group = StigGroup(id, group_title, group_description)
        
        #loop through the def build_rules that takes rules xml blob and creates 
        #an array of rules
        print(group_rules)
        for x in parse_rules(group_rules): 
            stig_groups.add_rule(x)
        stig_groups.append(tmp_group) #append group only after fully built from xml
    
    #TODO jsimmons@jasimmonsv.com move parsed files into data structure
    #TODO jsimmons@jasimmonsv.com using data structure, build JIRA Test Cases
 
if __name__ == '__main__':
    main()