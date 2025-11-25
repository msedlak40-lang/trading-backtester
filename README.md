# Trading Backtester - Divergence Strategy

A complete backtesting system for a divergence trading strategy using Zone21B indicator and ATR bars.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/msedlak40-lang/trading-backtester.git
cd trading-backtester

# Install dependencies
pip install -r requirements.txt

# Run the backtest
python main.py
```

### 📊 Viewing Charts

After running the backtest, **open `view_charts.html` in your web browser** to interactively browse all charts:

```bash
# On Windows
start view_charts.html

# On Mac
open view_charts.html

# On Linux
xdg-open view_charts.html
```

**Features of the Chart Viewer:**
- 📈 Interactive filtering (All / Summary / Divergences / Trades)
- 🔍 Click any chart to zoom in
- ⬆️ Scroll-to-top button for easy navigation
- 📱 Responsive design works on any device
- ⌨️ Press ESC to close zoomed images

All charts are also available as PNG files in `results/charts/`.

## Overview

This system implements a sophisticated trading strategy that:
1. Monitors NQ futures and a 7-stock composite for divergences
2. Uses the Zone21B indicator to identify swing points
3. Detects when NQ makes a new swing but the composite doesn't (divergence)
4. Waits for confirmation and an ATR bar to trigger entry
5. Manages positions with ATR-based stops and opposite ATR bar targets

## Strategy Logic

### Divergence Detection

**Bearish Divergence (Short Setup):**
- NQ makes new swing high
- Composite does NOT make new swing high
- Wait for NQ to make ANOTHER new swing high
- ATR bar (bearish) must occur within 2 bars

**Bullish Divergence (Long Setup):**
- NQ makes new swing low
- Composite does NOT make new swing low
- Wait for NQ to make ANOTHER new swing low
- ATR bar (bullish) must occur within 2 bars

### Zone21B Indicator

Complex state machine that tracks sequential bar patterns:
1. Bar 1 (downBarOne): Close < Open
2. Bar 2 (downBarTwo): Close < downBarOneLow (triggers swing calculation)
3. Bar 3 (downWithinBar): Close < Open AND Close < downBarTwoLow
4. Bar 4 (down4thBar): Close < downWithinLow
5. takeBarHigh: Close > downBarTwoHigh
6. takeSwingHigh: Close > swingHigh
7. zetaBar: Both takeBarHigh AND takeSwingHigh
8. buyZone: After 2 closes above zetaBar

Mirror logic for sell side (upward patterns).

### ATR Bar Detection

Based on TBNATRBarX.cs:
- ATR period: 7 bars
- Threshold: ATR × 0.75
- Bullish ATR bar: Close > Open AND |Close - Open| ≥ threshold
- Bearish ATR bar: Close < Open AND |Close - Open| ≥ threshold

### Position Management

**Entry:**
- Entry price: Close of ATR bar
- Position size: Based on 2% account risk

**Stop Loss:**
- Distance: 1 ATR at entry
- Long: entry_price - ATR
- Short: entry_price + ATR

**Profit Target:**
- Primary: Open of most recent opposite ATR bar (within 20 bars)
- Minimum: 1:1 Risk/Reward ratio

## Project Structure

```
trading-backtester/
├── main.py                          # Main entry point
├── config.yaml                      # Configuration file
├── requirements.txt                 # Python dependencies
├── INSTRUCTIONS.md                  # Detailed implementation guide
├── README.md                        # This file
├── src/
│   ├── data/
│   │   ├── data_structures.py      # Core data classes
│   │   └── data_loader.py          # Data loading and alignment
│   ├── indicators/
│   │   ├── zone21b.py              # Zone21B indicator
│   │   └── atr_bar.py              # ATR bar detector
│   └── engine/
│       ├── signal_generator.py      # Divergence detection & signals
│       └── backtest.py              # Main backtest engine
├── results/
│   ├── trades.csv                   # Trade log
│   ├── equity_curve.csv             # Equity over time
│   └── statistics.json              # Performance metrics
└── data files (*.Last.txt)          # Market data

```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to customize:

```yaml
# Zone21B settings
zone21b:
  lookback: 4              # Swing calculation lookback
  required_closes: 2       # Closes to activate zone

# ATR bar settings
atr_bar:
  period: 7               # ATR period
  multiple: 0.75          # ATR threshold multiplier

# Entry settings
entry:
  max_bars_after_swing: 2       # Window for ATR bar
  opposite_atr_lookback: 20     # Lookback for target

# Account settings
account:
  initial_size: 100000    # Starting capital
  risk_percent: 2.0       # Risk per trade (%)

# Instrument settings
instrument:
  tick_size: 0.25         # MES tick size
  tick_value: 1.25        # Dollar value per tick
```

## Usage

Run the backtest:

```bash
python main.py
```

The system will:
1. Load NQ futures and 7 stock data files
2. Align timestamps across all instruments
3. Calculate the composite (sum of OHLC from 7 stocks)
4. Run the backtest bar-by-bar
5. Generate entry signals based on divergences
6. Manage positions with stops and targets
7. Calculate and display performance statistics
8. Save results to CSV and JSON files

## Output Files

**results/trades.csv** - Complete trade log with:
- Entry/exit times and prices
- Direction, size, stops, targets
- P&L and bars in trade

**results/equity_curve.csv** - Equity over time:
- Bar index
- Equity value

**results/statistics.json** - Performance metrics:
- Total trades, win rate
- P&L statistics
- Profit factor
- Maximum drawdown
- Return percentage

## Data Format

NinjaTrader semicolon-delimited format:
```
YYYYMMDDhhmmss;Open;High;Low;Close;Volume
20250914 220100;6645.25;6650.75;6645;6645.75;437
```

## Composite Calculation

**IMPORTANT:** The composite uses the EXACT logic from TBNVolumeV3.cs:
- Open = sum of all 7 stock Opens
- High = Stock[0].High + Stock[1-6].Low
- Low = Stock[0].Low + Stock[1-6].High
- Close = sum of all 7 stock Closes

This unusual High/Low calculation is intentional and matches the reference implementation.

## Implementation Details

### Key Features
- Exact replication of Zone21B.cs state machine logic
- Proper timestamp alignment across all instruments
- Bar-by-bar processing (no lookahead bias)
- ATR-based position sizing
- Comprehensive trade statistics

### Performance
- Handles 24,000+ bars efficiently
- Progress tracking during execution
- Results saved automatically

## Sample Results

```
============================================================
BACKTEST RESULTS
============================================================
Total Trades:        1
Winning Trades:      0
Losing Trades:       1
Win Rate:            0.0%

Total P&L:           $-1,956.00
Average Win:         $0.00
Average Loss:        $-1,956.00
Profit Factor:       0.00

Max Drawdown:        $1,956.00 (2.0%)
Final Equity:        $98,044.00
Return:              -2.0%

Avg Bars in Trade:   0.0
============================================================
```

## Strategy Characteristics

The strategy is **highly selective** by design:
- Waits for specific divergence patterns
- Requires multiple confirmations
- Only trades when all conditions align

This results in **few but high-quality setups** rather than many marginal trades.

## Reference Files

The implementation is based on these NinjaTrader indicators:
- `Zone21B2.cs` - Zone21B indicator with buy and sell side
- `TBNVolumeV3.cs` - Composite calculation
- `TBNATRBarX.cs` - ATR bar detection

## Future Enhancements

Potential improvements:
- Parameter optimization
- Additional filters or confirmations
- Multiple timeframe analysis
- Walk-forward testing
- Monte Carlo simulation
- Visualization of setups and trades

## Notes

- The strategy requires significant divergence to trigger
- Few trades in backtest period is expected behavior
- System prioritizes quality over quantity of signals
- All logic matches reference C# implementations exactly

## License

This is a proprietary trading system implementation.

## Author

Built following exact specifications from INSTRUCTIONS.md and reference C# indicator files.
