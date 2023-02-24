from ceramics.model import Course, Student
from datetime import date

fake_course_params = ("Fake course name", date(2023, 2, 27), date(2023, 6, 30), 3, 50)


def test_student_can_enroll_in_course():
    student = Student("John")
    course = Course(*fake_course_params)
    course.enroll(student)
    assert student in course.enrollments


def test_student_can_disenroll_from_course():
    student = Student("John")
    course = Course(*fake_course_params, enrollments={student})
    course.disenroll(student)
    assert student not in course.enrollments
