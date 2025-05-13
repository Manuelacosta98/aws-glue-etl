import unittest
from jobs.transform.transform_data import transform_function  # Adjust the import based on your actual function name

class TestTransformData(unittest.TestCase):

    def test_transform_function(self):
        input_data = [...]  # Replace with appropriate test input
        expected_output = [...]  # Replace with expected output
        result = transform_function(input_data)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()