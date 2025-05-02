"""
Module API cho Admission Advisor.
Cung cấp các hàm và lớp để tương tác với API backend.
"""

from .client import ApiClient, default_client

__all__ = [
    'ApiClient',
    'default_client',
]
