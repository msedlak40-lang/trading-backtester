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
//
	#region
//	G		T
//	  A		  R
//	    I		A
//	      J		  D
//	        I		I
//	          N		  N
//				*		G
	#endregion
//
	public class Zone21B2 : Indicator, ICustomTypeDescriptor
	{
		
		#region Variables
		
		 // Wizard generated variables
		
			#region Indicator Properties
		
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> b A r *
		
			private bool	downBarCheck	= false;
		
			private bool	downBarOne		= false;
			private double	downBarOneLow	= 0;
			private double	downBarOneHigh	= 0;
			private bool	downBarTwo		= false;
			private double	downBarTwoLow	= 0;
			private double	downBarTwoHigh	= 0;
			private double	swingHigh		= 0;
			private int		swingHighBars	= 0;
			private double	insideSwingHigh = 0;
			private bool	takeSwingHigh	= false;
			private bool	takeBarHigh		= false;
		
			private bool	downWithinBar	= false;
			private double	downWithinHigh	= 0;
			private double	downWithinLow	= 0;
		
			private bool	down4thBar		= false;
			private double	down4thBarHigh	= 0;
			private double	down4thBarLow	= 0;
		
			private bool	underBar		= false;
			private double	underBarHigh	= 0;
			private double	underBarLow		= 0;
		
			private bool	iBar1down		= false;
			private double	iBar1downLow	= 0;
			private double	iBar1downHigh	= 0;
		
			private bool	iBar2down		= false;
			private double	iBar2downLow	= 0;
			private double	iBar2downHigh	= 0;
		
			private bool	iBar3down		= false;
			private double	iBar3downLow	= 0;
			private double	iBar3downHigh	= 0;
		
			private double	stored4thLow	= 0;
			private bool	lowerLow		= false;
						
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> Z E T A *
		
			private bool	zetaBar			= false;
		
			private double	zetaBarHigh		= 0;
			private double	zetaBarLow		= 0;
			private double	zetaBarClose	= 0;
		
			private int		closesAboveZ	= 1;
			private bool	zetaBarFT		= false;
		
			private double	possibleLow		= double.MaxValue;
							
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> Z O N E *
		
			private double	oldRunningLow	= double.MaxValue;
			private double	runningLow		= double.MaxValue;
				
			private double	storedSwingHigh	= 0;
		
			private bool	buyZone			= false;
			private double	buyZoneHigh		= 0;
			private double	buyZoneLow		= 0;
			private int		buyZoneCount	= 0;
						
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> b A r *
		
			private bool	upBarCheck		= false;

			private bool	upBarOne		= false;
			private double	upBarOneLow		= 0;
			private double	upBarOneHigh	= 0;
			private bool	upBarTwo		= false;
			private double	upBarTwoLow		= 0;
			private double	upBarTwoHigh	= 0;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			private double	swingLow		= double.MaxValue;
			private double	insideSwingLow	= double.MaxValue;
			private int		swingLowBars	= 0;
			private bool	takeSwingLow	= false;
			private bool	takeBarLow		= false;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			private bool	upWithinBar		= false;
			private double	upWithinHigh	= 0;
			private double	upWithinLow		= 0;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			private bool	up4thBar		= false;
			private double	up4thBarHigh	= 0;
			private double	up4thBarLow		= 0;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			private bool	overBar			= false;
			private double	overBarHigh		= 0;
			private double	overBarLow		= 0;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			private bool	iBar1up			= false;
			private double	iBar1upLow		= 0;
			private double	iBar1upHigh		= 0;
		
			private bool	iBar2up			= false;
			private double	iBar2upLow		= 0;
			private double	iBar2upHigh		= 0;
		
			private bool	iBar3up			= false;
			private double	iBar3upLow		= 0;
			private double	iBar3upHigh		= 0;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			private double	stored4thHigh	= 0;
			private bool	higherHigh		= false;
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> A L P H A *
			private bool	alphaBar		= false;
		
			private double	alphaBarHigh	= 0;
			private double	alphaBarLow		= 0;
			private double	alphaBarClose	= 0;
		
			private int		closesBelowA	= 1;
			private bool	alphaBarFT		= false;
		
			private double	possibleHigh	= 0;
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> Z O N E *
			private double	oldRunningHigh	= 0;
			private double	runningHigh		= 0;
				
			private double	storedSwingLow	= 0;
		
			private bool	sellZone		= false;
			private double	sellZoneHigh	= 0;
			private double	sellZoneLow		= 0;
			private int		sellZoneCount	= 0;
				
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> G L O B A L *
		
			private bool	useSwingLB		= true;
				
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>> D I S P L A Y *
		
			private bool	showColors		= false;
			private bool	showNumbers		= false;
			private bool	showSetupLines	= false;
			private bool	showSymbols		= false;
			private bool	showRunning		= false;
			private bool	showLevels		= false;
			private bool	showZetas		= false;
			private bool	showAlphas		= false;
			private bool	showZones		= false;
			private int		displayTicks	= 320;
			private bool	showResets		= false;
			private int		pixels			= 18;
		
			private int 	opacity 		= 25;
		
			private Brush	buyZoneColor	= Brushes.Blue;
			private Brush	swingHighColor	= Brushes.LightGreen;
			private Brush	swingHighText	= Brushes.SpringGreen;
				
			private Brush	sellZoneColor	= Brushes.Red;
			private Brush	swingLowColor	= Brushes.LightSteelBlue;
			private Brush	swingLowText	= Brushes.DarkOrange;
		
			private Brush	innerBarsColor	= Brushes.LightSteelBlue;
		
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>>
		
			NinjaTrader.Gui.Tools.SimpleFont	fntI			= new NinjaTrader.Gui.Tools.SimpleFont("Book Antiqua", 14);
			NinjaTrader.Gui.Tools.SimpleFont	fntII			= new NinjaTrader.Gui.Tools.SimpleFont("Courier New", 16);
			NinjaTrader.Gui.Tools.SimpleFont	fntIII			= new NinjaTrader.Gui.Tools.SimpleFont("Book Antiqua", 14);
			NinjaTrader.Gui.Tools.SimpleFont	fntIV			= new NinjaTrader.Gui.Tools.SimpleFont("Century Gothic", 15);
			NinjaTrader.Gui.Tools.SimpleFont	fntV			= new NinjaTrader.Gui.Tools.SimpleFont("Book Antiqua", 12);
		
			private int		textCount		= 0;
		
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - > - > - >
		
//			private string	leadType		= "HMA";
		
			#endregion
		
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>>
		
			#region Series
	
			private Series<double>		SIGNAL;
				
			#endregion
		
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>>
		
			#region Classes
		
			// - - - - - - - - - - - - -
					
			public class zoneData
			{
				public double	high			{get;set;}
				public double	low				{get;set;}
				public int		bar0ID			{get;set;}
				public DateTime	timeZoneStart	{get;set;}
				public DateTime	timeZoneEnd		{get;set;}
				public bool		dir				{get;set;}
				public bool		active			{get;set;}
				public zoneData(){
						high			= 0;
						low				= 0;
						bar0ID			= 0;
						timeZoneStart	= DateTime.MinValue;
						timeZoneEnd		= DateTime.MinValue;
						dir				= false;
						active			= true;
				}
			}
					
			// - - - - - - - - - - - - -
					
			public class setupData
			{
				public double	swingHigh			{get;set;}
				public double	swingLow			{get;set;}
				public double	pivot				{get;set;}
				
				public setupData(){
						swingHigh	= 0;
						swingLow	= 0;
						pivot		= 0;
				}
			}
			
			#endregion
		
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>>
		
			#region Lists
			
			public List<zoneData>BUYZONES 			= new List<zoneData>();
			public List<zoneData>SELLZONES 			= new List<zoneData>();
			public List<setupData>SETUP1B			= new List<setupData>();
			public List<setupData>SETUP1A			= new List<setupData>();
		
			#endregion
		
		// Warlock generated variables
		
		#endregion		
		
		//	-	-	-	-	-	-	-	-	>>
		
		#region States
		
		//	-	-	-	-	-	-	-	-	>>
		
		protected override void OnStateChange()
		{
			if (State == State.SetDefaults)
			{
				Description									= @"The Zone21 tells you what mode the market is in...";
				Name										= "Zone21B2";
				Calculate									= Calculate.OnBarClose;
				IsOverlay									= true;
				DisplayInDataBox							= true;
				DrawOnPricePanel							= true;
				DrawHorizontalGridLines						= true;
				DrawVerticalGridLines						= true;
				PaintPriceMarkers							= true;
				ScaleJustification							= NinjaTrader.Gui.Chart.ScaleJustification.Right;
//				ScaleJustification							= NinjaTrader.Gui.Chart.ScaleJustification.Overlay;
				//Disable this property if your indicator requires custom values that cumulate with each new market data event. 
				//See Help Guide for additional information.
				IsSuspendedWhileInactive					= true;
				MaximumBarsLookBack = MaximumBarsLookBack.Infinite;
				
			//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	> V A R S *
				
				printPrimaryBars = false;
				
				//	-	-	-	-	-	>
				
				useUpBarCheck	= false;
				useDownBarCheck	= false;
				
				dataType1		= "LOW";
				lowerTicks		= 1;
				dataType2		= "HIGH";
				higherTicks		= 1;
				
				useUnder		= true;
				useOver			= true;
				
				lookBack		= 4;
				respectBar3		= true;
				respectBar4		= true;
				
				rXlow			= "CLOSE";
				rXhigh			= "CLOSE";
				
				requiredCloses	= 2;
				wholeBarCancel	= false;
				
			//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	> P L O T S *
				
//				AddPlot(new Stroke(Brushes.Transparent, 2),	PlotStyle.Line,	"PLOT");
				
			}
			else if (State == State.Configure)
			{
//				AddDataSeries(Data.BarsPeriodType.Minute, 30);
			}
			else if (State == State.DataLoaded)
			{
				SIGNAL	= new Series<double>(this,MaximumBarsLookBack.TwoHundredFiftySix);
				
				ClearOutputWindow();
			}
		}
		
		#endregion
		
		//	-	-	-	-	-	-	-	-	>>
		
//		#region OnBarUpdate
		
		//	-	-	-	-	-	-	-	-	>>

		protected override void OnBarUpdate()
		{
			if ( CurrentBar < 10 )
			return;
			
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -	
			
			SIGNAL[0] = 0;
			
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			
			bool flip = false;
			
			switch (zoneType)
			{
				case "BUY"		:	flip = false;	break;
				case "SELL"		:	flip = true;	break;
			}
			
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			
//			#region Bar Logic
			
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			if ( useUpBarCheck && !upBarCheck && Close[0] > Open[0] ){
					upBarCheck=true;
					drawSignalTextCenter(showSymbols,ref textCount,"=X=",0,Brushes.DodgerBlue,fntV,Convert.ToInt32(pixels*0));
			}
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			if ( useDownBarCheck && !downBarCheck && Close[0] < Open[0] ){
					downBarCheck=true;
					drawSignalTextCenter(showSymbols,ref textCount,"=X=",0,Brushes.Red,fntV,Convert.ToInt32(pixels*0));
			}
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			
				#region Buy Setup
			
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			
	if ( useFlip ? !flip : true ){
		
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
		
			double priceInput1 = 0;
			double resetXlow = 0;
			
			switch (dataType1)
			{
				case "LOW"		:	priceInput1 = Low[0];	break;
				case "CLOSE"	:	priceInput1 = Close[0];	break;
			}
			
			switch (rXlow)
			{
				case "LOW"		:	resetXlow = Low[0];		break;
				case "CLOSE"	:	resetXlow = Close[0];	break;
			}
			
//			if ( stored4thLow != 0 && priceInput1 <= stored4thLow - lowerTicks * TickSize )
			lowerLow = stored4thLow != 0 && priceInput1 <= stored4thLow - lowerTicks * TickSize;
//			else	lowerLow = false;
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			
			bool recycleUnder = false;
			
			if ( useUnder )
			barUnder(ref recycleUnder,lowerLow,down4thBar,ref underBar,ref underBarHigh,ref underBarLow,ref stored4thLow);	
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			
			if ( runningLow != double.MaxValue ){
					if ( showRunning )
					Draw.Line(this,"Tag226" + CurrentBar , true , 0 , runningLow , 1 , runningLow , Brushes.Blue , DashStyleHelper.Dash , 1 ) ;
					if ( !iBar3down ){
							if ( Low[0] < runningLow )
									runningLow = Low[0];
					}
					else{
							if ( resetXlow < runningLow ){
									if ( !underBar
											&& ( respectBar3 ? !(!downWithinBar && Close[0] < downBarTwoLow) : !respectBar3 )
											&& ( respectBar4 ? (!(!down4thBar && Close[0] < downWithinLow) && !down4thBar) : !respectBar4 ) ){
													resetAllSwitches1B();
													runningLow = double.MaxValue;
													drawSignalTextBelow(showSymbols,ref textCount,"-iX*",0,Brushes.Khaki,fntV,Convert.ToInt32(pixels*0.38));
									}
							}
					}
			}
			
			if ( oldRunningLow != double.MaxValue ){
					if ( showRunning )
					Draw.Line(this,"Tag227" + CurrentBar , true , 0 , oldRunningLow , 1 , oldRunningLow , Brushes.Magenta , DashStyleHelper.Dash , 1 ) ;
					if ( Low[0] < oldRunningLow )
					if ( iBar1down
							&& !underBar
							&& ( respectBar3 ? !(!downWithinBar && Close[0] < downBarTwoLow) : !respectBar3 )
							&& ( respectBar4 ? (!(!down4thBar && Close[0] < downWithinLow) && !down4thBar) : !respectBar4 ) ){
									resetAllSwitches1B();
									runningLow = double.MaxValue;
									drawSignalTextBelow(showSymbols,ref textCount,"-xL*",0,Brushes.OrangeRed,fntV,Convert.ToInt32(pixels*0.38));
					}	
			}

//		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
						
			if ( !downBarOne ){
				if ( useUpBarCheck ? upBarCheck : !useUpBarCheck )
				if ( !underBar )	
					if ( Close[0] < Open[0] ){
							createDownBar(ref downBarOne,ref downBarOneHigh,ref downBarOneLow,"1",Brushes.Gold,Brushes.Yellow,1);
						//	-	-	-	-	-	>
							calculateSwingHigh(false,false,"*sH*");
					}
			}
			else{
				
					if ( !downBarTwo ){
						
							if ( Close[0] > downBarOneHigh ){
									downBarOne = false;
									drawSignalTextAbove(showSymbols,ref textCount,"+R1*",0,Brushes.Yellow,fntIII,pixels);
									SIGNAL[0] = 1;
							}
						
						if ( !underBar )
							if ( Close[0] < downBarOneLow ){
//									if ( lowerLow ){
//											resetAllSwitches1B();
//											stored4thLow = 0;
//											drawSignalTextBelow(showNumbers,ref textCount,"2U",0,Brushes.Magenta,fntIII,Convert.ToInt32(pixels*1));
//									}
//									else{
											createDownBar(ref downBarTwo,ref downBarTwoHigh,ref downBarTwoLow,"2",Brushes.Magenta,Brushes.Magenta,1);
								//	-	-	-	-	-	>
											runningLow = Low[0];
								//	-	-	-	-	-	>
											calculateSwingHigh(false,false,"+s2*");
//									}
							}
					}
					else{
						
						//	-	-	-	-	-	-	-	-	-	>
						
							if ( !takeBarHigh ){
									if ( Close[0] > downBarTwoHigh
											&& !downWithinBar ){
													takeBarHigh = true;
												if ( showSymbols )
													Draw.TriangleUp(this,"Tag101" + CurrentBar, true, 0, Low[0] - 6 * TickSize, Brushes.Black);
									}
							}
							else{
								if ( !underBar )
									insideBarsDown(downWithinBar,Brushes.Yellow,ref iBar1down,ref iBar1downHigh,ref iBar1downLow,
													ref iBar2down,ref iBar2downHigh,ref iBar2downLow,ref iBar3down,ref iBar3downHigh,ref iBar3downLow);
							}
							
						//	-	-	-	-	-	-	-	-	-	>	
						
							if ( !takeSwingHigh ){
									if ( Close[0] > swingHigh
											&& swingHigh != 0 ){
										
												takeSwingHigh = true;
										
												colorBars(showColors,0,Brushes.Cyan);
												
//											if ( showSymbols )
//												Draw.TriangleUp(this,"Tag102" + CurrentBar, true, 0, Low[0] - 4 * TickSize, Brushes.Cyan);
									}
							}
							else{
								
							}
							
						//	-	-	-	-	-	-	-	-	-	>	
							
							if ( !downWithinBar ){
								if ( !underBar )
									if ( Close[0] < Open[0]
											&& Close[0] < downBarTwoLow ){
//													if ( lowerLow ){
//															resetAllSwitches1B();
//															stored4thLow = 0;
//															drawSignalTextBelow(showNumbers,ref textCount,"3U",0,Brushes.Red,
//																					fntIII,Convert.ToInt32(pixels*1));
//													}
//													else{
															createDownBar(ref downWithinBar,ref downWithinHigh,ref downWithinLow,"3",
																			Brushes.Red,Brushes.Red,1);
//													}
									}
							}
							else{
									if ( !takeBarHigh ){
											if ( Close[0] > downWithinHigh
													&& !up4thBar ){
															takeBarHigh = true;
														if ( showSymbols )
															Draw.TriangleUp(this,"Tag102" + CurrentBar, true, 0, Low[0] - 6 * TickSize, Brushes.Blue);
											}
									}
									else{
										if ( !underBar )
											insideBarsDown(down4thBar,Brushes.Red,ref iBar1down,ref iBar1downHigh,ref iBar1downLow,
													ref iBar2down,ref iBar2downHigh,ref iBar2downLow,ref iBar3down,ref iBar3downHigh,ref iBar3downLow);
									}
									
								//	-	-	-	-	-	-	-	-	-	>
									
									barNo4Down(ref recycleUnder,underBar,downWithinLow,lowerLow,ref down4thBar,
													ref down4thBarHigh,ref down4thBarLow,ref stored4thLow);
									
								//	-	-	-	-	-	-	-	-	-	>
									
									drawHL(showSetupLines,downWithinHigh,downWithinLow,Brushes.Coral,Brushes.Brown,"Tag211","Tag212");

							}
							
						//	-	-	-	-	-	-	-	-	-	>
							
							if ( takeBarHigh && takeSwingHigh ){
								
									zetaBar = true;
								
									zetaBarHigh		= High[0];
									zetaBarLow		= Low[0];
									zetaBarClose	= Close[0];
								
									storedSwingHigh = swingHigh;
								
									possibleLow = runningLow;
								
									closesAboveZ = 1;
								
									resetAllSwitches1B();
								
									drawSignalTextAbove(showZetas,ref textCount,"-Z-",0,Brushes.Cyan,fntIII,Convert.ToInt32(pixels*1.62));
							}
							
							if ( !takeBarHigh && takeSwingHigh ){
								
									resetAllSwitches1B();
								
									drawSignalTextAbove(showSymbols,ref textCount,"*INC*",0,Brushes.Silver,fntIII,Convert.ToInt32(pixels*1.62));
							}
														
						//	-	-	-	-	-	-	-	-	-	>
							
							drawHL(showSetupLines,downBarTwoHigh,downBarTwoLow,Brushes.LightPink,Brushes.DeepPink,"Tag213","Tag214");

					}
					
					if ( showLevels )
					if ( swingHigh != 0 )
					Draw.Line(this,"Tag210" + CurrentBar , true , 0 , swingHigh , 1 , swingHigh , swingHighColor , DashStyleHelper.Dash , 2 ) ;
					
					drawHL(showSetupLines,downBarOneHigh,downBarOneLow,Brushes.Lime,Brushes.Orange,"Tag215","Tag216");

			}
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>	
			
			if ( stored4thLow != 0 ){
				
				if ( Low[0] < stored4thLow + displayTicks * TickSize )	
				if ( showLevels )
					Draw.Line(this,"Tag209" + CurrentBar , true , 0 , stored4thLow , 1 , stored4thLow , Brushes.SlateGray , DashStyleHelper.Dash , 2 ) ;
						
					if ( lowerLow ){
							drawSignalTextBelow(showSymbols,ref textCount,"*LL*",0,Brushes.Silver,fntIII,Convert.ToInt32(pixels*2));
//							resetAllSwitches1B();
						if ( useUnder )
						if ( !recycleUnder )
							stored4thLow = 0;		//	If RU/R4 & LL in same bar... logic hole...
					}	
			}
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>	
			
			if ( zetaBar ){
				
					//	-	-	-	-	-	-	-	-	-	>
					if ( !zetaBarFT ){
							if ( Close[0] < zetaBarLow ){
									zetaBar = false;
								if ( showZetas )
									Draw.TriangleDown(this,"Tag201" + CurrentBar, true, 0, High[0] + 6 * TickSize, Brushes.Crimson);
									drawSignalTextBelow(showZetas,ref textCount,"*F*",0,Brushes.DeepPink,fntIII,Convert.ToInt32(pixels*2.62));
								SIGNAL[0] = -6;
							}
							if ( Close[0] > zetaBarHigh ){
									closesAboveZ++;
									drawSignalTextAbove(showZetas,ref textCount,closesAboveZ.ToString(),0,Brushes.Cyan,fntIII,Convert.ToInt32(pixels*1.62));
							}
														
							bool checkActiveBuyZone = BUYZONES.Exists(x => x.active && x.low > possibleLow && x.low < storedSwingHigh);
							if ( !checkActiveBuyZone )
							if ( closesAboveZ == requiredCloses ){
																
									buyZone = true;
									buyZoneHigh = storedSwingHigh;
									buyZoneLow	= possibleLow;
									buyZoneCount = 0;
								
									zoneData bzd 		= new zoneData();
									bzd.high 			= buyZoneHigh;
									bzd.low 			= buyZoneLow;
									bzd.bar0ID 			= CurrentBar;
									bzd.dir				= true;
									bzd.timeZoneStart 	= Time[0];
									bzd.timeZoneEnd 	= Time[0];
								
									BUYZONES.Add(bzd);
								
//									Print(" BUYZONES.Count  ==  "+BUYZONES.Count);
//									Print(" Time  @  "+Time[0].TimeOfDay);
								
									runningLow = double.MaxValue;
								
									zetaBar = false;
																								
									drawSignalTextAbove(showSymbols,ref textCount,"*B1*",0,Brushes.DodgerBlue,fntIII,Convert.ToInt32(pixels*2.62));
								
									SIGNAL[0] = 2;
							}
							if ( closesAboveZ == requiredCloses+1 ){		//	Quick Fix... a better way might be needed
									zetaBar = false;
									runningLow = double.MaxValue;
							}
					}
					else{
						
					}
					//	-	-	-	-	-	-	-	-	-	>
					if ( showZetas )
					drawHL(true,zetaBarHigh,zetaBarLow,Brushes.Cyan,Brushes.LightGray,"Tag207","Tag208");
			}
			
			if ( buyZone ){
				
				if(BUYZONES.Count > 0){
					for(int i = 0; i < BUYZONES.Count; i++){
						if(BUYZONES[i].active){
							if ( wholeBarCancel && High[0] < BUYZONES[i].low ){
								BUYZONES[i].active = false;
								BUYZONES[i].timeZoneEnd = Time[0];
								if ( showColors )
								BarBrush = Brushes.Crimson;
								colorBars(showColors,0,Brushes.DarkRed);
								drawSignalTextBelow(showSymbols,ref textCount,"*CXL*",0,Brushes.Red,fntIII,Convert.ToInt32(pixels*2.62));
							}
							else if ( !wholeBarCancel && Close[0] < BUYZONES[i].low && Open[0] < BUYZONES[i].low ){
								BUYZONES[i].active = false;
								BUYZONES[i].timeZoneEnd = Time[0];
								if ( showColors )
								BarBrush = Brushes.DarkSlateGray;
								colorBars(showColors,0,Brushes.DarkRed);
								drawSignalTextBelow(showSymbols,ref textCount,"*BXL*",0,Brushes.Red,fntIII,Convert.ToInt32(pixels*2.62));
							}
						}
					}
				}
			//	-	-	-	-	-	-	-	-	-	>
				if ( showZones )
				if(BUYZONES.Count > 0){
					for(int i = 0; i < BUYZONES.Count; i++){
						if(BUYZONES[i].active){
							if ( Close[0] < BUYZONES[i].high + displayTicks * TickSize ){
									string tag = BUYZONES[i].timeZoneStart+" "+BUYZONES[i].high+" "+BUYZONES[i].low+" ttf b";
									drawZone(tag, BUYZONES[i].high, BUYZONES[i].low, BUYZONES[i].timeZoneStart, Time[0], buyZoneColor);
							}
						}
					}
				}
			}
	}
			
			#endregion
			
//		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
				
				#region Sell Setup Logic
			
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	if ( useFlip ? flip : !useFlip ){
		
			//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			double newHighInput = 0;
			double resetXhigh = 0;
			
			switch (dataType2)
			{
				case "HIGH"		:	newHighInput = High[0];		break;
				case "CLOSE"	:	newHighInput = Close[0];	break;
			}
			
			switch (rXhigh)
			{
				case "HIGH"		:	resetXhigh = High[0];		break;
				case "CLOSE"	:	resetXhigh = Close[0];		break;
			}
			
			if ( stored4thHigh != 0 && newHighInput >= stored4thHigh + higherTicks * TickSize )
					higherHigh = true;
			else	higherHigh = false;
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			
			bool recycleOver = false;
			
			if ( useOver )
			barOver(ref recycleOver,higherHigh,up4thBar,ref overBar,ref overBarHigh,ref overBarLow,ref stored4thHigh);
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>
			
			if ( runningHigh != 0 ){
					if ( showRunning )
					Draw.Line(this,"Tag226" + CurrentBar , true , 0 , runningHigh , 1 , runningHigh , Brushes.Yellow , DashStyleHelper.Dash , 1 ) ;
					if ( !iBar3up ){
							if ( High[0] > runningHigh )
									runningHigh = High[0];
					}
					else{
							if ( resetXhigh > runningHigh ){
									if ( !overBar
											&& ( respectBar3 ? !(!upWithinBar && Close[0] > upBarTwoHigh) : !respectBar3 )
											&& ( respectBar4 ? (!(!up4thBar && Close[0] > upWithinHigh) && !up4thBar) : !respectBar4 ) ){
													resetAllSwitches1A();
													runningHigh = 0;
													drawSignalTextAbove(showSymbols,ref textCount,"+iX*",0,Brushes.AliceBlue,fntV,Convert.ToInt32(pixels*0.38));
									}
							}
					}
			}
			
			if ( oldRunningHigh != 0 ){
					if ( showRunning )
					Draw.Line(this,"Tag227" + CurrentBar , true , 0 , oldRunningHigh , 1 , oldRunningHigh , Brushes.Lime , DashStyleHelper.Dash , 1 ) ;
					
					if ( resetXhigh > oldRunningHigh ){

							if ( iBar1up
									&& !overBar
									&& ( respectBar3 ? !(!upWithinBar && Close[0] > upBarTwoHigh) : !respectBar3 )
									&& ( respectBar4 ? (!(!up4thBar && Close[0] > upWithinHigh) && !up4thBar) : !respectBar4 ) ){
											resetAllSwitches1A();
											runningHigh = 0;
											drawSignalTextAbove(showSymbols,ref textCount,"+xL*",0,Brushes.AliceBlue,fntV,Convert.ToInt32(pixels*0.38));
							}
					}
			}
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>	
			
			if ( !upBarOne ){
				if ( useDownBarCheck ? downBarCheck : !useDownBarCheck )
				if ( !overBar )	
					if ( Close[0] > Open[0] ){
							createUpBar(ref upBarOne,ref upBarOneHigh,ref upBarOneLow,"1",Brushes.SpringGreen,Brushes.SpringGreen,1);
						//	-	-	-	-	-	>
							calculateSwingLow(false,false,"*sL*");
					}
			}
			else{
				
					if ( !upBarTwo ){
						
							if ( Close[0] < upBarOneLow ){
									upBarOne = false;
									drawSignalTextBelow(showSymbols,ref textCount,"-R1*",0,Brushes.Gold,fntIII,pixels);
									SIGNAL[0] = -1;
							}
						
						if ( !overBar )
							if ( Close[0] > upBarOneHigh ){
									createUpBar(ref upBarTwo,ref upBarTwoHigh,ref upBarTwoLow,"2",Brushes.DeepSkyBlue,Brushes.DeepSkyBlue,1);
								//	-	-	-	-	-	>
									runningHigh = High[0];
								//	-	-	-	-	-	>
									calculateSwingLow(false,false,"-s2*");
							}
					}
					else{
						
						//	-	-	-	-	-	-	-	-	-	>
						
							if ( !takeBarLow ){
									if ( Close[0] < upBarTwoLow
											&& !upWithinBar ){
													takeBarLow = true;
												if ( showSymbols )
													Draw.TriangleDown(this,"Tag101" + CurrentBar, true, 0, High[0] + 6 * TickSize, Brushes.Gold);
									}
							}
							else{
								if ( !overBar )
									insideBarsUp(upWithinBar,Brushes.SpringGreen,ref iBar1up,ref iBar1upHigh,ref iBar1upLow,
													ref iBar2up,ref iBar2upHigh,ref iBar2upLow,ref iBar3up,ref iBar3upHigh,ref iBar3upLow);
							}
							
						//	-	-	-	-	-	-	-	-	-	>	
						
							if ( !takeSwingLow ){
									if ( Close[0] < swingLow
											&& swingLow != double.MaxValue ){
										
												takeSwingLow = true;
										
												colorBars(showColors,0,Brushes.Crimson);
												
//											if ( showSymbols )
//												Draw.TriangleDown(this,"Tag102" + CurrentBar, true, 0, High[0] + 4 * TickSize, Brushes.Crimson);
									}
							}
							else{
								
							}
							
						//	-	-	-	-	-	-	-	-	-	>	
							
							if ( !upWithinBar ){
								if ( !overBar )
									if ( Close[0] > Open[0]
											&& Close[0] > upBarTwoHigh ){
													createUpBar(ref upWithinBar,ref upWithinHigh,ref upWithinLow,"3",Brushes.Blue,Brushes.Blue,1);
									}
							}
							else{
									if ( !takeBarLow ){
											if ( Close[0] < upWithinLow
													&& !up4thBar ){
															takeBarLow = true;
														if ( showSymbols )
															Draw.TriangleDown(this,"Tag102" + CurrentBar, true, 0, High[0] + 6 * TickSize, Brushes.Indigo);
											}
									}
									else{
										if ( !overBar )
											insideBarsUp(up4thBar,Brushes.Blue,ref iBar1up,ref iBar1upHigh,ref iBar1upLow,
													ref iBar2up,ref iBar2upHigh,ref iBar2upLow,ref iBar3up,ref iBar3upHigh,ref iBar3upLow);
									}
									
								//	-	-	-	-	-	-	-	-	-	>
									
									barNo4up(ref recycleOver,overBar,upWithinHigh,higherHigh,ref up4thBar,ref up4thBarHigh,ref up4thBarLow,ref stored4thHigh);
									
								//	-	-	-	-	-	-	-	-	-	>
									
									drawHL(showSetupLines,upWithinHigh,upWithinLow,Brushes.Coral,Brushes.Brown,"Tag211","Tag212");

							}
							
						//	-	-	-	-	-	-	-	-	-	>	
							
							if ( takeBarLow && takeSwingLow ){
								
									alphaBar = true;
								
									alphaBarHigh	= High[0];
									alphaBarLow		= Low[0];
									alphaBarClose	= Close[0];
								
									storedSwingLow = swingLow;
								
									possibleHigh = runningHigh;
								
									closesBelowA = 1;
								
									resetAllSwitches1A();
								
									drawSignalTextBelow(showAlphas,ref textCount,"-A-",0,Brushes.Red,fntIII,Convert.ToInt32(pixels*1.62));
							}
							
							if ( !takeBarLow && takeSwingLow ){
								
									resetAllSwitches1A();
								
									drawSignalTextBelow(showSymbols,ref textCount,"*INC*",0,Brushes.Silver,fntIII,Convert.ToInt32(pixels*1.62));
							}
							
						//	-	-	-	-	-	-	-	-	-	>
							
							drawHL(showSetupLines,upBarTwoHigh,upBarTwoLow,Brushes.LightPink,Brushes.DeepPink,"Tag213","Tag214");

					}
					
					if ( showLevels )
					if ( swingLow != double.MaxValue )
					Draw.Line(this,"Tag210" + CurrentBar , true , 0 , swingLow , 1 , swingLow , swingLowColor , DashStyleHelper.Dash , 2 ) ;
					
					drawHL(showSetupLines,upBarOneHigh,upBarOneLow,Brushes.Lime,Brushes.OrangeRed,"Tag215","Tag216");

			}
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>	
			
			if ( stored4thHigh != 0 ){
					
				if ( showLevels && Close[0] > stored4thHigh - displayTicks * TickSize )
					Draw.Line(this,"Tag209" + CurrentBar , true , 0 , stored4thHigh , 1 , stored4thHigh , Brushes.SteelBlue , DashStyleHelper.Dash , 2 ) ;
						
					if ( higherHigh ){
							drawSignalTextAbove(showSymbols,ref textCount,"*HH*",0,Brushes.PaleGreen,fntIII,Convert.ToInt32(pixels*2));
//							resetAllSwitches1A();
						if ( useOver )
						if ( !recycleOver )
							stored4thHigh = 0;		//	If RU/R4 & HH in same bar... logic hole...
					}	
			}
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>	
			
			if ( alphaBar ){
				
					//	-	-	-	-	-	-	-	-	-	>
					if ( !alphaBarFT ){
							if ( Close[0] > alphaBarHigh ){
									alphaBar = false;
								if ( showAlphas )
									Draw.TriangleUp(this,"Tag201" + CurrentBar, true, 0, Low[0] - 6 * TickSize, Brushes.Green);
									drawSignalTextAbove(showAlphas,ref textCount,"*F*",0,Brushes.Yellow,fntIII,Convert.ToInt32(pixels*2.62));
								SIGNAL[0] = 6;
							}
							if ( Close[0] < alphaBarLow ){
									closesBelowA++;
									drawSignalTextBelow(showAlphas,ref textCount,closesBelowA.ToString(),0,Brushes.DeepPink,fntIII,Convert.ToInt32(pixels*1.62));
							}
							
							bool checkActiveSellZone = SELLZONES.Exists(x => x.active && x.high < possibleHigh && x.high > storedSwingLow);
							if ( !checkActiveSellZone )
							if ( closesBelowA == requiredCloses ){
									sellZone = true;
									sellZoneHigh = possibleHigh;
									sellZoneLow	= storedSwingLow;
									sellZoneCount = 0;
								
									zoneData szd 	= new zoneData();
									szd.high 		= sellZoneHigh;
									szd.low 		= sellZoneLow;
									szd.bar0ID 		= CurrentBar;
									szd.dir			= false;
									szd.timeZoneStart 	= Time[0];
									szd.timeZoneEnd 	= Time[0];
								
									SELLZONES.Add(szd);
								
//									Print(" SELLZONES.Count  ==  "+SELLZONES.Count);
//									Print(" Time  @  "+Time[0].TimeOfDay);
								
									runningHigh = 0;
								
									alphaBar = false;
																								
									drawSignalTextBelow(showSymbols,ref textCount,"*S1*",0,Brushes.Red,fntIII,Convert.ToInt32(pixels*2.62));
								
									SIGNAL[0] = -2;
							}
							if ( closesBelowA == requiredCloses+1 ){	//	Quick Fix... a better way might be needed
									alphaBar = false;
									runningHigh = 0;
							}
					}
					else{
						
					}
					//	-	-	-	-	-	-	-	-	-	>
					if ( showAlphas )
					drawHL(true,alphaBarHigh,alphaBarLow,Brushes.LightPink,Brushes.DeepPink,"Tag207","Tag208");
			}
			
			if ( sellZone ){
				
				if(SELLZONES.Count > 0){
					for(int i = 0; i < SELLZONES.Count; i++){
						if(SELLZONES[i].active){
							if ( wholeBarCancel && Low[0] > SELLZONES[i].high ){
								SELLZONES[i].active = false;
								SELLZONES[i].timeZoneEnd = Time[0];
								if ( showColors )
								BarBrush = Brushes.Blue;
								colorBars(showColors,0,Brushes.DeepSkyBlue);
								drawSignalTextAbove(showSymbols,ref textCount,"*CXL*",0,Brushes.DodgerBlue,fntIII,Convert.ToInt32(pixels*2.62));
							}
							else if ( !wholeBarCancel && Close[0] > SELLZONES[i].high  && Open[0] > SELLZONES[i].high  ){
								SELLZONES[i].active = false;
								SELLZONES[i].timeZoneEnd = Time[0];
								if ( showColors )
								BarBrush = Brushes.Blue;
								colorBars(showColors,0,Brushes.Aqua);
								drawSignalTextAbove(showSymbols,ref textCount,"*BXL*",0,Brushes.DodgerBlue,fntIII,Convert.ToInt32(pixels*2.62));
							}
						}
					}
				}
				
				if ( showZones )
				if(SELLZONES.Count > 0){
					for(int i = 0; i < SELLZONES.Count; i++){
						if(SELLZONES[i].active){
							if ( Close[0] > SELLZONES[i].low - displayTicks * TickSize ){
									string tag = SELLZONES[i].timeZoneStart+" "+SELLZONES[i].high+" "+SELLZONES[i].low+" ttf a";
									drawZone(tag, SELLZONES[i].high, SELLZONES[i].low, SELLZONES[i].timeZoneStart, Time[0], sellZoneColor);
							}
						}
					}
				}
			}
			
		//	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	>	
	}		
				#endregion
			
//		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			
//			#endregion
	
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
					
				if ( printPrimaryBars ){
						Print("- - - - - - - - - - - -");
						Print(" z21-bAR No. "+CurrentBar+" ~ CLOSE*0  ==  "+Close[0].ToString("0.00")+" @ ~ "
								+Time[0].TimeOfDay.ToString());
						Print(" _SIGNAL*  ==  "+SIGNAL[0]);
//						Print(" primaryATR  ==  "+primaryATR.ToString("0.00"));
//						Print(" primaryTicksATR  ==  "+Convert.ToInt32(primaryATR/TickSize));
//						Print("- - - - - - - - - - - -");
				}
				
		// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -		
			
			#region DrawRegions
			
//			Draw.Region ( 	this,
//							"Tag 1" , 
//							CurrentBar , 
//							0 , 
//							UPPER , 
//							LOWER , 
//							null , 
//							sellZoneColor , 
//							opacity ,
//							0 ) ;
			
			#endregion
		}
		
		//	-	-	-	-	-	-	-	-	>>
		
//		#endregion
		
		// - - - - - - - - - - - - -
		
//		#region Objects
		
			#region colorBars
		
		private void colorBars (bool show,int barsBack,Brush paint)
		{
			if ( show )
			CandleOutlineBrushes[barsBack] = paint;
		}
		
			#endregion
		
			#region resetAllSwitches1B		
		
		private void resetAllSwitches1B ()
		{
			upBarCheck = false;
			downBarOne = false;
			downBarTwo = false;
			downWithinBar = false;
			down4thBar = false;
			underBar = false;
			iBar1down = false;
			iBar2down = false;
			iBar3down = false;
			swingHigh = 0;
			insideSwingHigh = 0;
			takeBarHigh = false;
			takeSwingHigh = false;
			oldRunningLow = double.MaxValue;
//			stored4thLow = 0;
			if ( showResets )
			BackBrushesAll[0] = Brushes.DarkRed;
		}
		
			#endregion		
		
			#region resetAllSwitches1A
		
		private void resetAllSwitches1A ()
		{
			downBarCheck = false;
			upBarOne = false;
			upBarTwo = false;
			upWithinBar = false;
			up4thBar = false;
			overBar = false;
			iBar1up = false;
			iBar2up = false;
			iBar3up = false;
			swingLow = double.MaxValue;
			insideSwingLow = double.MaxValue;
			takeBarLow = false;
			takeSwingLow = false;
			oldRunningHigh = 0;
//			stored4thHigh = 0;
			if ( showResets )
			BackBrushesAll[0] = Brushes.Navy;
		}
		
			#endregion
		
			#region createDownBar
		
		private void createDownBar (ref bool barName,ref double high,ref double low,string label,Brush barColor,Brush brush,double pxMx)
		{
			colorBars(showColors,0,barColor);
			barName = true;
			high = High[0];
			low = Low[0];
			drawSignalTextBelow(showNumbers,ref textCount,label,0,brush,fntIII,Convert.ToInt32(pixels*pxMx));
		}
		
			#endregion
		
			#region createUpBar
		
		private void createUpBar (ref bool barName,ref double high,ref double low,string label,Brush barColor,Brush brush,double pxMx)
		{
			colorBars(showColors,0,barColor);
			barName = true;
			high = High[0];
			low = Low[0];
			drawSignalTextAbove(showNumbers,ref textCount,label,0,brush,fntIII,Convert.ToInt32(pixels*pxMx));
		}
		
			#endregion
		
			#region calculateSwingHigh
		
		private void calculateSwingHigh (bool insideBars,bool insideBarTwo,string label)
		{
			double tempSwingHigh = High[0];
			int tempSwingHighBars = 0;
			for ( int i = 1; i <= lookBack; i++ ){
					if ( High[i] > tempSwingHigh ){
							tempSwingHigh = High[i];
							tempSwingHighBars = i;
					}
			}
			if ( insideBars ){
					if ( !insideBarTwo ){
							insideSwingHigh = tempSwingHigh;
							drawSignalTextAbove(showSymbols,ref textCount,label,tempSwingHighBars,swingHighText,fntV,Convert.ToInt32(pixels*2.13));
					}
					else{
							if ( tempSwingHigh > insideSwingHigh ){
									insideSwingHigh = tempSwingHigh;
									drawSignalTextAbove(showSymbols,ref textCount,label,tempSwingHighBars,swingHighText,fntV,Convert.ToInt32(pixels*2.13));	
							}
							swingHigh = tempSwingHigh;
					}		
			}
			else{
					if ( tempSwingHigh > swingHigh ){
							swingHigh = tempSwingHigh;
							drawSignalTextAbove(showSymbols,ref textCount,label,tempSwingHighBars,swingHighText,fntV,Convert.ToInt32(pixels*2.13));
							colorBars(showColors,tempSwingHighBars,Brushes.SpringGreen);
					}
			}
		}
		
			#endregion
		
			#region calculateSwingLow
		
		private void calculateSwingLow (bool insideBars,bool insideBarTwo,string label)
		{
			double tempSwingLow = Low[0];
			int tempSwingLowBars = 0;
			for ( int i = 1; i <= lookBack; i++ ){
					if ( Low[i] < tempSwingLow ){
							tempSwingLow = Low[i];
							tempSwingLowBars = i;
					}
			}
			if ( insideBars ){
					if ( !insideBarTwo ){
							insideSwingLow = tempSwingLow;
							drawSignalTextBelow(showSymbols,ref textCount,label,tempSwingLowBars,swingLowText,fntV,Convert.ToInt32(pixels*2.13));
					}
					else{
							if ( tempSwingLow < insideSwingLow ){
									insideSwingLow = tempSwingLow;
									drawSignalTextBelow(showSymbols,ref textCount,label,tempSwingLowBars,swingLowText,fntV,Convert.ToInt32(pixels*2.13));	
							}
							swingLow = tempSwingLow;
					}
			}
			else{
					if ( tempSwingLow < swingLow ){
							swingLow = tempSwingLow;	
							drawSignalTextBelow(showSymbols,ref textCount,label,tempSwingLowBars,swingLowText,fntV,Convert.ToInt32(pixels*2.13));
							colorBars(showColors,tempSwingLowBars,Brushes.SteelBlue);
					}
			}
		}
		
			#endregion		
		
			#region insideBarsDown
		
		private void insideBarsDown (bool crossCheck,Brush labelColor,ref bool bar1,ref double bar1H,ref double bar1L,
										ref bool bar2,ref double bar2H,ref double bar2L,ref bool bar3,ref double bar3H,ref double bar3L)
		{
			if ( !bar1 ){
					if ( Close[0] < Open[0]
							&& !crossCheck ){
									createDownBar(ref bar1,ref bar1H,ref bar1L,"1.1",innerBarsColor,labelColor,1.83);
								//	-	-	-	-	-	>		//	Measure NEW Swing High
									calculateSwingHigh(true,false,"*iH*");
					}
			}
			else{
					if ( !bar2 ){
							if ( Close[0] < bar1L ){
									createDownBar(ref bar2,ref bar2H,ref bar2L,"2.1",innerBarsColor,Brushes.Magenta,1.83);
								//	-	-	-	-	-	>
									oldRunningLow = runningLow;
									runningLow = Low[0];
								//	-	-	-	-	-	>		//	Measure NEW Swing High
									calculateSwingHigh(true,true,"*i2*");
							}
					}
					else{
							if ( !bar3 ){
									if ( Close[0] < bar2L ){
											createDownBar(ref bar3,ref bar3H,ref bar3L,"3.1",innerBarsColor,Brushes.PaleGreen,1.83);
									}
							}
							else{
									drawHL(showSetupLines,bar3H,bar3L,Brushes.LightBlue,Brushes.SteelBlue,"Tag223","Tag224");

							}
															
							drawHL(showSetupLines,bar2H,bar2L,Brushes.OliveDrab,Brushes.DarkCyan,"Tag221","Tag222");

					}
													
					drawHL(showSetupLines,bar1H,bar1L,Brushes.Aquamarine,Brushes.Indigo,"Tag219","Tag220");

					}
		}
		
			#endregion
		
			#region insideBarsUp
		
		private void insideBarsUp (bool crossCheck,Brush labelColor,ref bool bar1,ref double bar1H,ref double bar1L,
										ref bool bar2,ref double bar2H,ref double bar2L,ref bool bar3,ref double bar3H,ref double bar3L)
		{
			if ( !bar1 ){
					if ( Close[0] > Open[0]
							&& !crossCheck ){
									createUpBar(ref bar1,ref bar1H,ref bar1L,"1.1",innerBarsColor,labelColor,1.83);
								//	-	-	-	-	-	>		//	Measure NEW Swing Low
									calculateSwingLow(true,false,"*iL*");
					}
			}
			else{
					if ( !bar2 ){
							if ( Close[0] > bar1H ){
									createUpBar(ref bar2,ref bar2H,ref bar2L,"2.1",innerBarsColor,Brushes.Magenta,1.83);
								//	-	-	-	-	-	>
									oldRunningHigh = runningHigh;
									runningHigh = High[0];
								//	-	-	-	-	-	>		//	Measure NEW Swing Low
									calculateSwingLow(true,true,"*i2*");
							}
					}
					else{
							if ( !bar3 ){
									if ( Close[0] > bar2H ){
											createUpBar(ref bar3,ref bar3H,ref bar3L,"3.1",innerBarsColor,Brushes.PaleGreen,1.83);
									}
							}
							else{
									drawHL(showSetupLines,bar3H,bar3L,Brushes.LightBlue,Brushes.SteelBlue,"Tag223","Tag224");

							}
															
							drawHL(showSetupLines,bar2H,bar2L,Brushes.OliveDrab,Brushes.DarkCyan,"Tag221","Tag222");

					}
													
					drawHL(showSetupLines,bar1H,bar1L,Brushes.Aquamarine,Brushes.Indigo,"Tag219","Tag220");

					}
		}
		
			#endregion
		
			#region barNo4Down
		
		private void barNo4Down (ref bool patch,bool crossCheck,double sequencePrice,bool extremeCheck,ref bool name,
										ref double high,ref double low,ref double storedLow)
		{
			if ( !name ){
				if ( !crossCheck )
					if ( Close[0] < sequencePrice || extremeCheck ){
							createDownBar(ref name,ref high,ref low,"4",Brushes.Green,Brushes.Green,1);
					}
			}
			else{
					if ( Close[0] < low ){
							colorBars(showColors,0,Brushes.Green);
							high = High[0];
							low = Low[0];	
					}
					if ( Close[0] > high ){
												
//							if ( !takeSwingHigh )				//	Option to still create Zone
//									resetAllSwitches1B();
												
							resetAllSwitches1B();				//	Go with cancellation of bar 4 creates recycle
						
							zetaBar = false;
						
							setupData sd = new setupData();
							sd.swingLow = runningLow;
							sd.pivot = high;
							SETUP1B.Add(sd);
						
							runningLow = double.MaxValue;
												
							storedLow = low;
						
							patch = true;
																								
							drawSignalTextBelow(showSymbols,ref textCount,"+R4*",0,Brushes.Lime,fntIII,pixels);
						
							SIGNAL[0] = 4;
					}
					
					if ( !showSetupLines && showNumbers )
					Draw.Line(this,"Tag225" + CurrentBar , true , -1 , low , 0 , low , Brushes.SeaGreen , DashStyleHelper.Dash , 1 ) ;
					else
					drawHL(showSetupLines,high,low,Brushes.PaleGreen,Brushes.Green,"Tag217","Tag218");

				}
		}
		
			#endregion
		
			#region barNo4up
		
		private void barNo4up (ref bool patch,bool crossCheck,double sequencePrice,bool extremeCheck,ref bool name,
										ref double high,ref double low,ref double storedHigh)
		{
			if ( !name ){
				if ( !crossCheck )
					if ( Close[0] > sequencePrice || extremeCheck ){
							createUpBar(ref name,ref high,ref low,"4",Brushes.Turquoise,Brushes.Turquoise,1);
					}
			}
			else{
					if ( Close[0] > high ){
							colorBars(showColors,0,Brushes.Turquoise);
							high = High[0];
							low = Low[0];	
					}
					if ( Close[0] < low ){
												
//							if ( !takeSwingLow )				//	Option to still create Zone
//									resetAllSwitches1A();
												
							resetAllSwitches1A();				//	Go with cancellation of bar 4 creates recycle
						
							alphaBar = false;
						
							setupData sd = new setupData();
							sd.swingHigh = runningHigh;
							sd.pivot = low;
							SETUP1A.Add(sd);
						
							runningHigh = 0;
												
							storedHigh = high;
						
							patch = true;
																								
							drawSignalTextAbove(showSymbols,ref textCount,"-R4*",0,Brushes.HotPink,fntIII,pixels);
						
							SIGNAL[0] = -4;
					}
																
					if ( !showSetupLines && showNumbers )
					Draw.Line(this,"Tag225" + CurrentBar , true , -1 , low , 0 , low , Brushes.Turquoise , DashStyleHelper.Dash , 1 ) ;
					else
					drawHL(showSetupLines,high,low,Brushes.Aquamarine,Brushes.Turquoise,"Tag217","Tag218");

				}
		}
		
			#endregion
		
			#region barUnder		
		
		private void barUnder (ref bool patch,bool extremeCheck,bool crossCheck,ref bool name,ref double high,ref double low,ref double storedLow)
		{
			if ( !name ){
					if ( extremeCheck && !crossCheck ){
							createDownBar(ref name,ref high,ref low,"*U*",Brushes.Green,Brushes.Magenta,1);
					}
			}
			else{
					if ( Close[0] < low ){
							colorBars(showColors,0,Brushes.Green);
							high = High[0];
							low = Low[0];	
					}
					if ( Close[0] > high ){
												
//							if ( !takeSwingHigh )				//	Option to still create Zone
//									resetAllSwitches1B();
												
							resetAllSwitches1B();				//	Go with cancellation of bar 4 creates recycle
						
							zetaBar = false;
						
							setupData sd = new setupData();
							sd.swingLow = low;
							sd.pivot = high;
							SETUP1B.Add(sd);
						
							runningLow = double.MaxValue;
												
							storedLow = low;
						
							patch = true;
																								
							drawSignalTextBelow(showSymbols,ref textCount,"+RU*",0,Brushes.Lime,fntIII,pixels);
						
							SIGNAL[0] = 3;
					}
					
					if ( !showSetupLines && showNumbers )
					Draw.Line(this,"Tag225" + CurrentBar , true , -1 , low , 0 , low , Brushes.SeaGreen , DashStyleHelper.Dash , 1 ) ;
					else
					drawHL(showSetupLines,high,low,Brushes.PaleGreen,Brushes.Green,"Tag217","Tag218");

				}
		}
		
			#endregion
		
			#region barOver		
		
		private void barOver (ref bool patch,bool extremeCheck,bool crossCheck,ref bool name,ref double high,ref double low,ref double storedHigh)
		{
			if ( !name ){
					if ( extremeCheck && !crossCheck ){
							createUpBar(ref name,ref high,ref low,"*O*",Brushes.Turquoise,Brushes.SpringGreen,1);
					}
			}
			else{
					if ( Close[0] > high ){
							colorBars(showColors,0,Brushes.Turquoise);
							high = High[0];
							low = Low[0];	
					}
					if ( Close[0] < low ){
												
//							if ( !takeSwingLow )				//	Option to still create Zone
//									resetAllSwitches1A();
												
							resetAllSwitches1A();				//	Go with cancellation of bar 4 creates recycle
						
							alphaBar = false;
						
							setupData sd = new setupData();
							sd.swingHigh = high;
							sd.pivot = low;
							SETUP1A.Add(sd);
						
							runningHigh = 0;
																								
							storedHigh = high;
						
							patch = true;
																								
							drawSignalTextAbove(showSymbols,ref textCount,"-RO*",0,Brushes.Magenta,fntIII,pixels);
						
							SIGNAL[0] = -3;
					}
					
					if ( !showSetupLines && showNumbers )
					Draw.Line(this,"Tag225" + CurrentBar , true , -1 , low , 0 , low , Brushes.Turquoise , DashStyleHelper.Dash , 1 ) ;
					else
					drawHL(showSetupLines,high,low,Brushes.Aquamarine,Brushes.Turquoise,"Tag217","Tag218");
					
				}
		}
		
			#endregion			
		
			#region drawHighLow
		
		private void drawHL (bool show,double high,double low,Brush highColor,Brush lowColor,string highTag,string lowTag){
			if ( show ){
					Draw.Line(this, highTag + CurrentBar , true , -1 , high , 0 , high , highColor , DashStyleHelper.Dash , 1 ) ;
					Draw.Line(this, lowTag + CurrentBar , true , -1 , low , 0 , low , lowColor , DashStyleHelper.Dash , 1 ) ;
			}
		}
		
		private void drawZoneHL (bool show,double high,double low,Brush highColor,Brush lowColor,string highTag,string lowTag){
			if ( show ){
					Draw.Line(this, highTag + CurrentBar , true , 0 , high , -1 , high , highColor , DashStyleHelper.Dash , 1 ) ;
					Draw.Line(this, lowTag + CurrentBar , true , 0 , low , -1 , low , lowColor , DashStyleHelper.Dash , 1 ) ;
			}
		}
		
			#endregion
			
			#region drawSignalText
		
		private void drawSignalTextAbove (bool show,ref int signalCount,string label,int barsBack,Brush countBarText,SimpleFont countFont,int pixels)
		{
			signalCount++;
			
			string txCnt = signalCount.ToString();
			
			if ( show )
			Draw.Text(this,txCnt,true,label,barsBack,High[barsBack],pixels,countBarText,countFont,
						TextAlignment.Center,Brushes.Transparent,Brushes.Black,1);
		}
		
		private void drawSignalTextAbove (bool show,ref int signalCount,string label,DateTime barsBack,Brush countBarText,SimpleFont countFont,int pixels)
		{
			signalCount++;
			
			string txCnt = signalCount.ToString();
			
			int barsAgo = CurrentBar-Bars.GetBar(barsBack);
			
			if ( show )
			Draw.Text(this,txCnt,true,label,barsBack,High[barsAgo],pixels,countBarText,countFont,
						TextAlignment.Center,Brushes.Transparent,Brushes.Black,1);
		}
		
		private void drawSignalTextBelow (bool show,ref int signalCount,string label,int barsBack,Brush countBarText,SimpleFont countFont,int pixels)
		{
			signalCount++;
			
			string txCnt = signalCount.ToString();
			
			if ( show )
			Draw.Text(this,txCnt,true,label,barsBack,Low[barsBack],-pixels,countBarText,countFont,
						TextAlignment.Center,Brushes.Transparent,Brushes.Black,1);
		}
		
		private void drawSignalTextBelow (bool show,ref int signalCount,string label,DateTime barsBack,Brush countBarText,SimpleFont countFont,int pixels)
		{
			signalCount++;
			
			string txCnt = signalCount.ToString();
			
			int barsAgo = CurrentBar-Bars.GetBar(barsBack);
			
			if ( show )
			Draw.Text(this,txCnt,true,label,barsBack,Low[barsAgo],-pixels,countBarText,countFont,
						TextAlignment.Center,Brushes.Transparent,Brushes.Black,1);
		}
		
		private void drawSignalTextCenter (bool show,ref int signalCount,string label,int barsBack,Brush countBarText,SimpleFont countFont,int pixels)
		{
			signalCount++;
			
			string txCnt = signalCount.ToString();
			
			if ( show )
			Draw.Text(this,txCnt,true,label,barsBack,High[barsBack]-(High[barsBack]-Low[barsBack])/2,-pixels,countBarText,countFont,
						TextAlignment.Center,Brushes.Transparent,Brushes.Black,1);
		}
		
		private void drawSignalText (ref int signalCount,string label,Brush countBarText,SimpleFont countFont,
											Brushes sumText,SimpleFont sumFont,int pixels)
		{
			signalCount++;
			
			string txCnt = signalCount.ToString();
			
			bool side = Close[0] > Open[0];
			
			Draw.Text(this,txCnt,true,label,0,(side ? Low[0] : High[0]),(side? -pixels : pixels),countBarText,countFont,
						TextAlignment.Center,Brushes.Transparent,Brushes.Black,1);
			
//			Draw.Text(this,smCnt, true, smVal, 5, (side ? Low[0] : High[0])+ticksAbove*TickSize, 0, sumText, 
//						sumFont, StringAlignment.Center, Brushes.Transparent, Brushes.Black, 1) ;
			
		}
		
			#endregion
		
			#region drawZone
		
		private void drawZone(int tag,double high,double low,int firstBarTime,int lastBarTime,Brush brush)
		{
			Draw.Rectangle(this, tag + "area", false, firstBarTime, low, lastBarTime, high, Brushes.Transparent, brush, opacity);
		}
		private void drawZone(string tag,double high,double low, DateTime firstBarTime, DateTime lastBarTime,Brush brush)
		{
			Draw.Rectangle(this, tag, false, firstBarTime, low, lastBarTime, high, Brushes.Transparent, brush, opacity);
		}
		
			#endregion
			
			#region Modify Properties
		
        private void ModifyProperties(PropertyDescriptorCollection col){
			
			if ( !showZoneInputs){
					col.Remove(col.Find("useUpBarCheck"		, true));
					col.Remove(col.Find("useDownBarCheck"	, true));
					col.Remove(col.Find("useUnder"			, true));
					col.Remove(col.Find("useOver"			, true));
					col.Remove(col.Find("lookBack"			, true));
					col.Remove(col.Find("dataType1"			, true));
					col.Remove(col.Find("lowerTicks"		, true));
					col.Remove(col.Find("dataType2"			, true));
					col.Remove(col.Find("higherTicks"		, true));
					col.Remove(col.Find("respectBar3"		, true));
					col.Remove(col.Find("respectBar4"		, true));
					col.Remove(col.Find("rXlow"				, true));
					col.Remove(col.Find("rXhigh"			, true));
					col.Remove(col.Find("requiredCloses"	, true));
					col.Remove(col.Find("wholeBarCancel"	, true));
			}
			
		}
		
				#endregion
					
			#region Members
        public AttributeCollection GetAttributes(){ return TypeDescriptor.GetAttributes(GetType()); }
        public string GetClassName(){ return TypeDescriptor.GetClassName(GetType()); }
        public string GetComponentName(){ return TypeDescriptor.GetComponentName(GetType()); }
        public TypeConverter GetConverter(){ return TypeDescriptor.GetConverter(GetType()); }
        public EventDescriptor GetDefaultEvent(){ return TypeDescriptor.GetDefaultEvent(GetType()); }
        public PropertyDescriptor GetDefaultProperty(){ return TypeDescriptor.GetDefaultProperty(GetType()); }
        public object GetEditor(Type editorBaseType){ return TypeDescriptor.GetEditor(GetType(), editorBaseType); }
        public EventDescriptorCollection GetEvents(Attribute[] attributes){ return TypeDescriptor.GetEvents(GetType(), attributes); }
        public EventDescriptorCollection GetEvents(){ return TypeDescriptor.GetEvents(GetType()); }
        public PropertyDescriptorCollection GetProperties(Attribute[] attributes){
            PropertyDescriptorCollection orig 	= TypeDescriptor.GetProperties(GetType(), attributes);
            PropertyDescriptor[] arr 			= new PropertyDescriptor[orig.Count];
            orig.CopyTo(arr, 0);
            PropertyDescriptorCollection col 	= new PropertyDescriptorCollection(arr);
            ModifyProperties(col);
            return col;
        }
        public PropertyDescriptorCollection GetProperties(){ return TypeDescriptor.GetProperties(GetType()); }
        public object GetPropertyOwner(PropertyDescriptor pd){ return this; }
			#endregion
			
//		#endregion
		
		// - - - - - - - - - - - - -
									
//		#region Classes

			#region HTYPE
		
		internal class HTYPE : StringConverter{
			public override bool GetStandardValuesSupported(ITypeDescriptorContext context){return true;}
			public override bool GetStandardValuesExclusive(ITypeDescriptorContext context){return true;}
			public override System.ComponentModel.TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context){
//				return new StandardValuesCollection( new String[] {"HIGH", "LOW", "CLOSE"} );
				return new StandardValuesCollection( new String[] {"HIGH", "CLOSE"} );
			}
		}
		
			#endregion
		
			#region LTYPE
		
		internal class LTYPE : StringConverter{
			public override bool GetStandardValuesSupported(ITypeDescriptorContext context){return true;}
			public override bool GetStandardValuesExclusive(ITypeDescriptorContext context){return true;}
			public override System.ComponentModel.TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context){
//				return new StandardValuesCollection( new String[] {"HIGH", "LOW", "CLOSE"} );
				return new StandardValuesCollection( new String[] {"LOW", "CLOSE"} );
			}
		}
		
			#endregion
		
			#region ZTYPE
		
		internal class ZTYPE : StringConverter{
			public override bool GetStandardValuesSupported(ITypeDescriptorContext context){return true;}
			public override bool GetStandardValuesExclusive(ITypeDescriptorContext context){return true;}
			public override System.ComponentModel.TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context){
				return new StandardValuesCollection( new String[] {"BUY", "SELL"} );
			}
		}
		
			#endregion
		
			#region MATYPE
		
		internal class MATYPE : StringConverter{
			public override bool GetStandardValuesSupported(ITypeDescriptorContext context){return true;}
			public override bool GetStandardValuesExclusive(ITypeDescriptorContext context){return true;}
			public override System.ComponentModel.TypeConverter.StandardValuesCollection GetStandardValues(ITypeDescriptorContext context){
//				return new StandardValuesCollection( new String[] {"SMA", "WMA", "HMA", "EMA", "DEMA"} );
				return new StandardValuesCollection( new String[] {"HIGH", "LOW", "CLOSE"} );
			}
		}
		
			#endregion

//		#endregion
			
		// - - - - - - - - - - - - -

//		#region Properties
		
			#region Outputs
		
		[Browsable(false)]
		[XmlIgnore]
		public Series<double> SIGNALO { get { return SIGNAL; } }
		
			#endregion
		
			#region Zone Parameters
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "useFlip", GroupName = "02. Control Block", Order = 0)]
		public bool useFlip { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "zoneType", GroupName = "02. Control Block", Order = 1)]
        [TypeConverter(typeof(ZTYPE))]
        public string zoneType { get; set; }
		
		[Display(ResourceType = typeof(Custom.Resource), Name = "showZoneInputs", GroupName = "03. Zone Inputs", Order = 0)]
		[RefreshProperties(RefreshProperties.All)]
		public bool showZoneInputs { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "useUpBarCheck", GroupName = "04. Check Block", Order = 0)]
		public bool useUpBarCheck { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "useDownBarCheck", GroupName = "04. Check Block", Order = 1)]
		public bool useDownBarCheck { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "useUnder", GroupName = "04. Extreme Block", Order = 0)]
		public bool useUnder { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "useOver", GroupName = "04. Extreme Block", Order = 1)]
		public bool useOver { get; set; }
		
		[NinjaScriptProperty]
		[Range(1, int.MaxValue)]
		[Display(ResourceType = typeof(Custom.Resource), Name = "lookBack", GroupName = "04. Swing Block", Order = 1)]
        public int lookBack { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "lowerLowPrice", GroupName = "05. Low Block", Order = 1)]
        [TypeConverter(typeof(LTYPE))]
		public string dataType1 { get; set; }
		
		[NinjaScriptProperty]
		[Range(1, int.MaxValue)]
		[Display(ResourceType = typeof(Custom.Resource), Name = "lowerTicks", GroupName = "05. Low Block", Order = 2)]
        public int lowerTicks { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "higherHighPrice", GroupName = "06. High Block", Order = 0)]
        [TypeConverter(typeof(HTYPE))]
		public string dataType2 { get; set; }

		[NinjaScriptProperty]		
		[Range(1, int.MaxValue)]
		[Display(ResourceType = typeof(Custom.Resource), Name = "higherTicks", GroupName = "06. High Block", Order = 1)]
        public int higherTicks { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "respectBar3", GroupName = "07. Zone Interrupts", Order = 0)]
		public bool respectBar3 { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "respectBar4", GroupName = "07. Zone Interrupts", Order = 1)]
		public bool respectBar4 { get; set; }
		
		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "Reset X low", GroupName = "07. Zone Interrupts", Order = 2)]
        [TypeConverter(typeof(LTYPE))]
		public string rXlow { get; set; }

		[NinjaScriptProperty]		
		[Display(ResourceType = typeof(Custom.Resource), Name = "Reset X high", GroupName = "07. Zone Interrupts", Order = 3)]
        [TypeConverter(typeof(HTYPE))]
		public string rXhigh { get; set; }
		
		[NinjaScriptProperty]
		[Range(1, int.MaxValue)]
		[Display(ResourceType = typeof(Custom.Resource), Name = "requiredCloses", GroupName = "07. Zone Qualifiers", Order = 0)]
        public int requiredCloses { get; set; }

		[NinjaScriptProperty]		
		[Display(ResourceType = typeof(Custom.Resource), Name = "wholeBarCancel", GroupName = "07. Zone Qualifiers", Order = 1)]
		public bool wholeBarCancel { get; set; }
		
			#endregion
		
			#region Display
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showColors", GroupName = "Show/Hide Signals", Order = 0)]
		public bool ShowColors
		{
			get { return showColors; }
			set { showColors = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showNumbers", GroupName = "Show/Hide Signals", Order = 1)]
		public bool ShowNumbers
		{
			get { return showNumbers; }
			set { showNumbers = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showSetupLines", GroupName = "Show/Hide Signals", Order = 2)]
		public bool ShowSetupLines
		{
			get { return showSetupLines; }
			set { showSetupLines = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showSymbols", GroupName = "Show/Hide Signals", Order = 3)]
		public bool ShowSymbols
		{
			get { return showSymbols; }
			set { showSymbols = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showRunning", GroupName = "Show/Hide Signals", Order = 4)]
		public bool ShowRunning
		{
			get { return showRunning; }
			set { showRunning = value; }
		}		
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showLevels", GroupName = "Show/Hide Signals", Order = 5)]
		public bool ShowLevels
		{
			get { return showLevels; }
			set { showLevels = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showZetas", GroupName = "Show/Hide Signals", Order = 6)]
		public bool ShowZetas
		{
			get { return showZetas; }
			set { showZetas = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showAlphas", GroupName = "Show/Hide Signals", Order = 7)]
		public bool ShowAlphas
		{
			get { return showAlphas; }
			set { showAlphas = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showZones", GroupName = "Show/Hide Zones", Order = 8)]
		public bool ShowZones
		{
			get { return showZones; }
			set { showZones = value; }
		}
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "displayTicks", GroupName = "Show/Hide Zones", Order = 9)]
        public int DisplayTicks
        {
            get { return displayTicks; }
            set { displayTicks = Math.Max(1, value); }
        }

//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "showResets", GroupName = "Show/Hide Resets", Order = 10)]
		public bool ShowResets
		{
			get { return showResets; }
			set { showResets = value; }
		}
		
			#endregion
		
			#region Visual
		
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "Opacity", GroupName = "09. Contrast", Order = 0)]
		public int Opacity
		{
			get { return opacity; }
			set { opacity = Math.Max(1, value); }
		}
		
//		[XmlIgnore]
//		[NinjaScriptProperty]
//		[Display(Name = "buyZoneColor", GroupName = "10. UserColors")]
////		[Display(ResourceType = typeof(Custom.Resource), Name = "buyZoneColor", GroupName = "10. UserColors", Order = 1)]
//		public System.Windows.Media.Brush BuyZoneColor { get; set; }

//		[Browsable(false)]
//		public string buyZoneColorSerialize
//		{
//			get { return Serialize.BrushToString(buyZoneColor); }
//			set { buyZoneColor = Serialize.StringToBrush(value); }
//		}
		
		[XmlIgnore]
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "buyZoneColor", GroupName = "10. UserColors", Order = 1)]
        public Brush BuyZoneColor{
            get { return buyZoneColor; }
            set { buyZoneColor = value; }
        }
        [Browsable(false)]
        public string buyZoneColorS{
			get { return Serialize.BrushToString(buyZoneColor); }
  			set { buyZoneColor = Serialize.StringToBrush(value); }
        }
		
		[XmlIgnore]
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "sellZoneColor", GroupName = "10. UserColors", Order = 3)]
        public Brush SellZoneColor{
            get { return sellZoneColor; }
            set { sellZoneColor = value; }
        }
        [Browsable(false)]
        public string sellZoneColorS{
			get { return Serialize.BrushToString(sellZoneColor); }
  			set { sellZoneColor = Serialize.StringToBrush(value); }
        }
		
//		[XmlIgnore]
//		[NinjaScriptProperty]
//		[Display(ResourceType = typeof(Custom.Resource), Name = "swingHighText", GroupName = "10. UserColors", Order = 4)]
//        public Brush SwingHighText{
//            get { return swingHighText; }
//            set { swingHighText = value; }
//        }
//        [Browsable(false)]
//        public string swingHighTextS{
//			get { return Serialize.BrushToString(swingHighText); }
//  			set { swingHighText = Serialize.StringToBrush(value); }
//        }
		
////		[XmlIgnore]
////		[NinjaScriptProperty]
////		[Display(ResourceType = typeof(Custom.Resource), Name = "swingLowText", GroupName = "10. UserColors", Order = 5)]
////        public Brush SwingLowText{
////            get { return swingLowText; }
////            set { swingLowText = value; }
////        }
////        [Browsable(false)]
////        public string swingLowTextS{
////			get { return Serialize.BrushToString(swingLowText); }
////  			set { swingLowText = Serialize.StringToBrush(value); }
////        }
		
		[XmlIgnore]
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "swingHighColor", GroupName = "10. UserColors", Order = 6)]
        public Brush SwingHighColor{
            get { return swingHighColor; }
            set { swingHighColor = value; }
        }
        [Browsable(false)]
        public string swingHighColorS{
			get { return Serialize.BrushToString(swingHighColor); }
  			set { swingHighColor = Serialize.StringToBrush(value); }
        }
		
		[XmlIgnore]
//		[NinjaScriptProperty]
		[Display(ResourceType = typeof(Custom.Resource), Name = "swingLowColor", GroupName = "10. UserColors", Order = 7)]
        public Brush SwingLowColor{
            get { return swingLowColor; }
            set { swingLowColor = value; }
        }
        [Browsable(false)]
        public string swingLowColorS{
			get { return Serialize.BrushToString(swingLowColor); }
  			set { swingLowColor = Serialize.StringToBrush(value); }
        }
		
//		[XmlIgnore]
//		[NinjaScriptProperty]
//		[Display(ResourceType = typeof(Custom.Resource), Name = "innerBarsColor", GroupName = "10. UserColors", Order = 8)]
//        public Brush InnerBarsColor{
//            get { return innerBarsColor; }
//            set { innerBarsColor = value; }
//        }
//        [Browsable(false)]
//        public string innerBarsColorS{
//			get { return Serialize.BrushToString(innerBarsColor); }
//  			set { innerBarsColor = Serialize.StringToBrush(value); }
//        }
		
			#endregion
		
			#region DataWindow
		
		[Display(ResourceType = typeof(Custom.Resource), Name = "printPrimaryBars", GroupName = "13. printPrimaryBars", Order = 0)]
		public bool printPrimaryBars { get; set; }		
		
			#endregion
		
//		#endregion
		
	}
}

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private Zone21B2[] cacheZone21B2;
		public Zone21B2 Zone21B2(bool useFlip, string zoneType, bool useUpBarCheck, bool useDownBarCheck, bool useUnder, bool useOver, int lookBack, string dataType1, int lowerTicks, string dataType2, int higherTicks, bool respectBar3, bool respectBar4, string rXlow, string rXhigh, int requiredCloses, bool wholeBarCancel)
		{
			return Zone21B2(Input, useFlip, zoneType, useUpBarCheck, useDownBarCheck, useUnder, useOver, lookBack, dataType1, lowerTicks, dataType2, higherTicks, respectBar3, respectBar4, rXlow, rXhigh, requiredCloses, wholeBarCancel);
		}

		public Zone21B2 Zone21B2(ISeries<double> input, bool useFlip, string zoneType, bool useUpBarCheck, bool useDownBarCheck, bool useUnder, bool useOver, int lookBack, string dataType1, int lowerTicks, string dataType2, int higherTicks, bool respectBar3, bool respectBar4, string rXlow, string rXhigh, int requiredCloses, bool wholeBarCancel)
		{
			if (cacheZone21B2 != null)
				for (int idx = 0; idx < cacheZone21B2.Length; idx++)
					if (cacheZone21B2[idx] != null && cacheZone21B2[idx].useFlip == useFlip && cacheZone21B2[idx].zoneType == zoneType && cacheZone21B2[idx].useUpBarCheck == useUpBarCheck && cacheZone21B2[idx].useDownBarCheck == useDownBarCheck && cacheZone21B2[idx].useUnder == useUnder && cacheZone21B2[idx].useOver == useOver && cacheZone21B2[idx].lookBack == lookBack && cacheZone21B2[idx].dataType1 == dataType1 && cacheZone21B2[idx].lowerTicks == lowerTicks && cacheZone21B2[idx].dataType2 == dataType2 && cacheZone21B2[idx].higherTicks == higherTicks && cacheZone21B2[idx].respectBar3 == respectBar3 && cacheZone21B2[idx].respectBar4 == respectBar4 && cacheZone21B2[idx].rXlow == rXlow && cacheZone21B2[idx].rXhigh == rXhigh && cacheZone21B2[idx].requiredCloses == requiredCloses && cacheZone21B2[idx].wholeBarCancel == wholeBarCancel && cacheZone21B2[idx].EqualsInput(input))
						return cacheZone21B2[idx];
			return CacheIndicator<Zone21B2>(new Zone21B2(){ useFlip = useFlip, zoneType = zoneType, useUpBarCheck = useUpBarCheck, useDownBarCheck = useDownBarCheck, useUnder = useUnder, useOver = useOver, lookBack = lookBack, dataType1 = dataType1, lowerTicks = lowerTicks, dataType2 = dataType2, higherTicks = higherTicks, respectBar3 = respectBar3, respectBar4 = respectBar4, rXlow = rXlow, rXhigh = rXhigh, requiredCloses = requiredCloses, wholeBarCancel = wholeBarCancel }, input, ref cacheZone21B2);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.Zone21B2 Zone21B2(bool useFlip, string zoneType, bool useUpBarCheck, bool useDownBarCheck, bool useUnder, bool useOver, int lookBack, string dataType1, int lowerTicks, string dataType2, int higherTicks, bool respectBar3, bool respectBar4, string rXlow, string rXhigh, int requiredCloses, bool wholeBarCancel)
		{
			return indicator.Zone21B2(Input, useFlip, zoneType, useUpBarCheck, useDownBarCheck, useUnder, useOver, lookBack, dataType1, lowerTicks, dataType2, higherTicks, respectBar3, respectBar4, rXlow, rXhigh, requiredCloses, wholeBarCancel);
		}

		public Indicators.Zone21B2 Zone21B2(ISeries<double> input , bool useFlip, string zoneType, bool useUpBarCheck, bool useDownBarCheck, bool useUnder, bool useOver, int lookBack, string dataType1, int lowerTicks, string dataType2, int higherTicks, bool respectBar3, bool respectBar4, string rXlow, string rXhigh, int requiredCloses, bool wholeBarCancel)
		{
			return indicator.Zone21B2(input, useFlip, zoneType, useUpBarCheck, useDownBarCheck, useUnder, useOver, lookBack, dataType1, lowerTicks, dataType2, higherTicks, respectBar3, respectBar4, rXlow, rXhigh, requiredCloses, wholeBarCancel);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.Zone21B2 Zone21B2(bool useFlip, string zoneType, bool useUpBarCheck, bool useDownBarCheck, bool useUnder, bool useOver, int lookBack, string dataType1, int lowerTicks, string dataType2, int higherTicks, bool respectBar3, bool respectBar4, string rXlow, string rXhigh, int requiredCloses, bool wholeBarCancel)
		{
			return indicator.Zone21B2(Input, useFlip, zoneType, useUpBarCheck, useDownBarCheck, useUnder, useOver, lookBack, dataType1, lowerTicks, dataType2, higherTicks, respectBar3, respectBar4, rXlow, rXhigh, requiredCloses, wholeBarCancel);
		}

		public Indicators.Zone21B2 Zone21B2(ISeries<double> input , bool useFlip, string zoneType, bool useUpBarCheck, bool useDownBarCheck, bool useUnder, bool useOver, int lookBack, string dataType1, int lowerTicks, string dataType2, int higherTicks, bool respectBar3, bool respectBar4, string rXlow, string rXhigh, int requiredCloses, bool wholeBarCancel)
		{
			return indicator.Zone21B2(input, useFlip, zoneType, useUpBarCheck, useDownBarCheck, useUnder, useOver, lookBack, dataType1, lowerTicks, dataType2, higherTicks, respectBar3, respectBar4, rXlow, rXhigh, requiredCloses, wholeBarCancel);
		}
	}
}

#endregion
