"""
This module trains a linear regression model to predict Estimated MET values
and provides functions to calculate total calories to burn and exercise duration.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load dataset
URL = (
    "https://raw.githubusercontent.com/haobo-yuan/"
    "IDS706-FinalProject/refs/heads/main/exercise_dataset.csv"
)

exercise_df = pd.read_csv(URL)

# Data preprocessing
exercise_df.drop(columns=["ID", "Exercise", "Weather Conditions"], inplace=True)
exercise_df["Height"] = np.sqrt(exercise_df["Actual Weight"] / exercise_df["BMI"])

exercise_df["Estimated MET"] = exercise_df.apply(
    lambda row: row["Calories Burn"]
    / (row["Actual Weight"] * row["Duration"] * 0.0175),
    axis=1,
)

exercise_df.dropna(inplace=True)
exercise_df = pd.get_dummies(exercise_df, columns=["Gender"], drop_first=True)

# Define features and target
X = exercise_df[["Height", "Age", "Exercise Intensity", "Gender_Male", "Actual Weight"]]
y = exercise_df["Estimated MET"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Output model coefficients and intercept
coefficients = model.coef_
intercept = model.intercept_

print("Intercept:", intercept)
for feature, coef in zip(X.columns, coefficients):
    print(f"Coefficient for {feature}: {coef}")

# Generate linear regression formula
lr_formula = f"Estimated MET = {intercept:.4f}"
for feature, coef in zip(X.columns, coefficients):
    lr_formula += f" + ({coef:.4f} * {feature})"

print("\nLinear Regression Formula:")
print(lr_formula)


def total_calories_to_burn(actual_weight, dream_weight):
    """
    Calculate the total calories needed to reach the dream weight.

    Args:
        actual_weight (float): The current weight in kilograms.
        dream_weight (float): The desired weight in kilograms.

    Returns:
        float or str: The total calories to burn
        or a message if no weight loss is needed.
    """
    calories_per_kg = 7700
    weight_difference = actual_weight - dream_weight
    if weight_difference <= 0:
        return "No need to lose weight!"
    return weight_difference * calories_per_kg


def calculate_target_calories_and_duration(params):
    """
    Calculate the target calories to burn per session
    and the required exercise duration.

    Args:
        params (dict):
            - actual_weight: current weight in kg
            - dream_weight: desired weight in kg
            - num_of_weeks: number of weeks to achieve the goal
            - week_frequency: number of exercise sessions per week
            - height: The height in meters
            - age: The age in years
            - exercise_intensity: 1-10
            - gender:'Male' or 'Female'

    Returns:
        tuple: The target calories to burn per session,
               the required exercise duration in minutes,
               and the estimated MET value
        or str: A message if no weight loss is needed
    """
    assert (
        isinstance(params["actual_weight"], (int, float))
        and params["actual_weight"] > 0
    ), "Actual weight must be a positive number."
    assert (
        isinstance(params["dream_weight"], (int, float)) and params["dream_weight"] > 0
    ), "Dream weight must be a positive number."
    assert (
        isinstance(params["num_of_weeks"], int) and params["num_of_weeks"] > 0
    ), "Number of weeks must be a positive integer."
    assert (
        isinstance(params["week_frequency"], int) and params["week_frequency"] > 0
    ), "Week frequency must be a positive integer."
    assert (
        isinstance(params["height"], (int, float)) and params["height"] > 0
    ), "Height must be a positive number."
    assert (
        isinstance(params["age"], int) and 10 <= params["age"] <= 100
    ), "Age must be an integer between 10 and 100."
    assert (
        isinstance(params["exercise_intensity"], int)
        and 1 <= params["exercise_intensity"] <= 10
    ), "Exercise intensity must be an integer between 1 and 10."
    assert params["gender"].lower() in {
        "male",
        "female",
    }, "Gender must be 'Male' or 'Female'."

    # Extract inputs from the dictionary
    actual_weight = params["actual_weight"]
    dream_weight = params["dream_weight"]
    num_of_weeks = params["num_of_weeks"]
    week_frequency = params["week_frequency"]
    height = params["height"]
    age = params["age"]
    exercise_intensity = params["exercise_intensity"]
    gender = params["gender"]

    # Calculate target calories to burn per session
    total_calories = total_calories_to_burn(actual_weight, dream_weight)
    if isinstance(total_calories, str):
        return total_calories  # Return message if no weight loss is needed

    target_calories = total_calories / (num_of_weeks * week_frequency)

    # Validate exercise intensity
    if not 1 <= exercise_intensity <= 10:
        raise ValueError("Exercise intensity must be between 1 and 10.")

    # Calculate estimated MET
    gender_male = 1 if gender.lower() == "male" else 0
    estimated_met = (
        intercept
        + coefficients[0] * height
        + coefficients[1] * age
        + coefficients[2] * exercise_intensity
        + coefficients[3] * gender_male
        + coefficients[4] * actual_weight
    )

    if estimated_met <= 0:
        raise ValueError(
            "Estimated MET value is invalid. Please check your input parameters."
        )

    # Calculate exercise duration
    calorie_burn_rate = estimated_met * actual_weight * 0.0175
    duration = target_calories / calorie_burn_rate

    return target_calories, duration, estimated_met
