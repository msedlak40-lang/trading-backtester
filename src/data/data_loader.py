"""
Data loader for NinjaTrader format files.
Handles parsing, alignment, and composite calculation.
"""
from datetime import datetime
from typing import List, Dict, Tuple
from pathlib import Path
from src.data.data_structures import Bar


class DataLoader:
    """Loads and processes market data from NinjaTrader format files."""

    def __init__(self, base_path: str = "."):
        """Initialize data loader with base path for data files."""
        self.base_path = Path(base_path)

    def load_file(self, filename: str) -> List[Bar]:
        """
        Load a single NinjaTrader format file.
        Format: YYYYMMDDhhmmss;Open;High;Low;Close;Volume

        Args:
            filename: Name of the file to load

        Returns:
            List of Bar objects sorted by timestamp
        """
        filepath = self.base_path / filename
        bars = []

        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    parts = line.split(';')
                    if len(parts) != 6:
                        print(f"Warning: Skipping malformed line {line_num} in {filename}")
                        continue

                    # Parse datetime: YYYYMMDDhhmmss with space separator
                    # Example: "20250914 220100"
                    timestamp_str = parts[0].strip()
                    # Handle both formats: with and without space
                    timestamp_str = timestamp_str.replace(' ', '')

                    if len(timestamp_str) != 14:
                        print(f"Warning: Invalid timestamp format at line {line_num}: {timestamp_str}")
                        continue

                    year = int(timestamp_str[0:4])
                    month = int(timestamp_str[4:6])
                    day = int(timestamp_str[6:8])
                    hour = int(timestamp_str[8:10])
                    minute = int(timestamp_str[10:12])
                    second = int(timestamp_str[12:14])

                    timestamp = datetime(year, month, day, hour, minute, second)

                    # Parse OHLCV
                    open_price = float(parts[1])
                    high = float(parts[2])
                    low = float(parts[3])
                    close = float(parts[4])
                    volume = int(parts[5])

                    bar = Bar(
                        timestamp=timestamp,
                        open=open_price,
                        high=high,
                        low=low,
                        close=close,
                        volume=volume
                    )
                    bars.append(bar)

                except (ValueError, IndexError) as e:
                    print(f"Error parsing line {line_num} in {filename}: {e}")
                    continue

        # Sort by timestamp to ensure chronological order
        bars.sort(key=lambda b: b.timestamp)
        return bars

    def load_multiple_files(self, filenames: List[str]) -> Dict[str, List[Bar]]:
        """
        Load multiple files and return a dictionary mapping filename to bars.

        Args:
            filenames: List of filenames to load

        Returns:
            Dictionary mapping filename to list of bars
        """
        result = {}
        for filename in filenames:
            print(f"Loading {filename}...")
            bars = self.load_file(filename)
            result[filename] = bars
            print(f"  Loaded {len(bars)} bars")
        return result

    def align_timestamps(self, bars_dict: Dict[str, List[Bar]]) -> Dict[str, List[Bar]]:
        """
        Align all instruments to common timestamps.
        Keeps only bars that exist in ALL instruments.

        Args:
            bars_dict: Dictionary mapping instrument name to list of bars

        Returns:
            Dictionary with aligned bars (same timestamps across all instruments)
        """
        if not bars_dict:
            return {}

        # Get all unique timestamps from all instruments
        all_timestamps = {}
        for name, bars in bars_dict.items():
            timestamp_set = {bar.timestamp for bar in bars}
            all_timestamps[name] = timestamp_set

        # Find common timestamps (intersection)
        common_timestamps = set.intersection(*all_timestamps.values())
        print(f"\nTimestamp alignment:")
        print(f"  Total unique timestamps across all instruments: {sum(len(ts) for ts in all_timestamps.values())}")
        print(f"  Common timestamps (intersection): {len(common_timestamps)}")

        # Filter each instrument to only include common timestamps
        aligned = {}
        for name, bars in bars_dict.items():
            # Create a mapping of timestamp to bar for quick lookup
            timestamp_to_bar = {bar.timestamp: bar for bar in bars}

            # Keep only bars with common timestamps, sorted
            aligned_bars = [
                timestamp_to_bar[ts]
                for ts in sorted(common_timestamps)
                if ts in timestamp_to_bar
            ]
            aligned[name] = aligned_bars
            print(f"  {name}: {len(bars)} -> {len(aligned_bars)} bars")

        return aligned

    def calculate_composite(self, stock_bars_dict: Dict[str, List[Bar]],
                           stock_order: List[str]) -> List[Bar]:
        """
        Calculate composite bars from 7 stocks using EXACT logic from TBNVolumeV3.cs

        From TBNVolumeV3.cs lines 105-108:
        Open = sum of all opens
        High = Stock[0].High + Stock[1-6].Low  (!!!)
        Low = Stock[0].Low + Stock[1-6].High  (!!!)
        Close = sum of all closes

        This is the EXACT implementation from the reference code.

        Args:
            stock_bars_dict: Dictionary of stock name to aligned bars
            stock_order: Order of stocks (first stock treated differently)

        Returns:
            List of composite bars
        """
        if len(stock_order) != 7:
            raise ValueError("Composite requires exactly 7 stocks")

        # Verify all stocks have the same number of bars
        num_bars = len(stock_bars_dict[stock_order[0]])
        for stock in stock_order[1:]:
            if len(stock_bars_dict[stock]) != num_bars:
                raise ValueError(f"All stocks must have same number of bars. "
                               f"{stock_order[0]} has {num_bars}, {stock} has {len(stock_bars_dict[stock])}")

        composite_bars = []

        for i in range(num_bars):
            # Get bars for all stocks at index i
            bars = [stock_bars_dict[stock][i] for stock in stock_order]

            # Verify timestamps match
            timestamp = bars[0].timestamp
            if not all(bar.timestamp == timestamp for bar in bars):
                raise ValueError(f"Timestamp mismatch at index {i}")

            # Calculate composite OHLC using EXACT logic from TBNVolumeV3.cs
            # Line 105: Open = sum of all opens
            composite_open = sum(bar.open for bar in bars)

            # Line 106: High = Stock[0].High + Stock[1-6].Low
            composite_high = bars[0].high + sum(bar.low for bar in bars[1:])

            # Line 107: Low = Stock[0].Low + Stock[1-6].High
            composite_low = bars[0].low + sum(bar.high for bar in bars[1:])

            # Line 108: Close = sum of all closes
            composite_close = sum(bar.close for bar in bars)

            # Volume = sum of all volumes
            composite_volume = sum(bar.volume for bar in bars)

            composite_bar = Bar(
                timestamp=timestamp,
                open=composite_open,
                high=composite_high,
                low=composite_low,
                close=composite_close,
                volume=composite_volume
            )
            composite_bars.append(composite_bar)

        return composite_bars

    def load_all_data(self, nq_file: str, stock_files: List[str]) -> Tuple[List[Bar], List[Bar]]:
        """
        Load NQ futures and calculate composite from stocks.
        Returns aligned data ready for backtesting.

        Args:
            nq_file: NQ futures data file
            stock_files: List of 7 stock data files in order

        Returns:
            Tuple of (nq_bars, composite_bars) with aligned timestamps
        """
        print("=" * 60)
        print("LOADING DATA")
        print("=" * 60)

        # Load all files
        all_files = [nq_file] + stock_files
        all_bars = self.load_multiple_files(all_files)

        # Align timestamps
        print("\n" + "=" * 60)
        print("ALIGNING TIMESTAMPS")
        print("=" * 60)
        aligned_bars = self.align_timestamps(all_bars)

        # Extract NQ bars
        nq_bars = aligned_bars[nq_file]

        # Calculate composite from stocks
        print("\n" + "=" * 60)
        print("CALCULATING COMPOSITE")
        print("=" * 60)
        stock_bars_dict = {stock: aligned_bars[stock] for stock in stock_files}
        composite_bars = self.calculate_composite(stock_bars_dict, stock_files)

        print(f"  Composite bars created: {len(composite_bars)}")
        print(f"  First bar timestamp: {composite_bars[0].timestamp}")
        print(f"  Last bar timestamp: {composite_bars[-1].timestamp}")

        # Verify alignment
        if len(nq_bars) != len(composite_bars):
            raise ValueError(f"NQ bars ({len(nq_bars)}) != Composite bars ({len(composite_bars)})")

        for i, (nq_bar, comp_bar) in enumerate(zip(nq_bars, composite_bars)):
            if nq_bar.timestamp != comp_bar.timestamp:
                raise ValueError(f"Timestamp mismatch at index {i}")

        print("\n" + "=" * 60)
        print(f"DATA LOADING COMPLETE: {len(nq_bars)} aligned bars")
        print("=" * 60)

        return nq_bars, composite_bars
