"""
Chart visualization for NQ and Composite with divergences and trades.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np
from src.data.data_structures import Bar, Trade


class ChartVisualizer:
    """Visualize NQ and Composite charts with divergences and trades."""

    def __init__(self, nq_bars: List[Bar], composite_bars: List[Bar],
                 divergences: List[Dict], trades: List[Trade],
                 zone_nq_state_history: Optional[List] = None,
                 zone_comp_state_history: Optional[List] = None):
        """
        Initialize visualizer.

        Args:
            nq_bars: NQ futures bars
            composite_bars: Composite bars
            divergences: List of divergence detections
            trades: List of executed trades
            zone_nq_state_history: Zone21B state history for NQ (optional)
            zone_comp_state_history: Zone21B state history for composite (optional)
        """
        self.nq_bars = nq_bars
        self.composite_bars = composite_bars
        self.divergences = divergences
        self.trades = trades
        self.zone_nq_state_history = zone_nq_state_history
        self.zone_comp_state_history = zone_comp_state_history

    def plot_overview(self, start_idx: int = 0, end_idx: Optional[int] = None,
                     save_path: Optional[str] = None):
        """
        Plot overview charts showing NQ and Composite side by side.

        Args:
            start_idx: Start bar index
            end_idx: End bar index (None = all)
            save_path: Path to save chart (None = display)
        """
        if end_idx is None:
            end_idx = len(self.nq_bars)

        # Slice data
        nq_slice = self.nq_bars[start_idx:end_idx]
        comp_slice = self.composite_bars[start_idx:end_idx]

        # Filter divergences and trades in range
        div_in_range = [d for d in self.divergences
                       if start_idx <= d['bar_index'] < end_idx]
        trades_in_range = [t for t in self.trades
                          if start_idx <= t.entry_bar < end_idx]

        # Create figure with 2 subplots (stacked)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 12), sharex=True)
        fig.suptitle('Divergence Trading Strategy - NQ vs Composite', fontsize=16, fontweight='bold')

        # Plot NQ chart
        self._plot_instrument(ax1, nq_slice, start_idx, 'NQ Futures', 'blue')

        # Plot Composite chart
        self._plot_instrument(ax2, comp_slice, start_idx, 'Composite (7 Stocks)', 'green')

        # Mark divergences on both charts
        self._mark_divergences(ax1, ax2, div_in_range, start_idx)

        # Mark trades
        self._mark_trades(ax1, trades_in_range, start_idx)

        # Format x-axis
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax2.xaxis.set_major_locator(mdates.HourLocator(interval=4))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Chart saved to: {save_path}")
        else:
            plt.show()

        plt.close()

    def _plot_instrument(self, ax, bars: List[Bar], offset: int, title: str, color: str):
        """Plot candlestick chart for an instrument."""
        timestamps = [bar.timestamp for bar in bars]
        opens = [bar.open for bar in bars]
        highs = [bar.high for bar in bars]
        lows = [bar.low for bar in bars]
        closes = [bar.close for bar in bars]

        # Plot candlesticks
        for i, bar in enumerate(bars):
            # Bar color
            if bar.close >= bar.open:
                # Bullish - green
                bar_color = 'green'
                body_alpha = 0.6
            else:
                # Bearish - red
                bar_color = 'red'
                body_alpha = 0.6

            # High-low line (wick)
            ax.plot([bar.timestamp, bar.timestamp], [bar.low, bar.high],
                   color='black', linewidth=0.5, alpha=0.5)

            # Open-close rectangle (body)
            height = abs(bar.close - bar.open)
            bottom = min(bar.open, bar.close)

            rect = Rectangle((mdates.date2num(bar.timestamp) - 0.0002, bottom),
                           0.0004, height,
                           facecolor=bar_color, edgecolor='black',
                           linewidth=0.5, alpha=body_alpha)
            ax.add_patch(rect)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Price', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()

    def _mark_divergences(self, ax_nq, ax_comp, divergences: List[Dict], offset: int):
        """Mark divergence points on both charts."""
        for div in divergences:
            idx = div['bar_index'] - offset
            if idx < 0 or idx >= len(self.nq_bars):
                continue

            timestamp = div['timestamp']

            if div['type'] == 'BEARISH':
                # Mark on NQ chart (up arrow - NQ made new high)
                nq_price = div['nq_close']
                ax_nq.scatter(timestamp, nq_price, marker='^', s=200,
                            color='red', edgecolors='black', linewidths=1.5,
                            label='Divergence' if idx == 0 else '', zorder=5)
                ax_nq.annotate('BEARISH\nDIV', xy=(timestamp, nq_price),
                             xytext=(0, 20), textcoords='offset points',
                             fontsize=8, ha='center',
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.7),
                             arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

                # Mark on Composite (no new high)
                comp_price = div['comp_close']
                ax_comp.scatter(timestamp, comp_price, marker='o', s=150,
                              color='orange', edgecolors='black', linewidths=1.5,
                              zorder=5)

            else:  # BULLISH
                # Mark on NQ chart (down arrow - NQ made new low)
                nq_price = div['nq_close']
                ax_nq.scatter(timestamp, nq_price, marker='v', s=200,
                            color='lime', edgecolors='black', linewidths=1.5,
                            label='Divergence' if idx == 0 else '', zorder=5)
                ax_nq.annotate('BULLISH\nDIV', xy=(timestamp, nq_price),
                             xytext=(0, -20), textcoords='offset points',
                             fontsize=8, ha='center',
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='lime', alpha=0.7),
                             arrowprops=dict(arrowstyle='->', color='lime', lw=1.5))

                # Mark on Composite (no new low)
                comp_price = div['comp_close']
                ax_comp.scatter(timestamp, comp_price, marker='o', s=150,
                              color='cyan', edgecolors='black', linewidths=1.5,
                              zorder=5)

    def _mark_trades(self, ax, trades: List[Trade], offset: int):
        """Mark trade entries and exits."""
        for trade in trades:
            # Entry marker
            if trade.direction == 'LONG':
                entry_color = 'lime'
                entry_marker = '^'
                exit_color = 'green' if trade.pnl > 0 else 'red'
            else:  # SHORT
                entry_color = 'red'
                entry_marker = 'v'
                exit_color = 'green' if trade.pnl > 0 else 'red'

            # Plot entry
            ax.scatter(trade.entry_time, trade.entry_price, marker=entry_marker,
                      s=300, color=entry_color, edgecolors='black', linewidths=2,
                      label='Entry', zorder=10)
            ax.annotate(f'{trade.direction}\nENTRY\n${trade.entry_price:.2f}',
                       xy=(trade.entry_time, trade.entry_price),
                       xytext=(20, 20 if trade.direction == 'LONG' else -20),
                       textcoords='offset points',
                       fontsize=9, ha='left', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor=entry_color, alpha=0.8),
                       arrowprops=dict(arrowstyle='->', color=entry_color, lw=2))

            # Plot exit
            if trade.exit_time:
                ax.scatter(trade.exit_time, trade.exit_price, marker='X',
                          s=300, color=exit_color, edgecolors='black', linewidths=2,
                          label='Exit', zorder=10)
                ax.annotate(f'EXIT\n{trade.exit_reason}\n${trade.exit_price:.2f}\n'
                          f'P&L: ${trade.pnl:.2f}',
                           xy=(trade.exit_time, trade.exit_price),
                           xytext=(20, -20 if trade.direction == 'LONG' else 20),
                           textcoords='offset points',
                           fontsize=9, ha='left', fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor=exit_color, alpha=0.8),
                           arrowprops=dict(arrowstyle='->', color=exit_color, lw=2))

                # Draw line connecting entry to exit
                ax.plot([trade.entry_time, trade.exit_time],
                       [trade.entry_price, trade.exit_price],
                       color=exit_color, linewidth=2, linestyle='--', alpha=0.6)

            # Draw stop and target levels
            if trade.entry_time and trade.exit_time:
                time_range = [trade.entry_time, trade.exit_time]
                # Stop level
                ax.plot(time_range, [trade.stop_price, trade.stop_price],
                       color='red', linewidth=1.5, linestyle=':', label='Stop', alpha=0.7)
                # Target level
                ax.plot(time_range, [trade.target_price, trade.target_price],
                       color='green', linewidth=1.5, linestyle=':', label='Target', alpha=0.7)

    def plot_divergence_detail(self, divergence_index: int, bars_before: int = 50,
                               bars_after: int = 50, save_path: Optional[str] = None):
        """
        Plot detailed view of a specific divergence.

        Args:
            divergence_index: Index in divergences list
            bars_before: Bars to show before divergence
            bars_after: Bars to show after divergence
            save_path: Path to save chart
        """
        if divergence_index >= len(self.divergences):
            print(f"Divergence index {divergence_index} out of range (max: {len(self.divergences)-1})")
            return

        div = self.divergences[divergence_index]
        center_idx = div['bar_index']
        start_idx = max(0, center_idx - bars_before)
        end_idx = min(len(self.nq_bars), center_idx + bars_after)

        # Find any trades in this range
        trades_in_range = [t for t in self.trades
                          if start_idx <= t.entry_bar < end_idx]

        # Plot
        self.plot_overview(start_idx, end_idx, save_path)

    def create_summary_report(self, save_path: str = 'results/chart_summary.png'):
        """Create a summary visualization with key metrics."""
        fig = plt.figure(figsize=(20, 14))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # Main charts (top 2 rows)
        ax_nq = fig.add_subplot(gs[0:2, :])
        ax_comp = fig.add_subplot(gs[2, :], sharex=ax_nq)

        # Plot all data
        self._plot_instrument(ax_nq, self.nq_bars, 0, 'NQ Futures - Full Period', 'blue')
        self._plot_instrument(ax_comp, self.composite_bars, 0, 'Composite (7 Stocks) - Full Period', 'green')

        # Mark all divergences
        self._mark_divergences(ax_nq, ax_comp, self.divergences, 0)

        # Mark all trades
        self._mark_trades(ax_nq, self.trades, 0)

        # Format
        ax_comp.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax_comp.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.setp(ax_comp.xaxis.get_majorticklabels(), rotation=45, ha='right')

        fig.suptitle(f'Trading Strategy Summary - {len(self.divergences)} Divergences, '
                    f'{len(self.trades)} Trades', fontsize=16, fontweight='bold')

        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Summary chart saved to: {save_path}")
        plt.close()


def create_divergence_charts(nq_bars: List[Bar], composite_bars: List[Bar],
                             divergences: List[Dict], trades: List[Trade],
                             output_dir: str = 'results'):
    """
    Create charts for all divergences and a summary.

    Args:
        nq_bars: NQ futures bars
        composite_bars: Composite bars
        divergences: List of divergences
        trades: List of trades
        output_dir: Output directory for charts
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    visualizer = ChartVisualizer(nq_bars, composite_bars, divergences, trades)

    # Create summary chart
    print("\nCreating summary chart...")
    visualizer.create_summary_report(f'{output_dir}/chart_summary.png')

    # Create detailed chart for each divergence
    print(f"\nCreating detailed charts for {len(divergences)} divergences...")
    for i, div in enumerate(divergences):
        print(f"  Chart {i+1}/{len(divergences)}: {div['timestamp']}")
        visualizer.plot_divergence_detail(
            i, bars_before=100, bars_after=100,
            save_path=f'{output_dir}/divergence_{i+1}_{div["timestamp"].strftime("%Y%m%d_%H%M")}.png'
        )

    print(f"\nAll charts saved to {output_dir}/")
