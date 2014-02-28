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
#import xml.dom.minidom
from xml.dom.minidom import parse
#import unittest
import time
import logging
import json
import requests

DEF_SEVERITY = 'high'
DEF_WEIGHT = '10'
XML_FILE = 'U_Windows_7_V1R13_STIG_Manual-xccdf.xml' 
stig_groups = []


class StigIdent(object):
    """A StigIdent data object
    
    Attributes:
        system: a cross reference to DISA tracking
        content: the actual content of the ident
    """
    system = None
    content = None
    
    def __init__(self, sys = None, content = None):
        self.system = sys
        self.content = content
      
      
class StigFixtext(object):
    """A Fixtext data structure
    
    Attributes:
        fixref: a cross reference to DISA tracking
        content: the actual content of the fixtext
    """
    fixref = None
    content = None
    
    def __init__(self, fixref, content):
        self.fixref = fixref
        self.content = content
        
        
class StigFix(object):
    """A Fix data structure
    
    Attributes:
        fix_id: a cross reference DISA id
    """
    fix_id = None
    
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
    title = None
    publisher = None
    type = None
    subject = None
    identifier = None
    
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
    SYSTEM = None
    NAME = None
    HREF = None
    CONTENT = None
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
    ID = None
    VERSION = None
    TITLE = None
    DESCRIPTION = None
    REFERENCE = None
    IDENT = None
    FIXTEXT = None
    FIX = None
    _DISA_SEVERITY = DEF_SEVERITY
    severity = DEF_SEVERITY
    _DISA_WEIGHT = DEF_WEIGHT
    weight = DEF_WEIGHT
    checks = []
    
    def __init__(self, id, ver, title, desc, ref, ident, fixtext, fix, severity = DEF_SEVERITY, weight=DEF_WEIGHT):
        """Inits StigGroup with id, title, desc and a null array of Rules
    
        Args:
            id: Rule ID number (DISA Defined)
            ver: Rule version number
            title: Rule title(DISA Defined)
            desc: Provided rule description
            ref: Reference code
            ident: ???
            fixtext: DISA provided fix text
            fix: DISA provided fix
            severity: DISA provided severity (able to be altered per user)
            weight: DISA provided weight (able to be alterd per user)
            
        Returns:
            Properly formed StigRule object
            
        Raises:
            Exceptions
        """
        self.ID = id
        self.VERSION = ver
        self.TITLE = title
        self.DESCRIPTION = desc
        self.severity = severity
        self._DISA_SEVERITY = severity
        self.weight = weight
        self._DISA_WEIGHT = weight
        self.IDENT=  None
        self.checks=[]
        #Check that all data types are proper
        if isinstance(ref, StigReference):
            self.REFERENCE = ref        
        else: 
            raise Exception('Expecting StigReference type for StigRule')
        if isinstance(fixtext, StigFixtext):
            self.FIXTEXT = fixtext
        else:
            raise Exception('Expecting StigFixtext type for StigRule')
        if isinstance(fix, StigFix):
            self.FIX = fix
        else:
            raise Exception('Expecting StigFix type for StigRule')
        if isinstance(ident, StigIdent) or ident == None:
            self.IDENT = ident
        else:
            raise Exception('Expecting StigIDENT type for StigRule')
    
    def add_check(self, check):
        """Add a check to the provided rule
    
            Args:
                check: fully formed StigCheck object
                ver: Rule version number
                title: Rule title(DISA Defined)
            
            Returns:
                Properly formed StigRule object
            
            Raises:
                Exception
        """
        if isinstance(check, StigCheck):
            self.checks.append(check)
            return True
        else:
            raise Exception('Expecting StigCheck object in StigRule')
        
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
    ID = None
    TITLE = None
    DESCRIPTION = None
    rules = []
    
    def __init__(self, id, title, desc):
        """Inits StigGroup with id, title, desc and a null array of Rules
    
        Args:
            ID: Predefined ID of the specific STIG Group
            TITLE: The title of the STIG Group 
            DESCRIPTION: Description of the STIG Group
            RULES: Array of individual rules that belong to this STIG group
            
        Returns:
            Properly formed StigGroup
        
        Raises:
            N/A
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

        
def parse_reference(ref):
    """Parse the XML element and build StigRefernce
    Args:
        ref: this is an unparsed XML element following DISA Reference schema
      
    Returns:
        Returns a proper StigReference object
      
    Raises:
        N/A
    """
    _title = None
    _pub = None
    _type = None
    _subject = None
    _id = None
    _ret_ref = None
    
    for x in ref.childNodes:
        if x.nodeType == 3:
            pass
        else:
            if x.nodeName == 'dc:title':
                _title = x.firstChild.nodeValue
            elif x.nodeName == 'dc:publisher':
                _pub = x.firstChild.nodeValue
            elif x.nodeName == 'dc:type':
                _type = x.firstChild.nodeValue
            elif x.nodeName == 'dc:subject':
                _subject = x.firstChild.nodeValue
            elif x.nodeName == 'dc:identifier':
                _id = x.firstChild.nodeValue
    
    _ret_ref = StigReference(_title, _pub, _type, _subject, _id)
    #Error check
    if isinstance(_ret_ref, StigReference):
            return _ret_ref
    else:
        raise Exception('StigReference was not created properly')
    
    
def parse_fixtext(fixtext):
    """Parse the XML element and build StigRefernce
        
    Args:
        fixtext: this is an unparsed XML element following DISA Reference 
                 schema
      
    Returns:
        Returns a proper StigFixtext object
     
    Raises:
        Exception if StigFixtext is not a proper instance
    """
    
    _fixref = fixtext.getAttribute('fixref')
    _content = fixtext.firstChild.nodeValue
    _ret_fixtext = StigFixtext(_fixref, _content)
    #Error check
    if isinstance(_ret_fixtext, StigFixtext):
        return _ret_fixtext
    else:
        raise Exception('StigFixtext was not created properly')

        
def parse_check(checks):
    """Pass the XML element and build StigCheck Object
    
    Args:
        checks: an XML Element containing all the Checks for a given Rule
        
    Returns:
        an array of StigRule()
    
    Raises:
        Exception if StigCheck is not a proper instance
    """
    _name = None
    _sys = None
    _href = None
    _content = None
    _sys = checks.getAttribute('system')
    _tmp_check = None
    for x in checks.childNodes:
        if x.nodeType == 3:
            pass
        else:
            if x.nodeName == 'check-content-ref':
                _href = x.getAttribute('href')
                _name = x.getAttribute('name')
            if x.nodeName == 'check-content':
                _content = x.firstChild.nodeValue       
    _tmp_check = StigCheck(_name, _sys, _href, _content)
    if isinstance(_tmp_check, StigCheck):
        return _tmp_check
    else:
        raise Exception('StigCheck was not created properly')
      
      
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
    _rule_version = None
    _rule_title = None
    _rule_desc = None
    _rule_ref = None
    _rule_ident = None
    _rule_fixtext = None
    _rule_fix = None
    _rule_check = []
    _rule_id = rules.getAttribute('id')
    _rule_severity = rules.getAttribute('severity')
    _rule_weight = rules.getAttribute('weight')
    _tmp_rule = None
    for x in rules.childNodes:
        if x.nodeType == 3:
            pass
        else:
            if x.nodeName == 'version':
                _rule_version = x.firstChild.nodeValue
            elif x.nodeName == 'title':
                _rule_title = x.firstChild.nodeValue
            elif x.nodeName == 'description':
                _rule_desc = x.firstChild.nodeValue
            elif x.nodeName == 'reference':
                _rule_ref = parse_reference(x)
            elif x.nodeName == 'ident':
                _rule_ident = StigIdent(x.getAttribute('id'), 
                                        x.firstChild.nodeValue)
            elif x.nodeName == 'fixtext':
                _rule_fixtext = parse_fixtext(x)
            elif x.nodeName == 'fix':
                _rule_fix = StigFix(x.getAttribute('id'))
            elif x.nodeName == 'check':
                _rule_check.append(parse_check(x))
            else:
                raise Exception('Node not recognized')
    _tmp_rule = StigRule(_rule_id, _rule_version, _rule_title, 
                        _rule_desc, _rule_ref, _rule_ident, _rule_fixtext, _rule_fix, 
                        _rule_severity, _rule_weight)
    if len(_rule_check) > 0:
        for i in _rule_check:
            _tmp_rule.add_check(i)
    if isinstance(_tmp_rule, StigRule):
        return _tmp_rule
    else:
        raise Exception('StigRule was not properly created')

def f(x):
    return {
            'high': 1,
            'medium': 2,
            'low': 3
            }[x]
def g(x):
    if x < 14 : return 1
    elif x < 18 : return 2
    elif x < 22 : return 3
    elif x < 26 : return 4
    else: return 5
                
def _json_to_jira(group, project, user, url):
    """ Convirt from STIGGroup to JSON and then ship to Jira
    Args:
        groups: (StigGroup) Master list of all Requirements
        project: string with jira recognized project ID
        user: string with users jira username
        url: string with url to Jira API required
        
    Returns:
        True is succeeded, False in not
    
    Raises:
        AssertionErrors if passed vars are not of correct type.
    """
    assert type(group) is StigGroup, "Passed Group is not type StigGroup: %r" % group
    assert type(project) is str, "Passed Project is not a String: %r" % project
    assert type(user) is str, "Passed user is not a String: %r" % user
    assert type(url) is str, "Passed URL is not a String: %r" % url
        
    #TODO (jasimmonsv) Grab group and dump into variables
    if len(group.rules)>1: raise ValueError("More Rules in this Group then expected")
    _rule = group.rules[0]
    _calc = g(f(_rule.severity) * float(_rule.weight))
    
    _summary = group.ID+" "+group.TITLE
    _priority = str(_calc)
    _labels = [group.ID, _rule.ID]
    _id = "7"
    _assignee = "-1"
    _env = ""
    _desc = ""
    
    _project = {"id":project}
    _issuetype = {"id":_id}
    _reporter = {"name":user}
    _json_assignee = {"name": _assignee}
    _json_priority = {"id":_priority}
    
    _desc = _rule.TITLE+"\n\n"+_rule.DESCRIPTION
    
    #Populate all variables into json structure
    fields = {"project":_project, "summary":_summary, "issuetype":_issuetype,
            "reporter": _reporter, "assignee":_json_assignee, "priority":_json_priority,
            "labels":_labels, "environment":_env, "description":_desc 
            }
    _dict = [{"fields":fields}]
    _data=json.dumps(_dict)
    _headers = {"content-type": "application/json"}
    _resp=requests.post(url=url, data=_data[1:-1], headers=_headers, auth=("jirasys","xxxxxxxx"))
    _data = _resp.content
    return True

def printToHTML(groups):
    """
    Args:
        groups: Master list of all Requirements
        
    Returns:
        True is succeeded, False in not
    
    Raises:
        N/A
    """
    with open('./results.'+str(start)+'.html','w') as f:
        f.write('<html><body>')
        for group in groups:
            f.write(group.ID+"<br>")
            f.write(group.TITLE+"<br>")
            f.write(group.DESCRIPTION+"<br>")
            for rule in group.rules:
                f.write("****Rule****<br>")
                f.write("ID: "+rule.ID+"<br>")
                f.write("DISA Severity: "+rule._DISA_SEVERITY+"<br>")
                f.write("Rule Severity: "+rule.severity+"<br>")
                f.write("DISA Weight: "+rule._DISA_WEIGHT+"<br>")
                f.write("Rule Weight: "+rule.weight+"<br>")
                f.write("Version: "+rule.VERSION+"<br>")
                f.write("Title: "+rule.TITLE+"<br>")
                f.write("Description:<br>")
                f.write("\t"+rule.DESCRIPTION+"<br>")
                f.write("Reference:<br>")
                f.write("\tRef Title:\t"+rule.REFERENCE.title+"<br>")
                f.write("\tRef Publisher:\t"+rule.REFERENCE.publisher+"<br>")
                f.write("\tRef Type:\t"+rule.REFERENCE.type+"<br>")
                f.write("\tRef Subject:\t"+rule.REFERENCE.subject+"<br>")
                f.write("\tRef Identifier:\t"+rule.REFERENCE.identifier+"<br>")
                f.write("Ident: "+str(rule.IDENT)+"<br>")
                f.write("Fixtext:<br>")
                f.write("\tFixref: "+rule.FIXTEXT.fixref+"<br>")
                f.write("\tContent: "+rule.FIXTEXT.content+"<br>")
                f.write("Fix:<br>")
                f.write("\tID:\t"+rule.FIX.fix_id+"<br>")
                f.write("# Rule Checks:\t"+str(len(rule.checks))+"<br>")
                f.write('*****************************<br>')
        f.write('</body></html>')
    f.closed
    return True    
    
def main():
    """
    Args:
        N/A
    Returns:
        True or False
    Raises:
    """
    doc = parse(XML_FILE)
    group_title = None
    group_description = None
    _tmp_rules=[]
    stig_groups=[]
    groups = doc.getElementsByTagName('Group')
    for node in groups:
        _id = node.getAttribute('id')
        for x in node.childNodes:
            if x.nodeType == 3: #if node is a Text node
                pass
            else:
                if x.nodeName == 'title': 
                    group_title = x.firstChild.nodeValue
                elif x.nodeName == 'description':
                    group_description = x.firstChild.nodeValue
                elif x.nodeName == 'Rule':
                    _tmp_rules.append(parse_rules(x))
        tmp_group = StigGroup(_id, group_title, group_description)
        for i in _tmp_rules:
            tmp_group.add_rule(i)
        stig_groups.append(tmp_group) #append group only after fully built from xml
        _id = None
        group_title = None
        group_description = None
        group_rules = None
        _tmp_rules=[]
        tmp_group=None
        i=None
    for group in stig_groups:
        _json_to_jira(group,
                  "10108",      #Change this to specific Project Number
                  "634273",     #Change to users Jira loging
                  "http://jira.cmc.hl.com/rest/api/2/issue")
    print("Done!")
        
        
if __name__ == '__main__':
    start = time.time()
    logging.info('Time Started: %s',start)
    main()
