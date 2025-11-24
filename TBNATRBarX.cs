#region Using declarations
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Xml.Serialization;
using NinjaTrader.Cbi;
using NinjaTrader.Gui;
using NinjaTrader.Gui.Chart;
using NinjaTrader.Gui.SuperDom;
using NinjaTrader.Gui.Tools;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript;
using NinjaTrader.Core.FloatingPoint;
using NinjaTrader.NinjaScript.DrawingTools;
#endregion

//This namespace holds Indicators in this folder and is required. Do not change it. 
namespace NinjaTrader.NinjaScript.Indicators
{
	public class TBNATRBarX : Indicator
	{
		//private double openLinePrice = double.MinValue;
		//private int barIndex;
		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description									= @"Compares most recent bar range to the ATR range";
				Name										= "TBNATRBarX";
				Calculate									= Calculate.OnEachTick;
				IsOverlay									= false;
				DisplayInDataBox							= true;
				DrawOnPricePanel							= true;
				DrawHorizontalGridLines						= true;
				DrawVerticalGridLines						= true;
				//DrawOpenToCloseLine 						= false;
				PaintPriceMarkers							= true;
				ScaleJustification							= NinjaTrader.Gui.Chart.ScaleJustification.Right;
				//Disable this property if your indicator requires custom values that cumulate with each new market data event. 
				//See Help Guide for additional information.
				IsSuspendedWhileInactive					= true;
			
			}
			else if (State == State.Configure)
			{				
			}
		}
			public double Multiple { get; set; }
			//public bool DrawOpenToCloseLine { get; set; }
			
			protected override void OnBarUpdate()
		{
				double atr = Math.Ceiling(ATR(7)[0]/.01) * .01;
				double highlowRange = Math.Ceiling(Math.Abs(Open[0] - Close[0]) / .01) * .01;
				double threshold = atr * .75;
				
				//bool bullcondition = Close[0] > Open[0] && highlowRange >= Math.Ceiling((Multiple * atr)/.01) * .01;
				//bool bearcondition = Close[0] < Open[0] && highlowRange >= Math.Ceiling((Multiple * atr)/.01) * .01;
				//double atr = ATR(7)[0];
				//double highlowRange = Math.Abs(Open[0] - Close[0]);
			
			//Print("DateTime " + Time[0]);
			//Print("ATR " + atr);
			//Print("Range " + highlowRange);
			//Print("Threshold " + threshold);
			//Print("Bull " + bullcondition);
			//Print("Bear " + bearcondition);
			
				
				if (Close[0] > Open[0] && highlowRange >= Math.Ceiling((Multiple * atr)/.01) * .01)
				
					{
						BarBrush = Brushes.Green;
						//CandleOutlineBrushes[0] = Brushes.Green;
					//	if (DrawOpenToCloseLine)
                  //  {
						// Save the index of the current bar
                     //   barIndex = CurrentBars[0];
						// Add logic to draw a line from open to close
                   //Draw.HorizontalLine(this, "OpenToCloseLine", Open[0], Brushes.Blue);
                    }
				//	openLinePrice = Close[0];
                   
					
				else if (Close[0] < Open[0] && highlowRange >= Math.Ceiling((Multiple * atr)/.01) * .01)
					{
					BarBrush = Brushes.Magenta;
					}
					
				
					//}			
				else
				{
					BarBrush = null;
				}
			//}
			// protected override void OnRender(ChartControl chartControl, ChartScale chartScale)
		//{
		//base.OnRender(chartControl, chartScale);

            // Check if the user wants to draw the line and if it's the current bar
           // if (DrawOpenToCloseLine && barIndex == CurrentBars[0])
			//{
				// Draw a line manually starting from the current bar
              //  Draw.Line(this, "OpenToCloseLine", barIndex, openLinePrice, barIndex + 1, Close[0], Brushes.Blue);
	}
		}
	}

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private TBNATRBarX[] cacheTBNATRBarX;
		public TBNATRBarX TBNATRBarX()
		{
			return TBNATRBarX(Input);
		}

		public TBNATRBarX TBNATRBarX(ISeries<double> input)
		{
			if (cacheTBNATRBarX != null)
				for (int idx = 0; idx < cacheTBNATRBarX.Length; idx++)
					if (cacheTBNATRBarX[idx] != null &&  cacheTBNATRBarX[idx].EqualsInput(input))
						return cacheTBNATRBarX[idx];
			return CacheIndicator<TBNATRBarX>(new TBNATRBarX(), input, ref cacheTBNATRBarX);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.TBNATRBarX TBNATRBarX()
		{
			return indicator.TBNATRBarX(Input);
		}

		public Indicators.TBNATRBarX TBNATRBarX(ISeries<double> input )
		{
			return indicator.TBNATRBarX(input);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.TBNATRBarX TBNATRBarX()
		{
			return indicator.TBNATRBarX(Input);
		}

		public Indicators.TBNATRBarX TBNATRBarX(ISeries<double> input )
		{
			return indicator.TBNATRBarX(input);
		}
	}
}

#endregion
