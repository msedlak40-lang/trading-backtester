# Development Instructions for Claude Code

## Project Goal

Build a complete backtesting system for a divergence trading strategy that:
1. Loads 1-minute bar data for NQ futures and 7 stocks
2. Calculates TBN composite by summing OHLC values
3. Implements Zone21B indicator logic on both NQ and composite
4. Detects divergences (NQ makes new swing, composite doesn't)
5. Identifies ATR bars as entry triggers
6. Manages positions with ATR-based stops and opposite ATR bar targets
7. Calculates full trade statistics and performance metrics

## Reference Files

**CRITICAL:** Review these files in `/reference/` before starting:
- `Zone21B.cs` - Original Zone21B indicator (buy side)
- `Zone21B2.cs` - Zone21B with both buy and sell side
- `TBNVolumeV3.cs` - Composite calculation example
- `TBNATRBarX.cs` - ATR bar detection logic
- `MES_12-25_Last.txt` - Sample data format

## Strategy Rules (MUST IMPLEMENT EXACTLY)

### Zone21B Indicator Logic

**Sequential Bar Pattern (Downward for Buy Setup):**

1. **Bar 1 (downBarOne)**: 
   - Condition: `Close < Open` AND not in underBar
   - Stores: `downBarOneHigh`, `downBarOneLow`
   - Reset if: `Close > downBarOneHigh`

2. **Bar 2 (downBarTwo)**: 
   - Condition: `Close < downBarOneLow` AND not in underBar
   - Stores: `downBarTwoHigh`, `downBarTwoLow`
   - **Triggers**: Swing High Calculation
   - Sets: `runningLow = Low[0]`

3. **Swing High Calculation** (after Bar 2):
   - Look back `lookback` bars (default 4)
   - Find highest high in that range
   - Store as `swingHigh` with bar index `swingHighBars`

4. **Bar 3 (downWithinBar)**:
   - Condition: `Close < Open` AND `Close < downBarTwoLow` AND not in underBar
   - Stores: `downWithinHigh`, `downWithinLow`

5. **Bar 4 (down4thBar)**:
   - Condition: `Close < downWithinLow` OR `lowerLow` condition
   - Stores: `down4thBarHigh`, `down4thBarLow`, `stored4thLow`
   - **R4 (Recycle 4)**: If `Close > down4thBarHigh`, reset pattern, keep `stored4thLow`

6. **takeBarHigh**:
   - Triggers when: `Close > downBarTwoHigh` (or `downWithinHigh` depending on state)
   - Indicates price broke back above the pattern

7. **takeSwingHigh**:
   - Triggers when: `Close > swingHigh`
   - Indicates price broke above the swing high

8. **Zeta Bar** (Setup Complete):
   - Forms when: `takeBarHigh == true` AND `takeSwingHigh == true`
   - This is the setup completion signal
   - Stores: `zetaBarHigh`, `zetaBarLow`, `zetaBarClose`, `storedSwingHigh`
   - Resets all switches

9. **Buy Zone**:
   - Activates after Zeta bar with `requiredCloses` (default 2) closes below Zeta bar low
   - Range: `buyZoneHigh = storedSwingHigh`, `buyZoneLow = runningLow`

10. **Lower Low (LL)**:
    - Triggers when: price breaks below `stored4thLow`
    - Indicates potential trend continuation

11. **Under Bar**:
    - Special condition to handle price going below levels during pattern formation
    - Uses `lowerLow` flag to determine if Bar 4 conditions are met

**State Tracking (Critical):**
```python
# All boolean flags must be tracked
downBarOne, downBarTwo, downWithinBar, down4thBar, underBar
iBar1down, iBar2down, iBar3down  # Inside bars
takeBarHigh, takeSwingHigh
zetaBar, zetaBarFT
buyZone

# All price levels must be stored
downBarOneHigh, downBarOneLow
downBarTwoHigh, downBarTwoLow
downWithinHigh, downWithinLow
down4thBarHigh, down4thBarLow
swingHigh, swingHighBars
stored4thLow
runningLow
storedSwingHigh
zetaBarHigh, zetaBarLow, zetaBarClose
buyZoneHigh, buyZoneLow
```

**Mirror Logic for Sell Side:**
- Same pattern but inverted (upBarOne, upBarTwo, upWithinBar, up4thBar, overBar)
- Swing Low calculation instead of Swing High
- Alpha Bar instead of Zeta Bar
- Sell Zone instead of Buy Zone
- Higher High (HH) instead of Lower Low (LL)

### Entry Logic

**Divergence Detection:**

1. **Bearish Divergence (Short Setup):**
   - NQ: `Close > prior swing high` (new high made)
   - Composite: `Close NOT > prior swing high` (no new high)
   - This indicates NQ strength without composite confirmation

2. **Bullish Divergence (Long Setup):**
   - NQ: `Close < prior swing low` (new low made)
   - Composite: `Close NOT < prior swing low` (no new low)
   - This indicates NQ weakness without composite confirmation

3. **After Divergence:**
   - Wait for NQ to make ANOTHER new swing high/low
   - ATR bar must occur within `max_bars_after_swing` (default 2) bars of this new swing

**ATR Bar Detection:**

From `TBNATRBarX.cs`:
```python
atr = ATR(7)  # 7-period ATR
bar_range = abs(Close - Open)
threshold = atr * atr_multiple  # Default 0.75

# Bullish ATR Bar (Green)
if Close > Open and bar_range >= threshold:
    atr_bar_type = BULLISH

# Bearish ATR Bar (Magenta)
if Close < Open and bar_range >= threshold:
    atr_bar_type = BEARISH
```

**Entry Trigger:**

- **Short Entry**: Bearish divergence + Bearish ATR bar within window
- **Long Entry**: Bullish divergence + Bullish ATR bar within window
- **Entry Price**: Close of the ATR bar

### Exit Logic

**Stop Loss Calculation:**
```python
atr_at_entry = ATR(7) at entry bar
stop_distance_points = atr_at_entry

# For shorts
stop_price = entry_price + stop_distance_points

# For longs  
stop_price = entry_price - stop_distance_points
```

**Profit Target Calculation:**
```python
# Look back max opposite_atr_lookback bars (default 20)
# Find most recent OPPOSITE direction ATR bar

# For short entry (looking for prior bullish ATR bar)
for i in range(1, opposite_atr_lookback + 1):
    if bars[entry_index - i].is_bullish_atr_bar:
        target_price = bars[entry_index - i].open
        break

# For long entry (looking for prior bearish ATR bar)
for i in range(1, opposite_atr_lookback + 1):
    if bars[entry_index - i].is_bearish_atr_bar:
        target_price = bars[entry_index - i].open
        break

# Minimum target distance must equal stop distance
target_distance = abs(target_price - entry_price)
if target_distance < stop_distance_points:
    # Use 1:1 risk/reward
    if short:
        target_price = entry_price - stop_distance_points
    else:
        target_price = entry_price + stop_distance_points
```

**Position Sizing:**
```python
tick_size = 0.25  # MES
tick_value = 1.25  # $ per tick

risk_amount = account_size * (risk_percent / 100)
stop_distance_ticks = stop_distance_points / tick_size
risk_per_contract = stop_distance_ticks * tick_value

position_size = int(risk_amount / risk_per_contract)
```

## Implementation Priority

### Phase 1: Core Data Structures ✓
**Files:** `src/data_structures.py`

Create these classes:
```python
@dataclass
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    
    # Computed properties
    is_bullish: bool
    is_bearish: bool
    range: float
    true_range: float

@dataclass
class Zone21State:
    # All state variables from the .cs file
    # Buy side
    down_bar_one: bool = False
    down_bar_one_high: float = 0.0
    down_bar_one_low: float = 0.0
    # ... (all other state variables)
    
    # Sell side
    up_bar_one: bool = False
    # ... (mirror of buy side)

@dataclass
class Trade:
    entry_bar: int
    entry_time: datetime
    entry_price: float
    direction: str  # 'LONG' or 'SHORT'
    position_size: int
    stop_price: float
    target_price: float
    
    exit_bar: Optional[int] = None
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None

@dataclass  
class Position:
    trade: Trade
    is_active: bool = True
```

### Phase 2: Data Loading ✓
**Files:** `src/data_loader.py`

Tasks:
- [ ] Parse NinjaTrader semicolon format: `YYYYMMDDhhmmss;O;H;L;C;V`
- [ ] Handle datetime parsing
- [ ] Load NQ futures data
- [ ] Load 7 stock files from `/data/stocks/`
- [ ] Align timestamps across all instruments
- [ ] Handle missing bars (forward fill or skip)
- [ ] Calculate TBN composite bars: Sum OHLC across 7 stocks

```python
class DataLoader:
    def load_file(filepath: str) -> List[Bar]:
        """Load single file into Bar objects"""
        
    def align_timestamps(bars_list: List[List[Bar]]) -> List[List[Bar]]:
        """Align all instruments to same timestamps"""
        
    def calculate_composite(stock_bars: List[List[Bar]]) -> List[Bar]:
        """Sum OHLC across all stock bars to create composite"""
```

### Phase 3: Indicators ✓
**Files:** `src/indicators/zone21b.py`, `src/indicators/atr_bar.py`

#### Zone21B Indicator (`zone21b.py`)

This is the most complex component. Must track complete state machine.

```python
class Zone21BIndicator:
    def __init__(self, lookback: int = 4):
        self.lookback = lookback
        self.state = Zone21State()
        self.bars: List[Bar] = []
        
    def on_bar(self, bar: Bar) -> None:
        """
        Process single bar and update state.
        Must implement exact logic from Zone21B.cs OnBarUpdate()
        """
        self.bars.append(bar)
        
        # Implement sequential logic:
        # 1. Check for Bar 1
        # 2. Check for Bar 2 + calculate swing
        # 3. Check for takeBarHigh
        # 4. Check for Bar 3
        # 5. Check for Bar 4
        # 6. Check for takeSwingHigh
        # 7. Check for Zeta bar formation
        # 8. Track Lower Low
        # 9. Handle resets (R4, etc.)
        
    def calculate_swing_high(self) -> float:
        """Look back 'lookback' bars for highest high"""
        
    def calculate_swing_low(self) -> float:
        """Look back 'lookback' bars for lowest low"""
        
    def reset_pattern(self) -> None:
        """Reset all state flags"""
        
    def get_current_swing_high(self) -> Optional[float]:
        """Return current swing high if set"""
        
    def get_current_swing_low(self) -> Optional[float]:
        """Return current swing low if set"""
```

#### ATR Bar Indicator (`atr_bar.py`)

```python
class ATRBarDetector:
    def __init__(self, period: int = 7, multiple: float = 0.75):
        self.period = period
        self.multiple = multiple
        self.atr_values: List[float] = []
        
    def calculate_atr(self, bars: List[Bar]) -> float:
        """Calculate ATR for given period"""
        
    def is_atr_bar(self, bar: Bar, atr: float) -> str:
        """
        Check if bar qualifies as ATR bar.
        Returns: 'BULLISH', 'BEARISH', or None
        """
        bar_range = abs(bar.close - bar.open)
        threshold = atr * self.multiple
        
        if bar.close > bar.open and bar_range >= threshold:
            return 'BULLISH'
        elif bar.close < bar.open and bar_range >= threshold:
            return 'BEARISH'
        return None
```

### Phase 4: Signal Generation ✓
**Files:** `src/engine/signal_generator.py`

```python
class SignalGenerator:
    def __init__(self, config):
        self.zone_nq = Zone21BIndicator(config['lookback'])
        self.zone_composite = Zone21BIndicator(config['lookback'])
        self.atr_detector = ATRBarDetector(config['atr_period'], config['atr_multiple'])
        self.max_bars_after_swing = config['max_bars_after_swing']
        
        # Tracking state
        self.divergence_active = False
        self.divergence_type = None  # 'BULLISH' or 'BEARISH'
        self.bars_since_new_swing = 0
        
    def process_bar(self, nq_bar: Bar, composite_bar: Bar, bar_index: int):
        """
        Process bars from both instruments.
        Detect divergences and ATR bar triggers.
        Returns signal dict or None.
        """
        
        # Update indicators
        self.zone_nq.on_bar(nq_bar)
        self.zone_composite.on_bar(composite_bar)
        
        # Check for divergence
        divergence = self.check_divergence()
        
        # If divergence active, check for new swing + ATR bar
        if self.divergence_active:
            if self.check_new_swing():
                self.bars_since_new_swing = 0
            else:
                self.bars_since_new_swing += 1
                
            # Check if within window
            if self.bars_since_new_swing <= self.max_bars_after_swing:
                atr_signal = self.check_atr_bar(nq_bar)
                if atr_signal:
                    return self.generate_entry_signal(bar_index, nq_bar)
                    
        return None
        
    def check_divergence(self) -> bool:
        """
        Compare swing states between NQ and composite.
        Returns True if divergence detected.
        """
        nq_swing_high = self.zone_nq.get_current_swing_high()
        composite_swing_high = self.zone_composite.get_current_swing_high()
        
        # Check if NQ made new high but composite didn't
        # ... implement logic
        
    def check_new_swing(self) -> bool:
        """Check if new swing high/low formed after divergence"""
        
    def check_atr_bar(self, bar: Bar) -> Optional[str]:
        """Check if current bar is ATR bar of correct type"""
```

### Phase 5: Backtest Engine ✓
**Files:** `src/engine/backtest.py`

```python
class Backtester:
    def __init__(self, config):
        self.config = config
        self.account_size = config['account']['initial_size']
        self.risk_percent = config['account']['risk_percent']
        
        self.signal_generator = SignalGenerator(config)
        self.positions: List[Position] = []
        self.closed_trades: List[Trade] = []
        self.equity_curve: List[float] = []
        
    def load_data(self, nq_file: str, stocks_dir: str):
        """Load and prepare all data"""
        loader = DataLoader()
        self.nq_bars = loader.load_file(nq_file)
        stock_bars = loader.load_stocks(stocks_dir)
        self.composite_bars = loader.calculate_composite(stock_bars)
        
    def run(self) -> Dict:
        """
        Main backtest loop.
        Process each bar, check for signals, manage positions.
        """
        for i in range(len(self.nq_bars)):
            nq_bar = self.nq_bars[i]
            composite_bar = self.composite_bars[i]
            
            # Check for entry signals
            signal = self.signal_generator.process_bar(nq_bar, composite_bar, i)
            if signal:
                self.enter_trade(signal, i, nq_bar)
                
            # Manage open positions
            self.manage_positions(i, nq_bar)
            
            # Update equity curve
            self.update_equity(i)
            
        return self.calculate_statistics()
        
    def enter_trade(self, signal: Dict, bar_index: int, bar: Bar):
        """
        Enter new position with proper sizing and stops.
        """
        # Calculate ATR for stop distance
        atr = self.calculate_atr(bar_index)
        stop_distance = atr
        
        # Find opposite ATR bar for target
        target_price = self.find_opposite_atr_target(
            bar_index, 
            signal['direction'],
            bar.close,
            stop_distance
        )
        
        # Calculate position size
        position_size = self.calculate_position_size(stop_distance)
        
        # Create trade
        trade = Trade(
            entry_bar=bar_index,
            entry_time=bar.timestamp,
            entry_price=bar.close,
            direction=signal['direction'],
            position_size=position_size,
            stop_price=self.calculate_stop(bar.close, stop_distance, signal['direction']),
            target_price=target_price
        )
        
        self.positions.append(Position(trade=trade))
        
    def find_opposite_atr_target(self, entry_index: int, direction: str, 
                                   entry_price: float, stop_distance: float) -> float:
        """
        Look back max opposite_atr_lookback bars for opposite ATR bar.
        Return open of that bar as target.
        If not found or distance < stop, use 1:1 R/R.
        """
        lookback = self.config['entry']['opposite_atr_lookback']
        
        # Search backwards
        for i in range(1, min(lookback + 1, entry_index)):
            bar = self.nq_bars[entry_index - i]
            atr = self.calculate_atr(entry_index - i)
            atr_type = self.atr_detector.is_atr_bar(bar, atr)
            
            if direction == 'SHORT' and atr_type == 'BULLISH':
                target = bar.open
                if abs(target - entry_price) >= stop_distance:
                    return target
                    
            elif direction == 'LONG' and atr_type == 'BEARISH':
                target = bar.open
                if abs(target - entry_price) >= stop_distance:
                    return target
                    
        # Default to 1:1 if not found
        if direction == 'SHORT':
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
            
    def calculate_position_size(self, stop_distance: float) -> int:
        """
        Calculate position size based on risk %.
        """
        tick_size = self.config['instrument']['tick_size']
        tick_value = self.config['instrument']['tick_value']
        
        risk_amount = self.account_size * (self.risk_percent / 100)
        stop_ticks = stop_distance / tick_size
        risk_per_contract = stop_ticks * tick_value
        
        position_size = int(risk_amount / risk_per_contract)
        return max(1, position_size)
        
    def manage_positions(self, bar_index: int, bar: Bar):
        """
        Check all open positions for stop/target hits.
        """
        for position in self.positions:
            if not position.is_active:
                continue
                
            trade = position.trade
            
            # Check stop hit
            if trade.direction == 'LONG':
                if bar.low <= trade.stop_price:
                    self.close_trade(position, bar_index, trade.stop_price, 'STOP')
                elif bar.high >= trade.target_price:
                    self.close_trade(position, bar_index, trade.target_price, 'TARGET')
                    
            elif trade.direction == 'SHORT':
                if bar.high >= trade.stop_price:
                    self.close_trade(position, bar_index, trade.stop_price, 'STOP')
                elif bar.low <= trade.target_price:
                    self.close_trade(position, bar_index, trade.target_price, 'TARGET')
                    
    def close_trade(self, position: Position, bar_index: int, 
                     exit_price: float, reason: str):
        """Close position and calculate P&L"""
        trade = position.trade
        trade.exit_bar = bar_index
        trade.exit_time = self.nq_bars[bar_index].timestamp
        trade.exit_price = exit_price
        trade.exit_reason = reason
        
        # Calculate P&L
        if trade.direction == 'LONG':
            pnl_points = (exit_price - trade.entry_price) * trade.position_size
        else:
            pnl_points = (trade.entry_price - exit_price) * trade.position_size
            
        tick_size = self.config['instrument']['tick_size']
        tick_value = self.config['instrument']['tick_value']
        pnl_ticks = pnl_points / tick_size
        trade.pnl = pnl_ticks * tick_value
        trade.pnl_percent = (trade.pnl / self.account_size) * 100
        
        position.is_active = False
        self.closed_trades.append(trade)
        
    def calculate_statistics(self) -> Dict:
        """Calculate comprehensive trade statistics"""
        if not self.closed_trades:
            return {}
            
        total_trades = len(self.closed_trades)
        winning_trades = [t for t in self.closed_trades if t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl <= 0]
        
        win_rate = len(winning_trades) / total_trades * 100
        
        total_pnl = sum(t.pnl for t in self.closed_trades)
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        profit_factor = (
            sum(t.pnl for t in winning_trades) / abs(sum(t.pnl for t in losing_trades))
            if losing_trades and sum(t.pnl for t in losing_trades) != 0 else 0
        )
        
        # Max drawdown
        equity = [self.account_size]
        for trade in self.closed_trades:
            equity.append(equity[-1] + trade.pnl)
        max_equity = equity[0]
        max_dd = 0
        for e in equity:
            if e > max_equity:
                max_equity = e
            dd = (max_equity - e) / max_equity * 100
            if dd > max_dd:
                max_dd = dd
                
        return {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_dd,
            'final_equity': equity[-1]
        }
```

### Phase 6: Testing & Validation
**Files:** `tests/test_*.py`

Create unit tests for:
- [ ] Data loading and parsing
- [ ] Zone21B state transitions
- [ ] ATR calculation
- [ ] ATR bar detection
- [ ] Signal generation logic
- [ ] Position sizing
- [ ] Stop/target calculation
- [ ] P&L calculation

### Phase 7: Visualization (Optional)
**Files:** `src/visualization/` or notebooks

- [ ] Plot NQ with Zone21B overlays
- [ ] Plot composite with Zone21B overlays
- [ ] Mark divergence points
- [ ] Show entry/exit markers
- [ ] Equity curve chart
- [ ] Monthly performance heatmap

## Critical Implementation Notes

1. **Bar-by-Bar Processing**: Must process sequentially, no lookahead bias
2. **State Persistence**: Zone21B state must persist across bars correctly
3. **Exact Logic**: Zone21B logic must match .cs files exactly - this is critical
4. **Edge Cases**: Handle missing data, gaps, market hours
5. **Precision**: Use proper rounding for prices (tick size = 0.25)
6. **Performance**: Optimize for speed after correctness is verified

## Testing Strategy

1. **Unit Tests**: Test each component independently
2. **Integration Tests**: Test full pipeline with synthetic data
3. **Validation**: Compare Zone21B output with NinjaTrader results
4. **Backtest**: Run on historical data and verify logic

## Data Format Reference

```
NinjaTrader Format:
YYYYMMDDhhmmss;Open;High;Low;Close;Volume
20251117 050100;6786.25;6786.75;6785.75;6786.75;105
```

Date: YYYYMMDD (8 digits)
Time: hhmmss (6 digits, 24-hour, with space separator)
Prices: Float
Volume: Integer

## Expected Output

After running backtest, print:
```
=== Backtest Results ===
Total Trades: 45
Win Rate: 62.2%
Total P&L: $12,450
Profit Factor: 2.1
Max Drawdown: 8.3%
Average Win: $520
Average Loss: $-280
```

Also save:
- `results/trades.csv` - All trades with details
- `results/equity_curve.csv` - Equity over time
- `results/statistics.json` - Full statistics

## Implementation Checklist

Use this to track progress:

- [ ] Phase 1: Core data structures
- [ ] Phase 2: Data loading
- [ ] Phase 3: Zone21B indicator
- [ ] Phase 3: ATR bar detector
- [ ] Phase 4: Signal generator
- [ ] Phase 5: Backtest engine
- [ ] Phase 6: Testing
- [ ] Phase 7: Visualization (optional)

## Questions for User

If you encounter ambiguity in the logic:
- Post question in comments
- Reference specific line in .cs files
- Provide example scenario

## Final Notes

This is a complex algorithmic trading system. The Zone21B indicator state machine is the most challenging component. Take time to understand the .cs file logic before implementing.

Focus on correctness first, then optimization. The strategy's edge depends on exact implementation of the indicator logic and divergence detection.

Good luck! 🚀
