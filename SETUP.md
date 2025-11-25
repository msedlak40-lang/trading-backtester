# Trading Backtester - Setup Instructions

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Extract the files** to a folder on your computer

2. **Open a terminal/command prompt** in that folder

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backtest:**
   ```bash
   python main.py
   ```

### What Happens

The program will:
1. Load all data files (NQ futures + 7 stocks)
2. Run the complete backtest
3. Generate charts automatically
4. Save everything to `results/` folder

### Viewing the Charts

Charts are saved as PNG images in `results/charts/`:

- **summary.png** - Full overview with all divergences and trades
- **div_01.png through div_11.png** - Detailed view of each divergence

You can:
- Open them in any image viewer
- Use Windows Photo Viewer / Mac Preview
- View in your web browser
- Use an image organizer like XnView, IrfanView, etc.

### Configuration

Edit `config.yaml` to customize:

**Chart Settings:**
```yaml
visualization:
  enabled: true                    # Turn charts on/off
  bars_before_divergence: 100      # More context before divergence
  bars_after_divergence: 100       # More context after divergence
```

**Strategy Settings:**
```yaml
entry:
  max_bars_after_swing: 2          # Window for ATR bar (try 3-5 for more trades)

atr_bar:
  multiple: 0.75                   # ATR threshold (try 0.5 for more ATR bars)
```

**Debug Output:**
```yaml
debug:
  show_divergences: true           # Print divergence details
  show_atr_bars: true              # Print all ATR bars
  show_swing_updates: true         # Print swing updates
```

### Output Files

After running, check these folders:

**results/**
- `trades.csv` - All trade details
- `statistics.json` - Performance metrics
- `divergence_log.csv` - All divergences detected
- `equity_curve.csv` - Equity over time

**results/charts/**
- `summary.png` - Overview chart
- `div_XX_*.png` - Individual divergence charts

### Troubleshooting

**"Module not found" error:**
```bash
pip install --upgrade -r requirements.txt
```

**Charts not generating:**
- Check that `visualization.enabled: true` in config.yaml
- Check results/charts/ folder was created

**No divergences found:**
- Check date range of your data files
- Try adjusting Zone21B parameters in config.yaml

### Need Help?

- Check the logs printed during backtest
- Review INSTRUCTIONS.md for strategy details
- Examine the generated charts to see what's happening

## Advanced Usage

### Run with Custom Data

Replace the data files in the root directory:
- `MNQ 12-25.Last.txt` - Your NQ futures data
- `AAPL.Last.txt`, `MSFT.Last.txt`, etc. - Your stock data

Data format: `YYYYMMDDhhmmss;Open;High;Low;Close;Volume`

### Parameter Optimization

Try different settings in `config.yaml`:
- Increase `max_bars_after_swing` to 3-5 (more time to find ATR bar)
- Decrease `atr_bar.multiple` to 0.5 (easier to qualify as ATR bar)
- Change `zone21b.lookback` to 3 or 5 (different swing detection)

### View Specific Time Periods

The charts show 100 bars before/after each divergence by default.
Adjust in config.yaml to zoom in/out.

## What the Charts Show

### Summary Chart
- Top panel: NQ with all divergences marked
- Bottom panel: Composite showing where it diverged
- Red arrows: Divergence detection points
- Trade markers: Entry/exit with P&L

### Divergence Detail Charts
- 100 bars before and after the divergence
- Clear view of price action leading up to and following divergence
- ATR bar window visibility
- Trade execution if it occurred

Enjoy analyzing your divergences!
