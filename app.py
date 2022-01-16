from flask import Flask, render_template, url_for, request
import json

GRADES = ["F","E","D","C","B","A"]
STATIONS = ["SitUp","Jump","SitReach","PullUp","Shuttle","Run24"]
f = open("static/Standard.json")
standards = json.load(f)
f.close()

def get_grade(station, gender, age, score):
    for standard in standards:
        # Find standard 
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
    gender = request.args.get("gender")
    print(gender)
    age = int(request.args.get("age"))

    # Get raw scores to be displayed
    scores = []
    for station in STATIONS[:-1]: # All but 2.4km run since it is in 2 parts
        scores.append(request.args.get(station))
    scores.append("{}:{:02d}".format(request.args.get("Run24_min"),int(request.args.get("Run24_s"))))

    # Calc grades
    grades = []
    for i in range(6):
        grades.append(get_grade(STATIONS[i],gender,age,float(scores[i].replace(":","."))))

    return render_template("display.html",gender=gender,age=age,score=scores,grade=grades)


if __name__ == "__main__":
    app.run(debug=True)