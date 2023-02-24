from sqlalchemy import text

from ceramics import model
from ceramics.repository import SQLAlchemyRepository


def insert_student(session):
    session.execute(text("insert into students (id, name) values (1, 'John')"))


def insert_course(session):
    session.execute(text("insert into courses (id, name, start_date, end_date, weekday, price_per_lesson) values (1, 'Ceramics', '2023-02-27', '2023-06-30', 3, 50)"))


def insert_enrollment(session, student_id, course_id):
    session.execute(
        text(
            f"insert into enrollments (student_id, course_id) values (:student_id, :course_id)"
        ),
        dict(student_id=student_id, course_id=course_id),
    )


def test_repository_can_save_student(session):
    student = model.Student("John")

    repository = SQLAlchemyRepository(session, model.Student)
    repository.add(student)
    session.commit()

    rows = list(session.execute(text("select name from students")))
    assert rows == [("John",)]


def test_repository_can_retrieve_a_course_with_students(session):
    insert_student(session)
    insert_course(session)
    insert_enrollment(session, 1, 1)
    session.commit()

    repository = SQLAlchemyRepository(session, model.Course)
    course = repository.get(1)

    student = model.Student("John")
    assert student in course.enrollments
