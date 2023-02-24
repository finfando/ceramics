from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from ceramics import model

mapper_registry = registry()

student = Table(
    "students",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
)

course = Table(
    "courses",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
)

enrollment = Table(
    "enrollments",
    mapper_registry.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)


def start_mappers():
    student_mapper = mapper_registry.map_imperatively(model.Student, student)
    mapper_registry.map_imperatively(
        model.Course,
        course,
        properties={
            "enrollments": relationship(
                student_mapper, secondary=enrollment, collection_class=set
            )
        },
    )
