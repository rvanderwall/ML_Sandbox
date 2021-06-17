import java.io.*;
import java.util.*;
import java.lang.*;
import java.awt.Event;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Color;


class Attract extends Frame
{
	int xSize;
	int ySize;
	int xOffset;
	int yOffset;
	double xScale;
	double yScale;
	Graphics gr;
	int maxCount;
	double R;

	public Attract(String Title) {
		super(Title);
	}

	public void init(int x, int y, 
			 int xO,int yO,
			 double xS, double yS, int c)
	{
		xSize=x;
		ySize=y;
		xOffset = xO;
		yOffset = yO;
		xScale=xS;
		yScale=yS;
		maxCount = c;
		R = 4;
		resize(xSize,ySize);
		show();
		gr = getGraphics();
	    gr.setColor(Color.black);
	}


	// x and y will be between -1.0 and 1.0
	private void setPixel(double x, double y)
	{
	    // Since 0,0 is the upper left corner and we want it to be
	    // the lower left, offset it
	    int trueX, trueY;
	    trueX = (int)((x/xScale + 1.0) * xSize/2) + xOffset;
	    trueY = (int)(ySize - ((y/yScale + 1.0) * ySize/2)) + yOffset;
System.out.print("setPixel" +  " x=" + x + "->" + trueX + 
			       " y=" + y + "->" + trueY + "\n");
	    gr.drawRect(trueX, trueY, 1,1);
	}

	public void run(int back) {
	    double newX;
	    double prevs[];
	    int counter=0;

	    prevs = new double[back];
	    for (int iii=0; iii< back; iii++) prevs[iii]=0.05;

	    System.out.print("running\n");

	    try {
		while (counter < maxCount)
		{
		    //Thread.sleep(10);
		    newX  = R * prevs[0] * (1-prevs[0]);
		    setPixel(prevs[back-1],newX);
		    for (int iii = back-1; iii > 0;  iii--)
			prevs[iii] = prevs[iii-1];
		    prevs[0] = newX;
		    counter++;
		}
	    }
	    catch (Exception e) {
		return;
	    }
	}

	public void paint(Graphics g) {
		System.out.print("Handle 'paint' method\n");
		//g.setColor(Color.black);
		//g.drawLine(0,0,100,100);
		//g.drawRect(50,50,100,100);
	}

	public boolean handleEvent(Event ev) {
		if (ev.id == Event.WINDOW_DESTROY) {
			System.exit(0);
		}
		return false;
	}


	static public void main (String [] args) {
		// Use <xSize> <ySize> <xScale> <yScale> <count> <back>
		if (args.length < 4 ) {
		    System.out.print("Use: <xSize> <ySize> " +
				"<xOffset>  <yOffset> " +
				"<xScale>  <yScale>  <count>\n");
		    System.exit(0);
		}
		System.out.print("Attract Starting\n");
		Attract app = new Attract("Strange Attractor Simulator");
		app.init(Integer.valueOf(args[0]).intValue(),
			 Integer.valueOf(args[1]).intValue(),
			 Integer.valueOf(args[2]).intValue(),
			 Integer.valueOf(args[3]).intValue(),
			 Double.valueOf(args[4]).doubleValue(),
			 Double.valueOf(args[5]).doubleValue(),
			 Integer.valueOf(args[6]).intValue());
		app.run(Integer.valueOf(args[7]).intValue());
	}
}

