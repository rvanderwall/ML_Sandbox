//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//
//  This models an individual FLoy.
//

import java.awt.*;

public class Floy {

        // Minimum distance to maintain to avoid collisions
        public static final int DEFAULT_MIN_DISTANCE = 200;
        public static int Generic_Min_Distance = DEFAULT_MIN_DISTANCE;         // Value to use when creating a Floy
        private int minDistance;        
       
        // Number of neighbors that we care about
        public static final int DEFAULT_NUM_NEIGHBORS = 2;
        public static int Generic_Num_Neighbors = DEFAULT_NUM_NEIGHBORS;       // Value to use when creating a Floy
        private int numNeigbors;

        // Margins around playing field
        public static final int DEFAULT_MARGIN = 30;
        private static int Generic_Margin = DEFAULT_MARGIN;                     // Value to use when creating a Floy
	private int margin;
        
        //
        public static final float DEFAULT_ACCELERATION =  0.3f;
        public static float Generic_Acceleration = DEFAULT_ACCELERATION;       // Value to use when creating a Floy
	private float acceleration;
        
        // How forceful the flocking draw is.
        public static final float DEFAULT_ATTRACTION_TO_CENTER = 0.05f;
        public static float Generic_Attraction_To_Center = DEFAULT_ATTRACTION_TO_CENTER; // Value to use when creating a Floy
	private float attractionToCenter;
        
        // Maximum achievable speed.  Can't accelerate past this.
        public static final float DEFAULT_MAX_SPEED = 5.0f;
        public static float Generic_Max_Speed = DEFAULT_MAX_SPEED; // Value to use when creating a Floy
	private float maxSpeed;
        
        // ??
        public static final float DEFAULT_BOUNCE_SPEED = 0.8f;
        public static float Generic_Bounce_Speed = DEFAULT_BOUNCE_SPEED; // Value to use when creating a Floy
	private float bounceSpeed;
        
        // Speed that the floy begins with
        public static final float DEFAULT_INITIAL_SPEED = 4.0f;
        public static float Generic_Initial_Speed = DEFAULT_INITIAL_SPEED;
	private float v0;

        public static final float DEFAULT_FREE_WILL = 0.05f;
        public static float Generic_Free_Will = DEFAULT_FREE_WILL;
        private float freeWill;
        
        public static final int TYPE_FRIEND = 0;
        public static final int TYPE_FOE = 1;

        // dynamic attributes
	private float x;
	private float y;
	private float vx;
	private float vy;
	private float xtail;    // Previous position needed to draw tail
	private float ytail;
        
        // Size of playing field
	private int width;
	private int height;

	public Floy neighbors[];
	public Color color;
	public int energy;
	public int type;

	public Floy(Canvas canvas, int t) {

                useGenerics();

                height = canvas.size().height;
		width = canvas.size().width;
		type = t;

                if (type == TYPE_FRIEND)
                {
                    color = Color.green;
                    energy = 200;
                    x = (float) Math.random()*(width-margin*2) + margin;
		    y = (float) Math.random()*(height-margin*2) + margin;
                }
                else
                {
                    // Foes are different and come from the outside (upper left)
                    color = Color.red;
                    energy = 100;
                    x = margin;
                    y = margin;
                }
 

		xtail = x;
		ytail = y;

		vx = (float) Math.random()*v0-v0/2;
		vy = (float) Math.random()*v0-v0/2;

		neighbors = new Floy[numNeigbors];

	}


	// Find the distance from this FLoy to another floy
	public int dist(Floy ng)
	{
		int d,d1,d2;
		d1 = (int)(x - ng.x);
		d2 = (int)(y - ng.y);
		d = d1*d1 + d2*d2;
		return(d);
	}

        public void chooseNeighbors(Floy [] floys)
        {
            int maxFloy = floys.length;
	    for (int j=0; j < numNeigbors; j++) {
		int n =(int) (Math.random()*maxFloy);
                if (floys[n] == this) {
                    // choose again, we can't be our own neighbor
                    j--;
                    continue;
                }
		neighbors[j] = floys[n];
	    }
        }


	public void GetNewNeighbors()
	{
		Floy curNeighbor;

                // If a neighbor of my neighbor is closer than the neighbor,
                // use the neighbors neighbor.
                // Also, any foe automatically is a neighbor, so I can chase him out.
		for (int i=0;i<numNeigbors;i++) {
			curNeighbor=neighbors[i];;
			for (int j=0; j<curNeighbor.numNeigbors; j++) {
				if (dist(curNeighbor.neighbors[j]) < dist(curNeighbor))
					neighbors[i]=curNeighbor.neighbors[j];
				if (curNeighbor.neighbors[j].type == TYPE_FOE)
					neighbors[i]=curNeighbor.neighbors[j];
			}
		}
	}


        // A single Time increment has occured.  Find new locations and velocities for the floy
	public void Process() {
	
		int reverse;
		int i;
		int d;

		xtail = x;
		ytail = y;
		reverse = -1;
		
                if (neighbors[0] == null)
                    return;  //We don't have neighbors yet

		for (i=0; i < numNeigbors; i++) {
			d = dist(neighbors[i]);
			if (d == 0)
				reverse = 0;
			else if (d < minDistance) {
				if (neighbors[i].type != type) {
					if (type == 1) {
						energy--;
						reverse = -30;
					}
					else
						reverse = 30;
				}
				else
				   reverse = -1;
			}
			else  {
				if (type == 1)
					reverse = 0;
				else if (neighbors[i].type == 1) 
					reverse = 20;
				else
					reverse = 1;
			}

			if (x < neighbors[i].x)
				vx += acceleration*reverse;
			else
				vx -= acceleration*reverse;

			if (y < neighbors[i].y)
				vy += acceleration*reverse;
			else
				vy -= acceleration*reverse;
		}
	

		if (vx > maxSpeed)  vx = maxSpeed;
		if (vx < -maxSpeed) vx = -maxSpeed;
		if (vy > maxSpeed)  vy = maxSpeed;
		if (vy < -maxSpeed) vy = -maxSpeed;

		if (x < margin)        vx = bounceSpeed;
		if (x > width-margin)  vx = -bounceSpeed;
		if (y < margin)        vy = bounceSpeed;
		if (y > height-margin) vy = -bounceSpeed;
		
		if (type == 0) {
			if (x < width/2) vx += attractionToCenter;
			if (x > width/2) vx -= attractionToCenter;
			if (y < height/2) vy += attractionToCenter;
			if (y > height/2) vy -= attractionToCenter;
		}

		x += vx;
		y += vy;
		if (energy < 1)	{
			color = Color.green;
			type = 0;
		}
	}


        //Draw a floy with a tail
	public void Draw(Graphics g) {
		g.setColor(color);
		g.drawLine((int) xtail, (int) ytail,(int) x,(int) y);
		g.fillOval((int) x, (int) y, 3, 3);

	}

        private void useGenerics() {
            this.minDistance = Generic_Min_Distance;
            this.numNeigbors = Generic_Num_Neighbors;
            this.margin      = Generic_Margin;
            this.acceleration = Generic_Acceleration;
            this.attractionToCenter = Generic_Attraction_To_Center;
            this.maxSpeed    = Generic_Max_Speed;
            this.bounceSpeed = Generic_Bounce_Speed;
            this.v0          = Generic_Initial_Speed;
            this.freeWill    = Generic_Free_Will;
        }
        
        
       	static public void resetToDefaults() {
            Generic_Min_Distance   = DEFAULT_MIN_DISTANCE;
            Generic_Num_Neighbors  = DEFAULT_NUM_NEIGHBORS;
            Generic_Margin         = DEFAULT_MARGIN;
            Generic_Acceleration   = DEFAULT_ACCELERATION;
            Generic_Attraction_To_Center = DEFAULT_ATTRACTION_TO_CENTER;
            Generic_Max_Speed      = DEFAULT_MAX_SPEED;
            Generic_Bounce_Speed = DEFAULT_BOUNCE_SPEED;
            Generic_Initial_Speed  = DEFAULT_INITIAL_SPEED;
            Generic_Free_Will      = DEFAULT_FREE_WILL;
	}
}

