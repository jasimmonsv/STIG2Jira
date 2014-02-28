#! /usr/bin/python
"""
Test cases for STIG2Jira app
"""

from STIG2Jira import *
import unittest


class UnitTestCheckCheck(unittest.TestCase):
    """All the unit test cases for the Check Class
    """
    test_check = None
    
    def setUp(self):
        self.sys = 'C-18095r1_chk'
        self.name = 'M'
        self.href = 'VMS_XCCDF_Benchmark_Windows_7_STIG.xml'
        self.content = ('Analyze the system using the Security Configuration and'
                  'Analysis snap-in. Expand the Security Configuration and'
                  ' Analysis tree view. '
                  ''
                  'Navigate to Local Policies -&gt; Security Options.'
                  'If the value for “Audit: Shut down system immediately if'
                  ' unable to log security audits” is not set to “Disabled”,'
                  ' then this is a finding. '
                  'The policy referenced configures the following registry value:'
                  'Registry Hive: HKEY_LOCAL_MACHINE '
                  'Registry Path: \System\CurrentControlSet\Control\Lsa'
                  'Value Name:  CrashOnAuditFail'
                  ''
                  'Value Type:  REG_DWORD'
                  'Value:  0')
        
    def test_create_check(self):
        self.test_check = StigCheck(self.name, self.sys, self.href, self.content)
        self.assertIsInstance(self.test_check, StigCheck, 'StigCheck'
                            'was not created properly')
                            
    def tearDown(self):
        self.test_check = None
        
        
class UnitTestCheckReference(unittest.TestCase):
    """All the unit test cases for the Reference class
    """
    test_reference = None
    
    def setUp(self):
        self.title = 'VMS Target Windows 7'
        self.publisher = 'DISA FSO'
        self.type = 'VMS Target'
        self.subject = 'Windows 7'
        self.id = '1712'
        
    def test_create_reference(self):
        self.test_reference = StigReference(self.title, self.publisher, 
                                            self.type, self.subject, self.id)
        self.assertIsInstance(self.test_reference, StigReference, 'StigReference'
                            'was not created properly')
                            
    def tearDown(self):
        self.test_reference = None

        
class UnitTestCheckFix(unittest.TestCase):
    def setUp(self):
        self.fix_id = 'F-29449r1_fix'
        
    def test_create_fix(self):
        self.test_fix = StigFix(self.fix_id)
        self.assertIsInstance(self.test_fix, StigFix)
    
    def tearDown(self):
        self.test_fix = None
    
    
class UnitTestCheckIdent(unittest.TestCase):
    def setUp(self):
        self.system = 'http://cce.mitre.org'
        self.content = 'CCE-10602-1'
        
    def test_create_ident(self):
        test_ident = StigIdent(self.system, self.content)
        self.assertIsInstance(test_ident, StigIdent)
       
       
class UnitTestCheckFixtext(unittest.TestCase):
    def setUp(self):
        self.fixref = ''
        self.content = ''
        
    def test_create_fixtext(self):
        test_fixtext = StigFixtext(self.fixref, self.content)
        self.assertIsInstance(test_fixtext, StigFixtext)
        
        
class UnitTestCheckRule(unittest.TestCase):
    """All the unit test cases for the Rule class
    """
    ref = None
    check = None
    test_rule = None
        
    def setUp(self):
        #setup Ident
        self.ident = StigIdent('http://cce.mitre.org','CCE-10602-1')
        #Setup Reference type
        _title = 'VMS Target Windows 7'
        _publisher = 'DISA FSO'
        _type = 'VMS Target'
        _subject = 'Windows 7'
        _id = '1712'
        self.ref = StigReference(_title, _publisher, _type, _subject, _id)
        self.assertIsInstance(self.ref, StigReference, 'StigReference'
                            'was not created properly')
        #setup Check type
        _sys = 'C-18095r1_chk'
        _name = 'M'
        _href = 'VMS_XCCDF_Benchmark_Windows_7_STIG.xml'
        _content = ('Analyze the system using the Security Configuration and'
                  'Analysis snap-in. Expand the Security Configuration and'
                  ' Analysis tree view. '
                  ''
                  'Navigate to Local Policies -&gt; Security Options. '
                  'If the value for “Audit: Shut down system immediately if'
                  ' unable to log security audits” is not set to “Disabled”,'
                  ' then this is a finding. '
                  'The policy referenced configures the following registry value:'
                  'Registry Hive: HKEY_LOCAL_MACHINE '
                  'Registry Path: \System\CurrentControlSet\Control\Lsa'
                  'Value Name:  CrashOnAuditFail'
                  ''
                  'Value Type:  REG_DWORD'
                  'Value:  0')
        self.check = StigCheck(_name, _sys, _href, _content)
        self.assertIsInstance(self.check, StigCheck, 'StigCheck was not created'
                             ' properly')
        #setup Rule Type
        self.id = 'SV-25033r1_rule'
        self.ver = '3.015'
        self.title = 'System halts once an event log has reached its maximum size.'
        self.desc = ('&lt;VulnDiscussion&gt;A system that is configured to halt if an'
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
        self.fix = StigFix('F-29449r1_fix')
        self.assertIsInstance(self.fix, StigFix, 'StigFix was not created'
                             ' properly')
        #setup test_fixtext
        _fixref = 'F-31r1_fix'
        _content = 'Relocate equipment to a controlled access area.'
        self.test_fixtext = StigFixtext(_fixref, _content)
        self.assertIsInstance(self.test_fixtext, StigFixtext, 'StigFixtext was not created'
                             ' properly')
        #setup test_fixtext
        _fixref = 'F-31r1_fix'
        _content = 'Relocate equipment to a controlled access area.'
        test_fixtext = StigFixtext(_fixref, _content)
        #setup test_fix
        self.test_fix = StigFix('F-29449r1_fix')
        
    def test_create_rule(self):
        self.test_rule = StigRule(self.id, self.ver, self.title, self.desc, self.ref, 
                            self.ident, self.test_fixtext, self.test_fix)
        self.assertIsInstance(self.test_rule, StigRule, 'StigRule was not created' 
                            ' properly')
        
    def test_add_check(self):
        #TODO jasimmonsv@jasimmonsv.com Build list of checks to cycle through
        test_rule = StigRule(self.id, self.ver, self.title, self.desc, self.ref, 
                            self.ident, self.test_fixtext, self.test_fix)
        self.assertTrue(test_rule.add_check(self.check), 'Failed to add check to the'
                  ' Rule')
    
    def test_change_severity(self):
        severity = 'high'
        ch_severity = 'low'
        test_rule = StigRule(self.id, self.ver, self.title, self.desc, self.ref, 
                            self.ident, self.test_fixtext, self.test_fix, severity)
        self.assertTrue(test_rule.severity == severity)
        self.assertTrue(test_rule.change_severity(ch_severity))
        self.assertTrue(test_rule.severity == ch_severity)
        
    def test_change_weight(self):
        severity = 'high'
        weight = 10.0
        ch_weight = 5.3
        test_rule = StigRule(self.id, self.ver, self.title, self.desc, self.ref, 
                            self.ident, self.test_fixtext, self.test_fix, severity, weight)
        self.assertTrue(test_rule.weight == weight)
        self.assertTrue(test_rule.change_weight(ch_weight))
        self.assertTrue(test_rule.weight == ch_weight)
        
    def test_reset_severity(self):
        severity = 'high'
        ch_severity = 'low'
        test_rule = StigRule(self.id, self.ver, self.title, self.desc, self.ref, 
                            self.ident, self.test_fixtext, self.test_fix, severity)
        self.assertTrue(test_rule.severity == severity)
        self.assertTrue(test_rule.change_severity(ch_severity))
        self.assertTrue(test_rule.severity == ch_severity)
        self.assertTrue(test_rule.reset_severity())
        self.assertTrue(test_rule.severity == severity)
        
    def test_reset_weight(self):
        severity = 'high'
        weight = 10.0
        ch_weight = 5.3
        test_rule = StigRule(self.id, self.ver, self.title, self.desc, self.ref, 
                            self.ident, self.test_fixtext, self.test_fix, severity, weight)
        self.assertTrue(test_rule.weight == weight)
        self.assertTrue(test_rule.change_weight(ch_weight))
        self.assertTrue(test_rule.weight == ch_weight)
        self.assertTrue(test_rule.reset_weight())
        self.assertTrue(test_rule.weight == weight)
        
        
class UnitTestCheckGroup(unittest.TestCase):
    """All unit test cases for the Group class
    """
    test_group = None
    test_rule = None
    
    def setUp(self):
        #setup Ident
        test_ident = StigIdent('http://cce.mitre.org','CCE-10602-1')
        self.assertIsInstance(test_ident, StigIdent, 'StigIdent was not '
                             'created properly')
        #Setup Reference type
        _ref_title = 'VMS Target Windows 7'
        _ref_publisher = 'DISA FSO'
        _ref_type = 'VMS Target'
        _ref_subject = 'Windows 7'
        _ref_id = '1712'
        test_ref = StigReference(_ref_title, _ref_publisher, _ref_type, 
                                        _ref_subject, _ref_id)
        self.assertIsInstance(test_ref, StigReference, 'StigReference'
                            'was not created properly')
        #setup Check type
        _check_sys = 'C-18095r1_chk'
        _check_name = 'M'
        _check_href = 'VMS_XCCDF_Benchmark_Windows_7_STIG.xml'
        _check_content = ('Analyze the system using the Security Configuration and'
                  'Analysis snap-in. Expand the Security Configuration and'
                  ' Analysis tree view. '
                  ''
                  'Navigate to Local Policies -&gt; Security Options. '
                  'If the value for “Audit: Shut down system immediately if'
                  ' unable to log security audits” is not set to “Disabled”,'
                  ' then this is a finding. '
                  'The policy referenced configures the following registry value:'
                  'Registry Hive: HKEY_LOCAL_MACHINE '
                  'Registry Path: \System\CurrentControlSet\Control\Lsa'
                  'Value Name:  CrashOnAuditFail'
                  ''
                  'Value Type:  REG_DWORD'
                  'Value:  0')
        test_check = StigCheck(_check_name, _check_sys, _check_href, _check_content)
        self.assertIsInstance(test_check, StigCheck, 'StigCheck was not created'
                             ' properly')
        #setup test_fix
        test_fix = StigFix('F-29449r1_fix')
        self.assertIsInstance(test_fix, StigFix, 'StigFix was not created'
                             ' properly')
        #setup test_fixtext
        _fixref = 'F-31r1_fix'
        _content = 'Relocate equipment to a controlled access area.'
        test_fixtext = StigFixtext(_fixref, _content)
        self.assertIsInstance(test_fixtext, StigFixtext, 'StigFixtext was not created'
                             ' properly')
        #setup Rule Type
        rule_id = 'SV-25033r1_rule'
        rule_ver = '3.015'
        rule_title = 'System halts once an event log has reached its maximum size.'
        rule_desc = ('&lt;VulnDiscussion&gt;A system that is configured to halt if an'
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
        self.test_rule = StigRule(rule_id, rule_ver, rule_title, rule_desc, 
                             test_ref, test_ident, test_fixtext, test_fix)
        #Setup Group vars
        self.id = 'V-1090'
        self.title = 'Caching of logon credentials'
        self.desc = '&lt;GroupDescription&gt;&lt;/GroupDescription&gt;'
        self.rules = []
        
    def test_create_group(self):
        test_group = StigGroup(self.id, self.title, self.desc)
        self.assertIsInstance(test_group, StigGroup, 'StigGroup was not created'
                             'properly')
    
    def test_add_single_rule(self):
        test_group = StigGroup(self.id, self.title, self.desc)
        self.assertTrue(test_group.add_rule(self.test_rule))
        #TODO jasimmonsv@jasimmonsv.com Add more complete add rule tests
        
    def test_add_multiple_rules(self):
        test_group = StigGroup(self.id, self.title, self.desc)
        self.assertTrue(test_group.add_rule(self.test_rule))
        self.assertTrue(test_group.add_rule(self.test_rule))
        self.assertTrue(test_group.rules[0].ID == test_group.rules[1].ID)
        
        
class TestParseReference(unittest.TestCase): #TODO Build ParseReference TC
    def setUp(self):
        pass
        
        
class TestParseFixtext(unittest.TestCase):  #TODO Build ParseFixtext TC
    def setUp(self):
        pass

        
class TestParseRules(unittest.TestCase):  #TODO Build ParseRules TC
    def setUp(self):
        pass
        
        
class TestReadXML(unittest.TestCase):
    
    def setUp(self):
        from xml.dom.minidom import parse, parseString
        XML_FILE = 'U_Windows_7_V1R13_STIG_Manual-xccdf.xml'
        doc = parse(XML_FILE)
        self.groups = doc.getElementsByTagName('Group')
        
    def test_load_XML(self):
        group_title = ''
        group_description = ''
        group_rules = ''
        for node in self.groups:
            id = node.getAttribute('id')
            for x in node.childNodes:
                if x.nodeType == 3: #if node is a Text node
                    pass
                else:
                    if x.nodeName == 'title': 
                        group_title = x.firstChild.nodeValue
                    elif x.nodeName == 'description':
                        group_description = x.firstChild.nodeValue
                    elif x.nodeName == 'Rule':
                        group_rules = x
                            
    def test_parse_XML(self):
        group_title = ''
        group_description = ''
        group_rules = ''
        for node in self.groups:
            id = node.getAttribute('id')
            for x in node.childNodes:
                if x.nodeType == 3: #if node is a Text node
                    pass
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
            tmp_group.add_rule(parse_rules(group_rules))
            stig_groups.append(tmp_group) #append group only after fully built from xml        

            
if __name__ == '__main__':
    suiteCheck = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckCheck)
    suiteReference = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckReference)
    suiteFix = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckFix)
    suiteFixtext = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckFixtext)
    suiteIdent = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckIdent)
    suiteRule = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckRule)
    suiteGroup = unittest.TestLoader().loadTestsFromTestCase(UnitTestCheckGroup)
    suiteXML = unittest.TestLoader().loadTestsFromTestCase(TestReadXML)
    unittest.TextTestRunner(verbosity=2).run(suiteCheck)
    unittest.TextTestRunner(verbosity=2).run(suiteReference)
    unittest.TextTestRunner(verbosity=2).run(suiteFix)
    unittest.TextTestRunner(verbosity=2).run(suiteFixtext)
    unittest.TextTestRunner(verbosity=2).run(suiteIdent)
    unittest.TextTestRunner(verbosity=2).run(suiteRule)
    unittest.TextTestRunner(verbosity=2).run(suiteGroup)
    unittest.TextTestRunner(verbosity=2).run(suiteXML)
    #unittest.main()