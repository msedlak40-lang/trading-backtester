"""
Interactive Chart Viewer Application
Navigate through divergences with live updating charts
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Button, Slider, CheckButtons
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np
from src.data.data_structures import Bar, Trade


class InteractiveChartViewer:
    """Interactive desktop application for viewing charts with navigation."""

    def __init__(self, nq_bars: List[Bar], composite_bars: List[Bar],
                 divergences: List[Dict], trades: List[Trade]):
        """
        Initialize interactive chart viewer.

        Args:
            nq_bars: NQ futures bars
            composite_bars: Composite bars
            divergences: List of divergences
            trades: List of trades
        """
        self.nq_bars = nq_bars
        self.composite_bars = composite_bars
        self.divergences = divergences
        self.trades = trades

        # Current view state
        self.current_divergence_idx = 0
        self.bars_before = 100
        self.bars_after = 100
        self.show_swings = True
        self.show_divergence_markers = True

        # Create the figure and axes
        self.fig = plt.figure(figsize=(18, 10))
        self.fig.canvas.manager.set_window_title('Trading Backtester - Interactive Chart Viewer')

        # Main chart axes
        self.ax_nq = plt.subplot2grid((3, 4), (0, 0), colspan=4)
        self.ax_comp = plt.subplot2grid((3, 4), (1, 0), colspan=4, sharex=self.ax_nq)

        # Info panel
        self.ax_info = plt.subplot2grid((3, 4), (2, 0), colspan=2)
        self.ax_info.axis('off')

        # Control panel
        self.ax_controls = plt.subplot2grid((3, 4), (2, 2), colspan=2)
        self.ax_controls.axis('off')

        # Navigation buttons
        self.ax_prev = plt.axes([0.35, 0.02, 0.1, 0.04])
        self.ax_next = plt.axes([0.55, 0.02, 0.1, 0.04])
        self.ax_first = plt.axes([0.20, 0.02, 0.1, 0.04])
        self.ax_last = plt.axes([0.70, 0.02, 0.1, 0.04])

        self.btn_prev = Button(self.ax_prev, 'Previous (←)')
        self.btn_next = Button(self.ax_next, 'Next (→)')
        self.btn_first = Button(self.ax_first, 'First')
        self.btn_last = Button(self.ax_last, 'Last')

        self.btn_prev.on_clicked(self.prev_divergence)
        self.btn_next.on_clicked(self.next_divergence)
        self.btn_first.on_clicked(self.first_divergence)
        self.btn_last.on_clicked(self.last_divergence)

        # Context slider
        self.ax_slider = plt.axes([0.15, 0.08, 0.7, 0.02])
        self.slider = Slider(self.ax_slider, 'Context (bars)', 10, 500,
                            valinit=100, valstep=10)
        self.slider.on_changed(self.update_context)

        # Connect keyboard events
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        # Initial plot
        self.update_charts()

        plt.tight_layout()

    def on_key_press(self, event):
        """Handle keyboard shortcuts."""
        if event.key == 'right' or event.key == 'n':
            self.next_divergence(None)
        elif event.key == 'left' or event.key == 'p':
            self.prev_divergence(None)
        elif event.key == 'home':
            self.first_divergence(None)
        elif event.key == 'end':
            self.last_divergence(None)
        elif event.key == 'q':
            plt.close(self.fig)

    def prev_divergence(self, event):
        """Go to previous divergence."""
        if self.current_divergence_idx > 0:
            self.current_divergence_idx -= 1
            self.update_charts()

    def next_divergence(self, event):
        """Go to next divergence."""
        if self.current_divergence_idx < len(self.divergences) - 1:
            self.current_divergence_idx += 1
            self.update_charts()

    def first_divergence(self, event):
        """Go to first divergence."""
        self.current_divergence_idx = 0
        self.update_charts()

    def last_divergence(self, event):
        """Go to last divergence."""
        self.current_divergence_idx = len(self.divergences) - 1
        self.update_charts()

    def update_context(self, val):
        """Update context window size."""
        self.bars_before = int(val)
        self.bars_after = int(val)
        self.update_charts()

    def update_charts(self):
        """Update both charts based on current state."""
        # Clear previous plots
        self.ax_nq.clear()
        self.ax_comp.clear()
        self.ax_info.clear()
        self.ax_info.axis('off')
        self.ax_controls.clear()
        self.ax_controls.axis('off')

        if not self.divergences:
            self.ax_info.text(0.5, 0.5, 'No divergences to display',
                            ha='center', va='center', fontsize=14)
            self.fig.canvas.draw()
            return

        # Get current divergence
        div = self.divergences[self.current_divergence_idx]
        center_idx = div['bar_index']

        # Calculate window
        start_idx = max(0, center_idx - self.bars_before)
        end_idx = min(len(self.nq_bars), center_idx + self.bars_after)

        # Slice data
        nq_slice = self.nq_bars[start_idx:end_idx]
        comp_slice = self.composite_bars[start_idx:end_idx]

        # Plot NQ
        self._plot_candlesticks(self.ax_nq, nq_slice, 'NQ Futures', 'blue')

        # Plot Composite
        self._plot_candlesticks(self.ax_comp, comp_slice, 'Composite (7 Stocks)', 'green')

        # Mark divergence point
        div_bar_in_slice = center_idx - start_idx
        if 0 <= div_bar_in_slice < len(nq_slice):
            div_time = nq_slice[div_bar_in_slice].timestamp

            # Vertical line at divergence
            self.ax_nq.axvline(div_time, color='red', linewidth=2, linestyle='--',
                              alpha=0.7, label='Divergence')
            self.ax_comp.axvline(div_time, color='red', linewidth=2, linestyle='--', alpha=0.7)

            # Mark on NQ (made new high/low)
            if div['type'] == 'BEARISH':
                nq_price = div['nq_close']
                self.ax_nq.scatter(div_time, nq_price, s=300, marker='^',
                                  color='red', edgecolors='black', linewidths=2, zorder=10)
                self.ax_nq.text(div_time, nq_price, f"  NQ: {nq_price:.2f}\n  Swing: {div['nq_swing_high']:.2f}",
                              fontsize=9, verticalalignment='bottom', bbox=dict(boxstyle='round',
                              facecolor='red', alpha=0.7))

                # Mark on Composite (did NOT make new high)
                comp_price = div['comp_close']
                self.ax_comp.scatter(div_time, comp_price, s=300, marker='o',
                                    color='orange', edgecolors='black', linewidths=2, zorder=10)
                self.ax_comp.text(div_time, comp_price, f"  Comp: {comp_price:.2f}\n  Swing: {div['comp_swing_high']:.2f}",
                                fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round',
                                facecolor='orange', alpha=0.7))

            else:  # BULLISH
                nq_price = div['nq_close']
                self.ax_nq.scatter(div_time, nq_price, s=300, marker='v',
                                  color='lime', edgecolors='black', linewidths=2, zorder=10)
                self.ax_nq.text(div_time, nq_price, f"  NQ: {nq_price:.2f}\n  Swing: {div['nq_swing_low']:.2f}",
                              fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round',
                              facecolor='lime', alpha=0.7))

                # Mark on Composite
                comp_price = div['comp_close']
                self.ax_comp.scatter(div_time, comp_price, s=300, marker='o',
                                    color='cyan', edgecolors='black', linewidths=2, zorder=10)
                self.ax_comp.text(div_time, comp_price, f"  Comp: {comp_price:.2f}\n  Swing: {div['comp_swing_low']:.2f}",
                                fontsize=9, verticalalignment='bottom', bbox=dict(boxstyle='round',
                                facecolor='cyan', alpha=0.7))

        # Mark any trades in this window
        for trade in self.trades:
            if start_idx <= trade.entry_bar < end_idx:
                self._mark_trade(self.ax_nq, trade, start_idx)

        # Format axes
        self.ax_nq.legend(loc='upper left')
        self.ax_nq.grid(True, alpha=0.3)
        self.ax_comp.grid(True, alpha=0.3)

        # Format x-axis
        self.ax_comp.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
        self.ax_comp.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.setp(self.ax_comp.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Update info panel
        self._update_info_panel(div)

        # Update controls panel
        self._update_controls_panel()

        # Redraw
        self.fig.canvas.draw()

    def _plot_candlesticks(self, ax, bars: List[Bar], title: str, color: str):
        """Plot candlestick chart."""
        for bar in bars:
            # Determine color
            if bar.close >= bar.open:
                body_color = 'green'
                edge_color = 'darkgreen'
            else:
                body_color = 'red'
                edge_color = 'darkred'

            # High-low line
            ax.plot([bar.timestamp, bar.timestamp], [bar.low, bar.high],
                   color='black', linewidth=0.8, alpha=0.6)

            # Body
            height = abs(bar.close - bar.open)
            if height < 0.01:  # Doji
                height = 0.5
            bottom = min(bar.open, bar.close)

            width = timedelta(seconds=30)  # 30 seconds width
            rect = Rectangle((bar.timestamp - width/2, bottom), width, height,
                           facecolor=body_color, edgecolor=edge_color,
                           linewidth=0.5, alpha=0.7)
            ax.add_patch(rect)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Price', fontsize=12)

    def _mark_trade(self, ax, trade: Trade, offset: int):
        """Mark trade on chart."""
        entry_color = 'red' if trade.direction == 'SHORT' else 'lime'
        exit_color = 'green' if trade.pnl > 0 else 'red'

        # Entry
        marker = 'v' if trade.direction == 'SHORT' else '^'
        ax.scatter(trade.entry_time, trade.entry_price, s=400, marker=marker,
                  color=entry_color, edgecolors='black', linewidths=2, zorder=10)

        # Exit
        if trade.exit_time:
            ax.scatter(trade.exit_time, trade.exit_price, s=400, marker='X',
                      color=exit_color, edgecolors='black', linewidths=2, zorder=10)

            # Connect line
            ax.plot([trade.entry_time, trade.exit_time],
                   [trade.entry_price, trade.exit_price],
                   color=exit_color, linewidth=2, linestyle='--', alpha=0.6)

            # Stop and target lines
            ax.axhline(trade.stop_price, color='red', linestyle=':', linewidth=1.5, alpha=0.5)
            ax.axhline(trade.target_price, color='green', linestyle=':', linewidth=1.5, alpha=0.5)

    def _update_info_panel(self, div: Dict):
        """Update info panel with divergence details."""
        info_text = f"""
DIVERGENCE #{self.current_divergence_idx + 1} of {len(self.divergences)}

Type: {div['type']}
Time: {div['timestamp']}

NQ:
  Close: {div['nq_close']:.2f}
  Swing: {div.get('nq_swing_high', div.get('nq_swing_low', 'N/A')):.2f}

Composite:
  Close: {div['comp_close']:.2f}
  Swing: {div.get('comp_swing_high', div.get('comp_swing_low', 'N/A')):.2f}

Status: {div.get('status', 'N/A')}
        """

        self.ax_info.text(0.1, 0.5, info_text, fontsize=11, family='monospace',
                         verticalalignment='center')

    def _update_controls_panel(self):
        """Update controls panel."""
        controls_text = f"""
KEYBOARD SHORTCUTS:
  ← / P : Previous divergence
  → / N : Next divergence
  Home  : First divergence
  End   : Last divergence
  Q     : Quit

CONTEXT: {self.bars_before} bars before/after
        """

        self.ax_controls.text(0.1, 0.5, controls_text, fontsize=10, family='monospace',
                            verticalalignment='center')

    def show(self):
        """Display the interactive viewer."""
        plt.show()


def launch_interactive_viewer(nq_bars: List[Bar], composite_bars: List[Bar],
                              divergences: List[Dict], trades: List[Trade]):
    """
    Launch the interactive chart viewer.

    Args:
        nq_bars: NQ futures bars
        composite_bars: Composite bars
        divergences: List of divergences
        trades: List of trades
    """
    print("\n" + "=" * 60)
    print("LAUNCHING INTERACTIVE CHART VIEWER")
    print("=" * 60)
    print("\nControls:")
    print("  Buttons: Previous / Next / First / Last")
    print("  Keyboard: ← → (arrows), P/N (prev/next), Home/End, Q (quit)")
    print("  Slider: Adjust context window (bars before/after)")
    print("\n" + "=" * 60)

    viewer = InteractiveChartViewer(nq_bars, composite_bars, divergences, trades)
    viewer.show()
