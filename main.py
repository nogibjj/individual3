import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


exercise_df = pd.read_csv(
    "https://raw.githubusercontent.com/haobo-yuan/IDS706-FinalProject/refs/heads/main/exercise_dataset.csv?token=GHSAT0AAAAAACWVU3DE4LYU3NJ7QJFMAHNGZ2U3LYQ"
)


exercise_df.drop(columns=["ID", "Exercise", "Weather Conditions"], inplace=True)
# Data manipulation: calculate height from bmi and weight:
exercise_df["Height"] = np.sqrt(exercise_df["Actual Weight"] / exercise_df["BMI"])

exercise_df["Estimated MET"] = exercise_df.apply(
    lambda row: row["Calories Burn"]
    / (row["Actual Weight"] * row["Duration"] * 0.0175),
    axis=1,
)


exercise_df.dropna(inplace=True)


exercise_df = pd.get_dummies(exercise_df, columns=["Gender"], drop_first=True)
print(exercise_df.columns)
X = exercise_df[["Height", "Age", "Exercise Intensity", "Gender_Male", "Actual Weight"]]
y = exercise_df["Estimated MET"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

coefficients = model.coef_
intercept = model.intercept_

print("Intercept:", intercept)
for feature, coef in zip(X.columns, coefficients):
    print(f"Coefficient for {feature}: {coef}")

lr_formula = f"Estimated MET = {intercept:.4f}"
for feature, coef in zip(X.columns, coefficients):
    lr_formula += f" + ({coef:.4f} * {feature})"

print("\nLinear Regression Formula:")
print(lr_formula)


def total_calories_to_burn(actual_weight, dream_weight):
    # 1 kilogram of fat = 7700 calories
    calories_per_kg = 7700
    weight_difference = actual_weight - dream_weight
    if weight_difference <= 0:
        return "No need to lose weight!"
    total_calories = weight_difference * calories_per_kg
    return total_calories


def calculate_exercise_duration(
    target_calories, height, age, exercise_intensity, gender, actual_weight
):
    # Coefficients from the linear regression formula
    intercept = 13.7795
    coef_height = -0.0490
    coef_age = -0.0001
    coef_intensity = -0.0230
    coef_gender = 0.0021
    coef_weight = -0.0938

    # Gender_Male: 1 represents Male, 0 represents Female
    gender_male = 1 if gender.lower() == "male" else 0

    # Calculate the Estimated MET
    estimated_met = (
        intercept
        + coef_height * height
        + coef_age * age
        + coef_intensity * exercise_intensity
        + coef_gender * gender_male
        + coef_weight * actual_weight
    )

    # Ensure the estimated MET is positive
    if estimated_met <= 0:
        raise ValueError(
            "Estimated MET value is invalid. Please check your input parameters."
        )

    # Calculate calorie burn rate (kcal/min)
    calorie_burn_rate = estimated_met * actual_weight * 0.0175

    # Calculate the required exercise duration (minutes)
    duration = target_calories / calorie_burn_rate

    return duration, estimated_met
