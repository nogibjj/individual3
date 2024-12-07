import unittest
from main import total_calories_to_burn, calculate_exercise_duration


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
        height = 1.68
        actual_weight = 60
        age = 27
        exercise_intensity = 5
        gender = "Female"
        total_calories = 77000
        total_time = 12  # Weeks
        frequency_per_week = 5  # Exercise sessions per week

        target_calories = total_calories / (total_time * frequency_per_week)

        duration, estimated_met = calculate_exercise_duration(
            target_calories, height, age, exercise_intensity, gender, actual_weight
        )

        # Expected values (these may vary slightly depending on your linear model)
        self.assertGreater(duration, 0)
        self.assertGreater(estimated_met, 0)

        print(f"Total calories to burn: {total_calories:.2f} kcal")
        print(f"Target calories per session: {target_calories:.2f} kcal")
        print(f"Estimated MET: {estimated_met:.2f}")
        print(f"Exercise duration per session: {duration:.2f} minutes")

    def test_invalid_estimated_met(self):
        # Test case for invalid estimated MET (should raise ValueError)
        height = 1.68
        actual_weight = 60
        age = 27
        exercise_intensity = -1  # Invalid intensity
        gender = "Female"
        target_calories = 500

        with self.assertRaises(ValueError):
            calculate_exercise_duration(
                target_calories, height, age, exercise_intensity, gender, actual_weight
            )


if __name__ == "__main__":
    unittest.main()
