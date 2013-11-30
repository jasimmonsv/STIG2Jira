#! /usr/bin/python
"""
Test cases for STIG2Jira app
"""

from STIG2Jira import StigRule
from STIG2Jira import StigGroup
from STIG2Jira import StigCheck
from STIG2Jira import StigReference
import unittest

class TestReadXML(unittest.TestCase):
    def setUp(self):
        pass

class TestCheckCheck(unittest.TestCase):
    """All the unit test cases for the Check Class
    """
    test_check = None
    
    def setUp(self):
        sys = 'C-18095r1_chk'
        name = 'M'
        href = 'VMS_XCCDF_Benchmark_Windows_7_STIG.xml'
        content = ('Analyze the system using the Security Configuration and'
                  'Analysis snap-in. Expand the Security Configuration and'
                  ' Analysis tree view. '
                  ''
                  'Navigate to Local Policies -&gt; Security Options. '

'               If the value for “Audit: Shut down system immediately if unable to log security audits” is not set to “Disabled”, then this is a finding. '

                'The policy referenced configures the following registry value:'

                'Registry Hive: HKEY_LOCAL_MACHINE '
                'Registry Path: \System\CurrentControlSet\Control\Lsa'

                'Value Name:  CrashOnAuditFail'
                ''
                'Value Type:  REG_DWORD'
                'Value:  0')
        self.test_check = StigCheck(name, sys, href, content)
        assertIsInstance(self.test_check, StigCheck, 'StigCheck'
                            'was not created properly')
        
class TestCheckReference(unittest.TestCase):
    """All the unit test cases for the Reference class
    """
    test_reference = None
    
    def setUp(self):
        title = 'VMS Target Windows 7'
        publisher = 'DISA FSO'
        type = 'VMS Target'
        subject = 'Windows 7'
        id = '1712'
        self.test_reference = StigReference(title, publisher, type, subject, id)
        self.assertIsInstance(self.test_reference, StigReference, 'StigReference'
                            'was not created properly')
        
    def test_create_reference(self):
        title = 'VMS Target Windows 7'
        publisher = 'DISA FSO'
        type = 'VMS Target'
        subject = 'Windows 7'
        id = '1712'
        test_reference = StigReference(title, publisher, type, subject, id)
        self.assertIsInstance(test_reference, StigReference, 'StigReference'
                            'was not created properly')
class TestCheckRule(unittest.TestCase):
    """All the unit test cases for the Rule class
    """
    ref = None
    check = None
    test_rule = None
        
    def setUp(self):
        #Setup Reference type
        title = 'VMS Target Windows 7'
        publisher = 'DISA FSO'
        type = 'VMS Target'
        subject = 'Windows 7'
        id = '1712'
        self.ref = StigReference(title, publisher, type, subject, id)
        self.assertIsInstance(self.ref, StigReference, 'StigReference'
                            'was not created properly')
        #setup Check type
        sys = 'C-18095r1_chk'
        name = 'M'
        href = 'VMS_XCCDF_Benchmark_Windows_7_STIG.xml'
        content = ('Analyze the system using the Security Configuration and'
                  'Analysis snap-in. Expand the Security Configuration and'
                  ' Analysis tree view. '
                  ''
                  'Navigate to Local Policies -&gt; Security Options. '

'               If the value for “Audit: Shut down system immediately if unable to log security audits” is not set to “Disabled”, then this is a finding. '

                'The policy referenced configures the following registry value:'

                'Registry Hive: HKEY_LOCAL_MACHINE '
                'Registry Path: \System\CurrentControlSet\Control\Lsa'

                'Value Name:  CrashOnAuditFail'
                ''
                'Value Type:  REG_DWORD'
                'Value:  0')
        self.check = StigCheck(name, sys, href, content)
        self.assertIsInstance(self.check, StigCheck, 'StigCheck was not created'
                             ' properly')
        #setup Rule Type
        id = 'SV-25033r1_rule'
        ver = '3.015'
        title = 'System halts once an event log has reached its maximum size.'
        desc = ('&lt;VulnDiscussion&gt;A system that is configured to halt if an'
               ' event log becomes full can create a denial of service'
               ' situation.&lt;/VulnDiscussion&gt;&lt;FalsePositives&gt;&lt;/'
               ' FalsePositives&gt;&lt;FalseNegatives&gt;&lt;/'
               ' FalseNegatives&gt;&lt;Documentable&gt;false&lt;/Documentable'
               '&gt;&lt;Mitigations&gt;&lt;/Mitigations&gt;&lt;'
               'SeverityOverrideGuidance&gt;&lt;/SeverityOverrideGuidance&gt;'
               '&lt;PotentialImpacts&gt;&lt;/PotentialImpacts&gt;&lt;'
               'ThirdPartyTools&gt;&lt;/ThirdPartyTools&gt;&lt;'
               'MitigationControl&gt;&lt;/MitigationControl&gt;&lt;'
               'Responsibility&gt;System Administrator&lt;/Responsibility&gt;'
               '&lt;IAControls&gt;ECRR-1&lt;/IAControls&gt;')
        fixtext = ''
        severity = 'low'
        weight = '10.0'
        self.test_rule = StigRule(id, ver, title, desc, self.ref, fixtext)
        self.assertIsInstance(self.test_rule, StigRule, 'StigRule was not created' 
                            ' properly')
        
    def test_create_rule(self):
        id = ''
        ver = ''
        title = ''
        desc = ''
        fixtext = ''
        test_rule = StigRule(id, ver, title, desc, self.ref, fixtext)
        self.assertIsInstance(test_rule, StigRule, 'StigRule was not created' 
                            ' properly')
        
    def test_add_check(self):
        #TODO jasimmonsv@jasimmonsv.com Build list of checks to cycle through
        self.assertTrue(self.test_rule.add_check(self.check), 'Failed to add check to the'
                  ' Rule')
    
    def test_change_severity(self):
        pass
        
    def test_change_weight(self):
        pass
        
    def test_reset_severity(self):
        pass
        
    def test_reset_weight(self):
        pass
        
class TestCheckGroup(unittest.TestCase):
    """All unit test cases for the Group class
    """
    test_group = None
    
    def setUp(self):
        id = 'V-1090'
        title = 'Caching of logon credentials'
        desc = '&lt;GroupDescription&gt;&lt;/GroupDescription&gt;'
        rules = []
        self.test_group = StigGroup(id, title, desc)
        self.assertIsInstance(self.test_group, StigGroup, 'StigGroup was not created'
                             'properly')
    
    def test_create_group(self):
        id = ''
        title = ''
        desc = ''
        rules = []
        test_group = StigGroup(id, title, desc)
        self.assertIsInstance(test_group, StigGroup, 'StigGroup was not created'
                             'properly')
    
    def test_add_rule(self):
        self.assertTrue(self.test_group.add_rule(rule))
        
        
class TestCheckClass(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_create_check(self):
        name = 'M'
        sys = 'C-26718r2_chk'
        href = 'VMS_XCCDF_Benchmark_Windows_7_STIG.xml'
        content = ''
        test_check = StigCheck(name, sys, href, content)
        pass

class TestRuleClass(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_create_rule(self):
        pass
    
    def test_modify_rule(self):
        pass
    
if __name__ == '__main__':
    unittest.main()