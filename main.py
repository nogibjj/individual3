import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
exercise_df = pd.read_csv(
    "https://raw.githubusercontent.com/haobo-yuan/IDS706-FinalProject/main/exercise_dataset.csv"
)

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


# Function to calculate total calories to burn
def total_calories_to_burn(actual_weight, dream_weight):
    calories_per_kg = 7700
    weight_difference = actual_weight - dream_weight
    if weight_difference <= 0:
        return "No need to lose weight!"
    return weight_difference * calories_per_kg


# Function to calculate exercise duration
def calculate_exercise_duration(
    target_calories, height, age, exercise_intensity, gender, actual_weight
):
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

    calorie_burn_rate = estimated_met * actual_weight * 0.0175
    duration = target_calories / calorie_burn_rate

    return duration, estimated_met
