"""
API Client cho Admission Advisor.
"""

from typing import Dict, Any, Optional, Union, Callable
import requests
import logging
from datetime import datetime
from functools import wraps

# Import cấu hình
from ..config import Config

# Cấu hình logging
logger = logging.getLogger(__name__)

class ApiClient:
    """
    Client để tương tác với API backend.
    Xử lý các yêu cầu HTTP, lỗi và định dạng response.
    """

    def __init__(self, base_url: str = "") -> None:
        """
        Khởi tạo API client.

        Args:
            base_url: URL cơ sở của API
        """
        self.base_url = base_url

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Phương thức chung để thực hiện các yêu cầu HTTP.

        Args:
            method: Phương thức HTTP (GET, POST, etc.)
            endpoint: Endpoint API cần gọi
            **kwargs: Các tham số bổ sung cho request

        Returns:
            Dictionary chứa response từ API
        """
        url = f"{self.base_url}{endpoint}"
        try:
            # Thực hiện request
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()

            # Parse JSON response
            return response.json()
        except Exception as e:
            # Log lỗi và trả về response lỗi từ backend
            logger.error(f"Lỗi khi gọi API {url}: {str(e)}")
            return self._create_error_response(f"Lỗi API: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Thực hiện yêu cầu GET đến API.

        Args:
            endpoint: Endpoint API cần gọi
            params: Tham số query string (tùy chọn)

        Returns:
            Dictionary chứa response từ API
        """
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Thực hiện yêu cầu POST đến API.

        Args:
            endpoint: Endpoint API cần gọi
            data: Dữ liệu JSON để gửi trong body
            params: Tham số query string (tùy chọn)

        Returns:
            Dictionary chứa response từ API
        """
        return self._request("POST", endpoint, json=data, params=params)

    def _create_error_response(self, message: str) -> Dict[str, Any]:
        """
        Tạo response lỗi với định dạng nhất quán.

        Args:
            message: Thông báo lỗi

        Returns:
            Dictionary chứa thông tin lỗi theo định dạng chuẩn
        """
        return {
            "data": None,
            "message": message,
            "success": False,
            "timestamp": datetime.now().isoformat()
        }

# Lấy API_BASE_URL từ cấu hình
config = Config()

# Tạo instance mặc định của ApiClient với base_url từ cấu hình
default_client = ApiClient(base_url=config.API_BASE_URL)
