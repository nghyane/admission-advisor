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

from typing import Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class Student(BaseModel):
    """
    Đại diện cho một sinh viên tiềm năng với thông tin tối giản.
    """
    student_id: str
    name: str
    email: str
    phone: str
    high_school: str
    school_rank: float = 0.0
    interests: Dict[str, bool] = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """
        Chuyển đổi đối tượng Student thành chuỗi JSON.

        Returns:
            Chuỗi JSON đại diện cho đối tượng Student.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_student(student_id: str) -> Optional["Student"]:
        """
        Lấy thông tin sinh viên dựa trên ID.

        Args:
            student_id: ID của sinh viên cần lấy thông tin.

        Returns:
            Đối tượng Student nếu tìm thấy, None nếu không.
        """
        # Trong ứng dụng thực tế, đây sẽ là truy vấn cơ sở dữ liệu.
        # Trong ví dụ này, chúng ta chỉ trả về một sinh viên mẫu.
        return Student(
            student_id=student_id,
            name="Nguyễn Văn A",
            email="nguyenvana@example.com",
            phone="0912345678",
            high_school="THPT Chu Văn An",
            school_rank=8.5,
            interests={
                "technology": True,
                "business": False,
                "design": True,
                "communication": False
            }
        )
