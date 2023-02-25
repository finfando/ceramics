from datetime import datetime

from flask import Flask, redirect, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ceramics import config, model, orm, repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/students/new", methods=["GET", "POST"])
def new_student():
    if request.method == "GET":
        return render_template("new_student.html")
    elif request.method == "POST":
        session = get_session()
        repo = repository.SQLAlchemyRepository(session, model.Student)
        repo.add(model.Student(name=request.form["name"]))
        session.commit()
        return redirect("/students")


@app.route("/students", methods=["GET"])
def students():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session, model.Student)
    students = repo.list()
    return render_template("students.html", students=students)


@app.route("/courses/new", methods=["GET", "POST"])
def new_course():
    if request.method == "GET":
        return render_template("new_course.html")
    elif request.method == "POST":
        session = get_session()
        repo = repository.SQLAlchemyRepository(session, model.Course)
        repo.add(
            model.Course(
                name=request.form["name"],
                start_date=datetime.strptime(request.form["start_date"], "%Y-%m-%d"),
                end_date=datetime.strptime(request.form["end_date"], "%Y-%m-%d"),
                weekday=int(request.form["weekday"]),
                price_per_lesson=int(request.form["price_per_lesson"]),
            )
        )
        session.commit()
        return redirect("/courses")


@app.route("/courses", methods=["GET"])
def courses():
    session = get_session()
    repo = repository.SQLAlchemyRepository(session, model.Course)
    courses = repo.list()
    return render_template("courses.html", courses=courses)


@app.route("/courses/<int:id>", methods=["GET"])
def course(id):
    session = get_session()
    repo = repository.SQLAlchemyRepository(session, model.Course)
    course = repo.get(id)
    return render_template("course.html", course=course)


@app.route("/courses/<int:id>/enroll", methods=["GET", "POST"])
def course_enroll(id):
    if request.method == "GET":
        session = get_session()
        repo_course = repository.SQLAlchemyRepository(session, model.Course)
        course = repo_course.get(id)
        repo_student = repository.SQLAlchemyRepository(session, model.Student)
        students = set(repo_student.list()) - course.enrollments
        return render_template("enroll.html", course=course, students=students)
    elif request.method == "POST":
        session = get_session()
        repo_course = repository.SQLAlchemyRepository(session, model.Course)
        course = repo_course.get(id)
        repo_student = repository.SQLAlchemyRepository(session, model.Student)
        student = repo_student.get(request.form["students"])
        course.enroll(student)
        session.commit()
        return redirect(f"/courses/{id}")


@app.route("/courses/<int:course_id>/disenroll/<int:student_id>", methods=["GET"])
def course_disenroll(course_id, student_id):
    if request.method == "GET":
        session = get_session()
        repo_course = repository.SQLAlchemyRepository(session, model.Course)
        course = repo_course.get(course_id)
        repo_student = repository.SQLAlchemyRepository(session, model.Student)
        student = repo_student.get(student_id)
        course.disenroll(student)
        session.commit()
        return redirect(f"/courses/{course_id}")


@app.route("/courses/<int:id>/attendance/<date>", methods=["GET", "POST"])
def attendance(id, date):
    if request.method == "GET":
        session = get_session()
        repo = repository.SQLAlchemyRepository(session, model.Course)
        course = repo.get(id)

        date = datetime.strptime(date, "%Y-%m-%d").date() # TODO: use custom flask converter
        lesson = course.get_lesson_by_date(date)
        # remaining_enrolled_students = course.enrollments - {a.student for a in lesson.attendance}
        attendance = [model.Attendance(s, course, None) for s in course.enrollments]
        return render_template("lesson.html", course=course, lesson=lesson, attendance=attendance)


if __name__ == "__main__":
    app.run(debug=True)
