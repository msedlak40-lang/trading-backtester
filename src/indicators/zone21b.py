"""
Zone21B Indicator - Complex state machine for detecting setups and zones.
Based on Zone21B2.cs from NinjaTrader.

This indicator tracks a sequential bar pattern that leads to zone formation:
1. downBarOne: Close < Open
2. downBarTwo: Close < downBarOneLow (triggers swing calculation)
3. downWithinBar: Close < Open AND Close < downBarTwoLow
4. down4thBar: Close < downWithinLow
5. takeBarHigh: Close > downBarTwoHigh (or downWithinHigh)
6. takeSwingHigh: Close > swingHigh
7. zetaBar: Both takeBarHigh AND takeSwingHigh
8. buyZone: After requiredCloses above zetaBar
"""
from typing import List, Optional
from src.data.data_structures import Bar, Zone21State


class Zone21BIndicator:
    """
    Zone21B indicator with complete state machine.
    Implements buy side (downward pattern) and sell side (upward pattern).
    """

    def __init__(self, lookback: int = 4, required_closes: int = 2):
        """
        Initialize Zone21B indicator.

        Args:
            lookback: Bars to look back for swing high/low calculation
            required_closes: Number of closes above zeta/below alpha to activate zone
        """
        self.lookback = lookback
        self.required_closes = required_closes
        self.state = Zone21State()
        self.bars: List[Bar] = []

    def on_bar(self, bar: Bar) -> None:
        """
        Process a new bar and update state machine.
        This implements the exact logic from Zone21B2.cs OnBarUpdate()
        """
        self.bars.append(bar)
        current_idx = len(self.bars) - 1

        # Need at least 10 bars to start (from Zone21B2.cs line 374)
        if current_idx < 10:
            return

        # Process buy side (downward pattern for buy setup)
        self._process_buy_side(bar, current_idx)

        # Process sell side (upward pattern for sell setup)
        self._process_sell_side(bar, current_idx)

    def _process_buy_side(self, bar: Bar, idx: int) -> None:
        """Process buy side logic (downward pattern leading to buy zone)."""

        # Update running low tracking
        if self.state.running_low != float('inf'):
            if not self.state.i_bar_3_down:
                if bar.low < self.state.running_low:
                    self.state.running_low = bar.low

        # BAR 1: Look for first down bar
        if not self.state.down_bar_one:
            if not self.state.under_bar:
                if bar.close < bar.open:
                    self.state.down_bar_one = True
                    self.state.down_bar_one_high = bar.high
                    self.state.down_bar_one_low = bar.low
                    # Calculate swing high (Zone21B2.cs line 485)
                    self._calculate_swing_high(idx)

        # If we have bar one, look for subsequent bars
        else:
            # BAR 2: Look for second down bar
            if not self.state.down_bar_two:
                # Reset if price breaks above bar one high
                if bar.close > self.state.down_bar_one_high:
                    self.state.down_bar_one = False
                    return

                # Create bar two if close below bar one low
                if not self.state.under_bar:
                    if bar.close < self.state.down_bar_one_low:
                        self.state.down_bar_two = True
                        self.state.down_bar_two_high = bar.high
                        self.state.down_bar_two_low = bar.low
                        # Set running low (Zone21B2.cs line 508)
                        self.state.running_low = bar.low
                        # Calculate swing high
                        self._calculate_swing_high(idx)

            # After bar two, process the rest of the pattern
            else:
                # Check for takeBarHigh (Zone21B2.cs lines 518-525)
                if not self.state.take_bar_high:
                    if bar.close > self.state.down_bar_two_high and not self.state.down_within_bar:
                        self.state.take_bar_high = True

                # Check for takeSwingHigh (Zone21B2.cs lines 534-545)
                if not self.state.take_swing_high:
                    if bar.close > self.state.swing_high and self.state.swing_high != 0:
                        self.state.take_swing_high = True

                # BAR 3: Look for within bar (Zone21B2.cs lines 552-566)
                if not self.state.down_within_bar:
                    if not self.state.under_bar:
                        if bar.close < bar.open and bar.close < self.state.down_bar_two_low:
                            self.state.down_within_bar = True
                            self.state.down_within_high = bar.high
                            self.state.down_within_low = bar.low

                # After within bar, check for takeBarHigh again
                else:
                    if not self.state.take_bar_high:
                        if bar.close > self.state.down_within_high:
                            self.state.take_bar_high = True

                    # BAR 4: Look for 4th bar (simplified version)
                    if not self.state.down_4th_bar:
                        if bar.close < self.state.down_within_low or self.state.lower_low:
                            self.state.down_4th_bar = True
                            self.state.down_4th_bar_high = bar.high
                            self.state.down_4th_bar_low = bar.low
                            self.state.stored_4th_low = bar.low

                # ZETA BAR: Check if both conditions met (Zone21B2.cs lines 596-613)
                if self.state.take_bar_high and self.state.take_swing_high:
                    self.state.zeta_bar = True
                    self.state.zeta_bar_high = bar.high
                    self.state.zeta_bar_low = bar.low
                    self.state.zeta_bar_close = bar.close
                    self.state.stored_swing_high = self.state.swing_high
                    self.state.possible_low = self.state.running_low
                    self.state.closes_above_z = 1
                    # Reset switches
                    self._reset_buy_side_switches()

        # Process zeta bar logic
        if self.state.zeta_bar:
            if not self.state.zeta_bar_ft:
                # Check if failed (broke below zeta low)
                if bar.close < self.state.zeta_bar_low:
                    self.state.zeta_bar = False
                    return

                # Count closes above zeta high
                if bar.close > self.state.zeta_bar_high:
                    self.state.closes_above_z += 1

                # Activate buy zone after required closes (Zone21B2.cs lines 673-700)
                if self.state.closes_above_z == self.required_closes:
                    self.state.buy_zone = True
                    self.state.buy_zone_high = self.state.stored_swing_high
                    self.state.buy_zone_low = self.state.possible_low
                    self.state.buy_zone_count = 0
                    self.state.running_low = float('inf')
                    self.state.zeta_bar = False

                # Quick fix for closes_above_z overflow
                if self.state.closes_above_z == self.required_closes + 1:
                    self.state.zeta_bar = False
                    self.state.running_low = float('inf')

    def _process_sell_side(self, bar: Bar, idx: int) -> None:
        """Process sell side logic (upward pattern leading to sell zone)."""

        # Update running high tracking
        if self.state.running_high != 0:
            if not self.state.i_bar_3_up:
                if bar.high > self.state.running_high:
                    self.state.running_high = bar.high

        # BAR 1: Look for first up bar
        if not self.state.up_bar_one:
            if not self.state.over_bar:
                if bar.close > bar.open:
                    self.state.up_bar_one = True
                    self.state.up_bar_one_high = bar.high
                    self.state.up_bar_one_low = bar.low
                    # Calculate swing low
                    self._calculate_swing_low(idx)

        # If we have bar one, look for subsequent bars
        else:
            # BAR 2: Look for second up bar
            if not self.state.up_bar_two:
                # Reset if price breaks below bar one low
                if bar.close < self.state.up_bar_one_low:
                    self.state.up_bar_one = False
                    return

                # Create bar two if close above bar one high
                if not self.state.over_bar:
                    if bar.close > self.state.up_bar_one_high:
                        self.state.up_bar_two = True
                        self.state.up_bar_two_high = bar.high
                        self.state.up_bar_two_low = bar.low
                        # Set running high
                        self.state.running_high = bar.high
                        # Calculate swing low
                        self._calculate_swing_low(idx)

            # After bar two, process the rest of the pattern
            else:
                # Check for takeBarLow
                if not self.state.take_bar_low:
                    if bar.close < self.state.up_bar_two_low and not self.state.up_within_bar:
                        self.state.take_bar_low = True

                # Check for takeSwingLow
                if not self.state.take_swing_low:
                    if bar.close < self.state.swing_low and self.state.swing_low != float('inf'):
                        self.state.take_swing_low = True

                # BAR 3: Look for within bar
                if not self.state.up_within_bar:
                    if not self.state.over_bar:
                        if bar.close > bar.open and bar.close > self.state.up_bar_two_high:
                            self.state.up_within_bar = True
                            self.state.up_within_high = bar.high
                            self.state.up_within_low = bar.low

                # After within bar, check for takeBarLow again
                else:
                    if not self.state.take_bar_low:
                        if bar.close < self.state.up_within_low:
                            self.state.take_bar_low = True

                    # BAR 4: Look for 4th bar
                    if not self.state.up_4th_bar:
                        if bar.close > self.state.up_within_high or self.state.higher_high:
                            self.state.up_4th_bar = True
                            self.state.up_4th_bar_high = bar.high
                            self.state.up_4th_bar_low = bar.low
                            self.state.stored_4th_high = bar.high

                # ALPHA BAR: Check if both conditions met
                if self.state.take_bar_low and self.state.take_swing_low:
                    self.state.alpha_bar = True
                    self.state.alpha_bar_high = bar.high
                    self.state.alpha_bar_low = bar.low
                    self.state.alpha_bar_close = bar.close
                    self.state.stored_swing_low = self.state.swing_low
                    self.state.possible_high = self.state.running_high
                    self.state.closes_below_a = 1
                    # Reset switches
                    self._reset_sell_side_switches()

        # Process alpha bar logic
        if self.state.alpha_bar:
            if not self.state.alpha_bar_ft:
                # Check if failed (broke above alpha high)
                if bar.close > self.state.alpha_bar_high:
                    self.state.alpha_bar = False
                    return

                # Count closes below alpha low
                if bar.close < self.state.alpha_bar_low:
                    self.state.closes_below_a += 1

                # Activate sell zone after required closes
                if self.state.closes_below_a == self.required_closes:
                    self.state.sell_zone = True
                    self.state.sell_zone_high = self.state.possible_high
                    self.state.sell_zone_low = self.state.stored_swing_low
                    self.state.sell_zone_count = 0
                    self.state.running_high = 0
                    self.state.alpha_bar = False

                # Quick fix for closes_below_a overflow
                if self.state.closes_below_a == self.required_closes + 1:
                    self.state.alpha_bar = False
                    self.state.running_high = 0

    def _calculate_swing_high(self, current_idx: int) -> None:
        """
        Calculate swing high by looking back 'lookback' bars.
        From Zone21B2.cs - finds highest high in lookback period.
        """
        if current_idx < self.lookback:
            return

        # Look back 'lookback' bars from current position
        start_idx = max(0, current_idx - self.lookback)
        lookback_bars = self.bars[start_idx:current_idx + 1]

        if lookback_bars:
            highest_high = max(bar.high for bar in lookback_bars)
            self.state.swing_high = highest_high
            self.state.swing_high_bars = self.lookback

    def _calculate_swing_low(self, current_idx: int) -> None:
        """
        Calculate swing low by looking back 'lookback' bars.
        Mirror of swing high calculation for sell side.
        """
        if current_idx < self.lookback:
            return

        # Look back 'lookback' bars from current position
        start_idx = max(0, current_idx - self.lookback)
        lookback_bars = self.bars[start_idx:current_idx + 1]

        if lookback_bars:
            lowest_low = min(bar.low for bar in lookback_bars)
            self.state.swing_low = lowest_low
            self.state.swing_low_bars = self.lookback

    def _reset_buy_side_switches(self) -> None:
        """Reset all buy side state flags."""
        self.state.down_bar_one = False
        self.state.down_bar_two = False
        self.state.down_within_bar = False
        self.state.down_4th_bar = False
        self.state.take_bar_high = False
        self.state.take_swing_high = False
        self.state.under_bar = False
        self.state.i_bar_1_down = False
        self.state.i_bar_2_down = False
        self.state.i_bar_3_down = False

    def _reset_sell_side_switches(self) -> None:
        """Reset all sell side state flags."""
        self.state.up_bar_one = False
        self.state.up_bar_two = False
        self.state.up_within_bar = False
        self.state.up_4th_bar = False
        self.state.take_bar_low = False
        self.state.take_swing_low = False
        self.state.over_bar = False
        self.state.i_bar_1_up = False
        self.state.i_bar_2_up = False
        self.state.i_bar_3_up = False

    def get_current_swing_high(self) -> Optional[float]:
        """Get current swing high value if set."""
        if self.state.swing_high == 0:
            return None
        return self.state.swing_high

    def get_current_swing_low(self) -> Optional[float]:
        """Get current swing low value if set."""
        if self.state.swing_low == float('inf'):
            return None
        return self.state.swing_low

    def has_new_swing_high(self, bar: Bar) -> bool:
        """Check if current bar makes a new swing high."""
        swing = self.get_current_swing_high()
        if swing is None:
            return False
        return bar.close > swing

    def has_new_swing_low(self, bar: Bar) -> bool:
        """Check if current bar makes a new swing low."""
        swing = self.get_current_swing_low()
        if swing is None:
            return False
        return bar.close < swing

    def is_buy_zone_active(self) -> bool:
        """Check if buy zone is currently active."""
        return self.state.buy_zone

    def is_sell_zone_active(self) -> bool:
        """Check if sell zone is currently active."""
        return self.state.sell_zone

    def get_buy_zone_range(self) -> Optional[tuple]:
        """Get buy zone high and low if active."""
        if self.state.buy_zone:
            return (self.state.buy_zone_high, self.state.buy_zone_low)
        return None

    def get_sell_zone_range(self) -> Optional[tuple]:
        """Get sell zone high and low if active."""
        if self.state.sell_zone:
            return (self.state.sell_zone_high, self.state.sell_zone_low)
        return None
