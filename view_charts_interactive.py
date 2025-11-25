#!/usr/bin/env python3
"""
Interactive Chart Viewer Launcher

Run this to view charts with navigation controls.
Navigate through divergences using buttons or keyboard shortcuts.
"""
import yaml
import sys
from pathlib import Path
from src.data.data_loader import DataLoader
from src.engine.signal_generator import SignalGenerator
from src.engine.backtest import Backtester
from src.visualization.interactive_viewer import launch_interactive_viewer


def load_existing_results():
    """Load existing backtest results if available."""
    try:
        # Try to load divergences from CSV
        import csv
        from datetime import datetime

        divergences = []
        with open('results/divergence_log.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse divergence
                div = {
                    'bar_index': int(row['bar_index']),
                    'timestamp': datetime.fromisoformat(row['timestamp']),
                    'type': row['type'],
                    'nq_close': float(row['nq_close']),
                    'comp_close': float(row['comp_close']),
                    'status': row['status']
                }

                # Add swing values based on type
                if row['type'] == 'BEARISH':
                    div['nq_swing_high'] = float(row['nq_swing'])
                    div['comp_swing_high'] = float(row['comp_swing'])
                else:
                    div['nq_swing_low'] = float(row['nq_swing'])
                    div['comp_swing_low'] = float(row['comp_swing'])

                divergences.append(div)

        print(f"✓ Loaded {len(divergences)} divergences from results/divergence_log.csv")
        return divergences

    except FileNotFoundError:
        print("✗ No existing results found. Please run main.py first.")
        return None


def main():
    """Main launcher function."""
    print("=" * 70)
    print("INTERACTIVE CHART VIEWER")
    print("=" * 70)

    # Load configuration
    print("\nLoading configuration...")
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # Check if we need to run backtest first
    divergences = load_existing_results()

    if divergences is None:
        print("\nRunning backtest to generate data...")
        print("=" * 70)

        # Run backtest
        backtester = Backtester(config)
        backtester.load_data()
        stats = backtester.run()

        # Get results
        divergences = backtester.signal_generator.get_divergence_log()
        nq_bars = backtester.nq_bars
        composite_bars = backtester.composite_bars
        trades = backtester.closed_trades

    else:
        # Load data
        print("\nLoading market data...")
        loader = DataLoader()
        nq_bars, composite_bars = loader.load_all_data(
            config['data']['nq_file'],
            config['data']['stock_files']
        )

        # Load trades from CSV
        print("Loading trades...")
        trades = []
        try:
            import csv
            from datetime import datetime
            from src.data.data_structures import Trade

            with open('results/trades.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    trade = Trade(
                        entry_bar=0,  # We don't have this in CSV
                        entry_time=datetime.fromisoformat(row['entry_time']),
                        entry_price=float(row['entry_price']),
                        direction=row['direction'],
                        position_size=int(row['size']),
                        stop_price=float(row['stop']),
                        target_price=float(row['target']),
                        atr_at_entry=0,  # Not in CSV
                        exit_time=datetime.fromisoformat(row['exit_time']) if row['exit_time'] else None,
                        exit_price=float(row['exit_price']) if row['exit_price'] else None,
                        exit_reason=row['exit_reason'] if row['exit_reason'] else None,
                        pnl=float(row['pnl']) if row['pnl'] else None,
                        bars_in_trade=int(row['bars_in_trade']) if row['bars_in_trade'] else None
                    )
                    trades.append(trade)
            print(f"✓ Loaded {len(trades)} trades")
        except FileNotFoundError:
            print("✗ No trades file found")
            trades = []

    # Launch interactive viewer
    print("\n" + "=" * 70)
    print("LAUNCHING INTERACTIVE VIEWER")
    print("=" * 70)
    print(f"\n📊 {len(divergences)} divergences loaded")
    print(f"📈 {len(nq_bars)} bars of NQ data")
    print(f"💼 {len(trades)} trades executed")
    print("\n" + "=" * 70)

    launch_interactive_viewer(nq_bars, composite_bars, divergences, trades)


if __name__ == "__main__":
    main()
