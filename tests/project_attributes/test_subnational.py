from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import BDDTester
from lxml import etree


class TestSubNational(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'project_attributes', '21_sub-national_location.feature')

        tester = BDDTester(steps_path)
        self.feature = tester.load_feature(feature_path)
        self.test = self.feature.tests[1] # location point test
        self.codelists = {'GeographicVocabulary': ['A1', 'A2', 'A3', 'A4', 'G1', 'G2']}

    def test_basic_failure(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is False

    def test_exclusion(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <recipient-region code="998" />
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)


        assert result is None

    def test_transaction_exclusion(self):

        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction ref="1234" humanitarian="1">
            <aid-type code="B01" />   
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is None

    def test_transaction_exclusion_with_2_trasactions(self):

        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction ref="1234" humanitarian="1">
            <aid-type code="A01" />   
          </transaction>
          <transaction ref="1234" humanitarian="1">
            <aid-type code="B01" />   
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is None

    def test_pass_point(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <point />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is True

    def test_pass_location_id(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <location-id vocabulary="G1" code="1453782" />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is True

    def test_fail_location_id(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <location-id code="1453782" />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is False

    def test_pass_location_administrative(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <administrative vocabulary="G1" level="1" code="1453782" />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is True

    def test_fail_location_administrative(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <administrative vocabulary="BAD_CODE" level="1" code="1453782" />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is False

    def test_pass_no_vocabularies(self):
        # This should pass because there's a point element,
        # despite the fact that vocabulary is missing for
        # administrative and location-id

        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <location-id />
            <administrative />
            <point />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is True

    def test_pass_wrong_vocabularies(self):
        # This should pass because there's a point element,
        # despite the fact that vocabulary is missing for
        # administrative and location-id

        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <location>
            <location-id vocabulary="BAD_CODE" />
            <administrative vocabulary="BAD_CODE" />
            <point />
          </location>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is True
