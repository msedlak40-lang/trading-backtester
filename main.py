#!/usr/bin/env python3
"""
Main entry point for the trading backtest system.
"""
import yaml
from pathlib import Path
from src.engine.backtest import Backtester


def load_config(config_file: str = "config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    """Main execution function."""
    print("=" * 60)
    print("TRADING BACKTEST SYSTEM")
    print("Divergence Strategy with Zone21B and ATR Bars")
    print("=" * 60)

    # Load configuration
    print("\nLoading configuration...")
    config = load_config("config.yaml")

    # Create results directory if needed
    Path("results").mkdir(exist_ok=True)

    # Initialize backtester
    print("Initializing backtester...")
    backtester = Backtester(config)

    # Load data
    backtester.load_data()

    # Run backtest
    stats = backtester.run()

    # Print and save results
    if config['output']['print_summary']:
        backtester.print_summary(stats)

    backtester.save_results(stats)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
