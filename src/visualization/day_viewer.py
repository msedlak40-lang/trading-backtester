"""
Day-by-day interactive chart viewer
Shows NQ and Composite charts with Zone21B swings and ATR bars
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
from typing import List, Dict
from datetime import datetime
from src.data.data_structures import Bar
from src.indicators.indicator_tracker import IndicatorTracker


class DayByDayViewer:
    """Interactive viewer for scrolling through trading days"""

    def __init__(self, nq_bars: List[Bar], composite_bars: List[Bar],
                 nq_indicators: IndicatorTracker, composite_indicators: IndicatorTracker,
                 trading_days: List[str]):
        """
        Initialize day-by-day viewer

        Args:
            nq_bars: NQ bars (RTH only)
            composite_bars: Composite bars (RTH only)
            nq_indicators: NQ indicator tracker
            composite_indicators: Composite indicator tracker
            trading_days: List of trading days (YYYY-MM-DD format)
        """
        self.nq_bars = nq_bars
        self.composite_bars = composite_bars
        self.nq_indicators = nq_indicators
        self.composite_indicators = composite_indicators
        self.trading_days = trading_days
        self.current_day_index = 0

        # Create bar lookup by date
        self._create_day_lookup()

        # Setup figure
        self._setup_figure()

        # Display first day
        self.update_display()

    def _create_day_lookup(self):
        """Create lookup dictionaries for bars by day"""
        self.nq_by_day = {}
        self.composite_by_day = {}

        for bar in self.nq_bars:
            day_str = bar.timestamp.date().isoformat()
            if day_str not in self.nq_by_day:
                self.nq_by_day[day_str] = []
            self.nq_by_day[day_str].append(bar)

        for bar in self.composite_bars:
            day_str = bar.timestamp.date().isoformat()
            if day_str not in self.composite_by_day:
                self.composite_by_day[day_str] = []
            self.composite_by_day[day_str].append(bar)

    def _setup_figure(self):
        """Setup matplotlib figure and widgets"""
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.canvas.manager.set_window_title('Day-by-Day Chart Viewer')

        # Create grid layout
        # [NQ Chart]
        # [Composite Chart]
        # [Info Panel]
        # [Buttons]

        self.ax_nq = plt.subplot2grid((4, 5), (0, 0), colspan=5, rowspan=1)
        self.ax_comp = plt.subplot2grid((4, 5), (1, 0), colspan=5, rowspan=1)
        self.ax_info = plt.subplot2grid((4, 5), (2, 0), colspan=5, rowspan=1)

        # Navigation buttons
        self.ax_prev = plt.subplot2grid((4, 5), (3, 0), colspan=1)
        self.ax_next = plt.subplot2grid((4, 5), (3, 1), colspan=1)
        self.ax_first = plt.subplot2grid((4, 5), (3, 2), colspan=1)
        self.ax_last = plt.subplot2grid((4, 5), (3, 3), colspan=1)

        self.btn_prev = Button(self.ax_prev, 'Previous (←)')
        self.btn_next = Button(self.ax_next, 'Next (→)')
        self.btn_first = Button(self.ax_first, 'First Day')
        self.btn_last = Button(self.ax_last, 'Last Day')

        self.btn_prev.on_clicked(lambda x: self.previous_day())
        self.btn_next.on_clicked(lambda x: self.next_day())
        self.btn_first.on_clicked(lambda x: self.first_day())
        self.btn_last.on_clicked(lambda x: self.last_day())

        # Keyboard shortcuts
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        # Style
        self.ax_nq.set_facecolor('#f0f0f0')
        self.ax_comp.set_facecolor('#f0f0f0')
        self.ax_info.set_facecolor('#ffffff')
        self.ax_info.set_xticks([])
        self.ax_info.set_yticks([])

    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.key == 'left':
            self.previous_day()
        elif event.key == 'right':
            self.next_day()
        elif event.key == 'home':
            self.first_day()
        elif event.key == 'end':
            self.last_day()

    def previous_day(self):
        """Navigate to previous day"""
        if self.current_day_index > 0:
            self.current_day_index -= 1
            self.update_display()

    def next_day(self):
        """Navigate to next day"""
        if self.current_day_index < len(self.trading_days) - 1:
            self.current_day_index += 1
            self.update_display()

    def first_day(self):
        """Navigate to first day"""
        self.current_day_index = 0
        self.update_display()

    def last_day(self):
        """Navigate to last day"""
        self.current_day_index = len(self.trading_days) - 1
        self.update_display()

    def update_display(self):
        """Update the display with current day's data"""
        day_str = self.trading_days[self.current_day_index]

        # Get bars for this day
        nq_day_bars = self.nq_by_day.get(day_str, [])
        comp_day_bars = self.composite_by_day.get(day_str, [])

        # Get indicators for this day
        nq_day_indicators = self.nq_indicators.get_data_for_day(day_str)
        comp_day_indicators = self.composite_indicators.get_data_for_day(day_str)

        # Clear axes
        self.ax_nq.clear()
        self.ax_comp.clear()
        self.ax_info.clear()

        # Plot charts
        if nq_day_bars:
            self._plot_chart(self.ax_nq, nq_day_bars, nq_day_indicators, "NQ", day_str)
        if comp_day_bars:
            self._plot_chart(self.ax_comp, comp_day_bars, comp_day_indicators, "Composite", day_str)

        # Update info panel
        self._update_info_panel(day_str, nq_day_bars, comp_day_bars,
                                nq_day_indicators, comp_day_indicators)

        plt.draw()

    def _plot_chart(self, ax, bars: List[Bar], indicators: Dict, name: str, day_str: str):
        """
        Plot chart with candlesticks, swings, and ATR bars

        Args:
            ax: Matplotlib axis
            bars: Bars to plot
            indicators: Indicator data for this day
            name: Chart name (NQ or Composite)
            day_str: Day string for title
        """
        if not bars:
            return

        # Plot candlesticks
        for i, bar in enumerate(bars):
            color = 'green' if bar.close >= bar.open else 'red'
            line_color = 'darkgreen' if bar.close >= bar.open else 'darkred'

            # High-low line
            ax.plot([i, i], [bar.low, bar.high], color=line_color, linewidth=1)

            # Body
            height = abs(bar.close - bar.open)
            bottom = min(bar.open, bar.close)
            rect = Rectangle((i - 0.3, bottom), 0.6, height,
                           facecolor=color, edgecolor=line_color, linewidth=1)
            ax.add_patch(rect)

        # Get price range for swing line extension
        all_prices = [bar.high for bar in bars] + [bar.low for bar in bars]
        price_min = min(all_prices)
        price_max = max(all_prices)

        # Plot swing highs (horizontal lines)
        swing_highs = indicators['swing_highs']
        for swing in swing_highs:
            # Draw horizontal line across the chart at swing high price
            ax.axhline(y=swing.price, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)

        # Plot swing lows (horizontal lines)
        swing_lows = indicators['swing_lows']
        for swing in swing_lows:
            # Draw horizontal line across the chart at swing low price
            ax.axhline(y=swing.price, color='purple', linestyle='--', linewidth=1.5, alpha=0.7)

        # Highlight ATR bars
        atr_bars = indicators['atr_bars']
        for atr_bar in atr_bars:
            # Find the bar index in day's bars
            bar_idx = None
            for idx, bar in enumerate(bars):
                if bar.timestamp == atr_bar.timestamp:
                    bar_idx = idx
                    break

            if bar_idx is not None:
                bar = bars[bar_idx]
                # Draw rectangle around ATR bar
                highlight_color = 'lime' if atr_bar.direction == 'BULLISH' else 'orange'
                rect = Rectangle((bar_idx - 0.4, min(bar.open, bar.close)),
                               0.8, abs(bar.close - bar.open),
                               fill=False, edgecolor=highlight_color, linewidth=3)
                ax.add_patch(rect)

        # Formatting
        ax.set_title(f'{name} - {day_str}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Bar Index', fontsize=10)
        ax.set_ylabel('Price', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='blue', linestyle='--', label='Swing High'),
            Line2D([0], [0], color='purple', linestyle='--', label='Swing Low'),
            Line2D([0], [0], color='lime', linewidth=3, label='Bullish ATR Bar'),
            Line2D([0], [0], color='orange', linewidth=3, label='Bearish ATR Bar')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=8)

    def _update_info_panel(self, day_str: str, nq_bars: List[Bar], comp_bars: List[Bar],
                          nq_indicators: Dict, comp_indicators: Dict):
        """Update information panel"""
        self.ax_info.clear()
        self.ax_info.set_xlim(0, 1)
        self.ax_info.set_ylim(0, 1)
        self.ax_info.axis('off')

        # Info text
        info_lines = [
            f"Day {self.current_day_index + 1} of {len(self.trading_days)}: {day_str}",
            "",
            f"NQ Bars: {len(nq_bars)}",
            f"  Swing Highs: {len(nq_indicators['swing_highs'])}",
            f"  Swing Lows: {len(nq_indicators['swing_lows'])}",
            f"  ATR Bars: {len(nq_indicators['atr_bars'])}",
            "",
            f"Composite Bars: {len(comp_bars)}",
            f"  Swing Highs: {len(comp_indicators['swing_highs'])}",
            f"  Swing Lows: {len(comp_indicators['swing_lows'])}",
            f"  ATR Bars: {len(comp_indicators['atr_bars'])}",
            "",
            "Navigation: ← → (Previous/Next) | Home/End (First/Last Day)"
        ]

        y_pos = 0.9
        for line in info_lines:
            self.ax_info.text(0.05, y_pos, line, fontsize=10,
                            verticalalignment='top', family='monospace')
            y_pos -= 0.07

    def show(self):
        """Display the viewer"""
        plt.tight_layout()
        plt.show()


def launch_day_viewer(nq_bars: List[Bar], composite_bars: List[Bar],
                      nq_indicators: IndicatorTracker, composite_indicators: IndicatorTracker,
                      trading_days: List[str]):
    """
    Launch the day-by-day interactive viewer

    Args:
        nq_bars: NQ bars (RTH only)
        composite_bars: Composite bars (RTH only)
        nq_indicators: NQ indicator tracker
        composite_indicators: Composite indicator tracker
        trading_days: List of trading days
    """
    viewer = DayByDayViewer(nq_bars, composite_bars, nq_indicators,
                           composite_indicators, trading_days)
    viewer.show()
