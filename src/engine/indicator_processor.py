"""
Indicator processor for day-by-day chart viewing
Processes Zone21B and ATR indicators on market data
"""
from typing import List, Dict
from src.data.data_structures import Bar
from src.indicators.zone21b import Zone21BIndicator
from src.indicators.atr_bar import ATRBarDetector
from src.indicators.indicator_tracker import IndicatorTracker
from src.utils.time_filter import RTHFilter


class IndicatorProcessor:
    """Process indicators for both NQ and Composite data"""

    def __init__(self, zone21_lookback: int = 4, atr_period: int = 7, atr_multiple: float = 0.75):
        """
        Initialize indicator processor

        Args:
            zone21_lookback: Lookback period for Zone21B swing calculation
            atr_period: Period for ATR calculation
            atr_multiple: Multiple for ATR bar threshold
        """
        self.zone21_lookback = zone21_lookback
        self.atr_period = atr_period
        self.atr_multiple = atr_multiple

        # RTH filter (8:30 AM - 3:00 PM CST)
        self.rth_filter = RTHFilter()

    def process_data(self, nq_bars: List[Bar], composite_bars: List[Bar]) -> Dict:
        """
        Process all data and return indicator results

        Args:
            nq_bars: NQ bars (full dataset)
            composite_bars: Composite bars (full dataset)

        Returns:
            Dictionary containing:
                - nq_rth_bars: NQ bars filtered to RTH
                - composite_rth_bars: Composite bars filtered to RTH
                - nq_indicators: IndicatorTracker for NQ
                - composite_indicators: IndicatorTracker for Composite
                - trading_days: List of trading days
        """
        print("\n" + "="*80)
        print("PROCESSING INDICATORS FOR DAY-BY-DAY VIEWING")
        print("="*80)

        # Filter to RTH
        print("\nFiltering to Regular Trading Hours (8:30 AM - 3:00 PM CST)...")
        nq_rth_bars = self.rth_filter.filter_bars(nq_bars)
        composite_rth_bars = self.rth_filter.filter_bars(composite_bars)

        print(f"  NQ: {len(nq_bars):,} total bars -> {len(nq_rth_bars):,} RTH bars")
        print(f"  Composite: {len(composite_bars):,} total bars -> {len(composite_rth_bars):,} RTH bars")

        # Get trading days
        trading_days = self.rth_filter.get_trading_days(nq_rth_bars)
        print(f"\nTrading days: {len(trading_days)}")
        print(f"  First day: {trading_days[0]}")
        print(f"  Last day: {trading_days[-1]}")

        # Process NQ indicators
        print("\nProcessing NQ indicators...")
        nq_indicators = self._process_instrument(nq_rth_bars, "NQ")

        # Process Composite indicators
        print("\nProcessing Composite indicators...")
        composite_indicators = self._process_instrument(composite_rth_bars, "Composite")

        print("\n" + "="*80)
        print("INDICATOR PROCESSING COMPLETE")
        print("="*80)

        return {
            'nq_rth_bars': nq_rth_bars,
            'composite_rth_bars': composite_rth_bars,
            'nq_indicators': nq_indicators,
            'composite_indicators': composite_indicators,
            'trading_days': trading_days
        }

    def _process_instrument(self, bars: List[Bar], name: str) -> IndicatorTracker:
        """
        Process Zone21B and ATR indicators for a single instrument

        Args:
            bars: Bar data
            name: Instrument name (for logging)

        Returns:
            IndicatorTracker with all indicator data
        """
        # Initialize indicators
        zone21 = Zone21BIndicator(lookback=self.zone21_lookback)
        atr_detector = ATRBarDetector(period=self.atr_period, multiple=self.atr_multiple)
        tracker = IndicatorTracker()

        # Process each bar
        for idx, bar in enumerate(bars):
            # Update Zone21B
            zone21.on_bar(bar)

            # Track swing changes
            swing_high = zone21.get_current_swing_high()
            swing_low = zone21.get_current_swing_low()

            if swing_high is not None:
                tracker.update_swing_high(bar, idx, swing_high)

            if swing_low is not None:
                tracker.update_swing_low(bar, idx, swing_low)

            # Update ATR detector
            atr_bar_type = atr_detector.on_bar(bar)

            # Track ATR bars
            if atr_bar_type:
                atr_value = atr_detector.get_current_atr()
                bar_range = abs(bar.close - bar.open)
                tracker.add_atr_bar(bar, idx, atr_bar_type, atr_value, bar_range)

        # Summary
        print(f"  {name}:")
        print(f"    Swing Highs: {len(tracker.get_swing_highs())}")
        print(f"    Swing Lows: {len(tracker.get_swing_lows())}")
        print(f"    ATR Bars: {len(tracker.get_atr_bars())}")

        return tracker
