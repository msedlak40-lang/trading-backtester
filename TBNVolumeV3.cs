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
	public class TBNVolumeV3 : Indicator
	{
		private bool supportedBarsPeriodType;
		//private List<Indicator> additionalIndicators = new List<Indicator>();
		
		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description									= @"Difference between two instruments";
				Name										= "TBN Volume_V3";
				Calculate									= Calculate.OnBarClose;
				IsOverlay									= true;
				DisplayInDataBox							= true;
				DrawOnPricePanel							= true;
				DrawHorizontalGridLines						= true;
				DrawVerticalGridLines						= true;
				PaintPriceMarkers							= true;
				ScaleJustification							= NinjaTrader.Gui.Chart.ScaleJustification.Right;
				//Disable this property if your indicator requires custom values that cumulate with each new market data event. 
				//See Help Guide for additional information.
				IsSuspendedWhileInactive					= true;
				Symbol1										= "aapl";
				Symbol2										= "msft";
				Symbol3										= "tsla";
				Symbol4										= "meta";
				Symbol5										= "amzn";
				Symbol6										= "googl";
				Symbol7										= "nvda";
				supportedBarsPeriodType						= false;
				AddPlot(Brushes.Gray, "Open");
				AddPlot(Brushes.ForestGreen, "High");
				AddPlot(Brushes.Red, "Low");
				AddPlot(Brushes.Gray, "Close");
			}
			else if (State == State.Configure)
			{
				switch (BarsPeriod.BarsPeriodType)
				{
					case BarsPeriodType.Day:
					case BarsPeriodType.Week:
					case BarsPeriodType.Month:
					case BarsPeriodType.Year:
					case BarsPeriodType.Minute:
					case BarsPeriodType.Second:
						AddDataSeries(Symbol1, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						AddDataSeries(Symbol2, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						AddDataSeries(Symbol3, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						AddDataSeries(Symbol4, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						AddDataSeries(Symbol5, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						AddDataSeries(Symbol6, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						AddDataSeries(Symbol7, BarsPeriod.BarsPeriodType, BarsPeriod.Value);
						supportedBarsPeriodType = true;
						
						// Add additional indicators to the same panel
						//var ema = EMA(Closes[0], 20);
						//AddToChart(ema);
						
						
						break;
					default:
						break;						
				}
			}
			else if (State == State.DataLoaded)
			{
				if (!supportedBarsPeriodType)
				{
					throw new ArgumentException("Input series Period must be time-based (Minute,Day,Week,Month,Year,or Second).");
				}
			}
		}

		protected override void OnBarUpdate()
		{
			if (CurrentBars[0] < 1 || CurrentBars[1] < 1 || CurrentBars[2] < 1)// || CurrentBars[3] < 1 )//|| CurrentBars[4] < 1 || CurrentBars[5] < 1 || CurrentBars[6] < 1)
				return;
			
			Values[0][0] = Opens[1][0] + Opens[2][0] + Opens[3][0] + Opens[4][0] + Opens[5][0] + Opens[6][0] + Opens[7][0];
			Values[1][0] = Highs[1][0] + Lows[2][0] + Lows[3][0] + Lows[4][0] + Lows[5][0] + Lows[6][0] + Lows[7][0];
			Values[2][0] = Lows[1][0] + Highs[2][0] + Highs[3][0] + Highs[4][0] + Highs[5][0] + Highs[6][0] + Highs[7][0];
			Values[3][0] = Closes[1][0] + Closes[2][0] + Closes[3][0] + Closes[4][0] + Closes[5][0] + Closes[6][0] + Closes[7][0];
		
		}

	    protected override void OnRender(ChartControl chartControl, ChartScale chartScale)
        {
			try
			{
			var  w = chartControl.GetBarPaintWidth(chartControl.BarsArray[0]);
			using (var upBrush = new SharpDX.Direct2D1.SolidColorBrush(RenderTarget, SharpDX.Color.LimeGreen))
            {
				using (var downBrush = new SharpDX.Direct2D1.SolidColorBrush(RenderTarget, SharpDX.Color.Red))
				{
					using (var lineBrush = new SharpDX.Direct2D1.SolidColorBrush(RenderTarget, SharpDX.Color.Black))
					{
						// loop through only the rendered bars on the chart
						for(int barIndex = ChartBars.FromIndex; barIndex <= ChartBars.ToIndex; barIndex++)
						{
							var px = chartControl.GetXByBarIndex(ChartBars, barIndex);

							{
								 var yhigh = chartScale.GetYByValue(Values[1].GetValueAt(barIndex));// + Values[4].GetValueAt(barIndex)); // Adjust index if needed
                				 var ylow = chartScale.GetYByValue(Values[2].GetValueAt(barIndex)); // + Values[5].GetValueAt(barIndex)); // Adjust index if needed
								
								RenderTarget.DrawLine(new SharpDX.Vector2(px, yhigh), new SharpDX.Vector2(px, ylow), lineBrush);
							}
						
							{
								var yopen = chartScale.GetYByValue(Values[0].GetValueAt(barIndex)); // + Values[3].GetValueAt(barIndex)); // Adjust index if needed
                				var yclose = chartScale.GetYByValue(Values[3].GetValueAt(barIndex)); // + Values[6].GetValueAt(barIndex)); // Adjust index if needed
								
								if (yopen > yclose)
								{
									var r = new SharpDX.RectangleF(px - w / 2, yclose, w - 2, yopen - yclose);
			                    	RenderTarget.FillRectangle(r, upBrush);
									RenderTarget.DrawRectangle(r, lineBrush);
								}
								else
								{
									var r = new SharpDX.RectangleF(px - w / 2, yopen, w - 2, yclose - yopen);
			                    	RenderTarget.FillRectangle(r, downBrush);
									RenderTarget.DrawRectangle(r, lineBrush);
								}
							}
		                }
					}
				}
			}
			}
			catch (Exception e)
			{
				Print(e);
				throw;
			}
        }

		#region Properties

		[NinjaScriptProperty]
		[Display(Name="Symbol1", Description="Symbol 1; e.g. ^UVOL", Order=1, GroupName="Parameters")]
		public string Symbol1
		{ get; set; }
		
		[NinjaScriptProperty]
		[Display(Name="Symbol2", Description="Symbol 2; e.g. ^DVOL", Order=2, GroupName="Parameters")]
		public string Symbol2
		{ get; set; }
		
		[NinjaScriptProperty]
		[Display(Name="Symbol3", Description="Symbol 3; e.g. ^DVOL", Order=3, GroupName="Parameters")]
		public string Symbol3
		{ get; set; }
		
		[NinjaScriptProperty]
		[Display(Name="Symbol4", Description="Symbol 4; e.g. ^DVOL", Order=4, GroupName="Parameters")]
		public string Symbol4
		{ get; set; }
		
		[NinjaScriptProperty]
		[Display(Name="Symbol5", Description="Symbol 5; e.g. ^DVOL", Order=5, GroupName="Parameters")]
		public string Symbol5
		{ get; set; }
		
		[NinjaScriptProperty]
		[Display(Name="Symbol6", Description="Symbol 6; e.g. ^DVOL", Order=6, GroupName="Parameters")]
		public string Symbol6
		{ get; set; }
		
		[NinjaScriptProperty]
		[Display(Name="Symbol7", Description="Symbol 7; e.g. ^DVOL", Order=7, GroupName="Parameters")]
		public string Symbol7
		{ get; set; }
		
		#endregion

	}
}

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private TBNVolumeV3[] cacheTBNVolumeV3;
		public TBNVolumeV3 TBNVolumeV3(string symbol1, string symbol2, string symbol3, string symbol4, string symbol5, string symbol6, string symbol7)
		{
			return TBNVolumeV3(Input, symbol1, symbol2, symbol3, symbol4, symbol5, symbol6, symbol7);
		}

		public TBNVolumeV3 TBNVolumeV3(ISeries<double> input, string symbol1, string symbol2, string symbol3, string symbol4, string symbol5, string symbol6, string symbol7)
		{
			if (cacheTBNVolumeV3 != null)
				for (int idx = 0; idx < cacheTBNVolumeV3.Length; idx++)
					if (cacheTBNVolumeV3[idx] != null && cacheTBNVolumeV3[idx].Symbol1 == symbol1 && cacheTBNVolumeV3[idx].Symbol2 == symbol2 && cacheTBNVolumeV3[idx].Symbol3 == symbol3 && cacheTBNVolumeV3[idx].Symbol4 == symbol4 && cacheTBNVolumeV3[idx].Symbol5 == symbol5 && cacheTBNVolumeV3[idx].Symbol6 == symbol6 && cacheTBNVolumeV3[idx].Symbol7 == symbol7 && cacheTBNVolumeV3[idx].EqualsInput(input))
						return cacheTBNVolumeV3[idx];
			return CacheIndicator<TBNVolumeV3>(new TBNVolumeV3(){ Symbol1 = symbol1, Symbol2 = symbol2, Symbol3 = symbol3, Symbol4 = symbol4, Symbol5 = symbol5, Symbol6 = symbol6, Symbol7 = symbol7 }, input, ref cacheTBNVolumeV3);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.TBNVolumeV3 TBNVolumeV3(string symbol1, string symbol2, string symbol3, string symbol4, string symbol5, string symbol6, string symbol7)
		{
			return indicator.TBNVolumeV3(Input, symbol1, symbol2, symbol3, symbol4, symbol5, symbol6, symbol7);
		}

		public Indicators.TBNVolumeV3 TBNVolumeV3(ISeries<double> input , string symbol1, string symbol2, string symbol3, string symbol4, string symbol5, string symbol6, string symbol7)
		{
			return indicator.TBNVolumeV3(input, symbol1, symbol2, symbol3, symbol4, symbol5, symbol6, symbol7);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.TBNVolumeV3 TBNVolumeV3(string symbol1, string symbol2, string symbol3, string symbol4, string symbol5, string symbol6, string symbol7)
		{
			return indicator.TBNVolumeV3(Input, symbol1, symbol2, symbol3, symbol4, symbol5, symbol6, symbol7);
		}

		public Indicators.TBNVolumeV3 TBNVolumeV3(ISeries<double> input , string symbol1, string symbol2, string symbol3, string symbol4, string symbol5, string symbol6, string symbol7)
		{
			return indicator.TBNVolumeV3(input, symbol1, symbol2, symbol3, symbol4, symbol5, symbol6, symbol7);
		}
	}
}

#endregion
