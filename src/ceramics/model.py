from dataclasses import dataclass, field
from datetime import date

from ceramics.utils import weekly_date_range


@dataclass(unsafe_hash=True)
class Student:
    name: str


@dataclass(unsafe_hash=True, order=True)
class Lesson:
    date: str
    attendance: set["Attendance"] = field(hash=False, default_factory=set)


@dataclass(unsafe_hash=True)
class Attendance:
    student: Student
    lesson: Lesson
    present: bool


@dataclass(unsafe_hash=True)
class Course:
    name: str
    start_date: date
    end_date: date
    weekday: int
    price_per_lesson: int
    lessons: set[Lesson] = field(default_factory=set)
    enrollments: set[Student] = field(hash=False, default_factory=set)

    def __post_init__(self):
        self.add_lessons()

    def add_lessons(self):
        for date in weekly_date_range(self.start_date, self.end_date, self.weekday):
            self.lessons.add(Lesson(date))

    @property
    def lessons_sorted(self):
        return sorted(self.lessons)

    def enroll(self, student: Student):
        self.enrollments.add(student)

    def disenroll(self, student: Student):
        self.enrollments.remove(student)
