# Day-by-Day Chart Viewer Guide

## Overview

The Day-by-Day Chart Viewer is an interactive desktop application that lets you scroll through trading days to analyze NQ and Composite charts with Zone21B swing indicators and ATR bar markers.

## Features

- **Regular Trading Hours (RTH) Only**: Charts display only data from 8:30 AM - 3:00 PM CST
- **Side-by-Side Charts**: NQ and Composite charts shown together for easy comparison
- **Zone21B Swings**: Visual display of swing highs (blue dashed lines) and swing lows (purple dashed lines)
- **ATR Bar Highlighting**: Bullish ATR bars highlighted in green, bearish in orange
- **Day Navigation**: Easily scroll through each trading day
- **No Trade Logging**: Focuses purely on indicator visualization

## Installation

1. **Pull latest changes** (if running from repository):
   ```bash
   git pull origin claude/read-instructions-01EL3r9qxqCASRbjr3Add1D3
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Viewer

Launch the day-by-day viewer:

```bash
python view_days.py
```

## Navigation Controls

### Keyboard Shortcuts
- **Left Arrow** (←): Previous day
- **Right Arrow** (→): Next day
- **Home**: First day
- **End**: Last day

### Mouse Controls
- **Previous Button**: Go to previous day
- **Next Button**: Go to next day
- **First Day Button**: Go to first trading day
- **Last Day Button**: Go to last trading day

## Chart Elements

### NQ Chart (Top)
- **Green/Red Candlesticks**: Price bars (green = close > open, red = close < open)
- **Blue Dashed Lines**: Zone21B Swing Highs
- **Purple Dashed Lines**: Zone21B Swing Lows
- **Green Highlighted Bars**: Bullish ATR Bars (close > open, range >= 0.75 × ATR)
- **Orange Highlighted Bars**: Bearish ATR Bars (close < open, range >= 0.75 × ATR)

### Composite Chart (Middle)
Same elements as NQ chart, showing the 7-stock composite

### Information Panel (Bottom)
- Current day number and total days
- Bar counts for the day
- Indicator counts (swing highs, swing lows, ATR bars) for both NQ and Composite

## Understanding the Indicators

### Zone21B Swing Highs/Lows
- Calculated using 4-bar lookback
- Swing highs shown as horizontal blue dashed lines
- Swing lows shown as horizontal purple dashed lines
- These represent key support/resistance levels

### ATR Bars
- Bars with range >= 0.75 × ATR(7)
- Bullish: Close > Open with significant range (green highlight)
- Bearish: Close < Open with significant range (orange highlight)
- Used for trade entry and exit signals

## Data Processing

When you launch the viewer:
1. Loads NQ and 7-stock data from `data/` directory
2. Filters all bars to Regular Trading Hours (8:30 AM - 3:00 PM CST)
3. Processes Zone21B indicator on both NQ and Composite
4. Processes ATR(7) detector on both instruments
5. Groups data by trading day
6. Displays interactive charts

## Tips

- Use arrow keys for quick day-to-day navigation
- Look for divergences: Days where NQ makes a new swing high/low but Composite doesn't (or vice versa)
- ATR bars often signal significant momentum - watch for them near swing levels
- Swing lines persist across the chart to show key levels
- The info panel shows how many swings and ATR bars occurred each day

## Troubleshooting

### "ModuleNotFoundError: No module named 'matplotlib'"
Run: `pip install -r requirements.txt`

### Charts not displaying
Make sure you're not running from a remote SSH session without X11 forwarding. The viewer requires a graphical display.

### No trading days shown
Verify that your data files exist in the `data/` directory and are in the correct NinjaTrader format.

## Configuration

You can adjust indicator parameters in `config.yaml`:

```yaml
indicators:
  zone21b:
    lookback: 4  # Swing calculation lookback period
    required_closes: 2  # Closes needed to activate zone

  atr_bar:
    period: 7  # ATR period
    multiple: 0.75  # ATR multiple for bar qualification
```

## What's Different from Previous Viewer

The previous `view_charts_interactive.py` navigated divergence-to-divergence. This new viewer:
- Navigates day-by-day instead
- Shows RTH only (8:30 AM - 3:00 PM CST)
- Focuses on indicator visualization (swings and ATR bars)
- Does NOT log trades or detect divergences
- Gives you a clean view to manually analyze patterns

## Next Steps

Use this viewer to:
1. Validate Zone21B swing calculations
2. Verify ATR bar detection
3. Manually identify divergence patterns
4. Study market behavior during RTH
5. Understand the relationship between NQ and the Composite
