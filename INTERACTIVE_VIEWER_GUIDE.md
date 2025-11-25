# Interactive Chart Viewer Guide

## 🚀 Quick Start

Simply run:

```bash
python view_charts_interactive.py
```

This will launch an interactive desktop application where you can navigate through all divergences.

## 📊 What You'll See

The application shows **two main charts** side-by-side:

1. **Top Panel: NQ Futures**
   - Candlestick chart
   - Divergence markers (red arrows for bearish, green for bullish)
   - Trade entries/exits if applicable
   - Stop and target levels

2. **Middle Panel: Composite (7 Stocks)**
   - Candlestick chart
   - Shows where composite diverged from NQ
   - Orange/cyan markers at divergence points

3. **Bottom Panel: Info & Controls**
   - Left: Divergence details (type, prices, swings)
   - Right: Keyboard shortcut reference

## 🎮 Controls

### Navigation Buttons

- **First** - Jump to first divergence
- **Previous** - Go back one divergence (or press ← or P)
- **Next** - Go forward one divergence (or press → or N)
- **Last** - Jump to last divergence

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `←` or `P` | Previous divergence |
| `→` or `N` | Next divergence |
| `Home` | First divergence |
| `End` | Last divergence |
| `Q` | Quit application |

### Context Slider

At the bottom, there's a slider labeled **"Context (bars)"**:
- Drag left to see fewer bars (zoom in, more detail)
- Drag right to see more bars (zoom out, more context)
- Range: 10 to 500 bars before/after divergence
- Default: 100 bars

## 🔍 What to Look For

### Divergence Markers

**On NQ Chart:**
- 🔺 Red up-arrow = Bearish divergence (NQ made new high)
- 🔻 Green down-arrow = Bullish divergence (NQ made new low)
- Text shows: NQ close price and swing level

**On Composite Chart:**
- 🟠 Orange circle = Composite did NOT make new high (bearish div)
- 🔵 Cyan circle = Composite did NOT make new low (bullish div)
- Text shows: Composite close price and swing level

### Trade Markers (if trade occurred)

- **Entry**: Large triangle (▼ for SHORT, ▲ for LONG)
- **Exit**: Large X marker
- **Stop Level**: Red dotted horizontal line
- **Target Level**: Green dotted horizontal line
- **Trade Line**: Dashed line connecting entry to exit

### Vertical Red Line

The vertical dashed red line marks the exact bar where the divergence was detected.

## 📋 Info Panel Details

Left side shows:
```
DIVERGENCE #X of 11

Type: BEARISH / BULLISH
Time: 2025-09-18 14:12:00

NQ:
  Close: 24758.50
  Swing: 24753.50

Composite:
  Close: 2622.36
  Swing: 2628.70

Status: DETECTED
```

## 💡 Tips for Analysis

1. **Use the slider** to adjust context:
   - Zoom in (10-50 bars) to see price action details
   - Zoom out (200-500 bars) to see trend context

2. **Compare divergences**:
   - Navigate through all 11 to spot patterns
   - Notice which ones had follow-through
   - See which had ATR bars nearby

3. **Look for the one trade** (Divergence #11):
   - Notice the SHORT entry marker
   - See how quickly it hit the stop
   - Observe the ATR bar that triggered entry

4. **Analyze why most didn't trade**:
   - No ATR bar within 2-bar window after divergence
   - ATR bar detection is strict (0.75× ATR threshold)

## 🛠️ Troubleshooting

### "No divergences to display"

Run the backtest first:
```bash
python main.py
```

### Application won't open

Make sure you have matplotlib installed:
```bash
pip install matplotlib
```

### Charts look cramped

- Maximize the window
- Use the slider to reduce context (fewer bars)
- Close info panels if needed

### Performance is slow

- Reduce context window (use slider)
- Close other applications
- System with more RAM helps

## 🎯 Workflow

Typical analysis workflow:

1. **Run backtest** to generate data:
   ```bash
   python main.py
   ```

2. **Launch interactive viewer**:
   ```bash
   python view_charts_interactive.py
   ```

3. **Navigate through divergences**:
   - Use → key or Next button
   - Examine each setup carefully

4. **Adjust view as needed**:
   - Slide context to zoom in/out
   - Look for patterns across divergences

5. **Note observations**:
   - Which divergences look strongest?
   - Why didn't most trigger trades?
   - What could improve entry rate?

6. **Modify parameters** in `config.yaml` and re-run:
   ```yaml
   entry:
     max_bars_after_swing: 5  # Give more time

   atr_bar:
     multiple: 0.5  # Easier to qualify
   ```

## 🆚 Interactive Viewer vs Static Charts

| Feature | Interactive Viewer | Static PNG Charts |
|---------|-------------------|-------------------|
| Navigation | ✅ Buttons & keyboard | ❌ Manual file opening |
| Zoom | ✅ Slider control | ❌ Fixed scale |
| Context adjustment | ✅ Real-time | ❌ Regenerate needed |
| Speed | ⚡ Instant | 🐌 Must open each file |
| Analysis | ✅ Compare easily | ⚠️ Switch windows |
| Best for | Active analysis | Sharing/reports |

## 🎨 Customization

Want to modify the viewer? Edit `src/visualization/interactive_viewer.py`:

- Change default context: `self.bars_before = 200`
- Modify colors: Change color parameters in plot functions
- Add features: Extend the `InteractiveChartViewer` class

## 📝 Notes

- The viewer loads all data into memory (may take 10-20 seconds)
- First load reads from results files
- Subsequent runs are faster (data cached)
- You can have multiple viewers open to compare
- Close with Q key or close window

## 🎓 Learning the Strategy

Use the interactive viewer to:

1. **Understand divergence mechanics**
   - See exactly when NQ breaks swing
   - See exactly when Composite doesn't follow

2. **Learn ATR bar requirements**
   - Notice how rare they are
   - Understand the 2-bar window constraint

3. **Study the one successful trade**
   - Why did this one trigger?
   - What made it different?
   - Why did it lose?

4. **Identify improvements**
   - Should window be larger?
   - Should ATR threshold be lower?
   - Different swing detection?

---

**Happy analyzing! Use those arrow keys to scroll through divergences fast! 🚀**
