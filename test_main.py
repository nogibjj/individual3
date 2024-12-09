import unittest

from src.main import calculate_exercise_duration, total_calories_to_burn


class TestWeightLossFunctions(unittest.TestCase):
    def test_total_calories_to_burn(self):
        # Test case for calculating total calories to burn
        actual_weight = 60
        dream_weight = 50
        expected_calories = 77000  # (60 - 50) * 7700

        result = total_calories_to_burn(actual_weight, dream_weight)
        self.assertEqual(result, expected_calories)

    def test_no_weight_loss_needed(self):
        # Test case when no weight loss is needed
        actual_weight = 50
        dream_weight = 50
        result = total_calories_to_burn(actual_weight, dream_weight)
        self.assertEqual(result, "No need to lose weight!")

    def test_calculate_exercise_duration(self):
        # Test case for calculating exercise duration
        params = {
            "target_calories": 300,
            "height": 1.68,
            "age": 27,
            "exercise_intensity": 5,
            "gender": "Female",
            "actual_weight": 60,
        }
        duration, estimated_met = calculate_exercise_duration(params)

        self.assertGreater(duration, 0)
        self.assertGreater(estimated_met, 0)

    def test_invalid_estimated_met(self):
        # Test case for invalid estimated MET (should raise ValueError)
        params = {
            "target_calories": 500,
            "height": 1.68,
            "age": 27,
            "exercise_intensity": -1,  # Invalid intensity
            "gender": "Female",
            "actual_weight": 60,
        }

        with self.assertRaises(ValueError):
            calculate_exercise_duration(params)


if __name__ == "__main__":
    unittest.main()
