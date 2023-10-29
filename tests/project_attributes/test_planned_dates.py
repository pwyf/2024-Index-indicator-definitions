from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import BDDTester
from lxml import etree


class TestTitle(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'project_attributes', '16_planned_dates.feature')

        tester = BDDTester(steps_path)
        self.feature = tester.load_feature(feature_path)
        self.test_start = self.feature.tests[0]
        self.test_end = self.feature.tests[1]

    def test_planned_dates_not_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_start(activity) is False
        assert self.test_end(activity) is False

    def test_planned_start_date_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <activity-date type="1" iso-date="2023-01-01"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_start(activity) is True
        assert self.test_end(activity) is False

    def test_planned_end_date_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <activity-date type="3" iso-date="2023-01-01"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_start(activity) is False
        assert self.test_end(activity) is True

    def test_planned_end_date_default_finance_type_exclusion(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-finance-type code="501"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_start(activity) is False
        assert self.test_end(activity) is None

    def test_planned_end_date_transaction_finance_type_exclusion(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <finance-type code="501"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        assert self.test_start(activity) is False
        assert self.test_end(activity) is None
