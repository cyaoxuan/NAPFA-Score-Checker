from flask import Flask, render_template, url_for, request
import json

GRADES = ["F","E","D","C","B","A"]
f = open("static/Standard.json")
standards = json.load(f)
f.close()

def get_grade(station, gender, age, score):
    for standard in standards:
        if standard["Age"] == age and standard["Item"] == station and standard["Gender"] == gender:
            if station not in ["Shuttle","Run24"]: # Based on number, higher better
                for grade in GRADES:
                    if grade == "A" or score <= int(standard[grade]): # Grade found
                        break
            else: # Based on timing, lower better
                for grade in GRADES:
                    if grade == "A" or score >= float(standard[grade].replace(":",".")): # Grade found
                        break
    return grade

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/display/")
def display():
    gender, age = request.form.get("gender"), request.form.get("age")
    results = [request.form.get("situp"),request.form.get("jump"),request.form.get("sitreach"),request.form.get("pullup"),request.form.get("shuttle"),request.form.get("run24")]
    
    return render_template("display.html")


if __name__ == "__main__":
    app.run(debug=True)