"""
    Error model from CC API response.
"""
from typing import TypedDict


class Error(TypedDict):
    message: str
    code: int
    status: int
