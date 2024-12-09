import unittest
from src.main import (
    total_calories_to_burn,
    calculate_target_calories,
    calculate_exercise_duration,
)


class TestWeightLossFunctions(unittest.TestCase):
    def test_total_calories_to_burn(self):
        """Test total_calories_to_burn with a valid weight loss goal."""
        actual_weight = 70
        dream_weight = 65
        expected_calories = 38500  # (70 - 65) * 7700
        self.assertEqual(total_calories_to_burn(actual_weight, dream_weight), expected_calories)

    def test_total_calories_to_burn_no_weight_loss_needed(self):
        """Test total_calories_to_burn when no weight loss is needed."""
        actual_weight = 65
        dream_weight = 65
        self.assertEqual(total_calories_to_burn(actual_weight, dream_weight), "No need to lose weight!")

    def test_calculate_target_calories(self):
        """Test calculate_target_calories with valid inputs."""
        actual_weight = 70
        dream_weight = 65
        num_of_weeks = 4
        week_frequency = 3
        expected_target_calories = 38500 / (4 * 3)  # 38500 / (4 * 3)
        result = calculate_target_calories(actual_weight, dream_weight, num_of_weeks, week_frequency)
        self.assertAlmostEqual(result, expected_target_calories, places=2)

    def test_calculate_target_calories_no_weight_loss_needed(self):
        """Test calculate_target_calories when no weight loss is needed."""
        actual_weight = 65
        dream_weight = 65
        num_of_weeks = 4
        week_frequency = 3
        self.assertEqual(
            calculate_target_calories(actual_weight, dream_weight, num_of_weeks, week_frequency),
            "No need to lose weight!"
        )

    def test_calculate_exercise_duration(self):
        """Test calculate_exercise_duration with valid parameters."""
        actual_weight = 70
        dream_weight = 65
        num_of_weeks = 4
        week_frequency = 3

        # Dynamically calculate target calories
        target_calories = calculate_target_calories(actual_weight, dream_weight, num_of_weeks, week_frequency)

        params = {
            "height": 1.75,
            "age": 27,
            "exercise_intensity": 6,
            "gender": "Male",
            "actual_weight": actual_weight
        }

        # Add the calculated target_calories to params
        params["target_calories"] = target_calories

        duration, estimated_met = calculate_exercise_duration(params)
        self.assertGreater(duration, 0)
        self.assertGreater(estimated_met, 0)

    def test_calculate_exercise_duration_invalid_intensity(self):
        """Test calculate_exercise_duration with invalid exercise intensity."""
        actual_weight = 70
        dream_weight = 65
        num_of_weeks = 4
        week_frequency = 3

        # Dynamically calculate target calories
        target_calories = calculate_target_calories(actual_weight, dream_weight, num_of_weeks, week_frequency)

        params = {
            "target_calories": target_calories,
            "height": 1.75,
            "age": 27,
            "exercise_intensity": 11,  # Invalid intensity
            "gender": "Male",
            "actual_weight": actual_weight
        }

        with self.assertRaises(ValueError):
            calculate_exercise_duration(params)

    def test_calculate_exercise_duration_invalid_estimated_met(self):
        """Test calculate_exercise_duration with an invalid Estimated MET."""
        actual_weight = 70
        dream_weight = 65
        num_of_weeks = 4
        week_frequency = 3

        # Dynamically calculate target calories
        target_calories = calculate_target_calories(actual_weight, dream_weight, num_of_weeks, week_frequency)

        params = {
            "target_calories": target_calories,
            "height": 1.75,
            "age": 27,
            "exercise_intensity": 1,
            "gender": "Male",
            "actual_weight": actual_weight
        }

        # Force the Estimated MET to be a negative value to trigger an exception
        with self.assertRaises(ValueError):
            calculate_exercise_duration(params)


if __name__ == "__main__":
    unittest.main()
