from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from ceramics import model

mapper_registry = registry()

student = Table(
    "students",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
)

lesson = Table(
    "lessons",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date(), nullable=False),
    Column("course_id", Integer, ForeignKey("courses.id")),
)

course = Table(
    "courses",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("start_date", Date(), nullable=False),
    Column("end_date", Date(), nullable=False),
    Column("weekday", Integer(), nullable=False),
    Column("price_per_lesson", Integer(), nullable=False),
)

enrollment = Table(
    "enrollments",
    mapper_registry.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)

attendance = Table(
    "attendance",
    mapper_registry.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("lesson_id", Integer, ForeignKey("lessons.id"), primary_key=True),
    Column("present", Boolean),
)


def start_mappers():
    student_mapper = mapper_registry.map_imperatively(model.Student, student)
    attendance_mapper = mapper_registry.map_imperatively(model.Attendance, attendance)
    lessson_mapper = mapper_registry.map_imperatively(
        model.Lesson,
        lesson,
        properties={
            "attendance": relationship(attendance_mapper, collection_class=set),
        },
    )
    mapper_registry.map_imperatively(
        model.Course,
        course,
        properties={
            "lessons": relationship(lessson_mapper, collection_class=set),
            "enrollments": relationship(
                student_mapper, secondary=enrollment, collection_class=set
            ),
        },
    )
