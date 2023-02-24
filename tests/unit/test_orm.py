from sqlalchemy import text

from ceramics import model


def test_student_mapper_can_read_students(session):
    session.execute(text("insert into students (name) VALUES ('John')"))
    john = session.query(model.Student).one()
    assert john.name == "John"


def test_student_mapper_can_save_students(session):
    new_student = model.Student(name="John")
    session.add(new_student)
    session.commit()
    rows = list(session.execute(text("select name from students")))
    assert rows == [("John",)]
