from typing import List, Dict, Optional


def get_majors_list(campus: Optional[str] = None) -> List[dict]:
    """
    Trả về danh sách các ngành học, lọc theo campus nếu có
    
    Args:
        campus: Tên campus để lọc (tùy chọn)
        
    Returns:
        Danh sách các ngành học dưới dạng dictionary
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    majors = [
        {"major_code": "AI", "name": "Trí tuệ nhân tạo", "campus": "Đà Nẵng"},
        {"major_code": "CS", "name": "Khoa học máy tính", "campus": "Đà Nẵng"},
        {"major_code": "SE", "name": "Kỹ thuật phần mềm", "campus": "Đà Nẵng"},
        {"major_code": "BA", "name": "Kinh doanh số", "campus": "Hà Nội"},
        {"major_code": "FIN", "name": "Tài chính", "campus": "Hà Nội"},
        {"major_code": "MKT", "name": "Marketing số", "campus": "Hà Nội"},
        {"major_code": "DS", "name": "Khoa học dữ liệu", "campus": "Hồ Chí Minh"},
        {"major_code": "IOT", "name": "Internet vạn vật", "campus": "Hồ Chí Minh"}
    ]
    
    if campus:
        return [major for major in majors if campus in major["campus"]]
    return majors


def get_major_detail(major_code: str) -> dict:
    """
    Trả về chi tiết ngành học: môn học, cơ hội việc làm, mô tả
    
    Args:
        major_code: Mã ngành học
        
    Returns:
        Thông tin chi tiết về ngành học
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    major_details = {
        "AI": {
            "name": "Trí tuệ nhân tạo",
            "subjects": ["Machine Learning", "Deep Learning", "Python", "Computer Vision", "NLP"],
            "career": ["AI Engineer", "Data Scientist", "Machine Learning Engineer"],
            "description": "Chương trình đào tạo về trí tuệ nhân tạo, tập trung vào các kỹ thuật học máy và ứng dụng AI"
        },
        "CS": {
            "name": "Khoa học máy tính",
            "subjects": ["Algorithms", "Data Structures", "Operating Systems", "Computer Networks"],
            "career": ["Software Developer", "System Architect", "Research Scientist"],
            "description": "Chương trình đào tạo nền tảng về khoa học máy tính và các nguyên lý cơ bản"
        },
        "SE": {
            "name": "Kỹ thuật phần mềm",
            "subjects": ["Software Engineering", "Project Management", "Web Development", "Mobile Development"],
            "career": ["Software Engineer", "Project Manager", "DevOps Engineer"],
            "description": "Chương trình đào tạo về quy trình phát triển phần mềm và kỹ thuật lập trình"
        },
        "BA": {
            "name": "Kinh doanh số",
            "subjects": ["Digital Business Models", "E-commerce", "Business Analytics", "Digital Marketing"],
            "career": ["Business Analyst", "Digital Transformation Specialist", "E-commerce Manager"],
            "description": "Chương trình đào tạo về mô hình kinh doanh số và chuyển đổi số trong doanh nghiệp"
        },
        "FIN": {
            "name": "Tài chính",
            "subjects": ["Financial Management", "Investment Analysis", "FinTech", "Risk Management"],
            "career": ["Financial Analyst", "Investment Banker", "FinTech Specialist"],
            "description": "Chương trình đào tạo về quản lý tài chính và công nghệ tài chính"
        },
        "MKT": {
            "name": "Marketing số",
            "subjects": ["Digital Marketing", "Social Media Marketing", "SEO/SEM", "Content Marketing"],
            "career": ["Digital Marketing Manager", "Social Media Specialist", "SEO Expert"],
            "description": "Chương trình đào tạo về chiến lược marketing trên nền tảng số"
        },
        "DS": {
            "name": "Khoa học dữ liệu",
            "subjects": ["Data Mining", "Statistical Analysis", "Big Data", "Data Visualization"],
            "career": ["Data Scientist", "Data Analyst", "Business Intelligence Analyst"],
            "description": "Chương trình đào tạo về phân tích và xử lý dữ liệu lớn"
        },
        "IOT": {
            "name": "Internet vạn vật",
            "subjects": ["Embedded Systems", "IoT Protocols", "Sensor Networks", "Edge Computing"],
            "career": ["IoT Engineer", "Embedded Systems Developer", "Smart City Specialist"],
            "description": "Chương trình đào tạo về hệ thống kết nối và Internet vạn vật"
        }
    }
    
    if major_code in major_details:
        return major_details[major_code]
    return {"error": f"Không tìm thấy thông tin cho mã ngành {major_code}"}


def get_tuition_info(major: str, campus: str, year: int) -> dict:
    """
    Trả về học phí ngành học theo campus và năm
    
    Args:
        major: Mã ngành học
        campus: Tên campus
        year: Năm học
        
    Returns:
        Thông tin học phí
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    tuition_data = {
        # Năm 2025
        2025: {
            "Đà Nẵng": {
                "AI": {"tuition_fee": "27.300.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "CS": {"tuition_fee": "25.500.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "SE": {"tuition_fee": "26.800.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"}
            },
            "Hà Nội": {
                "BA": {"tuition_fee": "29.500.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "FIN": {"tuition_fee": "30.200.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "MKT": {"tuition_fee": "28.900.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"}
            },
            "Hồ Chí Minh": {
                "DS": {"tuition_fee": "28.500.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "IOT": {"tuition_fee": "27.800.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"}
            }
        },
        # Năm 2024
        2024: {
            "Đà Nẵng": {
                "AI": {"tuition_fee": "25.800.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "CS": {"tuition_fee": "24.200.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "SE": {"tuition_fee": "25.300.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"}
            },
            "Hà Nội": {
                "BA": {"tuition_fee": "28.000.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "FIN": {"tuition_fee": "28.700.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "MKT": {"tuition_fee": "27.400.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"}
            },
            "Hồ Chí Minh": {
                "DS": {"tuition_fee": "27.000.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"},
                "IOT": {"tuition_fee": "26.300.000 VND/kỳ", "note": "Miễn 100% nếu SchoolRank Top 10%", "currency": "VND"}
            }
        }
    }
    
    if year in tuition_data and campus in tuition_data[year] and major in tuition_data[year][campus]:
        return tuition_data[year][campus][major]
    return {"error": f"Không tìm thấy thông tin học phí cho ngành {major} tại campus {campus} năm {year}"}


def get_admission_methods(year: int) -> List[str]:
    """
    Liệt kê các hình thức xét tuyển theo năm
    
    Args:
        year: Năm xét tuyển
        
    Returns:
        Danh sách các hình thức xét tuyển
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    admission_methods = {
        2025: ["Học bạ", "Kết quả thi THPT", "Xét tuyển thẳng theo giải thưởng", "SchoolRank"],
        2024: ["Học bạ", "Kết quả thi THPT", "Xét tuyển thẳng theo giải thưởng"],
        2023: ["Học bạ", "Kết quả thi THPT"]
    }
    
    if year in admission_methods:
        return admission_methods[year]
    return ["Không có thông tin cho năm xét tuyển này"]


def get_scholarship_conditions(year: int) -> List[dict]:
    """
    Điều kiện nhận học bổng tương ứng học lực/SchoolRank
    
    Args:
        year: Năm học
        
    Returns:
        Danh sách các điều kiện học bổng
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    scholarship_conditions = {
        2025: [
            {"type": "100%", "condition": "SchoolRank top 10% + học bạ >= 8.5"},
            {"type": "70%", "condition": "SchoolRank top 20% + học bạ >= 8.0"},
            {"type": "50%", "condition": "SchoolRank top 30% + học bạ >= 7.5"},
            {"type": "30%", "condition": "Học bạ >= 8.0"}
        ],
        2024: [
            {"type": "100%", "condition": "Học bạ >= 9.0"},
            {"type": "70%", "condition": "Học bạ >= 8.5"},
            {"type": "50%", "condition": "Học bạ >= 8.0"},
            {"type": "30%", "condition": "Học bạ >= 7.5"}
        ]
    }
    
    if year in scholarship_conditions:
        return scholarship_conditions[year]
    return [{"error": f"Không có thông tin học bổng cho năm {year}"}]


def get_campuses() -> List[dict]:
    """
    Danh sách campus (tên, địa chỉ, thông tin liên hệ)
    
    Returns:
        Danh sách các campus
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    campuses = [
        {
            "name": "Đà Nẵng",
            "address": "Khu đô thị FPT, Ngũ Hành Sơn, Đà Nẵng",
            "phone": "0236.730.2266",
            "email": "danang@university.edu.vn",
            "has_dorm": True
        },
        {
            "name": "Hà Nội",
            "address": "Khu CNC Hòa Lạc, Km29 Đại lộ Thăng Long, Thạch Thất, Hà Nội",
            "phone": "024.7300.5588",
            "email": "hanoi@university.edu.vn",
            "has_dorm": True
        },
        {
            "name": "Hồ Chí Minh",
            "address": "Lô E2a-7, Đường D1, Khu Công nghệ cao, P. Long Thạnh Mỹ, TP. Thủ Đức",
            "phone": "028.7300.5588",
            "email": "hochiminh@university.edu.vn",
            "has_dorm": True
        },
        {
            "name": "Cần Thơ",
            "address": "Khu vực 6, P. Phú Thứ, Q. Cái Răng, TP. Cần Thơ",
            "phone": "0292.730.0068",
            "email": "cantho@university.edu.vn",
            "has_dorm": False
        }
    ]
    
    return campuses


def get_calendar_deadlines(year: int) -> dict:
    """
    Trả về các mốc thời gian quan trọng: nhận hồ sơ, công bố kết quả, nhập học
    
    Args:
        year: Năm xét tuyển
        
    Returns:
        Các mốc thời gian quan trọng
    """
    # Dữ liệu mẫu - trong thực tế sẽ lấy từ cơ sở dữ liệu
    calendar_deadlines = {
        2025: {
            "application_open": "2025-03-01",
            "application_close": "2025-06-30",
            "result_day": "2025-07-15",
            "enrollment_start": "2025-07-20",
            "enrollment_end": "2025-08-15",
            "orientation_day": "2025-08-25",
            "first_day": "2025-09-01"
        },
        2024: {
            "application_open": "2024-03-01",
            "application_close": "2024-06-30",
            "result_day": "2024-07-15",
            "enrollment_start": "2024-07-20",
            "enrollment_end": "2024-08-15",
            "orientation_day": "2024-08-25",
            "first_day": "2024-09-01"
        }
    }
    
    if year in calendar_deadlines:
        return calendar_deadlines[year]
    return {"error": f"Không có thông tin lịch tuyển sinh cho năm {year}"}


def get_introduction() -> str:
    """
    Trả về thông tin giới thiệu về Đại học FPT
    
    Returns:
        Thông tin giới thiệu về Đại học FPT
    """
    return """
    Đại học FPT (FPT University) là một trong những trường đại học hàng đầu ở Việt Nam, được thành lập vào năm 1992. Đại học FPT có 10 cơ sở giáo dục tại Hà Nội, Đà Nẵng, Hồ Chí Minh, Cần Thơ, Hải Phòng, Đà Lạt, Bà Rịa-Vũng Tàu, và Hà Nam.
    """
    

