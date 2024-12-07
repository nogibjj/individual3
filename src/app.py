from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global variables
result_duration = 45  # min
result_pace = [10, 0]  # min:sec


# Home route
@app.route("/")
def home():
    message = """Should there exist any problem, please contact the developer at: haobo.yuan@duke.edu"""
    return render_template("home.html", message=message)


# Input route with validation
@app.route("/input", methods=["GET", "POST"])
def input_data():
    if request.method == "POST":
        # Retrieve user inputs and perform validation
        try:
            data = {
                "gender": request.form.get("gender"),
                "age": int(request.form.get("age")),
                "height_ft": int(request.form.get("height_ft")),
                "height_in": int(request.form.get("height_in")),
                "weight_lbs": float(request.form.get("weight_lbs")),
                "target_weight_lbs": float(request.form.get("target_weight_lbs")),
                "duration_days": int(request.form.get("duration_days")),
                "weekly_frequency": int(request.form.get("weekly_frequency")),
            }

            # Validate inputs
            error_message = validate_data(data)
            if error_message:
                return render_template("input.html", error_message=error_message)

            # Logging the data
            save_data(data)
            return redirect(url_for("result"))

        except ValueError:
            # Handle any conversion errors
            return render_template(
                "input.html", error_message="Please enter valid numeric values."
            )

    return render_template("input.html")


# Result route
@app.route("/result")
def result():
    # Placeholder for results (replace with actual calculations later)
    result_data = {
        "duration": result_duration,  # Jogging duration per session in minutes
        "pace": f"{result_pace[0]}' {result_pace[1]}\" ",  # Suggested pace per mile (minutes:seconds)
    }
    # Logging the result
    save_data(result_data)
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
    app.run(host="0.0.0.0", port=8080, debug=True)
