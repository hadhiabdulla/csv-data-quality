import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from profile_csv import profile, render


FIXTURE = (
    'name,age,city\n'
    'anu,23,kochi\n'
    'rahul,,kochi\n'
    'meera,31,delhi\n'
    'anu,23,kochi\n'
    'ragged,44\n'
)


def write_tmp(text):
    fd, path = tempfile.mkstemp(suffix='.csv')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(text)
    return path


class ProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = write_tmp(FIXTURE)
        cls.p = profile(cls.path)

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.path)

    def test_shape(self):
        self.assertEqual(self.p['rows'], 5)
        self.assertEqual(self.p['columns'], 3)

    def test_duplicates_and_ragged(self):
        self.assertEqual(self.p['duplicate_rows'], 1)
        self.assertEqual(self.p['ragged_rows'], 1)

    def test_missing_and_distinct(self):
        age = next(c for c in self.p['columns_detail'] if c['name'] == 'age')
        self.assertEqual(age['missing'], 1)
        self.assertEqual(age['type'], 'numeric')
        self.assertEqual(age['distinct'], 3)

    def test_numeric_stats(self):
        age = next(c for c in self.p['columns_detail'] if c['name'] == 'age')
        self.assertEqual(age['min'], 23.0)
        self.assertEqual(age['max'], 44.0)
        self.assertEqual(age['mean'], 30.25)
        self.assertEqual(age['median'], 27.0)

    def test_text_top_values(self):
        city = next(c for c in self.p['columns_detail'] if c['name'] == 'city')
        self.assertEqual(city['type'], 'text')
        self.assertEqual(city['top'][0], ('kochi', 3))

    def test_render_contains_summary(self):
        out = render(self.p)
        self.assertIn('Rows: 5', out)
        self.assertIn('Duplicate rows: 1', out)
        self.assertIn('age [numeric]', out)

    def test_empty_file_exits(self):
        path = write_tmp('')
        with self.assertRaises(SystemExit):
            profile(path)
        os.unlink(path)


if __name__ == '__main__':
    unittest.main()
