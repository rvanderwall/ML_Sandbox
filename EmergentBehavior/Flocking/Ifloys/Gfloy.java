//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//

import java.awt.*;

public class Gfloy {

	int revdist;
	int numnb;
	int sleep;
	int margin;
	float acc;
	float acctomid;
	float maxspeed;
	float bouncespeed;
	float v0;
	float x;
	float y;
	float xtail;
	float ytail;
	float vx;
	float vy;
	int width;
	int height;
	int num;
	Gfloy neighbors[];
	Color color;
	int energy;
	int type;
	float xc;
	float yc;


	public Gfloy(String cr, int n, int w, int h, int t, int e, Color c) {

		width = w;
		height = h;
		num = n;
		type = t;
		energy = e;
		color = c;
		
		/*
		revdist = Gfloys.REVDIST;
		acc = Gfloys.ACC;
		acctomid = Gfloys.ACCTOMID;
		maxspeed = Gfloys.MAXSPEED;
		bouncespeed = Gfloys.BOUNCESPEED;
		v0 = Gfloys.V0;
		sleep = Gfloys.SLEEP;
		margin = Gfloys.MARGIN;
		numnb = Gfloys.NUMNB;
		*/

		DecodeChrom(cr);

		x = (float) Math.random()*(width-margin*2) + margin;
		y = (float) Math.random()*(height-margin*2) + margin;
		xtail = x;
		ytail = y;

		vx = (float) Math.random()*v0-v0/2;
		vy = (float) Math.random()*v0-v0/2;

		neighbors = new Gfloy[numnb];

	}


	private void DecodeChrom(String st) {

		int temp;

		revdist = (int) ((int) st.charAt(0) - 64)*10;
		acc = (float) ((int) st.charAt(1) - 64)/100;
		acctomid = (float) ((int) st.charAt(2) - 64)/100;
		maxspeed = (float) ((int) st.charAt(3) - 64)/10;
		bouncespeed = (float) ((int) st.charAt(4) - 64)/100;
		v0 = (float) ((int) st.charAt(5) - 64)/10;
		sleep = (int) st.charAt(6) - 64;
		margin = (int) st.charAt(7) - 64;
		numnb = (int) ((int) st.charAt(8) - 64)/10;
		//type = (int) ((int) st.charAt(9) - 64)/100;

		/*
		int leader =(int) (Math.random()*10);
		if (leader == 1) {
			acc = (float) (acc + 0.1);
			acctomid = (float) (acctomid + 0.1);
			maxspeed = maxspeed + 1;
			color = Color.white;
		}
		*/
	}

	private void DecodeChrom(GfloyParam params[]) {

	}

	public int dist(Gfloy ng)
	{
		int d,d1,d2;
		d1=(int)(x-ng.x);
		d2=(int)(y-ng.y);
		d=d1*d1+d2*d2;
		return(d);
	}
	

	public String GetColorName() {

		String s;

		if (color == Color.black) s = "BLACK";
		else if (color == Color.blue) s = "BLUE";
		else if (color == Color.cyan) s = "CYAN";
		else if (color == Color.darkGray) s = "DARKGRAY";
		else if (color == Color.gray) s = "GRAY";
		else if (color == Color.green) s = "GREEN";
		else if (color == Color.lightGray) s = "LIGHTGRAY";
		else if (color == Color.magenta) s = "GREEN";
		else if (color == Color.green) s = "MAGENTA";
		else if (color == Color.orange) s = "ORANGE";
		else if (color == Color.pink) s = "PINK";
		else if (color == Color.red) s = "RED";
		else if (color == Color.white) s = "WHITE";
		else if (color == Color.yellow) s = "YELLOW";
		else s = "GREEN";

		return s;

	}



	public void AssignColor(String c) {

		if (c.equals("BLACK")) color = Color.black;
		else if (c.equals("BLACK")) color = Color.black;
		else if (c.equals("BLUE")) color = Color.black;
		else if (c.equals("CYAN")) color = Color.black;
		else if (c.equals("DARKGRAY")) color = Color.black;
		else if (c.equals("GRAY")) color = Color.black;
		else if (c.equals("GREEN")) color = Color.black;
		else if (c.equals("LIGHTGRAY")) color = Color.black;
		else if (c.equals("MAGENTA")) color = Color.black;
		else if (c.equals("ORANGE")) color = Color.black;
		else if (c.equals("PINK")) color = Color.black;
		else if (c.equals("RED")) color = Color.black;
		else if (c.equals("WHITE")) color = Color.black;
		else if (c.equals("YELLOW")) color = Color.black;
		else color = Color.green;

	}


	public void GetNeighbors()
	{
		int i,j,k;
		Gfloy ng;

		for (i=0;i<numnb;i++) {
			ng=neighbors[i];;
			for (j=0;j<numnb;j++) {
				if (dist(ng.neighbors[j]) < dist(ng))
					neighbors[i]=ng.neighbors[j];
				if (ng.neighbors[j].type == 1)
					neighbors[i]=ng.neighbors[j];
			}
		}

		xc = 0;
		yc = 0;
		for (k=0;k<numnb;k++) {
			if (neighbors[k] == this) neighbors[k]=neighbors[k].neighbors[0];
			xc += neighbors[k].x;
			yc += neighbors[k].y;
		}
		xc = xc/numnb;
		yc = yc/numnb;
	}


	public void Process() {
	
		int rev;
		int i;
		int d;

		xtail = x;
		ytail = y;
		rev = -1;
		
		for (i=0;i<numnb;i++) {
			
			d = dist(neighbors[i]);
			if (d == 0)
				rev = 0;
			else if (d < revdist) {
				if (neighbors[i].type != type) {
					if (type == 1) {
						energy--;
						rev = -30;
					}
					else  {
						energy++;
						rev = 30;
					}
				}
				else
				   rev = -1;
			}
			else  {
				if (type == 1)
					rev = 0;
				else if (neighbors[i].type == 1) 
					rev = 20;
				else
					rev = 1;
			}

			if (x < neighbors[i].x)
				vx += acc*rev;
			else
				vx -= acc*rev;

			if (y < neighbors[i].y)
				vy += acc*rev;
			else
				vy -= acc*rev;
		}
	

		if (vx > maxspeed) vx = maxspeed;
		if (vx < -maxspeed) vx = -maxspeed;
		if (vy > maxspeed) vy = maxspeed;
		if (vy < -maxspeed) vy = -maxspeed;

		if (x < 0) vx = bouncespeed;
		if (x > width) vx = -bouncespeed;
		if (y < 0) vy = bouncespeed;
		if (y > height) vy = -bouncespeed;

		
		if (type == 0) {
			if (x < width/2) vx += acctomid;
			if (x > width/2) vx -= acctomid;
			if (y < height/2) vy += acctomid;
			if (y > height/2) vy -= acctomid;
		}

		x += vx;
		y += vy;
		if (energy < 1)	{
			Gfloys.joy.play();
			color = Color.green;
			type = 0;
			energy = 100;
		}
		else if (energy == 110) {
			energy++;
			color = Color.orange;
			maxspeed = maxspeed + 1;
			acc = (float) (acc + 1);
		}
		else if (energy == 120) {
			energy++;
			color = Color.red;
			maxspeed = maxspeed + 1;
			acc = (float) (acc+0.1);
		}

	}


	public void Draw(Graphics g) {

		g.setColor(color);
		g.drawLine((int) xtail, (int) ytail,(int) x,(int) y);
		g.fillOval((int) x, (int) y, 3, 3);

	}

}

