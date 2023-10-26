from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import BDDTester
from lxml import etree


class TestFlowType(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'joining_up', '25_aid_type.feature')

        tester = BDDTester(steps_path)
        feature = tester.load_feature(feature_path)
        self.test_present = feature.tests[0]
        self.test = feature.tests[1]
        self.codelists = {'AidType': ['A01', 'A02']}

    def test_default_aid_type_on_codelist(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_present(activity, codelists=self.codelists) is True
        assert self.test(activity, codelists=self.codelists) is True

    def test_default_aid_type_not_on_codelist(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="BAD"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is False

    def test_aid_type_on_codelist(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="A02"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is True

    def test_aid_type_not_on_codelist(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="BAD"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_present(activity, codelists=self.codelists) is True
        assert self.test(activity, codelists=self.codelists) is False

    def test_1_aid_type_not_on_codelist(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02"/>
          <transaction>
            <aid-type code="BAD"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is False

    # These next few are the same as the above,
    # just with vocabulary=1 explicitly defined,
    # instead of implicit.
    def test_default_aid_type_on_codelist_vocabulary_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02" vocabulary="1"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_present(activity, codelists=self.codelists) is True
        assert self.test(activity, codelists=self.codelists) is True

    def test_default_aid_type_not_on_codelist_vocabulary_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="BAD" vocabulary="1"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_present(activity, codelists=self.codelists) is True
        assert self.test(activity, codelists=self.codelists) is False

    def test_aid_type_on_codelist_vocabulary_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="A02" vocabulary="1"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is True

    def test_aid_type_not_on_codelist_vocabulary_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="BAD" vocabulary="1"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is False

    def test_1_aid_type_not_on_codelist_vocabulary_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02" vocabulary="1"/>
          <transaction>
            <aid-type code="BAD" vocabulary="1"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is False

    def test_default_aid_type_other_vocabulary(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02" vocabulary="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_present(activity, codelists=self.codelists) is True
        assert self.test(activity, codelists=self.codelists) is False

    def test_aid_type_other_vocabulary(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="A02" vocabulary="2"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_present(activity, codelists=self.codelists) is True
        assert self.test(activity, codelists=self.codelists) is False

    def test_default_aid_type_mixed_vocabulary(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02" />
          <default-aid-type code="1" vocabulary="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is True

    def test_aid_type_mixed_vocabulary(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="A02" />
            <aid-type code="1" vocabulary="2"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is True

    def test_default_aid_type_mixed_vocabulary_vocabularly_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A02" vocabulary="1"/>
          <default-aid-type code="1" vocabulary="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is True

    def test_aid_type_mixed_vocabulary_vocabulary_1(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="A02" vocabulary="1"/>
            <aid-type code="1" vocabulary="2"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
        assert result is True
