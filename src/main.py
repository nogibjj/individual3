"""
This module trains a linear regression model to predict Estimated MET values
and provides functions to calculate total calories to burn and exercise duration.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load dataset
url = (
    "https://raw.githubusercontent.com/haobo-yuan/"
    "IDS706-FinalProject/refs/heads/main/exercise_dataset.csv"
)

exercise_df = pd.read_csv(url)

# Data preprocessing
exercise_df.drop(columns=["ID", "Exercise", "Weather Conditions"], inplace=True)
exercise_df["Height"] = np.sqrt(exercise_df["Actual Weight"] / exercise_df["BMI"])

exercise_df["Estimated MET"] = exercise_df.apply(
    lambda row: row["Calories Burn"] /
    (row["Actual Weight"] * row["Duration"] * 0.0175),
    axis=1,
)

exercise_df.dropna(inplace=True)
exercise_df = pd.get_dummies(exercise_df, columns=["Gender"], drop_first=True)

# Define features and target
X = exercise_df[
    ["Height", "Age", "Exercise Intensity", "Gender_Male", "Actual Weight"]
]
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
        float or str: The total calories to burn or a message if no weight loss is needed.
    """
    calories_per_kg = 7700
    weight_difference = actual_weight - dream_weight
    if weight_difference <= 0:
        return "No need to lose weight!"
    return weight_difference * calories_per_kg


def calculate_target_calories(actual_weight, dream_weight, num_of_weeks, week_frequency):
    """
    Calculate the target calories to burn per session based on weight loss goal.

    Args:
        actual_weight (float): The current weight in kilograms.
        dream_weight (float): The desired weight in kilograms.
        num_of_weeks (int): The number of weeks to achieve the goal.
        week_frequency (int): The number of exercise sessions per week.

    Returns:
        float or str: The target calories to burn per session,
                      or a message if no weight loss is needed.
    """
    total_calories = total_calories_to_burn(actual_weight, dream_weight)
    if isinstance(total_calories, str):
        return total_calories
    return total_calories / (num_of_weeks * week_frequency)


def calculate_exercise_duration(params):
    """
    Calculate the required exercise duration to burn target calories.

    Args:
        params (dict): A dictionary containing the following keys:
            - target_calories (float): The target calories to burn.
            - height (float): The height in meters.
            - age (int): The age in years.
            - exercise_intensity (int): The exercise intensity level (1-10).
            - gender (str): The gender ('Male' or 'Female').
            - actual_weight (float): The actual weight in kilograms.

    Returns:
        tuple: The required exercise duration in minutes and the estimated MET value.

    Raises:
        ValueError: If the estimated MET is invalid or exercise intensity is not valid.
    """
    # Validate exercise intensity
    if not (1 <= params["exercise_intensity"] <= 10):
        raise ValueError("Exercise intensity must be between 1 and 10.")

    gender_male = 1 if params["gender"].lower() == "male" else 0
    estimated_met = (
        intercept
        + coefficients[0] * params["height"]
        + coefficients[1] * params["age"]
        + coefficients[2] * params["exercise_intensity"]
        + coefficients[3] * gender_male
        + coefficients[4] * params["actual_weight"]
    )

    if estimated_met <= 0:
        raise ValueError(
            "Estimated MET value is invalid. Please check your input parameters."
        )

    calorie_burn_rate = estimated_met * params["actual_weight"] * 0.0175
    duration = params["target_calories"] / calorie_burn_rate

    return duration, estimated_met

