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
from xml.dom.minidom import Node

XML_FILE = U_Windows_7_V1R13_STIG_Manual-xccdf.xml #TODO jsimmons@jasimmonsv.com set this from command line

class __StigCheck:
    """
    This a private class is an internal class built to store the specific check data for
    a given STIG rule.
    """
    _SYSTEM=''
    _Name=''
    _HREF=''
    _CONTENT = ''
    def __init__(self, name, sys = '', href = '', content = ''):
        """
        This class is built to easily store and manipulate the various checks within
        a single STIG.
    
        Args:
            system:
            name:
            href:
            content:
    
        Raises:
        """
        self._SYSTEM = system
        self._NAME = name
        self._HREF = href
        self._CONTENT = content
        
class StigRule:
    """
    This class is built to easily store and manipulate the various checks within
    a single STIG.
    
    Args:
    
    Raises:
    """
    _ID = ''
    _VERSION = ''
    _TITLE = ''
    _DESCRIPTION = ''
    _REFERENCE #TODO jsimmons@jasimmonsv.com build reference class
    Fixtext(Fixref), fixID #TODO jsimmons@jasimmonsv.com figure out purpose of fixtext and fixID
    _severity = 0
    _weight = 0
    Reference(title, publisher, type, subject, id), 
    _check = StigCheck()
    x=0
    
class StigGroup:
    """
    This class is built to easily store and manipulate the various checks within
    a single STIG.
    
    Args:
    
    Raises:
    """
    _ID = ''
    _TITLE=''
    _DESCRIPTION=''
    _RULES=[]
    
    def __init___(self, title, desc):
    """
    Initalize the Group
    
    Args:
        _TITLE: The title of the STIG Group 
        _DESCRIPTION: Description of the STIG Group
        _RULES: Array of individual rules that belong to this STIG group
    """
        self._TITLE=title
        self._DESCRIPTION=desc
        self._RULES=[]
    
    def add_rule(rule):
        """
        Add a pre-build rule to the STIG Group
    
        Args:
            rule: this is a prebuilt rule class
        
        Returns:
            Returns True if successful and an error if failure
        
        Raises:
            nothing at this time
        """
        Try:
            self._RULES.append(rule)
        Except:
            return e
        return True
        
    
def main():
    """
    
    Args:
    
    Returns:
    
    Raises:
    """
    doc = xml.dom.minidom.parce(xml_file)
    #TODO jsimmons@jasimmonsv.com read in xml file
    #TODO jsimmons@jasimmonsv.com parse XML FILE
    #TODO jsimmons@jasimmonsv.com move parsed files into data structure
    #TODO jsimmons@jasimmonsv.com using data structure, build JIRA Test Cases
 
if __name__ == '__main__':
    main()