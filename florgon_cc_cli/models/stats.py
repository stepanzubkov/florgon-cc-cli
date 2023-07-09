"""
    Stats model for url and paste stats.
"""
from typing import TypedDict, Dict, NotRequired


class Views(TypedDict):
    total: int
    by_refferers: NotRequired[Dict[str, int]]
    by_dates: NotRequired[Dict[str, int]]


class Stats(TypedDict):
    views: Views
