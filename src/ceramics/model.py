from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
from typing import Optional

from ceramics.utils import weekly_date_range


class AttendanceStatus(Enum):
    PRESENT = auto()
    ABSENT = auto()
    UNKNOWN = auto()


@dataclass(unsafe_hash=True)
class Student:
    name: str


@dataclass(unsafe_hash=True, order=True)
class Lesson:
    date: str
    attendance: set["Attendance"] = field(hash=False, default_factory=set)

    @property
    def students(self):
        return [a.student for a in self.attendance]

    def student_attendance(self, student):
        return next(a for a in self.attendance if a.student == student)

    def update_attendance_status(self, student: Student, status: AttendanceStatus):
        if student in self.students:
            attendance = self.student_attendance(student)
            attendance.status = status
        else:
            self.attendance.add(Attendance(student, status))


@dataclass(unsafe_hash=True)
class Attendance:
    student: Student = field(hash=True, compare=True)
    status: AttendanceStatus = field(
        hash=False, default_factory=lambda: AttendanceStatus.UNKNOWN
    )


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

    def get_lesson_by_date(self, date: date):
        return next(l for l in self.lessons if l.date == date)

    def enroll(self, student: Student):
        self.enrollments.add(student)

    def disenroll(self, student: Student):
        self.enrollments.remove(student)
