from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import BDDTester
from lxml import etree


class TestCapitalSpend(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'finance', '13_budget_alignment.feature')

        tester = BDDTester(steps_path)
        feature = tester.load_feature(feature_path)
        self.test = feature.tests[0]

    def test_capital_spend_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A09"/>
          <transaction>
            <aid-type code="A03"/>
          </transaction>
          <capital-spend percentage="0"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is True

    def test_capital_spend_not_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_capital_spend_not_relevant_status(self):
        xml = '''
        <iati-activity>
          <activity-status code="1"/>
          <activity-date type="4" iso-date="2011-01-01"/>
          <capital-spend percentage="100"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, today="2011-02-01")

        assert result is None

    def test_capital_spend_not_relevant_aid_type(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="{}"/>
          <capital-spend percentage="100"/>
        </iati-activity>
        '''

        for aid_type in ['A01', 'A02', 'G01']:
            activity = etree.fromstring(xml.format(aid_type))
            result = self.test(activity)

            assert result is None

    def test_capital_spend_not_relevant_transaction_aid_type(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <transaction>
            <aid-type code="A01"/>
          </transaction>
          <capital-spend percentage="100"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is None


class TestCRSCode(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'finance', '13_budget_alignment.feature')

        tester = BDDTester(steps_path)
        feature = tester.load_feature(feature_path)
        self.test = feature.tests[1]
        self.codelists = {'Sector': ['1000']}

    def test_sector_code(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A09"/>
          <transaction>
            <aid-type code="A03"/>
          </transaction>
          <sector code="1000"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is True

    def test_bad_sector_code(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A09"/>
          <transaction>
            <aid-type code="A03"/>
          </transaction>
          <sector code="43030"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is False

    def test_not_sector_code(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A09"/>
          <transaction>
            <aid-type code="A03"/>
          </transaction>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)

        assert result is False

    def test_sector_code_not_on_codelist(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <default-aid-type code="A09"/>
          <transaction>
            <aid-type code="A03"/>
          </transaction>
          <sector code="NOTACODE"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity, codelists=self.codelists)
