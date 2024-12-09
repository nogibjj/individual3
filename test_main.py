import unittest

from src.main import calculate_target_calories_and_duration, total_calories_to_burn


class TestMainModule(unittest.TestCase):
    def setUp(self):
        """Set up valid parameters and constants for testing."""
        self.valid_params = {
            "actual_weight": 80,
            "dream_weight": 60,
            "num_of_weeks": 4,
            "week_frequency": 3,
            "height": 1.75,
            "age": 30,
            "exercise_intensity": 6,
            "gender": "Male",
        }

    def test_total_calories_to_burn(self):
        """Test total calories to burn function."""
        # Case: valid weight loss
        result = total_calories_to_burn(80, 60)
        self.assertEqual(result, 154000)  # 20 kg * 7700 cal/kg

        # Case: no weight loss needed
        result = total_calories_to_burn(60, 60)
        self.assertEqual(result, "No need to lose weight!")

        # Case: invalid (negative weight difference)
        result = total_calories_to_burn(60, 70)
        self.assertEqual(result, "No need to lose weight!")

    def test_calculate_target_calories_and_duration_valid(self):
        """Test calculate_target_calories_and_duration with valid inputs."""
        result = calculate_target_calories_and_duration(self.valid_params)
        target_calories, duration, estimated_met = result
        self.assertGreater(target_calories, 0)
        self.assertGreater(duration, 0)
        self.assertGreater(estimated_met, 0)

    def test_calculate_target_calories_and_duration_no_weight_loss(self):
        """Test case when no weight loss is needed."""
        params = self.valid_params.copy()
        params["dream_weight"] = params["actual_weight"]
        result = calculate_target_calories_and_duration(params)
        self.assertEqual(result, "No need to lose weight!")

    def test_invalid_actual_weight(self):
        """Test with invalid actual weight."""
        params = self.valid_params.copy()
        params["actual_weight"] = -10  # Invalid weight
        with self.assertRaises(AssertionError):
            calculate_target_calories_and_duration(params)

    def test_invalid_dream_weight(self):
        """Test with invalid dream weight."""
        params = self.valid_params.copy()
        params["dream_weight"] = 0  # Invalid weight
        with self.assertRaises(AssertionError):
            calculate_target_calories_and_duration(params)

    def test_invalid_age(self):
        """Test with invalid age."""
        params = self.valid_params.copy()
        params["age"] = 150  # Out of range
        with self.assertRaises(AssertionError):
            calculate_target_calories_and_duration(params)

    def test_invalid_exercise_intensity(self):
        """Test with invalid exercise intensity."""
        params = self.valid_params.copy()
        params["exercise_intensity"] = 15  # Out of range
        with self.assertRaises(AssertionError):
            calculate_target_calories_and_duration(params)

    def test_invalid_gender(self):
        """Test with invalid gender."""
        params = self.valid_params.copy()
        params["gender"] = "Unknown"  # Invalid gender
        with self.assertRaises(AssertionError):
            calculate_target_calories_and_duration(params)


if __name__ == "__main__":
    unittest.main()
