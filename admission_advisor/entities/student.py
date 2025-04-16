# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Student entity module."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class AcademicRecord(BaseModel):
    """
    Represents a student's academic record.
    """
    institution: str
    degree: str
    major: str
    gpa: float
    graduation_date: str
    model_config = ConfigDict(from_attributes=True)


class TestScore(BaseModel):
    """
    Represents a standardized test score.
    """
    test_name: str
    score: float
    date_taken: str
    model_config = ConfigDict(from_attributes=True)


class ContactInformation(BaseModel):
    """
    Represents a student's contact information.
    """
    email: str
    phone_number: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    model_config = ConfigDict(from_attributes=True)


class AcademicInterest(BaseModel):
    """
    Represents a student's academic interests.
    """
    field_of_study: str
    program_level: str  # undergraduate, graduate, etc.
    specific_programs: List[str]
    career_goals: List[str]
    model_config = ConfigDict(from_attributes=True)


class ApplicationStatus(BaseModel):
    """
    Represents the status of a student's application.
    """
    application_id: str
    program_id: str
    submission_date: str
    status: str  # submitted, under review, accepted, rejected, etc.
    missing_documents: List[str] = []
    model_config = ConfigDict(from_attributes=True)


class Student(BaseModel):
    """
    Represents a prospective student.
    """
    student_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    contact_information: ContactInformation
    academic_records: List[AcademicRecord]
    test_scores: List[TestScore]
    academic_interests: AcademicInterest
    residency_status: str  # in-state, out-of-state, international
    applications: List[ApplicationStatus] = []
    scheduled_appointments: Dict = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """
        Converts the Student object to a JSON string.

        Returns:
            A JSON string representing the Student object.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_student(student_id: str) -> Optional["Student"]:
        """
        Retrieves a student based on their ID.

        Args:
            student_id: The ID of the student to retrieve.

        Returns:
            The Student object if found, None otherwise.
        """
        # In a real application, this would involve a database lookup.
        # For this example, we'll just return a dummy student.
        return Student(
            student_id=student_id,
            first_name="Maria",
            last_name="Garcia",
            date_of_birth="2003-05-15",
            contact_information=ContactInformation(
                email="maria.garcia@example.com",
                phone_number="+1-555-123-4567",
                address="123 College Ave",
                city="Anytown",
                state="CA",
                zip_code="90210",
                country="USA"
            ),
            academic_records=[
                AcademicRecord(
                    institution="Anytown High School",
                    degree="High School Diploma",
                    major="General Studies",
                    gpa=3.8,
                    graduation_date="2023-05-30"
                )
            ],
            test_scores=[
                TestScore(
                    test_name="SAT",
                    score=1350,
                    date_taken="2022-11-05"
                ),
                TestScore(
                    test_name="ACT",
                    score=29,
                    date_taken="2022-10-22"
                )
            ],
            academic_interests=AcademicInterest(
                field_of_study="Computer Science",
                program_level="undergraduate",
                specific_programs=["Computer Science", "Data Science", "Artificial Intelligence"],
                career_goals=["Software Engineer", "Data Scientist", "AI Researcher"]
            ),
            residency_status="in-state",
            applications=[
                ApplicationStatus(
                    application_id="APP-2023-001",
                    program_id="CS-BS-001",
                    submission_date="2023-12-15",
                    status="under review",
                    missing_documents=["Official Transcript"]
                )
            ],
            scheduled_appointments={}
        )
