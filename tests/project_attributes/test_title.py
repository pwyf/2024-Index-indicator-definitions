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
                            'project_attributes', '14_title.feature')

        tester = BDDTester(steps_path)
        self.feature = tester.load_feature(feature_path)
        self.test = self.feature.tests[0]

    def test_title_not_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_title_is_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <title>
            <narrative>A title</narrative>
          </title>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is True

    def test_title_no_narrative(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <title>A title</title>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_title_is_insufficiently_short(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <title>
            <narrative>Too short</narrative>
          </title>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity)

        assert result is False

    def test_title_is_sufficiently_long(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <title>
            <narrative>A much much longer title</narrative>
          </title>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity)

        assert result is True
