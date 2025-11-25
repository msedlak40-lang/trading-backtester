"""
Indicator tracking for visualization
Tracks swing points and ATR bars for charting
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from src.data.data_structures import Bar


@dataclass
class SwingPoint:
    """Represents a swing high or swing low point"""
    timestamp: datetime
    price: float
    bar_index: int
    swing_type: str  # 'high' or 'low'


@dataclass
class ATRBarMarker:
    """Represents an ATR bar marker"""
    timestamp: datetime
    bar_index: int
    direction: str  # 'BULLISH' or 'BEARISH'
    atr_value: float
    bar_range: float


class IndicatorTracker:
    """Tracks indicator values for visualization"""

    def __init__(self):
        self.swing_highs: List[SwingPoint] = []
        self.swing_lows: List[SwingPoint] = []
        self.atr_bars: List[ATRBarMarker] = []
        self.last_swing_high: Optional[float] = None
        self.last_swing_low: Optional[float] = None

    def update_swing_high(self, bar: Bar, bar_index: int, swing_high: float) -> None:
        """
        Update swing high tracking

        Args:
            bar: Current bar
            bar_index: Index of the bar
            swing_high: Swing high value
        """
        # Only add if swing high changed
        if swing_high != self.last_swing_high and swing_high > 0:
            self.swing_highs.append(SwingPoint(
                timestamp=bar.timestamp,
                price=swing_high,
                bar_index=bar_index,
                swing_type='high'
            ))
            self.last_swing_high = swing_high

    def update_swing_low(self, bar: Bar, bar_index: int, swing_low: float) -> None:
        """
        Update swing low tracking

        Args:
            bar: Current bar
            bar_index: Index of the bar
            swing_low: Swing low value
        """
        # Only add if swing low changed
        if swing_low != self.last_swing_low and swing_low < float('inf'):
            self.swing_lows.append(SwingPoint(
                timestamp=bar.timestamp,
                price=swing_low,
                bar_index=bar_index,
                swing_type='low'
            ))
            self.last_swing_low = swing_low

    def add_atr_bar(self, bar: Bar, bar_index: int, direction: str,
                    atr_value: float, bar_range: float) -> None:
        """
        Add ATR bar marker

        Args:
            bar: Current bar
            bar_index: Index of the bar
            direction: 'BULLISH' or 'BEARISH'
            atr_value: ATR value at this bar
            bar_range: Actual bar range
        """
        self.atr_bars.append(ATRBarMarker(
            timestamp=bar.timestamp,
            bar_index=bar_index,
            direction=direction,
            atr_value=atr_value,
            bar_range=bar_range
        ))

    def get_swing_highs(self) -> List[SwingPoint]:
        """Get all swing high points"""
        return self.swing_highs

    def get_swing_lows(self) -> List[SwingPoint]:
        """Get all swing low points"""
        return self.swing_lows

    def get_atr_bars(self) -> List[ATRBarMarker]:
        """Get all ATR bar markers"""
        return self.atr_bars

    def get_data_for_day(self, day_str: str) -> Dict:
        """
        Get all indicator data for a specific day

        Args:
            day_str: Date string in YYYY-MM-DD format

        Returns:
            Dictionary with swing highs, swing lows, and ATR bars for that day
        """
        day_swing_highs = [
            sp for sp in self.swing_highs
            if sp.timestamp.date().isoformat() == day_str
        ]
        day_swing_lows = [
            sp for sp in self.swing_lows
            if sp.timestamp.date().isoformat() == day_str
        ]
        day_atr_bars = [
            ab for ab in self.atr_bars
            if ab.timestamp.date().isoformat() == day_str
        ]

        return {
            'swing_highs': day_swing_highs,
            'swing_lows': day_swing_lows,
            'atr_bars': day_atr_bars
        }
