from main import total_calories_to_burn, calculate_exercise_duration

# Example input
height = 1.68  # Height in meters
actual_weight = 60
dream_weight = 50
age = 27  # Age in years
exercise_intensity = 5  # Exercise intensity level (1-10)
gender = "Female"  # Gender ('Male' or 'Female')
total_time = 12  # Weeks
frequency_per_week = 5  # Exercise 3 times per week

# Step 1: Calculate total calories to burn
total_calories = total_calories_to_burn(actual_weight, dream_weight)

# Check if weight loss is needed
if isinstance(total_calories, str):
    print(total_calories)
else:
    print(f"Total calories to burn: {total_calories:.2f} kcal")

    # Step 2: Calculate target calories per session
    target_calories = total_calories / (total_time * frequency_per_week)
    print(f"Target calories per session: {target_calories:.2f} kcal")

    # Step 3: Calculate exercise duration per session
    try:
        duration, estimated_met = calculate_exercise_duration(
            target_calories, height, age, exercise_intensity, gender, actual_weight
        )
        print(f"Estimated MET: {estimated_met:.2f}")
        print(
            f"You need to exercise for approximately {duration:.2f} minutes per session to burn {target_calories:.2f} kcal."
        )
    except ValueError as e:
        print(e)
