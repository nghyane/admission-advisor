from typing import Dict, Optional, Any
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from datetime import datetime

# Import client API trực tiếp
from ..api.client import default_client


def get_campuses(name: Optional[str] = None, address: Optional[str] = None, tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """
    Lấy danh sách các cơ sở (campus) của Đại học FPT.

    Sử dụng khi người dùng muốn biết các cơ sở đào tạo hoặc muốn lọc theo tên hay địa chỉ cụ thể.

    Args:
        name (Optional[str]): Tên campus cần lọc (nếu có).
        address (Optional[str]): Địa chỉ campus cần lọc (nếu có).
        tool_context (Optional[ToolContext]): Ngữ cảnh tool, dùng để ghi trạng thái gọi gần nhất.

    Returns:
        Dict[str, Any]: Kết quả bao gồm danh sách campus hoặc thông báo lỗi nếu có.
    """
    if tool_context and hasattr(tool_context, 'state'):
        # Sử dụng không có prefix cho thông tin phiên hiện tại
        tool_context.state['current_tool'] = 'get_campuses'
        # Sử dụng temp: prefix cho biến tạm thời
        tool_context.state['temp:api_params'] = {'name': name, 'address': address}

    params = {k: v for k, v in {'name': name, 'address': address}.items() if v is not None}
    return default_client.get("/api/campuses", params)


def get_majors_list(campus_code: Optional[str] = None, academic_year: Optional[int] = None, tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """
    Lấy danh sách ngành học của Đại học FPT, có thể lọc theo cơ sở và năm học.

    Dùng khi người dùng hỏi về ngành đào tạo ở campus cụ thể hoặc năm cụ thể.

    Args:
        campus_code (Optional[str]): Mã cơ sở đào tạo để lọc.
        academic_year (Optional[int]): Năm học cần lọc.
        tool_context (Optional[ToolContext]): Ngữ cảnh tool để lưu state liên quan.

    Returns:
        Dict[str, Any]: Danh sách ngành hoặc thông báo lỗi nếu có.
    """
    if tool_context and hasattr(tool_context, 'state'):
        # Sử dụng không có prefix cho thông tin phiên hiện tại
        tool_context.state['current_tool'] = 'get_majors_list'
        tool_context.state['current_campus'] = campus_code

        # Lưu năm học mặc định vào app state nếu được cung cấp
        if academic_year:
            tool_context.state['app:default_academic_year'] = academic_year

    params = {k: v for k, v in {'campus_code': campus_code, 'academic_year': academic_year}.items() if v is not None}
    return default_client.get("/api/majors", params)


def store_student_profile(
    name: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    high_school: Optional[str] = None,
    school_rank: Optional[float] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Lưu thông tin hồ sơ sinh viên vào state và đồng bộ với HubSpot nếu có email.

    Args:
        name (str): Tên sinh viên.
        email (Optional[str]): Email liên hệ.
        phone (Optional[str]): Số điện thoại.
        high_school (Optional[str]): Tên trường THPT.
        school_rank (Optional[float]): Xếp hạng hoặc điểm trung bình.
        tool_context (Optional[ToolContext]): Ngữ cảnh tool để lưu vào state.

    Returns:
        Dict[str, Any]: Trạng thái thao tác (thành công hoặc lỗi).
    """
    # Kiểm tra tool_context cơ bản
    if not tool_context or not hasattr(tool_context, 'state'):
        return {"status": "error", "message": "Không thể lưu thông tin sinh viên do thiếu tool_context"}

    # Tạo profile với các trường bắt buộc và tùy chọn
    profile = {"name": name, "updated_at": datetime.now().isoformat()}

    # Thêm các trường tùy chọn nếu có
    for key, value in {"email": email, "phone": phone, "high_school": high_school, "school_rank": school_rank}.items():
        if value is not None:
            profile[key] = value

    # Lưu vào state
    tool_context.state["user:student_profile"] = profile

    # Nếu không có email, chỉ lưu vào state
    if not email:
        return {"status": "success", "message": f"Đã lưu thông tin sinh viên {name} thành công"}

    # Lấy session_id từ invocation_context
    try:
        session_id = tool_context._invocation_context.session.id
    except (AttributeError, TypeError):
        return {"status": "partial_success", "message": f"Đã lưu thông tin sinh viên {name} vào state nhưng không đồng bộ được với HubSpot"}

    if not session_id:
        return {"status": "partial_success", "message": f"Đã lưu thông tin sinh viên {name} vào state nhưng không đồng bộ được với HubSpot"}

    # Chuẩn bị dữ liệu HubSpot
    hubspot_data = {"email": email, "session_id": session_id, "firstname": name}
    if phone: hubspot_data["phone"] = phone
    if high_school: hubspot_data["school"] = high_school
    if school_rank is not None: hubspot_data["school_rank"] = str(school_rank)

    # Gọi API để tạo/cập nhật contact trên HubSpot
    response = default_client.post("/api/hubspot/contact", hubspot_data)

    # Xử lý kết quả API
    if response.get("success"):
        # Lưu ID HubSpot vào profile nếu có
        if response.get("data", {}).get("id"):
            profile["hubspot_id"] = response["data"]["id"]
            tool_context.state["user:student_profile"] = profile

        return {
            "status": "success",
            "message": f"Đã lưu thông tin sinh viên {name} thành công và đồng bộ với HubSpot",
            "hubspot_data": response.get("data")
        }

    # Trả về kết quả từ API nếu không thành công
    return {
        "status": "partial_success",
        "message": f"Đã lưu thông tin sinh viên {name} vào state nhưng không đồng bộ được với HubSpot",
        "api_response": response
    }


def get_user_profile(tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """
    Truy xuất thông tin hồ sơ sinh viên đã lưu trong state từ lần tương tác trước.

    Args:
        tool_context (Optional[ToolContext]): Ngữ cảnh tool để truy cập state.

    Returns:
        Dict[str, Any]: Hồ sơ sinh viên nếu có, hoặc thông báo lỗi nếu chưa lưu.
    """
    if not tool_context or not hasattr(tool_context, 'state'):
        return {"status": "error", "message": "Không thể lấy thông tin người dùng do thiếu tool_context hoặc state không khả dụng"}

    # Truy xuất từ user: prefix
    profile = tool_context.state.get("user:student_profile")
    if not profile:
        return {"status": "error", "message": "Chưa có thông tin người dùng nào được lưu"}

    return {"status": "success", "profile": profile}


def get_major_detail(major_code: str, academic_year: Optional[int] = None, tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """
    Lấy thông tin chi tiết về một ngành học cụ thể theo mã ngành và năm học (nếu có).

    Dùng khi người dùng hỏi chi tiết ngành hoặc cần điều kiện đầu vào.

    Args:
        major_code (str): Mã ngành học cần lấy thông tin.
        academic_year (Optional[int]): Năm học cần lọc.
        tool_context (Optional[ToolContext]): Ngữ cảnh tool để lưu state liên quan.

    Returns:
        Dict[str, Any]: Thông tin ngành chi tiết hoặc lỗi nếu có.
    """
    if tool_context and hasattr(tool_context, 'state'):
        # Sử dụng không có prefix cho thông tin phiên hiện tại
        tool_context.state['current_tool'] = 'get_major_detail'
        tool_context.state['current_major_code'] = major_code

        # Lưu năm học mặc định vào app state nếu được cung cấp
        if academic_year:
            tool_context.state['app:default_academic_year'] = academic_year

    params = {k: v for k, v in {'academic_year': academic_year}.items() if v is not None}
    return default_client.get(f"/api/majors/{major_code}", params)



def get_admission_methods(
    major_code: Optional[str] = None,
    academic_year: Optional[int] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Lấy danh sách các phương thức xét tuyển, bổ sung trường 'scope': 'global' hoặc 'specific'.

    Args:
        major_id (Optional[int]): ID ngành học để lọc.
        academic_year (Optional[int]): Năm học để lọc.
        tool_context (Optional[ToolContext]): ToolContext được ADK truyền vào.

    Returns:
        Dict[str, Any]: Kết quả có bổ sung scope cho từng phương thức.
    """
    if tool_context and hasattr(tool_context, 'state'):
        # Sử dụng không có prefix cho thông tin phiên hiện tại
        tool_context.state['current_tool'] = 'get_admission_methods'
        if major_code:
            tool_context.state['current_major_code'] = major_code

        # Lưu năm học mặc định vào app state nếu được cung cấp
        if academic_year:
            tool_context.state['app:default_academic_year'] = academic_year

    # Build query params (không truyền is_active nếu không cần)
    params = {
        k: v for k, v in {
            'major_code': major_code,
            'academic_year': academic_year
        }.items() if v is not None
    }

    # Gọi API
    response = default_client.get("/api/admission-methods", params)

    # Nếu không thành công hoặc không có data → return như cũ
    if not response.get("success") or "data" not in response:
        return response

    # Bổ sung trường 'scope' cho từng phương thức
    for method in response["data"]:
        applications = method.get("applications", [])

        if not applications:
            method["scope"] = "unspecified"
        elif all(app.get("major") is None for app in applications):
            method["scope"] = "global"
        else:
            method["scope"] = "specific"

    return response


def get_dormitory_by_campus(
    campus_code: str,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Lấy danh sách ký túc xá tại một cơ sở của Đại học FPT.

    Args:
        campus_code (str): Mã cơ sở như HCM, HN, DN, v.v. (bắt buộc).
        tool_context (Optional[ToolContext]): Context của tool từ Google ADK.

    Returns:
        Dict[str, Any]: Kết quả gồm thông tin ký túc xá và campus.
    """
    if tool_context and hasattr(tool_context, "state"):
        # Sử dụng không có prefix cho thông tin phiên hiện tại
        tool_context.state["current_tool"] = "get_dormitory_by_campus"
        tool_context.state["current_campus"] = campus_code

    # Gọi API dormitories theo campus_code
    return default_client.get("/api/dormitories", {"campus_code": campus_code})


def get_scholarships_list(
    campus_code: Optional[str] = None,
    major_code: Optional[str] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Lấy danh sách học bổng Đại học FPT theo campus và/hoặc ngành học.

    Args:
        campus_code (Optional[str]): Mã cơ sở (HCM, HN, QN...).
        major_code (Optional[str]): Mã ngành học (7480107...).
        tool_context (Optional[ToolContext]): Ngữ cảnh làm việc.

    Returns:
        Dict[str, Any]: Danh sách học bổng đã phân loại scope.
    """
    if tool_context and hasattr(tool_context, 'state'):
        # Sử dụng không có prefix cho thông tin phiên hiện tại
        tool_context.state['current_tool'] = 'get_scholarships_list'
        if major_code:
            tool_context.state['current_major_code'] = major_code
        if campus_code:
            tool_context.state['current_campus'] = campus_code

    params = {}
    if campus_code:
        params["campus_code"] = campus_code
    if major_code:
        params["major_code"] = major_code

    response = default_client.get("/api/scholarships", params=params)

    if not response.get("success") or "data" not in response:
        return response

    scholarships = []
    for item in response["data"]:
        for availability in item.get("availabilities", []):
            major = availability.get("major")
            campus = availability.get("campus")
            academic_year = availability.get("academicYear", {}).get("year")

            if not major and not campus:
                scope = "global"
            elif not major and campus:
                scope = "campus_all_majors"
            elif major and campus:
                scope = "major_specific_campus"
            elif major and not campus:
                scope = "major_all_campuses"
            else:
                scope = "unknown"

            scholarships.append({
                "name": item.get("name"),
                "description": item.get("description"),
                "amount": item.get("amount"),
                "condition": item.get("condition"),
                "application_url": item.get("application_url"),
                "scope": scope,
                "major_code": major.get("code") if major else None,
                "campus_code": campus.get("code") if campus else None,
                "academic_year": academic_year,
            })

    return {"success": True, "scholarships": scholarships}


def debug_invocation_context(tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """
    Tool để hiển thị toàn bộ thông tin từ invocation_context.

    Args:
        tool_context (Optional[ToolContext]): Context của tool.

    Returns:
        Dict[str, Any]: Toàn bộ thông tin từ invocation_context.
    """
    if not tool_context:
        return {
            "status": "error",
            "message": "Missing tool context"
        }

    print("Tool Context:", tool_context._invocation_context.user_id)


    try:
        # Lấy toàn bộ thông tin từ invocation_context
        if hasattr(tool_context, 'invocation_context'):
            context_info = vars(tool_context.invocation_context)
            # Convert tất cả các giá trị thành string để đảm bảo có thể serialize
            serializable_info = {
                key: str(value)
                for key, value in context_info.items()
            }

            print("Invocation Context:", serializable_info)

            return {
                "status": "success",
                "invocation_context": serializable_info
            }
        else:
            return {
                "status": "error",
                "message": "No invocation_context available"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error accessing invocation_context: {str(e)}"
        }
