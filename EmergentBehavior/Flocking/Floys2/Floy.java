//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//

import java.awt.*;

public class Floy {

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
	Floy neighbors[];
	Color color;
	int energy;
	int type;
	float xc;
	float yc;


	public Floy(String cr, int n, int w, int h, int t, int e, Color c) {

		width = w;
		height = h;
		num = n;
		type = t;
		energy = e;
		color = c;
		
		revdist = Floys.REVDIST;
		acc = Floys.ACC;
		acctomid = Floys.ACCTOMID;
		maxspeed = Floys.MAXSPEED;
		bouncespeed = Floys.BOUNCESPEED;
		v0 = Floys.V0;
		sleep = Floys.SLEEP;
		margin = Floys.MARGIN;
		numnb = Floys.NUMNB;

		/*
		if ((cr != null) && (cr != ""))	{
			revdist = (int) cr.charAt(0) - 64;
			revdist = revdist*10;
			numnb = (int) cr.charAt(1) - 64;
			acc = (float) cr.charAt(2) - 64;
			acc = acc/10;
			acctomid = (float) cr.charAt(3) - 64;
			acctomid = acctomid/10;
			maxspeed = (float) cr.charAt(4) - 64;
			maxspeed = maxspeed/10;
			bouncespeed = (float) cr.charAt(5) - 64;
			bouncespeed = bouncespeed/10;
		}
		*/

		/*
		revdist = 200;
		acctomid = 0.1f;
		acc = 0.3f;
		maxspeed = 5f;
		bouncespeed = 0.8f;
		numnb = 2;
		*/

		x = (float) Math.random()*(width-margin*2) + margin;
		y = (float) Math.random()*(height-margin*2) + margin;
		xtail = x;
		ytail = y;

		vx = (float) Math.random()*v0-v0/2;
		vy = (float) Math.random()*v0-v0/2;

		neighbors = new Floy[numnb];

	}


	public int dist(Floy ng)
	{
		int d,d1,d2;
		d1=(int)(x-ng.x);
		d2=(int)(y-ng.y);
		d=d1*d1+d2*d2;
		return(d);
	}
	


	public void GetNeighbors()
	{
		int i,j,k;
		Floy ng;

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
					else
						rev = 30;
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
			color = Color.green;
			type = 0;
			//Floys.beep.play();
		}
		
	}


	public void Draw(Graphics g) {

		g.setColor(color);
		g.drawLine((int) xtail, (int) ytail,(int) x,(int) y);
		g.fillOval((int) x, (int) y, 3, 3);

	}

}

