import unittest
from jobs.extract.extract_data_job import extract_data

class TestExtractData(unittest.TestCase):

    def test_extract_data(self):
        # Add your test cases here
        result = extract_data()
        self.assertIsNotNone(result)
        # Add more assertions based on expected output

if __name__ == '__main__':
    unittest.main()