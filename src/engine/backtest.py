"""
Backtest Engine - Main backtesting system with position management.
"""
import json
from typing import List, Dict, Optional
from datetime import datetime
from src.data.data_structures import Bar, Trade, Position
from src.data.data_loader import DataLoader
from src.engine.signal_generator import SignalGenerator


class Backtester:
    """Main backtesting engine with position management and statistics."""

    def __init__(self, config: dict):
        """
        Initialize backtester with configuration.

        Args:
            config: Full configuration dictionary
        """
        self.config = config
        self.account_size = config['account']['initial_size']
        self.risk_percent = config['account']['risk_percent']
        self.tick_size = config['instrument']['tick_size']
        self.tick_value = config['instrument']['tick_value']

        # Initialize components
        self.signal_generator = SignalGenerator(config)

        # Data storage
        self.nq_bars: List[Bar] = []
        self.composite_bars: List[Bar] = []

        # Trading state
        self.positions: List[Position] = []
        self.closed_trades: List[Trade] = []
        self.equity_curve: List[float] = [self.account_size]
        self.current_equity = self.account_size

    def load_data(self) -> None:
        """Load and prepare all market data."""
        loader = DataLoader()
        self.nq_bars, self.composite_bars = loader.load_all_data(
            self.config['data']['nq_file'],
            self.config['data']['stock_files']
        )

        print(f"\nBacktest data ready: {len(self.nq_bars)} bars")
        if self.nq_bars:
            print(f"Date range: {self.nq_bars[0].timestamp} to {self.nq_bars[-1].timestamp}")

    def run(self) -> Dict:
        """
        Execute the backtest.
        Process each bar, generate signals, manage positions, track equity.

        Returns:
            Dictionary of backtest statistics
        """
        print("\n" + "=" * 60)
        print("RUNNING BACKTEST")
        print("=" * 60)

        total_bars = len(self.nq_bars)
        print_interval = max(1, total_bars // 20)  # Print progress every 5%

        for i in range(total_bars):
            nq_bar = self.nq_bars[i]
            comp_bar = self.composite_bars[i]

            # Progress indicator
            if i % print_interval == 0:
                pct = (i / total_bars) * 100
                print(f"Progress: {pct:.1f}% ({i}/{total_bars} bars) - "
                      f"{nq_bar.timestamp.date()} - "
                      f"Trades: {len(self.closed_trades)} - "
                      f"Equity: ${self.current_equity:,.2f}")

            # Generate entry signals
            if not self.positions:  # Only one position at a time
                signal = self.signal_generator.process_bar(nq_bar, comp_bar, i)
                if signal:
                    self.enter_trade(signal, i, nq_bar)

            # Manage open positions
            self.manage_positions(i, nq_bar)

            # Update equity curve
            self.update_equity(i)

        print("\n" + "=" * 60)
        print("BACKTEST COMPLETE")
        print("=" * 60)

        # Calculate statistics
        stats = self.calculate_statistics()
        return stats

    def enter_trade(self, signal: Dict, bar_index: int, bar: Bar) -> None:
        """
        Enter a new position based on signal.

        Args:
            signal: Signal dictionary from signal generator
            bar_index: Current bar index
            bar: Current bar
        """
        direction = signal['type']
        entry_price = signal['entry_price']
        atr = signal['atr']

        # Calculate stop distance (1 ATR)
        stop_distance = atr

        # Calculate stop price
        if direction == 'LONG':
            stop_price = entry_price - stop_distance
        else:  # SHORT
            stop_price = entry_price + stop_distance

        # Find opposite ATR bar for target
        target_price = self.find_opposite_atr_target(
            bar_index, direction, entry_price, stop_distance
        )

        # Calculate position size
        position_size = self.calculate_position_size(stop_distance)

        # Create trade
        trade = Trade(
            entry_bar=bar_index,
            entry_time=bar.timestamp,
            entry_price=entry_price,
            direction=direction,
            position_size=position_size,
            stop_price=stop_price,
            target_price=target_price,
            atr_at_entry=atr
        )

        # Create position
        position = Position(trade=trade)
        self.positions.append(position)

        if self.config['output']['print_trades']:
            print(f"\n>>> ENTRY: {direction} @ {entry_price:.2f} "
                  f"[{bar.timestamp}] "
                  f"Size: {position_size} "
                  f"Stop: {stop_price:.2f} "
                  f"Target: {target_price:.2f}")

    def find_opposite_atr_target(self, entry_index: int, direction: str,
                                 entry_price: float, stop_distance: float) -> float:
        """
        Find opposite direction ATR bar for target.
        If not found or distance < stop, use 1:1 R/R.

        Args:
            entry_index: Entry bar index
            direction: 'LONG' or 'SHORT'
            entry_price: Entry price
            stop_distance: Stop distance in points

        Returns:
            Target price
        """
        lookback = self.config['entry']['opposite_atr_lookback']
        atr_detector = self.signal_generator.get_atr_detector()

        # Find opposite ATR bar
        opposite_atr_bar = atr_detector.find_opposite_atr_bar(
            entry_index, direction, lookback
        )

        if opposite_atr_bar:
            # Use open of opposite ATR bar as target
            target = opposite_atr_bar.open_price

            # Verify minimum distance (must be >= stop distance for 1:1 R/R)
            target_distance = abs(target - entry_price)
            if target_distance >= stop_distance:
                return target

        # Default to 1:1 R/R if not found or insufficient distance
        if direction == 'LONG':
            return entry_price + stop_distance
        else:  # SHORT
            return entry_price - stop_distance

    def calculate_position_size(self, stop_distance: float) -> int:
        """
        Calculate position size based on risk %.

        Args:
            stop_distance: Stop distance in points

        Returns:
            Number of contracts
        """
        # Risk amount in dollars
        risk_amount = self.current_equity * (self.risk_percent / 100)

        # Calculate risk per contract
        stop_ticks = stop_distance / self.tick_size
        risk_per_contract = stop_ticks * self.tick_value

        if risk_per_contract == 0:
            return 1

        # Calculate position size
        position_size = int(risk_amount / risk_per_contract)

        # Minimum 1 contract
        return max(1, position_size)

    def manage_positions(self, bar_index: int, bar: Bar) -> None:
        """
        Check all open positions for stop/target hits.

        Args:
            bar_index: Current bar index
            bar: Current bar
        """
        for position in self.positions:
            if not position.is_active:
                continue

            trade = position.trade

            # Check for stop or target hit
            if trade.direction == 'LONG':
                # Check stop (low <= stop)
                if bar.low <= trade.stop_price:
                    self.close_position(position, bar_index, bar, trade.stop_price, 'STOP')
                # Check target (high >= target)
                elif bar.high >= trade.target_price:
                    self.close_position(position, bar_index, bar, trade.target_price, 'TARGET')

            else:  # SHORT
                # Check stop (high >= stop)
                if bar.high >= trade.stop_price:
                    self.close_position(position, bar_index, bar, trade.stop_price, 'STOP')
                # Check target (low <= target)
                elif bar.low <= trade.target_price:
                    self.close_position(position, bar_index, bar, trade.target_price, 'TARGET')

    def close_position(self, position: Position, bar_index: int, bar: Bar,
                      exit_price: float, reason: str) -> None:
        """
        Close a position and update equity.

        Args:
            position: Position to close
            bar_index: Exit bar index
            bar: Exit bar
            exit_price: Exit price
            reason: Exit reason ('STOP' or 'TARGET')
        """
        position.close(bar_index, bar.timestamp, exit_price, reason,
                      self.tick_size, self.tick_value)

        trade = position.trade
        self.current_equity += trade.pnl
        self.closed_trades.append(trade)

        if self.config['output']['print_trades']:
            print(f"<<< EXIT: {trade.direction} @ {exit_price:.2f} "
                  f"[{bar.timestamp}] "
                  f"Reason: {reason} "
                  f"P&L: ${trade.pnl:,.2f} "
                  f"Bars: {trade.bars_in_trade}")

    def update_equity(self, bar_index: int) -> None:
        """Update equity curve."""
        # Current equity = closed trades P&L + unrealized P&L
        equity = self.account_size + sum(t.pnl for t in self.closed_trades)

        # Add unrealized P&L from open positions
        for position in self.positions:
            if position.is_active:
                trade = position.trade
                bar = self.nq_bars[bar_index]

                # Estimate unrealized P&L using current close
                if trade.direction == 'LONG':
                    unrealized_points = (bar.close - trade.entry_price) * trade.position_size
                else:
                    unrealized_points = (trade.entry_price - bar.close) * trade.position_size

                unrealized_ticks = unrealized_points / self.tick_size
                unrealized_pnl = unrealized_ticks * self.tick_value
                equity += unrealized_pnl

        self.equity_curve.append(equity)

    def calculate_statistics(self) -> Dict:
        """
        Calculate comprehensive trading statistics.

        Returns:
            Dictionary of statistics
        """
        if not self.closed_trades:
            print("\nNo trades executed!")
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'max_drawdown_pct': 0.0,
                'final_equity': self.account_size,
                'return_pct': 0.0
            }

        total_trades = len(self.closed_trades)
        winning_trades = [t for t in self.closed_trades if t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl <= 0]

        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0

        total_pnl = sum(t.pnl for t in self.closed_trades)
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0

        total_wins = sum(t.pnl for t in winning_trades)
        total_losses = abs(sum(t.pnl for t in losing_trades))
        profit_factor = total_wins / total_losses if total_losses > 0 else 0

        # Calculate max drawdown
        peak_equity = self.account_size
        max_dd = 0
        max_dd_pct = 0

        for equity in self.equity_curve:
            if equity > peak_equity:
                peak_equity = equity
            dd = peak_equity - equity
            dd_pct = (dd / peak_equity) * 100 if peak_equity > 0 else 0
            if dd > max_dd:
                max_dd = dd
                max_dd_pct = dd_pct

        final_equity = self.equity_curve[-1] if self.equity_curve else self.account_size
        return_pct = ((final_equity - self.account_size) / self.account_size) * 100

        # Average bars in trade
        avg_bars = sum(t.bars_in_trade for t in self.closed_trades) / total_trades

        stats = {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_dd,
            'max_drawdown_pct': max_dd_pct,
            'final_equity': final_equity,
            'return_pct': return_pct,
            'avg_bars_in_trade': avg_bars
        }

        return stats

    def print_summary(self, stats: Dict) -> None:
        """Print formatted summary of results."""
        print("\n" + "=" * 60)
        print("BACKTEST RESULTS")
        print("=" * 60)
        print(f"Total Trades:        {stats['total_trades']}")
        print(f"Winning Trades:      {stats['winning_trades']}")
        print(f"Losing Trades:       {stats['losing_trades']}")
        print(f"Win Rate:            {stats['win_rate']:.1f}%")
        print(f"\nTotal P&L:           ${stats['total_pnl']:,.2f}")
        print(f"Average Win:         ${stats['avg_win']:,.2f}")
        print(f"Average Loss:        ${stats['avg_loss']:,.2f}")
        print(f"Profit Factor:       {stats['profit_factor']:.2f}")
        print(f"\nMax Drawdown:        ${stats['max_drawdown']:,.2f} ({stats['max_drawdown_pct']:.1f}%)")
        print(f"Final Equity:        ${stats['final_equity']:,.2f}")
        print(f"Return:              {stats['return_pct']:.1f}%")
        print(f"\nAvg Bars in Trade:   {stats['avg_bars_in_trade']:.1f}")
        print("=" * 60)

    def save_results(self, stats: Dict) -> None:
        """Save results to files."""
        # Save statistics
        stats_file = self.config['output']['statistics_file']
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"\nStatistics saved to: {stats_file}")

        # Save trades to CSV
        trades_file = self.config['output']['trades_file']
        with open(trades_file, 'w') as f:
            # Header
            f.write("entry_time,entry_price,direction,size,stop,target,"
                   "exit_time,exit_price,exit_reason,pnl,bars_in_trade\n")

            # Trades
            for trade in self.closed_trades:
                f.write(f"{trade.entry_time},{trade.entry_price},{trade.direction},"
                       f"{trade.position_size},{trade.stop_price},{trade.target_price},"
                       f"{trade.exit_time},{trade.exit_price},{trade.exit_reason},"
                       f"{trade.pnl},{trade.bars_in_trade}\n")
        print(f"Trades saved to: {trades_file}")

        # Save equity curve
        equity_file = self.config['output']['equity_file']
        with open(equity_file, 'w') as f:
            f.write("bar,equity\n")
            for i, equity in enumerate(self.equity_curve):
                f.write(f"{i},{equity}\n")
        print(f"Equity curve saved to: {equity_file}")
