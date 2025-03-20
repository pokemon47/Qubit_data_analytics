import unittest
from app import app  # Import the Flask app from app.py

class TestFlaskAPI(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
    
    def test_server_is_active(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        print(f"-{self._testMethodName} passed")

    def test_predict_positive_titles(self):
        data = {
            "titles": [
                "Tesla stocks surged after good earnings report",
                "Tesla announces new product lineup for 2025",
                "Tesla expands into new markets in Asia"
            ]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json
        self.assertEqual(result["total"], 3)
        self.assertGreater(result["total_positive"], result["total_negative"], "positive sentiments must be greater than negative sentiments")
        
        print(f"-{self._testMethodName} passed")

    def test_predict_mixed_titles(self):
        """
        Test that the API correctly processes a list of mixed titles.
        """
        data = {
            "titles": [
                "Tesla losing market share",
                "Tesla faces declining sales in Europe",
                "Tesla expands to new markets in Asia"
            ]
        }
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json
        self.assertGreater(result["total_negative"], result["total_positive"], "negative sentiments must be greater than positive sentiments")
        
        print(f"-{self._testMethodName} passed")

    def test_empty_titles(self):
        """
        Test that the API correctly handles an empty list of titles.
        """
        data = {"titles": []}
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["total_positive"], 0)
        self.assertEqual(result["total_negative"], 0)
        
        print(f"-{self._testMethodName} passed")

    def test_invalid_input(self):
        """
        Test that the API returns an error if titles are not provided as a list.
        """
        data = {"titles": "Tesla stocks surged after good earnings report"}
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)
        
        result = response.json
        self.assertEqual(result["error"], "'titles' must be a list of strings")
        
        print(f"-{self._testMethodName} passed")


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=0).run(unittest.TestLoader().loadTestsFromTestCase(TestFlaskAPI))
