from flask import Flask, flash, request, render_template

import hackbright

app = Flask(__name__)
app.secret_key = 'random string'


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github", "jhacks")
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", 
                            first=first, 
                            last=last,
                            github=github,
                            projects=projects)


@app.route("/student_search")
def get_student_form():
    """Shows a form to search for a student."""

    return render_template("student_search.html")


@app.route("/add-student")
def add_student():
    """Shows a form to add a new student"""

    return render_template("new_student.html")


@app.route("/confirmed-student", methods=["POST"])
def student_added():
    """Adds student to database"""


    first = request.form.get("first")
    last = request.form.get("last")
    github = request.form.get("github")

    hackbright.make_new_student(first, last, github)

    flash("You have successfully added a new student!")

    return render_template("student_confirmed.html", 
                            first=first,
                            last=last, 
                            github=github)

@app.route("/project")
def display_project():
    """Displays information about a project"""

    title = request.args.get("title")
    
    # projects is a list with project_title, description, max_grade
    projects = hackbright.get_project_by_title(title)

    # student_grades is a list of tuples containing github account and 
    # grade associated with that account
    student_grades = hackbright.get_grades_by_title(title)
    print student_grades


    return render_template("project_info.html",
                            title=title, 
                            projects=projects,
                            student_grades=student_grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
