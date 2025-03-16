import unittest
import requests

class TestFlaskAPI(unittest.TestCase):
    
    # Assuming your Flask API is running locally on port 5000
    api_url = "http://127.0.0.1:5000/predict"

    def test_predict_positive_titles(self):
        """
        Test that the API correctly processes a list of positive titles.
        """
        data = {
            "titles": [
                "Tesla stocks surged after good earnings report",
                "Tesla announces new product lineup for 2025",
                "Tesla expands into new markets in Asia"
            ]
        }
        response = requests.post(self.api_url, json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertEqual(result["total"], 3)
        self.assertGreater(result["total_positive"], result["total_negative"], "positive sentiments must be greater than negative sentiments")
        
        # print("test_predict_positive_titles passed")
        print(f"-{self._testMethodName} passed")

    def test_predict_mixed_titles(self):
        """
        Test that the API correctly processes a list of negative titles.
        """
        data = {
            "titles": [
                "Tesla losing market share",
                "Tesla faces declining sales in Europe",
                "Tesla expands into new markets in Asia"
            ]
        }
        response = requests.post(self.api_url, json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertEqual(result["total"], 3)
        self.assertGreater(result["total_negative"], result["total_positive"], "negative sentiments must be greater than positive sentiments")
        
        # print("test_predict_mixed_titles passed")
        print(f"-{self._testMethodName} passed")

    def test_empty_titles(self):
        """
        Test that the API correctly handles an empty list of titles.
        """
        data = {"titles": []}
        response = requests.post(self.api_url, json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["total_positive"], 0)
        self.assertEqual(result["total_negative"], 0)
        
        # print("test_empty_titles passed")
        print(f"-{self._testMethodName} passed")

    def test_invalid_input(self):
        """
        Test that the API returns an error if titles are not provided as a list.
        """
        data = {"titles": "Tesla stocks surged after good earnings report"}
        response = requests.post(self.api_url, json=data)
        self.assertEqual(response.status_code, 400)
        
        result = response.json()
        self.assertEqual(result["error"], "'titles' must be a list of strings")
        
        # print("test_invalid_input passed")
        print(f"-{self._testMethodName} passed")


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=0).run(unittest.TestLoader().loadTestsFromTestCase(TestFlaskAPI))
