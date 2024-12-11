#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, request, url_for, session
from main import calculate_target_calories_and_duration


app = Flask(__name__)
app.secret_key = "haobo.yuan@duke.edu"

# Global variables
result_duration = 45  # min
result_pace = [10, 0]  # min:sec


# Home route
@app.route("/")
def home():
    message = (
        "Should there exist any problem, please contact the developer at: "
        "haobo.yuan@duke.edu"
    )
    return render_template("home.html", message=message)


@app.route("/health")
def health_check():
    return "OK"

# Input route
@app.route("/input", methods=["GET", "POST"])
def input_data():
    if request.method == "POST":
        try:
            height_meters = float(request.form.get("height_ft")) * 0.3048 + \
                float(request.form.get("height_in")) * 0.0254
            params = {
                "gender": request.form.get("gender"),
                "age": int(request.form.get("age")),
                "height": height_meters,
                "actual_weight": float(request.form.get("weight_lbs")) * 0.453592,
                "dream_weight": float(request.form.get("target_weight_lbs")) * 0.453592,
                "num_of_weeks": int(request.form.get("num_of_weeks")),
                "week_frequency": int(request.form.get("weekly_frequency")),
                "exercise_intensity": int(request.form.get("exercise_intensity")),
            }
            result = calculate_target_calories_and_duration(params)
            if isinstance(result, str):
                return render_template("input.html", error_message=result)
            session["result"] = {
                "target_calories": round(result[0]),
                "duration": round(result[1]),
                "estimated_met": round(result[2], 1)  # keep one decimal
            }
            return redirect(url_for("result"))
        except Exception as e:
            return render_template("input.html", error_message=e)
    return render_template("input.html")


# Result route
@app.route("/result")
def result():
    result_data = session.get("result", None)
    if not result_data:
        print("Result data is missing.")
        return redirect(url_for("input_data"))

    return render_template("result.html", result=result_data)


# Save data function
def save_data(data):
    # Save data to a file or database as needed (simple file save here)
    with open("logging/user_data.txt", "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")


# Data validation function
def validate_data(data):
    if data["age"] <= 0 or data["age"] > 100:
        return "Age must be between 10 and 100."
    if data["height_ft"] <= 0 or data["height_ft"] > 8:
        return "Height in feet must be between 1 and 8."
    if data["height_in"] < 0 or data["height_in"] >= 12:
        return "Height in inches must be between 0 and 11."
    if data["weight_lbs"] <= 0 or data["weight_lbs"] > 500:
        return "Current weight must be between 50 and 500 lbs."
    if data["target_weight_lbs"] <= 0 or data["target_weight_lbs"] > 500:
        return "Target weight must be between 50 and 500 lbs."
    if data["duration_days"] <= 0 or data["duration_days"] > 365:
        return "Duration must be between 7 and 365 days."
    if data["weekly_frequency"] <= 0 or data["weekly_frequency"] > 7:
        return "Workout frequency must be between 1 and 7 days per week."
    if data["weight_lbs"] <= data["target_weight_lbs"]:
        return "Target weight must be less than current weight for weight loss."
    return None


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080, debug=True)
    app.run(host="0.0.0.0", port=8080)
