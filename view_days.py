#!/usr/bin/env python3
"""
Day-by-Day Chart Viewer Launcher
Launch interactive viewer to scroll through trading days
"""
import yaml
from src.data.data_loader import DataLoader
from src.engine.indicator_processor import IndicatorProcessor
from src.visualization.day_viewer import launch_day_viewer


def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("DAY-BY-DAY CHART VIEWER")
    print("="*80)

    # Load configuration
    print("\nLoading configuration...")
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # Extract configuration
    data_config = config['data']
    zone21_config = config['zone21b']
    atr_config = config['atr_bar']

    # Load data
    print("\nLoading market data...")
    loader = DataLoader(base_path='data')
    nq_bars, composite_bars = loader.load_all_data(
        nq_file=data_config['nq_file'],
        stock_files=data_config['stock_files']
    )

    print(f"\nLoaded data:")
    print(f"  NQ bars: {len(nq_bars):,}")
    print(f"  Composite bars: {len(composite_bars):,}")

    # Process indicators
    processor = IndicatorProcessor(
        zone21_lookback=zone21_config['lookback'],
        atr_period=atr_config['period'],
        atr_multiple=atr_config['multiple']
    )

    results = processor.process_data(nq_bars, composite_bars)

    # Launch interactive viewer
    print("\nLaunching interactive viewer...")
    print("\nControls:")
    print("  Left Arrow / Previous Button: Go to previous day")
    print("  Right Arrow / Next Button: Go to next day")
    print("  Home / First Day Button: Go to first day")
    print("  End / Last Day Button: Go to last day")
    print("\nCharts show:")
    print("  - Blue dashed lines: Swing Highs")
    print("  - Purple dashed lines: Swing Lows")
    print("  - Green highlighted bars: Bullish ATR Bars")
    print("  - Orange highlighted bars: Bearish ATR Bars")
    print("\n" + "="*80 + "\n")

    launch_day_viewer(
        nq_bars=results['nq_rth_bars'],
        composite_bars=results['composite_rth_bars'],
        nq_indicators=results['nq_indicators'],
        composite_indicators=results['composite_indicators'],
        trading_days=results['trading_days']
    )


if __name__ == "__main__":
    main()
