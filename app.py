from flask import Flask, render_template, url_for, request
import json

GRADES = ["F","E","D","C","B","A"]
STATIONS = ["SitUp","Jump","SitReach","PullUp","Shuttle","Run24"]
STATIONS_DISPLAY = ["Sit Up","Standing Board Jump","Sit and Reach","(Inclined) Pull Up","Shuttle Run","2.4km Run"]
f = open("static/Standard.json")
STANDARDS = json.load(f)
f.close()

def get_grade_next_score(station, gender, age, score):
    for standard in STANDARDS:
        # Find standard 
        if standard["Age"] == age and standard["Item"] == station and standard["Gender"] == gender:
            if station in ["SitUp","Jump","SitReach","PullUp"]: # Based on number, higher better
                for grade in GRADES:
                    if grade == "A":
                        next_score = "-"
                        break
                    elif score <= int(standard[grade]): # Grade found, find score to next grade
                        next_score = str(int(standard[grade]) + 1)
                        break
            elif station == "Shuttle": # Based on timing, lower better
                for grade in GRADES:
                    if grade == "A":
                        next_score = "-"
                        break
                    elif score >= float(standard[grade]):
                        next_score = "{:.1f}".format(float(standard[grade]) - 0.1)
                        break
            else: # 2.4km run, based on timing, lower better
                for grade in GRADES:
                    if grade == "A":
                        next_score = "-"
                        break
                    elif score >= float(standard[grade].replace(":",".")): # Grade found, find score to next grade
                        next_score = ("{:.02f}".format(float(standard[grade].replace(":",".")) - 0.01)).replace(".",":")
                        break
    return grade, next_score

def get_award(points):
    # Bronze Award Requirements: At least an E grade performance in all 6 test items and a total of 6 or more points.
    # Silver Award Requirements: At least a D grade performance in all 6 test items and a total of 15 or more points.
    # Gold Award Requirements: At least a C grade performance in all 6 test items and a total of 21 or more points.
    if sum(points) >= 21 and all(point >= 3 for point in points):
        return "Gold"
    elif sum(points) >= 15 and all(point >= 2 for point in points):
        return "Silver"
    elif sum(points) >= 6 and all(point >= 1 for point in points):
        return "Bronze"
    else:
        return "None"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/display/")
def display():
    gender = request.args.get("gender")
    age = int(request.args.get("age"))

    # Get raw scores to be displayed
    scores = []
    for station in STATIONS[:-1]: # All but 2.4km run since it is in 2 parts
        scores.append(request.args.get(station))
    scores.append("{}:{:02d}".format(request.args.get("Run24_min"),int(request.args.get("Run24_s"))))

    # Calc grades and score to next grade
    grades = []
    next_scores = []
    for i in range(6):
        grade, next_score = get_grade_next_score(STATIONS[i],gender,age,float(scores[i].replace(":",".")))
        grades.append(grade)
        next_scores.append(next_score)

    # Calc points
    points = []
    for grade in grades:
        points.append(GRADES.index(grade))

    return render_template("display.html",stations=STATIONS_DISPLAY,gender=gender,age=age,scores=scores,grades=grades,\
        next_scores=next_scores,points=points,total_points=sum(points),award=get_award(points))


if __name__ == "__main__":
    app.run(debug=True)