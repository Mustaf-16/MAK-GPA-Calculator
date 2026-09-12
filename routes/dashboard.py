from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping


GRADE_POINTS = {
    "A+": 5.0,
    "A": 5.0,
    "B+": 4.5,
    "B": 4.0,
    "C+": 3.5,
    "C": 3.0,
    "D+": 2.5,
    "D": 2.0,
    "E": 1.5,
    "E-": 1.0,
    "F": 0.0,
}


class MAKGradingSystem:
    """Convert MAK marks and letter grades into grade points."""

    grade_points = GRADE_POINTS

    @classmethod
    def grade_from_mark(cls, mark: float) -> str:
        """Convert a mark from 0 to 100 into a MAK letter grade."""
        try:
            mark = float(mark)
        except (TypeError, ValueError) as error:
            raise ValueError("Mark must be a number between 0 and 100") from error

        if not isfinite(mark) or not 0 <= mark <= 100:
            raise ValueError("Mark must be between 0 and 100")

        if mark >= 90:
            return "A+"
        if mark >= 80:
            return "A"
        if mark >= 75:
            return "B+"
        if mark >= 70:
            return "B"
        if mark >= 65:
            return "C+"
        if mark >= 60:
            return "C"
        if mark >= 55:
            return "D+"
        if mark >= 50:
            return "D"
        return "F"

    @classmethod
    def grade_point(cls, grade: str) -> float:
        """Return the point value for a MAK letter grade."""
        normalized_grade = str(grade).strip().upper()
        try:
            return cls.grade_points[normalized_grade]
        except KeyError as error:
            valid_grades = ", ".join(cls.grade_points)
            raise ValueError(f"Invalid grade. Use one of: {valid_grades}") from error


@dataclass(frozen=True)
class Course:
    """Represent one course used in a GPA calculation."""

    credits: float
    mark: float | None = None
    grade: str | None = None

    def get_grade(self) -> str:
        """Return the course grade, deriving it from the mark when needed."""
        if self.grade is not None and str(self.grade).strip():
            return str(self.grade).strip().upper()
        if self.mark is not None:
            return MAKGradingSystem.grade_from_mark(self.mark)
        raise ValueError("Each course must have a mark or grade")

    def get_grade_point(self) -> float:
        """Return this course's grade-point value."""
        return MAKGradingSystem.grade_point(self.get_grade())


def _course_from_mapping(course: Mapping[str, object]) -> Course:
    """Build a Course from form/JSON-friendly dictionary data."""
    return Course(
        credits=course["credits"],
        mark=course.get("mark"),
        grade=course.get("grade"),
    )

class GPA:
    """Calculate a credit-weighted GPA for a collection of courses."""

    def __init__(self, courses: Iterable[Course | Mapping[str, object]]):
        self.courses = [
            _course_from_mapping(course) if isinstance(course, Mapping) else course
            for course in courses
        ]

    def calculate(self) -> float:
        """Return the GPA on the MAK 5.0 scale."""
        total_quality_points = 0.0
        total_credits = 0.0

        for course in self.courses:
            try:
                credits = float(course.credits)
            except (TypeError, ValueError) as error:
                raise ValueError("Course credits must be a positive number") from error
            if not isfinite(credits) or credits <= 0:
                raise ValueError("Course credits must be a positive number")

            total_quality_points += credits * course.get_grade_point()
            total_credits += credits

        if total_credits == 0:
            raise ValueError("At least one course is required")

        return round(total_quality_points / total_credits, 2)


# Keep the original function API for existing Flask routes and callers.
def grade_from_mark(mark: float) -> str:
    return MAKGradingSystem.grade_from_mark(mark)


def grade_point(grade: str) -> float:
    return MAKGradingSystem.grade_point(grade)


def calculate_gpa(courses: Iterable[Course | Mapping[str, object]]) -> float:
    return GPA(courses).calculate()


def classify_gpa(gpa: float) -> str:
    """Return the academic classification for a GPA on the 5.0 scale."""
    try:
        gpa = float(gpa)
    except (TypeError, ValueError) as error:
        raise ValueError("GPA must be a number between 0 and 5") from error

    if not isfinite(gpa) or not 0 <= gpa <= 5:
        raise ValueError("GPA must be between 0 and 5")

    if gpa >= 4.40:
        return "First Class"
    if gpa >= 3.60:
        return "Second Class - Upper"
    if gpa >= 2.80:
        return "Second Class - Lower"
    if gpa >= 1.00:
        return "Pass"
    return "Below Pass"


# Backward-compatible names for callers using the original method names.
def MAK_GRADE(mark: float) -> str:
    return grade_from_mark(mark)
