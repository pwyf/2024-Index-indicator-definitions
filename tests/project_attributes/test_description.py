from os.path import dirname, join, realpath
from unittest import TestCase

from bdd_tester import BDDTester
from lxml import etree


class TestDescription(TestCase):
    def setUp(self):
        self.FILEPATH = dirname(realpath(__file__))
        steps_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                          'step_definitions.py')
        feature_path = join(self.FILEPATH, '..', '..', 'test_definitions',
                            'project_attributes', '15_description.feature')

        tester = BDDTester(steps_path)
        self.feature = tester.load_feature(feature_path)
        self.test = self.feature.tests[0]

    def test_description_not_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_description_is_present(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <description>
            <narrative>A description</narrative>
          </description>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is True

    def test_description_no_narrative(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <description>A description</description>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        result = self.test(activity)

        assert result is False

    def test_description_is_insufficiently_short(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <description>
            <narrative>A short description</narrative>
          </description>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity)

        assert result is False

    def test_description_is_sufficiently_long(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <description>
            <narrative>
              A much much longer description.

              Lorem ipsum dolor sit amet consectetur adipiscing elit
              gravida in, vestibulum libero est pretium scelerisque
              praesent egestas at parturient, fames metus pulvinar
              dictum cursus feugiat tellus orci. Hac arcu tellus nec
              diam quam rutrum ut libero ullamcorper gravida congue,
              tempus fermentum sollicitudin venenatis odio luctus cum dis
              feugiat. Feugiat ridiculus natoque nisl suspendisse molestie
              posuere dui ac suscipit luctus, ullamcorper odio nec
              phasellus quisque vivamus sociis euismod tempor, blandit
              viverra turpis urna sagittis nisi aliquet duis tellus.
            </narrative>
          </description>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity)

        assert result is True

    def test_description_whitespace_is_(self):
        xml = '''
        <iati-activity>
          <activity-status code="2"/>
          <description>
            <narrative>
                                                                                a
            </narrative>
          </description>
        </iati-activity>
        '''

        activity = etree.fromstring(xml)
        test = self.feature.tests[1]
        result = test(activity)

        assert result is False
