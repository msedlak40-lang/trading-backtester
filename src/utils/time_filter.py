"""
Time filtering utilities for market data
"""
from datetime import time
from typing import List
from src.data.data_structures import Bar


class RTHFilter:
    """Filter bars to Regular Trading Hours (RTH)"""

    def __init__(self, start_time: time = time(8, 30), end_time: time = time(15, 0)):
        """
        Initialize RTH filter

        Args:
            start_time: Start of RTH session (default 8:30 AM)
            end_time: End of RTH session (default 3:00 PM)

        Note: Times should be in CST
        """
        self.start_time = start_time
        self.end_time = end_time

    def filter_bars(self, bars: List[Bar]) -> List[Bar]:
        """
        Filter bars to only include those within RTH

        Args:
            bars: List of bars to filter

        Returns:
            List of bars within RTH hours
        """
        rth_bars = []

        for bar in bars:
            bar_time = bar.timestamp.time()

            # Check if bar is within RTH
            if self.start_time <= bar_time < self.end_time:
                rth_bars.append(bar)

        return rth_bars

    def get_trading_days(self, bars: List[Bar]) -> List[str]:
        """
        Get list of unique trading days from bars

        Args:
            bars: List of bars

        Returns:
            List of date strings (YYYY-MM-DD format)
        """
        days = set()

        for bar in bars:
            days.add(bar.timestamp.date().isoformat())

        return sorted(list(days))

    def get_bars_for_day(self, bars: List[Bar], day_str: str) -> List[Bar]:
        """
        Get all bars for a specific trading day

        Args:
            bars: List of bars (should already be RTH filtered)
            day_str: Date string in YYYY-MM-DD format

        Returns:
            List of bars for that day
        """
        day_bars = []

        for bar in bars:
            if bar.timestamp.date().isoformat() == day_str:
                day_bars.append(bar)

        return day_bars
