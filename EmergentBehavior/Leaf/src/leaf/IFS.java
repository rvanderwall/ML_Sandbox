

import java.io.*;
import java.util.*;
import java.lang.*;
import java.awt.Event;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Color;
//import IFS;


class IFS
{
	double a[];
	double b[];
	double c[];
	double d[];
	double e[];
	double f[];
	double p[];
	Random rnum;
	double newX;
	double newY;

	public IFS(String file)
	{
	   try {
		File fl = new File(file);
		FileReader fIn = new FileReader(fl);
		BufferedReader in = new BufferedReader(fIn);
		Vector lines = new Vector();
		String curLine;
		while (( curLine = in.readLine()) != null) {
			lines.add(curLine);
		}
		int numLines= lines.size();
		a = new double[numLines];
		b = new double[numLines];
		c = new double[numLines];
		d = new double[numLines];
		e = new double[numLines];
		f = new double[numLines];
		p = new double[numLines];
		rnum = new Random((long)3.14159);

		for (int idx = 0; idx < numLines; idx++) {
		    curLine = (String)lines.elementAt(idx);
		    StringTokenizer _parser = new StringTokenizer(
				curLine, " \t",false);
		    String tok = _parser.nextToken();
		    a[idx]=Double.valueOf(tok).doubleValue();
		    tok = _parser.nextToken();
		    b[idx]=Double.valueOf(tok).doubleValue();
		    tok = _parser.nextToken();
		    c[idx]=Double.valueOf(tok).doubleValue();
		    tok = _parser.nextToken();
		    d[idx]=Double.valueOf(tok).doubleValue();
		    tok = _parser.nextToken();
		    e[idx]=Double.valueOf(tok).doubleValue();
		    tok = _parser.nextToken();
		    f[idx]=Double.valueOf(tok).doubleValue();
		    tok = _parser.nextToken();
		    p[idx]=Double.valueOf(tok).doubleValue();
		}
	   }
	   catch (IOException e) {
		System.out.print("Cannot open file:" + file);
		System.exit(0);
	   }
	}

	 
	double getNewX(double x, double y)
	{
		int idx;
		// Generate a random Number
		double prob = rnum.nextDouble();
		for (idx=0; idx < p.length; idx++)
		{
		    if ( prob < p[idx] )
		    {
			// Use this probability
			break;
		    }
		    prob = prob - p[idx];
		}
		
		newX = a[idx] * x + b[idx] * y + e[idx];
		newY = c[idx] * x + d[idx] * y + f[idx];
		return newX;
	}

	// We've already found newY.  We really should return a Point
	double getNewY(double x, double y) {
		return newY;
	}

}


