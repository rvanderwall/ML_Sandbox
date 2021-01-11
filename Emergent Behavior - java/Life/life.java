// life.java Conway's Game of Life  
// W.B.Langdon@cs.bham.ac.uk 5 Feb 1997 
// $Revision: 1.13 $

package life;

//Modifications (in reverse order)

//WBL  1 Mar 1997 Allow use as stand alone application and network files
//WBL 25 Feb 1997 put into a package
//WBL  5 Feb 1997 new file

import java.awt.Graphics;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Color;
import java.awt.Point;
import java.awt.Event;
import java.awt.Frame;
import java.util.Date;
import java.io.*;
import java.net.URL;
import java.net.MalformedURLException;


class pair {
	int x = 0;
	int y = 0;
	pair (int xx, int yy) {x=xx; y=yy;};
	pair (int xx)         {x=xx; y=xx;};
	boolean equal(pair b) {return (this.x==b.x) && (this.y==b.y);};
	boolean within(pair a, pair b) {
		return	(this.x>=a.x) && (this.y>=a.y) &&
			(this.x< b.x) && (this.y< b.y);
	}
	pair(String xy) throws Exception {
		int sep = xy.indexOf('x');
		x = Integer.parseInt(xy.substring(0,sep));
		y = Integer.parseInt(xy.substring(sep+1,xy.length()));
	}
}//end class pair

class game {
	boolean[][] board;
//	int[][] debug;
	pair dim = new pair(0,0);
//	int max = 0;
	game(pair size, double init_fraction) {
		dim.x = size.x;
		dim.y = size.y;
		board = new boolean[dim.x][dim.y];
//		debug = new int[dim.x][dim.y];
		for(int i = 0; i < dim.x; i++)
		for(int j = 0; j < dim.y; j++) {
			board[i][j] = (Math.random() < init_fraction);
		}
	}

	game(game in, pair size, double init_fraction) {
		dim.x = size.x;
		dim.y = size.y;
		board = new boolean[dim.x][dim.y];
//		debug = new int[dim.x][dim.y];
		for(int i = 0; i < dim.x; i++)
		for(int j = 0; j < dim.y; j++) {
			board[i][j] = (in!=null && i<in.dim.x && j<in.dim.y)?
					in.board[i][j]		:
					(Math.random() < init_fraction);
		}
	}

game(game in, InputStream s, double init_fraction) throws IOException {
	DataInputStream f = new DataInputStream(s);
	String line;
	pair file_dim;
	line = f.readLine();
	{int i;
	 for(i=0;i<line.length();i++){
		if(line.charAt(i)=='-' || (line.charAt(i)>='0' && line.charAt(i)<='9')) {
			break;
		}
	 }
	String s1 = line.substring(i);
	int sep =   s1.indexOf(' ');
	String n1 = s1.substring(0,sep);
	String n2 = s1.substring(sep+1);
	int x = Math.abs(Integer.parseInt(n1));
	int y = Math.abs(Integer.parseInt(n2));
	file_dim = new pair(x,y);
	}
//System.err.println("File dimensions "+file_dim.x+"x"+file_dim.y);

	boolean temp_board[][] = new boolean[file_dim.x][file_dim.y];
	for(int yy=0; yy<file_dim.y; yy++) {
		for(line = f.readLine(); line!=null&&line.charAt(0)=='#';){;};
//		System.err.println("Read: "+line);
		for(int xx=0; xx<file_dim.x; xx++) {
		    temp_board[xx][yy] =
			(line!=null&&xx<line.length() && line.charAt(xx)=='*');
		}//endfor xx
	}//endfor yy

if(in==null) {
	dim = file_dim;
	board = temp_board;
}
else {	//Add file to existing game
	dim = new pair((file_dim.x>in.dim.x)? file_dim.x:in.dim.x,
		       in.dim.y+file_dim.y);
	board = new boolean[dim.x][dim.y];
	for(int xx=0;xx<dim.x;xx++)
	for(int yy=0;yy<dim.y;yy++) {
		board[xx][yy]= (yy<in.dim.y)? xx<in.dim.x && in.board[xx][yy] :
			        xx<file_dim.x && temp_board[xx][yy-in.dim.y];
	}//endfor xx,yy
}//end Add file to existing game
}//end game

	void out(OutputStream o) throws IOException {
		OutputStream s1 = new BufferedOutputStream(o);
		DataOutputStream s = new DataOutputStream(s1);
		for(int yy = 0; yy<dim.y; yy++) {
		for(int xx = 0; xx<dim.x; xx++) {
			if(board[xx][yy]) s.writeByte('*');
			else              s.writeByte('.');
		}
		s.writeByte('\n');
		}//endfor all rows in board
		s.flush();
	}//end out

int neighbours(int x, int y) {
	int answer = 0;
	for(int i = x-1; i <= x+1; i++)
	for(int j = y-1; j <= y+1; j++) {
		if(i>=0 && i <dim.x &&
		   j>=0 && j <dim.y &&
		   !(i == x && j == y) &&
		   board[i][j])
			answer++;
	}
//	debug[x][y] = answer;
	return answer;
}//end neighbours

public void update() {
//System.err.println("game.update");
	boolean [][] nextboard = new boolean[dim.x][dim.y];
	{for(int i = 0; i < dim.x; i++)
	 for(int j = 0; j < dim.y; j++) {
		int n = neighbours(i,j);
/*		nextboard[i][j] = (n==3)? true		:
				  (n<2||n>3)? false	:
				  board[i][j];
*/
		switch(neighbours(i,j)){
		case 0: case 1: case 4: case 5: case 6: case 7: case 8:
			nextboard[i][j] = false;
			break;
		case 2:
			nextboard[i][j] = board[i][j];
			break;
		case 3:
			nextboard[i][j] = true;
			break;
		default:
			//nextboard[i][j] = 99; //bug
		}
	}}
	{for(int i = 0; i < dim.x; i++)
	 for(int j = 0; j < dim.y; j++) {
		board[i][j] = nextboard[i][j];
	}}
}//end update()

}//end class game

class date extends java.applet.Applet {
private
	Font f = new Font ("TimesRoman", Font.BOLD, 36);
	FontMetrics fm = getFontMetrics(f);
	Date theDate;
	String s;
	pair size;
public
	void update() {
		theDate = new Date();
		s = theDate.toString();
		size = new pair(fm.stringWidth(s),fm.getHeight());
	}
	date() {update();};
	void drawdate(Graphics g, int x, int y) {
		g.setFont(f);
//		g.setColor(getBackground());
		g.setColor(getForeground());
//		g.setColor(Color.blue);
		g.fillRect(x,y-size.y,size.x,size.y);
		g.setColor(Color.red);
//		g.setColor(getForeground());
		g.drawString(s,x,y);
	}
}//end class date

public class life extends java.applet.Applet implements Runnable {
	Thread runner;
	game gol;
	date TheDate = new date();
	static double init_fraction = 0.4;

static void help() {
System.err.println("-n\t\tnumber of generations");
System.err.println("-geometry nxm\tboard size");
System.err.println("file\t\tStarting configuration");
System.err.println("");
}//end help

public static void main(String args[]) throws Exception
{
System.err.println("# Life $Revision: 1.13 $ W.B.Langdon@cs.bham.ac.uk");
	game g = null;
	int a;
	int max = -1;
	pair given_size;
	for(a = 0; a < args.length; a++) {
		try {
		if(args[a].charAt(0)=='?') { a=args.length; }
		else if(args[a].charAt(0)=='-') {
			if(args[a].charAt(1)=='n' || args[a].charAt(1)=='N') {
				if(a+1<args.length) {
					max = Integer.parseInt(args[a+1]);
					a++;
				} else { a=args.length; }
			}
			else if(args[a].charAt(1)=='g'||args[a].charAt(1)=='G')
			{
				if(a+1<args.length) {
					given_size = new pair(args[a+1]);
					g=new game(g,given_size,init_fraction);
					a++;
				} else { a=args.length; }
			}
			else { a=args.length; }
		}
		else {  InputStream file;
			try {file = new FileInputStream(args[a]);}
			catch (Exception e) {
				URL url = new URL(args[a]);
				file = url.openStream();
			}//FileInputStream failed
			g = new game(g,file,0.0);
			}
		if(a==args.length)
			help();
		}//end try
		catch (Exception e) {
		if((e instanceof NumberFormatException) ||
		   (e instanceof StringIndexOutOfBoundsException) ||
		   (e instanceof IOException)||
		   (e instanceof MalformedURLException)			) {
		System.err.print("Command line Error: " + e.getMessage());
		if(a  <args.length) System.err.print(" concerning " + args[a]);
		if(a+1<args.length) System.err.print(" " + args[a+1]);
		System.err.println();
		a=args.length; 
		}
		else throw e;
		}//end catch
	}
	if(a==args.length) {
//	    System.err.print("Processed command line OK, max "+max);
//	    if(g!=null) System.err.print(" game "+g.dim.x+"x"+g.dim.y);
//	    System.err.println();

	    if(max < 0) {//run interactively
		Frame f = new Frame("Life");
		life l = new life();
		l.gol = g;
		l.init();
		f.add("Center",l);
		if(l.gol!=null) {
			Point br = point_tile(l.gol.dim.x,l.gol.dim.y);
			f.resize(br.x+10,br.y+30);//need to allow 9,29 for margins
			}
		else
			f.resize(origin.x+300,origin.y+300);
		f.show();
		l.start();
	    }
	    else {//run in batch mode
		if(g==null) {
		    System.err.println("Reading initial game from stdin");
		    g = new game(g,System.in,0.0);
		}
		for(int i=0; i<max; i++) g.update();
		g.out(System.out);
	    }//endelse batch mode
	}//endif processed command line ok
//	System.err.println("main done");
}//end main

public void start() {
	if(runner==null) {
		runner = new Thread(this);
		runner.start();
	}
}//end start()

public void stop() {
	if(runner!=null) {
		runner.stop();
		runner = null;
	}
}//end stop()

public boolean mouseEnter(Event evt, int x, int y) {
	mouse = null;
	stop();
	return true;
}//end mouseEnter

public boolean mouseExit(Event evt, int x, int y) {
	start();
	return true;
}//end mouseExit

private	pair zero = new pair(0,0);
private	pair mouse;

public boolean mouseDown(Event evt, int x, int y) {
	pair t = display_tile(x,y);
	if(!t.within(zero,gol.dim)) return false;
	gol.board[t.x][t.y] = !	gol.board[t.x][t.y];

	mouse = t;
	repaint();
	return true;
}//end mouseDown

public void run() {
	while(true) {
		TheDate.update();
		if(gol!=null) gol.update();
		repaint();
		try{ Thread.sleep(1000); }
		catch (InterruptedException e) {}
	}
}//end run()

public void update(Graphics g) {
	paint(g);
}//end update()

//private static final	pair tile = new pair(15);
private static final	pair tile = new pair(5);
private static final	Point origin = new Point(1,50);

private static pair display_tile(int x, int y) {
	return new pair((x-origin.x)/tile.x,(y-origin.y)/tile.y );
}//end display_tile

private static Point point_tile(int x, int y) {
	return new Point(origin.x+x*tile.x,origin.y+y*tile.y );
}//end point_tile

public void paint(Graphics g) {
	TheDate.drawdate(g,origin.x,origin.y);

	pair sq = new pair(tile.x-1);
//	pair dsq = new pair(8);
//	pair dd = new pair((tile.x-dsq.x)/2);

	pair screen = display_tile(size().width,size().height);
//System.err.println("paint size "+size().width+","+size().height+
//" screen "+screen.x+","+screen.y);
//	display_tile(size().width,size().height,screen);
	if(gol==null) 
		gol = new game(screen,init_fraction);
	else if(!screen.equal(gol.dim))
		gol = new game(gol,screen,init_fraction);

	for(int i = 0; i < gol.dim.x; i++)
	for(int j = 0; j < gol.dim.y; j++) {
/*		switch(gol.debug[i][j]) {
		case 0:	g.setColor(Color.white);  break;
		case 1:	g.setColor(Color.red);    break;
		case 2:	g.setColor(Color.orange); break;
		case 3:	g.setColor(Color.yellow); break;
		case 4:	g.setColor(Color.green);  break;
		case 5:	g.setColor(Color.blue);   break;
		case 6:	g.setColor(Color.magenta); break;
		case 7:	g.setColor(Color.cyan); break;
		case 8:	g.setColor(Color.pink);  break;
		default:
			g.setColor(Color.black);
		}
		g.fillRect(origin.x+i*tile.x,origin.y+j*tile.y,sq.x,sq.y);
end debug*/
		if(gol.board[i][j])
			g.setColor(Color.green);
		else
			g.setColor(Color.white);

		g.fillRect(origin.x+i*tile.x,origin.y+j*tile.y,sq.x,sq.y);
//debug		g.fillRect(origin.x+i*tile.x+dd.x,origin.y+j*tile.y+dd.y,
//debug			   dsq.x,dsq.y);

	}//endfor i,j

	if(mouse != null) {
		g.setColor(Color.red);
		{	
		Point x0 = point_tile(0,mouse.y);
		Point xT = point_tile(gol.dim.x,mouse.y);
		Point y0 = point_tile(mouse.x,0);
		Point yT = point_tile(mouse.x,gol.dim.x);
		g.drawLine(x0.x,x0.y,xT.x,xT.y);
		g.drawLine(y0.x,y0.y,yT.x,yT.y);
		}{
		Point x0 = point_tile(0,mouse.y+1);
		Point xT = point_tile(gol.dim.x,mouse.y+1);
		Point y0 = point_tile(mouse.x+1,0);
		Point yT = point_tile(mouse.x+1,gol.dim.x);
		g.drawLine(x0.x,x0.y,xT.x,xT.y);
		g.drawLine(y0.x,y0.y,yT.x,yT.y);
		}
	}
}//end paint


}//end class life
