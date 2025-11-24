# ⚡ Quick Reference - Claude Code Commands

## Single Command Setup

```bash
# 1. Extract the archive
tar -xzf trading-backtester.tar.gz
cd trading-backtester

# 2. Add your data files to data/nq/ and data/stocks/

# 3. Initialize git
git init && git add . && git commit -m "Initial setup"

# 4. Run Claude Code
claude-code "Read INSTRUCTIONS.md and begin implementation"
```

## Alternative: More Specific Command

```bash
claude-code "Read INSTRUCTIONS.md and implement Phase 1 through Phase 5, then run tests"
```

## What's Inside INSTRUCTIONS.md

- ✅ Complete strategy specification
- ✅ Zone21B state machine logic from .cs files
- ✅ Entry/exit rules with code examples
- ✅ 7 implementation phases with checklists
- ✅ Data structures and class definitions
- ✅ Testing requirements
- ✅ Expected output format

## Claude Code Will Build

1. `src/data_structures.py` - Bar, Trade, Position classes
2. `src/data_loader.py` - CSV parser, composite calculator
3. `src/indicators/zone21b.py` - Full indicator logic
4. `src/indicators/atr_bar.py` - ATR bar detector
5. `src/engine/signal_generator.py` - Divergence detector
6. `src/engine/backtest.py` - Main backtesting engine
7. `tests/` - Unit tests for all components

## After It's Built

```bash
# Run backtest
python quickstart.py

# Or use Python API
python
>>> from src.engine.backtest import Backtester
>>> import yaml
>>> with open('config/strategy_config.yaml') as f:
...     config = yaml.safe_load(f)
>>> bt = Backtester(config)
>>> bt.load_data('data/nq/MES_12-25_Last.txt', 'data/stocks/')
>>> results = bt.run()
>>> print(results)
```

## Customization

Edit `config/strategy_config.yaml`:
- `account.risk_percent` - Risk per trade (default 1%)
- `indicator.lookback` - Swing lookback (default 4 bars)
- `indicator.atr_period` - ATR period (default 7)
- `indicator.atr_multiple` - ATR bar threshold (default 0.75)
- `entry.max_bars_after_swing` - ATR bar window (default 2)
- `entry.opposite_atr_lookback` - Target search (default 20)

## Troubleshooting

**Claude Code asks questions?** 
- It's being careful! Answer based on the strategy discussion

**Missing data files?**
- Add your data to `data/nq/` and `data/stocks/`

**Import errors?**
- Run: `pip install -r requirements.txt`

**Logic questions?**
- Check `/reference/*.cs` files for original indicator code

## File Locations

- Strategy config: `config/strategy_config.yaml`
- Reference indicators: `reference/*.cs`
- Sample data: `reference/MES_12-25_Last.txt`
- Implementation guide: `INSTRUCTIONS.md` ⭐
