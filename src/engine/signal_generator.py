"""
Signal Generator - Detects divergences and generates entry signals.

Divergence Logic:
1. Bearish Divergence (Short Setup):
   - NQ makes new swing high (Close > prior swing high)
   - Composite does NOT make new swing high
   - Wait for NQ to make ANOTHER new swing high
   - ATR bar must occur within max_bars_after_swing

2. Bullish Divergence (Long Setup):
   - NQ makes new swing low (Close < prior swing low)
   - Composite does NOT make new swing low
   - Wait for NQ to make ANOTHER new swing low
   - ATR bar must occur within max_bars_after_swing
"""
from typing import Optional, Dict, List
from src.data.data_structures import Bar, DivergenceState
from src.indicators.zone21b import Zone21BIndicator
from src.indicators.atr_bar import ATRBarDetector


class SignalGenerator:
    """
    Generates entry signals based on divergence detection and ATR bars.
    """

    def __init__(self, config: dict):
        """
        Initialize signal generator with configuration.

        Args:
            config: Configuration dictionary with zone21b, atr_bar, and entry settings
        """
        # Initialize indicators for NQ
        self.zone_nq = Zone21BIndicator(
            lookback=config['zone21b']['lookback'],
            required_closes=config['zone21b']['required_closes']
        )

        # Initialize indicators for composite
        self.zone_composite = Zone21BIndicator(
            lookback=config['zone21b']['lookback'],
            required_closes=config['zone21b']['required_closes']
        )

        # Initialize ATR bar detector (uses NQ bars)
        self.atr_detector = ATRBarDetector(
            period=config['atr_bar']['period'],
            multiple=config['atr_bar']['multiple']
        )

        # Entry settings
        self.max_bars_after_swing = config['entry']['max_bars_after_swing']

        # Divergence tracking
        self.divergence = DivergenceState()

        # Track previous swing values for divergence detection
        self.prev_nq_swing_high = None
        self.prev_nq_swing_low = None
        self.prev_comp_swing_high = None
        self.prev_comp_swing_low = None

        # Debug settings
        self.debug = config.get('debug', {})
        self.show_divergences = self.debug.get('show_divergences', False)
        self.show_swing_updates = self.debug.get('show_swing_updates', False)
        self.show_atr_bars = self.debug.get('show_atr_bars', False)

        # Divergence log
        self.divergence_log: List[Dict] = []

    def process_bar(self, nq_bar: Bar, composite_bar: Bar, bar_index: int) -> Optional[Dict]:
        """
        Process bars from both NQ and composite.
        Detect divergences and generate entry signals.

        Args:
            nq_bar: NQ futures bar
            composite_bar: Composite bar
            bar_index: Current bar index

        Returns:
            Signal dictionary if entry condition met, None otherwise
            Signal format: {
                'type': 'LONG' or 'SHORT',
                'bar_index': int,
                'entry_price': float,
                'atr': float,
                'reason': str
            }
        """
        # Update indicators
        self.zone_nq.on_bar(nq_bar)
        self.zone_composite.on_bar(composite_bar)
        atr_bar_type = self.atr_detector.on_bar(nq_bar)

        # Debug: Show ATR bars
        if self.show_atr_bars and atr_bar_type:
            print(f"  ATR Bar: {atr_bar_type} @ {nq_bar.timestamp} - Price: {nq_bar.close:.2f}")

        # Check for new divergence
        self._check_for_divergence(nq_bar, composite_bar, bar_index)

        # If divergence is active, check for entry signal
        if self.divergence.active:
            signal = self._check_for_entry_signal(
                nq_bar, composite_bar, bar_index, atr_bar_type
            )
            if signal:
                # Reset divergence after signal
                self.divergence = DivergenceState()
                return signal

        return None

    def _check_for_divergence(self, nq_bar: Bar, comp_bar: Bar, bar_index: int) -> None:
        """
        Check if a divergence has formed.

        Bearish Divergence: NQ makes new high, composite doesn't
        Bullish Divergence: NQ makes new low, composite doesn't
        """
        # Get current swing values
        nq_swing_high = self.zone_nq.get_current_swing_high()
        nq_swing_low = self.zone_nq.get_current_swing_low()
        comp_swing_high = self.zone_composite.get_current_swing_high()
        comp_swing_low = self.zone_composite.get_current_swing_low()

        # Check for BEARISH divergence (short setup)
        # NQ makes new high, composite doesn't
        if nq_swing_high and comp_swing_high:
            # NQ broke above its swing high
            if nq_bar.close > nq_swing_high:
                # Composite did NOT break above its swing high
                if comp_bar.close <= comp_swing_high:
                    # New bearish divergence detected
                    if not self.divergence.active or self.divergence.type != 'BEARISH':
                        self.divergence = DivergenceState(
                            active=True,
                            type='BEARISH',
                            nq_swing_value=nq_swing_high,
                            composite_swing_value=comp_swing_high,
                            bars_since_new_swing=0,
                            new_swing_detected=False
                        )

                        # Log divergence
                        div_info = {
                            'bar_index': bar_index,
                            'timestamp': nq_bar.timestamp,
                            'type': 'BEARISH',
                            'nq_close': nq_bar.close,
                            'nq_swing_high': nq_swing_high,
                            'comp_close': comp_bar.close,
                            'comp_swing_high': comp_swing_high,
                            'status': 'DETECTED'
                        }
                        self.divergence_log.append(div_info)

                        if self.show_divergences:
                            print(f"\n>>> BEARISH DIVERGENCE DETECTED @ {nq_bar.timestamp}")
                            print(f"    NQ Close: {nq_bar.close:.2f} > Swing High: {nq_swing_high:.2f}")
                            print(f"    Composite Close: {comp_bar.close:.2f} <= Swing High: {comp_swing_high:.2f}")
                            print(f"    Waiting for 2nd swing confirmation...")

        # Check for BULLISH divergence (long setup)
        # NQ makes new low, composite doesn't
        if nq_swing_low and comp_swing_low:
            # NQ broke below its swing low
            if nq_bar.close < nq_swing_low:
                # Composite did NOT break below its swing low
                if comp_bar.close >= comp_swing_low:
                    # New bullish divergence detected
                    if not self.divergence.active or self.divergence.type != 'BULLISH':
                        self.divergence = DivergenceState(
                            active=True,
                            type='BULLISH',
                            nq_swing_value=nq_swing_low,
                            composite_swing_value=comp_swing_low,
                            bars_since_new_swing=0,
                            new_swing_detected=False
                        )

                        # Log divergence
                        div_info = {
                            'bar_index': bar_index,
                            'timestamp': nq_bar.timestamp,
                            'type': 'BULLISH',
                            'nq_close': nq_bar.close,
                            'nq_swing_low': nq_swing_low,
                            'comp_close': comp_bar.close,
                            'comp_swing_low': comp_swing_low,
                            'status': 'DETECTED'
                        }
                        self.divergence_log.append(div_info)

                        if self.show_divergences:
                            print(f"\n>>> BULLISH DIVERGENCE DETECTED @ {nq_bar.timestamp}")
                            print(f"    NQ Close: {nq_bar.close:.2f} < Swing Low: {nq_swing_low:.2f}")
                            print(f"    Composite Close: {comp_bar.close:.2f} >= Swing Low: {comp_swing_low:.2f}")
                            print(f"    Waiting for 2nd swing confirmation...")

    def _check_for_entry_signal(self, nq_bar: Bar, comp_bar: Bar,
                                bar_index: int, atr_bar_type: Optional[str]) -> Optional[Dict]:
        """
        Check if entry conditions are met after divergence.

        After divergence, we need:
        1. NQ to make ANOTHER new swing high/low (second confirmation)
        2. ATR bar of correct type within max_bars_after_swing window
        """
        # Check if NQ makes a new swing (after initial divergence)
        if self.divergence.type == 'BEARISH':
            # For bearish divergence, need NQ to make another new high
            nq_swing = self.zone_nq.get_current_swing_high()
            if nq_swing and nq_bar.close > nq_swing:
                # NQ made a new swing high
                if not self.divergence.new_swing_detected:
                    self.divergence.new_swing_detected = True
                    self.divergence.bars_since_new_swing = 0

                    if self.show_divergences:
                        print(f"    ✓ 2ND SWING CONFIRMED @ {nq_bar.timestamp}")
                        print(f"      NQ: {nq_bar.close:.2f} > {nq_swing:.2f}")
                        print(f"      Looking for BEARISH ATR bar within {self.max_bars_after_swing} bars...")

        elif self.divergence.type == 'BULLISH':
            # For bullish divergence, need NQ to make another new low
            nq_swing = self.zone_nq.get_current_swing_low()
            if nq_swing and nq_bar.close < nq_swing:
                # NQ made a new swing low
                if not self.divergence.new_swing_detected:
                    self.divergence.new_swing_detected = True
                    self.divergence.bars_since_new_swing = 0

                    if self.show_divergences:
                        print(f"    ✓ 2ND SWING CONFIRMED @ {nq_bar.timestamp}")
                        print(f"      NQ: {nq_bar.close:.2f} < {nq_swing:.2f}")
                        print(f"      Looking for BULLISH ATR bar within {self.max_bars_after_swing} bars...")

        # If new swing detected, increment bar counter
        if self.divergence.new_swing_detected:
            self.divergence.bars_since_new_swing += 1

            # Check if within window and ATR bar occurred
            if self.divergence.bars_since_new_swing <= self.max_bars_after_swing:
                # Check for correct ATR bar type
                if self.divergence.type == 'BEARISH' and atr_bar_type == 'BEARISH':
                    if self.show_divergences:
                        print(f"    ✓✓ BEARISH ATR BAR FOUND @ {nq_bar.timestamp}")
                        print(f"       ENTRY SIGNAL GENERATED!")
                    # Short entry signal
                    return {
                        'type': 'SHORT',
                        'bar_index': bar_index,
                        'entry_price': nq_bar.close,
                        'atr': self.atr_detector.get_current_atr(),
                        'reason': 'Bearish divergence + Bearish ATR bar'
                    }
                elif self.divergence.type == 'BULLISH' and atr_bar_type == 'BULLISH':
                    if self.show_divergences:
                        print(f"    ✓✓ BULLISH ATR BAR FOUND @ {nq_bar.timestamp}")
                        print(f"       ENTRY SIGNAL GENERATED!")
                    # Long entry signal
                    return {
                        'type': 'LONG',
                        'bar_index': bar_index,
                        'entry_price': nq_bar.close,
                        'atr': self.atr_detector.get_current_atr(),
                        'reason': 'Bullish divergence + Bullish ATR bar'
                    }

            # If exceeded window without ATR bar, reset divergence
            if self.divergence.bars_since_new_swing > self.max_bars_after_swing:
                if self.show_divergences:
                    print(f"    ✗ ATR bar window EXPIRED @ {nq_bar.timestamp}")
                    print(f"      Divergence reset (no ATR bar within {self.max_bars_after_swing} bars)\n")
                self.divergence = DivergenceState()

        return None

    def get_atr_detector(self) -> ATRBarDetector:
        """Get the ATR detector instance (for target calculation)."""
        return self.atr_detector

    def get_divergence_state(self) -> DivergenceState:
        """Get current divergence state."""
        return self.divergence

    def get_divergence_log(self) -> List[Dict]:
        """Get the divergence log."""
        return self.divergence_log

    def save_divergence_log(self, filepath: str) -> None:
        """Save divergence log to CSV file."""
        if not self.divergence_log:
            print(f"No divergences detected to save.")
            return

        with open(filepath, 'w') as f:
            # Write header
            f.write("bar_index,timestamp,type,nq_close,nq_swing,comp_close,comp_swing,status\n")

            # Write divergences
            for div in self.divergence_log:
                if div['type'] == 'BEARISH':
                    f.write(f"{div['bar_index']},{div['timestamp']},{div['type']},"
                           f"{div['nq_close']},{div['nq_swing_high']},"
                           f"{div['comp_close']},{div['comp_swing_high']},"
                           f"{div['status']}\n")
                else:  # BULLISH
                    f.write(f"{div['bar_index']},{div['timestamp']},{div['type']},"
                           f"{div['nq_close']},{div['nq_swing_low']},"
                           f"{div['comp_close']},{div['comp_swing_low']},"
                           f"{div['status']}\n")

        print(f"Divergence log saved to: {filepath}")
