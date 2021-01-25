

import java.io.*;
import java.util.*;
import java.lang.*;
import java.awt.Event;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Color;
//import IFS;


class Leaf extends Frame
{

	int xSize;
	int ySize;
	int xOffset;
	int yOffset;
	double xScale;
	double yScale;
	Graphics gr;
	IFS ifs;
	int maxCount;

	public Leaf(String Title) {
		super(Title);
	}

	public void init(int x, int y, 
			 int xO,int yO,
			 double xS, double yS, int c) {
		xSize=x;
		ySize=y;
		xOffset = xO;
		yOffset = yO;
		xScale=xS;
		yScale=yS;
		maxCount = c;
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
//System.out.print("setPixel" +  " x=" + x + "->" + trueX + 
//			       " y=" + y + "->" + trueY + "\n");
	    gr.drawRect(trueX, trueY, 1,1);
      	}

	public void run(String cFile) {
	    double curX = 0.0;
	    double curY = 0.0;
	    double newX,newY;
	    int counter=0;

	    System.out.print("running\n");
	    ifs = new IFS(cFile);

	    try {
		while (counter < maxCount)
		{
		    //Thread.sleep(10);
		    newX  = ifs.getNewX(curX,curY);
		    newY  = ifs.getNewY(curX,curY);
		    setPixel(newX,newY);
		    curX = newX;
		    curY = newY;
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
		// Use <file> <xSize> <ySize> <xScale> <yScale> <count>
		if (args.length < 4 ) {
		    System.out.print("Use: <file> <xSize> <ySize> " +
				"<xOffset>  <yOffset> " +
				"<xScale>  <yScale>  <count>\n");
		    System.exit(0);
		}
		System.out.print("Leaf Starting\n");
                int xSize = Integer.valueOf(args[1]).intValue();
                int ySize = Integer.valueOf(args[2]).intValue();
                double xScale = Double.valueOf(args[5]).doubleValue();
                double yScale = Double.valueOf(args[6]).doubleValue();
                int xOffset = Integer.valueOf(args[3]).intValue();
                int yOffset = Integer.valueOf(args[4]).intValue();
                int count   = Integer.valueOf(args[7]).intValue();
                
		Leaf app = new Leaf("Leaf Simulator");
		app.init(xSize, ySize, xOffset, yOffset, xScale, yScale, count);
		app.run(args[0]);
	}
}

