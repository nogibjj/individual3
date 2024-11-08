from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('home.html', message="Welcome to the Jogging Weight Loss Guide!")

# Input route
@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        # Retrieve and validate user inputs
        data = {
            "gender": request.form.get("gender"),
            "age": int(request.form.get("age")),
            "height_ft": int(request.form.get("height_ft")),
            "height_in": int(request.form.get("height_in")),
            "weight_lbs": float(request.form.get("weight_lbs")),
            "target_weight_lbs": float(request.form.get("target_weight_lbs")),
            "duration_days": int(request.form.get("duration_days")),
            "weekly_frequency": int(request.form.get("weekly_frequency"))
        }
        # Save the input data
        save_data(data)
        return redirect(url_for('result'))
    return render_template('input.html')

# Result route
@app.route('/result')
def result():
    # Placeholder for results (replace with actual calculations later)
    result_data = {
        "session_duration": 45,   # Jogging duration per session in minutes
        "pace": "10:00"           # Suggested pace per mile (minutes:seconds)
    }
    return render_template('result.html', result=result_data)

# Save data function
def save_data(data):
    # Save data to a file or database as needed (simple file save here)
    with open('user_data.txt', 'a') as f:
        f.write(str(data) + '\n')

if __name__ == '__main__':
    app.run(debug=True)
