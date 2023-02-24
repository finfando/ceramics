from dataclasses import dataclass, field
from datetime import date


@dataclass(unsafe_hash=True)
class Student:
    name: str


@dataclass(unsafe_hash=True)
class Course:
    name: str
    start_date: date
    end_date: date
    weekday: int
    price_per_lesson: int
    enrollments: set[Student] = field(hash=False, default_factory=set)

    def enroll(self, student: Student):
        self.enrollments.add(student)

    def disenroll(self, student: Student):
        self.enrollments.remove(student)


def enroll(course: Course, student: Student):
    course.enroll(student)
