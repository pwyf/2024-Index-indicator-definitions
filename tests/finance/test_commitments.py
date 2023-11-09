from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import BDDTester
from lxml import etree


class TestCommitments(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'finance',
                            '11_commitment.feature')

        tester = BDDTester(steps_path)
        feature = tester.load_feature(feature_path)
        self.test = feature.tests[0]

    def test_commitment_no_value(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <transaction-type code="2"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_commitment_zero_value(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <transaction-type code="2"/>
            <value>0</value>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_commitment_zero_value_decimal(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <transaction-type code="2"/>
            <value>0.0</value>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_commitment_non_zero(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <transaction-type code="2"/>
            <value>123.45</value>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is True

    def test_commitment_not_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <transaction-type code="3"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

