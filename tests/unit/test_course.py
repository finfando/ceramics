from ceramics.model import Course, Student


def test_student_can_enroll_in_course():
    student = Student("John")
    course = Course("Ceramics")
    course.enroll(student)
    assert student in course.enrollments


def test_student_can_disenroll_from_course():
    student = Student("John")
    course = Course("Ceramics", enrollments={student})
    course.disenroll(student)
    assert student not in course.enrollments
